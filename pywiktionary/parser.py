# pylint: disable=anomalous-backslash-in-string
# pylint: disable=too-many-locals, too-many-branches, too-many-statements
"""Parser to extract IPA text from pronunciation section in wiki text.
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

from bs4 import BeautifulSoup
from .IPA import IPA


class Parser(object):
    """Wiktionary parser to extract IPA text from pronunciation section.

    To extraction IPA for a certain language, specify ``lang`` parameter,
    default is extracting IPA for all available languages.

    To convert IPA text to X-SAMPA text, use ``XSAMPA`` parameter.

    Parameters
    ----------
    lang : string
        String of language type.
    XSAMPA : boolean
        Option for IPA to X-SAMPA conversion.
    """
    def __init__(self, lang=None, XSAMPA=False):
        self.lang = lang
        self.XSAMPA = XSAMPA
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
            "IPA": re.compile("<span[^>]*>([^<]+)<\/span>")
        }

    def expand_template(self, text):
        """Expand IPA Template through Wiktionary API.

        Used to expand ``{{*-IPA}}`` template in parser and return IPA list.

        Parameters
        ----------
        text : string
            String of template text inside "{{" and "}}".

        Returns
        -------
        list of string
            List of expanded IPA text.

        Examples
        --------
        >>> parser = Parser()
        >>> template = "{{la-IPA|eccl=yes|thēsaurus}}"
        >>> parser.expand_template(template)
        ['/tʰeːˈsau̯.rus/', '[tʰeːˈsau̯.rʊs]', '/teˈsau̯.rus/']
        """
        self.param["text"] = text.encode("utf-8")
        res = urlopen(self.api, urlencode(self.param).encode()).read()
        content = json.loads(res.decode("utf-8"))
        html = content["expandtemplates"]["wikitext"]
        # Use BeautifulSoup instead of raw regex expr
        # return self.regex["IPA"].findall(html)
        soup = BeautifulSoup(html, "html.parser")
        span = soup.find_all("span", {"class": "IPA"})
        return list(map(lambda x: x.text, span))

    def parse(self, wiki_text):
        """Parse Wiktionary wiki text.

        Split Wiktionary wiki text into different langugaes and return
        parseed IPA result.

        Parameters
        ----------
        wiki_text : string
            String of Wiktionary wiki text, from XML dump or Wiktionary API.

        Returns
        -------
        dict
            Dict of parsed IPA results.
            Key: language name; Value: list of IPA text.
        """
        parse_result = {}
        h2_lst = self.regex["h2"].findall(wiki_text)
        if self.lang and self.lang not in h2_lst:
            parse_result = {self.lang: "Language not found."}
            return parse_result
        h2_split = self.regex["h2"].split(wiki_text)
        i = 0
        while i < len(h2_split):
            if h2_split[i] in h2_lst:
                if not self.lang or h2_split[i] == self.lang:
                    pronunciation = self.parse_detail(h2_split[i+1])
                    if not pronunciation:
                        pronunciation = "IPA not found."
                    parse_result[h2_split[i]] = pronunciation
                i += 1
            i += 1
        return parse_result

    def parse_detail(self, wiki_text, depth=3):
        """Parse the section of a certain language in wiki text.

        Parse pronunciation section of the certain language recursively.

        Parameters
        ----------
        wiki_text : string
            String of wiki text in a language section.
        depth : int
            Integer indicated depth of pronunciation section.

        Returns
        -------
        list of dict
            List of extracted IPA text in
            ``{"IPA": "", "X-SAMPA": "", "lang": ""}`` format.
        """
        parse_result = []
        detail_lst = self.regex["h" + str(depth)].findall(wiki_text)
        detail_split = self.regex["h" + str(depth)].split(wiki_text)
        # To avoid maximum recursion depth exceeded.
        if len(detail_split) > 99999:
            return "Maximum recursion depth exceeded in wiki text."
        i = 0
        while i < len(detail_split):
            if detail_split[i] in detail_lst:
                header_name = detail_split[i].lower()
                if header_name == "pronunciation":
                    parse_result += \
                        self.parse_pronunciation(detail_split[i+1])
                elif ("etymology" in header_name and
                      header_name != "etymology"):
                    parse_result += \
                        self.parse_detail(detail_split[i+1], depth=4)
                i += 1
            i += 1
        return parse_result

    def parse_pronunciation(self, wiki_text):
        """Parse pronunciation section in wiki text.

        Parse IPA text from pronunciation section and convert to X-SAMPA.

        Parameters
        ----------
        wiki_text : string
            String of pronunciation section in wiki text.

        Returns
        -------
        list of dict
            List of extracted IPA text in
            ``{"IPA": "", "X-SAMPA": "", "lang": ""}`` format.
        """
        parse_result = []
        pronun_lst = self.regex["pronun"].findall(wiki_text)
        for each in pronun_lst:
            node_lst = self.regex["node"].findall(each)
            for node in node_lst:
                node_detail = node.split("|")
                if "IPA" in node_detail[0]:
                    if node_detail[0] == "IPA":
                        lang = re.sub(self.regex["lang"], "", node_detail[-1])
                        for each_ipa in node_detail[1:-1]:
                            parse_result.append({
                                "IPA": each_ipa,
                                "lang": lang,
                            })
                    else:
                        ipa_key = node_detail[0].split("-")
                        if len(ipa_key) == 2 and ipa_key[1] == "IPA":
                            extend_lst = self.expand_template("{{%s}}" % node)
                            for each_ipa in extend_lst:
                                parse_result.append({
                                    "IPA": each_ipa,
                                    "lang": ipa_key[0],
                                })
                        else:
                            parse_result.append({
                                "IPA": "Unknown IPA.",
                                "lang": "null",
                            })
        if self.XSAMPA:
            for item in parse_result:
                item.update({
                    "X-SAMPA": IPA.IPA_to_XSAMPA(item["IPA"]),
                })
        return parse_result
