import logging
from rich.logging import RichHandler

from .task import Task, JobSpecs, JobData, JobName, TaskName
from .pipeline import Pipeline
from .executors import BaseExecutor, MultiprocessingExecutor, SequentialExecutor, RayExecutor

logger = logging.getLogger('taku')

__version__ = '0.7.0'

def setup_logger():
    logger.addHandler(RichHandler(
        markup=True, rich_tracebacks=True, log_time_format="[%m-%d %H:%M:%S]"))
    logger.setLevel(logging.INFO)
