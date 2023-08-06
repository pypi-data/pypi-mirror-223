import copy
import json
import pickle

import taku
import omegaconf

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


# Typehints to clarify the meaning of the data
TaskName = str
JobName = str
JobData = Any


@dataclass
class JobSpecs:
    # Name of the job
    job_name: JobName
    # Input of the job (from user specifications)
    job_in_data: JobData = None
    # Input of the job (from the output of upstream job)
    job_dependencies: List[JobName] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.job_name)



class Task(ABC):
    """ Don't store too much data in the task, as it will be pickled and sent to the workers. """

    default_meta = {'status': 'not-saved'}

    def __init__(self, name: TaskName, hparams: Any, meta_override_dir: Optional[Path] = None) -> None:
        super().__init__()
        self.name = name
        self._meta_dir: Optional[Path] = None
        self._meta_override_dir = meta_override_dir
        self._hparams = omegaconf.OmegaConf.create(hparams)

    @abstractmethod
    def gather_jobs(self, upstream_job_names: List[JobName]) -> List[JobSpecs]:
        """This has full knowledge of all the jobs in the previous stage"""
        pass

    @abstractmethod
    def run(self, job_name: JobName, job_data: JobData, 
            upstream_job_names: List[str], upstream_job_data: List[JobData]) -> JobData:
        """Run the task."""
        pass

    def gather_finished_jobs(self) -> List[JobName]:
        """Gather the names of finished jobs, used to fake a finished state."""
        raise NotImplementedError

    @property
    def meta_dir(self) -> Optional[Path]:
        if self._meta_override_dir is not None:
            return self._meta_override_dir
        return self._meta_dir

    @property
    def saved_meta(self) -> Dict:
        if self.meta_dir is None:
            return copy.copy(self.default_meta)
        meta_path = self.meta_dir / 'taku.json'
        if not meta_path.exists():
            return copy.copy(self.default_meta)
        with meta_path.open('r') as f:
            meta = json.load(f)
        return meta
    
    @property
    def hparams(self) -> omegaconf.DictConfig:
        assert isinstance(self._hparams, omegaconf.DictConfig)
        return self._hparams

    def check_hparams(self) -> bool:
        saved_hparams = self.saved_meta.get('hparams', {})
        if len(saved_hparams) == 0:
            return True
        
        param_match = True
        for k, v in saved_hparams.items():
            if k not in self._hparams:
                taku.logger.warning(f"Parameter {k} is missing in the provided arguments.")
                param_match = False

            if self._hparams[k] != v:
                taku.logger.warning(f"Parameter {k} is different from the saved value "
                                       f"{self._hparams[k]} vs {saved_hparams[k]}.")
                param_match = False

        for k, v in self._hparams.items():
            if k not in saved_hparams:
                taku.logger.warning(f"Parameter {k} is new in the provided arguments.")
                param_match = False
            
        return param_match
    
    def save_meta(self, all_jobs: Optional[List[JobName]] = None, status: str = 'done') -> None:
        """Save the meta information of the task."""
        assert self.meta_dir is not None, "Save directory is not specified"

        if all_jobs is None:
            all_jobs = self.saved_meta.get('all_jobs', [])

        meta_path = self.meta_dir / 'taku.json'
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        with meta_path.open('w') as f:
            json.dump({
                'status': status,
                'all_jobs': all_jobs,
                'hparams': omegaconf.OmegaConf.to_container(self._hparams)
            }, f, indent=4)

    def has_job_data(self, job_name: str) -> bool:
        """Check if the output of the task is cached."""
        if self.meta_dir is None:
            return False
        return (self.meta_dir / f'{job_name}.pkl').exists()

    def save_job_data(self, job_name: str, job_data: JobData) -> None:
        """Save the output of the task."""
        assert self.meta_dir is not None, "Save directory is not specified"
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        with (self.meta_dir / f'{job_name}.pkl').open('wb') as f:
            pickle.dump(job_data, f)

    def load_job_data(self, job_name: str) -> JobData:
        """Load the output of the task."""
        assert self.meta_dir is not None, "Save directory is not specified"
        with (self.meta_dir / f'{job_name}.pkl').open('rb') as f:
            job_data = pickle.load(f)
        return job_data
