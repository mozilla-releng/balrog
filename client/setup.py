from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="balrogclient",
    version="1.4",
    description="Balrog Admin API Client",
    author="Mozilla Release Engineers",
    author_email="release+python@mozilla.com",
    url="https://github.com/mozilla-releng/balrog",
    license="MPL-2.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=["requests"],
    test_suite="tests",
)
