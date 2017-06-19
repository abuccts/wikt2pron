"""wiktionary.py
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from pywiktionary.parser import Parser


class Wiktionary(object):
    """Wiktionary
    """
    def __init__(self, lang=None, x_sampa=False):
        self.lang = lang
        self.x_sampa = x_sampa
        self.set_parser()

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
            return parser.parse(wiki_text)[self.lang]
        return parser.parse(wiki_text)
