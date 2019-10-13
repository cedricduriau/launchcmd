# tool modules
from launchcmd import packageutils

# third party modules
import pytest


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
