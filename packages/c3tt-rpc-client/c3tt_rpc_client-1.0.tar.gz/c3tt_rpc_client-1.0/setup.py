#!/usr/bin/env python3

from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='c3tt_rpc_client',
      version='1.0',
      description='Client-Library for https://github.com/crs-tools/tracker',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='C3VOC',
      author_email='voc+pypi@c3voc.de',
      url='https://github.com/voc/c3tt_rpc_client',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Operating System :: OS Independent",
          "Development Status :: 5 - Production/Stable",
      ],
      zip_safe=True)
