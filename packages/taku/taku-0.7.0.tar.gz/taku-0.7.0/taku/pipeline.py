import copy
from typing import List, Dict, Optional, Tuple, TypeVar
import taku
import taku.task as task
import taku.executors as executors
from pathlib import Path
from functools import partial


JobGeneration = List[List[task.JobSpecs]]
TaskSubclass = TypeVar("TaskSubclass", bound=task.Task)


class Pipeline:
    def __init__(self, tasks: List[TaskSubclass], meta_dir: Path = Path("/tmp/taku")) -> None:
        self.tasks = tasks
        self.meta_dir = meta_dir

        for t in self.tasks:
            t._meta_dir = self.meta_dir / t.name
            t.check_hparams()

        self._fake_task_meta = {}

    @property
    def is_clean(self) -> bool:
        return len(self._fake_task_meta) == 0

    def fake_task_done(self, task_name: str) -> None:
        """ Fake a task as done. """
        task = [t for t in self.tasks if t.name == task_name][0]
        if task.saved_meta['status'] == 'done':
            taku.logger.warning(f"Task {task_name} is already done, no need to fake it.")
            return
        fake_meta = copy.copy(task.saved_meta)
        fake_meta['status'] = 'done'
        taku.logger.warning(
            f"Fake task {task_name} as done. This will offend the pipeline integrity, hence it will be marked unclean."
            f"This usually means that task meta-data will not be saved anymore.")
        taku.logger.info("Gathering finished jobs in the task...")
        fake_meta['all_jobs'] = task.gather_finished_jobs()
        self._fake_task_meta[task_name] = fake_meta

    def get_task_meta(self, task: taku.Task) -> Dict:
        """ Get the meta data of a task. """
        if task.name in self._fake_task_meta:
            return self._fake_task_meta[task.name]
        return task.saved_meta

    def torch_dataset(self,
                      force_rerun_tasks: Optional[List[str]] = None,
                      skip_on_error: bool = False):
        """ Return a torch dataset """
        force_rerun_tasks = force_rerun_tasks or []

        # Determine the run paths
        run_paths = self._determine_run_paths([], force_rerun_tasks, True)
        assert len(run_paths) == 1, "torch_dataset can only be called on a single run path"

        start_idx, end_idx = run_paths[0][0], run_paths[0][-1]

        job_generations, job_specs, pivot_task = \
            self._gather_per_job_generations(start_idx, end_idx)
        
        # Late import to avoid direct torch dependency
        from .dataset import Dataset

        gen_func = partial(self._run_per_job_thread, 
                           all_tasks=[pivot_task] + self.tasks[start_idx:end_idx + 1],
                           saving_tasks=[], 
                           force_rerun_tasks=force_rerun_tasks, 
                           need_output=True)
        return Dataset(gen_func, job_generations, skip_on_error)

    def _sanitize_task_names(self, task_names: List[str]) -> List[str]:
        all_task_names = [t.name for t in self.tasks]
        existed_tasks = [t for t in task_names if t in all_task_names]
        if len(existed_tasks) != len(task_names):
            non_existed_tasks = [t for t in task_names if t not in all_task_names]
            taku.logger.warning(f"Task names {non_existed_tasks} are not found in the pipeline, ignored.")
        return existed_tasks

    def _determine_run_paths(self, 
                             saving_tasks: List[str], 
                             force_rerun_tasks: List[str],
                             need_output: bool,
                             split_save: bool = False) -> List[List[int]]:
        """Determine the run paths, which are continuous segments on the pipeline."""

        all_task_names = [t.name for t in self.tasks]
        
        # Determine the run paths
        run_path_starting_tasks = [all_task_names.index(t) for t in saving_tasks] + \
            [all_task_names.index(t) for t in force_rerun_tasks]
        if need_output:
            run_path_starting_tasks.append(len(self.tasks) - 1)
        run_path_starting_tasks = sorted(list(set(run_path_starting_tasks)), reverse=True)

        task_mask = [False] * len(self.tasks)
        for tidx in run_path_starting_tasks:
            for pidx in range(tidx, -1, -1):
                # This may not be accurate (because sometimes status is not saved), 
                # but during job execution this will be skipped.
                if self.get_task_meta(self.tasks[pidx])['status'] == 'done' and \
                        all_task_names[pidx] not in force_rerun_tasks:
                    break
                task_mask[pidx] = True
        if need_output:
            task_mask[-1] = True

        # Find continuous segments on task_mask with True value
        run_paths = []
        for pidx in range(len(task_mask)):
            if task_mask[pidx]:
                if len(run_paths) == 0 or run_paths[-1][-1] != pidx - 1:
                    run_paths.append([pidx])
                else:
                    run_paths[-1].append(pidx)

        # In split save mode, each run path will be split into multiple paths, each ending with a saving task
        #   This would possibly optimize task schedule to avoid duplicates, with the additional cost of
        #   re-loading previous generated results from disk.
        if split_save:
            new_run_paths = []
            for run_path in run_paths:
                if len(new_run_paths) == 0 or len(new_run_paths[-1]) > 0:
                    new_run_paths.append([])
                for r in run_path:
                    new_run_paths[-1].append(r)
                    if all_task_names[r] in saving_tasks:
                        new_run_paths.append([])
            if len(new_run_paths) > 0 and len(new_run_paths[-1]) == 0:
                new_run_paths.pop()
            run_paths = new_run_paths

        taku.logger.info(f"Found {len(run_paths)} run paths: {run_paths}")

        return run_paths
    
    def _gather_per_job_generations(self, start_idx: int, end_idx: int) -> \
        Tuple[List[JobGeneration], Dict[int, List[task.JobSpecs]], Optional[task.Task]]:
        # Output value: list of per-job generations, each job is a generation, each generation is a list of (upstream) jobs

        if start_idx == 0:
            pivot_task = None
            start_job_names = []
        else:
            # Fake input jobs
            pivot_task = self.tasks[start_idx - 1]
            start_job_names = [
                task.JobSpecs(job_name, {}, []) 
                for job_name in self.get_task_meta(self.tasks[start_idx - 1])['all_jobs']
            ]

        job_specs = {start_idx - 1: start_job_names}

        for idx in range(start_idx, end_idx + 1):
            t = self.tasks[idx]
            # Force gather_jobs!
            job_specs[idx] = t.gather_jobs([t.job_name for t in job_specs[idx - 1]])

        # Split jobs into generations
        job_inv_specs = {
            idx: {job_spec.job_name: i for i, job_spec in enumerate(job_specs[idx])}
            for idx in job_specs.keys()
        }

        def probe(job_spec, idx):
            if idx - 1 not in job_inv_specs:
                return [[job_spec]]
            elif idx == 0:
                # For job with no dep, return empty list
                return [[], [job_spec]]
            
            sub_generation = []

            assert len(job_spec.job_dependencies) > 0, "There's one job with no dependency!"
            for dep_name in job_spec.job_dependencies:
                dep_spec_idx = job_inv_specs[idx - 1][dep_name]
                dep_spec = job_specs[idx - 1][dep_spec_idx]
                sub_generation.append(probe(dep_spec, idx - 1))

            # Dedup to avoid duplicated parent jobs
            sub_generation = [list(set(sum(g, []))) for g in zip(*sub_generation)]  # type: ignore

            return sub_generation + [[job_spec]]
        
        job_generations = [probe(final_spec, end_idx) for final_spec in job_specs[end_idx]]
        return job_generations, job_specs, pivot_task

    def run_per_task(self,
                     saving_tasks: Optional[List[str]] = None, 
                     force_rerun_tasks: Optional[List[str]] = None,
                     need_output: bool = False,
                     executor: executors.BaseExecutor = executors.MultiprocessingExecutor(num_workers=0)):
        """
        Run the pipeline using per-task strategy. The logic is as follows:
            1. Directly assemble tasks into generations.
            2. Run each generation in parallel and grab the result.
        Note that this will ALWAYS hold intermediate results in memory -- use run_per_job to avoid this.
        """
        saving_tasks = saving_tasks or []
        saving_tasks = self._sanitize_task_names(saving_tasks)
        force_rerun_tasks = force_rerun_tasks or []
        force_rerun_tasks = self._sanitize_task_names(force_rerun_tasks)

        # Determine the run paths
        run_paths = self._determine_run_paths(saving_tasks, force_rerun_tasks, need_output)

        # For each run path, gather jobs and run them
        for run_path in run_paths:
            # Inclusive, (start_idx-1) is guaranteed to has jobs
            start_idx, end_idx = run_path[0], run_path[-1]

            if start_idx == 0:
                job_specs = []
                pivot_task = None
                pivot_task_completed = True
            else:
                pivot_task = self.tasks[start_idx - 1]
                job_specs = [
                    task.JobSpecs(job_name, {}, []) 
                    for job_name in self.get_task_meta(pivot_task)['all_jobs']
                ]
                pivot_task_completed = self.get_task_meta(pivot_task)['status'] == 'done'

            gen_res = {}
            for idx, tsk in enumerate([pivot_task] + self.tasks[start_idx:end_idx + 1]):
                
                if idx > 0:
                    assert tsk is not None
                    job_specs = tsk.gather_jobs([j.job_name for j in job_specs])

                if tsk is None:
                    continue

                taku.logger.info(f"Running task {tsk.name}...")

                # Run the job
                output_needed = idx < end_idx - start_idx + 1 or (need_output and end_idx == len(self.tasks) - 1)

                # Filter upstream job data based on job_specs dependency (this saves partial's memory)
                upstream_job_data = [{k: gen_res[k] for k in job_spec.job_dependencies} for job_spec in job_specs]

                if tsk.name in saving_tasks and self.is_clean:
                    tsk.save_meta(None, 'attempted')

                raw_res, raw_run_info = executor.run(self._run_per_task_thread, (job_specs, upstream_job_data),
                                                    (tsk, 
                                                    tsk.name in saving_tasks if tsk is not None else False, 
                                                    tsk.name in force_rerun_tasks if tsk is not None else False,
                                                    output_needed))
                
                # Continue with only successful jobs
                success_job_res = [(j, res) for (j, r, res) in zip(job_specs, raw_run_info, raw_res) if r.success]
                gen_res = {k.job_name: v for k, v in success_job_res}

                # ... save completed jobs for consistency
                is_success = len(success_job_res) == len(job_specs) and pivot_task_completed
                if tsk.name in saving_tasks and self.is_clean:
                    tsk.save_meta([j.job_name for j, _ in success_job_res], 'done' if is_success else 'attempted')
            
            if need_output:
                return [gen_res.get(job_spec.job_name, None) for job_spec in job_specs]


    def run_per_job(self,
                    saving_tasks: Optional[List[str]] = None, 
                    force_rerun_tasks: Optional[List[str]] = None,
                    need_output: bool = False,
                    split_save: bool = False,
                    executor: executors.BaseExecutor = executors.MultiprocessingExecutor(num_workers=0)):
        """
        Run the pipeline using per-job strategy. The logic is as follows:
            1. Determine run paths, which are continuous segments on the pipeline.
            2. For each run path, gather jobs and assemble them into generations (one generation per task).
            3. Run the jobs in parallel.
        If a job in a task is dependent on multiple jobs in the previous task, then those jobs might be cached multiple times.
        """
        saving_tasks = saving_tasks or []
        saving_tasks = self._sanitize_task_names(saving_tasks)
        force_rerun_tasks = force_rerun_tasks or []
        force_rerun_tasks = self._sanitize_task_names(force_rerun_tasks)

        # Determine the run paths
        run_paths = self._determine_run_paths(saving_tasks, force_rerun_tasks, need_output, split_save=split_save)

        # For each run path, gather jobs and run them
        res = None
        for run_path in run_paths:
            # Inclusive, (start_idx-1) is guaranteed to has jobs
            start_idx, end_idx = run_path[0], run_path[-1]

            job_generations, job_specs, pivot_task = self._gather_per_job_generations(start_idx, end_idx)
            pivot_task_completed = pivot_task is None or self.get_task_meta(pivot_task)['status'] == 'done'

            for idx in range(start_idx, end_idx + 1):
                if self.tasks[idx].name in saving_tasks and self.is_clean:
                    # Mark attempted but does not touch job-list (for convenience)
                    self.tasks[idx].save_meta(None, 'attempted')

            # Run jobs in parallel
            res, run_info = executor.run(self._run_per_job_thread, 
                                        (job_generations, ),
                                        ([pivot_task] + self.tasks[start_idx:end_idx + 1], 
                                        saving_tasks, 
                                        force_rerun_tasks, 
                                        need_output and end_idx == len(self.tasks) - 1))
            
            # Gather finished jobs for each generation
            if self.is_clean:
                for tidx, idx in enumerate(range(start_idx, end_idx + 1)):
                    if self.tasks[idx].name in saving_tasks:
                        # If the job generation is successful, then all sub-jobs should be completed.
                        completed_jobs = sum([jg[tidx + 1] for ri, jg in zip(run_info, job_generations) if ri.success], [])
                        completed_jobs = list(set(completed_jobs))
                        # Re-sort to align with the original job_specs
                        js_indexer = {j.job_name: i for i, j in enumerate(job_specs[idx])}
                        completed_jobs = sorted(completed_jobs, key=lambda j: js_indexer[j.job_name])
                        is_success = len(completed_jobs) == len(job_specs[idx]) and pivot_task_completed
                        self.tasks[idx].save_meta([j.job_name for j in completed_jobs], 'done' if is_success else 'attempted')

        return res

    @staticmethod
    def _run_per_task_thread(job_spec: task.JobSpecs,
                             upstream_job_data: Dict[str, task.JobData],
                             task: task.Task,
                             save: bool,
                             force_rerun: bool,
                             need_output: bool,
                             override_has_job_data: Optional[bool] = None):
        assert task is not None

        has_job_data = override_has_job_data if override_has_job_data is not None \
                       else task.has_job_data(job_spec.job_name)

        if has_job_data and not force_rerun:

            if need_output:
                run_output = task.load_job_data(job_spec.job_name)

            else:
                run_output = None

        else:
            run_output = task.run(job_spec.job_name, job_spec.job_in_data, 
                                  job_spec.job_dependencies, 
                                  [upstream_job_data[jn] for jn in job_spec.job_dependencies])
            if save:
                task.save_job_data(job_spec.job_name, run_output)

        if need_output:
            return run_output

    @staticmethod
    def _run_per_job_thread(job_generation: JobGeneration, 
                            all_tasks: List[Optional[TaskSubclass]], 
                            saving_tasks: List[str],
                            force_rerun_tasks: List[str],
                            need_output: bool):

        assert len(job_generation) == len(all_tasks)

        # First do a pass to check what jobs are completed 
        # (to avoid loading unnecessary data that are not used for subsequent jobs)
        completed_jobs = set()
        for tidx, (task, job_gen) in enumerate(zip(all_tasks, job_generation)):
            if task is None:
                continue
            for job_spec in job_gen:
                if task.has_job_data(job_spec.job_name):
                    completed_jobs.add(job_spec.job_name)

        # Then run the actual jobs
        last_job_data = {}
        for tidx, (task, job_gen) in enumerate(zip(all_tasks, job_generation)):
            if task is None:
                continue

            cur_job_data = {}
            for job_spec in job_gen:

                # Figure out whether output is needed:
                #   1. If all jobs dependent on this job are completed, then output is not needed.
                #   2. If this is the last task and need_output is True, then output is needed.

                if tidx < len(all_tasks) - 1:
                    job_need_output = any([j.job_name not in completed_jobs 
                                        for j in job_generation[tidx + 1] 
                                        if job_spec.job_name in j.job_dependencies])
                else:
                    job_need_output = need_output

                run_output = Pipeline._run_per_task_thread(job_spec, last_job_data, task,
                                                           task.name in saving_tasks,
                                                           task.name in force_rerun_tasks,
                                                           job_need_output,
                                                           override_has_job_data=job_spec.job_name in completed_jobs)
                cur_job_data[job_spec.job_name] = run_output
            last_job_data = cur_job_data

        if need_output:
            assert len(last_job_data) == 1
            return last_job_data.__iter__().__next__()

        return None
