# -*- coding: utf-8  -*-

from __future__ import unicode_literals

PHONEME_CODES_1 = {
	"ɑ": "AA",
	"æ": "AE",
	"ʌ": "AH",
	"ɔ": "AO",
	"b": "B",
	"ʧ": "CH",
	"d": "D",
	"ð": "DH",
	"ɛ": "EH",
	"f": "F",
	"ɡ": "G",
	"h": "HH",
	"i": "IH",
	"ʤ": "JH",
	"k": "K",
	"l": "L",
	"m": "M",
	"n": "N",
	"ŋ": "NG",
	"p": "P",
	"ɹ": "R",
	"s": "S",
	"ʃ": "SH",
	"t": "T",
	"θ": "TH",
	"ʊ": "UH",
	"u": "UW",
	"v": "V",
	"w": "W",
	"j": "Y",
	"z": "Z",
	"ʒ": "ZH"
}

PHONEME_CODES_2 = {
	"ɑʊ": "AW",
	"ɑɪ": "AY",
	"ɜɹ": "ER",
	"eɪ": "EY",
	"ɪː": "IY",
	"iː": "IY",
	"oʊ": "OW",
	"ɔɪ": "OY"
}

def IPA2CMUBET(ipa_pronun):
	pronun = []
	i = 0
	ipa_pronun += ' '
	while i < len(ipa_pronun) - 1:
		if ipa_pronun[i:i+2] in PHONEME_CODES_2.keys():
			pronun.append(PHONEME_CODES_2[ipa_pronun[i:i+2]])
			i += 1
		elif ipa_pronun[i] in PHONEME_CODES_1.keys():
			pronun.append(PHONEME_CODES_1[ipa_pronun[i]])
		i += 1
	pronun.append('.')
	return ' '.join(pronun)

