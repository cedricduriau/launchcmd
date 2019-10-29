# stdlib modules
import os
import glob
import json


# =============================================================================
# private
# =============================================================================
def _get_manifest_files(directory):
    """Returns the manifest files from a directory.

    :param directory: Directory to get manifest files from.
    :type directory: str

    :rtype: list[str]
    """
    glob_path = os.path.join(directory, "*.manifest")
    files = glob.glob(glob_path)
    return files


def _validate_manifest_files(directory, files):
    """Validates the manifest files found inside a directory.

    :param directory: Directory the manifest files were found in.
    :type directory: str

    :param files: Manifest files found inside directory.
    :type files: list[str]
    """
    if not files:
        msg = "no manifest file (*.manifest) found in {}"
        raise IOError(msg.format(directory))


def _validate_manifest_file(manifest_files, package_name):
    """Validates that a list of manifest files contains a package manifest.

    :param manifest_files: Manifest files to search package manifest in.
    :type manifest_files: list[str]

    :param package_name: Name of a package to validate manifest file for.
    :type package_name: str
    """
    for manifest_file in manifest_files:
        basename = os.path.splitext(os.path.basename(manifest_file))[0]
        if basename == package_name:
            return

    msg = "no manifest file (*.manifest) found for package {}"
    raise IOError(msg.format(package_name))


# =============================================================================
# public
# =============================================================================
def get_manifest_path_from_directory(repo_dir, package_name):
    """Returns the manifest file from a directory.

    :param directory: Directory to get manifest file from.
    :type directory: str

    :rtype: str
    """
    manifest_files = _get_manifest_files(repo_dir)
    _validate_manifest_files(repo_dir, manifest_files)
    _validate_manifest_file(manifest_files, package_name)
    manifest_file = manifest_files[0]
    return manifest_file


def build_manifest_filepath(directory, package_name):
    """Builds the manifest filepath of a package.

    :param directory: Directory of the manifest file.
    :type directory: str

    :param package_name: Name of a package to build manifest filepath for.
    :type package_name: str

    :rtype: str
    """
    filename = "{}.manifest".format(package_name)
    filepath = os.path.join(directory, filename)
    return filepath


def build_manifest(package_name="", version="", comment="", files=[]):
    """Builds the manifest data set.

    :param package_name: Name of the package to release.
    :type package_name: str

    :param version: Version of the release.
    :type version: str

    :param comment: Comment of the release.
    :type comment: str

    :param files: Relative paths of files to release.
    :type files: list[str]

    :rtype: dict
    """
    return {"package": package_name,
            "version": version,
            "comment": comment,
            "files": files[:]}


def read_manifest(path):
    """Returns the manifest file content.

    :param path: Path of the manifest file to read.
    :type path: str

    :rtype: dict
    """
    if not os.path.exists(path):
        raise IOError("manifest file does not exist: {}".format(path))

    with open(path, "r") as fp:
        try:
            return json.load(fp)
        except json.JSONDecodeError as e:
            msg = "unable to decode manifest file: {}\n{}"
            raise ValueError(msg.format(path, str(e)))


def write_manifest(path, manifest=None):
    """Writes a manifest on disk.

    :param path: Path of the manifest to write.
    :type path: str

    :param manifest: Manifest data.
    :type manifest: dict or None
    """
    if not manifest:
        manifest = build_manifest()

    with open(path, "w") as fp:
        json.dump(manifest, fp, indent=4)
