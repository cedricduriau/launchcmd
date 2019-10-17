# stdlib modules
import re
import os
import shutil
import subprocess

# tool modules
from launchcmd import gitutils
from launchcmd import moduleutils
from launchcmd import settings
from launchcmd import pathutils
from launchcmd import manifestutils

REGEX_PACKAGE_NAME = re.compile(r"^([a-zA-Z0-9]+)$")
REGEX_VERSION = re.compile(r"^([\d]+[.][\d]+[.][\d]+)$")


def build_package_release_tag(package_name, version):
    """Returns the name of a release for a package.

    :param package_name: Name of the package to release.
    :type package_name: str

    :param version: Version of the release.
    :type version: str

    :rtype: str
    """
    return "{}#{}".format(package_name, version)


def split_package_release_tag(tag_name):
    """Splits a release tag into the package name and version.

    :param tag_name: Release tag to split.
    :type tag_name: str

    :rtype: list[str]
    """
    return tag_name.split("#")


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


def validate_version(version):
    """Validates a release version.

    :param version: Version of a release.
    :type version: str
    """
    match = REGEX_VERSION.search(version)
    if not match:
        msg = "invalid version {}, expected structure like: '0.1.0'"
        raise ValueError(msg.format(version))


def validate_comment(comment):
    """Validates a release comment.

    :param comment: Comment of a release.
    :type comment: str
    """
    if not comment:
        raise ValueError("comment is empty")


def validate_files(files, module_file):
    """Validates files to release.

    :param files: Absolute paths of files to release.
    :type files: list[str]

    :param module_file: Absolute path of package module file to release.
    :type module_file: str
    """
    if not files:
        raise ValueError("at least one file must be provided for release")

    for f in files:
        if f == module_file:
            break
    else:
        msg = "module file must be provided for release: {}"
        raise ValueError(msg.format(module_file))


def get_package_release_directory(package_name, version):
    """Returns the release directory of a package.

    :param package_name: Name of a package.
    :type package_name: str

    :param version: Version of a release.
    :type version: str
    """
    release_dir = os.path.join(settings.SOFTWARE_ROOT, package_name, version)
    return release_dir


def get_package_install_directory(level_dir, package_name):
    """Returns the install directory of a package for a level.

    :param level_dir: Directory of a level.
    :type level_dir: str

    :param package_name: Name of a package.
    :type package_name: str
    """
    level_package_dir = pathutils.get_level_installed_packages_dir(level_dir)
    package_dir = os.path.join(level_package_dir, package_name)
    return package_dir


def release_package(repository_dir, package_name, version, comment, files):
    """Releases a package.

    Releasing a package will do the following:
    1. The repository being released will be tagged.
    2. The repository will be copied/cloned to the software bank.
    3. The release manifest will be generated inside the release directory.
    4. All write permissions will be removed from released files.

    :param repository_dir: Directory of the repository to release.
    :type repository_dir: str

    :param package_name: Name of the package to release.
    :type package_name: str

    :param version: Version of the release.
    :type version: str

    :param comment: Comment of the release.
    :type comment: str

    :param files: Files to release.
    :type files: list[str]
    """
    # validate direct input
    gitutils.validate_directory_is_repository(repository_dir)
    validate_package_name(package_name)
    validate_version(version)
    validate_comment(comment)

    # validate module file with package name as filename exists
    module_filepath = moduleutils.build_module_filepath(repository_dir, package_name)
    if not os.path.exists(module_filepath):
        msg = "module file for package (name={}) cannot be found: {}"
        raise IOError(msg.format(package_name, module_filepath))

    # validate files for release
    validate_files(files, module_filepath)

    # validate release does not exist as git tag
    gitutils.pull_tags(repository_dir)
    tag_name = build_package_release_tag(package_name, version)
    tags = gitutils.get_tags(repository_dir)
    if tag_name in tags:
        msg = "package (name={}, version={}) already has a git tag named after release {!r}"
        raise ValueError(msg.format(package_name, version, tag_name))

    # validate release does not exist in software bank
    release_dir = get_package_release_directory(package_name, version)
    if os.path.exists(release_dir):
        msg = "package (name={}, version={}) has already been released on filesystem: {}"
        raise IOError(msg.format(package_name, version, release_dir))

    # ensure everything is pushed to git in current branch
    git_status = gitutils.get_status(repository_dir)
    if git_status:
        msg = "package contains changes that are not pushed to remote, push your changes to continue:\n{}"
        raise IOError(msg.format(os.linesep.join(git_status)))

    # create & push git tag
    gitutils.create_tag(repository_dir, tag_name)
    gitutils.push_tag(repository_dir, tag_name)

    # copy/clone package inside software bank
    os.makedirs(release_dir)
    gitutils.clone_repository(repository_dir, release_dir)

    # write manifest
    rel_files = [f.replace(repository_dir, "").lstrip(os.sep) for f in files]
    manifest = manifestutils.build_manifest(package_name=package_name,
                                            version=version,
                                            comment=comment,
                                            files=rel_files)
    manifest_path = manifestutils.build_manifest_filepath(release_dir, package_name)
    manifestutils.write_manifest(manifest_path, manifest)

    # remove write permissions of released package
    subprocess.check_call(["chmod", "-R", "a-w", release_dir])


