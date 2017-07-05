"""`Wiktionary pronunciation collector`

A Python toolkit converting pronunciation in enwiktionary xml dump
to cmudict format. Support `IPA`_ and `X-SAMPA`_ format at present.

.. _IPA: https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
.. _X-SAMPA: https://en.wikipedia.org/wiki/X-SAMPA
"""

from .wiktionary import Wiktionary
from .parser import Parser
from .IPA import IPA


__author__ = "Yifan Xiong"
__version__ = "0.0.2"
__email__ = "abuccts@gmail.com"
