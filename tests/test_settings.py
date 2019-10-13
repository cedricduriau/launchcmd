# stdlib modules
import uuid

# tool modules
from launchcmd import settings

# third party modules
import pytest


def test_get_env_var_value(patch_pipeline_project):
    """Test getting the value of a valid environment variable."""
    settings._get_env_var_value("LAUNCHCMD_PIPELINE_PROJECT")


def test_get_env_var_value_fail():
    """Test getting the value of an invalid environment variable."""
    with pytest.raises(EnvironmentError):
        settings._get_env_var_value(str(uuid.uuid4()))
