# stdlib modules
import os
import glob


# =============================================================================
# private
# =============================================================================
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


def validate_directory_has_modules(directory):
    """Validates a directory has at least one module file.

    :param directory: Directory to valdiate.
    :type directory: str
    """
    module_files = _get_modules_from_directory(directory)

    if not module_files:
        msg = "no module files found in directory: {}"
        raise IOError(msg.format(directory))


def get_modules_from_directory(directory):
    """Returns the module file of a directory.

    :param directory: Directory to get module files from.
    :type directory: str

    :rtype: str
    """
    validate_directory_has_modules(directory)
    module_files = _get_modules_from_directory(directory)
    return module_files
