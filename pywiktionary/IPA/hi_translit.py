# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Transliteration for Hindi.
Modifiled from https://en.wiktionary.org/wiki/Module:hi-translit Lua module partially.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unicodedata

import regex as re


conv = {
    # consonants
    "क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ṅ",
    "च": "c", "छ": "ch", "ज": "j", "झ": "jh", "ञ": "ñ",
    "ट": "ṭ", "ठ": "ṭh", "ड": "ḍ", "ढ": "ḍh", "ण": "ṇ",
    "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
    "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m",
    "य": "y", "र": "r", "ल": "l", "व": "v", "ळ": "ḷ",
    "श": "ś", "ष": "ṣ", "स": "s", "ह": "h",
    "क़": "q", "ख़": "x", "ग़": "ġ", "ऴ": "ḻ",
    "ज़": "z", "ष़": "ḻ", "झ़": "ž", "ड़": "ṛ", "ढ़": "ṛh",
    "फ़": "f", "थ़": "θ", "ऩ": "ṉ", "ऱ": "ṟ",
    # "ज्ञ": "gy",

    # vowel diacritics
    "ि": "i", "ु": "u", "े": "e", "ो": "o",
    "ा": "ā", "ी": "ī", "ू": "ū",
    "ृ": "ŕ",
    "ै": "ai", "ौ": "au",
    "ॉ": "ŏ",
    "ॅ": "ĕ",

    # vowel signs
    "अ": "a", "इ": "i", "उ": "u", "ए": "e", "ओ": "o",
    "आ": "ā", "ई": "ī", "ऊ": "ū",
    "ऋ": "ŕ",
    "ऐ": "ai", "औ": "au",
    "ऑ": "ŏ",
    "ऍ": "ĕ",

    "ॐ": "om",

    # chandrabindu
    "ँ": "̃",

    # anusvara
    "ं": "ṁ",

    # visarga
    "ः": "ḥ",

    # virama
    "्": "",

    # numerals
    "०": "0", "१": "1", "२": "2", "३": "3", "४": "4",
    "५": "5", "६": "6", "७": "7", "८": "8", "९": "9",

    # punctuation
    # danda
    "।": ".",
    # compound separator
    "+": "",

    # abbreviation sign
    "॰": ".",
}

nasal_assim = {
    "ज़": "न",
    "क": "ङ", "ख": "ङ", "ग": "ङ", "घ": "ङ",
    "च": "ञ", "छ": "ञ", "ज": "ञ", "झ": "ञ",
    "ट": "ण", "ठ": "ण", "ड": "ण", "ढ": "ण",
    "प": "म", "फ": "म", "ब": "म", "भ": "म", "म": "म",
}

perm_cl = {
    "म्ल": True,
    "व्ल": True,
    "न्ल": True,
}

all_cons, special_cons = "कखगघङचछजझञटठडढतथदधपफबभशषसयरलवहणनम", "यरलवहनम"
vowel, vowel_sign = "aिुृेोाीूैौॉॅ", "अइउएओआईऊऋऐऔऑऍ"
syncope_pattern = "([" + vowel + vowel_sign + "])" + \
                  "(़?[" + all_cons + "])a" + \
                  "(़?[" + re.sub("य", "", all_cons) + "])" + \
                  "([ंँ]?[" + vowel + vowel_sign + "])"


def transliterate(text):
    def repl1(match):
        c, d = match.group(1), match.group(2)
        if d == "":
            return c + "a"
        return c + d
    def repl2(match):
        opt, first, second, third = \
            match.group(1), match.group(2), match.group(3), match.group(4)
        if (re.match("[" + special_cons + "]", first) and \
            re.match("्", second) and \
            (first + second + third) not in perm_cl.keys()) or \
            re.match("य[ीेै]", first + second):
            return "a" + opt + first + second + third
        return "" + opt + first + second + third
    def repl3(match):
        succ, prev = match.group(1), match.group(2)
        if succ + prev == "a":
            return succ + "्म" + prev
        if succ == "" and re.match("[" + vowel + "]", prev):
            return succ + "̃" + prev
        if succ in nasal_assim.keys():
            return succ + nasal_assim[succ] + prev
        return succ + "n" + prev
    def repl4(match):
        k = match.group()
        if k in conv.keys():
            return conv[k]
        return k

    text = re.sub("([" + all_cons + "]़?)([" + vowel + "्]?)", repl1, text)

    for word in re.findall("[ऀ-ॿa]+", text):
        orig_word = str(word)
        rev_word = word[::-1]
        rev_word = re.sub("^a(़?)([" + all_cons + "])(.)(.?)", repl2, rev_word)
        while re.match(syncope_pattern, rev_word):
            rev_word = re.sub(syncope_pattern, r"\1\2\3\4", rev_word)
        rev_word = re.sub("(.?)ं(.)", repl3, rev_word)
        text = re.sub(orig_word, rev_word[::-1], text)

    text = re.sub(".़?", repl4, text)
    text = re.sub("a([iu])̃", r"a͠\1", text)
    text = re.sub("ज्ञ", repl4, text)
    return unicodedata.normalize("NFC", text)
