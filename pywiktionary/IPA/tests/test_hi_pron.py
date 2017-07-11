# pylint: disable=anomalous-backslash-in-string
# pylint: disable=no-init, too-few-public-methods
"""Unittest for hi_pron.py
Testcases modified from https://en.wiktionary.org/wiki/Module:hi-IPA/testcases.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from six import with_metaclass

from .. import hi_pron


# Testcases for Hindi text to IPA conversion
TESTCASES = [
    # (text, IPA)
    ("मैं", "mɛ̃ː"),
    ("देश", "d̪eːʃ"),
    ("मेरा", "meː.ɾɑː"),
    ("खिलौना", "kʰɪ.lɔː.nɑː"),
    ("नौटंकी", "nɔː.ʈəŋ.kiː"),
    ("हौं", "ɦɔ̃ː"),
    ("मुँह", "mʊ̃ʱ"),
    ("माह", "mɑːʱ"),
    ("बहना", "bɛːʱ.nɑː"),
    ("विवाह", "ʋɪ.ʋɑːʱ"),
    ("ग़म", "ɡəm"),
    # ("ख़रगोश", "kʰəɾ.ɡoːʃ"), #FIXME
    ("इकट्ठा", "ɪ.kəʈ.ʈʰɑː"),
    ("संस्थान", "sən.st̪ʰɑːn"),
    ("मधु", "mə.d̪ʱʊ"), #FIXME
]


class TestHiPronMeta(type):
    """TestHiPron meta class
    """
    def __new__(mcs, name, bases, dicts):
        def gen_test_hi_to_IPA(hi_text, hi_IPA):
            """Generate hi text to IPA testcases.

            Parameters
            ----------
            hi_text : string
                String of Hindi text in {{hi-IPA}} template
                parsed from Wiktionary.
            hi_IPA : string
                String of expected Hindi IPA after conversion.

            Returns
            -------
            test: function
                AssertEqual of two texts.
            """
            def test(self):
                """AssertEqual of hi text and converted IPA.
                """
                return self.assertEqual(
                    hi_pron.to_IPA(hi_text),
                    hi_IPA
                )
            return test

        for i, (hi_text, hi_IPA) in enumerate(TESTCASES):
            test_hi_to_IPA_name = "test_hi_to_IPA_%06d" % i
            dicts[test_hi_to_IPA_name] = \
                gen_test_hi_to_IPA(hi_text, hi_IPA)
        return type.__new__(mcs, name, bases, dicts)


class TestHiPron(with_metaclass(TestHiPronMeta, unittest.TestCase)):
    """TestHiPron class
    """
    pass


if __name__ == "__main__":
    unittest.main()
