from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read()

with open(path.join(here, "version.txt")) as f:
    version = f.read()

setup(
    name="balrog",
    version=version,
    description="Mozilla's Update Server",
    author="Ben Hearsum",
    author_email="ben@hearsum.ca",
    packages=find_packages(exclude=["vendor"]),
    include_package_data=True,
    install_requires=requirements,
    url="https://github.com/mozilla/balrog",
)
