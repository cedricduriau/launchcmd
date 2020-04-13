# stdlib modules
import os

# tool modules
from launchcmd import packageutils


def get_module_file(path):
    """
    Return the package module.

    :param path: Directory of a repository, local, released or installed.
    :type path: str

    :rtype: str
    """
    package = packageutils.get_package_name(path)
    path = os.path.join(path, package + ".module")
    return path
