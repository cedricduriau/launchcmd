# stdlib modules
import os

# tool modules
from launchcmd import packageutils

# third party modules
import pytest


def test_build_package_release_tag():
    """Test building a package release tag."""
    result = packageutils.build_package_release_tag("package", "version")
    assert result == "package#version"


def test_split_package_release_tag():
    """Test splitting a package release tag."""
    result = packageutils.split_package_release_tag("package#version")
    assert result == ["package", "version"]


def test_validate_package_name():
    """Test validating valid package names."""
    packageutils.validate_package_name("1234")  # digits
    packageutils.validate_package_name("test")  # lowercase
    packageutils.validate_package_name("TEST")  # uppercase


def test_validate_package_name_fail():
    """Test validating invalid package names."""
    with pytest.raises(ValueError):
        packageutils.validate_package_name("")

    with pytest.raises(ValueError):
        packageutils.validate_package_name("1234-Foo_Man_CHU")


def test_validate_version():
    """Test validating a valid release version."""
    packageutils.validate_version("0.1.0")


def test_validate_version_fail():
    """Test validating an invalid release version."""
    with pytest.raises(ValueError):
        packageutils.validate_version("x")


def test_validate_comment():
    """Test validating a valid comment."""
    packageutils.validate_comment("test comment")


def test_validate_comment_fail():
    """Test validating an invalid comment."""
    with pytest.raises(ValueError):
        packageutils.validate_comment(None)

    with pytest.raises(ValueError):
        packageutils.validate_comment("")


def test_validate_files():
    """Test validating a valid list of module files."""
    module_filepath = "/tmp/test.module"
    files = [module_filepath]
    packageutils.validate_files(files, module_filepath)


def test_validate_files_fail():
    """Test validating an invalid list of module files."""
    module_filepath = "/tmp/test.module"

    # no files
    with pytest.raises(ValueError):
        packageutils.validate_files([], module_filepath)

    # expected module not found
    with pytest.raises(ValueError):
        packageutils.validate_files(["other"], module_filepath)


def test_get_package_release_directory(patch_software_root, software_root):
    """Test getting the release directory of a package."""
    result = packageutils.get_package_release_directory("testrepository", "0.1.0")
    expected = os.path.join(software_root, "testrepository", "0.1.0")
    assert result == expected


def test_get_package_install_directory(test_episode_dir):
    """Test getting the install directory of a package."""
    level_dir = test_episode_dir.format("test", "film", "ep01")
    result = packageutils.get_package_install_directory(level_dir, "testrepository")
    expected = os.path.join(level_dir, ".common", "packages", "testrepository")
    assert result == expected
