from setuptools import setup,find_packages
from pathlib import Path
log_desc= Path("README.md").read_text()
setup(
    name="holamundoplayer1",
    version="0.0.1",
    long_description=log_desc,
    packages=find_packages(
        exclude=["mocks","tests"]
    )
)