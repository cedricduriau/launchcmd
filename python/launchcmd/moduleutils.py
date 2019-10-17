# stdlib modules
import os
import glob

# tool modules
from launchcmd import pathutils


# =============================================================================
# private
# =============================================================================
def _load_module_python_library():
    modules_root = os.path.expandvars("$MODULESHOME")
    python_lib = os.path.join(modules_root, "init", "python.py")
    exec(open(python_lib).read())


def _get_modules_from_directory(directory):
    """Returns the module files of a directory.

    :param directory: Directory to get module files from.
    :type directory: str

    :rtype: list[str]
    """
    glob_path = os.path.join(directory, "*.module")
    module_files = glob.glob(glob_path)
    return module_files


# =============================================================================
# public
# =============================================================================
def build_module_filepath(directory, package_name):
    """Returns the filepath of a module named after a package.

    :param directory: Directory of the module file.
    :type directory: str

    :param package_name: Name of a package.
    :type package_name: str

    :rtype: str
    """
    filename = "{}.module".format(package_name)
    path = os.path.join(directory, filename)
    return path


def validate_directory_has_module(directory):
    """Validates a directory has exactly one module file.

    :param directory: Directory to valdiate.
    :type directory: str
    """
    module_files = _get_modules_from_directory(directory)

    if not module_files:
        msg = "no module files found in directory: {}"
        raise IOError(msg.format(directory))

    if len(module_files) > 1:
        msg = "multiple module files found in directory: {}"
        raise IOError(msg.format(directory))


def get_module_from_directory(directory):
    """Returns the module file of a directory.

    :param directory: Directory to get module files from.
    :type directory: str

    :rtype: str
    """
    validate_directory_has_module(directory)
    module_files = _get_modules_from_directory(directory)
    return module_files[0]


def get_modules_from_level(level_dir):
    package_dirs = pathutils.get_installed_packges(level_dir)
    module_files = list(map(get_module_from_directory, package_dirs))
    return module_files


def get_all_loaded_modules():
    loaded_modules_str = os.getenv("LOADEDMODULES", "")
    loaded_modules = loaded_modules_str.split(os.pathsep)
    loaded_modules = list(filter(None, loaded_modules))
    return loaded_modules


def get_snapshot_loaded_modules():
    loaded_modules_str = os.getenv("_LAUNCHCMD_LOADEDMODULES_SNAPSHOT", "")
    loaded_modules = loaded_modules_str.split(os.pathsep)
    loaded_modules = list(filter(None, loaded_modules))
    return loaded_modules


def load_module(modulefile):
    _load_module_python_library()
    module("load", modulefile)


def unload_module(modulefile):
    _load_module_python_library()
    module("unload", modulefile)
