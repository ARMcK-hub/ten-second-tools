# Welcome to Psycronous
Psyncronous is an asyncronous python pool executor module that includes:
- AsyncProcessExecutor: Multi-Processing Pool Executor
- AsyncThreadedExecutor: Multi-Threaded Pool Executor

All pool executors work by passing an AsyncJob to the executor instance.
A job can be created by supplying a syncronous Callable and a processing Queue.

## Example:
```
import AsyncJob
import AsyncProcessExecutor
from queue import Queue

# defining syncronous executable
def my_exe(input: int) -> None:
    print(input)

# defining processing queue (Note that items must be a Tuple object)
my_queue = Queue()
for i in range(10):
    input = Tuple(i)
    my_queue.put(input)

# creating an asyncronous job from executable and queue
my_job = AsyncJob(my_exe, my_queue)

# executing job with a pool executor
ape = AsyncProcessExecutor()
ape.execute(my_job)
```