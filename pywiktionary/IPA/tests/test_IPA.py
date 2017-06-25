from __future__ import absolute_import
from __future__ import unicode_literals

try:
	import unittest2 as unittest
except ImportError:
	import unittest
from six import with_metaclass

from .. import IPA

TestData = [
    ("/ukrɑˈjɪnɑ/", "/ukrA\"jInA/"),
]

class TestIPAMeta(type):
	def __new__(mcs, name, bases, dict):
	
		def gen_test_IPA_to_XSAMPA(IPA_text, XSAMPA_text):
			def test(self):
				return self.assertEqual(IPA.IPA_to_XSAMPA(IPA_text), XSAMPA_text)
			return test
		
		for i, (IPA_text, CMUBET_text) in enumerate(TestData):
			test_IPA2CMUBET_name = "test_IPA_to_XSAMPA_%06d" % i
			dict[test_IPA_to_XSAMPA_name] = gen_test_IPA_to_XSAMPA(IPA_text, CMUBET_text)
		return type.__new__(mcs, name, bases, dict)

class TestIPA(with_metaclass(TestIPAMeta, unittest.TestCase)):
	pass

if __name__ == "__main__":
	unittest.main()
