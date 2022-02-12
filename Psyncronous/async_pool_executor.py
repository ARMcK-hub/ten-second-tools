import os
from typing import Optional, Callable, List
from abc import ABC, abstractmethod
from concurrent.futures import Executor
from queue import Queue, Empty
from datetime import datetime

from .async_job import AsyncJob


class AsyncPoolExecutor(ABC):
  """
  AsyncPoolExecutor is an abstract pool execution object that runs an AsyncJob. 
  The job's executable, completed by the execution pool, runs by looping through its associated queue until the queue is empty.
  
  NOTE: an executable should not contain within itself reference to an AsyncPoolExecutor, or deadlock will occur.
  """
  job_list: List[AsyncJob] = []
  
  def __init__(self, num_workers: int = os.cpu_count(), silent: Optional[bool] = True) -> None:
    self.num_workers = num_workers
    self.silent = silent

  @abstractmethod
  def _get_pool_executor(self) -> Executor:
    # factory method used to identify the type of pool executor
    raise NotImplementedError

  def execute(self, job: AsyncJob) -> None:
    # executes an AsyncJob using a queued process loop
    self.job_list.append(job)
    job.start_time = datetime.now()
    
    if not self.silent:
      print(f"Job ({job.id}) Start Time: {job.start_time}")
    
    pool_executor = self._get_pool_executor()

    with pool_executor(max_workers = self.num_workers) as executor:
      # setting futures
      futures = []
      for i in range(self.num_workers):
        futures.append(executor.submit(self.__queued_process_loop, job.executable, job.process_queue))

      # wait for all threads to finish
      for f in futures:
        f.result()
    
    # updating job status
    job.end_time = datetime.now()
    job.duration = job.end_time - job.start_time
    job.completed = True
    
    if not self.silent:
      print(f"Job ({job.id}) End Time: {job.end_time}          (Duration: {job.duration})")

  def __queued_process_loop(self, function: Callable, process_queue: Queue) -> None:
    # processing loop for , continues until queue is empty
    while True:
      try:
        # acquiring item from queue
        queue_args = process_queue.get(False)
      except Empty:
        break
      # running executable
      function(*queue_args)
