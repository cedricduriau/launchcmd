# stdlib modules
import os


def abs(path):
    return os.path.abspath(os.path.expanduser(path))


ROOT = os.path.abspath(os.path.expanduser(os.getenv("LCMD_ROOT_DIR", "~/.launchcmd")))
RELEASE_ROOT = os.path.join(ROOT, "released")
