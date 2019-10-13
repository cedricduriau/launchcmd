# stdlib modules
import os


def _get_env_var_value(env_var_name):
    """Returns the value of an environment variable, if set, raises otherwise.

    :rtype: str
    """
    value = os.getenv(env_var_name)
    if not value:
        msg = "environment variable {!r} is not set"
        raise EnvironmentError(msg.format(env_var_name))
    return value


PROJECT_ROOT = _get_env_var_value("LAUNCHCMD_PROJECT_ROOT")
SOFTWARE_ROOT = _get_env_var_value("LAUNCHCMD_SOFTWARE_ROOT")
