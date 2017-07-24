# pylint: disable=anomalous-backslash-in-string
# pylint: disable=no-init, too-few-public-methods
"""Unittest for es_pron.py
Testcases modified from https://en.wiktionary.org/wiki/Module:es-pronunc/testcases.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from six import with_metaclass

from .. import es_pron


# Testcases for Spanish text to IPA conversion
TESTCASES = [
    # (text, IPA)
    ("baca", "ˈbaka"),
    ("la baca", "laˈβaka"),
    ("enviar", "ẽmˈbjaɾ"),
    ("dama", "ˈd̪ama"),
    ("la dama", "laˈðama"),
    ("nada", "ˈnaða"),
    ("sabiendo", "saˈβjẽn̪d̪o"),
    ("hiena", "ˈɟ͡ʝena"),
    ("la hiena", "laˈʝena"),
    ("yaca", "ˈɟ͡ʝaka"),
    ("la yaca", "laˈʝaka"),
    ("cónyuge", "ˈkõɲɟ͡ʝuxe"),
    ("guerra", "ˈɡera"),
    ("la guerra", "laˈɣera"),
    ("Domingo", "d̪oˈmĩŋɡo"),
    ("chile", "ˈt͡ʃile"),
    ("el chile", "elˈt͡ʃile"),
]


class TestEsPronMeta(type):
    """TestEsPron meta class
    """
    def __new__(mcs, name, bases, dicts):
        def gen_test_es_to_IPA(es_text, es_IPA):
            """Generate es text to IPA testcases.

            Parameters
            ----------
            es_text : string
                String of Spanish text in {{es-IPA}} template
                parsed from Wiktionary.
            es_IPA : string
                String of expected Spanish IPA after conversion.

            Returns
            -------
            test: function
                AssertEqual of two texts.
            """
            def test(self):
                """AssertEqual of es text and converted IPA.
                """
                return self.assertEqual(
                    es_pron.to_IPA(es_text),
                    es_IPA
                )
            return test

        for i, (es_text, es_IPA) in enumerate(TESTCASES):
            test_es_to_IPA_name = "test_es_to_IPA_%06d" % i
            dicts[test_es_to_IPA_name] = \
                gen_test_es_to_IPA(es_text, es_IPA)
        return type.__new__(mcs, name, bases, dicts)


class TestEsPron(with_metaclass(TestEsPronMeta, unittest.TestCase)):
    """TestEsPron class
    """
    pass


if __name__ == "__main__":
    unittest.main()
