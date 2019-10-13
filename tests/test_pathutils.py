# tool modules
from launchcmd import pathutils


def test_get_directories(test_project_dir, test_division_dir, test_episode_dir):
    """Test getting the directories of levels from a certain location."""
    result = pathutils.get_level_directories("test/film/ep01")

    dir_project = test_project_dir.format("test")
    dir_division = test_division_dir.format("test", "film")
    dir_episode = test_episode_dir.format("test", "film", "ep01")
    expected = [dir_project, dir_division, dir_episode]

    assert result == expected


def test_get_directory(test_episode_dir):
    """Test getting the directory of a certain level location."""
    result = pathutils.get_level_directory("test/film/ep01")
    expected = test_episode_dir.format("test", "film", "ep01")
    assert result == expected
