import random
from typing import Callable, List, Tuple
import torch.utils.data as data
from taku.pipeline import JobGeneration, Pipeline
from taku import logger


class SkipItem(Exception):
    pass


class Dataset(data.Dataset):
    """Dataset class."""

    def __init__(self, job_func: Callable, job_generations: List[JobGeneration], skip_on_error: bool = False):
        self.job_func = job_func
        self.job_generations = job_generations
        self.skip_on_error = skip_on_error

    def __len__(self):
        return len(self.job_generations)

    def __getitem__(self, index):
        if self.skip_on_error:
            try:
                return self.job_func(self.job_generations[index])
            except SkipItem:
                return self[random.randint(0, len(self) - 1)]
            except Exception:
                # Just return a random other item.
                logger.warning(f"Tasklib dataset: get item {index} error, but handled.")
                return self[random.randint(0, len(self) - 1)]
        else:
            try:
                return self.job_func(self.job_generations[index])
            except SkipItem:
                return self[random.randint(0, len(self) - 1)]
