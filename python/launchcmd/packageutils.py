# stdlib modules
import re
import os
import subprocess

# tool modules
from launchcmd import gitutils
from launchcmd import moduleutils
from launchcmd import settings

REGEX_PACKAGE_NAME = re.compile(r"^([a-zA-Z0-9]+)$")


# =============================================================================
# public
# =============================================================================
def validate_package_name(package_name):
    """
    Validates the name of a package.

    :param package_name: Name of a package.
    :type package_name: str
    """
    if not package_name:
        raise ValueError("package name must be at least one character long")

    match = REGEX_PACKAGE_NAME.search(package_name)
    if not match:
        raise ValueError("invalid package name {!r}, can only contain "
                         "alphanumerical characters".format(package_name))


def build_package_release_name(package_name, version):
    return "{}#{}".format(package_name, version)


def release_package(repository_dir, version, comment):
    # validate package dir is a repository
    gitutils.validate_repository_dir(repository_dir)

    # ensure everything is pushed to git in current branch
    git_status = gitutils.get_status(repository_dir)
    if git_status:
        msg = "package contains changes that are not pushed to remote:\n{}"
        raise IOError(msg.format(os.linesep.join(git_status)))

    # validate package dir has a module file
    moduleutils.validate_directory_has_module(repository_dir)

    # validate package name from module file
    module_filepath = moduleutils.get_module_from_directory(repository_dir)
    package_name = os.path.splitext(os.path.basename(module_filepath))[0]
    validate_package_name(package_name)

    # validate release does not exist as git tag
    tag_name = build_package_release_name(package_name, version)
    tags = gitutils.get_tags(repository_dir)
    if tag_name in tags:
        msg = "package (name={}, version={}) already has a git tag named after release {!r}"
        raise ValueError(msg.format(package_name, version, tag_name))

    # validate release does not exist in software bank
    release_dir = os.path.join(settings.SOFTWARE_ROOT, package_name, version)
    if os.path.exists(release_dir):
        msg = "package (name={}, version={}) has already been released on filesystem: {}"
        raise IOError(msg.format(package_name, version, release_dir))

    # create git tag
    gitutils.create_tag(repository_dir, tag_name)

    # clone tag inside software bank
    os.makedirs(release_dir)
    gitutils.clone_repository(repository_dir, release_dir)

    # remove write permissions of released package
    subprocess.check_call(["chmod", "-R", "a-w", release_dir])
