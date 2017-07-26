"""IPA and X-SAMPA related variables and functions.
Modified from https://en.wiktionary.org/wiki/Module:IPA Lua module partially.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import regex as re

from .data import XSAMPA
from .data import CMUBET


# X-SAMPA symbol set
m_XSAMPA = XSAMPA.data

# IPA <-> XSAMPA lookup tables
i2x_lookup = {}
for XSAMPA_symbol, IPA_data in m_XSAMPA.items():
    # duplicate X-SAMPA mapping
    if XSAMPA_symbol in ["v\\", "'", "_="]:
        continue
    IPA_symbol = IPA_data["IPA_symbol"]
    i2x_lookup[IPA_symbol] = XSAMPA_symbol
    if "with_descender" in IPA_data.keys():
        with_descender = IPA_data["with_descender"]
        i2x_lookup[with_descender] = XSAMPA_symbol

# CMUBET symbol set
m_CMUBET = CMUBET.data

# IPA <-> CMUBET lookup tables
# IPA symbols not in CMUBET are included from Arpabet
# Refer to https://en.wikipedia.org/wiki/Arpabet for details
i2c_lookup = {
    "ɪ": "IH",
    "ə": "AX",
    "aɪ": "AY",
    "aʊ": "AW",
    "ɝ": "ER",
    "ɚ": "AXR",
    "dʒ": "JH",
    "m̩": "EM",
    "n̩": "EN",
    "ŋ̍": "ENG",
    "ɫ": "L",
    "ɫ̩": "EL",
    "r": "R",
    "ɾ": "DX",
    "ɾ̃": "NX",
    "ʔ": "Q",
    # from http://courses.csail.mit.edu/6.345//notes/IPA/
    "e": "EY",
    "ɦ": "HV",
    "o": "OW",
    "ɨ": "IX",
    # add to nearest phoneme
    "a": "AA",
    "ɜ": "ER",
    "ɒ": "O",
}
for CMUBET_symbol, IPA_symbol in m_CMUBET.items():
    i2c_lookup[IPA_symbol] = CMUBET_symbol


def IPA_to_XSAMPA(text):
    """Convert IPA to X-SAMPA.

    Use `IPA`_ and `X-SAMPA`_ symbol sets used in Wiktionary.

    .. _IPA: https://en.wiktionary.org/wiki/Module:IPA/data/symbols
    .. _X-SAMPA: https://en.wiktionary.org/wiki/Module:IPA/data/X-SAMPA

    Parameters
    ----------
    text : string
        String of IPA text parsed from Wiktionary.

    Returns
    -------
    string
        Converted X-SAMPA text.

    Notes
    -----
    - Use ``_j`` for palatalized instead of ``'``
    - Use ``=`` for syllabic instead of ``_=``
    - Use ``~`` for nasalization instead of ``_~``
    - Please refer to :doc:`sym` for more details.

    Examples
    --------
    >>> IPA_text = "/t͡ʃeɪnd͡ʒ/" # en: [[change]]
    >>> XSAMPA_text = IPA_to_XSAMPA(IPA_text)
    >>> XSAMPA_text
    "/t__SeInd__Z/"
    """
    text = re.sub("ːː", ":", text)
    text += " "
    XSAMPA_lst = []
    i = 0
    while i < len(text) - 1:
        if text[i:i+2] in i2x_lookup.keys():
            XSAMPA_lst.append(i2x_lookup[text[i:i+2]])
            i += 1
        elif text[i] in i2x_lookup.keys():
            XSAMPA_lst.append(i2x_lookup[text[i]])
        else:
            XSAMPA_lst.append(text[i])
        i += 1
    return "".join(XSAMPA_lst)


def IPA_to_CMUBET(text):
    """Convert IPA to CMUBET for US English.

    Use `IPA`_ and symbol set used in Wiktionary and
    `CMUBET`_ symbol set used in CMUDict.

    .. _IPA: https://en.wiktionary.org/wiki/Module:IPA/data/symbols
    .. _CMUBET: https://cmusphinx.github.io/wiki/cmubet/

    Parameters
    ----------
    text : string
        String of IPA text parsed from Wiktionary.

    Returns
    -------
    string
        Converted CMUBET text.
    """
    text = re.sub("ːː", ":", text)
    text = text.lstrip("/[").rstrip("]/")
    text += " "
    CMUBET_lst = []
    i = 0
    while i < len(text) - 1:
        if text[i:i+2] in i2c_lookup.keys():
            CMUBET_lst.append(i2c_lookup[text[i:i+2]])
            i += 1
        elif text[i] in i2c_lookup.keys():
            CMUBET_lst.append(i2c_lookup[text[i]])
        else:
            continue
        i += 1
    return " ".join(CMUBET_lst)
