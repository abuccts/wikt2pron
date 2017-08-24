# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Modifiled from https://en.wiktionary.org/wiki/Module:ru-translit Lua module partially.

FIXME:

1. (DONE) If you write '''Б'''ез, it transliterates to '''B'''jez instead of
   '''B'''ez.
2. (DONE) Convert ъ to nothing before comma or other non-letter particle, e.g.
   in Однимъ словомъ, идешь на чтеніе.
3. (DONE) Make special-casing for adjectives in -го and for что (and friends)
    be the default, and implement transformations in Cyrillic rather than after
    translit so that we can display the transformed Cyrillic in the
    "phonetic respelling" notation of {{ru-IPA}}.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import regex as re


GR = u"\u0300" # grave =  ̀
TEMP_G = u"\uFFF1" # substitute to preserve g from changing to v

def ine(x):
    """convert "" to None"""
    if not x:
        return None
    return x

# In this table, we now map Cyrillic е and э to je and e, and handle the
# post-consonant version (plain e and ɛ) specially.
tab = {
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "Je", "Ё": "Jó", "Ж": "Ž", "З": "Z", "И": "I", "Й": "J",
    "К": "K", "Л": "L", "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U", "Ф": "F",
    "Х": "X", "Ц": "C", "Ч": "Č", "Ш": "Š", "Щ": "Šč", "Ъ": "ʺ", "Ы": "Y", "Ь": "ʹ", "Э": "E", "Ю": "Ju", "Я": "Ja",
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "je", "ё": "jó", "ж": "ž", "з": "z", "и": "i", "й": "j",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
    "х": "x", "ц": "c", "ч": "č", "ш": "š", "щ": "šč", "ъ": "ʺ", "ы": "y", "ь": "ʹ", "э": "e", "ю": "ju", "я": "ja",
    # Russian style quotes
    "«": "“", "»": "”",
    # archaic, pre-1918 letters
    "І": "I", "і": "i", "Ѳ": "F", "ѳ": "f",
    "Ѣ": "Jě", "ѣ": "jě", "Ѵ": "I", "ѵ": "i",
}

# following based on ru-common for use with is_monosyllabic()
# any Cyrillic or Latin vowel, including ёЁ and composed Cyrillic vowels with grave accent;
# not including accented Latin vowels except ě (FIXME, might want to change this)
vowels = "аеиоуяэыюіѣѵүАЕИОУЯЭЫЮІѢѴҮѐЀѝЍёЁAEIOUYĚƐaeiouyěɛ"
# FIXME! Bypass some cases
consonants_fix = "éо̀"

# FIXME! Doesn't work with ɣ, which gets included in this character set
non_consonants = "[" + vowels + consonants_fix + "ЪЬъьʹʺ]"
consonants = "[^" + vowels + consonants_fix + "ЪЬъьʹʺ]"

map_to_plain_e_map = {
    "Е": "E", "е": "e",
    "Ѣ": "Ě", "ѣ": "ě",
    "Э": "Ɛ", "э": "ɛ",
}
def map_to_plain_e(match):
    pre, e = match.group(1), match.group(2)
    return pre + map_to_plain_e_map[e]

map_to_je_map = {
    "Е": "Je", "е": "je",
    "Ѣ": "Jě", "ѣ": "jě",
    "Э": "E", "э": "e",
}
def map_to_je(match):
    pre, e = match.group(1), match.group(2)
    if not e:
        e = pre
        pre = ""
    return pre + map_to_je_map[e]

# decompose composed grave chars; they will map to uncomposed Latin letters for
# consistency with other char+grave combinations, and we do this early to
# avoid problems converting to e or je
decompose_grave_map = {
    "ѐ": "е" + GR,
    "Ѐ": "Е" + GR,
    "ѝ": "и" + GR,
    "Ѝ": "И" + GR,
}

# True if Cyrillic or decomposed Latin word has no more than one vowel;
# includes non-syllabic stems such as льд-; copied from ru-common and modified
# to avoid having to import that module (which would slow things down
# significantly)
def is_monosyllabic(word):
    return not re.search("[" + vowels + "].*[" + vowels + "]", word)

