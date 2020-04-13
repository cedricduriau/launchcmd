# stdlib modules
import os

# tool modules
from launchcmd import shellutils


def validate_repository(directory):
    """Validates a repository has a .git directory.

    :param directory: Directory of a repository.
    :type directory: str
    """
    contents = os.listdir(directory)
    if ".git" not in contents:
        msg = "following directory is not a git repository, no .git directory found: {}"
        raise IOError(msg.format(directory))


def get_status(repository):
    """Returns the unstaged changes of a repository,

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: list[str]
    """
    cmd = "cd {} && git status --porcelain".format(repository)
    status = shellutils.run_check_output(cmd)
    return status


def get_tags(repository):
    """Returns all tags of a repository.

    :param repository: Directory of a repository.
    :type repository: str

    :rtype: list[str]
    """
    cmd = "cd {} && git tag".format(repository)
    tags = shellutils.run_check_output(cmd)
    return tags


def pull_tags(repository):
    """Pulls all tags from the remote locally.

    :param repository: Directory of a repository.
    :type repository: str
    """
    cmd = "cd {} && git pull --quiet --tags".format(repository)
    tags = shellutils.run_check_output(cmd)
    return tags


def add(repository, *paths):
    cmd = "cd {} && git add {}".format(repository, " ".join(paths))
    shellutils.run_check_output(cmd)


def commit(repository, message):
    cmd = "cd {} && git commit -m \"{}\"".format(repository, message)
    shellutils.run_check_output(cmd)


def push(repository, quiet=True):
    cmd = "cd {} && git push".format(repository)
    if quiet:
        cmd += " -q"
    shellutils.run_check_output(cmd)


def create_tag(repository, tag_name):
    """Creates a new tag in a repository.

    :param repository: Directory of a repository.
    :type repository: str

    :param tag_name: Name of the tag to create.
    :type tag_name: str
    """
    cmd = "cd {} && git tag {}".format(repository, tag_name)
    shellutils.run_check_output(cmd)


def push_tag(repository, tag_name):
    """Pushes a tag to the remote.

    :param repository: Directory of a repository.
    :type repository: str

    :param tag_name: Name of the tag to push.
    :type tag_name: str
    """
    cmd = "cd {} && git push --quiet origin {}".format(repository, tag_name)
    shellutils.run_check_output(cmd)
