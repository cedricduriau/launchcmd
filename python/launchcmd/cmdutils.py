# tool modules
from launchcmd import envvarutils
from launchcmd import pathutils


# =============================================================================
# private
# =============================================================================
def _build_cd_command(path):
    """Builds the command to set the current working directory.

    :param path: Directory to set as current working directory.
    :type path: str

    :rtype: str
    """
    return "cd {}".format(path)


def _build_set_env_vars_command(env_vars):
    """
    Builds the command to set environment variables.

    :param env_vars: Environment variables to set.
    :type env_vars: dict[str, str]

    :rtype: str
    """
    commands = ["export {}={}".format(k, v) for k, v in env_vars.items()]
    return " && ".join(commands)


def _build_unset_env_vars_command(env_vars):
    """
    Builds the command to unset environment variables.

    :param env_vars: Environment variables to unset.
    :type env_vars: dict[str, str]

    :rtype: str
    """
    commands = ["unset {}".format(k) for k in env_vars]
    return " && ".join(commands)


# =============================================================================
# public
# =============================================================================
def build_launchcmd_command(dir_level):
    """Builds the command to set the environment according to a level.

    :param dir_level: Directory of the level to set environment for.
    :type dir_level: str

    :rtype: str
    """
    commands = []

    # get all parent levels related to given level
    level_dirs = pathutils.get_level_directories(dir_level)

    # build env vars to unset
    unset_env_vars = envvarutils.get_env_vars_to_unset()
    unset_env_vars_command = _build_unset_env_vars_command(unset_env_vars)
    commands.append(unset_env_vars_command)

    # build env vars to set
    set_env_vars = envvarutils.get_env_vars_to_set(level_dirs)
    set_env_vars_command = _build_set_env_vars_command(set_env_vars)
    commands.append(set_env_vars_command)

    # TODO: build PS1 location as prefix in bold

    # build cd command
    cmd_command = _build_cd_command(dir_level)
    commands.append(cmd_command)

    # build command string
    commands = filter(None, commands)
    command_str = " && ".join(commands)
    return command_str
