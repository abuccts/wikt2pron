# pylint: disable=anomalous-backslash-in-string
# pylint: disable=no-init, too-few-public-methods
"""Unittest for IPA.py.
Testcases modified from https://en.wiktionary.org/wiki/Module:IPA/testcases.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from six import with_metaclass

from .. import IPA


# Testcases for IPA text and X-SAMPA text conversion
TESTCASES = [
    # (IPA, XSAMPA)
    # en: [[dictionary]] https://en.wiktionary.org/wiki/dictionary
    ("/ˈdɪkʃən(ə)ɹi/", "/\"dIkS@n(@)r\\i/"),
    ("/ˈdɪkʃənɛɹi/", "/\"dIkS@nEr\\i/"),
    # en: [[battleship]] https://en.wiktionary.org/wiki/battleship
    ("[ˈbætl̩ʃɪp]", "[\"b{tl=SIp]"),
    # en: [[murder]] https://en.wiktionary.org/wiki/murder
    ("[ˈmɝdɚ]", "[\"m3`d@`]"),
    # en: [[dazzle]] https://en.wiktionary.org/wiki/dazzle
    ("/ˈdæzl̩/", "/\"d{zl=/"),
    # en: [[change]] https://en.wiktionary.org/wiki/change
    ("/t͡ʃeɪnd͡ʒ/", "/t__SeInd__Z/"),
    # uk: [[Україна]] https://en.wiktionary.org/wiki/Україна
    ("/ukrɑˈjɪnɑ/", "/ukrA\"jInA/"),
    # fa: [[نوروز]] https://en.wiktionary.org/wiki/نوروز
    ("[næu̯ˈɾoːz]", "[n{u_^\"4o:z]"),
    ("[nou̯ˈɾuːz]", "[nou_^\"4u:z]"),
    ("[noːˈɾuːz]", "[no:\"4u:z]"),
    ("[næu̯ˈɾɵːz]", "[n{u_^\"48:z]"),
    # cmn: [[新年]] https://en.wiktionary.org/wiki/新年
    ("[ɕɪn˥˥niɛn˧˥]", "[s\In__T__TniEn__M__T]"),
    # yue: [[唔]] https://en.wiktionary.org/wiki/唔
    ("[ŋ̍˩˨]", "[N=__B__L]"),
    # ga: [[báid]] https://en.wiktionary.org/wiki/báid
    #     [[bád]]  https://en.wiktionary.org/wiki/bád
    ("[bˠɑːdʲ]", "[b_GA:d_j]"),
    ("[bˠɑːd̪ˠ]", "[b_GA:d_d_G]"),
    # nl: [[crème]] https://en.wiktionary.org/wiki/crème
    ("/krɛ(ː)m/", "/krE(:)m/"),
]


class TestIPAMeta(type):
    """TestIPA meta class
    """
    def __new__(mcs, name, bases, dicts):
        def gen_test_IPA_to_XSAMPA(IPA_text, XSAMPA_text):
            """Generate IPA to X-SAMPA testcases.

            Parameters
            ----------
            IPA_text : string
                String of IPA text parsed from Wiktionary.
            XSAMPA_text : string
                String of expected X-SAMPA text after conversion.

            Returns
            -------
            test: function
                AssertEqual of two texts.
            """
            def test(self):
                """AssertEqual of IPA text and converted X-SAMPA text.
                """
                return self.assertEqual(
                    IPA.IPA_to_XSAMPA(IPA_text),
                    XSAMPA_text
                )
            return test

        for i, (IPA_text, XSAMPA_text) in enumerate(TESTCASES):
            test_IPA_to_XSAMPA_name = "test_IPA_to_XSAMPA_%06d" % i
            dicts[test_IPA_to_XSAMPA_name] = \
                gen_test_IPA_to_XSAMPA(IPA_text, XSAMPA_text)
        return type.__new__(mcs, name, bases, dicts)


class TestIPA(with_metaclass(TestIPAMeta, unittest.TestCase)):
    """TestIPA class
    """
    pass


if __name__ == "__main__":
    unittest.main()
