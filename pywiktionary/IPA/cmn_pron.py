# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Mandarin in zh-pron module. Implements "|m=" parameter for template {{zh-pron}}.
Modified from https://en.wiktionary.org/wiki/Module:cmn-pron Lua module partially.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import unicodedata

import regex as re


tones =  "[̄́̌̀]"
pinyin_tone = {
    "̄": "1",
    "́": "2",
    "̌": "3",
    "̀": "4",
}

pinyin_detone = {
    "ā": "a", "á": "a", "ǎ": "a", "à": "a",
    "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
    "ē": "e", "é": "e", "ě": "e", "è": "e",
    "ê̄": "ê", "ế": "ê", "ê̌": "ê", "ề": "ê",
    "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
    "ū": "u", "ú": "u", "ǔ": "u", "ù": "u",
    "ǖ": "ü", "ǘ": "ü", "ǚ": "ü", "ǜ": "ü",
    "m̄": "m", "ḿ": "m", "m̌": "m", "m̀": "m",
    "n̄": "n", "ń": "n", "ň": "n", "ǹ": "n",
}

ipa_initial = {
    "b": "p", "p": "pʰ", "m": "m", "f": "f",
    "d": "t", "t": "tʰ", "n": "n", "l": "l",
    "g": "k", "k": "kʰ", "h": "x", "ng": "ŋ",
    "j": "t͡ɕ", "q": "t͡ɕʰ", "x": "ɕ",
    "z": "t͡s", "c": "t͡sʰ", "s": "s", "r": "ʐ",
    "zh": "ʈ͡ʂ", "ch": "ʈ͡ʂʰ", "sh": "ʂ",
    "": "",
}

ipa_initial_tl = {
    "p": "b̥", "t": "d̥", "k": "g̊",
    "t͡ɕ": "d͡ʑ̥", "t͡s": "d͡z̥", "ʈ͡ʂ": "ɖ͡ʐ̥",
}

ipa_final = {
    "yuanr": "ɥɑɻ",
    "iangr": "jɑ̃ɻ",
    "yangr": "jɑ̃ɻ",
    "uangr": "wɑ̃ɻ",
    "wangr": "wɑ̃ɻ",
    "yingr": "jɤ̃ɻ",
    "wengr": "ʊ̃ɻ",
    "iongr": "jʊ̃ɻ",
    "yongr": "jʊ̃ɻ",
    "yuan": "y̯ɛn",
    "iang": "i̯ɑŋ",
    "yang": "i̯ɑŋ",
    "uang": "u̯ɑŋ",
    "wang": "u̯ɑŋ",
    "ying": "iŋ",
    "weng": "u̯əŋ",
    "iong": "i̯ʊŋ",
    "yong": "i̯ʊŋ",
    "ianr": "jɑɻ",
    "yanr": "jɑɻ",
    "uair": "wɑɻ",
    "wair": "wɑɻ",
    "uanr": "wɑɻ",
    "wanr": "wɑɻ",
    "iaor": "jaʊɻʷ",
    "yaor": "jaʊɻʷ",
    "üanr": "ɥɑɻ",
    "vanr": "ɥɑɻ",
    "angr": "ɑ̃ɻ",
    "yuer": "ɥɛɻ",
    "weir": "wəɻ",
    "wenr": "wəɻ",
    "your": "jɤʊɻʷ",
    "yinr": "jəɻ",
    "yunr": "ɥəɻ",
    "engr": "ɤ̃ɻ",
    "ingr": "jɤ̃ɻ",
    "ongr": "ʊ̃ɻ",
    "uai": "u̯aɪ̯",
    "wai": "u̯aɪ̯",
    "yai": "i̯aɪ̯",
    "iao": "i̯ɑʊ̯",
    "yao": "i̯ɑʊ̯",
    "ian": "i̯ɛn",
    "yan": "i̯ɛn",
    "uan": "u̯a̠n",
    "wan": "u̯a̠n",
    "üan": "y̯ɛn",
    "van": "y̯ɛn",
    "ang": "ɑŋ",
    "yue": "y̯œ",
    "wei": "u̯eɪ̯",
    "you": "i̯oʊ̯",
    "yin": "in",
    "wen": "u̯ən",
    "yun": "yn",
    "eng": "ɤŋ",
    "ing": "iŋ",
    "ong": "ʊŋ",
    "air": "ɑɻ",
    "anr": "ɑɻ",
    "iar": "jɑɻ",
    "yar": "jɑɻ",
    "uar": "wɑɻ",
    "war": "wɑɻ",
    "aor": "aʊɻʷ",
    "ier": "jɛɻ",
    "yer": "jɛɻ",
    "uor": "wɔɻ",
    "wor": "wɔɻ",
    "üer": "ɥɛɻ",
    "ver": "ɥɛɻ",
    "eir": "əɻ",
    "enr": "əɻ",
    "uir": "wəɻ",
    "unr": "wəɻ",
    "our": "ɤʊɻʷ",
    "iur": "jɤʊɻ",
    "inr": "jəɻ",
    "ünr": "ɥəɻ",
    "vnr": "ɥəɻ",
    "yir": "jəɻ",
    "wur": "wuɻ",
    "yur": "ɥəɻ",
    "yo": "i̯ɔ",
    "ia": "i̯a̠",
    "ya": "i̯a̠",
    "ua": "u̯a̠",
    "wa": "u̯a̠",
    "ai": "aɪ̯",
    "ao": "ɑʊ̯",
    "an": "a̠n",
    "ie": "i̯ɛ",
    "ye": "i̯ɛ",
    "uo": "u̯ɔ",
    "wo": "u̯ɔ",
    "ue": "ɥ̯œ",
    "üe": "ɥ̯œ",
    "ve": "ɥ̯œ",
    "ei": "eɪ̯",
    "ui": "u̯eɪ̯",
    "ou": "oʊ̯",
    "iu": "i̯oʊ̯",
    "en": "ən",
    "in": "in",
    "un": "u̯ən",
    "ün": "yn",
    "vn": "yn",
    "yi": "i",
    "wu": "u",
    "yu": "y",
    "mˋ": "m̩",
    "ng": "ŋ̩",
    "ňg": "ŋ̩",
    "ńg": "ŋ̩",
    "ê̄": "ɛ",
    "ê̌": "ɛ",
    "ar": "ɑɻ",
    "er": "ɤɻ",
    "or": "wɔɻ",
    "ir": "iəɻ",
    "ur": "uɻ",
    "ür": "yəɻ",
    "vr": "yəɻ",
    "a": "a̠",
    "e": "ɤ",
    "o": "u̯ɔ",
    "i": "i",
    "u": "u",
    "ü": "y",
    "v": "y",
    "m": "m̩",
    "ḿ": "m̩",
    "n": "n̩",
    "ń": "n̩",
    "ň": "n̩",
    "ê": "ɛ",
}

