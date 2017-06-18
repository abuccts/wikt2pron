"""setup.py for pywiktionary
"""

from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pywiktionary",
    version="0.0.1.dev1",

    description="Toolkit converting pronunciation in enwiktionary xml dump to cmudict format",
    long_description=long_description,

    url="https://github.com/abuccts/enwiktionary2cmudict",

    author="Yifan Xiong",
    author_email="abuccts@gmail.com",

    license="BSD-2-Clause",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],

    keywords="wiktionary cmudict IPA parser",
    packages=find_packages(exclude=["contrib", "docs", "tests", "mwxml"]),
    install_requires=["mwxml"],
)
