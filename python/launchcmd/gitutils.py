# stdlib modules
import os

# tool modules
from launchcmd import shellutils


def validate_directory_is_repository(directory):
    """Validates a repository has a .git directory.

    :param directory: Directory of a repository.
    :type directory: str
    """
    contents = os.listdir(directory)
    if ".git" not in contents:
        msg = "following directory is not a git repository, no .git directory found: {}"
        raise IOError(msg.format(directory))


def get_status(repository_dir):
    """Returns the unstaged changes of a repository,

    :param repository_dir: Directory of a repository.
    :type repository_dir: str

    :rtype: list[str]
    """
    cmd = "cd {} && git status --porcelain".format(repository_dir)
    status = shellutils.run_check_output(cmd)
    return status


def get_tags(repository_dir):
    """Returns all tags of a repository.

    :param repository_dir: Directory of a repository.
    :type repository_dir: str

    :rtype: list[str]
    """
    cmd = "cd {} && git tag".format(repository_dir)
    tags = shellutils.run_check_output(cmd)
    return tags


def pull_tags(repository_dir):
    """Pulls all tags from the remote locally.

    :param repository_dir: Directory of a repository.
    :type repository_dir: str
    """
    cmd = "cd {} && git pull --quiet --tags".format(repository_dir)
    tags = shellutils.run_check_output(cmd)
    return tags


def create_tag(repository_dir, tag_name):
    """Creates a new tag in a repository.

    :param repository_dir: Directory of a repository.
    :type repository_dir: str

    :param tag_name: Name of the tag to create.
    :type tag_name: str
    """
    cmd = "cd {} && git tag {}".format(repository_dir, tag_name)
    shellutils.run_check_output(cmd)


def push_tag(repository_dir, tag_name):
    """Pushes a tag to the remote.

    :param repository_dir: Directory of a repository.
    :type repository_dir: str

    :param tag_name: Name of the tag to push.
    :type tag_name: str
    """
    cmd = "cd {} && git push --quiet origin {}".format(repository_dir, tag_name)
    shellutils.run_check_output(cmd)


def clone_repository(repository_dir, target_dir):
    """Copies the repository to a target directory.

    :param repository_dir: Directory of the repository to copy/clone.
    :type repository_dir: str

    :param target_dir: Directory to copy/clone the repository content in.
    :type target_dir: str
    """
    # ensure the cmd looks like cp -R $repository_dir/. $target_dir/
    if not repository_dir.endswith(os.sep):
        repository_dir += os.sep
    repository_dir += "."

    if not target_dir.endswith(os.sep):
        target_dir += os.sep

    cmd = "cp -R {} {}".format(repository_dir, target_dir)
    shellutils.run_check_output(cmd)
