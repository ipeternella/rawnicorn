"""
Environment variables reading functions.
"""
import os
from distutils.util import strtobool
from typing import List


class MissingEnvironmentVariable(Exception):
    """
    Raised when a required env var was not found.
    """


def getenv_or_default(env_name: str, default_value: str) -> str:
    """
    Gets an env variable or returns a default value.
    """
    if (env_value := os.getenv(env_name)) is None:
        return default_value

    return env_value


def getenv_or_exception(env_name: str) -> str:
    """
    Gets an env variable or raises an exception.
    """
    if (env_value := os.getenv(env_name)) is None:
        raise MissingEnvironmentVariable("Missing required env var is missing: %s", env_name)

    return env_value


def getenv_as_bool(env_name: str) -> bool:
    """
    Evals env var strings as booleans.
    """
    env_var = getenv_or_exception(env_name)

    return strtobool(env_var)


def getenv_as_list(env_name: str, default_value: str = "", sep: str = ",", required=True) -> List[str]:
    """
    Gets an env as a split list according to a given separator which defaults to ','.

    If required == True, then an exception is raised if the env is not found. Otherwise, a default_value parameter
    is used to defined a default value if the env value is not found.
    """
    if required:
        env_var = getenv_or_exception(env_name)
    else:
        env_var = getenv_or_default(env_name, default_value)

    env_list = [item.strip() for item in env_var.split(sep)]

    return env_list
