# stdlib modules
import os
import glob


def get_modules_from_directory(directory):
    """Returns the module files of a directory.

    :param directory: Directory to get module files from.
    :type directory: str

    :rtype: list[str]
    """
    glob_path = os.path.join(directory, "*.module")
    module_files = glob.glob(glob_path)
    return module_files


def validate_directory_has_module(directory):
    """Validates a directory has exactly one module file.

    :param directory: Directory to valdiate.
    :type directory: str
    """
    module_files = get_modules_from_directory(directory)

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
    module_files = get_modules_from_directory(directory)
    return module_files[0]
