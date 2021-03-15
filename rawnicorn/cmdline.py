#!/usr/bin/env python
"""
Command-line cli tools for interacting with the server.
"""
import argparse

# main parser
cmdline_parser = argparse.ArgumentParser(
    description="Rawnicorn is a very raw and simple web server.", epilog="Ready to setup some sockets?"
)

# required args
cmdline_parser.add_argument(
    "--host", required=True, type=str, help="A valid domain name or ip address to bind a socket to."
)
cmdline_parser.add_argument("--port", required=True, type=int, help="A valid ipv4 address.")

# optional args (with default values)
cmdline_parser.add_argument(
    "--workers", type=int, default=1, help="Number of workers to be spawned to handle requests."
)
cmdline_parser.add_argument("--threads", type=int, default=1, help="Number of threads spawned by the workers.")
cmdline_parser.add_argument(
    "--log-level",
    type=str,
    default="INFO",
    choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    help="Logging level for the server.",
)
