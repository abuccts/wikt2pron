"""Wiktionary class for IPA extraction from XML dump or MediaWiki API.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
try:
    from urllib import urlencode, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen

from .parser import Parser


class Wiktionary(object):
    """Wiktionary class for IPA extraction from XML dump or MediaWiki API.

    To extraction IPA for a certain language, specify `lang` parameter,
    default is extracting IPA for all available languages.

    To convert IPA text to X-SAMPA text, use `x_sampa` parameter.

    Parameters
    ----------
    lang : string
        String of language type.
    x_sampa : boolean
        Option for IPA to X-SAMPA conversion.
    """
    def __init__(self, lang=None, x_sampa=False):
        self.lang = lang
        self.x_sampa = x_sampa
        self.set_parser()
        self.api = "https://en.wiktionary.org/w/api.php"
        self.param = {
            "action": "query",
            "titles": None,
            "prop": "revisions",
            "rvprop": "content",
            "rvlimit": 1,
            "format": "json"
        }

    def set_lang(self, lang):
        """Set language.

        Parameters
        ----------
        lang : string
            String of language name.
        """
        self.lang = lang
        self.set_parser()

    def set_x_sampa(self, x_sampa):
        """Set X-SAMPA conversion option.

        Parameters
        ----------
        x_sampa : boolean
            Option for IPA to X-SAMPA conversion.
        """
        self.x_sampa = x_sampa
        self.set_parser()

    def set_parser(self):
        """Set parser for Wiktionary.

        Use the Wiktionary `lang` and `x_sampa` parameters.
        """
        self.parser = Parser(
            lang=self.lang,
            x_sampa=self.x_sampa,
        )

    def get_entry_pronunciation(self, wiki_text):
        """Extraction IPA for entry in Wiktionary XML dump.

        Parameters
        ----------
        wiki_text : string
            String of XML entry wiki text.

        Returns
        -------
        dict
            Dict of word's IPA results.
            Key: language name; Value: list of IPA text.
        """
        if self.lang:
            return self.parser.parse(wiki_text)[self.lang]
        return self.parser.parse(wiki_text)

    def lookup(self, word):
        """Look up IPA of word through Wiktionary API.

        Parameters
        ----------
        word : string
            String of a word to be looked up.

        Returns
        -------
        dict
            Dict of word's IPA results.
            Key: language name; Value: list of IPA text.
        """
        self.param["titles"] = word.encode("utf-8")
        param = urlencode(self.param).encode()
        res = urlopen(self.api, param).read()
        content = json.loads(res.decode("utf-8"))
        try:
            val = list(content["query"]["pages"].values())
            wiki_text = val[0]["revisions"][0]["*"]
        except (KeyError, IndexError):
            return "Word not found."
        else:
            return
        return self.get_entry_pronunciation(wiki_text)
