#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='googlegeocodingcli',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=3.3',
        'requests>=2.5.1'
    ],
    entry_points='''
        [console_scripts]
        geocode=scripts.googlegeocodingcli:geocode
        reverse_geocode=scripts.googlegeocodingcli:reverse_geocode
    ''',

    author="Max Hurl",
    author_email="max@maxhurl.co.uk",
    description="This a CLI tool to geocode data files using the Google APIs",
    license="BSD",
)
