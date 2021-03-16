"""
Rawnicorn's master process.
"""
import errno
import logging
import os
import signal
import socket
import sys
import time
from logging.config import dictConfig
from typing import Any
from typing import Dict
from typing import Optional

from rawnicorn.config import RawnicornConfig
from rawnicorn.logger import build_logging_config
from rawnicorn.workers import BasicWorker


class MasterRawnicorn:
    """
    Master server and worker manager/supervisor for the server.
    """

    # pids
    pid: int
    workerpool: Dict[int, Any]

    # sockets
    listener_socket: Optional[socket.socket]  # main server socket

    # config
    config: RawnicornConfig
    config_log: Dict

    # loggers
    log: logging.Logger
    log_err: logging.Logger

    # running
    running: bool

    def __init__(self, config: RawnicornConfig) -> None:
        self.config = config
        self.listener_socket = None
        self.running = False
        self.workerpool = dict()

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

    def _is_master_process(self, pid):
        """
        Helper method to detected if a given process's pid is the supervisor's pid or a child pid.
        """
        return self.pid == pid

    def _handle_child_process(self, new_worker: BasicWorker) -> None:
        """
        Method invoked only in the spawned child processes.
        """
        # child process: fork_pid == 0, so get the new PID from the OS
        child_pid = os.getpid()

        new_worker.ppid = self.pid
        new_worker.pid = child_pid

        # start new worker's main loop in the forked process
        new_worker.run()
        sys.exit(0)

    def _handle_master_process(self, new_worker: BasicWorker, fork_pid: int) -> None:
        """
        Method invoke only by the master supervisor process.
        """
        self.log.info("Adding new child...")
        self.workerpool[fork_pid] = new_worker

    def _fork_worker(self) -> None:
        """
        Forks a new worker process (exists the master main loop).
        """
        self.log.info("Spawning new worker...")

        # created in advance so that parent and child processes can access
        new_worker = BasicWorker(self.log, self.log_err)

        # fork from here on
        fork_pid = os.fork()

        if fork_pid != 0:
            self._handle_master_process(new_worker, fork_pid)
        else:
            self._handle_child_process(new_worker)

    def _kill_worker(self, worker_pid: int, sig: signal.Signals):
        """
        Kills a worker from the worker pool by sending OS finishing signal such as SIGKILL.
        """
        self.log.info(f"Killing worker: {worker_pid}")
        os.kill(worker_pid, sig)

    def _supervise_workers(self) -> None:
        """
        Forever loop run by the master process. Supervises workers in order to create
        new workers, or even kill them when necessary.
        """
        while self.running:
            time.sleep(5)
            # check workers health, the pool size and kill if needed
            num_workers = len(self.workerpool)

            if num_workers < self.config.workers:
                self._fork_worker()

    def boot(self) -> None:
        """
        Boots the server master and creates the main socket connection.
        """
        self.pid = os.getpid()  # master PID

        self._initialize_loggers(self.config.log_level)
        self._initialize_sockets()

        self.running = True
        self.log.info(f"Listening at: {self.config.address} ({self.pid})")

    def run(self) -> None:
        """
        Master server's loop.
        """
        self.boot()

        try:
            self._supervise_workers()
        except (StopIteration, KeyboardInterrupt):
            self.stop()

    def stop(self) -> None:
        """
        Shutdowns master process, its workers and closes listening sockets.
        """
        current_pid = os.getpid()

        if not self._is_master_process(current_pid):
            self.log.info("Worker detected, exiting...")

        self.log.info("Shutting down sockets...")
        if self.listener_socket is not None:
            self.listener_socket.close()

        self.log.info("Shutting down workers...")
        for worker_pid in self.workerpool.keys():
            self._kill_worker(worker_pid, signal.SIGKILL)

        self.log.info("Finished master process")
