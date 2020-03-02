from glob import glob
from os import path
from os.path import basename, splitext

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))
# We're using a pip8 style requirements file, which allows us to embed hashes
# of the packages in it. However, setuptools doesn't support parsing this type
# of file, so we need to strip those out before passing the requirements along
# to it.
with open(path.join(here, "requirements", "base.txt")) as f:
    requirements = []
    for line in f:
        # Skip empty and comment lines
        if not line.strip() or line.strip().startswith("#"):
            continue
        # Skip lines with hash values
        if not line.strip().startswith("--"):
            requirements.append(line.split(";")[0].split()[0])
            requirement_without_python_filter = line.split(";")[0]
            requirement_without_trailing_characters = requirement_without_python_filter.split()[0]

with open(path.join(here, "version.txt")) as f:
    version = f.read().strip()

setup(
    name="balrog",
    version=version,
    description="Mozilla's Update Server",
    author="Mozilla Release Engineering",
    author_email="release@mozilla.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=requirements,
    test_suite="tests",
    url="https://github.com/mozilla-releng/balrog",
    license="MPL-2.0",
    zip_safe=False,
    entry_points={"console_scripts": ["migrate_releases_table_data = auslib.cli.migrate_releases_table_data:cmd",],},
)
