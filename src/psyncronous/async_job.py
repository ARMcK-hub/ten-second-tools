from typing import Callable, Optional
from dataclasses import dataclass

import uuid
from queue import Queue
from datetime import datetime, timedelta


@dataclass
class AsyncJob:
    """
    AsyncJob that has an executable function and a processing queue. To be executed in an async executor.
    """

    executable: Callable
    process_queue: Queue
    id: str = str(uuid.uuid4())
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    completed: Optional[bool] = False
