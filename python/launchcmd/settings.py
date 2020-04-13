# stdlib modules
import os


def abs(path):
    return os.path.abspath(os.path.expanduser(path))


ROOT = abs(os.getenv("LC_ROOT_DIR", "~/.launchcmd"))
RELEASE_ROOT = os.path.join(ROOT, "released")
CURRENT_LOCATION = abs(os.getenv("LC_CURRENT_LOCATION", ""))
