# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Modifiled from https://en.wiktionary.org/wiki/Module:ru-common Lua module partially.
Rewritten from Author: Benwing; some very early work by CodeCat and Atitarev

This module holds some commonly used functions for the Russian language.
It's generally for use from other modules, not #invoke, although some functions
can be invoked from a template (export.iotation(), export.reduce_stem(),
export.dereduce_stem() -- this was actually added to support calling from a
bot script rather than from a user template). There's also export.main(),
which supposedly can be used to invoke most functions in this module from a
template, but it may or may not work. There may also be issues when invoking
such functions from templates when transliteration is present, due to the
need for the transliteration to be decomposed, as mentioned below (all strings
from Wiktionary pages are normally in composed form).

NOTE NOTE NOTE: All functions assume that transliteration (but not Russian)
has had its acute and grave accents decomposed using export.decompose().
This is the first thing that should be done to all user-specified
transliteration and any transliteration we compute that we expect to work with.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unicodedata

import regex as re


AC = u"\u0301" # acute =  ́
GR = u"\u0300" # grave =  ̀
CFLEX = u"\u0302" # circumflex =  ̂
BREVE = u"\u0306" # breve  ̆
DIA = u"\u0308" # diaeresis =  ̈
CARON = u"\u030C" # caron  ̌

# any accent
accent = AC + GR + DIA + BREVE + CARON
# regex for any optional accent(s)
opt_accent = "[" + accent + "]*"
# any composed Cyrillic vowel with grave accent
composed_grave_vowel = "ѐЀѝЍ"
# any Cyrillic vowel except ёЁ
vowel_no_jo = "аеиоуяэыюіѣѵАЕИОУЯЭЫЮІѢѴ" + composed_grave_vowel
# any Cyrillic vowel, including ёЁ
vowel = vowel_no_jo + "ёЁ"
# any vowel in transliteration
tr_vowel = "aeěɛiouyAEĚƐIOUY"
# any consonant in transliteration, omitting soft/hard sign
tr_cons_no_sign = "bcčdfghjklmnpqrsštvwxzžBCČDFGHJKLMNPQRSŠTVWXZŽ"
# any consonant in transliteration, including soft/hard sign
tr_cons = tr_cons_no_sign + "ʹʺ"
# regex for any consonant in transliteration, including soft/hard sign,
# optionally followed by any accent
tr_cons_acc_re = "[" + tr_cons + "]" + opt_accent
# any Cyrillic consonant except sibilants and ц
cons_except_sib_c = "бдфгйклмнпрствхзьъБДФГЙКЛМНПРСТВХЗЬЪ"
# Cyrillic sibilant consonants
sib = "шщчжШЩЧЖ"
# Cyrillic sibilant consonants and ц
sib_c = sib + "цЦ"
# any Cyrillic consonant
cons = cons_except_sib_c + sib_c
# Cyrillic velar consonants
velar = "кгхКГХ"
# uppercase Cyrillic consonants
uppercase = "АЕИОУЯЭЫЁЮІѢѴБДФГЙКЛМНПРСТВХЗЬЪШЩЧЖЦ"

recomposer = {
    "и" + BREVE: "й",
    "И" + BREVE: "Й",
    "е" + DIA: "ё", # WARNING: Cyrillic е and Е
    "Е" + DIA: "Ё",
    "e" + CARON: "ě", # WARNING: Latin e and E
    "E" + CARON: "Ě",
    "c" + CARON: "č",
    "C" + CARON: "Č",
    "s" + CARON: "š",
    "S" + CARON: "Š",
    "z" + CARON: "ž",
    "Z" + CARON: "Ž",
    # used in ru-pron:
    "ж" + BREVE: "ӂ", # used in ru-pron
    "Ж" + BREVE: "Ӂ",
    "j" + CFLEX: "ĵ",
    "J" + CFLEX: "Ĵ",
    "j" + CARON: "ǰ",
    # no composed uppercase equivalent of J-caron
    "ʒ" + CARON: "ǯ",
    "Ʒ" + CARON: "Ǯ",
}

grave_deaccenter = {
    GR: "", # grave accent
    "ѐ": "е", # composed Cyrillic chars w/grave accent
    "Ѐ": "Е",
    "ѝ": "и",
    "Ѝ": "И",
}


# Decompose acute, grave, etc. on letters (esp. Latin) into individivual
# character + combining accent. But recompose Cyrillic and Latin characters
# that we want to treat as units and get caught in the crossfire. We mostly
# want acute and grave decomposed; perhaps should just explicitly decompose
# those and no others.
def decompose(text):
    def repl(match):
        k = match.group()
        if k in recomposer.keys():
            return recomposer[k]
        return k
    text = unicodedata.normalize("NFD", text)
    text = re.sub(".[" + BREVE + DIA + CARON + "]", repl, text)
    return text

# Remove grave accents; don't affect acute or composed diaeresis in ёЁ or
# uncomposed diaeresis in -ѣ̈- (as in plural сѣ̈дла of сѣдло́).
# NOTE: Translit must already be decomposed! See comment at top.
def remove_grave_accents(word):
    def repl(match):
        k = match.group()
        if k in grave_deaccenter.keys():
            return grave_deaccenter[k]
        return k
    ru_removed = re.sub("[̀ѐЀѝЍ]", repl, word)
    return ru_removed
