import six
from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))
# We're using a pip8 style requirements file, which allows us to embed hashes
# of the packages in it. However, setuptools doesn't support parsing this type
# of file, so we need to strip those out before passing the requirements along
# to it.
with open(path.join(here, 'requirements.txt')) as f:
    requirements = []
    for line in f:
        # Skip lines with hash values
        if not line.strip().startswith("--"):
            version_skip = [
                "python_version=='2" in line and not six.PY2,
                "python_version=='3" in line and not six.PY3,
                "python_version>='3" in line and not six.PY3,
            ]
            if any(version_skip):
                continue
            requirements.append(line.split(';')[0].split()[0])


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
    license="MPL-2.0",
)
