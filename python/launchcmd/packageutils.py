# stdlib modules
import os

# tool modules
from launchcmd import settings


# =============================================================================
# private
# =============================================================================
def _get_packages(root):
    """
    Return the packages of a directory.

    :param root: Directory of the release root or an install location.
    :type root: str

    :rtype: dict[str, list[str]]
    """
    if not os.path.exists(root):
        return {}

    names = os.listdir(root)
    packages = {}

    for package in names:
        package_root = os.path.join(root, package)
        versions = os.listdir(package_root)
        packages[package] = versions

    return packages


# =============================================================================
# public
# =============================================================================
def get_package_name(repository):
    """
    Return the package name of a repository.

    :param repository: Directory to a repository.
    :type repository: str

    :rtype: str
    """
    name = os.path.splitext(os.path.basename(repository))[0]
    return name


def get_release_directory(package, version):
    """
    Return the release directory of a package.

    :param package: Name of a package.
    :type package: str

    :param version: Version of a package.
    :type version: str

    :rtype: str
    """
    path = os.path.join(settings.RELEASE_ROOT, package, version)
    return path


def get_install_directory(package, version, location):
    """
    Return the install directory of a package.

    :param package: Name of a package.
    :type package: str

    :param version: Version of a package.
    :type version: str

    :param location: Directory to install in.
    :type location: str

    :rtype: str
    """
    path = os.path.join(location, package, version)
    return path


def get_released_packages():
    """
    Return all released packages.

    :rtype: dict[str, list[str]]
    """
    released = _get_packages(settings.RELEASE_ROOT)
    return released


def get_installed_packages(location):
    """
    Return all install packages of a location.

    :param location: Directory to get installed package for.
    :type location: str

    :rtype: dict[str, list[str]]
    """
    install_root = settings.os.path.join(location, "installed")
    installed = _get_packages(install_root)
    return installed
