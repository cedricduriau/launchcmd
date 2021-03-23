# stdlib modules
import os

# tool modules
from launchcmd import packageutils


def get_repository_module(path):
    """
    Return the module of a repository.

    :param path: Directory of a repository.
    :type path: str

    :rtype: str
    """
    package = packageutils.get_package_name(path)
    path = os.path.join(path, package + ".module")
    return path


def get_installed_module(path):
    """
    Return the module of an installed package.

    :param path: Directory of an installed package.
    :type path: str

    :rtype: str
    """
    package_dir, version = os.path.split(path)
    package = os.path.basename(package_dir)
    path = os.path.join(path, package + ".module")
    return path


def get_installed_modules(path):
    """
    Return the modules of all packages installed at a location.

    :param path: Location where packages are installed.
    :type path: str

    :rtype: list[str]
    """
    directory = os.path.abspath(path)
    packages = packageutils.get_installed_packages(directory)

    modules = []
    for package, versions in packages.items():
        for version in versions:
            package_dir = directory.joinpath(".installed", package, version)
            module_f = get_installed_module(package_dir)
            if os.path.exists(module_f):
                modules.append(module_f)

    return modules
