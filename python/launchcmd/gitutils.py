# stdlib modules
import os

# tool modules
from launchcmd import shellutils


def validate_repository(directory):
    """
    Validate a repository has a .git directory.

    :param directory: Directory of a repository.
    :type directory: str
    """
    contents = os.listdir(directory)
    if ".git" not in contents:
        msg = "following directory is not a git repository, no .git directory found: {}"
        raise IOError(msg.format(directory))


def get_status(repository):
    """
    Return the unstaged changes of a repository,

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: list[str]
    """
    cmd = "cd {} && git status --porcelain".format(repository)
    status = shellutils.run_check_output(cmd)
    return status


def get_tags(repository):
    """
    Return the tags of a repository.

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: list[str]
    """
    cmd = "cd {} && git tag".format(repository)
    tags = shellutils.run_check_output(cmd)
    return tags


def pull_tags(repository):
    """
    Pull tags from the remote.

    :param repository: Directory of a repository.
    :type repository: str
    """
    cmd = "cd {} && git pull --quiet --tags".format(repository)
    tags = shellutils.run_check_output(cmd)
    return tags


def add(repository, *paths):
    """
    Add paths to stage for commit.

    :param repository: Directory of a repository.
    :type repository: str

    :param paths: Paths to stage for commit.
    :type paths: tuple(str)
    """
    cmd = "cd {} && git add {}".format(repository, " ".join(paths))
    shellutils.run_check_output(cmd)


def commit(repository, message):
    """
    Commit staged changed.

    :param repository: Directory of a repository.
    :type repository: str

    :param message: Commit message.
    :type message: str
    """
    cmd = "cd {} && git commit -m \"{}\"".format(repository, message)
    shellutils.run_check_output(cmd)


def push(repository, quiet=True):
    """
    Push recent commits.

    :param repository: Directory of a repository.
    :type repository: str

    :param quiet: Whether to print the output in the console or not.
    :type quiet: bool
    """
    cmd = "cd {} && git push".format(repository)
    if quiet:
        cmd += " -q"
    shellutils.run_check_output(cmd)


def create_tag(repository, tag_name):
    """
    Create a tag.

    :param repository: Directory of a repository.
    :type repository: str

    :param tag_name: Name of the tag to create.
    :type tag_name: str
    """
    cmd = "cd {} && git tag {}".format(repository, tag_name)
    shellutils.run_check_output(cmd)


def push_tag(repository, tag_name):
    """
    Push a tag to the remote.

    :param repository: Directory of a repository.
    :type repository: str

    :param tag_name: Name of the tag to push.
    :type tag_name: str
    """
    cmd = "cd {} && git push --quiet origin {}".format(repository, tag_name)
    shellutils.run_check_output(cmd)
