# stdlib modules
import os
from pathlib import Path


ROOT = Path(os.getenv("LCMD_ROOT_DIR", "~/.launchcmd")).absolute()
RELEASE_ROOT = os.path.join(ROOT, "released")
