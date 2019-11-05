# stdlib modules
import os

# tool modules
from launchcmd import packageutils

# third party modules
import pytest


def test_release_package_contents(software_root, tmpdir):
    rel_files = [".gitignore"]
    src_dir = os.path.join(software_root, "testrepository", "0.1.0")

    # single file
    dst_dir = str(tmpdir)
    packageutils._release_package_contents(src_dir, rel_files, dst_dir)
    assert os.path.exists(os.path.join(dst_dir, ".gitignore"))

    # single file into subdir
    dst_dir = os.path.join(str(tmpdir), "test")
    packageutils._release_package_contents(src_dir, rel_files, dst_dir)
    assert os.path.exists(os.path.join(dst_dir, ".gitignore"))

    # single file from subdir
    rel_files = ["bin/testrepository"]
    packageutils._release_package_contents(src_dir, rel_files, dst_dir)
    assert os.path.exists(os.path.join(dst_dir, "bin", "testrepository"))


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


def test_release_package(repository_directory,
                         mock_gitutils_pull_tags_donothing,
                         mock_gitutils_get_status_empty,
                         mock_gitutils_get_tags_empty,
                         mock_gitutils_create_tag_donothing,
                         mock_gitutils_push_tag_donothing,
                         patch_software_root_tmp):
    """Test releasing a valid package."""
    files = [os.path.join(repository_directory, "bin/testrepository"),
             os.path.join(repository_directory, "testrepository.module")]
    packageutils.release_package(repository_directory, "testrepository", "0.2.0", "test", files)

    software_root = os.environ["LAUNCHCMD_SOFTWARE_ROOT"]
    release_dir = os.path.join(software_root, "testrepository", "0.2.0")
    f1 = os.path.join(release_dir, "bin", "testrepository")
    f2 = os.path.join(release_dir, "testrepository.module")

    # check files
    assert os.path.exists(f1)
    assert os.path.exists(f2)

    # check permissions
    result = oct(os.stat(f1).st_mode)
    assert result == "0o100555"

    result = oct(os.stat(f2).st_mode)
    assert result == "0o100444"


def test_release_package_fail_no_module_found(repository_directory):
    """Test releasing a package with a package name that does not refer to an
    existing module file."""
    with pytest.raises(FileNotFoundError):
        packageutils.release_package(repository_directory, "foo", "0.2.0", "test", ["foo"])


def test_release_package_fail_tag_exists(repository_directory,
                                         mock_gitutils_pull_tags_donothing):
    """Test releasing a package where the git tag already exists."""
    modulefile = os.path.join(repository_directory, "testrepository.module")
    with pytest.raises(ValueError):
        packageutils.release_package(repository_directory, "testrepository", "0.1.0", "test", [modulefile])


def test_release_package_fail_unstaged_changes(repository_directory,
                                               mock_gitutils_pull_tags_donothing,
                                               mock_gitutils_get_tags_empty,
                                               patch_software_root_tmp):
    """Test releasing a package with unstaged changed."""
    modulefile = os.path.join(repository_directory, "testrepository.module")

    # create dummy file to add changes to repo
    f = os.path.join(repository_directory, ".dummy")
    open(f, "w").close()

    with pytest.raises(ValueError):
        packageutils.release_package(repository_directory, "testrepository", "0.2.0", "test", [modulefile])

    # remove dummy file
    os.remove(f)


def test_get_released_package_versions(patch_software_root):
    """Test getting the releases of a package."""
    result = packageutils.get_released_package_versions("testrepository")
    assert result == ["0.0.0", "0.1.0"]


def test_get_installed_packages_tags(test_episode_dir):
    """Test getting the installed packages of a level."""
    level_dir = test_episode_dir.format("test", "film", "ep01")
    result = packageutils.get_installed_packages_tags(level_dir)
    assert result == ["testrepository#0.1.0"]


def test_install_package(patch_software_root, tmpdir):
    level_dir = str(tmpdir)
    packageutils.install_package(level_dir, "testrepository", "0.1.0")

    common_dir = os.path.join(level_dir, ".common")
    assert os.path.isdir(common_dir)

    packages_dir = os.path.join(common_dir, "packages")
    assert os.path.isdir(os.path.join(common_dir, "packages"))
    assert os.path.isdir(os.path.join(packages_dir, "testrepository"))
    assert os.path.isdir(os.path.join(packages_dir, "testrepository", "bin"))
    assert os.path.isfile(os.path.join(packages_dir, "testrepository", "bin", "testrepository"))
    assert os.path.isfile(os.path.join(packages_dir, "testrepository", "testrepository.module"))

    tags_dir = os.path.join(common_dir, "tags")
    assert os.path.isdir(tags_dir)
    assert os.path.isfile(os.path.join(common_dir, "tags", "testrepository#0.1.0"))
