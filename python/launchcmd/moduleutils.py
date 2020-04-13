# stdlib modules
import os

# tool modules
from launchcmd import packageutils


def get_module_file(path):
    package = packageutils.get_package_name(path)
    path = os.path.join(path, package + ".module")
    return path
