"""
Workers used by Rawnicorn.
"""
import logging
import time
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

    # loggers
    log: logging.Logger
    log_err: logging.Logger

    running: bool

    def __init__(self, log: logging.Logger, log_err: logging.Logger) -> None:
        self.log = log
        self.log_err = log_err

    def boot(self) -> None:
        self.log.info(f"Booting worker with PID: {self.pid}")
        self.running = True

    def run(self) -> None:
        """
        Worker's main loop.
        """
        self.boot()

        while self.running:
            self.log.info(f"[{self.pid}]: Worker working...")
            time.sleep(5)
