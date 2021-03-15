"""
Rawnicorn's master process.
"""
import errno
import logging
import os
import socket
import sys
from logging.config import dictConfig
from typing import Dict
from typing import Optional

from rawnicorn.config import RawnicornConfig
from rawnicorn.logger import build_logging_config


class MasterRawnicorn:
    """
    Master server and worker manager for the server.
    """

    pid: int
    config: RawnicornConfig
    config_log: Dict
    listener_socket: Optional[socket.socket]  # main server socket

    log: logging.Logger
    log_err: logging.Logger

    def __init__(self, config: RawnicornConfig) -> None:
        self.config = config
        self.listener_socket = None

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

    def boot(self) -> None:
        """
        Boots the server master and creates the main socket connection.
        """
        self.pid = os.getpid()  # master PID

        self._initialize_loggers(self.config.log_level)
        self._initialize_sockets()

        self.log.info(f"Booting with PID: {self.pid}")
