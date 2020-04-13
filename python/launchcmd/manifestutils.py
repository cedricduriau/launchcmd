# stdlib modules
from __future__ import absolute_import
import os
import json

# tool modules
from launchcmd import packageutils


def get_manifest_file(repository):
    """
    Return the repository manifest file.

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: str
    """
    package = packageutils.get_package_name(repository)
    path = os.path.join(repository, package + ".manifest")
    return path


def write_manifest(path, manifest):
    """
    Write a repository manifest file.

    :param path: Path to write manifest to.
    :type path: str

    :param manifest: Manifest to write.
    :type manifest: dict
    """
    with open(path, "w") as fp:
        json.dump(manifest, fp, indent=4, sort_keys=True)
        fp.write(os.linesep)


def create_manifest(repository):
    """
    Creates an empty/default repository manifest.

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: str
    """
    path = get_manifest_file(repository)
    manifest = {"package": None, "version": None, "message": None, "ignore": [".git"]}
    write_manifest(path, manifest)
    return path


def read_manifest(repository):
    """
    Read a repository manifest.

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: dict
    """
    path = get_manifest_file(repository)
    with open(path, "r") as fp:
        contents = json.load(fp)
    return contents


def update_manifest(repository, manifest):
    """
    Update a repository manifest.

    :param repository: Directory of a repository.
    :type repository: str

    :param manifest: Updates manifest to write.
    :type manifest: dict
    """
    current_manifest = read_manifest(repository)
    new_manifest = current_manifest.copy()
    new_manifest.update(manifest)

    path = get_manifest_file(repository)
    write_manifest(path, manifest)