ipa_null = {
    "a": True, "o": True, "e": True, "ê": True,
    "ai": True, "ei": True, "ao": True, "ou": True,
    "an": True, "en": True, "er": True, 
    "ang": True, "ong": True, "eng": True,
}

ipa_tl_ts = {
    "1": "²", "2": "³", "3": "⁴", "4": "¹", "5": "¹",
}

ipa_third_t_ts = {
    "1": "²¹⁴⁻²¹¹",
    "3": "²¹⁴⁻³⁵",
    "5": "²¹⁴",
    "2": "²¹⁴⁻²¹¹",
    "1-2": "²¹⁴⁻²¹¹",
    "4-2": "²¹⁴⁻²¹¹",
    "4": "²¹⁴⁻²¹¹",
    "1-4": "²¹⁴⁻²¹¹",
}

ipa_t_values = {
    "4": "⁵¹",
    "1-4": "⁵⁵⁻⁵¹",
    "1": "⁵⁵",
    "2": "³⁵",
    "1-2": "⁵⁵⁻³⁵",
    "4-2": "⁵¹⁻³⁵",
}

def tone_determ(text):
    text = unicodedata.normalize("NFD", text)
    match = re.search(tones, text)
    if match and match.group() in pinyin_tone.keys():
        return pinyin_tone[match.group()]
    return "5"


def pinyin_transform(text):
    if re.search("​", text):
        return ""
    text = re.sub(
        unicodedata.normalize("NFD", "ü"),
        "ü",
        re.sub(
            unicodedata.normalize("NFD", "ê"),
            "ê",
            unicodedata.normalize("NFD", text)
        )
    )
    if re.search(
            "[aeiouêü]" + tones + "[aeiou]?[aeiouêü]" + tones + "",
            text.lower()):
        return ""
    text = text.lower()
    if not re.search(tones, text) and re.match("[1-5]", text):
        return re.sub("(\d)(\p{Ll})", "\1 \2", text)
    if re.search("[一不,.?]", text):
        text = re.sub(
            "([一不])$",
            lambda x: " yī" if x.group() == "一" else " bù",
            text
        )
        text = re.sub("([一不])", r" \1 ", text)
        text = re.sub("([,.?])", r" \1 ", text)
        text = re.sub(" +", " ", text)
        text = re.sub("^ ", "", text)
        text = re.sub(" $", "", text)
        text = re.sub("\. \. \.", "...", text)
    text = re.sub("['\-]", " ", text)
    text = re.sub(
        "([aeiouêü]" + tones + "?n?g?r?)([bpmfdtnlgkhjqxzcsywr]h?)",
        r"\1 \2",
        text
    )
    text = re.sub(" ([grn])$", r"\1", text)
    text = re.sub(" ([grn]) ", r"\1 ", text)

    return unicodedata.normalize("NFC", text)

