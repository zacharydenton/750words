#!/usr/bin/env python

from distutils.core import setup
import sevenfifty

setup (
    name = "sevenfifty",
    description = "Write 750 words daily on the command line.",

    author = sevenfifty.__author__,
    author_email = sevenfifty.__author_email__,
    version = sevenfifty.__version__,
    url = sevenfifty.__url__,
    long_description = sevenfifty.__longdescr__,
    classifiers = sevenfifty.__classifiers__,
    packages = ['sevenfifty',
               ],
    scripts = ['750words'],
    requires = ['nltk']
)
