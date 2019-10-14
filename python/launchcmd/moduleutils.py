# stdlib modules
import os
import glob


def get_modules_from_directory(directory):
    glob_path = os.path.join(directory, "*.module")
    module_files = glob.glob(glob_path)
    return module_files


def validate_directory_has_module(directory):
    module_files = get_modules_from_directory(directory)

    if not module_files:
        msg = "no module files found in directory: {}"
        raise IOError(msg.format(directory))

    if len(module_files) > 1:
        msg = "multiple module files found in directory: {}"
        raise IOError(msg.format(directory))


def get_module_from_directory(directory):
    validate_directory_has_module(directory)
    module_files = get_modules_from_directory(directory)
    return module_files[0]