def to_IPA(text, IPA_tone=True):
    """Generates Mandarin IPA from Pinyin.

    Implements ``|m=`` parameter for template `{{zh-pron}}`_.

    .. _{{zh-pron}}: https://en.wiktionary.org/wiki/Template:zh-pron

    Parameters
    ----------
    text : string
        String of ``|m=`` parameter parsed in `{{zh-pron}}`_ from Wiktionary.

    IPA_tone : bool
        Whether add IPA tone in result.

    Returns
    -------
    string
        Converted Mandarin IPA.

    Notes
    -----
    - Modified from `Wiktioanry cmn-pron Lua module`_ partially.

    .. _Wiktioanry cmn-pron Lua module: https://en.wiktionary.org/wiki/Module:cmn-pron

    Examples
    --------
    >>> cmn_text = "pīnyīn" # zh: [[拼音]]
    >>> cmn_IPA = cmn_pron.to_IPA(cmn_text)
    >>> cmn_IPA
    "pʰin⁵⁵ in⁵⁵"
    """
    def repl1(match):
        k = match.group()
        if k in pinyin_detone.keys():
            return pinyin_detone[k]
        return k
    def repl2(match):
        a, b, c = match.group(1), match.group(2), match.group(3)
        if b not in ipa_initial.keys() or c not in ipa_final.keys():
            return ""
        return a + ipa_initial[b] + ipa_final[c]
    def repl3(match):
        a, b = match.group(1), match.group(2)
        return ipa_initial[a] + b
    def repl4(match):
        a, b = match.group(1), match.group(2)
        return ipa_initial_tl[a] + b

    tone = {}
    tone_cat = {}
    text = re.sub("[,.]", "", pinyin_transform(text))
    text = re.sub(" +", " ", text)
    p = text.split(" ")

    for i in range(len(p)):
        tone_cat[i] = tone_determ(p[i])
        p[i] = re.sub(".[̄́̌̀]?", repl1, p[i])

        if p[i] == "一":
            if tone_determ(p[i+1]) == "4":
                tone_cat[i] = "1-2"
            else:
                tone_cat[i] = "1-4"
        elif p[i] == "不":
            if tone_determ(p[i+1]) == "4":
                tone_cat[i] = "4-2"
            else:
                tone_cat[i] = "4"
            p[i] = "bu"

    for i in range(len(p)):
        if p[i] in ipa_null.keys() and ipa_null[p[i]]:
            p[i] = "ˀ" + p[i]
        p[i] = re.sub("([jqx])u", r"\1ü", p[i])

        if p[i] == "ng":
            p[i] = ipa_final["ng"]
        else:
            p[i] = re.sub("^(ˀ?)([bcdfghjklmnpqrstxz]?h?)(.+)$", repl2, p[i])

        p[i] = re.sub("(ʈ?͡?[ʂʐ]ʰ?)i", r"\1ʐ̩", p[i])
        p[i] = re.sub("(t?͡?sʰ?)i", r"\1z", p[i])
        p[i] = re.sub("ˀu̯ɔ", "ˀ̯ɔ", p[i])
        p[i] = re.sub("ʐʐ̩", "ʐ̩", p[i])

        if tone_cat[i] == "5":
            p[i] = re.sub("^([ptk])([^͡ʰ])", repl3, p[i])
            p[i] = re.sub("^([tʈ]͡[sɕʂ])([^ʰ])", repl4, p[i])
            p[i] = re.sub("ɤ$", "ə", p[i])
            if i > 0 and tone_cat[i-1] in ipa_tl_ts.keys():
                tone[i] = ipa_tl_ts[tone_cat[i-1]]
            else:
                tone[i] = ""
        elif tone_cat[i] == "3":
            if i == len(tone_cat) - 1:
                if i == 0:
                    tone[i] = "²¹⁴"
                else:
                    tone[i] = "²¹⁴⁻²¹⁽⁴⁾"
            else:
                tone[i] = ipa_third_t_ts[tone_cat[i+1]]
        elif i < len(p) - 1 and tone_cat[i] == "4" and tone_cat[i+1] == "4":
            tone[i] = "⁵¹⁻⁵³"
        elif i < len(p) - 1 and tone_cat[i] == "4" and tone_cat[i+1] == "1-4":
            tone[i] = "⁵¹⁻⁵³"
        elif i < len(p) - 1 and tone_cat[i] == "1-4" and tone_cat[i+1] == "4":
            tone[i] = "⁵⁵⁻⁵³"
        else:
            tone[i] = ipa_t_values[tone_cat[i]]

        if IPA_tone:
            p[i] += tone[i]

    return " ".join(p)