def get_released_package_versions(package_name):
    """Gets the release versions of a package.

    :param package_name: Name of the package to get released versions from.
    :type package_name: str

    :rtype: list[str]
    """
    release_directory = os.path.join(settings.SOFTWARE_ROOT, package_name)
    versions = os.listdir(release_directory)
    return versions


def get_installed_packages(level_dir):
    """Returns the installed package releases of a level.

    :param level_dir: Directory of a level.
    :type level_dir: str

    :rtype: list[str]
    """
    installed_tags_dir = pathutils.get_level_installed_tags_dir(level_dir)

    tags = []
    if os.path.exists(installed_tags_dir):
        tags = os.listdir(installed_tags_dir)

    return tags


def install_package(level_dir, package_name, version):
    """Installs a package release on a level.

    :param level_dir: Directory of the level to install to.
    :type level_dir: str

    :param package_name: Name of the package release to install.
    :type package_name: str

    :param version: Version of the release to install.
    :type version: str
    """
    # get release directory
    release_dir = get_package_release_directory(package_name, version)
    if not os.path.exists(release_dir):
        msg = "no release found for package (name={}, version={})"
        raise IOError(msg.format(package_name, version))

    # check if package is already installed
    tag_name = build_package_release_tag(package_name, version)
    tags = get_installed_packages(level_dir)

    if tag_name in tags:
        msg = "package (name={}, version={}) already installed on {}"
        raise IOError(msg.format(package_name, version, level_dir))

    # check if another version is already installed
    release_to_uninstall = None
    for _tag_name in tags:
        i_name, i_version = split_package_release_tag(_tag_name)
        if package_name == i_name and version != i_version:
            release_to_uninstall = _tag_name
            break

    # uninstall other release version
    if release_to_uninstall:
        _package, _version = split_package_release_tag(tag_name)
        uninstall_package(level_dir, _package, _version)

    # ensure umask is cleared
    os.umask(0000)

    # copy/clone package inside level
    install_dir = get_package_install_directory(level_dir, package_name)
    if not os.path.exists(install_dir):
        os.makedirs(install_dir, 0o2775)

    # TODO: do not copy all, read specific files to copy from manifest
    gitutils.clone_repository(release_dir, install_dir)
    subprocess.check_call(["chmod", "-R", "a-w", release_dir])

    # write tag
    installed_tags_dir = pathutils.get_level_installed_tags_dir(level_dir)
    if not os.path.exists(installed_tags_dir):
        os.makedirs(installed_tags_dir, 0o2775)

    tag_filepath = os.path.join(installed_tags_dir, tag_name)
    open(tag_filepath, "w").close()
    subprocess.check_call(["chmod", "a-w", tag_filepath])


def uninstall_package(level_dir, package_name, version):
    """Uninstalls a package from a level.

    :param level_dir: Directory of the level to uninstall from.
    :type level_dir: str

    :param package_name: Name of the package release to uninstall.
    :type package_name: str

    :param version: Version of the release to uninstall.
    :type version: str
    """
    # check if package is installed
    tag_name = build_package_release_tag(package_name, version)
    tags = get_installed_packages(level_dir)

    if tag_name not in tags:
        msg = "package (name={}, version={}) is not installed on {}"
        raise IOError(msg.format(package_name, version, level_dir))

    # delete released package
    install_dir = get_package_install_directory(level_dir, package_name)
    subprocess.check_call(["chmod", "-R", "a+w", install_dir])
    shutil.rmtree(install_dir)

    # ensure umask is cleared
    os.umask(0000)

    # delete tag
    installed_tags_dir = pathutils.get_level_installed_tags_dir(level_dir)
    tag_filepath = os.path.join(installed_tags_dir, tag_name)
    os.chmod(tag_filepath, 0o0777)
    os.remove(tag_filepath)

    # remove entire .common structure if no other packages are present
    tags = get_installed_packages(level_dir)
    if not tags:
        common_dir = pathutils.get_level_common_dir(level_dir)
        shutil.rmtree(common_dir)
