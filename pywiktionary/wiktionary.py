"""wiktionary.py
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from pywiktionary.parser import Parser


class Wiktionary(object):
    """Wiktionary
    """
    def __init__(self, lang="English", cmubet=True, phoneme_only=False):
        self.lang = lang
        self.cmubet = cmubet
        self.phoneme_only = phoneme_only

    def set_lang(self, lang):
        """set_lang
        """
        self.lang = lang

    def pronun(self, text, lang=None, cmubet=None, phoneme_only=None):
        """pronun
        """
        lang = lang if lang else self.lang
        cmubet = cmubet if cmubet else self.cmubet
        phoneme_only = phoneme_only if phoneme_only else self.phoneme_only
        result = {}
        if isinstance(lang, list):
            for eachlang in lang:
                if eachlang != "English":
                    cmubet = False
                parser = Parser(
                    lang=eachlang,
                    cmubet=cmubet,
                    phoneme_only=phoneme_only
                )
                result[eachlang] = parser.parse(text)[eachlang]
        else:
            if lang != "English":
                cmubet = False
            parser = Parser(
                lang=lang,
                cmubet=cmubet,
                phoneme_only=phoneme_only
            )
            result[lang] = parser.parse(text)[lang]

        # return parser.parse(text)
        return result
