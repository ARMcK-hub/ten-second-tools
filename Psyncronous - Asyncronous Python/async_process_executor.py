from concurrent.futures import Executor
from concurrent.futures.process import ProcessPoolExecutor

from.async_pool_executor import AsyncPoolExecutor

class AsyncProcessExecutor(AsyncPoolExecutor):
  """
  AsyncProcessExecutor is a mutli-process executor.
  The job's executable, completed by the execution pool, runs by looping through its associated queue until the queue is empty.
  Implementation should be used for CPU intensive tasks. 
  Async processes DO NOT share a data space.
  """

  def _get_pool_executor(self) -> Executor:
    return ProcessPoolExecutor