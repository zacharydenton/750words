#!/usr/bin/env python
from distutils.core import setup

setup(
    name="750words",
    description="Write 750 words daily on the command line.",
    author="Zach Denton",
    author_email="z@chdenton.com",
    version="0.4",
    long_description=open('README.md').read(),
    scripts=['750words']
)
