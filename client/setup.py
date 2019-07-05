#! /usr/bin/env python

from setuptools import setup

setup(
    name="balrogclient",
    version="0.5.0",
    description="Balrog Admin API Client",
    author="Mozilla Release Engineers",
    author_email="release+python@mozilla.com",
    url="https://github.com/mozilla/balrog",
    license="MPL-2.0",
    packages=["balrogclient"],
    test_suite="balrogclient.test",
    install_requires=["requests"],
    include_package_data=True,
)
