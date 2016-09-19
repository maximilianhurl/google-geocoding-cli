#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='googlegeocodingcli',
    version='0.2',
    url='https://github.com/maximilianhurl/google-geocoding-cli',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=6.6',
        'requests>=2.11.1',
        'six>=1.10.0'
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
