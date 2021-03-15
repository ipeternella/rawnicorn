"""
Environment variables reading functions.
"""
import os
import socket


class SocketDefinitions:
    """
    Socket definitions and constants.
    """

    # Socket Kinds (Types)
    TCP_SOCKET_KIND: socket.SocketKind = socket.SOCK_STREAM  # connection-based (sequence, two-way, byte-streams): tcp
    UDP_SOCKET_KIND = socket.SOCK_DGRAM  # connectionless (datagram-based): udp

    # Socket Address Families
    IPV4_SOCKET_FAMILY = socket.AF_INET
    IPV6_SOCKET_FAMILY = socket.AF_INET6


class RawnicornSocketConfig:
    """
    Repository with socket-related config.
    """

    socket_family: socket.AddressFamily
    socket_type: socket.SocketKind
    max_backlog_connections: int

    def __init__(
        self, socket_family: socket.AddressFamily, socket_type: socket.SocketKind, max_backlog_connections: int
    ) -> None:
        self.socket_family = socket_family
        self.socket_type = socket_type
        self.max_backlog_connections = max_backlog_connections


class RawnicornConfig:
    """
    Repository of all the settings supplied to run Rawnicorn.
    """

    host: str
    port: int
    address: str
    workers: int
    threads: int
    log_level: str
    socket_config: RawnicornSocketConfig
    root_dir: str = os.path.dirname(os.path.abspath(__file__))

    def __init__(
        self, host: str, port: int, workers: int, threads: int, log_level: str, socket_config: RawnicornSocketConfig
    ) -> None:
        self.host = host
        self.port = port
        self.address = f"{host}:{port}"
        self.workers = workers
        self.threads = threads
        self.log_level = log_level
        self.socket_config = socket_config


def bind_config(
    host: str, port: int, workers: int, threads: int, log_level: str, max_backlog_connections=5
) -> RawnicornConfig:
    socket_cfg = RawnicornSocketConfig(
        socket_family=SocketDefinitions.IPV4_SOCKET_FAMILY,
        socket_type=SocketDefinitions.TCP_SOCKET_KIND,
        max_backlog_connections=max_backlog_connections,
    )

    server_cfg = RawnicornConfig(
        host=host, port=port, workers=workers, threads=threads, log_level=log_level, socket_config=socket_cfg
    )

    return server_cfg
