# stdlib modules
import os
import sys
from setuptools import setup
from setuptools import find_packages

# tool modules
f = os.path.abspath(__file__)
package_dir = os.path.join(os.path.dirname(f), "python")
sys.path.insert(0, package_dir)
from launchcmd import __version__  # noqa

requirements_dev = ["flake8", "radon", "flake8-polyfill"]


setup(name="launchcmd",
      version=__version__,
      description="Lightweight software and enviroment manager.",
      license="GPLv3",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/launchcmd",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/launchcmd"],
      extras_require={"dev": requirements_dev},
      data_files=[(os.path.expanduser("~/.launchcmd/released"), [])])
