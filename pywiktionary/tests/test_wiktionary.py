# pylint: disable=no-init, too-few-public-methods
"""Unittest for wiktionary.py.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from six import with_metaclass

from ..wiktionary import Wiktionary


# Testcases for extracting IPA from XML dump
XML_DUMP_FILE = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "../data/enwiktionary-test-pages-articles-multistream.xml",
))
XML_DUMP_CASES = [
    # en: [[dictionary]] https://en.wiktionary.org/wiki/dictionary
    {
        "id": 16,
        "title": "dictionary",
        "pronunciation": [
            {"IPA": "/ˈdɪkʃ(ə)n(ə)ɹɪ/", "lang": "en"},
            {"IPA": "/ˈdɪkʃənɛɹi/", "lang": "en"},
        ],
    },
    # en: [[battleship]] https://en.wiktionary.org/wiki/battleship
    {
        "id": 65195,
        "title": "battleship",
        "pronunciation": "IPA not found.",
    },
    # en: [[murder]] https://en.wiktionary.org/wiki/murder
    {
        "id": 39478,
        "title": "murder",
        "pronunciation": [
            {"IPA": "/ˈmɜːdə(ɹ)/", "lang": "en"},
            {"IPA": "/ˈmɝ.dɚ/", "lang": "en"},
        ],
    },
    # en: [[dazzle]] https://en.wiktionary.org/wiki/dazzle
    {
        "id": 80141,
        "title": "dazzle",
        "pronunciation": [
            {"IPA": "/ˈdæzəl/", "lang": "en"},
        ],
    },
]


class TestWiktionaryMeta(type):
    """TestWiktionary meta class
    """
    def __new__(mcs, name, bases, dicts):
        def gen_test_extract_IPA(extract_result, expected_result):
            """Generate XML dump IPA extraction testcases.

            Parameters
            ----------
            extract_result : dict
                Extract IPA result from XML dump.
            expected_result : dict
                Expected IPA result for XML dump.

            Returns
            -------
            test: function
                AssertDictEqual of two dicts.
            """
            def test(self):
                """AssertDictEqual of extract result and expected result.
                """
                return self.assertDictEqual(extract_result, expected_result)
            return test

        wikt = Wiktionary(lang="English", XSAMPA=False)
        extract_results = wikt.extract_IPA(XML_DUMP_FILE)
        assert len(extract_results) == len(XML_DUMP_CASES)
        for i, (extract_result, expected_result) in \
                enumerate(zip(extract_results, XML_DUMP_CASES)):
            test_extract_IPA_name = "test_extract_IPA_%06d" % i
            dicts[test_extract_IPA_name] = \
                gen_test_extract_IPA(extract_result, expected_result)
        return type.__new__(mcs, name, bases, dicts)


class TestWiktionary(
        with_metaclass(TestWiktionaryMeta, unittest.TestCase)):
    """TestWiktionary class
    """
    pass


if __name__ == "__main__":
    unittest.main()
