# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long, invalid-name
"""Implements the template {{ru-IPA}}.
Modified from https://en.wiktionary.org/wiki/Module:ru-pron Lua module partially.
Rewritten from Author: Originally Wyang; rewritten by Benwing;
additional contributions from Atitarev and a bit from others


FIXME:

1. (DONE) Geminated /j/ from -йя-: treat as any other gemination, meaning it
   may not always be pronounced geminated. Currently we geminate it very late,
   after all the code that reduces geminates. Should be done earlier and
   places that include regexps with /j/ should be modified to also include
   the gemination marker ː. Words with йя: аллилу́йя, ауйяма, ва́йя, ма́йя,
   папа́йя, парано́йя, пира́йя, ра́йя, секво́йя, Гава́йям.
2. (DONE) Should have geminated jj in йе (occurs in e.g. фойе́). Should work
   with gem=y (see FIXME #1). Words with йе: фойе́, колба Эрленмейера, скала
   Айерс, Айерс-Рок, йети, Кайенна, конве́йер, конвейерный, сайентология,
   фейерверк, Гава́йев. Note also Гава́йи with йи.
3. (DONE, CINEMANTIQUE OK WITH FIXES) In Асунсьо́н and Вьентья́н, put a syllable
   break after the н and before consonant + /j/. Use the perm_syl_onset
   mechanism or at least the code that accesses that mechanism. Should
   possibly do this also in VCʲj and V‿Cʲj and VCj and V‿Cj sequences;
   ask Cinemantique if this makes sense.
4. (DONE, CINEMANTIQUE OK WITH FIXES) Fix non-palatal е in льстец.  Other
   words that will be affected (and probably wrong): льви́ца, львя́тник,
   льняно́й, льстить, льди́на, львиный, manual pronunciation given as lʲvʲit͡sə
   and lʲvʲɵnək. Ask Cinemantique.
5. (DONE, CINEMANTIQUE SAYS NO IT DOESN'T) In львёнок, rendered as ˈlʲvɵnək
   instead of ˈlʲvʲɵnək. Apparently same issue as льстец, having to do with
   ь in beginning. This apparently has to do with the "assimilative
   palatalization of consonants when followed by front vowels" code, which
   blocks palatalization when the syllable begins with a cluster with a hard
   sign, or a soft sign followed by a consonant. Then "retraction of front
   vowels in syllables blocking assimilative palatalization" converts e to ɛ
   and i to y in such cases of blocked palatalization (not needed for žcš,
   which are handled by phon_respellings). Ask Cinemantique if this whole
   business makes any sense.
6. (DONE) In prefixes/suffixes like -ин, treat single syllable word as
   unstressed. Also support tilde to force unstressed syllable.
7. (DONE) In ни́ндзя, дз becomes palatal and н should palatal-assimilate to it.
8. (DONE) In под сту́лом, should render as pɐt͡s‿ˈstuləm when actually renders as
   pɐˈt͡s‿stuləm. Also occurs in без ша́пки (bʲɪˈʂ‿ʂapkʲɪ instead of
   bʲɪʂ‿ˈʂapkʲɪ); has something to do with ‿. Similarly occurs in
   не к ме́сту, which should render as nʲɪ‿k‿ˈmʲestʊ, and от я́блони, which
   should render as ɐt‿ˈjæblənʲɪ.
9. (STILL UNCLEAR) In собра́ние, Anatoli renders it as sɐˈbranʲɪ(j)ə with
   optional (j). Ask him when this exactly applies. Does it apply in all ɪjə
   sequences? Only word-finally? Also ijə?
10. (DONE) убе́жищa renders as ʊˈbʲeʐɨɕːʲə instead of ʊˈbʲeʐɨɕːə; уда́ча
   similarly becomes ʊˈdat͡ɕʲə instead of ʊˈdat͡ɕə.
10a. (DONE) Remove the "offending clause" just mentioned, labeled FIXME (10a),
   and fix it as the comment above it describes.
10b. (DONE) Remove the clause labeled "FIXME (10b)".
10c. (DONE) Investigate the clause labeled "FIXME (10c)".  This relates to
   FIXME #9 above concerning собра́ние.
10d. (DONE, NEEDS TESTING) Investigate the clause labeled "FIXME (10d)"
   and apply the instructions there about removing a line and seeing
   whether anything changes.
11. (DONE) тро́лль renders with geminated final l, and with ʲ on wrong side of
   gemination (ːʲ instead of ʲː); note how this also occurs above in -ɕːʲə
   from убе́жищa. (This issue with тро́лль will be masked by the change to
   generally degeminate l; use фуррь; note also галльский.)
12. (DONE, NEEDS TESTING) May be additional errors with gemination in
    combination with explicit / syllable boundary, because of the code
	expecting that syllable breaks occur in certain places; should probably
	rewrite the whole gemination code to be less fragile and not depend on
	exactly where syllable breaks occur in consonant clusters, which it does
	now (might want to rewrite to avoid the whole business of breaking by
	syllable and processing syllable-by-syllable).
13. Many assimilations won't work properly with an explicit / syllable
   boundary.
14. (DONE, ASK WYANG FOR ITS PURPOSE) Eliminate pal=y. Consider first asking
   Wyang why this was put in originally.
15. (DONE) Add test cases: Цю́рих, от а́ба, others.
15a. (DONE) Add test cases: фуррь, по абази́ну (for assimilation of schwas
    across ‿)
15b. (DONE) Add test case англо-норма́ннский (to make sure degemination of нн
    occurs when not between vowels), multi-syllable word ending in a geminate:
	ато́лл (not so good because лл always degeminated), коло́сс, Иоа́нн (good
	because of нн), ха́ос, эвфеми́зм, хору́гвь (NOTE: ruwikt claims гв is voiced,
	I doubt it, ask Cinemantique), наря́д на ку́хню (non-devoicing of д before
	н in next word, ask Cinemantique about this, does it also apply to мрл?),
	ко̀е-кто́
16. (DONE, ADDED SPECIAL HACK; REMOVED WITH NEW FINAL-Е CODE, SHOULD HANDLE
    THROUGH pos=pro; DOESN'T HAVE ANYTHING TO DO WITH SECONDARY STRESS ON О)
	Caused a change in ко̀е-кто́, perhaps because I rewrote code that accepted
	an acute or circumflex accent to also take a grave accent. See how кое is
	actually pronounced here and take action if needed. (ruwiki claims кое is
	indeed pronounced like кои, ask Cinemantique what the rule for final -е
	is and why different in кое vs. мороженое, anything to do with secondary
	stress on о?)
17. (DONE) Rewrote voicing/devoicing assimilation; should make assimilation of
    эвфеми́зм automatic and not require phon=.
18. (DONE) Removed redundant fronting-of-a code near end; make sure this
    doesn't change anything.
19. (DONE, ANSWER IS YES) do сь and зь assimilate before шж, and
    if so do they become ɕʑ? Ask Cinemantique.
20. (DONE) Add pos= to handle final -е. Possibilities appear to be neut
    (neuter noun), adj (adjective, autodetected whether singular or plural),
	comp (comparative), pre (prepositional case), adv (adverb), verb or v (2nd
	plural verb forms).
21. (DONE, DEVOICE UNLESS NEXT WORD BEGINS WITH VOICED OBSTRUENT OR V+VOICED
    OBSTRUENT) Figure out what to do with devoicing or non-devoicing before
	mnrlv vowel. Apparently non-devoicing before vowel is only in fast speech
	with a close juncture and Anatoli doesn't want that; but what about before
	the consonants?
22. (DONE) Figure out what to do with fronting of a and u after or between
	soft consonants, esp. when triggered by a following soft consonant with
	optional or compulsory assimilation. Probably the correct thing to do
	in the case of optional assimilation is to give two pronunciations
	separated by commas, one with non-front vowel + hard consonant, the
	other with front vowel + soft consonant.
23. (DONE, OK) Implement compulsory assimilation of xkʲ; ask Cinemantique to
    make sure this is correct.
24. (DONE, BUT ANATOLI THINKS CONJUNCTION A MIGHT NOT BE REDUCED) Add а to
    list of unstressed particles, but only recognize it and о (and perhaps all
	the others) when not followed by a hyphen; then fix unnecessary cases with
	о̂ (look at tracking cflex category) and the various hacks used in а ведь,
	а сейчас, а то, а не то, а также, а как же; will need to add а̂ to а капелла
	and possibly elsewhere; use different-pron tracking to catch this.
25. (DONE) Add / before цз, чж in Chinese words to ensure syllable boundary in
    right place; ensure that this doesn't mess things up when occurring at
	beginning of word or whatever.
26. (DONE) Rule on voicing assimilation before v: It says in Chew "A
    Computational Phonology of Russian" that v is an obstruent before
	obstruents and a sonorant before sonorants, i.e. v triggers voicing
	assimilation if followed by an obstruent; verify that our code works this
	way.
27. (DONE, NEEDS TESTING) Implement _ to block all assimilation; probably this
    will happen automatically and we just need to remove the _ at the end.
28. (NOT DONE, NOT CORRECT) Change unstressed palatal o to have values like
    regular o, for words like майора́т, Ога́йо, Йоха́ннесбург
29. (DONE) If we need partial reduction of non-final е/я to [ə] instead of [ɪ],
    one way is to use another diacritic, e.g. dot-under; or use a spelling
	like ьа.
30. (DONE) BUG: воѐнно-морско́й becomes [vɐˌenːə mɐrˈskoj] without [je], must be
    due to ѐ being a composed character (may be a bug in the translit module;
	add a test case).
31. In в Япо́нии, в Евро́пе, the initial [j] should be required not optional.
32. (DONE) Should be possible to write п(ь)я́нка, скам(ь)я́ and get optional
    palatalization.
33. (CODE PRESENT BUT NOT COMPLETED) Final unstressed -е that becomes [e]
    should become [ɪ] when not followed by end of utterance or pause.
34. In То́гане (phon=То́ганэ), final -э should be pronounced [e]. Should apply
    in general to -э after paired consonants, but not to e.g. се́рдце.
35. (DONE) тц,дц,тч,дч shoud be always-geminated by default.
36. (DONE) treat ! and ? as separate words so we don't have issues with
    word-final -е before them.
37. (DONE) Distinguish stress accents from other accents.
38. т(ь)ся not directly after the stress should be optionally geminated.
39. (DONE) нра̀вственно-эти́ческий should have optional not mandatory gemination
    of нн.
40. (DONE) Make дц in -дцат- be optionally-geminated, for words like
    одиннадцать, двадцать, тридцатый, etc.
41. (DONE) Don't show grave accents in annotations (but do in phon=).
42. (DONE) -чш- (as in лучший) should be pronounced as -тш-.
43. (DONE) Fix fronting of [au] in two syllables in a row.
44. (DONE) Add pos=imp for imperatives, use it to treat -ться differently from
    infinitives.
45. (DONE) CFLEX should not be treated as stress for the purpose of determining
    whether written а reduces to [ɐ] or [ə].
46. (DONE) Fix [дт]ьт, [сз]ьс sequences (esp. in imperatives) and make
    palatalization of labials optional in [мбпфв]ь[ст][еияёю] (again esp. in
    imperatives).
47. (DONE) Optional palatalization of -ся should apply only to -лся, not always.
48. (DONE) Reduction of стл -> сл should apply only in стлив, not always.
49. (DONE) Convert счит -> щит by default, as with счёт.
50. (DONE) Don't require that m_ru_translit.apply_tr_fixes() be called prior
    to ipa(), but include an argument so that text transformed this way can
    be passed in.
51. (DONE) pos=X/Y and gem=X/Y should require same number of elements as actual
    words rather than counting phonetically-joined words.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import regex as re
from . import ru_common as com
from . import ru_translit


def list_to_set(lst):
    """convert list to set"""
    res = {}
    for each in lst:
        res[each] = True
    return res

remove_grave_accents_from_phonetic_respelling = True # Anatoli's desired value

def sub_repeatedly(pattern, repl, term):
    """apply sub() repeatedly until no change"""
    while True:
        new_term = re.sub(pattern, repl, term)
        if new_term == term:
            return term
        term = new_term

# If enabled, compare this module with new version of module in
# Module:User:Benwing2/ru-pron to make sure all pronunciations are the same.
# To check for differences, go to Template:tracking/ru-pron/different-pron
# and look at what links to the page.
# test_new_ru_pron_module = False

# If enabled, do new code for final -е; else, the old way
new_final_e_code = True
# If enabled, do special case for final -е not before a pause
final_e_non_pausal = False

AC = u"\u0301" # acute =  ́
GR = u"\u0300" # grave =  ̀
CFLEX = u"\u0302" # circumflex =  ̂
DUBGR = u"\u030F" # double grave =  ̏
DOTABOVE = u"\u0307" # dot above =  ̇
DOTBELOW = u"\u0323" # dot below =  ̣
TEMPCFLEX = u"\uFFF1" # placeholder to be converted to a circumflex

vow = "aeiouyɛəäạëöü"
ipa_vow = vow + "ɐɪʊɨæɵʉ"
vowels, vowels_c = "[" + vow + "]", "([" + vow + "])"
# No need to include DUBGR here because we rewrite it to CFLEX very early
acc = AC + GR + CFLEX + DOTABOVE + DOTBELOW
accents = "[" + acc + "]"
stress_accents = "[" + AC + GR + "]"

perm_syl_onset = list_to_set([
    "spr", "str", "skr", "spl", "skl",
    # FIXME, do we want sc?
    "sp", "st", "sk", "sf", "sx", "sc",
    "pr", "br", "tr", "dr", "kr", "gr", "fr", "vr", "xr",
    "pl", "bl", "kl", "gl", "fl", "vl", "xl",
    # FIXME, do we want the following? If so, do we want vn?
    "ml", "mn",
    # FIXME, dž is now converted to ĝž, which will have a syllable
    # boundary in between
    "šč", "dž",
])

# FIXME: Consider changing ӂ internally to ʑ to match ɕ (it is used externally
# in e.g. дроӂӂи (pronunciation spelling of дрожжи)
translit_conv = {
    "c": "t͡s", "č": "t͡ɕ", "ĉ": "t͡ʂ",
    "g": "ɡ", "ĝ": "d͡ʐ",
    "ĵ": "d͡z", "ǰ": "d͡ʑ", "ӂ": "ʑ",
    "š": "ʂ", "ž": "ʐ",
}

translit_conv_j = {
    "cʲ": "t͡sʲ",
    "ĵʲ": "d͡zʲ",
}

allophones = {
    "a": ("a", "ɐ", "ə"),
    "e": ("e", "ɪ", "ɪ"),
    "i": ("i", "ɪ", "ɪ"),
    "o": ("o", "ɐ", "ə"),
    "u": ("u", "ʊ", "ʊ"),
    "y": ("ɨ", "ɨ", "ɨ"),
    "ɛ": ("ɛ", "ɨ", "ɨ"),
    "ä": ("a", "ɪ", "ɪ"),
    "ạ": ("a", "ɐ", "ə"),
    "ë": ("e", "ɪ", "ɪ"),
    "ö": ("ɵ", "ɪ", "ɪ"),
    "ü": ("u", "ʊ", "ʊ"),
    "ə": ("ə", "ə", "ə"),
}

devoicing = {
    "b": "p", "d": "t", "g": "k",
    "z": "s", "v": "f",
    "ž": "š", "ɣ": "x",
    "ĵ": "c", "ǰ": "č", "ĝ": "ĉ",
    "ӂ": "ɕ",
}

voicing = {
    "p": "b", "t": "d", "k": "g",
    "s": "z", "f": "v",
    "š": "ž", "c": "ĵ", "č": "ǰ", "ĉ": "ĝ",
    "x": "ɣ", "ɕ": "ӂ",
}

iotating = {
    "a": "ä",
    "e": "ë",
    "o": "ö",
    "u": "ü",
}

retracting = {
    "e": "ɛ",
    "i": "y",
}

fronting = {
    "a": "æ",
    "u": "ʉ",
    "ʊ": "ʉ",
}

# Prefixes that we recognize specially when they end in a geminated
# consonant. The first element is the result after applying voicing/devoicing,
# gemination and other changes. The second element is the original spelling,
# so that we don't overmatch and get cases like Поттер. We check for these
# prefixes at the beginning of words and also preceded by ne-, po- and nepo-.
geminate_pref = [
    # "abː", #"adː",
    ("be[szšž]ː", "be[sz]"),
    # "braomː",
    ("[vf]ː", "v"),
    ("vo[szšž]ː", "vo[sz]"),
    ("i[szšž]ː", "i[sz]"),
    # "^inː",
    ("kontrː", "kontr"),
    ("superː", "super"),
    ("tran[szšž]ː", "trans"),
    ("na[tdcč]ː", "nad"),
    ("ni[szšž]ː", "ni[sz]"),
    ("o[tdcč]ː", "ot"), # "^omː",
    ("o[bp]ː", "ob"),
    ("obe[szšž]ː", "obe[sz]"),
    ("po[tdcč]ː", "pod"),
    ("pre[tdcč]ː", "pred"), # "^paszː", "^pozː",
    ("ra[szšž]ː", "ra[sz]"),
    ("[szšž]ː", "[szšž]"), # ž on right for жжёт etc., ш on left for США
    ("me[žš]ː", "mež"),
    ("če?re[szšž]ː", "če?re[sz]"),
    # certain double prefixes involving ra[zs]-
    ("predra[szšž]ː", "predra[sz]"),
    ("bezra[szšž]ː", "bezra[sz]"),
    ("nara[szšž]ː", "nara[sz]"),
    ("vra[szšž]ː", "vra[sz]"),
    ("dora[szšž]ː", "dora[sz]"),
    # "^sverxː", "^subː", "^tröxː", "^četyröxː",
]

sztab = {
    "s": "cs",
    "z": "ĵz",
}
def ot_pod_sz(match):
    pre, sz = match.group(1), match.group(2)
    return pre + sztab[sz]

phonetic_subs = [
    ("h", "ɣ"),

    ("šč", "ɕː"), # conversion of šč to geminate

    # the following group is ordered before changes that affect ts
    ("n[dt]sk", "n(t)sk"),
    ("s[dt]sk", "sck"),

    # Add / before цз, чж sequences (Chinese words) and assimilate чж
    ("cz", "/cz"),
    ("čž", "/ĝž"),

    # main changes for affricate assimilation of [dt] + sibilant, including ts;
    # we either convert to "short" variants t͡s, d͡z, etc. or to "long" variants
    # t͡ss, d͡zz, etc.
    # 1. т с, д з across word boundary, also т/с, д/з with explicitly written
    #    slash, use long variants.
    ("[dt](ʹ?[ ‿⁀/]+)s", r"c\1s"),
    ("[dt](ʹ?[ ‿⁀/]+)z", r"ĵ\1z"),
    # 2. тс, дз + vowel use long variants.
    ("[dt](ʹ?)s(j?" + vowels + ")", r"c\1s\2"),
    ("[dt](ʹ?)z(j?" + vowels + ")", r"ĵ\1z\2"),
    # 3. тьс, дьз use long variants.
    ("[dt]ʹs", "cʹs"),
    ("[dt]ʹz", "ĵʹz"),
    # 4. word-initial от[сз]-, под[сз]- use long variants because there is
    #    a morpheme boundary.
    ("(⁀o" + accents + "?)t([sz])", ot_pod_sz),
    ("(⁀po" + accents + "?)d([sz])", ot_pod_sz),
    # 5. other тс, дз use short variants.
    ("[dt]s", "c"),
    ("[dt]z", "ĵ"),
    # 6. тш, дж always use long variants (FIXME, may change)
    ("[dtč](ʹ?[ \-‿⁀/]*)š", r"ĉ\1š"),
    ("[dtč](ʹ?[ \-‿⁀/]*)ž", r"ĝ\1ž"),
    # 7. soften palatalized hard hushing affricates resulting from the previous
    ("ĉʹ", "č"),
    ("ĝʹ", "ǰ"),

    # changes that generate ɕː and ɕč through assimilation:
    # зч and жч become ɕː, as does сч at the beginning of a word and in the
    # sequence счёт when not following [цдт] (подсчёт); else сч becomes ɕč
    # (отсчи́тываться), as щч always does (рассчитáть written ращчита́ть)
    ("[cdt]sč", "čɕː"),
    ("ɕːč", "ɕč"),
    ("[zž]č", "ɕː"),
    ("[szšž]ɕː?", "ɕː"),
    ("⁀sč", "⁀ɕː"),
    ("sč(j?[oi]" + accents + "?)t", r"ɕː\1t"),
    ("sč", "ɕč"),

    # misc. changes for assimilation of [dtsz] + sibilants and affricates
    ("[sz][dt]c", "sc"),
    ("([rn])[dt]([cč])", r"\1\2"),
    # -дцат- (in numerals) has optionally-geminated дц
    ("dca(" + accents + "?)t", r"c(c)a\1t"),
    # дц, тц, дч, тч + vowel always remain geminated, so mark this with ˑ;
    # if not followed by a vowel, as in e.g. путч, use normal gemination
    # (it will normally be degeminated)
    ("[dt]([cč])(" + vowels + ")", r"\1ˑ\2"),
    ("[dt]([cč])", r"\1\1"),
    # the following is ordered before the next one, which applies assimilation
    # of [тд] to щ (including across word boundaries)
    ("n[dt]ɕ", "nɕ"),
    # [сз] and [сз]ь before soft affricates [щч], including across word
    # boundaries; note that the common sequence сч has already been handled
    ("[zs]ʹ?([ ‿⁀/]*[ɕč])", r"ɕ\1"),
    # reduction of too many ɕ"s, which can happen from the previous
    ("ɕɕː", "ɕː"),
    # assimilation before [тдц] and [тдц]ь before щ
    ("[cdt]ʹ?([ ‿⁀/]*)ɕ", r"č\1ɕ"),
    # assimilation of [сз] and [сз]ь before [шж]
    ("[zs]([ ‿⁀/]*)š", r"š\1š"),
    ("[zs]([ ‿⁀/]*)ž", r"ž\1ž"),
    ("[zs]ʹ([ ‿⁀/]*)š", r"ɕ\1š"),
    ("[zs]ʹ([ ‿⁀/]*)ž", r"ӂ\1ž"),
    # assimilation of [сз]ь before с[еияёю] (in imperatives esp. before ся)
    ("[zs]ʹs([eij])", r"sˑ\1"),
    # assimilation of [тд]ь before т[еияёю] (e.g. in imperatives esp. before те)
    ("[td]ʹt([eij])", r"tˑ\1"),

    # optional palatalization of palatalized labials before another consonant
    # in [ст][еияёю] (esp. in imperatives before -те, -ся)
    # FIXME, perhaps we should either generalize this or restrict it only
    # to imperatives
    ("([mpbfv])ʹ([st][eij])", r"\1(ʹ)\2"),

    ("sverxi", "sverxy"),
    ("stʹd", "zd"),
    # this will often become degeminated
    ("tʹd", "dd"),

    # loss of consonants in certain clusters
    ("([ns])[dt]g", r"\1g"),
    ("zdn", "zn"),
    ("lnc", "nc"),
    ("[sz]t(li" + accents + "?v)", r"s\1"),
    ("[sz]tn", "sn"),

     # backing of /i/ after hard consonants in close juncture
    ("([mnpbtdkgfvszxɣrlšžcĵĉĝ])⁀‿⁀i", r"\1⁀‿⁀y"),
]

cons_assim_palatal = {
    # assimilation of tn, dn, sn, zn, st, zd, nč, nɕ is handled specially
    "compulsory": list_to_set([
        "ntʲ", "ndʲ", "xkʲ",
        "csʲ", "ĵzʲ", "ncʲ", "nĵʲ",
    ]),
    "optional": list_to_set([
        "slʲ", "zlʲ", "nsʲ", "nzʲ",
        "mpʲ", "mbʲ", "mfʲ", "fmʲ",
    ])
}

# words which will be treated as accentless (i.e. their vowels will be
# reduced), and which will liaise with a preceding or following word;
# this will not happen if the words have an accent mark, cf.
# по́ небу vs. по не́бу, etc.
accentless = {
    # class "pre": particles that join with a following word
    "pre": list_to_set([
        "bez", "bliz", "v", "vo", "da", "do",
        "za", "iz", "iz-pod", "iz-za", "izo", "k", "ko", "mež",
        "na", "nad", "nado", "ne", "ni", "ob", "obo", "ot", "oto",
        "pered", "peredo", "po", "pod", "podo", "pred", "predo", "pri", "pro",
        "s", "so", "u", "čerez",
    ]),
    # class "prespace": particles that join with a following word, but only
    #   if a space (not a hyphen) separates them; hyphens are used here
    #   to spell out letters, e.g. а-эн-бэ́ for АНБ (NSA = National Security
    #   Agency) or о-а-э́ for ОАЭ (UAE = United Arab Emirates)
    "prespace": list_to_set(["a", "o"]),
    # class "post": particles that join with a preceding word
    "post": list_to_set([
        "by", "b", "ž", "že", "li", "libo", "lʹ", "ka",
        "nibudʹ", "tka"
    ]),
    # class "posthyphen": particles that join with a preceding word, but only
    #   if a hyphen (not a space) separates them
    "posthyphen": list_to_set(["to"]),
}

# Pronunciation of final unstressed -е, depending on the part of speech and
#   exact ending. Also used for pronunciation of -ться in imperatives vs.
#   infinitives.
#
# Endings:
#   oe = -ое
#   ve = any other vowel plus -е (FIXME, may have to split out -ее)
#   je = -ье
#   softpaired = soft paired consonant + -е
#   hardsib = hard sibilant (ц, ш, ж) + -е
#   softsib = soft sibilant (ч, щ) + -е
#
# Parts of speech:
#   def = default used in absence of pos
#   n/noun = neuter noun in the nominative/accusative singular (but not ending
#     in adjectival -ое or -ее; those should be considered as adjectives)
#   pre = prepositional case singular
#   dat = dative case singular (treated same as prepositional case singular)
#   voc = vocative case (currently treated as 'mid')
#   nnp = noun nominative plural in -е (гра́ждане, боя́ре, армя́не); not
#     adjectival plurals in -ие or -ые, including adjectival nouns
#     (да́нные, а́вторские)
#   inv = invariable noun or other word (currently treated as 'mid')
#   a/adj = adjective or adjectival noun (typically either neuter in -ое or
#     -ее, or plural in -ие, -ые, or -ье, or short neuter in unpaired
#     sibilant + -е)
#   c/com = comparative (typically either in -ее or sibilant + -е)
#   adv = adverb
#   p = preposition (treated same as adverb)
#   v/vb/verb = finite verbal form (usually 2nd-plural in -те), but not
#     imperatives (use pos=imp) and not participle forms, which should be
#     treated as adjectives
#   pro = pronoun (кое-, какие-, ваше, сколькие)
#   num = number (двое, трое, обе, четыре; currently treated as 'mid')
#   pref = prefix (treated as 'high' because integral part of word)
#   hi/high = force high values ([ɪ] or [ɨ])
#   mid = force mid values ([e] or [ɨ])
#   lo/low/schwa = force low, really schwa, values ([ə])
#
# Possible values:
#   1. ə [ə], e [e], i [ɪ] after a vowel or soft consonant
#   2. ə [ə] or y [ɨ] after a hard sibilant
#
# If a part of speech doesn't have an entry for a given type of ending,
#   it receives the default value. If a part of speech's entry is a string,
#   it's an alias for another way of specifying the same part of speech
#   (e.g. n=noun).
pos_properties = {
    "def": {"oe": "ə", "ve": "e", "je": "e", "softpaired": "e", "hardsib": "y", "softsib": "e", "tsjapal": "n"},
    "noun": {"oe": "ə", "ve": "e", "je": "e", "softpaired": "e", "hardsib": "ə", "softsib": "e"},
    "n": "noun",
    "pre": {"oe": "e", "ve": "e", "softpaired": "e", "hardsib": "y", "softsib": "e"},
    "dat": "pre",
    "voc": "mid",
    "nnp": {"softpaired": "e"}, # FIXME, not sure about this
    "inv": "mid", # FIXME, not sure about this (e.g. вице-, кофе)
    "adj": {"oe": "ə", "ve": "e", "je": "ə"}, # FIXME: Not sure about -ее, e.g. neut adj си́нее; FIXME, not sure about short neuter adj, e.g. похо́же from похо́жий, дорогосто́яще from дорогосто́ящий, should this be treated as neuter noun?
    "a": "adj",
    "com": {"ve": "e", "hardsib": "y", "softsib": "e"},
    "c": "com",
    "adv": {"softpaired": "e", "hardsib": "y", "softsib": "e"},
    "p": "adv", # FIXME, not sure about prepositions
    "verb": {"softpaired": "e"},
    "v": "verb",
    "vb": "verb",
    # Imperatives like other verbs except that final -ться is palatalized
    "imp": {"softpaired": "e", "tsjapal": "y"},
    "impv": "imp",
    "pro": {"oe": "i", "ve": "i"}, # FIXME, not sure about ваше, сколькие, какие-, кое-
    "num": "mid", # FIXME, not sure about обе
    "pref": "high",
    # forced values
    "high": {"oe": "i", "ve": "i", "je": "i", "softpaired": "i", "hardsib": "y", "softsib": "i"},
    "hi": "high",
    "mid": {"oe": "e", "ve": "e", "je": "e", "softpaired": "e", "hardsib": "y", "softsib": "e"},
    "low": {"oe": "ə", "ve": "ə", "je": "ə", "softpaired": "ə", "hardsib": "ə", "softsib": "ə"},
    "lo": "low",
    "schwa": "low",
}

def ine(x):
    """convert "" to None"""
    if not x:
        return None
    return x

# remove accents that we don't want to appear in the phonetic respelling
def phon_respelling(text, remove_grave):
    text = re.sub("[" + CFLEX + DUBGR + DOTABOVE + DOTBELOW + "‿]", "", text)
    # Remove grave accents from annotations but maybe not from phonetic respelling
    if remove_grave:
        text = com.remove_grave_accents(text)
    return text


# Return the actual IPA corresponding to Cyrillic text. ADJ, GEN, BRACKET
# and POS are as in [[Template:ru-IPA]]. If IS_TRANFORMED is true, the text
# has already been passed through m_ru_translit.apply_tr_fixes(); otherwise,
# this will be done.
def to_IPA(text, adj="", gem="", bracket="", pos=""):
    """Generates Russian IPA from spelling.

    Implements template `{{ru-IPA}}`_.

    .. _{{ru-IPA}}: https://en.wiktionary.org/wiki/Template:ru-IPA

    Parameters
    ----------
    text : string
        String of ru-IPA text parsed in `{{ru-IPA}}`_ from Wiktionary.

    adj : string
        String of ``|noadj=`` parameter parsed in `{{ru-IPA}}`_.

    gem : string
        String of ``|gem=`` parameter parsed in `{{ru-IPA}}`_.

    bracket : string
        String of ``|bracket=`` parameter parsed in `{{ru-IPA}}`_.

    pos : string
        String of ``|pos=`` parameter parsed in `{{ru-IPA}}`_.

    Returns
    -------
    string
        Converted Russian IPA.

    Notes
    -----
    - Modified from `Wiktioanry ru-pron Lua module`_ partially.
    - Rewritten from Author: Originally *Wyang*; rewritten by *Benwing*;
      additional contributions from *Atitarev* and a bit from others.
    - Testcases are modified from `Wiktionary ru-pron/testcases`_.

    .. _Wiktioanry ru-pron Lua module: https://en.wiktionary.org/wiki/Module:ru-pron
    .. _Wiktionary ru-pron/testcases: https://en.wiktionary.org/wiki/Module:ru-pron/testcases

    Examples
    --------
    >>> ru_text = "счастли́вый" # ru: [[счастли́вый]]
    >>> ru_IPA = ru_pron.to_IPA(ru_text)
    >>> ru_IPA
    "ɕːɪs⁽ʲ⁾ˈlʲivɨj"
    """
    origtext, transformed_text = ru_translit.apply_tr_fixes(text)
    text = transformed_text

    if not gem:
        gem = ""
    # If a multipart gemination spec, split into components.
    if "/" in gem:
        gem = gem.split("/")
        for i in range(len(gem)):
            if gem[i]:
                gem[i] = gem[i][0]
    else:
        if gem:
            gem = gem[0]
    # Verify that gem (or each part of multipart gem) is recognized
    for g in (gem if isinstance(gem, list) else [gem]):
        if g != "" and g != "y" and g != "o" and g != "n":
            return ""

    bracket = ine(bracket[0] if bracket else bracket)
    if bracket == "n":
        bracket = None

    if not pos:
        pos = "def"
    # If a multipart part of speech, split into components, and convert
    # each blank component to the default.
    if "/" in pos:
        pos = pos.split("/")
        for i in range(len(pos)):
            if not pos[i]:
                pos[i] = "def"
    # Verify that pos (or each part of multipart pos) is recognized
    for p in (pos if isinstance(pos, list) else [pos]):
        if p not in pos_properties.keys():
            return ""

    text = text.lower()

#    combined_gem = "/".join(gem) if isinstance(gem, list) else gem
#    if combined_gem:
#        track("gem")
#        track("gem/" + combined_gem)
#    if adj:
#        track("adj")
#    # don't include h here because we allow it as a legitimate alternative
#    # for ɣ. Include vowels with all of the accents that have special meaning
#    # for this module. (FIXME, maybe should also include double-grave accents,
#    # although probably not used anywhere.)
#    if re.search("[a-gi-zščžáéíóúýàèìòùỳâêîôûŷạẹịọụỵȧėȯẏ]", text):
#        track("latin-text")
#    if re.search("[сз]ч", text):
#        track("sch")
#    if re.search("[шж]ч", text):
#        track("shch")
#    if re.search(CFLEX, text):
#        track("cflex")
#    if re.search(DUBGR, text):
#        track("dubgr")

    text = re.sub("``", DUBGR, text)
    text = re.sub("`", GR, text)
    text = re.sub("@", DOTABOVE, text)
    text = re.sub("\^", CFLEX, text)
    text = re.sub(DUBGR, CFLEX, text)

    # translit doesn't always convert э to ɛ (depends on whether a consonant
    # precedes), so do it ourselves before translit
    text = re.sub("э", "ɛ", text)
    # vowel + йе should have double jj, but the translit module will translit
    # it the same as vowel + е, so do it ourselves before translit
    text = re.sub(
        "([" + com.vowel + "]" + com.opt_accent + ")й([еѐ])",
        r"\1йй\2",
        text
    )
    # transliterate and decompose Latin vowels with accents, recomposing
    # certain key combinations; don't include accent on monosyllabic ё, so
    # that we end up without an accent on such words. NOTE: Not clear we
    # need to be decomposing like this any more, although it is still
    # useful if the user supplies Latin text, which we allow (although
    # undocumented).
    text = com.decompose(ru_translit.tr_after_fixes(text))

    # handle old ě (e.g. сѣдло́), and ě̈ from сѣ̈дла
    text = re.sub("ě̈", "jo" + AC, text)
    text = re.sub("ě", "e", text)
    # handle sequences of accents (esp from ё with secondary/tertiary stress)
    text = re.sub(accents + "+(" + accents + ")", r"\1", text)

    # convert commas and en/en dashes to IPA foot boundaries
    text = re.sub("\s*[,–—]\s*", " | ", text)

    # canonicalize multiple spaces
    text = re.sub("\s+", " ", text)

    # Add primary stress to single-syllable words preceded or followed by
    # unstressed particle or preposition. Add "tertiary" stress to remaining
    # single-syllable words that aren't a particle, preposition, prefix or
    # suffix and don't already bear an accent (including force-reduction
    # accents, i.e. dot-above/dot-below); "tertiary stress" means a vowel is
    # treated as stressed for the purposes of vowel reduction but isn't
    # marked with a primary or secondary stress marker; we repurpose a
    # circumflex for this purpose. We need to preserve the distinction
    # between spaces and hyphens because (1) we only recognize certain
    # post-accentless particles following a hyphen (to distinguish e.g.
    # 'то' from '-то'); (2) we only recognize certain pre-accentless
    # particles preceding a space (to distinguish particles 'о' and 'а' from
    # spelled letters о and а, which should not be reduced); and (3) we
    # recognize hyphens for the purpose of marking unstressed prefixes and
    # suffixes.
    word = re.split("([ \-]+)", text)
    for i in range(len(word)):
        # check for single-syllable words that need a stress; they must meet
        # the following conditions:
        # 1. must not be an accentless word, which is any of the following:
        #         1a. in the "pre" class, or
        if not (word[i] in accentless["pre"].keys() or \
                # 1b. in the "prespace" class if followed by space and another word, or
                i < len(word) - 2 and word[i] in accentless["prespace"].keys() and word[i+1] == " " or \
                # 1c. in the "post" class if preceded by another word and
                #     not followed by a hyphen (this is because words like
                #     ка and же are also used for spelling initialisms), or
                i > 1 and word[i] in accentless["post"].keys() and (i+1 >= len(word) or word[i+1] != "-") or \
                # 1d. in the "posthyphen" class preceded by a hyphen and another word
                #     (and not followed by a hyphen, see 1c);
                i > 1 and word[i] in accentless["posthyphen"].keys() and word[i-1] == "-" and (i+1 >= len(word) or word[i+1] != "-")) and ( \
        # 2. must be one syllable;
            len(re.sub("[^" + vow + "]", "", word[i])) == 1) and ( \
        # 3. must not have any accents (including dot-above, forcing reduction);
            not re.search(accents, word[i])) and ( \
        # 4. must not be a prefix or suffix, identified by a preceding or trailing hyphen, i.e. one of the following:
        #         4a. utterance-initial preceded by a hyphen, or
            not (i == 2 and word[1] == "-" and word[0] == "" or \
                # 4b. non-utterance-initial preceded by a hyphen, or
                i >= 2 and word[i-1] == " -" or \
                # 4c. utterance-final followed by a hyphen, or
                i == len(word) - 3 and word[i+1] == "-" and word[i+2] == "" or \
                # 4d. non-utterance-final followed by a hyphen;
                i <= len(word) - 3 and word[i+1] == "- ")):

        # OK, we have a stressable single-syllable word; either add primary
        # or tertiary stress:
        # 1. add primary stress if preceded or followed by an accentless word,
            if (i > 1 and word[i-2] in accentless["pre"].keys() or \
                i > 1 and word[i-1] == " " and word[i-2] in accentless["prespace"].keys() or \
                i < len(word) - 2 and word[i+2] in accentless["post"].keys() and word[i+3] != "-" or \
                i < len(word) - 2 and word[i+1] == "-" and word[i+2] in accentless["posthyphen"].keys() and word[i+3] != "-"):
                word[i] = re.sub(vowels_c, r"\1" + AC, word[i])
        # 2. else add tertiary stress
            else:
                word[i] = re.sub(vowels_c, r"\1" + CFLEX, word[i])

    # count number of words and make sure we have correct number of
    # gemination and part-of-speech specs if a multipart spec is given
    num_real_words = 0
    for i in range(len(word)):
        if i % 2 == 0 and word[i] != "":
            num_real_words += 1
    if isinstance(gem, list) and len(gem) != num_real_words:
        return ""
    if isinstance(pos, list) and len(pos) != num_real_words:
        return ""

    # make unaccented prepositions and particles liaise with the following or
    # preceding word; in the process, fix up number of elements in gem/pos
    # tables so there's a single element for the combined word
    real_word_index = 0
    for i in range(len(word)):
        if i % 2 == 0 and word[i] != "":
            real_word_index += 1
        if i < len(word) - 2 and (word[i] in accentless["pre"].keys() or word[i] in accentless["prespace"].keys() and word[i+1] == " "):
            word[i+1] = "‿"
            if isinstance(gem, list) and real_word_index <= len(gem):
                del gem[real_word_index-1]
            if isinstance(pos, list) and real_word_index <= len(pos):
                del pos[real_word_index-1]
        elif i > 1 and (word[i] in accentless["post"].keys() and (i+1 >= len(word) or word[i+1] != "-") or \
                word[i] in accentless["posthyphen"].keys() and word[i-1] == "-" and (i+1 >= len(word) or word[i+1] != "-")):
            word[i-1] = "‿"
            # for unaccented words that liaise with the preceding word,
            # remove the gemination spec corresponding to the unaccented word
            # because the gemination in question is almost certainly in the
            # preceding word, but remove the POS spec corresponding to the
            # preceding word because it's the final -е of the unaccented word
            # that the POS will refer to
            if isinstance(gem, list) and real_word_index <= len(gem):
                del gem[real_word_index-1]
            if isinstance(pos, list) and 1 < real_word_index < len(pos):
                del pos[real_word_index-2]

    # rejoin words, convert hyphens to spaces and eliminate stray spaces
    # resulting from this
    text = "".join(word)
    text = re.sub("[\-\s]+", " ", text)
    text = re.sub("^ ", "", text)
    text = re.sub(" $", "", text)

    # add a ⁀ at the beginning and end of every word and at close juncture
    # boundaries; we will remove this later but it makes it easier to do
    # word-beginning and word-end re.subs
    text = re.sub(" ", "⁀ ⁀", text)
    text = re.sub("([!?])", r"⁀\1⁀", text)
    text = "⁀" + text + "⁀"
    text = re.sub("‿", "⁀‿⁀", text)

    # save original word spelling before respellings, (de)voicing changes,
    # geminate changes, etc. for implementation of geminate_pref
    orig_word = text.split(" ")

    # insert or remove /j/ before [aou] so that palatal versions of these
    # vowels are always preceded by /j/ and non-palatal versions never are
    # (do this before the change below adding tertiary stress to final
    # palatal о):
    # (1) Non-palatal [ou] after always-hard шж (e.g. in брошю́ра, жю́ри)
    #     despite the spelling (FIXME, should this also affect [a]?)
    text = re.sub("([šž])j([ou])", r"\2\3", text)
    # (2) Palatal [aou] after always-soft щчӂ and voiced variant ǰ (NOTE:
    #     this happens before the change šč -> ɕː in phonetic_subs)
    text = re.sub("([čǰӂ])([aou])", r"\1j\2", text)
    # (3) ьо is pronounced as ьйо, i.e. like (possibly unstressed) ьё, e.g.
    #     in Асунсьо́н
    text = re.sub("ʹo", "ʹjo", text)

    # add tertiary stress to some final -о (this needs to be done before
    # eliminating dot-above, after adding ⁀, after adding /j/ before palatal о):
    # (1) after vowels, e.g. То́кио
    text = re.sub("(" + vowels + accents + "?o)⁀", r"\1" + CFLEX + "⁀", text)
    # (2) when palatal, e.g. ра́нчо, га́учо, ма́чо, Ога́йо
    text = re.sub("jo⁀", "jo" + CFLEX + "⁀", text)

    # eliminate dot-above, which has served its purpose of preventing any
    # sort of stress (needs to be done after adding tertiary stress to
    # final -о)
    text = re.sub(DOTABOVE, "", text)
    # eliminate dot-below (needs to be done after changes above that insert
    # j before [aou] after always-soft щчӂ)
    text = re.sub("ja" + DOTBELOW, "jạ", text)
    if re.search(DOTBELOW, text):
        return ""

    if adj:
        text = re.sub("(.[aoe]́?)go(" + AC + "?)⁀", r"\1vo\2⁀", text)
        text = re.sub("(.[aoe]́?)go(" + AC + "?)sja⁀", r"\1vo\2sja⁀", text)

    def fetch_pos_property(i, ending):
        thispos = pos[i] if isinstance(pos, list) else pos
        chart = pos_properties[thispos]
        while isinstance(chart, str): # handle aliases
            chart = pos_properties[chart]
        assert(isinstance(chart, dict))
        if ending in chart.keys():
            sub = chart[ending]
        else:
            sub = pos_properties["def"][ending]
        assert(sub)
        return sub

    # Pos-specific handling of final -ться: palatalized if pos=imp, else not
    # (infinitives). If we have multiple parts of speech, we need to be
    # trickier, splitting by word.
    def final_tsja_processing(pron, i):
        tsjapal = fetch_pos_property(i, "tsjapal")
        if tsjapal == "n":
            # FIXME!!! Should these also pay attention to grave accents?
            pron = re.sub("́tʹ?sja⁀", "́cca⁀", pron)
            pron = re.sub("([^́])tʹ?sja⁀", r"\1ca⁀", pron)
        return pron
    if isinstance(pos, list):
        # split by word and process each word
        word = text.split(" ")
        for i in range(len(word)):
            word[i] = final_tsja_processing(word[i], i)
        text = " ".join(word)
    else:
        text = final_tsja_processing(text, 0)

    # phonetic substitutions of various sorts
    for phonsub in phonetic_subs:
        text = re.sub(phonsub[0], phonsub[1], text)

    #voicing, devoicing
    #NOTE: v before an obstruent assimilates in voicing and triggers voicing
    #assimilation of a preceding consonant; neither happens before a sonorant
    #1. absolutely final devoicing
    text = re.sub(
        "([bdgvɣzžĝĵǰӂ])(ʹ?⁀)$",
        lambda x: devoicing[x.group(1)] + x.group(2),
        text
    )
    #2. word-final devoicing before another word
    text = re.sub(
        "([bdgvɣzžĝĵǰӂ])(ʹ?⁀ ⁀[^bdgɣzžĝĵǰӂ])",
        lambda x: devoicing[x.group(1)] + x.group(2),
        text
    )
    #3. voicing/devoicing assimilation; repeat to handle recursive assimilation
    while True:
        new_text = re.sub(
            "([bdgvɣzžĝĵǰӂ])([ ‿⁀ʹːˑ()/]*[ptkfxsščɕcĉ])",
            lambda x: devoicing[x.group(1)] + x.group(2),
            text
        )
        new_text = re.sub(
            "([ptkfxsščɕcĉ])([ ‿⁀ʹːˑ()/]*v?[ ‿⁀ʹːˑ()/]*[bdgɣzžĝĵǰӂ])",
            lambda x: voicing[x.group(1)] + x.group(2),
            new_text
        )
        if new_text == text:
            break
        text = new_text

    #re-notate orthographic geminate consonants
    text = re.sub("([^" + vow + ".\-_])" + r"\1", r"\1ː", text)
    text = re.sub("([^" + vow + ".\-_])" + r"\(\1\)", r"\1(ː)", text)

    #rewrite iotated vowels
    text = re.sub(
        "(j[\(ːˑ\)]*)([aeou])",
        lambda x: x.group(1) + iotating[x.group(2)],
        text
    )
    # eliminate j after consonant and before iotated vowel (including
    # semi-reduced ạ)
    text = re.sub("([^" + vow + acc + "ʹʺ‿⁀ ]/?)j([äạëöü])", r"\1\2", text)

    #split by word and process each word
    word = text.split(" ")

    for i in range(len(word)):
        pron = word[i]

        # Check for gemination at prefix boundaries; if so, convert the
        # regular gemination symbol ː to a special symbol ˑ that indicates
        # we always preserve the gemination unless gem=n. We look for
        # certain sequences at the beginning of a word, but make sure that
        # the original spelling is appropriate as well (see comment above
        # for geminate_pref).
        if re.search("ː", pron):
            orig_pron = orig_word[i]
            deac = re.sub(accents, "", pron)
            orig_deac = re.sub(accents, "", orig_pron)
            for newspell, oldspell in geminate_pref:
                # FIXME! The re.sub below will be incorrect if there is
                # gemination in a joined preposition or particle
                if re.search("⁀" + oldspell, orig_deac) and re.search("⁀" + newspell, deac) or \
                    re.search("⁀ne" + oldspell, orig_deac) and re.search("⁀ne" + newspell, deac):
                    pron = re.sub("(⁀[^‿⁀ː]*)ː", r"\1ˑ", pron)

        #degemination, optional gemination
        thisgem = gem[i] if isinstance(gem, list) else gem
        if thisgem == "y":
            # leave geminates alone, convert ˑ to regular gemination; ˑ is a
            # special gemination symbol used at prefix boundaries that we
            # remove only when gem=n, else we convert it to regular gemination
            pron = re.sub("ˑ", "ː", pron)
        elif thisgem == "o":
            # make geminates optional, except for ɕӂ, also ignore left paren
            # in (ː) sequence
            pron = re.sub("([^ɕӂ\(\)])[ːˑ]", r"\1(ː)", pron)
        elif thisgem == "n":
            # remove gemination, except for ɕӂ
            pron = re.sub("([^ɕӂ\(\)])[ːˑ]", r"\1", pron)
        else:
            # degeminate l's
            pron = re.sub("(l)ː", r"\1", pron)
            # preserve gemination between vowels immediately after the stress,
            # special gemination symbol ˑ also remains, ɕӂ remain geminated,
            # žn remain geminated between vowels even not immediately after
            # the stress, n becomes optionally geminated when after but not
            # immediately after the stress, ssk and zsk remain geminated
            # immediately after the stress, else degeminate; we signal that
            # gemination should remain by converting to special symbol ˑ,
            # then removing remaining ː not after ɕӂ and left paren; do
            # various subs repeatedly in case of multiple geminations in a word
            # 1. immediately after the stress
            pron = sub_repeatedly("(" + vowels + stress_accents + "[^ɕӂ\(\)])ː(" + vowels + ")", r"\1ˑ\2", pron)
            # 2. remaining geminate n after the stress between vowels
            pron = sub_repeatedly("(" + stress_accents + ".*?" + vowels + accents + "?n)ː(" + vowels + ")", r"\1(ː)\2", pron)
            # 3. remaining ž and n between vowels
            pron = sub_repeatedly("(" + vowels + accents + "?[žn])ː(" + vowels + ")", r"\1ˑ\2", pron)
            # 4. ssk (and zsk, already normalized) immediately after the stress
            pron = re.sub("(" + vowels + stress_accents + "[^" + vow + "]*s)ː(k)", r"\1ˑ\2", pron)
            # 5. eliminate remaining gemination, except for ɕː and ӂː
            pron = re.sub("([^ɕӂ\(\)])ː", r"\1", pron)
            # 6. convert special gemination symbol ˑ to regular gemination
            pron = re.sub("ˑ", "ː", pron)

        # handle soft and hard signs, assimilative palatalization
        # 1. insert j before i when required
        pron = re.sub("ʹi", "ʹji", pron)
        # 2. insert glottal stop after hard sign if required
        pron = re.sub("ʺ([aɛiouy])", r"ʔ\1", pron)
        # 3. (ь) indicating optional palatalization
        pron = re.sub("\(ʹ\)", "⁽ʲ⁾", pron)
        # 4. assimilative palatalization of consonants when followed by
        #    front vowels or soft sign
        pron = re.sub("([mnpbtdkgfvszxɣrl])([ː()]*[eiäạëöüʹ])", r"\1ʲ\2", pron)
        pron = re.sub("([cĵ])([ː()]*[äạöüʹ])", r"\1ʲ\2", pron)
        # 5. remove hard and soft signs
        pron = re.sub("[ʹʺ]", "", pron)

        # reduction of unstressed word-final -я, -е; but special-case
        # unstressed не, же. Final -я always becomes [ə]; final -е may
        # become [ə], [e], [ɪ] or [ɨ] depending on the part of speech and
        # the preceding consonants/vowels.
        pron = re.sub("[äạ]⁀", "ə⁀", pron)
        pron = re.sub("⁀nʲe⁀", "⁀nʲi⁀", pron)
        pron = re.sub("⁀že⁀", "⁀žy⁀", pron)
        # function to fetch the appropriate value for ending and part of
        # speech, handling aliases and defaults and converting 'e' to 'ê'
        # so that the unstressed [e] sound is preserved
        def fetch_e_sub(ending):
            sub = fetch_pos_property(i, ending)
            if sub == "e":
                # add TEMPCFLEX (which will be converted to CFLEX) to preserve
                # the unstressed [e] sound, which will otherwise be converted
                # to [ɪ]; we do this instead of adding CFLEX directly because
                # we later convert some instances of the resulting "e" to
                # "i", and we don"t want to do this when the user explicitly
                # wrote a Cyrillic е with a circumflex on it. [NOTE that
                # formerly applied when we added CFLEX directly: DO NOT
                # use ê here directly because it"s a single composed char,
                # when we need the e and accent to be separate.]
                return "e" + TEMPCFLEX
            else:
                return sub
        def repl1(match):
            v, ac = match.group(1), match.group(2)
            if v == "o":
                ty = "oe"
            else:
                ty = "ve"
            return v + ac + fetch_e_sub(ty) + "⁀"
        def repl2(match):
            ch, mod = match.group(1), match.group(2)
            if ch == "j":
                ty = "je"
            elif re.search("[cĵšžĉĝ]", ch):
                ty = "hardsib"
            elif re.search("[čǰɕӂ]", ch):
                ty = "softsib"
            else:
                ty = "softpaired"
            return ch + mod + fetch_e_sub(ty) + "⁀"
        if new_final_e_code:
            # handle substitutions in two parts, one for vowel+j+e sequences
            # and the other for cons+e sequences
            pron = re.sub(vowels_c + "(" + accents + "?j)ë⁀", repl1, pron)
            # consonant may palatalized, geminated or optional-geminated
            pron = re.sub("(.)(ʲ?[ː()]*)[eë]⁀", repl2, pron)
            if final_e_non_pausal:
                # final [e] should become [ɪ] when not followed by pause or
                # end of utterance (in other words, followed by space plus
                # anything but a pause symbol, or followed by tie bar).
                pron = re.sub("e" + TEMPCFLEX + "⁀‿", "i⁀‿", pron)
                if i < len(word) - 1 and word[i+1] != "⁀|⁀":
                    pron = re.sub("e" + TEMPCFLEX + "⁀$", "i⁀", pron)
            # now convert TEMPCFLEX to CFLEX; we use TEMPCFLEX so the previous
            # two regexps won"t affect cases where the user explicitly wrote
            # a circumflex
            pron = re.sub(TEMPCFLEX, CFLEX, pron)
        else:
            # Do the old way, which mostly converts final -е to schwa, but
            # has highly broken retraction code for vowel + [шжц] + е (but
            # not with accent on vowel!) before it that causes final -е in
            # this circumstance to become [ɨ], and a special hack for кое-.
            pron = re.sub(vowels_c + "([cĵšžĉĝ][ː()]*)[eë]", r"\1\2ɛ", pron)
            pron = re.sub("⁀ko(" + stress_accents + ")jë⁀", r"⁀ko\1ji⁀", pron)
            pron = re.sub("[eë]⁀", "ə⁀", pron)

        # retraction of е and и after цшж
        pron = re.sub(
            "([cĵšžĉĝ][ː()]*)([ei])",
            lambda x: x.group(1) + retracting[x.group(2)],
            pron
        )

        #syllabify, inserting @ at syllable boundaries
        #1. insert @ after each vowel
        pron = re.sub("(" + vowels + accents + "?)", r"\1@", pron)
        #2. eliminate word-final @
        pron = re.sub("@+⁀$", "⁀", pron)
        #3. move @ forward directly before any ‿⁀, as long as at least
        #   one consonant follows that; we will move it across ‿⁀ later
        pron = re.sub(
            "@([^@" + vow + acc + "]*)([‿⁀]+[^‿⁀@" + vow + acc + "])",
            r"\1@\2",
            pron
        )
        #4. in a consonant cluster, move @ forward so it"s before the
        #   last consonant
        pron = re.sub(
            "@([^‿⁀@" + vow + acc + "]*)([^‿⁀@" + vow + acc + "ːˑ()ʲ]ʲ?[ːˑ()]*‿?[" + vow + acc + "])",
            r"\1@\2",
            pron
        )
        #5. move @ backward if in the middle of a "permanent onset" cluster,
        #   e.g. sk, str, that comes before a vowel, putting the @ before
        #   the permanent onset cluster
        def repl3(match):
            a, aund, b, bund, c, d = \
                match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), match.group(6)
            if a+b+c in perm_syl_onset.keys() or c == "j" and re.search("[čǰɕӂʲ]", b):
                return "@" + a + aund + b + bund + c + d
            elif b+c in perm_syl_onset.keys():
                return a + aund + "@" + b + bund + c + d
            return match.group()
        pron = re.sub(
            "([^‿⁀@_" + vow + acc + "]?)(_*)([^‿⁀@_" + vow + acc + "])(_*)@([^‿⁀@" + vow + acc + "ːˑ()ʲ])(ʲ?[ːˑ()]*[‿⁀]*[" + vow + acc + "])",
            repl3,
            pron
        )
        def repl4(match):
            x = match.group()
            if "/" in x:
                x = re.sub("@", "", x)
                x = re.sub("/", "@", x)
            return x
        #6. if / is present (explicit syllable boundary), remove any @
        #   (automatic boundary) and convert / to @
        if "/" in pron:
            pron = re.sub("[^" + vow + acc + "]+", repl4, pron)
        #7. remove @ followed by a final consonant cluster
        pron = re.sub("@([^‿⁀@" + vow + "]+⁀)$", r"\1", pron)
        #8. remove @ preceded by an initial consonant cluster (should only
        #   happen when / is inserted by user or in цз, чж sequences)
        pron = re.sub("^(⁀[^‿⁀@" + vow + "]+)@", r"\1", pron)
        #9. make sure @ isn"t directly before linking ‿⁀
        pron = re.sub("@([‿⁀]+)", r"\1@", pron)

        # handle word-initial unstressed o and a; note, vowels always
        # followed by at least one char because of word-final ⁀
        # do after syllabification because syllabification doesn't know
        # about ɐ as a vowel
        pron = re.sub("^⁀[ao]([^" + acc + "])", r"⁀ɐ\1", pron)

        #split by syllable
        syllable = pron.split("@")

        #create set of 1-based syllable indexes of stressed syllables
        #(acute, grave, circumflex)
        stress = {}
        for j in range(len(syllable)):
            if re.search(stress_accents, syllable[j]):
                stress[j] = "real"
            elif re.search(CFLEX, syllable[j]):
                stress[j] = "cflex"
            else:
                stress[j] = ""

        # iterate syllable by syllable to handle stress marks, vowel allophony
        syl_conv = []
        for j in range(len(syllable)):
            syl = syllable[j]

            alnum = None
            #vowel allophony
            if stress[j]:
                # convert acute/grave/circumflex accent to appropriate
                # IPA marker of primary/secondary/unmarked stress
                alnum = 0
                syl = re.sub("(.*)́", r"ˈ\1", syl)
                syl = re.sub("(.*)̀", r"ˌ\1", syl)
                syl = re.sub(CFLEX, "", syl)
            elif j+1 < len(syllable) and stress[j+1] == "real":
                # special-casing written а immediately before the stress,
                # but only for primary/secondary stress, not circumflex
                alnum = 1
            else:
                alnum = 2
            syl = re.sub(
                vowels_c,
                lambda x: allophones[x.group(1)][alnum] if x.group(1) != "" else x.group(),
                syl
            )
            syl_conv.append(syl)

        pron = "".join(syl_conv)

        # Optional (j) before ɪ, which is always unstressed
        pron = re.sub("⁀jɪ", "⁀(j)ɪ", pron)
        pron = re.sub("([" + ipa_vow + "])jɪ", r"\1(j)ɪ", pron)

        def repl5(match):
            a, b, c = match.group(1), match.group(2), match.group(3)
            if not a:
                return a + b + "ʲ" + c
            else:
                return a + b + "⁽ʲ⁾" + c
        #consonant assimilative palatalization of tn/dn/sn/zn, depending on
        #whether [rl] precedes
        pron = re.sub("([rl]?)([ː()ˈˌ]*[dtsz])([ː()ˈˌ]*nʲ)", repl5, pron)

        #consonant assimilative palatalization of st/zd, depending on
        #whether [rl] precedes
        pron = re.sub("([rl]?)([ˈˌ]?[sz])([ː()ˈˌ]*[td]ʲ)", repl5, pron)

        def repl6(match):
            a, b, c = match.group(1), match.group(2), match.group(3)
            if a+c in cons_assim_palatal["compulsory"].keys():
                return a + "ʲ" + b + c
            elif a+c in cons_assim_palatal["optional"].keys():
                return a + "⁽ʲ⁾" + b + c
            else:
                return a + b + c
        #general consonant assimilative palatalization
        pron = sub_repeatedly(
            "([szntdpbmfcĵx])([ː()ˈˌ]*)([szntdpbmfcĵlk]ʲ)",
            repl6,
            pron
        )

        # further assimilation before alveolopalatals
        pron = re.sub("n([ː()ˈˌ]*)([čǰɕӂ])", r"nʲ\1\2", pron)

        # optional palatal assimilation of вп, вб only word-initially
        pron = re.sub("⁀([ː()ˈˌ]*[fv])([ː()ˈˌ]*[pb]ʲ)", r"⁀\1⁽ʲ⁾\2", pron)

        # optional palatal assimilation of бв but not in обв-
        pron = re.sub("b([ː()ˈˌ]*vʲ)", r"b⁽ʲ⁾\1", pron)
        if re.search("⁀o" + accents + "?bv", word[i]):
            # ə in case of a word with a preceding preposition
            pron = re.sub("⁀([ː()ˈˌ]*[ɐəo][ː()ˈˌ]*)b⁽ʲ⁾([ː()ˈˌ]*vʲ)", r"⁀\1b\2", pron)

        # Word-final -лся (normally in past verb forms) should have optional
        # palatalization. Need to rewrite as -лсьа to defeat this.
        # FIXME: Should we move this to phonetic_subs?
        if re.search("ls[äạ]⁀", word[i]):
            pron = re.sub("lsʲə⁀", "ls⁽ʲ⁾ə⁀", pron)

        word[i] = pron

    text = " ".join(word)
    if bracket:
        text = "[" + text + "]"

    # Front a and u between soft consonants. If between a soft and
    # optionally soft consonant (should only occur in that order, shouldn't
    # ever have a or u preceded by optionally soft consonant),
    # split the result into two. We only split into two even if there
    # happen to be multiple optionally fronted a's and u's to avoid
    # excessive numbers of possibilities (and it simplifies the code).
    # 1. First, temporarily add soft symbol to inherently soft consonants.
    text = re.sub("([čǰɕӂj])", r"\1ʲ", text)
    # 2. Handle case of [au] between two soft consonants
    text = sub_repeatedly(
        "(ʲ[ː()]*)([auʊ])([ˈˌ]?.ʲ)",
        lambda x: x.group(1) + fronting[x.group(2)] + x.group(3),
        text
    )
    # 3. Handle [au] between soft consonant and optional j, which is still fronted
    text = sub_repeatedly(
        "(ʲ[ː()]*)([auʊ])([ˈˌ]?\(jʲ\))",
        lambda x: x.group(1) + fronting[x.group(2)] + x.group(3),
        text
    )
    # 4. Handle case of [au] between soft and optionally soft consonant
    if re.search("ʲ[ː()]*[auʊ][ˈˌ]?.⁽ʲ⁾", text):
        opt_hard = re.sub("(ʲ[ː()]*)([auʊ])([ˈˌ]?.)⁽ʲ⁾", r"\1\2\3", text)
        opt_soft = re.sub(
            "(ʲ[ː()]*)([auʊ])([ˈˌ]?.)⁽ʲ⁾",
            lambda x: x.group(1) + fronting[x.group(2)] + x.group(3) + "ʲ",
            text
        )
        text = opt_hard + ", " + opt_soft
    # 5. Undo addition of soft symbol to inherently soft consonants.
    text = re.sub("([čǰɕӂj])ʲ", r"\1", text)

    # convert special symbols to IPA
    text = re.sub("[cĵ]ʲ", lambda x: translit_conv_j[x.group()], text)
    text = re.sub(
        "[cčgĉĝĵǰšžɕӂ]",
        lambda x: translit_conv[x.group()] if x.group() in translit_conv.keys() else x.group(),
        text
    )

    # Assimilation involving hiatus of ɐ and ə
    text = re.sub("ə([‿⁀]*)[ɐə]", r"ɐ\1ɐ", text)

    # eliminate ⁀ symbol at word boundaries
    # eliminate _ symbol that prevents assimilations
    text = re.sub("[⁀_]", "", text)

    return text
