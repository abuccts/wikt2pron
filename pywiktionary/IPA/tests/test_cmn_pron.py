# pylint: disable=anomalous-backslash-in-string
# pylint: disable=no-init, too-few-public-methods
"""Unittest for cmn_pron.py
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from six import with_metaclass

from .. import cmn_pron


# Testcases for Mandari text to IPA conversion
TESTCASES = [
    # (text, IPA)
    ("pīnyīn", "pʰin⁵⁵ in⁵⁵"),
    ("一", "i⁵⁵"),
    ("不", "pu⁵¹"),
    ("一不", "⁵⁵⁻³⁵ pu⁵¹"),
    ("不一", "pu⁵¹ i⁵⁵"),
]


class TestCmnPronMeta(type):
    """TestCmnPron meta class
    """
    def __new__(mcs, name, bases, dicts):
        def gen_test_cmn_to_IPA(cmn_text, cmn_IPA):
            """Generate cmn text to IPA testcases.

            Parameters
            ----------
            cmn_text : string
                String of Mandari text in "|m=" parameter of
                {{zh-pron}} template parsed from Wiktionary.
            cmn_IPA : string
                String of expected Mandari IPA after conversion.

            Returns
            -------
            test: function
                AssertEqual of two texts.
            """
            def test(self):
                """AssertEqual of cmn text and converted IPA.
                """
                return self.assertEqual(
                    cmn_pron.to_IPA(cmn_text),
                    cmn_IPA
                )
            return test

        for i, (cmn_text, cmn_IPA) in enumerate(TESTCASES):
            test_cmn_to_IPA_name = "test_cmn_to_IPA_%06d" % i
            dicts[test_cmn_to_IPA_name] = \
                gen_test_cmn_to_IPA(cmn_text, cmn_IPA)
        return type.__new__(mcs, name, bases, dicts)


class TestCmnPron(with_metaclass(TestCmnPronMeta, unittest.TestCase)):
    """TestCmnPron class
    """
    pass


if __name__ == "__main__":
    unittest.main()
