# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Generates Spanish IPA from spelling. Implements template {{es-IPA}}.
Modified from https://en.wiktionary.org/wiki/Module:es-pronunc Lua module partially.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import regex as re


def to_IPA(word, LatinAmerica=False, phonetic=True):
    """Generates Spanish IPA from spelling.

    Implements template `{{es-IPA}}`_.

    .. _{{es-IPA}}: https://en.wiktionary.org/wiki/Template:es-IPA

    Parameters
    ----------
    word : string
        String of es-IPA text parsed in `{{es-IPA}}`_ from Wiktionary.

    LatinAmerica : bool
        Value of ``|LatinAmerica=`` parameter parsed in `{{es-IPA}}`_.

    phonetic : bool
        Value of ``|phonetic=`` parameter parsed in `{{es-IPA}}`_.

    Returns
    -------
    string
        Converted Spanish IPA.

    Notes
    -----
    - Modified from `Wiktioanry es-pronunc Lua module`_ partially.
    - Testcases are modified from `Wiktionary es-pronunc/testcases`_.

    .. _Wiktioanry es-pronunc Lua module: https://en.wiktionary.org/wiki/Module:es-pronunc
    .. _Wiktionary es-pronunc/testcases: https://en.wiktionary.org/wiki/Module:es-pronunc/testcases

    Examples
    --------
    >>> es_text = "baca" # es: [[baca]]
    >>> es_IPA = es_pron.to_IPA(es_text)
    >>> es_IPA
    "ˈbaka"
    """
    word = word.lower()
    word = re.sub("[^abcdefghijklmnopqrstuvwxyzáéíóúüñ.]", "", word)
	
    # determining whether "y" is a consonant or a vowel + diphthongs, "-mente" suffix
    word = re.sub("y([^aeiouáéíóú])", r"i\1", word)
    word = re.sub("y([aeiouáéíóú])", r"ɟ\1", word) # not the real sound
    word = re.sub("hi([aeiouáéíóú])", r"ɟ\1", word)
    word = re.sub("y$", "ï", word)
    word = re.sub("mente$", "ménte", word)

    # x
    word = re.sub("x", "ks", word)

    # "c" & "g" before "i" and "e" and all that stuff
    if LatinAmerica:
        word = re.sub("c([ieíé])", "s" + r"\1", word)
    else:
        word = re.sub("c([ieíé])", "θ" + r"\1", word)
    word = re.sub("gü([ieíé])", r"ɡw\1", word)
    word = re.sub("ü", "", word)
    word = re.sub("gu([ieíé])", r"ɡ\1", word)
    word = re.sub("g([ieíé])", r"x\1", word)

    # alphabet-to-phoneme
    word = re.sub("qu", "c", word)
    word = re.sub("v", "b", word)
    word = re.sub("ch", "ʃ", word) # not the real sound
    # ['g']='ɡ':  U+0067 LATIN SMALL LETTER G → U+0261 LATIN SMALL LETTER SCRIPT G
    word = re.sub(
        "[cgjñry]",
        lambda x: {"c": "k", "g": "ɡ", "j": "x", "ñ": "ɲ", "r": "ɾ"}[x.group()],
        word
    )
    word = re.sub("^ɾ", "r", word)
    word = re.sub("ɾɾ", "r", word)
    word = re.sub("lɾ", "lr", word)
    word = re.sub("nɾ", "nr", word)
    word = re.sub("ɾ([bdfɡklʎmnɲpstxzʃɟ])", r"r\1", word)
    word = re.sub("n([bm])", r"m\1", word)
    if LatinAmerica:
        word = re.sub("ll", "ɟ", word)
        word = re.sub("z", "z", word)
    else:
        word = re.sub("ll", "ʎ", word)
        word = re.sub("z", "θ", word) # not the real LatAm sound

    # syllable division
    word = re.sub("([aeiouáéíóú])([^aeiouáéíóú.])([aeiouáéíóú])", r"\1.\2\3", word)
    word = re.sub("([aeiouáéíóú])([^aeiouáéíóú.])([aeiouáéíóú])", r"\1.\2\3", word)
    word = re.sub("([aeiouáéíóú])([^aeiouáéíóú.])([^aeiouáéíóú.])([aeiouáéíóú])", r"\1\2.\3\4", word)
    word = re.sub("([aeiouáéíóú])([^aeiouáéíóú.])([^aeiouáéíóú.])([aeiouáéíóú])", r"\1\2.\3\4", word)
    word = re.sub("([aeiouáéíóú])([^aeiouáéíóú.])([^aeiouáéíóú.])([^aeiouáéíóú.])([aeiouáéíóú])", r"\1\2.\3\4\5", word)
    word = re.sub("([aeiouáéíóú])([^aeiouáéíóú.])([^aeiouáéíóú.])([^aeiouáéíóú.])([aeiouáéíóú])", r"\1\2.\3\4\5", word)
    word = re.sub("([pbktdɡ])\.([lɾ])", r".\1\2", word)
    word = re.sub("([^aeiouáéíóú.])\.s([^aeiouáéíóú.])", r"\1s.\2", word)
    word = re.sub("([aeoáéíóú])([aeoáéíóú])", r"\1.\2", word)
    word = re.sub("([ií])([ií])", r"\1.\2", word)
    word = re.sub("([uú])([uú])", r"\1.\2", word)

    # diphthongs
    word = re.sub("ih?([aeouáéóú])", r"j\1", word)
    word = re.sub("uh?([aeioáéíó])", r"w\1", word)

    # accentuation
    syllables = word.split(".")
    if re.search("[áéíóú]", word):
        for i in range(len(syllables)):
            if re.search("[áéíóú]", syllables[i]):
                syllables[i] = "ˈ" + syllables[i]
    else:
        if re.search("[^aeiouns]$", word):
            syllables[len(syllables)-1] = "ˈ" + syllables[len(syllables)-1]
        else:
            if len(syllables) > 1:
                syllables[len(syllables)-2] = "ˈ" + syllables[len(syllables)-2]

    # syllables nasalized if ending with "n", voiceless consonants in syllable-final position to voiced
    for i in range(len(syllables)):
        syllables[i] = re.sub(
            "[áéíóú]",
            lambda x: {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}[x.group()],
            syllables[i]
        )
        if phonetic and re.search("[mnɲ][^aeiou]?$", syllables[i]):
            syllables[i] = re.sub(
                "([aeiou])",
                lambda x: {"a": "ã", "e": "ẽ", "i": "ĩ", "o": "õ", "u": "ũ"}[x.group()],
                syllables[i]
            )
        syllables[i] = re.sub(
            "[ptk]$",
            lambda x: {"p": "b", "t": "d", "k": "ɡ"}[x.group()],
            syllables[i]
        )
    word = "".join(syllables)

    # real sound of LatAm Z
    word = re.sub("z", "s", word)
    # secondary stress
    word = re.sub("ˈ(.+)ˈ", r"ˌ\1ˈ", word)
    word = re.sub("ˈ(.+)ˌ", r"ˌ\1ˌ", word)
    word = re.sub("ˌ(.+)ˈ(.+)ˈ", r"ˌ\1ˌ\2ˈ", word)

    # phonetic transcription
    if phonetic:
        # θ,  s,  f before voiced consonants
        word = re.sub("θ([ˈˌ]?[mnɲbdɟɡlʎɾrh])", r"θ̬\1", word)
        word = re.sub("s([ˈˌ]?[mnɲbdɟɡlʎɾrh])", r"z\1", word)
        word = re.sub("f([ˈˌ]?[mnɲbdɟɡlʎrh])", r"v\1", word)
        # lots of allophones going on
        word = re.sub(
            "[bdɟɡ]",
            lambda x: {"b": "β", "d": "ð", "ɟ": "ʝ", "ɡ": "ɣ"}[x.group()],
            word
        )
        word = re.sub(
            "^[ˈˌ]?[βðɣʝ]",
            lambda x: {
                "β": "b", "ð": "d", "ʝ": "ɟ", "ɣ": "ɡ",
                "ˈβ": "ˈb", "ˈð": "ˈd", "ˈʝ": "ˈɟ", "ˈɣ": "ˈɡ",
                "ˌβ": "ˌb", "ˌð": "ˌd", "ˌʝ": "ˌɟ", "ˌɣ": "ˌɡ"
            }[x.group()],
            word
        )
        word = re.sub("([mnɲ][ˈˌ]?)β", r"\1b", word)
        word = re.sub("([lʎmnɲ][ˈˌ]?)ð", r"\1d", word)
        word = re.sub("([mnɲ][ˈˌ]?)ɣ", r"\1ɡ", word)
        word = re.sub("([lʎmnɲ][ˈˌ]?)ʝ", r"\1ɟ", word)
        word = re.sub(
            "[td]",
            lambda x: {"t": "t̪", "d": "d̪"}[x.group()],
            word
        )
        # nasal assimilation before consonants
        word = re.sub("n([ˈˌ]?[f])", r"ɱ\1", word)
        word = re.sub("n([ˈˌ]?[td])", r"n̪\1", word)
        word = re.sub("n([ˈˌ]?[θ])", r"n̟\1", word)
        word = re.sub("n([ˈˌ]?ʃ)", r"nʲ\1", word)
        word = re.sub("n([ˈˌ]?[ɟʎ])", r"ɲ\1", word)
        word = re.sub("n([ˈˌ]?[kxɡ])", r"ŋ\1", word)
        # lateral assimilation before consonants
        word = re.sub("l([ˈˌ]?[td])", r"l̪\1", word)
        word = re.sub("l([ˈˌ]?[θ])", r"l̟\1", word)
        # semivowels
        word = re.sub("([aeouãẽõũ][iïĩ])", r"\1̯", word)
        word = re.sub("([aeioãẽĩõ][uũ])", r"\1̯", word)

    word = re.sub("h", "", word) # silent "h"
    word = re.sub("ʃ", "t͡ʃ", word) # fake "ch" to real "ch"
    word = re.sub("ɟ", "ɟ͡ʝ", word) # fake "y" to real "y"
    word = re.sub("ï", "i", word) # fake "y$" to real "y$"

    return word
