#! /usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="balrogclient",
    version="0.0.1",
    description="Balrog Admin API Client",
    author="Release Engineers",
    author_email="release@mozilla.com",

    packages=['balrogclient'],

    test_suite='balrogclient.test',
    install_requires=[
        'requests',
    ],
    include_package_data=True,
)
