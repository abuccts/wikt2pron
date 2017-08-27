# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Generates French IPA from spelling. Implements template {{fr-IPA}}.
Modified from https://en.wiktionary.org/wiki/Module:fr-pron Lua module partially.
Rewritten from rewritten by Benwing and original by Kc kennylau.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import regex as re


# apply sub() repeatedly until no change
def sub_repeatedly(pattern, repl, term):
    while True:
        new_term = re.sub(pattern, repl, term)
        if new_term == term:
            return term
        term = new_term

def ine(x):
    if x == "":
        return None
    return x

# pairs of consonants where a schwa between then can never be deleted;
# primarily, consonants that are the same except possibly for voicing
no_delete_schwa_between_list = {
    # WARNING: IPA ɡ used here
    "kɡ", "ɡk", "kk", "ɡɡ",
    "td", "dt", "tt", "dd",
    "bp", "pb", "pp", "bb",
    "ʃʒ", "ʒʃ", "ʃʃ", "ʒʒ",
    "fv", "vf", "ff", "vv",
    "sz", "zs", "ss", "zz",
    "jj", "ww", "ʁʁ", "ll", "nn", "ɲɲ", "mm",
    # FIXME, should be others
}

# generate set
no_delete_schwa_between = {}
for ch in no_delete_schwa_between_list:
    no_delete_schwa_between[ch] = True

remove_diaeresis_from_vowel = {
    "ä": "a",
    "ë": "e",
    "ï": "i",
    "ö": "o",
    "ü": "u",
    "ÿ": "i",
}

# True if C1 and C2 form an allowable onset (in which case we always
# attempt to place them after the syllable break)
def allow_onset_2(c1, c2):
    # WARNING: Both IPA and non-IPA g below, and both r and ʁ, because it is
    # called both before and after the substitutions of these chars.
    return (c2 == "l" or c2 == "r" or c2 == "ʁ") and \
           re.match("[bkdfgɡpstv]", c1) or \
           c1 == "d" and c2 == "ʒ" or \
           c1 != "j" and c2 == "j" or \
           (c2 == "w" or c2 == "W" or c2 == "ɥ")

# list of vowels, including both input Latin and output IPA; note that
# IPA nasal vowels are two-character sequences with a combining tilde,
# which we include as the last char
oral_vowel_no_schwa = "aeiouyAEIOUYéàèùâêîôûŷäëïöüÿăŏŭɑɛɔæœø"
oral_vowel = oral_vowel_no_schwa + "əƏĕė"
vowel_no_schwa = oral_vowel_no_schwa + "̃"
vowel = oral_vowel + "̃"
vowel_c = "[" + vowel + "]"
vowel_no_schwa_c = "[" + vowel_no_schwa + "]"
vowel_maybe_nasal_r = "[" + oral_vowel + "]̃?"
non_vowel_c = "[^" + vowel + "]"
oral_vowel_c = "[" + oral_vowel + "]"
vowel_no_i = "aeouəAEOUƏéàèùâêôûäëöüăĕŏŭɛɔæœø"
vowel_no_i_c = "[" + vowel_no_i + "]"
# special characters that should be carried through but largely ignored when
# syllabifying; single quote prevents interpretation of sequences,
# ‿ indicates liaison, ⁀ is a word boundary marker, - is a literal hyphen
# (we include word boundary markers because they mark word boundaries with
# words joined by hyphens, but should be ignored for syllabification in
# such a case), parens are used to explicitly indicate an optional sound, esp.
# a schwa
syljoiner_c = "[_'‿⁀\-()]" # don't include syllable marker or space
opt_syljoiners_c = syljoiner_c + "*"
schwajoiner_c = "[_'‿⁀\-. ]" # also include . and space but not ()
opt_schwajoiners_c = schwajoiner_c + "*"
cons_c = "[^" + vowel + ".⁀ \-]" # includes underscore, quote and liaison marker
cons_no_liaison_c = "[^" + vowel + ".⁀‿ \-]" # includes underscore and quote but not liaison marker
real_cons_c = "[^" + vowel + "_'‿.⁀ \-()]" # excludes underscore, quote and liaison marker
cons_or_joiner_c = "[^" + vowel + ". ]" # includes all joiners
front_vowel = "eiéèêĕėəɛæœy" # should not include capital E, used in cœur etc.
front_vowel_c = "[" + front_vowel + "]"


