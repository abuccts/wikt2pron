# -*- coding: utf-8  -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import re
import json
try:
	from urllib import urlencode, urlopen
except ImportError:
	from urllib.parse import urlencode
	from urllib.request import urlopen

from pywiktionary.phoneme import IPA2CMUBET


POS = ["noun", "verb", "adjective", "adverb", "determiner", "abbreviation",
       "article", "preposition", "conjunction", "proper noun", "letter", 
	   "character", "phrase", "proverb", "idiom", "symbol", "syllable",
	   "numeral", "initialism", "interjection"]


class Parser(object):
	def __init__(self, lang=None, CMUBET=None, phoneme_only=None):
		self.lang = lang
		self.CMUBET = CMUBET
		self.phoneme_only = phoneme_only
		self.api = "https://en.wiktionary.org/w/api.php"
		self.param = {"action": "expandtemplates", "text": None, "prop": "wikitext", "format": "json"}
		self.regex = {
			"lang": re.compile("^lang="),
			"node": re.compile("{{([^}]+)}}"),
			"pronun": re.compile("\* ([^\n]+)\n"),
			"h2": re.compile("(?:\A|\n)={2}([a-zA-Z0-9 -]+)={2}\n"),
			"h3": re.compile("\n={3}([a-zA-Z0-9 -]+)={3}\n"),
			"h4": re.compile("\n={4}([a-zA-Z0-9 -]+)={4}\n"),
			"IPA": re.compile("<span[^>]*>([^<]+)<\/span>")
		}
	
	def expand_template(self, text):
		self.param["text"] = text.encode("utf-8")
		res = urlopen(self.api, urlencode(self.param).encode()).read()
		content = json.loads(res.decode("utf-8"))
		html = content["expandtemplates"]["wikitext"]
		return self.regex["IPA"].findall(html)
	
	def parse_details(self, text, depth=3):
		result = {}
		details_lst = self.regex["h" + str(depth)].findall(text)
		details_split = self.regex["h" + str(depth)].split(text)
		pronun_result = {}
		pos_result = []
		etymology_result = details_split[0] if depth == 4 else ""
		i = 0
		while i < len(details_split):
			if details_split[i] in details_lst:
				name = details_split[i].lower()
				if name == "pronunciation":
					pronun_result = self.parse_pronun(details_split[i + 1])
				elif name in POS:
					pos_result.append(details_split[i])
				elif "etymology" in name:
					if name == "etymology":
						etymology_result = details_split[i + 1]
					else:
						result[details_split[i]] = self.parse_details(details_split[i + 1], depth=4)
				i += 1
			i += 1
		if len(pronun_result) > 0:
			result["Pronunciation"] = pronun_result
		if len(pos_result) > 0:
			result["Part of Speech"] = pos_result
#		if len(etymology_result) > 0:
#			result["Etymology"] = etymology_result
		return result
	
	def parse_pronun(self, text):
		result = []
		pronun_lst = self.regex["pronun"].findall(text)
		for each in pronun_lst:
			item = {}
			accent_result = []
			enPR_result = []
			IPA_result = []
			audio_result = []
			node_lst = self.regex["node"].findall(each)
			for node in node_lst:
				node_detail = node.split("|")
				if node_detail[0] == "a":
					accent_result += node_detail[1:]
				elif node_detail[0] == "enPR":
					enPR_result += node_detail[1:]
				elif "IPA" in node_detail[0]:
					if node_detail[0] == "IPA":
						lang = re.sub(self.regex["lang"], "", node_detail[-1])
						IPA_result.append((node_detail[1:-1], lang))
					else:
						ipa_key = node_detail[0].split("-")
						if len(ipa_key) == 2 and ipa_key[1] == "IPA":
							IPA_result.append((self.expand_template("{{%s}}"%node), ipa_key[0]))
						else:
							IPA_result.append((["Unknown IPA."], "null"))
				elif node_detail[0] == "audio":
					lang = re.sub(self.regex["lang"], "", node_detail[-1])
					audio_result.append(tuple(node_detail[1:-1]) + (lang,))
			if len(accent_result) > 0:
				item["Accent"] = accent_result[0] if len(accent_result) == 1 else accent_result
			if len(enPR_result) > 0:
				item["enPR"] = enPR_result[0] if len(enPR_result) == 1 else enPR_result
			if len(IPA_result) > 0:
				item["IPA"] = IPA_result[0] if len(IPA_result) == 1 else IPA_result
				if self.CMUBET:
					CMUBET_result = []
					for ipa_lst, ipa_lang in IPA_result:
						cmubet_lst = []
						for ipa_pronun in ipa_lst:
							cmubet_pronun = IPA2CMUBET(ipa_pronun)
							cmubet_lst.append(cmubet_pronun)
						CMUBET_result.append(cmubet_lst)
					item["CMUBET"] = CMUBET_result[0] if len(CMUBET_result) == 1 else CMUBET_result
			if len(audio_result) > 0:
				item["Audio"] = audio_result[0] if len(audio_result) == 1 else audio_result
			if len(item) > 0:
				result.append(item)
		return result
	
	def parse(self, text):
		result = {}
		h2_lst = self.regex["h2"].findall(text)
		if self.lang not in h2_lst:
			return {self.lang: "language not found"}
		h2_split = self.regex["h2"].split(text)
		i = 0
		while i < len(h2_split):
			if h2_split[i] in h2_lst:
				if h2_split[i] == self.lang:
					result[h2_split[i]] = self.parse_details(h2_split[i + 1])
				i += 1
			i += 1
		
		if self.phoneme_only:
			pronunciations = []
			for h3 in sorted(result[self.lang].keys()):
				if h3 == "Pronunciation":
					pronunciations += result[self.lang][h3]
				elif "Etymology" in h3:
					for h4 in result[self.lang][h3]:
						if h4 == "Pronunciation":
							pronunciations += result[self.lang][h3][h4]
			ipa_lst, cmubet_lst = [], []
			for pronun in pronunciations:
				if "IPA" in pronun.keys():
					if isinstance(pronun["IPA"], list):
						for each in pronun["IPA"]:
							ipa_lst += each[0]
					else:
						ipa_lst += pronun["IPA"][0]
					if self.CMUBET:
						cmubet_lst += pronun["CMUBET"] if isinstance(pronun["CMUBET"][0], list) else [pronun["CMUBET"]]
			cmubet_lst = [x for l in cmubet_lst for x in l]
			return {"IPA": ipa_lst, "CMUBET": cmubet_lst} if self.CMUBET else {"IPA": ipa_lst}
		return result
