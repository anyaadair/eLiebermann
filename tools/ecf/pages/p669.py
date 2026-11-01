# Liebermann, Gesetze I p. 669: ECf and ECf retr 38,2–39 (39,1 begins on p. 669 and runs on: see p670.py)
D = lambda de, en: (de, en)
FA = D('<i>an den Kläger im Anefang; denn solcher Process, mit Voraussetzung, dass der Gegenstand nicht bloss in falscher Handelsform erworben, sondern von jemandem gestohlen war, konnte allein zum Reinigungseide und zur Friedloslegung des ausbleibenden Gewähren führen</i>',
       'to the claimant in the vouching process (Anefang); for such a suit, presupposing that the object had not merely been acquired in an improper form of trade but had been stolen from someone, could only lead to an oath of purgation and to the outlawing of the warrantor who failed to appear')
FB = D('<i>hier nur Leumundszeugen</i>', 'here only character witnesses')
FC = D('Gesetzwidrigkeit, <i>aus nordöstlichem Frankreich bezeugt von Ducange</i>', 'unlawfulness; attested from north-eastern France by Ducange')
FDd = D('<i>zwischen diesem Zeugniss und dem künftigen Eide denke hinzu</i> Verhaftung <i>oder</i> Verbürgung', 'between this testimony and the future oath, supply arrest or surety')
FE = D('<i>befragt vom königlichen Justiciar, findet das Shiregericht das Beweisurtheil, wie schwer dem Käufer der Eid zu gestalten sei, ‘dass er den Verkäufer für schuldlos hielt’; vgl.</i> 23, 4 <i>und die Formel</i> Swerian 9',
       'asked by the royal justiciar, the shire court finds the judgement of proof, how hard the oath ‘that he held the seller to be blameless’ is to be made for the buyer; cf. 23, 4 and the formula Swerian 9')
FF = D('<i>jener Verkäufer</i>', 'that seller')
FFF = D('<i>C.</i> 38', 'c. 38')
FG = D('<i>eine</i> Flæscmangara stræt <i>hat Winchester</i> 996 (<i>Earle</i> Landchar. 364), banci in macello <i>York im</i> 11. <i>Jh.</i> (Domesday), <i>das Wort</i> mangara <i>manche Nordische Kaufstadt, wie Dublin</i>',
       'Winchester has a Flæscmangara stræt in 996 (Earle, Landchar. 364), York banci in macello in the 11th century (Domesday), and many northern trading towns, such as Dublin, the word mangara')
