# https://en.wiktionary.org/wiki/Module:IPA

from __future__ import unicode_literals

from .data import XSAMPA


m_XSAMPA = XSAMPA.data

# IPA <-> XSAMPA lookup tables
i2x_lookup = {}
for XSAMPA_symbol, IPA_data in m_XSAMPA.items():
    IPA_symbol = IPA_data["IPA_symbol"]
    i2x_lookup[IPA_symbol] = XSAMPA_symbol
    if "with_descender" in IPA_data.keys():
        with_descender = IPA_data["with_descender"]
        i2x_lookup[with_descender] = XSAMPA_symbol

def IPA_to_XSAMPA(text):
    text = text.replace('ːː', ':')
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
