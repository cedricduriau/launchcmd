# stdlib modules
import os

# tool modules
from launchcmd import pathutils


def get_level_env_vars(level_dirs):
    """Returns the environment variables defining the levels.

    :param level_dirs: Level directories to get level env vars for.
    :type level_dirs: list[str]

    :rtype: dict[str, str]
    """
    env_vars = {}

    for level_dir in level_dirs:
        level_type = pathutils.get_level_type(level_dir)
        env_var_name = "LAUNCHCMD_LEVEL_{}".format(level_type)
        env_vars[env_var_name] = os.path.basename(level_dir)

    return env_vars


def get_env_vars_to_set(level_dirs):
    """Returns the environment variables to set for specific levels.

    :param level_dirs: Level directories to get env vars for.
    :type level_dirs: list[str]

    :rtype: dict[str, str]
    """
    env_vars = {}

    # level
    level_env_vars = get_level_env_vars(level_dirs)
    env_vars.update(level_env_vars)

    # cached env vars
    cached_env_vars = {"_LAUNCHCMD_{}".format(k): v for k, v in env_vars.items()}
    env_vars.update(cached_env_vars)

    return env_vars


def get_env_vars_to_unset():
    """Returns the environment variables to unset for specific levels.

    :param level_dirs: Level directories to get env vars for.
    :type level_dirs: list[str]

    :rtype: dict[str, str]
    """
    cached_env_vars = []
    set_env_vars = []

    cache_prefix = "_LAUNCHCMD_"
    for env_var in os.environ:
        if env_var.startswith(cache_prefix):
            cached_env_vars.append(env_var)
            # get real environment variable name from cached name
            set_env_var = "".join(env_var[len(cache_prefix):])
            set_env_vars.append(set_env_var)

    env_vars = []
    env_vars.extend(set_env_vars)
    env_vars.extend(cached_env_vars)

    return env_vars
