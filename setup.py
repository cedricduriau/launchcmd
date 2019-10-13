# stdlib modules
from setuptools import setup, find_packages


setup(name="launchcmd",
      version="0.1.0",
      description="Lightweight software packaging and deployment tool.",
      license="MIT",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/launchcmd",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/_launchcmd", "bin/releasepackage"])