# Apply transformations to the Cyrillic to more closely match pronunciation.
# Return two arguments: the "original" text (after decomposing composed
# grave characters), and the transformed text. If the two are different,
# {{ru-IPA}} should display a "phonetic respelling" notation. 
# NOADJ disables special-casing for adjectives in -го, while FORCEADJ forces
# special-casing for adjectives, including those in -аго (pre-reform spelling)
# and disables checking for exceptions (e.g. много, ого). NOSHTO disables
# special-casing for что and related words.
def apply_tr_fixes(text, noadj="", noshto="", forceadj=""):
    # decompose composed grave characters before we convert Cyrillic е to
    # Latin e or je
    text = re.sub("[ѐЀѝЍ]", lambda x: decompose_grave_map[x.group()], text)

    origtext = str(text)

    # the second half of the if-statement below is an optimization; see above.
    if not noadj and "го" in text:
        if not forceadj:
            # handle много
            text = re.sub(
                "(?<!\p{L}|́|̀)([Мм]но[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]

            # handle немного, намного
            text = re.sub(
                "(?<!\p{L}|́|̀)([Нн][еа]мно[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle до́рого [short form of дорогой, adverb]
            text = re.sub(
                "(?<!\p{L}|́|̀)([Дд]о[́̀]?ро)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle недо́рого [short form of недорогой, adverb]
            text = re.sub(
                "(?<!\p{L}|́|̀)([Нн]едо[́̀]?ро)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle стро́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Сс]тро[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle нестро́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Нн]естро[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle убо́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Уу]бо[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle поло́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Пп]оло[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle длинноно́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Дд]линноно[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle коротконо́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Кк]оротконо[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle кривоно́го
            text = re.sub(
                "(?<!\p{L}|́|̀)([Кк]ривоно[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle пе́го [short form of пе́гий "piebald"]
            text = re.sub(
                "(?<!\p{L}|́|̀)([Пп]е[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle лого, сого, ого
            text = re.sub(
                "(?<!\p{L}|́|̀)([лсЛС]?[Оо][́̀]?)г(о[́̀]?)(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + r"\2",
                "\0" + text + "\0"
            )[1:-1]
            # handle Того, То́го (but not того or Того́, which have /v/)
            text = re.sub(
                "(?<!\p{L}|́|̀)(То́?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle лего
            text = re.sub(
                "(?<!\p{L}|́|̀)([Лл]е[́̀]?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]
            # handle игого, огого; note, we substitute TEMP_G for both г's
            # because otherwise the ого- at the beginning gets converted to ово
            text = re.sub(
                "(?<!\p{L}|́|̀)([ИиОо])гог(о[́̀]?)(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о" + TEMP_G + r"\2",
                "\0" + text + "\0"
            )[1:-1]
            # handle Диего
            text = re.sub(
                "(?<!\p{L}|́|̀)(Дие́?)го(?!\p{L}|́|̀)",
                r"\1" + TEMP_G + "о",
                "\0" + text + "\0"
            )[1:-1]

        #handle genitive/accusative endings, which are spelled -ого/-его/-аго
        # (-ogo/-ego/-ago) but transliterated -ovo/-evo/-avo; only for adjectives
        # and pronouns, excluding words like много, ого (-аго occurs in
        # pre-reform spelling); ́ is an acute accent, ̀ is a grave accent
        forceadj_pattern = "аА" if forceadj else ""
        pattern = "([оеОЕ" + forceadj_pattern + "][́̀]?)([гГ])([оО][́̀]?)"
        reflexive = "([сС][яЯ][́̀]?)"
        v = {"г": "в", "Г": "В"}
        text = re.sub(
            pattern + "(?!\p{L}|́|̀)",
            lambda x: x.group(1) + v[x.group(2)] + x.group(3) + "",
            "\0" + text + "\0"
        )[1:-1]
        text = re.sub(
            pattern + reflexive + "(?!\p{L}|́|̀)",
            lambda x: x.group(1) + v[x.group(2)] + x.group(3) + x.group(4),
            "\0" + text + "\0"
        )[1:-1]
        # handle сегодня
        text = re.sub(
            "(?<!\p{L}|́|̀)([Сс]е)г(о[́̀]?дня)(?!\p{L}|́|̀)",
            r"\1в\2",
            "\0" + text + "\0"
        )[1:-1]
        # handle сегодняшн-
        text = re.sub(
            "(?<!\p{L}|́|̀)([Сс]е)г(о[́̀]?дняшн)",
            r"\1в\2",
            "\0" + text + "\0"
        )[1:-1]

        # replace TEMP_G with g; must be done after the -go -> -vo changes
        text = re.sub(TEMP_G, "г", text)

    # the second half of the if-statement below is an optimization; see above.
    if not noshto and "то" in text:
        ch2sh = {"ч": "ш", "Ч": "Ш"}
        # Handle что
        text = re.sub(
            "(?<!\p{L}|́|̀)([Чч])(то[́̀]?)(?!\p{L}|́|̀)",
            lambda x: ch2sh[x.group(1)] + x.group(2),
            "\0" + text + "\0"
        )[1:-1]
        # Handle чтобы, чтоб
        text = re.sub(
            "(?<!\p{L}|́|̀)([Чч])(то[́̀]?бы?)(?!\p{L}|́|̀)",
            lambda x: ch2sh[x.group(1)] + x.group(2),
            "\0" + text + "\0"
        )[1:-1]
        # Handle ничто
        text = re.sub(
            "(?<!\p{L}|́|̀)([Нн]и)ч(то[́̀]?)(?!\p{L}|́|̀)",
            r"\1ш\2",
            "\0" + text + "\0"
        )[1:-1]

    text = re.sub("([МмЛл][яеё][́̀]?)г([кч])", r"\1х\2", text)

    return origtext, text

# Transliterate after the pronunciation-related transformations of
# export.apply_tr_fixes() have been applied. Called from {{ru-IPA}}.
# INCLUDE_MONOSYLLABIC_JO_ACCENT is as in export.tr().
def tr_after_fixes(text, include_monosyllabic_jo_accent=""):
    # Remove word-final hard sign, either utterance-finally or followed by
    # a non-letter character such as space, comma, period, hyphen, etc.
    text = re.sub("[Ъъ]$", "", text)
    text = re.sub("[Ъъ]([^\p{L}])", r"\1", text)

    # the if-statement below isn't necessary but may speed things up,
    # particularly when include_monosyllabic_jo_accent isn't set, in that
    # in the majority of cases where ё doesn't occur, we avoid a pattern find
    # (in is_monosyllabic()) and three pattern subs. The translit module needs
    # to be as fast as possible since it may be called hundreds or
    # thousands of times on some pages.
    if re.search("[Ёё]", text):
        # We need to special-case ё after a "hushing" consonant, which becomes
        # ó (or o), without j. We also need special cases for monosyllabic ё
        # when INCLUDE_MONOSYLLABIC_JO_ACCENT isn't set, so we don't add the
        # accent mark that we would otherwise include.
        if not include_monosyllabic_jo_accent and is_monosyllabic(text):
            text = re.sub("([жшчщЖШЧЩ])ё", r"\1o", text)
            text = re.sub("ё", "jo", text)
            text = re.sub("Ё", "Jo", text)
        else:
            text = re.sub("([жшчщЖШЧЩ])ё", r"\1ó", text)
            # conversion of remaining ё will occur as a result of 'tab'.

    # ю after ж and ш becomes u (e.g. брошюра, жюри)
    text = re.sub("([жшЖШ])ю", r"\1u", text)

    # the if-statement below isn't necessary but may speed things up in that
    # in the majority of cases where the letters below don't occur, we avoid
    # six pattern subs.
    if re.search("[ЕеѢѣЭэ]", text):
        # е after a dash at the beginning of a word becomes e, and э becomes ɛ
        # (like after a consonant)
        text = re.sub("^(\-)([ЕеѢѣЭэ])", map_to_plain_e, text)
        text = re.sub("(\s\-)([ЕеѢѣЭэ])", map_to_plain_e, text)
        # don't get confused by single quote or parens between consonant and е;
        # e.g. Б'''ез''', американ(ец)
        text = re.sub("(" + consonants + "['\(\)]*)([ЕеѢѣЭэ])", map_to_plain_e, text)

        # This is now the default
        # е after a vowel or at the beginning of a word becomes je, and э becomes e
        # text = re.sub("^([ЕеѢѣЭэ])", map_to_je, text)
        # text = re.sub("(" + non_consonants + ")([ЕеѢѣЭэ])", map_to_je, text)
        # # need to do it twice in case of sequences of such vowels
        # text = re.sub("^([ЕеѢѣЭэ])", map_to_je, text)
        # text = re.sub("(" + non_consonants + ")([ЕеѢѣЭэ])", map_to_je, text)

    def repl_tab(match):
        k = match.group()
        if k in tab.keys():
            return tab[k]
        return k
    text = str(re.sub(".", repl_tab, text))
    return text

# Transliterates text, which should be a single word or phrase. It should
# include stress marks, which are then preserved in the transliteration.
# ё is a special case: it is rendered (j)ó in multisyllabic words and
# monosyllabic words in multi-word phrases, but rendered (j)o without an
# accent in isolated monosyllabic words, unless INCLUDE_MONOSYLLABIC_JO_ACCENT
# is specified. (This is used in conjugation and declension tables.)
# NOADJ disables special-casing for adjectives in -го, while FORCEADJ forces
# special-casing for adjectives and disables checking for exceptions
# (e.g. много). NOSHTO disables special-casing for что and related words.
def tr(text, lang="", sc="", include_monosyllabic_jo_accent="", noadj="", noshto="", forceadj=""):
    origtext, subbed_text = apply_tr_fixes(text, noadj, noshto, forceadj)
    return tr_after_fixes(subbed_text, include_monosyllabic_jo_accent)

# translit with various special-case substitutions; NOADJ disables
# special-casing for adjectives in -го, while FORCEADJ forces special-casing
# for adjectives and disables checking for expections (e.g. много).
# NOSHTO disables special-casing for что and related words. SUB is used
# to implement arbitrary substitutions in the Cyrillic text before other
# transformations are applied and before translit. It is of the form
# FROM/TO,FROM/TO,+.
def tr_sub(text, include_monosyllabic_jo_accent="", noadj="", noshto="", sub="", forceadj=""):
    if sub:
        subs = sub.split(",")
        for subpair in subs:
            subsplit = subpair.split("/")
            text = re.sub(subsplit[0], subsplit[1], text)

    return tr(text, None, None, include_monosyllabic_jo_accent, noadj, noshto, forceadj)

#for adjectives, pronouns
def tr_adj(text, include_monosyllabic_jo_accent=""):
    # we have to include "forceadj" because typically when tr_adj() is called
    # from the noun or adjective modules, it's called with suffix ого, which
    # would otherwise trigger the exceptional case and be transliterated as ogo
    return tr(text, None, None, include_monosyllabic_jo_accent,
        False, "noshto", "forceadj")
