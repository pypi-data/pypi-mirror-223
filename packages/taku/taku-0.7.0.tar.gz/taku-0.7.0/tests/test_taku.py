from pathlib import Path
from typing import List, Optional
import taku
import shutil
from taku import Task, Pipeline, setup_logger
from taku.task import JobData, JobName, JobSpecs, TaskName


class TaskA(Task):
    def __init__(self, name: TaskName, save_dir: str) -> None:
        super().__init__(name, {}, meta_override_dir=Path(save_dir))

    def gather_jobs(self, upstream_job_names: List[JobName]) -> List[JobSpecs]:
        return [JobSpecs('A1'), JobSpecs('A2')]
    
    def run(self, job_name, job_data, upstream_job_names, upstream_job_data):
        taku.logger.info(f"TaskA {job_name} is running, {upstream_job_names}, {upstream_job_data}")
        return job_name



class TaskB(Task):
    def __init__(self, name: TaskName, save_dir: str) -> None:
        super().__init__(name, {}, meta_override_dir=Path(save_dir))

    def gather_jobs(self, upstream_job_names: List[JobName]) -> List[JobSpecs]:
        taku.logger.info(f"Gathering jobs for {self.name}, upstream = {upstream_job_names}")
        specs = [[JobSpecs(f"{self.name}1-{jn}", {}, [jn]), JobSpecs(f"{self.name}2-{jn}", {}, [jn])] 
                 for jn in upstream_job_names]
        specs = sum(specs, [])
        taku.logger.info(f"New jobs {specs}")
        return specs
    
    def run(self, job_name, job_data, upstream_job_names, upstream_job_data):
        taku.logger.info(f"TaskB {job_name} is running, {upstream_job_names}, {upstream_job_data}")
        assert len(upstream_job_data) == 1
        return f"{job_name}({upstream_job_data[0]})"


class TaskC(Task):
    def __init__(self, name: TaskName, save_dir: str) -> None:
        super().__init__(name, {}, meta_override_dir=Path(save_dir))

    def gather_jobs(self, upstream_job_names: List[JobName]) -> List[JobSpecs]:
        taku.logger.info(f"Gathering jobs for {self.name}, upstream = {upstream_job_names}")
        return [JobSpecs(f"{self.name}-[{'+'.join(upstream_job_names)}]", {}, upstream_job_names)]
    
    def run(self, job_name, job_data, upstream_job_names, upstream_job_data):
        taku.logger.info(f"TaskC {job_name} is running, {upstream_job_names}, {upstream_job_data}")
        return f"Gathered"


if __name__ == "__main__":
    base_dir = Path('test_taku')
    shutil.rmtree(base_dir, ignore_errors=True)
    base_dir.mkdir(exist_ok=True)

    exectuor = taku.MultiprocessingExecutor(num_workers=2)

    setup_logger()
    pipeline = Pipeline([
        TaskA('A', base_dir / "a"), TaskB("B", base_dir / "b/"), TaskB("C", base_dir / "c/"), TaskC("D", base_dir / "d/") # type: ignore
    ])
    res = pipeline.run_per_job(saving_tasks=['B', 'A'], need_output=True, force_rerun_tasks=['A'], executor=exectuor)
    print(res)

    pipeline = Pipeline([
        TaskA('A', base_dir / "a"), TaskB("B", base_dir / "b/"), TaskB("C", base_dir / "c/") # type: ignore
    ])
    res = pipeline.run_per_job(saving_tasks=[], need_output=True, force_rerun_tasks=['A', 'C'], executor=exectuor)
    print(res)

    shutil.rmtree(base_dir, ignore_errors=True)

    pipeline = Pipeline([
        TaskA('A', base_dir / "a"), TaskB("B", base_dir / "b/"), TaskB("C", base_dir / "c/"), TaskC("D", base_dir / "d/") # type: ignore
    ])
    res = pipeline.run_per_task(saving_tasks=['B', 'A', 'C'], need_output=True, force_rerun_tasks=['A'], executor=exectuor)
    print(res)

    pipeline = Pipeline([
        TaskB("C", base_dir / "c/"), TaskC("D", base_dir / "d/") # type: ignore
    ])
    res = pipeline.run_per_task(saving_tasks=['D'], need_output=True, executor=exectuor)
    print(res)

    shutil.rmtree(base_dir, ignore_errors=True)

    pipeline = Pipeline([
        TaskA('A', base_dir / "a"), TaskB("B", base_dir / "b/") # type: ignore
    ])
    dataset = pipeline.torch_dataset()
    from torch.utils.data import DataLoader
    dataloader = DataLoader(dataset, batch_size=2, num_workers=2)
    for batch in dataloader:
        print(batch)

    shutil.rmtree(base_dir, ignore_errors=True)
