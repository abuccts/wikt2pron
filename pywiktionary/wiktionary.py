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

import mwxml
from .parser import Parser


class Wiktionary(object):
    """Wiktionary class for IPA extraction from XML dump or MediaWiki API.

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

    def set_XSAMPA(self, XSAMPA):
        """Set X-SAMPA conversion option.

        Parameters
        ----------
        XSAMPA : boolean
            Option for IPA to X-SAMPA conversion.
        """
        self.XSAMPA = XSAMPA
        self.set_parser()

    def set_parser(self):
        """Set parser for Wiktionary.

        Use the Wiktionary ``lang`` and ``XSAMPA`` parameters.
        """
        self.parser = Parser(
            lang=self.lang,
            XSAMPA=self.XSAMPA,
        )

    def get_entry_pronunciation(self, wiki_text, title=None):
        """Extraction IPA for entry in Wiktionary XML dump.

        Parameters
        ----------
        wiki_text : string
            String of XML entry wiki text.
        title: string
            String of wiki entry title.

        Returns
        -------
        dict
            Dict of word's IPA results.
            Key: language name; Value: list of IPA text.
        """
        if self.lang:
            return self.parser.parse(wiki_text, title=title)[self.lang]
        return self.parser.parse(wiki_text, title=title)

    def extract_IPA(self, dump_file):
        """Extraction IPA list from Wiktionary XML dump.

        Parameters
        ----------
        dump_file : string
            Path of Wiktionary XML dump file.

        Returns
        -------
        list
            List of extracted IPA results in
            ``{"id": "", "title": "", "pronunciation": ""}`` format.
        """
        dump = mwxml.Dump.from_file((open(dump_file, "rb")))
        lst = []
        for page in dump:
            for revision in page:
                if revision.page.namespace == 0:
                    pronunciation = self.get_entry_pronunciation(
                        revision.text,
                        title=revision.page.title,
                    )
                    lst.append({
                        "id": revision.page.id,
                        "title": revision.page.title,
                        "pronunciation": pronunciation,
                    })
        return lst

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
        return self.get_entry_pronunciation(wiki_text, title=word)
