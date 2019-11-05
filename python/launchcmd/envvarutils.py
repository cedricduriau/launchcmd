# stdlib modules
import os

# tool modules
from launchcmd import pathutils

# env vars
ENV_VAR_PREFIX = "LAUNCHCMD_"
LEVEL_ENV_VAR_PREFIX = ENV_VAR_PREFIX + "LEVEL_"
ENV_VAR_CACHED_MODULES = "_LAUNCHCMD_MODULES"


def build_level_env_vars(level_dirs):
    """Returns the environment variables defining the levels.

    :param level_dirs: Level directories to get level env vars for.
    :type level_dirs: list[str]

    :rtype: dict[str, str]
    """
    env_vars = {}

    for level_dir in level_dirs:
        level_type = pathutils.get_level_type(level_dir)
        env_var_name = LEVEL_ENV_VAR_PREFIX + level_type.upper()
        env_vars[env_var_name] = os.path.basename(level_dir)

    return env_vars


def build_cached_env_vars(env_vars):
    """Builds the cached variant of environment variables.

    :param env_vars: Environment variables to get cached variants for.
    :type env_vars: dict[str, str]

    :rtype: dict[str, str]
    """
    env_vars = {"_" + k: v for k, v in env_vars.items()}
    return env_vars


def get_level_env_vars():
    """Returns the level environment variables currently set.

    :rtype: dict[str, str]
    """
    env_vars = {k: v for k, v in os.environ.items() if k.startswith(LEVEL_ENV_VAR_PREFIX)}
    return env_vars


def get_cached_level_env_vars():
    """Returns the cached level environment variables currently set.

    :rtype: dict[str, str]
    """
    env_vars = {k: v for k, v in os.environ.items() if k.startswith("_" + LEVEL_ENV_VAR_PREFIX)}
    return env_vars


def get_cached_modules():
    """Returns the cached loaded modules from environment.

    :rtype: list[str]
    """
    modules_str = os.getenv(ENV_VAR_CACHED_MODULES, "")
    if not modules_str:
        return []

    modules = modules_str.split(os.pathsep)
    return modules
