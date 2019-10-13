# stdlib modules
import re

REGEX_PACKAGE_NAME = re.compile(r"^([a-zA-Z0-9]+)$")


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
