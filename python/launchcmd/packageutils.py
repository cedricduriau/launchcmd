# stdlib modules
import os

# tool modules
from launchcmd import settings


# =============================================================================
# private
# =============================================================================
def _get_packages(root):
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
    name = os.path.splitext(os.path.basename(repository))[0]
    return name


def get_release_directory(package, version):
    path = os.path.join(settings.RELEASE_ROOT, package, version)
    return path


def get_install_directory(package, version, location):
    path = os.path.join(location, package, version)
    return path


def get_released_packages():
    released = _get_packages(settings.RELEASE_ROOT)
    return released


def get_installed_packages(location):
    install_root = settings.os.path.join(location, "installed")
    installed = _get_packages(install_root)
    return installed
