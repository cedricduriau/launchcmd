# stdlib modules
from __future__ import absolute_import
import os
import shutil
import subprocess

# tool modules
from launchcmd import gitutils
from launchcmd import moduleutils
from launchcmd import manifestutils
from launchcmd import packageutils
from launchcmd import releaseutils


# =============================================================================
# public
# =============================================================================
def release_package(repository, version, message):
    """
    Releases a package.

    :param repository: Repository to release.
    :type repository: str

    :param version: Version of the release.
    :type version: str

    :param message: Message of the release.
    :type message: str
    """
    repository = os.path.abspath(os.path.expanduser(repository))

    # check if repository exists
    if not os.path.exists(repository):
        raise RuntimeError("repository does not exist: {}".format(repository))

    # check if repository is git repository
    gitutils.validate_repository(repository)

    # check if repository is staged
    unstaged = gitutils.get_status(repository)
    if unstaged:
        raise RuntimeError("repository contains unstaged changes")

    # check if tag exists
    tags = gitutils.get_tags(repository)
    if version in tags:
        raise RuntimeError("tag {} already exists".format(version))

    # check if module exists
    module_file = moduleutils.get_module_file(repository)
    if not os.path.exists(module_file):
        raise RuntimeError("no module file found: {}".format(module_file))

    # read / create manifest
    manifest_file = manifestutils.get_manifest_file(repository)
    if not os.path.exists(manifest_file):
        manifestutils.create_manifest(repository)
    manifest = manifestutils.read_manifest(repository)

    # update manifest
    package = packageutils.get_package_name(repository)
    manifest["package"] = package
    manifest["version"] = version
    manifest["message"] = message
    manifestutils.update_manifest(repository, manifest)

    # commit & push manifest
    gitutils.add(repository, manifest_file)
    gitutils.commit(repository, "update manifest for release {}".format(version))
    gitutils.push(repository)

    # create git tag
    gitutils.create_tag(repository, version)
    gitutils.push_tag(repository, version)
    gitutils.pull_tags(repository)

    # get files to release
    files = releaseutils.get_release_files(repository, manifest)

    # copy file to release
    release = releaseutils.get_release_directory(package, version)
    releaseutils.copy_release_files(repository, release, files)

    # lock release directory
    subprocess.check_call(["chmod", "-R", "-w", release])


def list_released_packages():
    """Print all released packages."""
    packages = packageutils.get_released_packages()
    for package in sorted(packages.keys()):
        versions = packages[package]
        versions.sort()
        for version in sorted(versions):
            print(package + "-" + version)


def install_package(package, version, location):
    """
    Install a package to a location.

    :param package: Package of the release to install.
    :type package: str

    :param version: Version of the release to install.
    :type version: str

    :param location: Location to install to.
    :type location: str
    """
    release = packageutils.get_release_directory(package, version)
    install = packageutils.get_install_directory(package, version, location)
    if os.path.exists(install):
        raise RuntimeError("{}-{} already installed".format(package, version))
    shutil.copytree(release, install)


def list_installed_packages(location):
    """
    Print all installed packages of a location.

    :param location: Directory to print installed packages of.
    :type location: str
    """
    location = os.path.abspath(os.path.expanduser(location))
    packages = packageutils.get_installed_packages(location)
    for package in sorted(packages.keys()):
        versions = packages[package]
        for version in sorted(versions):
            print(package + "-" + version)


def uninstall_package(package, version, location):
    """
    Uninstall a package from a location.

    :param package: Package of the release to uninstall.
    :type package: str

    :param version: Version of the release to uninstall.
    :type version: str

    :param location: Location to uninstall from.
    :type location: str
    """
    install = packageutils.get_install_directory(package, version, location)
    if not os.path.exists(install):
        raise RuntimeError("{}-{} not installed".format(package, version))
    shutil.rmtree(install)
