from concurrent.futures import Executor
from concurrent.futures.thread import ThreadPoolExecutor

from .async_pool_executor import AsyncPoolExecutor


class AsyncThreadedExecutor(AsyncPoolExecutor):
    """
    AsyncThreadedExecutor is a multi-threaded executor.
    The job's executable, completed by the execution pool, runs by looping through its associated queue until the queue is empty.
    Implementation should be used for I/O intensive tasks.
    Async threads DO share a data space, so a lock must be used in the executable when interacting with global variables.
    """

    def _get_pool_executor(self) -> Executor:
        return ThreadPoolExecutor
