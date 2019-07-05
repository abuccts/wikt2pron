"""Setup for pywiktionary.
"""

import sys
from os import path
from setuptools import setup, find_packages

if sys.version_info[0] == 2:
    raise RuntimeError("Python 3 needed.")

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pywiktionary",
    version="0.0.3",

    description="A Python toolkit converting pronunciation in enwiktionary xml dump to cmudict format",
    long_description=long_description,

    url="https://github.com/abuccts/wikt2pron",

    author="Yifan Xiong",
    author_email="abuccts@gmail.com",

    license="BSD-2-Clause",

    keywords="wiktionary cmudict IPA parser",
    packages=find_packages(exclude=["contrib", "docs", "tests", "mwxml"]),
    install_requires=["regex", "mwxml", "beautifulsoup4", "six"],
    tests_require = ["nose", "pylint"],
    test_suite="nose.collector",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
