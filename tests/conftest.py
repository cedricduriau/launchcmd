# stdlib modules
import os
from importlib import reload

# tool modules
from launchcmd import settings
from launchcmd import gitutils

# third party modules
import pytest


# =============================================================================
# fixtures
# =============================================================================
@pytest.fixture
def file_system_root():
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, "filesystem")


@pytest.fixture
def software_root(file_system_root):
    software_root = os.path.join(file_system_root, "software")
    return software_root


@pytest.fixture
def repositories_root(file_system_root):
    repositories_root = os.path.join(file_system_root, "repositories")
    return repositories_root


@pytest.fixture
def repository_directory(repositories_root):
    repository_directory = os.path.join(repositories_root, "testrepository")
    return repository_directory


@pytest.fixture
def test_project_dir(patch_project_root):
    project_root = os.environ["LAUNCHCMD_PROJECT_ROOT"]
    project_dir = os.path.join(project_root, "{}")
    return project_dir


@pytest.fixture
def test_division_dir(test_project_dir):
    division_dir = os.path.join(test_project_dir, "{}")
    return division_dir


@pytest.fixture
def test_episode_dir(test_division_dir):
    episode_dir = os.path.join(test_division_dir, "{}")
    return episode_dir


@pytest.fixture
def test_sequence_dir(test_episode_dir):
    sequence_dir = os.path.join(test_episode_dir, "{}")
    return sequence_dir


@pytest.fixture
def test_shot_dir(test_sequence_dir):
    shot_dir = os.path.join(test_sequence_dir, "{}")
    return shot_dir


# =============================================================================
# env patches
# =============================================================================
@pytest.fixture
def patch_project_root(file_system_root):
    project_root = os.path.join(file_system_root, "projects")
    os.environ["LAUNCHCMD_PROJECT_ROOT"] = project_root
    reload(settings)


@pytest.fixture
def patch_software_root(software_root):
    os.environ["LAUNCHCMD_SOFTWARE_ROOT"] = software_root
    reload(settings)


@pytest.fixture
def patch_software_root_tmp(tmpdir):
    os.environ["LAUNCHCMD_SOFTWARE_ROOT"] = str(tmpdir)
    reload(settings)


@pytest.fixture
def patch_pipeline_project():
    os.environ["LAUNCHCMD_PIPELINE_PROJECT"] = "pipeline"
    reload(settings)


# =============================================================================
# monkey patches
# =============================================================================
@pytest.fixture
def mock_gitutils_pull_tags_donothing(monkeypatch):
    def mock_return(*args, **kwargs):
        return
    monkeypatch.setattr(gitutils, "pull_tags", mock_return)


@pytest.fixture
def mock_gitutils_get_status_empty(monkeypatch):
    def mock_return(*args, **kwargs):
        return []

    monkeypatch.setattr(gitutils, "get_status", mock_return)


@pytest.fixture
def mock_gitutils_get_tags_empty(monkeypatch):
    def mock_return(*args, **kwargs):
        return []

    monkeypatch.setattr(gitutils, "get_tags", mock_return)


@pytest.fixture
def mock_gitutils_create_tag_donothing(monkeypatch):
    def mock_return(*args, **kwargs):
        return

    monkeypatch.setattr(gitutils, "create_tag", mock_return)


@pytest.fixture
def mock_gitutils_push_tag_donothing(monkeypatch):
    def mock_return(*args, **kwargs):
        return

    monkeypatch.setattr(gitutils, "push_tag", mock_return)
