# stdlib modules
import os
import json


def build_manifest():
    """Builds an empty manifest data set.

    :rtype: dict
    """
    return {"files": []}


def write_manifest(path, manifest):
    """Writes manifest data into a file.

    :param path: Manifest file to write.
    :type path: str

    :param manifest: Manifest data to write to file.
    :type manifest: dict
    """
    with open(path, "w") as fp:
        json.dump(manifest, fp, indent=4)


def build_manifest_path(repo_dir, package_name):
    """Builds the manifest filepath.

    :param repo_dir: Directory of the repository/package.
    :type repo_dir: str

    :param package_name: Name of the package.
    :type package_name: str

    :rtype: str
    """
    suffix = ".manifest"
    if not package_name.endswith(suffix):
        package_name += suffix
    return os.path.join(repo_dir, package_name)


def build_file_entry(relative_path, file_type, destination):
    """Builds a manifest file entry.

    :param relative_path: Path of a file entry relative to the repository.
    :type relative_path: str

    :param file_type: Type the file entry is tagged as.
    :type file_type: str

    :param destination: Directory relative to the repository determining the
                        install location of the file entry.
    :type destination: str

    :rtype: dict[str, str]
    """
    return {"rel_path": relative_path,
            "file_type": file_type,
            "destination": destination}


def add_file_entry(manifest, file_entry):
    """Adds a file entry to a manifest.

    :param manifest: Manifest to add file entry to.
    :type manifest: dict

    :param file_entry: File entry to add to the manifest.
    :type file_entry: dict
    """
    manifest["files"].append(file_entry)
