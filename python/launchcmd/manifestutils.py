# stdlib modules
from __future__ import absolute_import
import os
import json

# tool modules
from launchcmd import packageutils


def get_manifest_file(repository):
    package = get_package_name(repository)
    path = os.path.join(repository, package + ".manifest")
    return path


def write_manifest(path, manifest):
    with open(path, "w") as fp:
        json.dump(manifest, fp, indent=4, sort_keys=True)
        fp.write(os.linesep)
    return path


def create_manifest(repository):
    path = get_manifest_file(repository)
    manifest = {"package": None, "version": None, "message": None, "ignore": [".git"]}
    write_manifest(path, manifest)
    return path


def read_manifest(repository):
    path = get_manifest_file(repository)
    with open(path, "r") as fp:
        contents = json.load(fp)
    return contents


def update_manifest(repository, manifest):
    path = get_manifest_file(repository)
    current_manifest = read_manifest(repository)
    new_manifest = current_manifest.copy()
    new_manifest.update(manifest)
    write_manifest(path, manifest)
    return path
