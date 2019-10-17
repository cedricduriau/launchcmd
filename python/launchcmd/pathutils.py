# stdlib modules
import os
import glob

# tool modules
from launchcmd import settings


# =============================================================================
# private
# =============================================================================
def _get_level_type_files(dir_level):
    """Returns the level type files insie a level directory.

    :param dir_level: Directory of a level.
    :type dir_level: str

    :rtype: list[str]
    """
    glob_path = os.path.join(dir_level, ".launchcmd_level_*")
    files = glob.glob(glob_path)
    return files


def _validate_level_type_files(files):
    """Validates the level type files of a level directory.

    :param files: Level files found inside a level directory.
    :type files: list[str]
    """
    if not files:
        raise IOError("no level file found (.launchcmd_level_*)")

    if len(files) > 1:
        raise IOError("multiple level files found (.launchcmd_level_*)")


def _get_level_type_from_file(filepath):
    """Returns the level type from a level type filepath.

    :param filepath: Level type filepath.
    :type filepath: str

    :rtype: str
    """
    basename = os.path.basename(filepath)
    level_type = basename.replace(".launchcmd_level_", "").upper()
    return level_type


# =============================================================================
# public
# =============================================================================
def get_level_directories(location):
    """Gets the directories of all levels found up until given location.

    :param location: Relative or absolute path of a level.
    :type location: str

    :rtype: list[str]
    """
    if location.startswith(settings.PROJECT_ROOT):
        location = location.replace(settings.PROJECT_ROOT, "")

    location = location.strip(os.sep)
    parts = location.split(os.sep)

    level_dirs = []
    for i, part in enumerate(parts):
        full_name = parts[:i + 1]
        level_dir = os.path.join(settings.PROJECT_ROOT, *full_name)
        level_dirs.append(level_dir)

    return level_dirs


def get_level_directory(location):
    """Gets the level directory of given location.

    :param location: Relative or absolute path of a level.
    :type location: str

    :rtype: str
    """
    level_dirs = get_level_directories(location)
    return level_dirs[-1]


def get_level_type(dir_level):
    """Gets the level type from a level directory.

    :param dir_level: Directory of a level.
    :type dir_level: str

    :rtype: str
    """
    level_type_files = _get_level_type_files(dir_level)

    try:
        _validate_level_type_files(level_type_files)
    except IOError as e:
        msg = "location {} is not a valid level, {}"
        raise IOError(msg.format(dir_level, str(e)))

    level_type_file = level_type_files[0]
    level_type = _get_level_type_from_file(level_type_file)

    return level_type


def get_level_common_dir(level_dir):
    """Returns the common directory of a level.

    :param dir_level: Directory of a level.
    :type dir_level: str

    :rtype: str
    """
    common_dir = os.path.join(level_dir, ".common")
    return common_dir


def get_level_installed_packages_dir(level_dir):
    """Returns the installed_packagae directory of a level.

    :param dir_level: Directory of a level.
    :type dir_level: str

    :rtype: str
    """
    common_dir = get_level_common_dir(level_dir)
    installed_packges_dir = os.path.join(common_dir, "packages")
    return installed_packges_dir
