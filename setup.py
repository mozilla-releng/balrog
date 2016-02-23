from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))
f = open(path.join(here, "requirements.txt"))
requirements = f.read()
f.close()

setup(
    name="balrog",
    version="1.0",
    description="Mozilla's Update Server",
    author="Ben Hearsum",
    author_email="ben@hearsum.ca",
    packages=find_packages(exclude=["vendor"]),
    include_package_data=True,
    install_requires=requirements,
    url="https://github.com/mozilla/balrog",
)
