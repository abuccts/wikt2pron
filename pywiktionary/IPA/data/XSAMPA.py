"""X-SAMPA symbol set.
Modified from https://en.wiktionary.org/wiki/Module:IPA/data/X-SAMPA
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


# X-SAMPA symbols
data = {
    # not in official X-SAMPA; from http://www.kneequickie.com/kq/Z-SAMPA
    "b\\": {
        "IPA_symbol": "ⱱ",
    },
    "b_<": {
        "IPA_symbol": "ɓ",
    },
    "d`": {
        "IPA_symbol": "ɖ",
        "has_descender": True,
    },
    "d_<": {
        "IPA_symbol": "ɗ",
    },
    # not in official X-SAMPA; Wikipedia-specific
    "d`_<": {
        "IPA_symbol": "ᶑ",
        "has_descender": True,
    },
    "g": {
        "IPA_symbol": "ɡ",
        "has_descender": True,
    },
    "g_<": {
        "IPA_symbol": "ɠ",
        "has_descender": True,
    },
    "h\\": {
        "IPA_symbol": "ɦ",
    },
    "j\\": {
        "IPA_symbol": "ʝ",
        "has_descender": True,
    },
    "l`": {
        "IPA_symbol": "ɭ",
        "has_descender": True,
    },
    "l\\": {
        "IPA_symbol": "ɺ",
    },
    "n`": {
        "IPA_symbol": "ɳ",
        "has_descender": True,
    },
    "p\\": {
        "IPA_symbol": "ɸ",
        "has_descender": True,
    },
    "r`": {
        "IPA_symbol": "ɽ",
        "has_descender": True,
    },
    "r\\": {
        "IPA_symbol": "ɹ",
    },
    "r\\`": {
        "IPA_symbol": "ɻ",
        "has_descender": True,
    },
    "s`": {
        "IPA_symbol": "ʂ",
        "has_descender": True,
    },
    "s\\": {
        "IPA_symbol": "ɕ",
    },
    "t`": {
        "IPA_symbol": "ʈ",
    },
    "v\\": {
        "IPA_symbol": "ʋ",
    },
    "x\\": {
        "IPA_symbol": "ɧ",
        "has_descender": True,
    },
    "z`": {
        "IPA_symbol": "ʐ",
        "has_descender": True,
    },
    "z\\": {
        "IPA_symbol": "ʑ",
    },
    "A": {
        "IPA_symbol": "ɑ",
    },
    "B": {
        "IPA_symbol": "β",
        "has_descender": True,
    },
    "B\\": {
        "IPA_symbol": "ʙ",
    },
    "C": {
        "IPA_symbol": "ç",
        "has_descender": True,
    },
    "D": {
        "IPA_symbol": "ð",
    },
    "E": {
        "IPA_symbol": "ɛ",
    },
    "F": {
        "IPA_symbol": "ɱ",
        "has_descender": True,
    },
    "G": {
        "IPA_symbol": "ɣ",
        "has_descender": True,
    },
    "G\\": {
        "IPA_symbol": "ɢ",
    },
    "G\\_<": {
        "IPA_symbol": "ʛ",
    },
    "H": {
        "IPA_symbol": "ɥ",
        "has_descender": True,
    },
    "H\\": {
        "IPA_symbol": "ʜ",
    },
    "I": {
        "IPA_symbol": "ɪ",
    },
    "I\\": {
        "IPA_symbol": "ɪ̈",
    },
    "J": {
        "IPA_symbol": "ɲ",
        "has_descender": True,
    },
    "J\\": {
        "IPA_symbol": "ɟ",
    },
    "J\\_<": {
        "IPA_symbol": "ʄ",
        "has_descender": True,
    },
    "K": {
        "IPA_symbol": "ɬ",
    },
    "K\\": {
        "IPA_symbol": "ɮ",
        "has_descender": True,
    },
    "L": {
        "IPA_symbol": "ʎ",
    },
    "L\\": {
        "IPA_symbol": "ʟ",
    },
    "M": {
        "IPA_symbol": "ɯ",
    },
    "M\\": {
        "IPA_symbol": "ɰ",
        "has_descender": True,
    },
    "N": {
        "IPA_symbol": "ŋ",
        "has_descender": True,
    },
    "N\\": {
        "IPA_symbol": "ɴ",
    },
    "O": {
        "IPA_symbol": "ɔ",
    },
    "O\\": {
        "IPA_symbol": "ʘ",
    },
    "P": {
        "IPA_symbol": "ʋ",
    },
    "Q": {
        "IPA_symbol": "ɒ",
    },
    "R": {
        "IPA_symbol": "ʁ",
    },
    "R\\": {
        "IPA_symbol": "ʀ",
    },
    "S": {
        "IPA_symbol": "ʃ",
        "has_descender": True,
    },
    "T": {
        "IPA_symbol": "θ",
    },
    "U": {
        "IPA_symbol": "ʊ",
    },
    "U\\": {
        "IPA_symbol": "ʊ̈",
    },
    "V": {
        "IPA_symbol": "ʌ",
    },
    "W": {
        "IPA_symbol": "ʍ",
    },
    "X": {
        "IPA_symbol": "χ",
        "has_descender": True,
    },
    "X\\": {
        "IPA_symbol": "ħ",
    },
    "Y": {
        "IPA_symbol": "ʏ",
    },
    "Z": {
        "IPA_symbol": "ʒ",
        "has_descender": True,
    },
    "\"": {
        "IPA_symbol": "ˈ",
    },
    "%": {
        "IPA_symbol": "ˌ",
    },
    # not in official X-SAMPA; from http://www.kneequickie.com/kq/Z-SAMPA
    "%\\": {
        "IPA_symbol": "ᴙ",
    },
    "'": {
        "IPA_symbol": "ʲ",
        "is_diacritic": True,
    },
    ":": {
        "IPA_symbol": "ː",
        "is_diacritic": True,
    },
    ":\\": {
        "IPA_symbol": "ˑ",
        "is_diacritic": True,
    },
    "@": {
        "IPA_symbol": "ə",
    },
    "@`": {
        "IPA_symbol": "ɚ",
    },
    "@\\": {
        "IPA_symbol": "ɘ",
    },
    "{": {
        "IPA_symbol": "æ",
    },
    "}": {
        "IPA_symbol": "ʉ",
    },
    "1": {
        "IPA_symbol": "ɨ",
    },
    "2": {
        "IPA_symbol": "ø",
    },
    "3": {
        "IPA_symbol": "ɜ",
    },
    "3`": {
        "IPA_symbol": "ɝ",
    },
    "3\\": {
        "IPA_symbol": "ɞ",
    },
    "4": {
        "IPA_symbol": "ɾ",
    },
    "5": {
        "IPA_symbol": "ɫ",
    },
    "6": {
        "IPA_symbol": "ɐ",
    },
    "7": {
        "IPA_symbol": "ɤ",
    },
    "8": {
        "IPA_symbol": "ɵ",
    },
    "9": {
        "IPA_symbol": "œ",
    },
    "&": {
        "IPA_symbol": "ɶ",
    },
    "?": {
        "IPA_symbol": "ʔ",
    },
    "?\\": {
        "IPA_symbol": "ʕ",
    },
    "<\\": {
        "IPA_symbol": "ʢ",
    },
    ">\\": {
        "IPA_symbol": "ʡ",
    },
    "^": {
        "IPA_symbol": "ꜛ",
    },
    "!": {
        "IPA_symbol": "ꜜ",
    },
    # not in official X-SAMPA
    "!!": {
        "IPA_symbol": "‼",
    },
    "!\\": {
        "IPA_symbol": "ǃ",
    },
    "|\\": {
        "IPA_symbol": "ǀ",
        "has_descender": True,
    },
    "||": {
        "IPA_symbol": "‖",
        "has_descender": True,
    },
    "|\\|\\": {
        "IPA_symbol": "ǁ",
        "has_descender": True,
    },
    "=\\": {
        "IPA_symbol": "ǂ",
        "has_descender": True,
    },
    # linking mark, liaison
    "-\\": {
        "IPA_symbol": "‿",
        "is_diacritic": True,
    },
    # coarticulated; not in official X-SAMPA
    "__": {
        "IPA_symbol": u"\u0361",
    },
    # fortis, strong articulation; not in official X-SAMPA
    "_:": {
        "IPA_symbol": u"\u0348",
    },
    "_\"": {
        "IPA_symbol": u"\u0308",
        "is_diacritic": True,
    },
    # advanced
    "_+": {
        "IPA_symbol": u"\u031F",
        "with_descender": "˖",
        "is_diacritic": True,
    },
    # retracted
    "_-": {
        "IPA_symbol": u"\u0320",
        "with_descender": "˗",
        "is_diacritic": True,
    },
    # rising tone
    "_/": {
        "IPA_symbol": u"\u030C",
        "is_diacritic": True,
    },
    # voiceless
    "_0": {
        "IPA_symbol": u"\u0325",
        "with_descender": u"\u030A",
        "is_diacritic": True,
    },
    # syllabic
    "=": {
        "IPA_symbol": u"\u0329",
        "with_descender": u"\u030D",
        "is_diacritic": True,
    },
    # syllabic (both are OK according to https://en.wikipedia.org/wiki/X-SAMPA)
    "_=": {
        "IPA_symbol": u"\u0329",
        "with_descender": u"\u030D",
        "is_diacritic": True,
    },
    # strident: not in official X-SAMPA;
    # from http://www.kneequickie.com/kq/Z-SAMPA
    "_%\\": {
        "IPA_symbol": u"\u1DFD",
    },
    # ejective
    "_>": {
        "IPA_symbol": "ʼ",
        "is_diacritic": True,
    },
    # pharyngealized
    "_?\\": {
        "IPA_symbol": "ˤ",
        "is_diacritic": True,
    },
    # falling tone
    "_\\": {
        "IPA_symbol": u"\u0302",
        "is_diacritic": True,
    },
    # non-syllabic
    "_^": {
        "IPA_symbol": u"\u032F",
        "with_descender": u"\u0311",
        "is_diacritic": True,
    },
    # no audible release
    "_}": {
        "IPA_symbol": u"\u031A",
        "is_diacritic": True,
    },
    # r-coloring (colouring), rhotacization
    "`": {
        "IPA_symbol": u"\u02DE",
        "is_diacritic": True,
    },
    # nasalization
    "~": {
        "IPA_symbol": u"\u0303",
        "is_diacritic": True,
    },
    # advanced tongue root
    "_A": {
        "IPA_symbol": u"\u0318",
        "is_diacritic": True,
    },
    # apical
    "_a": {
        "IPA_symbol": u"\u033A",
        "is_diacritic": True,
    },
    # extra-low tone
    "_B": {
        "IPA_symbol": u"\u030F",
        "is_diacritic": True,
    },
    # low rising tone
    "_B_L": {
        "IPA_symbol": u"\u1DC5",
        "is_diacritic": True,
    },
    # less rounded
    "_c": {
        "IPA_symbol": u"\u031C",
        "is_diacritic": True,
    },
    # dental
    "_d": {
        "IPA_symbol": u"\u032A",
        "is_diacritic": True,
    },
    # velarized or pharyngealized (dark)
    "_e": {
        "IPA_symbol": u"\u0334",
        "is_diacritic": True,
    },
    # downstep
    "<F>": {
        "IPA_symbol": "↘",
    },
    # falling tone
    "_F": {
        "IPA_symbol": u"\u0302",
        "is_diacritic": True,
    },
    # velarized
    "_G": {
        "IPA_symbol": "ˠ",
        "is_diacritic": True,
    },
    # high tone
    "_H": {
        "IPA_symbol": u"\u0301",
        "is_diacritic": True,
    },
    # high rising tone
    "_H_T": {
        "IPA_symbol": u"\u1DC4",
        "is_diacritic": True,
    },
    # aspiration
    "_h": {
        "IPA_symbol": "ʰ",
        "is_diacritic": True,
    },
    # palatalization
    "_j": {
        "IPA_symbol": "ʲ",
        "is_diacritic": True,
    },
    # creaky voice, laryngealization, vocal fry
    "_k": {
        "IPA_symbol": u"\u0330",
        "is_diacritic": True,
    },
    # low tone
    "_L": {
        "IPA_symbol": u"\u0300",
        "is_diacritic": True,
    },
    # lateral release
    "_l": {
        "IPA_symbol": "ˡ",
        "is_diacritic": True,
    },
    # mid tone
    "_M": {
        "IPA_symbol": u"\u0304",
        "is_diacritic": True,
    },
    # laminal
    "_m": {
        "IPA_symbol": u"\u033B",
        "is_diacritic": True,
    },
    # linguolabial
    "_N": {
        "IPA_symbol": u"\u033C",
        "is_diacritic": True,
    },
    # nasal release
    "_n": {
        "IPA_symbol": "ⁿ",
        "is_diacritic": True,
    },
    # more rounded
    "_O": {
        "IPA_symbol": u"\u0339",
        "is_diacritic": True,
    },
    # lowered
    "_o": {
        "IPA_symbol": u"\u031E",
        "with_descender": "˕",
        "is_diacritic": True,
    },
    # retracted tongue root
    "_q": {
        "IPA_symbol": u"\u0319",
        "is_diacritic": True,
    },
    # global rise
    "<R>": {
        "IPA_symbol": "↗",
    },
    # rising tone
    "_R": {
        "IPA_symbol": u"\u030C",
        "is_diacritic": True,
    },
    # rising falling tone
    "_R_F": {
        "IPA_symbol": u"\u1DC8",
        "is_diacritic": True,
    },
    # raised
    "_r": {
        "IPA_symbol": u"\u031D",
        "is_diacritic": True,
    },
    # extra-high tone
    "_T": {
        "IPA_symbol": u"\u030B",
        "is_diacritic": True,
    },
    # breathy voice, murmured voice, murmur, whispery voice
    "_t": {
        "IPA_symbol": u"\u0324",
        "is_diacritic": True,
    },
    # voiced
    "_v": {
        "IPA_symbol": u"\u032C",
        "is_diacritic": True,
    },
    # labialized
    "_w": {
        "IPA_symbol": "ʷ",
        "is_diacritic": True,
    },
    # extra-short
    "_X": {
        "IPA_symbol": u"\u0306",
        "is_diacritic": True,
    },
    # mid-centralized
    "_x": {
        "IPA_symbol": u"\u033D",
        "is_diacritic": True,
    },
    "__T": {
        "IPA_symbol": "˥",
    },
    "__H": {
        "IPA_symbol": "˦",
    },
    "__M": {
        "IPA_symbol": "˧",
    },
    "__L": {
        "IPA_symbol": "˨",
    },
    "__B": {
        "IPA_symbol": "˩",
    },
    # not X-SAMPA; for convenience
    # dotted circle
    "0": {
        "IPA_symbol": "◌",
    },
}

identical = "acehklmnorstuvwxz"
for char in identical:
    data[char] = {"IPA_symbol": char}

identical_with_descender = "jpqy"
for char in identical_with_descender:
    data[char] = {"IPA_symbol": char, "has_descender": True}
