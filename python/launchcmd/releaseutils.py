# stdlib modules
import os
import re
import shutil


def get_release_files(repository, manifest):
    """
    Return the files to release.

    :param repository: Directory to a repository.
    :type repository: str

    :param manifest: Manifest of the repository.
    :type manifest: dict

    :rtype: list[str]
    """
    regexes = list(map(re.compile, manifest["ignore"]))
    files = []

    for dirpath, dirnames, filenames in os.walk(repository):
        for filename in filenames:
            fpath = os.path.join(dirpath, filename)
            for regex in regexes:
                if regex.search(fpath):
                    break
            else:
                files.append(fpath)

    return files


def release_file(repository, release, path):
    """
    Release a repository file.

    :param repository: Directory to a repository.
    :type repository: str

    :param release: Directory to a release.
    :type release: str

    :param path: File to release.
    :type path: str
    """
    dst_f = path.replace(repository, release)
    dst_d = os.path.dirname(dst_f)

    if not os.path.exists(dst_d):
        os.makedirs(dst_d)

    shutil.copy2(path, dst_f)