NP = {}
CLAUSES = [
 {'code': 'ECf', 'n': '38.2', 'page': 669, 'erkl': ['lagemannos'],
  'text': 'Quodsi aliquis{1} aliter emerit, quod stulte emit{2} perdat{f:a}{3}; et forisfacturam{4}! Et postea inquiret{5} iusticia per{f:b} lagemannos{6} et per{7} meliores homines de burgo uel de{8} hundredo uel uilla, ubi emptor{9} ipse manserit, de quali uita ipse est{10}, et si antea{7} audierunt{11} eum{7} calumpniari{12} de exlegalitate{f:c}.',
  'notes': {'f:a': FA, 'f:b': FB, 'f:c': FC, 1: D('aliter aliquis <i>S</i>', 'aliter aliquis S'), 2: D('emat <i>Hr</i>', 'emat Hr'), 3: D('-det <i>Hk</i>', '-det Hk'), 4: D('forsf. <i>Rl</i>', 'forsf. Rl'),
            5: D('-rat <i>S Hr</i>', '-rat S Hr'), 6: D('laghe. <i>Rl;</i> lagahem. <i>Hk</i>', 'laghe. Rl; lagahem. Hk'), 7: D('<i>fehlt Hr</i>', 'lacking in Hr'), 8: D('<i>fehlt Hk S</i>', 'lacking in Hk S'),
            9: D('i. e. <i>Hk Hr</i>', 'i. e. Hk Hr'), 10: D('sit <i>Hr</i>', 'sit Hr'), 11: D('-rint <i>Hk S Hr</i>', '-rint Hk S Hr'), 12: D('eum <i>fügt nochmals zu Rl</i>', 'Rl adds eum again')}},
 {'code': 'ECf', 'n': '38.3', 'page': 669,
  'text': 'Quodsi{13} testati{14} fuerint eum{15} de legalitate{f:d}{16}, expurget se iudicio{f:e} comitatus, quod uenditorem nesciebat reum de hac uenditione nec de aliqua{17} alia exlegalitate{f:c}{18}.',
  'notes': {'f:c': FC, 'f:d': FDd, 'f:e': FE, 13: D('Qu. t. f. e. de leg. <i>überspringt Rl</i>', 'Rl skips Qu. t. f. e. de leg.'), 14: D('edificati <i>Hr</i>', 'edificati Hr'), 15: D('esse <i>fügt zu Hr</i>', 'Hr adds esse'),
            16: D('exleg. <i>Hk S</i>', 'exleg. Hk S'), 17: D('alia aliqua <i>Rl S</i>', 'alia aliqua Rl S'), 18: D('expurget — alia aliqua exleg. <i>wiederholt Rl</i>', 'Rl repeats expurget — alia aliqua exleg.')}},
 {'code': 'ECf', 'n': '38.3a', 'page': 669,
  'text': 'Et si scit{19} uenditorem, quis{20} sit uel{21} ubi sit, dicat; et iusticia querat eum ad faciendam iusticiam; et si{f:f} inueniri{23} non poterit, utlagetur{f:f}.',
  'notes': {'f:f': FF, 19: D('sciat <i>S</i>', 'sciat S'), 20: D('qui <i>Rl</i>', 'qui Rl'), 21: D('et <i>S</i>', 'et S'), 23: D('n. i. <i>Hr;</i> -ire <i>Hk</i>', 'n. i. Hr; -ire Hk')},
  'editorial': ['There is no note 22 in the ECf column of this page: Liebermann’s numbering goes from 21 to 23.', 'Liebermann puts his note f both after “si” and after “utlagetur”.']},
 {'code': 'ECf', 'n': '39', 'page': 669,
  'text': '{24}Cum autem{25}, ut dictum{f:ff} est, defensum esset, quod non emerent{26} animalia preter plegios, clamauerunt macerarii, quos Angli uocant{f:g} flaismangeres{27}, de ciuitatibus et burgis, quod quaque{28} die oportebat eos emere animalia, occidere et{29} uendere.',
  'notes': {'f:ff': FFF, 'f:g': FG, 24: D('<sp>De mascerariis</sp> <i>überschreibt Hr</i>', 'Hr heads it De mascerariis'), 25: D('a. di. est (sit <i>Hr</i>) <i>ohne</i> ut de. e. <i>Hk S Hr</i>', 'a. di. est (sit Hr) without ut de. e. Hk S Hr'),
            26: D('emt² a. sine plegiis <i>Hr</i>', 'emt² a. sine plegiis Hr'), 27: D('flesm. <i>Hk;</i> fleism. <i>S;</i> et <i>fügt zu Hk;</i> fleshenweris <i>Hr</i>', 'flesm. Hk; fleism. S; Hk adds et; fleshenweris Hr'),
            28: D('quadam <i>Hr</i>', 'quadam Hr'), 29: D('<i>fehlt Hk</i>', 'lacking in Hk')}},

 {'code': 'ECfRetr', 'n': '38.2', 'page': 669,
  'text': 'Si quis <b>hominum</b> aliter{1} <sp>emeret</sp>{2}, quod stulte <sp>emisset</sp> <b>(cito</b>{3}<b>)</b> perdet{4}; et{5} forisfacturam! Postea <sp>inquisisset</sp> iusticia{6} per lagamannos{7} et per meliores homines de burgo uel <b>de</b>{8} uilla uel de{9} hundredo, ubi <sp>mansisset</sp> emtor <b>et</b> de{10} quali uita <sp>fuisset</sp>, et si <b>unquam</b> <sp>audissent</sp> eum calumniari de exlegalitate.',
  'notes': {'f:a': FA, 'f:b': FB, 'f:c': FC, 1: D('alter <i>Va</i>', 'alter Va'), 2: D('e. q. s. <i>fehlt Hv</i>', 'e. q. s. lacking in Hv'), 3: D('<i>fehlt Cb Lb Hv</i>', 'lacking in Cb Lb Hv'),
            4: D('perderet <i>Cb Lb Hv Ph Db</i>', 'perderet Cb Lb Hv Ph Db'), 5: D('et f. <i>fehlt Co</i>', 'et f. lacking in Co'), 6: D('<i>fehlt Hv;</i> -am <i>Ph</i>', 'lacking in Hv; -am Ph'),
            7: D('lagem. <i>Cb Lond;</i> lakem. <i>Ph</i>', 'lagem. Cb Lond; lakem. Ph'), 8: D('<i>fehlt Hv</i>', 'lacking in Hv'), 9: D('<i>fehlt Cb Hv;</i> -eto <i>Cb</i>', 'lacking in Cb Hv; -eto Cb'), 10: D('qualis uite <i>Hv</i>', 'qualis uite Hv')}},
 {'code': 'ECfRetr', 'n': '38.3', 'page': 669,
  'text': 'Quodsi{11} <sp>testaretur</sp> eum de <b>bona uita</b>{12} <b>et</b> legalitate, <sp>purgaret</sp> se iudicio comitatus, quod uenditorem <sp>nesciret</sp>{13} reum de hac uenditione nec de aliqua alia exlegalitate.',
  'notes': {'f:c': FC, 'f:d': FDd, 'f:e': FE, 11: D('Qui si testarentur <i>Cb Lond;</i> Q. -rentur <i>Lb</i>', 'Qui si testarentur Cb Lond; Q. -rentur Lb'), 12: D('fama <i>Hv</i>', 'fama Hv'), 13: D('-rent <i>K</i>', '-rent K')}},
 {'code': 'ECfRetr', 'n': '38.3a', 'page': 669,
  'text': 'Et si <sp>sciret</sp> uenditorem <b>suum,</b> quis{14} <sp>esset</sp> uel ubi <sp>fuisset</sp>, <sp>diceret</sp>; iusticia{15} <b>uero</b> <sp>quereret</sp>{16} eum ad faciendam{17} <b>de eo</b> iusticiam; <b>qui</b> si inueniri non <sp>posset</sp>{18}, <sp>utlagaretur</sp>.',
  'notes': {'f:f': FF, 14: D('qui <i>K</i>', 'qui K'), 15: D('-iarius <i>Hv</i>', '-iarius Hv'), 16: D('requireret <i>Cb;</i> queret <i>Lond</i>', 'requireret Cb; queret Lond'),
            17: D('<i>so Cb Hv;</i> -dum <i>übr.;</i> i. de eo <i>Hv</i>', 'so Cb Hv; -dum the others; i. de eo Hv'), 18: D('-ent <i>K</i>', '-ent K')}},
 {'code': 'ECfRetr', 'n': '39', 'page': 669,
  'text': 'De{19} <b>emptoribus et macerariis</b>{20}<b>. (Qualiter quaue necessitate hoc decretum fuit postea ex parte mutatum.)</b> Cum autem dictum est, quod <b>nullus hominum</b> <sp>emeret</sp>{21} <b>absque</b> plegiis animal <b>uiuum,</b> clamauerunt macherarii{22} de ciuitatibus{23} et{24} <b>(de</b>{25}<b>)</b> burgis, quos{26} Angli uocant{27} flesmongeres{28}, quod <b>una</b>quaque die oportebat{29} eos animalia <b>uiua</b> emere{30}, occidere et uendere; <b>nam in occisione animalium erat uita eorum.</b>',
  'notes': {'f:ff': FFF, 'f:g': FG,
            19: D('De e. et m. <i>nur Lond;</i> De occisionibus animalium contra natale <i>Pl S;</i> De murmure ementium <i>Cb;</i> Modificatio precedentium decretorum <i>Db;</i> Qualiter—mutatum <i>Lb Va Hv</i>',
                  'De e. et m. only Lond; De occisionibus animalium contra natale Pl S; De murmure ementium Cb; Modificatio precedentium decretorum Db; Qualiter—mutatum Lb Va Hv'),
            20: D('macecra. <i>K</i>', 'macecra. K'), 21: D('<i>fehlt Va;</i> abs. pl. u. an. em., cl. <i>Hv</i>', 'lacking in Va; abs. pl. u. an. em., cl. Hv'),
            22: D('de ciu. macecrini, <i>umgestellt in</i> m. de c. <i>Cb;</i> machecrarii <i>Lb;</i> marchetrarii <i>Va;</i> macecra. <i>K</i>', 'de ciu. macecrini, transposed to m. de c. Cb; machecrarii Lb; marchetrarii Va; macecra. K'),
            23: D('-tate <i>Va</i>', '-tate Va'), 24: D('et—flesm. <i>fehlt Hv</i>', 'et—flesm. lacking in Hv'), 25: D('<i>fehlt Cb Lb Co</i>', 'lacking in Cb Lb Co'), 26: D('quod <i>K</i>', 'quod K'), 27: D('f. u. <i>Co</i>', 'f. u. Co'),
            28: D('-gares <i>Va</i>', '-gares Va'), 29: D('-teret <i>Va;</i> -tet eos u. a. e., uen. et oc. <i>Hv</i>', '-teret Va; -tet eos u. a. e., uen. et oc. Hv'), 30: D('et <i>fügt zu K</i>', 'K adds et')},
  'editorial': ['The heading has two parts: “De emptoribus et macerariis”, found only in Lond, and “Qualiter … mutatum”, in Lb Va Hv (note 19); Liebermann prints the second in brackets.']},
]
