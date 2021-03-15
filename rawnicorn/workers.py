"""
Workers used by Rawnicorn.
"""
from typing import Any
from typing import TypedDict


class WorkerPool(TypedDict):
    pid: int
    worker: Any


class BasicWorker:
    """
    Worker which uses the forked process without spawning threads to handle requests.
    """

    # pids
    ppid: int  # the parent's PID
    pid: int  # worker's PID

    def __init__(self, ppid: int) -> None:
        self.ppid = ppid

    def boot(self) -> None:
        pass

    def run(self) -> None:
        """
        Worker's main loop.
        """
        pass
