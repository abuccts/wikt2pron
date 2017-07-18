# pylint: disable=anomalous-backslash-in-string
# pylint: disable=no-init, too-few-public-methods
"""Unittest for ru_pron.py
Testcases modified from https://en.wiktionary.org/wiki/Module:ru-pron/testcases.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from six import with_metaclass

from .. import ru_pron


# Testcases for Russian text to IPA conversion
TESTCASES = [
    (("а́втор-исполни́тель",), "ˈaftər ɪspɐlˈnʲitʲɪlʲ"), #FIXME
    (("ни с того́ ни с сего́",), "nʲɪ‿s‿tɐˈvo nʲɪ‿s‿sʲɪˈvo"), #FIXME
    (("рас(с)тёгивать",), "rɐsʲ(ː)ˈtʲɵɡʲɪvətʲ"),
    # handling of стл # in стлив but not elsewhere
    (("счастли́вый",), "ɕːɪs⁽ʲ⁾ˈlʲivɨj"),
    (("костля́вый",), "kɐstˈlʲavɨj"),
    (("истле́ть",), "ɪstˈlʲetʲ"),
    # optional palatalization of final -ся (currently only after л)
    (("роди́лся",), "rɐˈdʲils⁽ʲ⁾ə"),
    (("Зо́ся",), "ˈzosʲə"),
    # palatalization before consonants in imperative forms
    (("вы́сыпьте",), "ˈvɨsɨp⁽ʲ⁾tʲe"),
    (("рассы́пься",), "rɐˈsːɨp⁽ʲ⁾sʲə"),
    (("знако́мьтесь",), "znɐˈkom⁽ʲ⁾tʲɪsʲ"),
    (("ме́тьте",), "ˈmʲetʲːe"),
    # also should geminate even not directly after the stress
    (("вы́гладьте",), "ˈvɨɡlətʲːe"),
    (("отме́ться", None, "imp"), "ɐtˈmʲet͡sʲsʲə"), #FIXME
    (("бро́сься",), "ˈbrosʲːə"),
    (("оби́дься", None, "imp"), "ɐˈbʲit͡sʲsʲə"), #FIXME
    # unstressed а before final -е
    (("элева́торе", None, "pre"), "ɨlʲɪˈvatərʲe"),
    # fronting after two a's or u's in successive syllables
    (("включа́ть",), "fklʲʉˈt͡ɕætʲ"),
    (("умоля́ющий",), "ʊmɐˈlʲæjʉɕːɪj"),
    # palatal assimilation in дм
    (("седми́ца",), "sʲɪdˈmʲit͡sə"), #FIXME
    # tie bar in дн, тн
    (("сего́дня",), "sʲɪˈvodʲnʲə"), #FIXME
    # optional palatalization assimilation in тл, syllable division before cluster (Avanesov has a tie bar here)
    (("светле́ть",), "svʲɪtˈlʲetʲ"), #FIXME
    # optional palatalization assimilation in см
    (("сейсми́чный",), "sʲɪjsˈmʲit͡ɕnɨj"), #FIXME
    # optional palatalization assimilation in св
    (("сверло́",), "svʲɪrˈlo"), #FIXME
    # optional palatalization assimilation in сб
    (("сбива́ть",), "zbʲɪˈvatʲ"), #FIXME
    # optional palatalization assimilation in ств, тв
    (("противобо́рстве", None, "pre"), "prətʲɪvɐˈborstvʲe"), #FIXME
    (("рукоприкла́дстве", None, "pre"), "rʊkəprʲɪˈklat͡stvʲe"), #FIXME
    (("самоутвержде́ние", None, "n"), "səməʊtvʲɪrʐˈdʲenʲɪje"), #FIXME
    # optional palatalization assimilation in сдв, дв (?),
    (("сдвиг",), "zdvʲik"), #FIXME
    # ч should be hard in чш
    (("лу́чший",), "ˈlut͡ʂʂɨj"),
    # as per talk re Тогане
    (("Зимба́бвэ",), "zʲɪmˈbabvɨ"), #FIXME
    (("То́го",), "ˈtoɡə"),
    (("того́",), "tɐˈvo"),
    # gemination should be optional
    (("нра̀вственно-эти́ческий",), "ˌnrafstvʲɪn(ː)ə ɨˈtʲit͡ɕɪskʲɪj"),
    # -ка- should be stressed
    (("эн-ка-вэ-дэ́",), "ɛn ka vɛ ˈdɛ"),
    # comma shouldn't interfere with destressing же
    (("то же, что",), "ˈto‿ʐɨ | ʂto"),
    # ё + э + no other vowels used to cause problems
    (("гёрлфрэнд",), "ˈɡʲɵrlfrɨnt"),
    # [j] not optional in such positions
    (("в Япо́нии", None, "n"), "v‿(j)ɪˈponʲɪɪ"), #FIXME
    # final -е
    # compare to моро́женая, a word in -нои or -наи (or обы́чаи),
    (("моро́женое", None, "n"), "mɐˈroʐɨnəjə"),
    # compare to собра́ния, о собра́нии
    (("собра́ние", None, "n"), "sɐˈbranʲɪje"),
    # compare to всле́дствия, о всле́дствии
    (("всле́дствие", None, "n"), "ˈfs⁽ʲ⁾lʲet͡stvʲɪje"),
    # compare to сча́стья, о го́стье, го́стьи
    (("сча́стье", None, "n"), "ˈɕːæsʲtʲje"),
    # compare to со́лнца, брето́нца, о брето́нце, брето́нцы
    (("со́лнце", None, "n"), "ˈsont͡sə"),
    # compare to се́рдца, две́рца, о две́рце, две́рцы
    (("се́рдце", None, "n"), "ˈsʲert͡sə"),
    # compare to ло́жа, до́жи
    (("ло́же", None, "n"), "ˈloʐə"),
    # compare to по́ля, до́ли
    (("по́ле", None, "n"), "ˈpolʲe"),
    # compare to жили́ща, пи́ща, о пи́ще, пи́щи
    (("жили́ще", None, "n"), "ʐɨˈlʲiɕːe"),
    # compare to ве́ча, встре́чи
    (("ве́че", None, "n"), "ˈvʲet͡ɕe"),
    # compare to Гео́ргия, Гео́ргии
    (("а́вторские", None, "a"), "ˈaftərskʲɪje"), #FIXME
    # compare to Алба́ния, Алба́нии, си́нее
    (("да́нные", None, "a"), "ˈdanːɨje"), #FIXME
    # compare to Абисси́ния, Абисси́нии
    (("си́нее", None, "a"), "ˈsʲinʲɪje"),
    # compare to ли́сья, ли́сьи
    (("ли́сье", None, "a"), "ˈlʲisʲjə"),
    # compare to рази́ня, рази́не, си́ни
    (("си́не", None, "a"), "ˈsʲinʲe"),
    # compare to Гвине́я, о Гвине́е, Гвине́и
    (("дурне́е", None, "c"), "dʊrˈnʲeje"),
    # compare to По́льша, о По́льше, По́льши
    (("бо́льше", None, "c"), "ˈbolʲʂɨ"),
    # compare to до́жа, о до́же, до́жи
    (("доро́же", None, "c"), "dɐˈroʐɨ"),
    # compare to сме́рча, о сме́рче, сме́рчи
    (("ле́хче", None, "c"), "ˈlʲext͡ɕe"),
    # compare to гу́ща, о гу́ще, гу́щи
    (("гу́ще", None, "c"), "ˈɡuɕːe"),
    # compare to неде́ля, неде́ле, неде́ли
    (("досе́ле", None, "adv"), "dɐˈsʲelʲe"),
    # compare to ста́жа, о ста́же, ста́жи
    (("та́кже", None, "adv"), "ˈtaɡʐɨ"),
    # compare to да́ча, о да́че, да́чи
    (("ина́че", None, "adv"), "ɪˈnat͡ɕe"),
    # compare to ве́ща, ве́ще, ве́щи (from ве́щий)
    (("злове́ще", None, "adv"), "zlɐˈvʲeɕːe"),
    # compare to пла́ца, пла́це, пла́цы
    (("вкра́тце", None, "adv"), "ˈfkrat͡sːɨ"),
    # compare to тя́тя, о тя́те, тя́ти
    (("не пла́чьте", None, "v"), "nʲɪ‿ˈplat͡ɕtʲe"),
    # compare to тётя, о тёте, тёти
    (("дава́йте", None, "v"), "dɐˈvajtʲe"),
    # compare to сбо́я, сбо́е, сбо́и
    (("дво́е", None, "mid"), "ˈdvoje"),
    # compare to сбо́я, сбо́е, сбо́и
    (("дво́е", None, "low"), "ˈdvojə"),
    # compare to ши́ре (from широко́),, зве́ря, о зве́ре, зве́ри
    (("четы́ре", None, "mid"), "t͡ɕɪˈtɨrʲe"),
    # compare to тётя, о тёте, тёти, пло́ти
    (("о го́де", None, "pre"), "ɐ‿ˈɡodʲe"),
    # compare to вы́игрыша, вы́игрыши
    (("о вы́игрыше", None, "pre"), "ɐ‿ˈvɨɪɡrɨʂɨ"),
    # compare to такела́жа, колла́жа, о колла́же, колла́жи
    (("о такела́же", None, "pre"), "ɐ‿təkʲɪˈlaʐɨ"),
    # compare to да́ча, о да́че, да́чи
    (("о пла́че", None, "pre"), "ɐ‿ˈplat͡ɕe"),
    # compare to австрали́йца, австрали́йци
    (("об австрали́йце", None, "pre"), "ɐb‿əfstrɐˈlʲijt͡sɨ"),
    # compare to сбо́я, о сбо́е, сбо́и
    (("о бо́е", None, "pre"), "ɐ‿ˈboje"),
    # compare to ине́я, ине́и
    (("об и́нее", None, "pre"), "ɐˈb‿ɨnʲɪje"),
    # compare to пля́жа, пля́же, пля́жи
    (("кня́же", None, "voc"), "ˈknʲaʐɨ"),
    # compare to ха́рча, о ха́рче, сме́рча, о сме́рче, сме́рчи
    (("ста́рче", None, "voc"), "ˈstart͡ɕe"),
    # compare to ды́ня, o ды́не, ды́ни
    (("сы́не", None, "voc"), "ˈsɨnʲe"),
    # compare to сбо́я, о сбо́е, сбо́и
    (("ко̀е-кто́", None, "pro"), "ˌko(j)ɪ ˈkto"),
    # compare to ки́я, о ки́и
    (("каки́е-нибудь лека́рства", None, "pro"), "kɐˈkʲi(j)ɪ‿nʲɪbʊtʲ lʲɪˈkarstvə"), #FIXME
    (("си́ние воротнички́",), "ˈsʲinʲɪje vərətʲnʲɪt͡ɕˈkʲi"), #FIXME
    # case involving multiple parts of speech
    (("Адриати́ческое мо́ре", None, "a/n"), "ɐdrʲɪɐˈtʲit͡ɕɪskəjə ˈmorʲe"),
    # end of final -е

    (("компа̀кт-ди́ск",), "kɐmˌpaɡd ˈdʲisk"),
    (("воѐнно-морско́й",), "vɐˌjenːə mɐrˈskoj"),
    (("ра́нчо",), "ˈranʲt͡ɕɵ"),
    (("а не то",), "ɐ‿nʲɪ‿ˈto"),
    (("а как же",), "ɐ‿ˈkaɡ‿ʐɨ"),
    (("а̂ капэ́лла", None, "opt"), "a kɐˈpɛl(ː)ə"),
    (("о-а-э́",), "o a ˈɛ"),
    (("лёгкий",), "ˈlʲɵxʲkʲɪj"),
    (("мя́гкий",), "ˈmʲæxʲkʲɪj"),
    (("не́‿за‿што",), "ˈnʲe‿zə‿ʂtə"),
    (("град идёт",), "ɡrat ɪˈdʲɵt"),
    (("гра̂д‿идёт",), "ɡrad‿ɨˈdʲɵt"),
    (("град‿идёт",), "ɡrəd‿ɨˈdʲɵt"),
    (("ро́г‿изоби́лия",), "ˈroɡ‿ɨzɐˈbʲilʲɪjə"),
    (("приводи́ть в замеша́тельство",), "prʲɪvɐˈdʲidʲ v‿zəmʲɪˈʂatʲɪlʲstvə"),
    (("ты ве́ришь в Бо́га",), "tɨ ˈvʲerʲɪʐ ˈv‿boɡə"),
    (("муж Ва́ли",), "muʂ ˈvalʲɪ"),
    (("брат вдовы́",), "brad vdɐˈvɨ"),
    (("ваш взор",), "vaʐ vzor"),
    (("от взгля́дов",), "ɐd‿ˈvzɡlʲadəf"),
    (("волк ка́ждый год линя́ет",), "volk ˈkaʐdɨj ɡot lʲɪˈnʲæ(j)ɪt"),
    (("сча́стливо",), "ˈɕːaslʲɪvə, ˈɕːæsʲlʲɪvə"),
    (("да́вя̣т",), "ˈdavʲət"),
    (("посме́шища̣м",), "pɐsˈmʲeʂɨɕːəm"),
    (("код Мо́рзэ",), "kot ˈmorzɨ"),
    (("наря́д на ку́хню",), "nɐˈrʲat nɐ‿ˈkuxnʲʊ"),
    (("ждать щу́ку",), "ʐdat͡ɕ ˈɕːukʊ"),
    (("за́пись Шу́берта",), "ˈzapʲɪɕ ˈʂubʲɪrtə"),
    (("гусь жа́ренный",), "ɡuʑ ˈʐarʲɪn(ː)ɨj"),
    (("туз черве́й",), "tuɕ t͡ɕɪrˈvʲej"),
    (("о̀ргкомите́т",), "ˌorkəmʲɪˈtʲet"), #FIXME
    (("То́кио же",), "ˈtokʲɪo‿ʐɨ"),
    (("ве́псский",), "ˈvʲepsːkʲɪj"),
    (("Черке́сск",), "t͡ɕɪrˈkʲesːk"),
    (("ада́жио",), "ɐˈdaʐɨo"),
    (("арпе́джио",), "ɐrˈpʲed͡ʐʐɨo"),
    (("с глаз доло́й — из се́рдца вон",), "ˈz‿ɡlaz dɐˈloj | ɪs‿ˈsʲert͡sə von"),
    (("аппле́т",), "ɐˈplʲet"),
    (("Киргизста́н",), "kʲɪrɡʲɪˈstan"),
    (("жжёт",), "ʐːot"), #FIXME
    (("друг к дру́гу",), "druɡ ˈɡ‿druɡʊ"),
    (("(и) пода́вно",), "(i) pɐˈdavnə"),
    (("рабфа́к",), "rɐpˈfak"),
    (("со́бственник",), "ˈsopstvʲɪnʲ(ː)ɪk"),
    (("твё́рдость",), "ˈtvʲɵrdəsʲtʲ"),
    (("просчё́т",), "prɐˈɕːɵt"),
    (("кало́сс",), "kɐˈlos"),
    (("Иоа́нн",), "ɪɐˈan"),
    (("йе́ти",), "ˈjetʲɪ"),
    (("а̀нгло-норма́ннский",), "ˌanɡlə nɐrˈmanskʲɪj"),
    (("фуррь",), "furʲ"),
    (("ха́о̂с",), "ˈxaos"),
    (("эвфеми́зм",), "ɨfʲɪˈmʲizm"),
    (("хору́гвь",), "xɐˈrukfʲ"),
    (("по абази́ну",), "pɐ‿ɐbɐˈzʲinʊ"),
    (("под абази́ном",), "pəd‿əbɐˈzʲinəm"),
    (("подсти́лка",), "pɐt͡sʲˈsʲtʲilkə"), #FIXME
    (("э́ллипс",), "ˈɛlʲɪps"),
    (("иди́ллия",), "ɪˈdʲilʲɪjə"),
    (("-ин",), "ɪn"),
    (("фойе́", None, "y"), "fɐˈjːe"),
    (("льстец",), "lʲsʲtʲet͡s"),
    (("инсти́нкт",), "ɪn⁽ʲ⁾ˈsʲtʲinkt"),
    (("ни́ндзя",), "ˈnʲinʲd͡zʲzʲə"), #FIXME
    (("Хэйлунцзя́н",), "xɨjlʊnʲˈd͡zʲzʲan"), #FIXME
    (("проце́нтщик",), "prɐˈt͡sɛnʲɕːɪk"),
    (("брюзжа́ть",), "brʲʊˈʐːatʲ"),
    (("львёнок",), "ˈlʲvʲɵnək"),
    (("помпе́зный",), "pɐm⁽ʲ⁾ˈpʲeznɨj"),
    (("любви́",), "lʲʊbˈvʲi, lʲʉbʲˈvʲi"),
    (("обвини́тельный",), "ɐbvʲɪˈnʲitʲɪlʲnɨj"),
    (("вбира́ть",), "v⁽ʲ⁾bʲɪˈratʲ"),
    (("впечатли́тельный",), "f⁽ʲ⁾pʲɪt͡ɕɪtˈlʲitʲɪlʲnɨj"),
    (("дѐло в то́м, што",), "ˌdʲelə ˈf‿tom | ʂto"),
    (("де́вственная плева́",), "ˈdʲefstvʲɪn(ː)əjə plʲɪˈva"),
    (("хуаця́о",), "xʊɐˈt͡sʲao"), #FIXME
    (("Цю́рих",), "ˈt͡sʲʉrʲɪx"), #FIXME
    (("тайцзицюа́нь",), "təjd͡zʲzʲɪt͡sʲʊˈanʲ"), #FIXME
    (("Цзили́нь",), "d͡zʲzʲɪˈlʲinʲ"), #FIXME
    (("будь што бу́дет",), "but͡ɕ ʂto ˈbudʲɪt"),
    (("дух бодр, плоть же не́мощна",), "duɣ bodr | ˈplod͡ʑ‿ʐɨ ˈnʲeməɕːnə"),
    (("Пи́тсбург",), "ˈpʲid͡zbʊrk"),
    (("Ло̀с-А́нджелес",), "ˌlos ˈand͡ʐʐɨlʲɪs"),
    (("АльДжази́ра",), "ɐlʲd͡ʐʐɐˈzʲirə"),
    (("Петрозаво́дск",), "pʲɪtrəzɐˈvot͡sk"),
    (("Джо́рджтаун",), "ˈd͡ʐʐort͡ʂʂtəʊn"),
    (("Нджаме́на",), "nd͡ʐʐɐˈmʲenə"),
    (("муншту́к",), "mʊnʂˈtuk"),
    (("Джордж",), "d͡ʐʐort͡ʂʂ"),
    (("Гуйчжо́у",), "ɡʊjˈd͡ʐʐoʊ"),
    (("Чжэцзя́н",), "d͡ʐʐɨˈd͡zʲzʲan"), #FIXME
    (("аге́нтство",), "ɐˈɡʲent͡stvə"),
    (("с жено́й",), "ʐ‿ʐɨˈnoj"),
    (("без ша́пки",), "bʲɪʂ‿ˈʂapkʲɪ"),
    (("отста́вка",), "ɐt͡sˈstafkə"),
    (("отстегну́ть",), "ɐt͡sʲsʲtʲɪɡˈnutʲ"), #FIXME
    (("подсласти́тель",), "pət͡sslɐˈsʲtʲitʲɪlʲ"),
    (("о́тзвук",), "ˈod͡zzvʊk"),
    (("коттэ́дж",), "kɐˈtɛt͡ʂʂ"),
    (("подсчёт",), "pɐt͡ɕˈɕːɵt"),
    (("отсчи́тываться",), "ɐt͡ɕˈɕːitɨvət͡sə"),
    (("отжи́ть",), "ɐd͡ʐˈʐɨtʲ"),
    (("таджи́к",), "tɐd͡ʐˈʐɨk"),
    (("дщерь",), "t͡ɕɕːerʲ"),
    (("тще́тно",), "ˈt͡ɕɕːetnə"),
    (("мла́дший",), "ˈmlat͡ʂʂɨj"),
    (("отшиби́ть",), "ɐt͡ʂʂɨˈbʲitʲ"),
    (("пядь земли́",), "pʲæd͡zʲ zʲɪˈmlʲi"), #FIXME
    (("под сту́лом",), "pɐt͡s‿ˈstuləm"),
    (("надзо́р",), "nɐd͡zˈzor"),
    (("отсю́да",), "ɐt͡sʲˈsʲudə"), #FIXME
    (("отсу́да",), "ɐt͡sˈsudə"),
    (("вѐт/слу́жба",), "ˌvʲet͡sˈsluʐbə"),
    (("куро́ртник",), "kʊˈrort⁽ʲ⁾nʲɪk"),
    (("сболтнёшь",), "zbɐlt⁽ʲ⁾ˈnʲɵʂ"),
    (("сболтну́ть",), "zbɐltˈnutʲ"),
    (("спу́тник",), "ˈsputʲnʲɪk"),
    (("расчерти́ть",), "rəɕt͡ɕɪrˈtʲitʲ"),
    (("убе́жищa",), "ʊˈbʲeʐɨɕːə"),
    (("уда́ча",), "ʊˈdat͡ɕə"),
    (("тро́лль",), "ˈtrolʲ"),
    (("подча́с",), "pɐˈt͡ɕːas"),
    (("в ссо́ри",), "ˈf‿sːorʲɪ"),
    #	{ "четырё̀хле́тний",), "t͡ɕɪtɨˌrʲɵxˈlʲet⁽ʲ⁾nʲɪj"), # should there be a syllable boundary between x and l?
    (("подтрибу́нный",), "pətːrʲɪˈbunːɨj"),
    (("што́-то",), "ˈʂto‿tə"),
    (("не всё то зо́лото",), "nʲɪ‿ˈfsʲɵ to ˈzolətə"),
    (("не по нутру́",), "nʲɪ‿pə‿nʊˈtru"),
    (("в то вре́мя как",), "ˈf‿to ˈvrʲemʲə kak"),
    (("не к ме́сту",), "nʲɪ‿k‿ˈmʲestʊ"),
    (("де́сять за́поведей",), "ˈdʲesʲɪd͡zʲ ˈzapəvʲɪdʲɪj"), #FIXME
    (("мно́го бу́дешь знать",), "ˈmnoɡə ˈbudʲɪʐ znatʲ"),
    (("вою́ю",), "vɐˈjʉjʊ"),
    (("безъя́тие", None, "n"), "bʲɪzˈjætʲɪje"),
    (("То́кио",), "ˈtokʲɪo"),
    (("розе́ттский ка́мень",), "rɐˈzʲet͡skʲɪj ˈkamʲɪnʲ"),
    (("от я́блони",), "ɐt‿ˈjablənʲɪ"),
    (("от А́ни",), "ɐˈt‿anʲɪ"),
    (("дама́сский",), "dɐˈmasːkʲɪj"),
    (("ельча́нин",), "(j)ɪlʲˈt͡ɕænʲɪn"),
    (("коменда́нтский ча́с",), "kəmʲɪnˈdan(t)skʲɪj ˈt͡ɕas"),
    (("а̀нгло-норма́ннский",), "ˌanɡlə nɐrˈmanskʲɪj"),
    (("исла́ндский",), "ɪsˈlan(t)skʲɪj"),
    (("коопера́ция",), "kɐɐpʲɪˈrat͡sɨjə"),
    (("съе́ӂӂая",), "ˈsjeʑːɪjə"),
    (("сѣдло́",), "sʲɪdˈlo"),
    (("сѣ̈дла",), "ˈsʲɵdlə"),
    (("мне жа́рко",), "mnʲe ˈʐarkə"),
    (("на вку́с и на цвет това́рищей нет",), "nɐ‿ˈfkus i nɐ‿ˈt͡svʲet tɐˈvarʲɪɕːɪj nʲet"),
    (("ма́стер на все ру́ки",), "ˈmasʲtʲɪr nɐ‿ˈfsʲe ˈrukʲɪ"),
    (("мля",), "mlʲa"),
    (("четырё̀хзвёздный",), "t͡ɕɪtɨˌrʲɵɣzˈvʲɵznɨj"),
    (("сегрегациони́сский",), "sʲɪɡrʲɪɡət͡sɨɐˈnʲisːkʲɪj"),
    (("сегрегациони́стский",), "sʲɪɡrʲɪɡət͡sɨɐˈnʲist͡skʲɪj"),
    (("пья́нка",), "ˈpʲjankə"), #FIXME
    (("нѐореали́зм",), "ˌnʲeərʲɪɐˈlʲizm"),
    (("ре́гентша",), "ˈrʲeɡʲɪnt͡ʂʂə"),
    (("нра́вственный",), "ˈnrafstvʲɪn(ː)ɨj"),
    (("што́-лѝбо",), "ˈʂto ˌlʲibə"),
    (("гроздь",), "ɡrosʲtʲ"),
    (("ружьё",), "rʊʐˈjɵ"),
    (("фильм",), "fʲilʲm"),
    (("взаѝмопонима́ние", None, "n"), "vzɐˌiməpənʲɪˈmanʲɪje"),
    (("скамья́",), "skɐˈmʲja"), #FIXME
    (("славянофи́льство",), "sləvʲɪnɐˈfʲilʲstvə"),
    (("сельдь",), "sʲelʲtʲ"),
    (("секво́йя",), "sʲɪkˈvojːə"),
    (("ро́жью",), "ˈroʐjʊ"),
    (("Ю̀жно-Африка́нская Респу́блика",), "ˌjuʐnə ɐfrʲɪˈkanskəjə rʲɪˈspublʲɪkə"),
    (("Дза̀уджика́у",), "ˌd͡zzaʊd͡ʐʐɨˈkaʊ"),
    (("Вели́кая Арме́ния",), "vʲɪˈlʲikəjə ɐrˈmʲenʲɪjə"),
    (("Асунсьо́н",), "ɐsʊn⁽ʲ⁾ˈsʲjɵn"),
    (("Амударья́",), "ɐmʊdɐˈrʲja"),
    (("та́ять",), "ˈta(j)ɪtʲ"),
    (("Арха́нгельск",), "ɐrˈxanɡʲɪlʲsk"),
    (("нецелесообра́зный",), "nʲɪt͡sɨlʲɪsɐɐˈbraznɨj"),
    (("тьфу",), "tʲfu"),
    (("съезд",), "sjest"),
    (("съёмка",), "ˈsjɵmkə"),
    (("предвкуше́ние", None, "n"), "prʲɪtfkʊˈʂɛnʲɪje"),
    (("файрво́лл",), "fɐjrˈvol"),
    (("элѐктроэнэ́ргия",), "ɨˌlʲektrəɨˈnɛrɡʲɪjə"),
    (("нало̀гоплате́льщик",), "nɐˌloɡəplɐˈtʲelʲɕːɪk"),
    (("НЭП",), "nɛp"),
    (("Вьентья́н",), "vʲjɪnʲˈtʲjan"),
    (("шпиль",), "ʂpʲilʲ"),
    (("ка-гэ-бэ́",), "ka ɡɛ ˈbɛ"),
    (("презре́нный",), "prʲɪzˈrʲenːɨj"),
    (("несоверше́нный",), "nʲɪsəvʲɪrˈʂɛnːɨj"),
    (("пятсо́т",), "pʲɪt͡sˈsot"),
    (("шестьдеся́т",), "ʂɨzʲdʲɪˈsʲat"),
    (("пятьдеся́т",), "pʲɪdʲɪˈsʲat"),
    (("сʔу́женный",), "ˈsʔuʐɨn(ː)ɨj"),
    (("съу́женный",), "ˈsʔuʐɨn(ː)ɨj"),
    (("воӂӂа́",), "vɐˈʑːa"),
    (("дро́ӂӂи",), "ˈdroʑːɪ"),
    (("погля́дывать",), "pɐˈɡlʲadɨvətʲ"),
    (("до встре́чи",), "dɐ‿ˈfstrʲet͡ɕɪ"),
    (("варьи́ровать",), "vɐˈrʲjirəvətʲ"),
    (("юла́",), "jʊˈla"),
    (("валя́ться",), "vɐˈlʲat͡sːə"),
    (("подде́ржка",), "pɐˈdʲːerʂkə"),
    (("сверхинтере́сный",), "svʲɪrxɨnʲtʲɪˈrʲesnɨj"),
    (("вещдо́к",), "vʲɪʑːˈdok"),
    (("яйцо́",), "(j)ɪjˈt͡so"),
    (("ещё",), "(j)ɪˈɕːɵ"),
    (("за́яц",), "ˈza(j)ɪt͡s"),
    (("отдохну́ть",), "ɐdːɐxˈnutʲ"),
    (("до́чь бы",), "ˈdod͡ʑ‿bɨ"),
    (("де́йственный",), "ˈdʲejstvʲɪn(ː)ɨj"),
    (("я",), "ja"),
    (("дождь",), "doʂtʲ"),
    (("дощ",), "doɕː"),
    (("ночь",), "not͡ɕ"),
    (("смеёшься",), "smʲɪˈjɵʂsʲə"),
    (("ничья́",), "nʲɪˈt͡ɕja"),
    (("аа́к",), "ɐˈak"),
    (("аа́м",), "ɐˈam"),
    (("аа́нгич",), "ɐˈanɡʲɪt͡ɕ"),
    (("ааро́новец",), "ɐɐˈronəvʲɪt͡s"),
    (("ааро́новщина",), "ɐɐˈronəfɕːɪnə"),
    (("а́ба",), "ˈabə"),
    (("абава́н",), "ɐbɐˈvan"),
    (("абавуа́",), "ɐbəvʊˈa"),
    (("абажу́р",), "ɐbɐˈʐur"),
    (("аба́з",), "ɐˈbas"),
    (("абаза́",), "ɐbɐˈza"),
    (("абази́н",), "ɐbɐˈzʲin"),
    (("абази́нка",), "ɐbɐˈzʲinkə"),
    (("абази́я",), "ɐbɐˈzʲijə"),
    (("аба́к",), "ɐˈbak"),
    (("абака́",), "ɐbɐˈka"),
    (("абако́ст",), "ɐbɐˈkost"),
    (("абаку́мыч",), "ɐbɐˈkumɨt͡ɕ"),
    (("Аба́лкин",), "ɐˈbalkʲɪn"),
    (("абало́н",), "ɐbɐˈlon"),
    (("абандо́н",), "ɐbɐnˈdon"),
    (("абарогно́з",), "ɐbərɐɡˈnos"),
    (("абато́н",), "ɐbɐˈton"),
    (("абаша́",), "ɐbɐˈʂa"),
    (("абба́си",), "ɐˈbasʲɪ"),
    (("абба́т",), "ɐˈbat"),
    (("аббати́са",), "ɐbɐˈtʲisə"),
    (("абба́тство",), "ɐˈbat͡stvə"),
    (("аббревиату́ра",), "ɐbrʲɪvʲɪɐˈturə"),
    (("аббревиа́ция",), "ɐbrʲɪvʲɪˈat͡sɨjə"),
    (("абда́л",), "ɐbˈdal"),
    (("абдери́т",), "ɐbdʲɪˈrʲit"),
    (("абде́ст",), "ɐbˈdʲest"),
    (("абдика́ция",), "ɐbdʲɪˈkat͡sɨjə"),
    (("абдо́мен",), "ɐbˈdomʲɪn"),
    (("абдукта́нт",), "ɐbdʊkˈtant"),
    (("абду́ктор",), "ɐbˈduktər"),
    (("абду́кция",), "ɐbˈdukt͡sɨjə"),
    (("абэвэ́га",), "ɐbɨˈvɛɡə"),
    (("а́белев",), "ˈabʲɪlʲɪf"),
    (("абе́лия",), "ɐˈbʲelʲɪjə"),
    (("абельмо́ш",), "ɐbʲɪlʲˈmoʂ"),
    (("аберра́ция",), "ɐbʲɪˈrat͡sɨjə"),
    (("абе́с",), "ɐˈbʲes"),
    (("абесси́в",), "ɐbʲɪˈsʲif"),
    (("абза́ц",), "ɐbˈzat͡s"),
    (("абиети́н",), "ɐbʲɪ(j)ɪˈtʲin"),
    (("аби́лка",), "ɐˈbʲilkə"),
    (("абисса́ль",), "ɐbʲɪˈsalʲ"),
    (("абисси́нец",), "ɐbʲɪˈsʲinʲɪt͡s"),
    (("абитурие́нт",), "ɐbʲɪtʊrʲɪˈjent"),
    (("абитурие́нтка",), "ɐbʲɪtʊrʲɪˈjentkə"),
    (("аблакта́ция",), "ɐblɐkˈtat͡sɨjə"),
    (("аблакти́рование", None, "n"), "ɐblɐkˈtʲirəvənʲɪje"),
    (("аблактиро́вка",), "ɐbləktʲɪˈrofkə"),
    (("аблати́в",), "ɐblɐˈtʲif"),
    (("абла́ут",), "ɐˈblaʊt"),
    (("абляти́в",), "ɐblʲɪˈtʲif"),
    (("абля́ция",), "ɐˈblʲat͡sɨjə"),
    (("аболициони́зм",), "ɐbəlʲɪt͡sɨɐˈnʲizm"),
    (("аболициони́ст",), "ɐbəlʲɪt͡sɨɐˈnʲist"),
    (("аболициони́стка",), "ɐbəlʲɪt͡sɨɐˈnʲistkə"),
    (("абонеме́нт",), "ɐbənʲɪˈmʲent"),
    (("абоне́нт",), "ɐbɐˈnʲent"),
    (("аборда́ж",), "ɐbɐrˈdaʂ"),
    (("абориге́н",), "ɐbərʲɪˈɡʲen"),
    (("або́рт",), "ɐˈbort"),
    (("абрази́в",), "ɐbrɐˈzʲif"),
    (("абрази́вность",), "ɐbrɐˈzʲivnəsʲtʲ"),
    (("абра́зия",), "ɐˈbrazʲɪjə"),
    (("абракада́бра",), "ɐbrəkɐˈdabrə"),
    (("абрико́с",), "ɐbrʲɪˈkos"),
    (("абрикоти́н",), "ɐbrʲɪkɐˈtʲin"),
    (("а́брис",), "ˈabrʲɪs"),
    (("аброга́ция",), "ɐbrɐˈɡat͡sɨjə"),
    (("абса́нс",), "ɐpˈsans"),
    (("абси́да",), "ɐpˈsʲidə"),
    (("абсолю́т",), "ɐpsɐˈlʲut"),
    (("абсолютиза́ция",), "ɐpsəlʲʉtʲɪˈzat͡sɨjə"),
    (("абсолютизи́рование", None, "n"), "ɐpsəlʲʉtʲɪˈzʲirəvənʲɪje"),
    (("абсолютизи́ровать",), "ɐpsəlʲʉtʲɪˈzʲirəvətʲ"),
    (("абсолюти́зм",), "ɐpsəlʲʉˈtʲizm"),
    (("абсолюти́ст",), "ɐpsəlʲʉˈtʲist"),
    (("абсолю́тность",), "ɐpsɐˈlʲutnəsʲtʲ"),
    (("абсолю́тный",), "ɐpsɐˈlʲutnɨj"),
    (("абсорба́т",), "ɐpsɐrˈbat"),
    (("абсорбе́нт",), "ɐpsɐrˈbʲent"),
    (("абсо́рбер",), "ɐpˈsorbʲɪr"),
    (("абсорби́рование", None, "n"), "ɐpsɐrˈbʲirəvənʲɪje"),
    (("абсорби́ровать",), "ɐpsɐrˈbʲirəvətʲ"),
    (("абсорби́роваться",), "ɐpsɐrˈbʲirəvət͡sə"),
    (("абсо́рбция",), "ɐpˈsorpt͡sɨjə"),
    (("абстине́нт",), "ɐpsʲtʲɪˈnʲent"),
    (("абстине́нция",), "ɐpsʲtʲɪˈnʲent͡sɨjə"),
    (("абстраги́рование", None, "n"), "ɐpstrɐˈɡʲirəvənʲɪje"),
    (("абстраги́ровать",), "ɐpstrɐˈɡʲirəvətʲ"),
    (("абстра́кт",), "ɐpˈstrakt"),
    (("абстра́ктность",), "ɐpˈstraktnəsʲtʲ"),
    (("абстра́ктный",), "ɐpˈstraktnɨj"),
    (("абстракциони́зм",), "ɐpstrəkt͡sɨɐˈnʲizm"),
    (("абстракциони́ст",), "ɐpstrəkt͡sɨɐˈnʲist"),
    (("абстра́кция",), "ɐpˈstrakt͡sɨjə"),
    (("абсу́рд",), "ɐpˈsurt"),
    (("абсурди́зм",), "ɐpsʊrˈdʲizm"),
    (("абсурди́ст",), "ɐpsʊrˈdʲist"),
    (("абсу́рдность",), "ɐpˈsurdnəsʲtʲ"),
    (("абсу́рдный",), "ɐpˈsurdnɨj"),
    (("абсце́сс",), "ɐpˈst͡sɛs"),
    (("абсци́сса",), "ɐpˈst͡sɨsːə"),
    (("абули́я",), "ɐbʊˈlʲijə"),
    (("абха́з",), "ɐpˈxas"),
    (("аванга́рд",), "ɐvɐnˈɡart"),
    (("аванпо́ст",), "ɐvɐnˈpost"),
    (("ава́нс",), "ɐˈvans"),
    (("авансце́на",), "ɐvɐnˈst͡sɛnə"),
    (("авантю́ра",), "ɐvɐnʲˈtʲurə"),
    (("авантюри́зм",), "ɐvənʲtʲʉˈrʲizm"),
    (("авантюри́ст",), "ɐvənʲtʲʉˈrʲist"),
    (("авантюри́стка",), "ɐvənʲtʲʉˈrʲistkə"),
    (("ава́рец",), "ɐˈvarʲɪt͡s"),
    (("ава́рия",), "ɐˈvarʲɪjə"),
    (("авата́р",), "ɐvɐˈtar"),
    (("авгу́р",), "ɐvˈɡur"),
    (("а́вгуст",), "ˈavɡʊst"),
    (("А́вель",), "ˈavʲɪlʲ"),
    (("авеню́",), "ɐvʲɪˈnʲu"),
    (("авиаба́за",), "ɐvʲɪɐˈbazə"),
    (("авиабиле́т",), "ɐvʲɪəbʲɪˈlʲet"),
    (("авиабрига́да",), "ɐvʲɪəbrʲɪˈɡadə"),
    (("авиагоризо́нт",), "ɐvʲɪəɡərʲɪˈzont"),
    (("авиадиви́зия",), "ɐvʲɪədʲɪˈvʲizʲɪjə"),
    (("авиазвено́",), "ɐvʲɪəzvʲɪˈno"),
    (("авиакомпа́ния",), "ɐvʲɪəkɐmˈpanʲɪjə"),
    (("авиако́рпус",), "ɐvʲɪɐˈkorpʊs"),
    (("авиали́ния",), "ɐvʲɪɐˈlʲinʲɪjə"),
    (("авиама́тка",), "ɐvʲɪɐˈmatkə"),
    (("авианалёт",), "ɐvʲɪənɐˈlʲɵt"),
    (("авиано́сец",), "ɐvʲɪɐˈnosʲɪt͡s"),
    (("авиаотря́д",), "ɐvʲɪɐɐˈtrʲat"),
    (("авиапо́лк",), "ɐvʲɪɐˈpolk"),
    (("авиапо́чта",), "ɐvʲɪɐˈpot͡ɕtə"),
    (("авиапредприя́тие", None, "n"), "ɐvʲɪəprʲɪtprʲɪˈjætʲɪje"),
    (("авиа́тор",), "ɐvʲɪˈatər"),
    (("авиауда́р",), "ɐvʲɪəʊˈdar"),
    (("авиа́ция",), "ɐvʲɪˈat͡sɨjə"),
    (("ага́р-ага́р",), "ɐˈɡar ɐˈɡar"),
    (("заво́д подря́дчик",), "zɐˈvot pɐˈdrʲæt͡ɕːɪk"),
    (("пингпо́нг",), "pʲɪnkˈponk"),
    (("пти́ца-адъюта́нт",), "ˈptʲit͡sə ɐdjʊˈtant"),
    (("в чём де́ло",), "ˈf‿t͡ɕɵm ˈdʲelə"),
    (("голосовы́е свя́зки", None, "a"), "ɡələsɐˈvɨje ˈsvʲaskʲɪ"), #FIXME
    (("да́мы и господа́",), "ˈdamɨ i ɡəspɐˈda"),
    (("ссо́ра",), "ˈsːorə"),
    (("введе́ние", None, "n"), "vʲːɪˈdʲenʲɪje"),
    (("ввод",), "vːot"),
    (("гру́зчик",), "ˈɡruɕːɪk"),
    (("то́нна",), "ˈtonːə"),
    (("наедине́",), "nə(j)ɪdʲɪˈnʲe"),
    (("поеди́нок",), "pə(j)ɪˈdʲinək"),
    # palatal assimilation
    (("степь",), "sʲtʲepʲ"),
    (("здесь",), "zʲdʲesʲ"),
    (("по́нчик",), "ˈponʲt͡ɕɪk"),
    (("ка́менщик",), "ˈkamʲɪnʲɕːɪk"),
    (("снег",), "sʲnʲek"),
    (("снести́",), "sʲnʲɪˈsʲtʲi"),
    (("толстя́к",), "tɐlˈs⁽ʲ⁾tʲak"),
    (("о́ползни",), "ˈopəlz⁽ʲ⁾nʲɪ"),
    (("злить",), "z⁽ʲ⁾lʲitʲ"),
    (("подня́ть",), "pɐdʲˈnʲætʲ"),
    (("отня́ть",), "ɐtʲˈnʲætʲ"),
    (("ви́нтик",), "ˈvʲinʲtʲɪk"),
    (("пе́нсия",), "ˈpʲen⁽ʲ⁾sʲɪjə"),
    (("с(ь)ни́керс",), "ˈs⁽ʲ⁾nʲikʲɪrs"),
    # gemination of certain sequences
    (("расщепи́ть",), "rəɕːɪˈpʲitʲ"),
    (("сшить",), "ʂːɨtʲ"),
    (("сжать",), "ʐːatʲ"),
    (("отцепи́ть",), "ɐt͡sːɨˈpʲitʲ"),
    (("отчёт",), "ɐˈt͡ɕːɵt"),
    # consonants eliminated in certain clusters
    (("здра́ствуй",), "ˈzdrastvʊj"),
    (("чу́ствовать",), "ˈt͡ɕustvəvətʲ"),
    (("по́здно",), "ˈpoznə"),
    (("уздцы́",), "ʊˈst͡sɨ"),
    (("голла́ндцы",), "ɡɐˈlant͡sɨ"),
    (("ланша́фт",), "lɐnˈʂaft"),
    (("рентге́н",), "rʲɪnˈɡʲen"),
    (("сердчи́шко",), "sʲɪrˈt͡ɕiʂkə"),
    (("счастли́вый",), "ɕːɪs⁽ʲ⁾ˈlʲivɨj"),
    (("ме́стный",), "ˈmʲesnɨj"),
    (("улыба́ется",), "ʊlɨˈba(j)ɪt͡sə"),
    (("чёрный",), "ˈt͡ɕɵrnɨj"),
    (("у́зко",), "ˈuskə"),
]


class TestRuPronMeta(type):
    """TestRuPron meta class
    """
    def __new__(mcs, name, bases, dicts):
        def gen_test_ru_to_IPA(ru_args, ru_IPA):
            """Generate ru text to IPA testcases.

            Parameters
            ----------
            ru_args : tuple
                Tuple of Russian text and args in {{ru-IPA}} template
                parsed from Wiktionary.
            ru_IPA : string
                String of expected Russian IPA after conversion.

            Returns
            -------
            test: function
                AssertEqual of two texts.
            """
            def test(self):
                """AssertEqual of ru text and converted IPA.
                """
                return self.assertEqual(
                    ru_pron.to_IPA(*ru_args),
                    ru_IPA
                )
            return test

        for i, (ru_args, ru_IPA) in enumerate(TESTCASES):
            if len(ru_args) > 1:
                ru_text, pos, gem = ru_args
                ru_args = (ru_text, None, gem, None, pos)
            test_ru_to_IPA_name = "test_ru_to_IPA_%06d" % i
            dicts[test_ru_to_IPA_name] = \
                gen_test_ru_to_IPA(ru_args, ru_IPA)
        return type.__new__(mcs, name, bases, dicts)


class TestRuPron(with_metaclass(TestRuPronMeta, unittest.TestCase)):
    """TestRuPron class
    """
    pass


if __name__ == "__main__":
    unittest.main()
