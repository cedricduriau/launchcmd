# stdlib modules
import os

# tool modules
from launchcmd import pathutils

# third party modules
import pytest


def test_get_level_type_files(test_project_dir):
    """Test getting the level type files from a valid level."""
    project_dir = test_project_dir.format("test")
    result = pathutils._get_level_type_files(project_dir)
    expected = [os.path.join(project_dir, ".launchcmd_level_project")]
    assert result == expected


def test_validate_level_type_files():
    """Test validating valid level types."""
    pathutils._validate_level_type_files([".launchcmd_level_project"])


def test_validate_level_type_files_fail():
    """Test validating invalid level types."""
    # no entries
    with pytest.raises(IOError):
        pathutils._validate_level_type_files([])

    # multiple entries
    with pytest.raises(IOError):
        pathutils._validate_level_type_files(["foo", "bar"])


def test_get_level_type_from_file():
    """Test getting the level type from a filepath."""
    result = pathutils._get_level_type_from_file("/tmp/.launchcmd_level_project")
    assert result == "project"


def test_get_directories(test_project_dir, test_division_dir, test_episode_dir):
    """Test getting the directories of levels from a certain location."""
    project_dir = test_project_dir.format("test")
    division_dir = test_division_dir.format("test", "film")
    episode_dir = test_episode_dir.format("test", "film", "ep01")
    expected = [project_dir, division_dir, episode_dir]

    # get levels from relative location
    result_rel = pathutils.get_level_directories("test/film/ep01")
    assert result_rel == expected

    # get levels from absolute location
    result_abs = pathutils.get_level_directories(episode_dir)
    assert result_abs == expected


def test_get_directory(test_episode_dir):
    """Test getting the directory of a certain level location."""
    result = pathutils.get_level_directory("test/film/ep01")
    expected = test_episode_dir.format("test", "film", "ep01")
    assert result == expected


def test_get_level_type(test_episode_dir):
    """Test getting the level type from a valid level directory."""
    episode_dir = test_episode_dir.format("test", "film", "ep01")
    result = pathutils.get_level_type(episode_dir)
    assert result == "episode"


def test_get_level_type_fail(test_episode_dir):
    """Test getting the level type from an invalid level directory."""
    # no level type file present
    episode_dir = test_episode_dir.format("test", "film", "ep01-no-level-type-file")
    with pytest.raises(IOError):
        pathutils.get_level_type(episode_dir)


def test_get_level_common_dir(test_episode_dir):
    """Test getting the .common directory of a valid level."""
    episode_dir = test_episode_dir.format("test", "film", "ep01")
    result = pathutils.get_level_common_dir(episode_dir)
    expected = os.path.join(episode_dir, ".common")
    assert result == expected


def test_get_level_installed_packages_dir(test_episode_dir):
    """Test getting the .common/packages directory of a valid level."""
    episode_dir = test_episode_dir.format("test", "film", "ep01")
    result = pathutils.get_level_installed_packages_dir(episode_dir)
    expected = os.path.join(episode_dir, ".common", "packages")
    assert result == expected


def test_get_level_installed_tags_dir(test_episode_dir):
    """Test getting the .common/tags directory of a valid level."""
    episode_dir = test_episode_dir.format("test", "film", "ep01")
    result = pathutils.get_level_installed_tags_dir(episode_dir)
    expected = os.path.join(episode_dir, ".common", "tags")
    assert result == expected
