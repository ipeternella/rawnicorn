"""
Rawnicorn's master process.
"""
import errno
import logging
import os
import socket
import sys
from logging.config import dictConfig
from typing import Any
from typing import Dict
from typing import Optional

from rawnicorn.config import RawnicornConfig
from rawnicorn.logger import build_logging_config
from rawnicorn.workers import BasicWorker
from rawnicorn.workers import WorkerPool


class MasterRawnicorn:
    """
    Master server and worker manager for the server.
    """

    # pids
    pid: int
    workerpool: WorkerPool

    # sockets
    listener_socket: Optional[socket.socket]  # main server socket

    # config
    config: RawnicornConfig
    config_log: Dict

    # loggers
    log: logging.Logger
    log_err: logging.Logger

    def __init__(self, config: RawnicornConfig) -> None:
        self.config = config
        self.listener_socket = None
        self.workerpool = {}

    def _initialize_loggers(self, log_level: str) -> None:
        """
        Setups the main stdout and stderr loggers.
        """
        self.config_log = build_logging_config(log_level)
        dictConfig(self.config_log)

        self.log = logging.getLogger("rawnicorn.access")
        self.log_err = logging.getLogger("rawnicorn.error")

    def _initialize_sockets(self) -> None:
        """
        Creates a new socket descriptor to be inherited by the workers from the file descriptors table.
        """
        socket_family = self.config.socket_config.socket_family
        socket_type = self.config.socket_config.socket_type

        if self.listener_socket is None:

            try:
                self.listener_socket = socket.socket(socket_family, socket_type)
            except OSError as e:
                if e.errno == errno.EADDRINUSE:
                    self.log_err.error(f"Address {self.config.address} is already in use.")
                    sys.exit(1)
                else:
                    self.log_err.exception("An error occured while opening the listener socket", e)

    def _handle_forked_child_process(self, new_worker: BasicWorker):
        # child process: fork_pid == 0, so get the new PID from the OS
        child_pid = os.getpid()

        new_worker.ppid = self.pid
        new_worker.pid = child_pid

    def _handle_master_process(self, new_worker: BasicWorker, fork_pid: int):
        # master process
        self.workerpool[fork_pid] = new_worker

    def _fork_worker(self):
        """
        Forks a new worker process (exists the master main loop).
        """
        # created in advance so that parent and child processes can access
        new_worker = BasicWorker()

        # fork from here on
        fork_pid = os.fork()

        if fork_pid != 0:
            self._handle_master_process(new_worker)
        else:
            self._handle_child_process(new_worker)

    def boot(self) -> None:
        """
        Boots the server master and creates the main socket connection.
        """
        self.pid = os.getpid()  # master PID

        self._initialize_loggers(self.config.log_level)
        self._initialize_sockets()

        self.log.info(f"Listening at: {self.config.address} ({self.pid})")

    def run(self) -> None:
        """
        Master server's loop.
        """
        self.boot()