def to_IPA(text, pos=""):
    """Generates French IPA from spelling.
    
    Implements template `{{fr-IPA}}`_.

    .. _{{fr-IPA}}: https://en.wiktionary.org/wiki/Template:fr-IPA

    Parameters
    ----------
    text : string
        String of fr-IPA text parsed in `{{fr-IPA}}`_ from Wiktionary.

    pos : string
        String of ``|pos=`` parameter parsed in `{{fr-IPA}}`_.

    Returns
    -------
    string
        Converted French IPA.

    Notes
    -----
    - Modified from `Wiktioanry fr-pron Lua module`_ partially.
    - Rewritten from rewritten by *Benwing* and original by *Kc kennylau*.
    - Testcases are modified from `Wiktionary fr-pron/testcases`_.
    
    .. _Wiktioanry fr-pron Lua module: https://en.wiktionary.org/wiki/Module:fr-pron
    .. _Wiktionary fr-pron/testcases: https://en.wiktionary.org/wiki/Module:fr-pron/testcases

    Examples
    --------
    >>> fr_text = "hæmorrhagie" # fr: [[hæmorrhagie]]
    >>> fr_IPA = fr_pron.to_IPA(fr_text)
    >>> fr_IPA
    "e.mɔ.ʁa.ʒi"
    """
    def repl1(match):
        vow = match.group(1)
        if vow in remove_diaeresis_from_vowel.keys():
            return "gu" + remove_diaeresis_from_vowel[vow]
        return "g" + vow
    def repl2(match):
        v1, v2, mn, c = \
            match.group(1), match.group(2), match.group(3), match.group(4)
        if mn == "n" or re.search("[bpBP]", c) or v2 == "o" or v2 == "ɛ":
            nasaltab = {
                "a": "ɑ̃", "ä": "ɑ̃", "e": "ɑ̃", "ë": "ɑ̃",
                "ɛ": "ɛ̃", "i": "ɛ̃", "ï": "ɛ̃", "o": "ɔ̃", "ö": "ɔ̃",
                "ø": "œ̃", "œ": "œ̃", "u": "œ̃", "ü": "œ̃",
            } # à jeun
            if re.search("[éiï]", v1) and v2 == "e":
                return v1 + ".ɛ̃" + c # bien, européen, païen
            elif v1 == "j" and v2 == "e":
                return "jɛ̃" + c # moyen
            elif v1 == "o" and v2 == "i":
                return "wɛ̃" + c # coin, point
            elif v2 in nasaltab.keys():
                return v1 + nasaltab[v2] + c
        return v1 + v2 + mn + c
    def repl3(match):
        k = match.group()
        if k in remove_diaeresis_from_vowel.keys():
            return remove_diaeresis_from_vowel[k]
        return k
    def repl4(match):
        a, dot, b = \
            match.group(1), match.group(2), match.group(3)
        if re.search("[bdfɡkpstvzʃʒ]", a) and re.search("[mnlʁwj]", b):
            return a + dot + b + "ə" + "⁀"
        if re.search("[lmn]", a) and b == "ʁ":
            return a + dot + b + "ə" + "⁀"
        return a + dot + b + "(ə)" + "⁀"
    def repl5(match):
        v1, c1, c2, v2 = \
            match.group(1), match.group(2), match.group(3), match.group(4)
        if c1 == "ʁ" and c2 == "ʁ":
            return v1 + "." + c1 + "Ə." + c2 + v2
        return v1 + c1 + "." + c2 + v2
    def repl6(match):
        v1, c1, sep1, sep2, c2, v2 = \
            match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), match.group(6)
        if c1 + c2 in no_delete_schwa_between.keys() and \
            no_delete_schwa_between[c1 + c2]:
            return v1 + c1 + sep1 + "Ə" + sep2 + c2 + v2
        return v1 + c1 + sep1 + "(Ə)" + sep2 + c2 + v2

    text = text.lower()

    # To simplify checking for word boundaries and liaison markers, we
    # add ⁀ at the beginning and end of all words, and remove it at the end.
    # Note that the liaison marker is ‿.
    text = re.sub("\s*,\s*", "⁀⁀ | ⁀⁀", text)
    text = re.sub("\s+", "⁀ ⁀", text)
    text = re.sub("\-+", "⁀-⁀", text)
    text = "⁀⁀" + text + "⁀⁀"

    if pos == "v":
        # special-case for verbs
        text = re.sub("ai⁀", "é⁀", text)
        # vient, tient, and compounds will have to be special-cased, no easy
        # way to distinguish e.g. initient (silent) from retient (not silent).
        text = re.sub("ent⁀", "e⁀", text)
        text = re.sub("ent‿", "ət‿", text)
        # portions, retiens as verbs should not have /s/
        text = re.sub("ti([oe])ns([⁀‿])", r"t_i\1ns\2", text)
    # various early substitutions
    text = re.sub("ǝ", "ə", text) # replace wrong schwa with same-looking correct one
    text = re.sub("œu", "Eu", text) # capital E so it doesn't trigger c -> s
    text = re.sub("oeu", "Eu", text)
    text = re.sub("œil", "Euil", text)
    text = re.sub("œ", "æ", text) # keep as æ, mapping later to è or é
    # pas, gaz
    text = re.sub("[aä]([sz][⁀‿])", r"â\1", text)
    text = re.sub("à", "a", text)
    text = re.sub("ù", "u", text)
    text = re.sub("î", "i", text)
    text = re.sub("[Ee]û", "ø", text)
    text = re.sub("û", "u", text)
    text = re.sub("bs", "ps", text) # absolute, obstacle, subsumer, etc.
    text = re.sub("ph", "f", text)
    text = re.sub("gn", "ɲ", text)
    text = re.sub("⁀désh", "⁀déz", text)
    text = re.sub("([⁀‿])et([⁀‿])", r"\1é\2", text)
    text = re.sub("([⁀‿'])es([⁀‿])", r"\1ès\2", text)
    text = re.sub("([⁀‿'])est([⁀‿])", r"\1èt\2", text)
    text = re.sub("⁀ress", "⁀rəss", text) # ressortir, etc. should have schwa
    text = re.sub("⁀intrans(" + vowel_c + ")", r"⁀intranz\1", text)
    text = re.sub("⁀trans(" + vowel_c + ")", r"⁀tranz\1", text)
    # adverbial -emment is pronounced -amment
    text = re.sub("emment([⁀‿])", r"amment\1", text)
    text = re.sub("ie(ds?[⁀‿])", r"ié\1", text) # pied, assieds, etc.
    text = re.sub("[eæ]([dgpt]s?[⁀‿])", r"è\1", text) # permet
    text = re.sub("ez([⁀‿])", r"éz\1", text) # assez, avez, etc.
    text = re.sub("er‿", "èr‿", text) # premier étage
    text = re.sub("([⁀‿]" + cons_c + "*)er(s?[⁀‿])", r"\1èr\2", text) # cher, fer, vers
    text = re.sub("er(s?[⁀‿])", r"ér\1", text) # premier(s)
    text = re.sub("(⁀" + cons_c + "*)e(s[⁀‿])", r"\1é\2", text) # ses, tes, etc.
    text = re.sub("oien", "oyen", text) # iroquoien

    # s, c, g, j, q (ç handled below after dropping silent -s; x handled below)
    text = re.sub("cueil", "keuil", text) # accueil, etc.
    text = re.sub("gueil", "gueuil", text) # orgueil
    text = re.sub("(" + vowel_c + ")s(" + vowel_c + ")", r"\1z\2", text)
    text = re.sub("c('?" + front_vowel_c + ")", r"s\1", text)
    text = re.sub("qu'", "k'", text) # qu'on
    text = re.sub("qu(" + vowel_c + ")", r"k\1", text)
    text = re.sub("ge([aoAOàâôäöăŏɔ])", r"j\1", text)
    text = re.sub("g(" + front_vowel_c + ")", r"j\1", text)
    # gu+vowel -> g+vowel, but gu+vowel+diaeresis -> gu+vowel
    text = re.sub("gu(" + vowel_c + ")", repl1, text)
    text = re.sub("gü", "gu", text) # aiguë might be spelled aigüe
    # parking, footing etc.; also -ing_ e.g. swinguer respelled swing_guer,
    # Washington respelled Washing'tonne
    text = re.sub("(" + cons_c + ")ing([_'⁀‿])", r"\1iŋ\2", text)
    text = re.sub("ngt", "nt", text) # vingt, longtemps
    text = re.sub("j", "ʒ", text)
    text = re.sub("s?[cs]h", "ʃ", text)
    text = re.sub("[cq]", "k", text)
    # following two must follow s -> z between vowels
    text = re.sub("([^sçx⁀])ti([oe])n", r"\1si\2n", text) # tion, tien
    text = re.sub("([^sçx⁀])tial", r"\1sial", text)

    # special hack for uï; must follow guï handling and precede ill handling
    text = re.sub("uï", "ui", text) # ouir, etc.

    # special hack for oel, oil, oêl; must follow intervocal s -> z and
    # ge + o -> j, and precede -il- handling
    text = re.sub("o[eê]l", "wAl", text) # moelle, poêle
    # poil but don't affect -oill- (otherwise interpreted as /ɔj/)
    text = re.sub("oil([^l])", r"wAl\1", text)

    # ill, il; must follow j -> ʒ above
    # NOTE: In all of the following, we purposely do not check for a vowel
    # following -ill-, so that respellings can use it before a consonant
    # (e.g. [[boycotter]] respelled 'boillcotter')
    # (1) special-casing for C+uill (juillet, cuillère, aiguille respelled
    #     aiguïlle)
    text = sub_repeatedly("(" + cons_c + ")uill", r"\1ɥij", text)
    # (2) -ill- after a vowel; repeat if necessary in case of VillVill
    #     sequence (ailloille respelling of ayoye)
    text = sub_repeatedly("(" + vowel_c + ")ill", r"\1j", text)
    # (3) any other ill, except word-initially (illustrer etc.)
    text = re.sub("([^⁀])ill", r"\1ij", text)
    # (4) final -il after a vowel; we consider final -Cil to contain a
    #     pronounced /l/ (e.g. 'il', 'fil', 'avril', 'exil', 'volatil', 'profil')
    text = re.sub("(" + vowel_c + ")il([⁀‿])", r"\1j\2", text)
    # (5) -il- after a vowel, before a consonant (not totally necessary;
    #     unlikely to occur normally, respelling can use -ill-)
    text = re.sub("(" + vowel_c + ")il(" + cons_c + ")", r"\1j\2", text)

    # y; include before removing final -e so we can distinguish -ay from
    # -aye
    text = re.sub("ay([⁀‿])", r"ai\1", text) # Gamay
    text = re.sub("éy", "éj", text) # used in respellings, eqv. to 'éill'
    text = re.sub("(" + vowel_no_i_c + ")y", r"\1iy", text)
    text = re.sub("yi([" + vowel + ".])", r"y.y\1", text)
    text = re.sub("'y‿", "'j‿", text) # il n'y‿a
    text = re.sub("(" + cons_c + ")y(" + cons_c + ")", r"\1i\2", text)
    text = re.sub("(" + cons_c + ")ye?([⁀‿])", r"\1i\2", text)
    text = re.sub("⁀y(" + cons_c + ")", r"⁀i\1", text)
    text = re.sub("⁀y⁀", "⁀i⁀", text)
    text = re.sub("y", "j", text)

    # nasal hacks
    # make 'n' before liaison in certain cases both nasal and pronounced
    text = re.sub("(⁀[mts]?on)‿", r"\1N‿", text) # mon, son, ton, on
    text = re.sub("('on)‿", r"\1N‿", text) # qu'on, l'on
    text = re.sub("([eu]n)‿", r"\1N‿", text) # en, bien, un, chacun etc.
    # in bon, certain etc. the preceding vowel isn't nasal
    text = re.sub("n‿", "N‿", text)

    # other liaison hacks
    text = re.sub("d‿", "t‿", text) # grand arbre, pied-à-terre
    text = re.sub("[sx]‿", "z‿", text) # vis-a-vis, beaux-arts, premiers enfants, etc.
    text = re.sub("f‿", "v‿", text) # neuf ans, etc.
    # treat liaison consonants that would be dropped as if they are extra-word,
    # so that preceding "word-final" letters are still dropped and preceding
    # vowels take on word-final qualities
    text = re.sub("([bdgkpstxz]‿)", r"⁀\1", text)
    text = re.sub("i‿", "ij‿", text) # y a-t-il, gentil enfant

    # silent letters
    # do this first so we also drop preceding letters of needed
    text = re.sub("[sxz]⁀", "⁀", text)
    # silence -c and -ct in nc(t), but not otherwise
    text = re.sub("nkt?⁀", "n⁀", text)
    text = re.sub("([ks])t⁀", r"\1T⁀", text) # final -kt, -st pronounced
    text = re.sub("ér⁀", "é⁀", text) # premier, converted earlier to premiér
    # p in -mp, b in -mb will be dropped, but temporarily convert to capital
    # letter so a trace remains below when we handle nasals
    text = re.sub("m([bp])⁀", lambda x: "m" + x.group(1).upper() + "⁀", text)
    # plomb
    # do the following after dropping r so we don't affect -rt
    text = re.sub("[dgpt]⁀", "⁀", text)
    # remove final -e in various circumstances; leave primarily when
    # preceded by two or more distinct consonants; in V[mn]e and Vmme/Vnne,
    # use [MN] so they're pronounced in full
    text = re.sub("(" + vowel_c + ")n+e([⁀‿])", r"\1N\2", text)
    text = re.sub("(" + vowel_c + ")m+e([⁀‿])", r"\1M\2", text)
    text = re.sub("(" + cons_c + r")\1e([⁀‿])", r"\1\2", text)
    text = re.sub("([mn]" + cons_c + ")e([⁀‿])", r"\1\2", text)
    text = re.sub("(" + vowel_c + cons_c + "?)e([⁀‿])", r"\1\2", text)

    # ç; must follow s -> z between vowels (above); do after dropping final s
    # so that ç can be used in respelling to force a pronounced s
    text = re.sub("ç", "s", text)

    # x
    text = re.sub("[eæ]x(" + vowel_c + ")", r"egz\1", text)
    text = re.sub("⁀x", "⁀gz", text)
    text = re.sub("x", "ks", text)

    # double consonants: eCC treated specially, then CC -> C; do after
    # x -> ks so we handle exciter correctly
    text = re.sub(r"⁀e([mn])\1(" + vowel_c + ")", r"⁀en_\1\2", text) # emmener, ennui
    text = re.sub("⁀(h?)[eæ](" + cons_c + r")\2", r"⁀\1é\2", text) # effacer, essui, errer, henné
    text = re.sub("[eæ](" + cons_c + r")\1", r"è\1", text) # mett(r)ons, etc.
    text = re.sub("(" + cons_c + r")\1", r"\1", text) # TO BE FIXED

    # diphthongs
    # uppercase is used to avoid the output of one change becoming the input
    # to another; we later lowercase the vowels; î and û converted early;
    # we do this before i/u/ou before vowel -> glide (for e.g. bleuet),
    # and before nasal handling because e.g. ou before n is not converted
    # into a nasal vowel (Bouroundi, Cameroun); au probably too, but there
    # may not be any such words
    text = re.sub("ou", "U", text)
    text = re.sub("e?au", "O", text)
    text = re.sub("[Ee]uz", "øz", text)
    text = re.sub("[Ee]u([⁀‿])", r"ø\1", text)
    text = re.sub("[Ee][uŭ]", "œ", text)
    text = re.sub("[ae]i", "ɛ", text)

    # Nasalize vowel + n, m
    # Do before syllabification so we syllabify quatre-vingt-un correctly.
    # We affect (1) n before non-vowel, (2) m before b/p (including B/P, which
    # indicate original b/p that are slated to be deleted in words like
    # plomb, champs), (3) -om (nom, dom, pronom, condom, etc.) and
    # (4) -aim/-eim (faim, Reims etc.), (4). We leave alone other m's,
    # including most final m. We do this after diphthongization, which
    # arguably simplifies things somewhat; but we need to handle the
    # 'oi' diphthong down below so we don't run into problems with the 'noi'
    # sequence (otherwise we'd map 'oi' to 'wa' and then nasalize the n
    # because it no longer precedes a vowel).
    text = sub_repeatedly(
        "(.)(" + vowel_c + ")([mn])(" + non_vowel_c + ")",
        repl2,
        text
    )
    # special hack for maximum, aquarium, circumlunaire, etc.
    text = re.sub("um(" + non_vowel_c + ")", r"ɔm\1", text)
    # now remove BP that represent original b/p to be deleted, which we've
    # preserved so far so that we know that preceding m can be nasalized in
    # words like plomb, champs
    text = re.sub("[BP]", "", text)

    # do after nasal handling so 'chinois' works correctly
    text = re.sub("oi", "wA", text)

    # remove silent h
    # do after diphthongs to keep vowels apart as in envahir, but do
    # before syllabification so it is ignored in words like hémorrhagie
    text = re.sub("h", "", text)

    # syllabify
    # (1) break up VCV as V.CV, and VV as V.V; repeat to handle successive
    #     syllables
    text = sub_repeatedly(
        "(" + vowel_maybe_nasal_r + opt_syljoiners_c + ")" + \
        "(" + real_cons_c + "?" + \
        opt_syljoiners_c + oral_vowel_c + ")",
        r"\1.\2",
        text
    )
    # (2) break up other VCCCV as VC.CCV, and VCCV as VC.CV; repeat to handle successive syllables
    text = sub_repeatedly(
        "(" + vowel_maybe_nasal_r + opt_syljoiners_c + \
        real_cons_c + opt_syljoiners_c + ")" + \
        "(" + real_cons_c + cons_or_joiner_c + \
        "*" + oral_vowel_c + ")",
        r"\1.\2",
        text
    )

    def resyllabify(text):
        def resyllabify_repl1(match):
            lparen, c1, j1, j2, c2 = \
                match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)
            if allow_onset_2(c1, c2):
                return "." + lparen + c1 + j1 + j2 + c2
            return match.group()
        def resyllabify_repl2(match):
            j1, c1, rparen, j2, c2 = \
                match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)
            if not allow_onset_2(c1, c2) and not (c1 == "s" and re.search("^[ptk]$", c2)):
                return j1 + c1 + rparen + "." + j2 + c2
            return match.group()

        # (3) resyllabify C.C as .CC for various CC that can form an onset:
        #     resyllabify C.[lr] as .C[lr] for C = various obstruents;
        #     resyllabify d.ʒ, C.w, C.ɥ, C.j as .dʒ, .Cw, .Cɥ, .Cj (C.w comes from
        #     written Coi; C.ɥ comes from written Cuill; C.j comes e.g. from
        #     des‿yeux, although most post-consonantal j generated later);
        #     don't resyllabify j.j
        text = re.sub(
            "(\(?)(" + real_cons_c + ")" + \
            "(" + opt_syljoiners_c + ")\." + \
            "(" + opt_syljoiners_c + ")" + \
            "(" + real_cons_c + ")",
            resyllabify_repl1,
            text
        )

        # (4) resyllabify .CC as C.C for CC that can't form an onset (opposite of
        #     the previous step); happens e.g. in ouest-quart
        text = re.sub(
            "\.(" + opt_syljoiners_c + ")" + \
            "(" + real_cons_c + ")(\)?)" + \
            "(" + opt_syljoiners_c + ")" + \
            "(" + real_cons_c + ")",
            resyllabify_repl2,
            text
        )

        # (5) fix up dʒ and tʃ followed by another consonant (management respelled
        #     'manadjment' or similar)
        text = re.sub(
            "\.([\(]?[dt]" + opt_syljoiners_c + "[ʒʃ])" + \
            "(" + opt_syljoiners_c + ")" + \
            "(" + real_cons_c + ")",
            r"\1.\2\3",
            text
        )
        return text

    text = resyllabify(text)

    # (6) eliminate diaeresis (note, uï converted early)
    text = re.sub("[äëïöüÿ]", repl3, text)

    # single vowels
    text = re.sub("â", "ɑ", text)
    # don't do this, too many exceptions
    # text = re.sub("a(\.?)z", r"ɑ\1z", text)
    text = re.sub("ă", "a", text)
    text = re.sub("e\.j", "ɛ.j", text) # réveiller
    text = sub_repeatedly(
        "e\.(" + cons_no_liaison_c + '*' + vowel_c + ")",
        r"ə.\1",
        text
    )
    text = re.sub("e([⁀‿])", r"ə\1", text)
    text = re.sub("æ\.", "é.", text)
    text = re.sub("æ([⁀‿])", r"é\1", text)
    text = re.sub("[eèêæ]", "ɛ", text)
    text = re.sub("é", "e", text)
    text = re.sub("o([⁀‿])", r"O\1", text)
    text = re.sub("o(\.?)z", r"O\1z", text)
    text = re.sub("[oŏ]", "ɔ", text)
    text = re.sub("ô", "o", text)
    text = re.sub("u", "y", text)

    # other consonants
    text = re.sub("r", "ʁ", text)
    text = re.sub("g", "ɡ", text) # use IPA variant of g

    # (mostly) final schwa deletions (FIXME, combine with schwa deletions below)
    # 1. delete all instances of ė
    text = re.sub("\.([^.⁀]+)ė", r"\1", text)
    # 2. delete final schwa, only in the last word, not in single-syllable word
    #    (⁀. can occur after a hyphen, e.g. in puis-je)
    text = re.sub("([^⁀])\.([^ə.⁀]+)ə⁀⁀", r"\1\2⁀", text)
    # 3. delete final schwa before vowel in the next word, not in a single-
    #    syllable word (croyez-le ou non); the out-of-position \4 looks weird
    #    but the effect is that we preserve the initial period when there's a
    #    hyphen and period after the schwa (con.tre-.a.tta.quer ->
    #    con.tra.tta.quer) but not across a space (con.tre a.tta.quer ->
    #    contr a.tta.quer)
    text = re.sub(
        "([^⁀])\.([^ə.⁀]+)ə⁀([⁀ \-]*)(\.?)(" + vowel_c + ")",
        r"\1\4\2⁀\3\5",
        text
    )
    # 4. delete final schwa before vowel in liaison, not in a single-syllable
    #    word
    text = re.sub("([^⁀]\.[^ə.⁀]+)ə‿\.?(" + vowel_c + ")", r"\1‿\2", text)
    # 5. delete schwa after any vowel (agréerons, soierie)
    text = re.sub("(" + vowel_c + ").ə", r"\1", text)
    # 6. make final schwa optional after two consonants except fricative + approximant
    text = re.sub(
        "(" + cons_c + ")(" + "\.?" + ")(" + cons_c + ")ə⁀",
        repl4,
        text
    )

    # i/u/ou -> glide before vowel
    # -- do from right to left to handle continuions and étudiions
    #    correctly
    # -- do repeatedly until no more subs (required due to right-to-left
    #    action)
    # -- convert to capital J and W as	a signal that we can convert them
    #    back to /i/ and /u/ later on if they end up preceding a schwa or
    #    following two consonants in the same syllable, whereas we don't
    #    do this to j from other sources (y or ill) and w from other
    #    sources (w or oi); will be lowercased later; not necessary to do
    #    something similar to ɥ, which can always be converted back to /y/
    #    because it always originates from /y/.
    while True:
        new_text = re.sub("^(.*)i\.?(" + vowel_c + ")", r"\1J\2", text)
        new_text = re.sub("^(.*)y\.?(" + vowel_c + ")", r"\1ɥ\2", new_text)
        new_text = re.sub("^(.*)U\.?(" + vowel_c + ")", r"\1W\2", new_text)
        if new_text == text:
            break
        text = new_text

    # hack for agréions, pronounced with /j.j/
    text = re.sub("e.J", "ej.J", text)

    # glides -> full vowels after two consonants in the same syllable
    # (e.g. fl, tr, etc.), but only glides from original i/u/ou (see above)
    # and not in the sequence 'ui' (e.g. bruit), and only when the second
    # consonant is l or r (not in abstiennent)
    text = re.sub("(" + cons_c + "[lʁ])J(" + vowel_c + ")", r"\1i.j\2", text)
    text = re.sub("(" + cons_c + "[lʁ])W(" + vowel_c + ")", r"\1u.\2", text)
    text = re.sub("(" + cons_c + "[lʁ])ɥ(" + vowel_no_i_c + ")", r"\1y.\2", text)
    # remove _ that prevents interpretation of letter sequences; do this
    # before deleting internal schwas
    text = re.sub("_", "", text)

    # internal schwa
    # 1. delete schwa in VCəCV sequence word-internally when neither V is schwa,
    #    except in ʁəʁ sequence (déchirerez); use uppercase schwa when not
    #    deleting it, see below; FIXME, we might want to prevent schwa deletion
    #    with other consonant sequences
    text = sub_repeatedly(
        "(" + vowel_no_schwa_c + ")\." + \
        "(" + real_cons_c + ")ə\." + \
        "(" + real_cons_c + ")" + \
        "(" + vowel_no_schwa_c + ")",
        repl5,
        text
    )
    # 2. make optional internal schwa in remaining VCəCV sequences, including
    # across words, except between certain pairs of consonants (FIXME, needs
    # to be smarter); needs to happen after /e/ -> /ɛ/ before schwa in next
    # syllable and after removing ' and _ (or we need to take them into account);
    # include .* so we go right-to-left, convert to uppercase schwa so
    # we can handle sequences of schwas and not get stuck if we want to
    # leave a schwa alone.
    text = sub_repeatedly(
        "(.*" + vowel_c + opt_schwajoiners_c + ")" + \
        "(" + real_cons_c + ")" + \
        "(" + opt_schwajoiners_c + ")ə" + \
        "(" + opt_schwajoiners_c + ")" + \
        "(" + real_cons_c + ")" + \
        "(" + opt_schwajoiners_c + vowel_c + ")",
        repl6,
        text
    )

    # lowercase any uppercase letters (AOUMNJW etc.); they were there to
    # prevent certain later rules from firing
    text = text.lower()

    # ĕ forces a pronounced schwa
    text = re.sub("ĕ", "ə", text)

    # need to resyllabify again in cases like 'saladerie', where deleting the
    # schwa above caused a 'd.r' boundary that needs to become '.dr'.
    text = resyllabify(text)

    # convert apostrophe to joiner/liaison marker
    text = re.sub("'", "‿", text)
    # remove hyphens and word-boundary markers
    text = re.sub("[⁀\-]", "", text)

    return text
