# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
try:
	from urllib import urlencode, urlopen
except ImportError:
	from urllib.parse import urlencode
	from urllib.request import urlopen

from pywiktionary.parser import Parser


class Wiktionary(object):
	def __init__(self, lang="English", CMUBET=True, phoneme_only=False):
		self.lang = lang
		self.CMUBET = CMUBET
		self.phoneme_only = phoneme_only

	def set_lang(self, lang):
		self.lang = lang

	def pronun(self, text, lang=None, CMUBET=None, phoneme_only=None):
		lang = self.lang if lang is None else lang
		CMUBET = self.CMUBET if CMUBET is None else CMUBET
		phoneme_only = self.phoneme_only if phoneme_only is None else phoneme_only
		if lang != "English":
			CMUBET = False
		parser = Parser(lang=lang, CMUBET=CMUBET, phoneme_only=phoneme_only)

		return parser.parse(text)
		