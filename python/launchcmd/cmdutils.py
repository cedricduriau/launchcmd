# tool modules
from launchcmd import envvarutils
from launchcmd import pathutils
from launchcmd import packageutils
from launchcmd import moduleutils


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
    """Builds the command to set environment variables.

    :param env_vars: Environment variables to set.
    :type env_vars: dict[str, str]

    :rtype: str
    """
    commands = ["export {}={}".format(k, v) for k, v in env_vars.items()]
    return " && ".join(commands)


def _build_unset_env_vars_command(env_vars):
    """Builds the command to unset environment variables.

    :param env_vars: Environment variables to unset.
    :type env_vars: dict[str, str]

    :rtype: str
    """
    commands = ["unset {}".format(k) for k in env_vars]
    return " && ".join(commands)


def _build_module_load_command(module_files):
    """Builds the command to load modules.

    :param module_files: Module files to load.
    :type module_files: list[str]

    :rtype: str
    """
    commands = ["module load {}".format(f) for f in module_files]
    return " && ".join(commands)


def _build_module_unload_command(module_files):
    """Builds the command to unload modules.

    :param module_files: Module files to unload.
    :type module_files: list[str]

    :rtype: str
    """
    commands = ["module unload {}".format(f) for f in module_files]
    return " && ".join(commands)


# =============================================================================
# public
# =============================================================================
def build_launchcmd_command(level_dir):
    """Builds the command to set the environment according to a level.

    :param level_dir: Directory of the level to set environment for.
    :type level_dir: str

    :rtype: str
    """
    commands = []

    # get all parent levels related to given level
    level_dirs = pathutils.get_level_directories(level_dir)

    # build cd command
    cd_command = _build_cd_command(level_dir)
    commands.append(cd_command)

    # get level vars to set
    level_env_vars_to_set = envvarutils.build_level_env_vars(level_dirs)

    # get cached level vars to set
    cached_level_env_vars_to_set = envvarutils.build_cached_env_vars(level_env_vars_to_set)

    # get level vars to unset
    level_env_vars_set = envvarutils.get_level_env_vars()
    level_env_vars_to_unset = set(level_env_vars_set.keys()) - set(level_env_vars_to_set.keys())

    # get cached level vars to unset
    cached_level_env_vars_set = envvarutils.get_cached_level_env_vars()
    cached_level_env_vars_to_unset = set(cached_level_env_vars_set.keys()) - set(cached_level_env_vars_to_set.keys())

    # build unset level env vars cmd
    unset_level_env_vars = _build_unset_env_vars_command(level_env_vars_to_unset)
    commands.append(unset_level_env_vars)

    # build unset cached level env vars cmd
    unset_cached_level_env_vars = _build_unset_env_vars_command(cached_level_env_vars_to_unset)
    commands.append(unset_cached_level_env_vars)

    # build set level env vars cmd
    set_level_env_vars = _build_set_env_vars_command(level_env_vars_to_set)
    commands.append(set_level_env_vars)

    # build set cached level env vars cmd
    set_cached_level_env_vars = _build_set_env_vars_command(cached_level_env_vars_to_set)
    commands.append(set_cached_level_env_vars)

    # get modules to load
    module_files_to_load = []
    for _level_dir in level_dirs:
        package_dirs = packageutils.get_installed_packages_directories(_level_dir)
        for packge_dir in package_dirs:
            _module_files = moduleutils.get_modules_from_directory(packge_dir)
            module_files_to_load.extend(_module_files)

    # get modules to unload
    module_files_to_unload = envvarutils.get_cached_modules()
    module_files_to_unload = list(set(module_files_to_unload) - set(module_files_to_load))

    # build module unload cmd
    module_unload_cmd = _build_module_unload_command(module_files_to_unload)
    commands.append(module_unload_cmd)

    # build module load cmd
    module_load_cmd = _build_module_load_command(module_files_to_load)
    commands.append(module_load_cmd)

    # build command string
    commands = filter(None, commands)
    command_str = " && ".join(commands)
    return command_str
