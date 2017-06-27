"""wiktionary.py
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
    """Wiktionary
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
        """set_lang
        """
        self.lang = lang
        self.set_parser()

    def set_x_sampa(self, x_sampa):
        """set_x_sampa
        """
        self.x_sampa = x_sampa
        self.set_parser()

    def set_parser(self):
        """set_parser
        """
        self.parser = Parser(
            lang=self.lang,
            x_sampa=self.x_sampa,
        )

    def get_entry_pronunciation(self, wiki_text):
        """get_entry_pronunciation
        """
        if self.lang:
            return self.parser.parse(wiki_text)[self.lang]
        return self.parser.parse(wiki_text)

    def lookup(self, word):
        """lookup
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
