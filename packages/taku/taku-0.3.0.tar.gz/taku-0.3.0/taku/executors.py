import os
import time
import multiprocessing

from abc import ABC, abstractmethod
from typing import Tuple, Callable, List, Optional, Any, Union

import itertools
from tqdm import tqdm
import taku

from dataclasses import dataclass


@dataclass
class RunInfo:
    success: bool = True
    exit_code: int = 0
    exception: Optional[Exception] = None


class BaseExecutor(ABC):
    @abstractmethod
    def run(self, func: Callable, full_args: Tuple, partial_args: Tuple) -> Tuple[List, List[RunInfo]]:
        pass

    def pack_args(self, full_args: Tuple, partial_args: Tuple):
        assert len(full_args) > 0, "Must provide at least one full argument to run"

        num_jobs = len(full_args[0])

        expanded_args = []
        for arg in full_args:
            assert len(arg) == num_jobs
            expanded_args.append(arg)

        for arg in partial_args:
            expanded_args.append(itertools.repeat(arg, num_jobs))

        return num_jobs, expanded_args


class SequentialExecutor(BaseExecutor):
    def run(self, func, full_args, partial_args):
        num_jobs, expanded_args = self.pack_args(full_args, partial_args)

        results, run_info = [], []
        for idx, arg in tqdm(enumerate(zip(*expanded_args)), total=num_jobs):
            results.append(func(*arg))
            run_info.append(RunInfo())
        return results, run_info


class MultiprocessingExecutor(BaseExecutor):
    
    def __init__(self, num_workers: int, method: Optional[str] = None) -> None:
        self.num_workers = num_workers
        self.method = method

    @staticmethod
    def _func_wrapper(func, results_list, idx, args):
        try:
            results_list[idx] = func(*args)
        except Exception as e:
            taku.logger.warning(f"MultiprocessingExecutor: Exception in job {idx}: {e}")
            results_list[idx] = e

    @staticmethod
    def _wait_for_process_slot(
        processes: dict, concurrency: int
    ) -> int:
        counter = 0
        while True:
            counter = sum([1 for i, p in processes.items() if p.is_alive()])
            if counter < concurrency:
                return counter
            time.sleep(0.01)

    def run(self, func, full_args, partial_args):
        
        if self.num_workers == 0:
            taku.logger.info(f"MultiprocessingExecutor: Running in serial mode.")
            return SequentialExecutor().run(func, full_args, partial_args)

        num_jobs, expanded_args = self.pack_args(full_args, partial_args)

        ctx = multiprocessing.get_context(method=self.method)
        manager = ctx.Manager()
        results_list = manager.list([None] * num_jobs)

        all_processes = {}
        for idx, arg in tqdm(enumerate(zip(*expanded_args)), total=num_jobs, desc="mp-jobs"):
            self._wait_for_process_slot(all_processes, self.num_workers)

            p = ctx.Process(target=self._func_wrapper, args=(func, results_list, idx, arg), daemon=True) # type: ignore
            all_processes.update({idx: p})
            p.start()

        for p in all_processes.values():
            p.join()

        # Obtain results
        results, run_info = [], []
        for idx, r in enumerate(results_list):
            exit_code = all_processes[idx].exitcode
            if isinstance(r, Exception):
                run_info.append(RunInfo(success=False, exit_code=exit_code, exception=r))
                results.append(None)
            else:
                run_info.append(RunInfo(success=exit_code == 0, exit_code=exit_code))
                results.append(r)

        num_bad = len([r for r in run_info if not r.success])
        num_exceptions = len([r for r in run_info if r.exception is not None])
        taku.logger.info(f"MultiprocessingExecutor: Total jobs = {num_jobs}, of which "
                            f"{num_bad} jobs failed with {num_exceptions} exceptions.")

        return results, run_info


class RayExecutor(BaseExecutor):
    def __init__(self, cpus_per_task: Optional[Union[int, float]] = None, gpus_per_task: Optional[Union[int, float]] = None) -> None:
        super().__init__()
        self.cpus_per_task = cpus_per_task
        self.gpus_per_task = gpus_per_task

    @staticmethod
    def _run_with_cwd(func, args, cwd: str, array_index: int):
        os.chdir(cwd)
        return (func(*args), array_index)

    def run(self, func: Callable[..., Any], full_args: Tuple, partial_args: Tuple):
        import ray
        import psutil
        from ray.exceptions import RayTaskError

        num_jobs, expanded_args = self.pack_args(full_args, partial_args)

        try:
            import os
            ray.init(runtime_env={"working_dir": os.getcwd()})
        except ConnectionError as e:
            taku.logger.warning(f"RayExecutor: ConnectionError: {e}, "
                                   f"Use 'ray start --head --num-gpus xxx' to start a ray cluster.")
            raise

        remote_func = ray.remote(
            num_cpus=self.cpus_per_task or psutil.cpu_count(),
            num_gpus=self.gpus_per_task or 0
        )(self._run_with_cwd)

        jobs = [remote_func.remote(func, arg, os.getcwd(), job_id) for job_id, arg in enumerate(zip(*expanded_args))]
        prog_bar = tqdm(total=num_jobs, desc="ray-jobs")
        results = [None for _ in range(num_jobs)]
        run_info = [RunInfo(success=False) for _ in range(num_jobs)]

        while len(jobs): 
            done_id, jobs = ray.wait(jobs)
            prog_bar.update(len(done_id))

            for obj_ref in done_id:
                try:
                    task_res, arr_idx = ray.get(obj_ref)
                    results[arr_idx] = task_res
                    run_info[arr_idx] = RunInfo()
                except (RayTaskError, Exception) as e:
                    taku.logger.warning(f"RayExecutor: Exception in job {e}")

        prog_bar.close()

        return results, run_info
