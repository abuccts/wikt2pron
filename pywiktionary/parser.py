# pylint: disable=anomalous-backslash-in-string
# pylint: disable=too-many-locals, too-many-branches, too-many-statements
"""parser.py
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import re
import json
try:
    from urllib import urlencode, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen

from pywiktionary.phoneme import ipa2cmubet


POS = [
    "noun", "verb", "adjective", "adverb", "determiner", "abbreviation",
    "article", "preposition", "conjunction", "proper noun", "letter",
    "character", "phrase", "proverb", "idiom", "symbol", "syllable",
    "numeral", "initialism", "interjection",
]


class Parser(object):
    """Parser
    """
    def __init__(self, lang=None, cmubet=None, phoneme_only=None):
        self.lang = lang
        self.cmubet = cmubet
        self.phoneme_only = phoneme_only
        self.api = "https://en.wiktionary.org/w/api.php"
        self.param = {
            "action": "expandtemplates",
            "text": None,
            "prop": "wikitext",
            "format": "json"
        }
        self.regex = {
            "lang": re.compile("^lang="),
            "node": re.compile("{{([^}]+)}}"),
            "pronun": re.compile("\* ([^\n]+)\n"),
            "h2": re.compile("(?:\A|\n)={2}([a-zA-Z0-9 -]+)={2}\n"),
            "h3": re.compile("\n={3}([a-zA-Z0-9 -]+)={3}\n"),
            "h4": re.compile("\n={4}([a-zA-Z0-9 -]+)={4}\n"),
            "ipa": re.compile("<span[^>]*>([^<]+)<\/span>")
        }

    def expand_template(self, text):
        """expand_template
        """
        self.param["text"] = text.encode("utf-8")
        res = urlopen(self.api, urlencode(self.param).encode()).read()
        content = json.loads(res.decode("utf-8"))
        html = content["expandtemplates"]["wikitext"]
        return self.regex["ipa"].findall(html)

    def parse_details(self, text, depth=3):
        """parse_details
        """
        result = {}
        details_lst = self.regex["h" + str(depth)].findall(text)
        details_split = self.regex["h" + str(depth)].split(text)
        pronun_result = {}
        pos_result = []
        # etymology_result = details_split[0] if depth == 4 else ""
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
                        # etymology_result = details_split[i + 1]
                        pass
                    else:
                        result[details_split[i]] = \
                            self.parse_details(
                                details_split[i + 1],
                                depth=4
                            )
                i += 1
            i += 1
        if pronun_result:
            result["Pronunciation"] = pronun_result
        if pos_result:
            result["Part of Speech"] = pos_result
        # if len(etymology_result) > 0:
        #     result["Etymology"] = etymology_result
        return result

    def parse_pronun(self, text):
        """parse_pronun
        """
        result = []
        pronun_lst = self.regex["pronun"].findall(text)
        for each in pronun_lst:
            item = {}
            accent_result = []
            enpr_result = []
            ipa_result = []
            audio_result = []
            node_lst = self.regex["node"].findall(each)
            for node in node_lst:
                node_detail = node.split("|")
                if node_detail[0] == "a":
                    accent_result += node_detail[1:]
                elif node_detail[0] == "enpr":
                    enpr_result += node_detail[1:]
                elif "ipa" in node_detail[0]:
                    if node_detail[0] == "ipa":
                        lang = re.sub(self.regex["lang"], "", node_detail[-1])
                        ipa_result.append((node_detail[1:-1], lang))
                    else:
                        ipa_key = node_detail[0].split("-")
                        if len(ipa_key) == 2 and ipa_key[1] == "ipa":
                            ipa_result.append(
                                (self.expand_template("{{%s}}" % node),
                                 ipa_key[0])
                            )
                        else:
                            ipa_result.append(
                                (["Unknown ipa."],
                                 "null")
                            )
                elif node_detail[0] == "audio":
                    lang = re.sub(self.regex["lang"], "", node_detail[-1])
                    audio_result.append(tuple(node_detail[1:-1]) + (lang,))
            if accent_result:
                if len(accent_result) == 1:
                    item["Accent"] = accent_result[0]
                else:
                    item["Accent"] = accent_result
            if enpr_result:
                if len(enpr_result) == 1:
                    item["enpr"] = enpr_result[0]
                else:
                    item["enpr"] = enpr_result
            if ipa_result:
                if len(ipa_result) == 1:
                    item["ipa"] = ipa_result[0]
                else:
                    item["ipa"] = ipa_result
                if self.cmubet:
                    cmubet_result = []
                    for ipa_lst, _ in ipa_result:
                        cmubet_lst = []
                        for ipa_pronun in ipa_lst:
                            cmubet_pronun = ipa2cmubet(ipa_pronun)
                            cmubet_lst.append(cmubet_pronun)
                        cmubet_result.append(cmubet_lst)
                    if len(cmubet_result) == 1:
                        item["cmubet"] = cmubet_result[0]
                    else:
                        item["cmubet"] = cmubet_result
            if audio_result:
                if len(audio_result) == 1:
                    item["Audio"] = audio_result[0]
                else:
                    item["Audio"] = audio_result
            if item:
                result.append(item)
        return result

    def parse(self, text):
        """parse
        """
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
            for header3 in sorted(result[self.lang].keys()):
                if header3 == "Pronunciation":
                    pronunciations += result[self.lang][header3]
                elif "Etymology" in header3:
                    for header4 in result[self.lang][header3]:
                        if header4 == "Pronunciation":
                            pronunciations += \
                                result[self.lang][header3][header4]
            ipa_lst, cmubet_lst = [], []
            for pronun in pronunciations:
                if "ipa" in pronun.keys():
                    if isinstance(pronun["ipa"], list):
                        for each in pronun["ipa"]:
                            ipa_lst += each[0]
                    else:
                        ipa_lst += pronun["ipa"][0]
                    if self.cmubet:
                        if isinstance(pronun["cmubet"][0], list):
                            cmubet_lst += pronun["cmubet"]
                        else:
                            cmubet_lst += [pronun["cmubet"]]
            cmubet_lst = [x for l in cmubet_lst for x in l]
            if self.cmubet:
                return {"ipa": ipa_lst, "cmubet": cmubet_lst}
            return {"ipa": ipa_lst}
        return result
