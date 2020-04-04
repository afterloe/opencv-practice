#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from setuptools import setup

PROJECT_NAME = "meter_reader_4_pointer"
VERSION = "1.2.0"

setup(
    name=PROJECT_NAME,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["opencv-python", "pyyaml", "imutils"],
)
