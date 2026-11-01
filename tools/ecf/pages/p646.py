# Liebermann, Gesetze I p. 646: ECf and ECf retr 20,3–20,6 (ECf retr 21 rubric on this page: see p647.py)
D = lambda de, en: (de, en)
FA = D('<i>vgl.</i> 24, 1. <i>Dem Verfasser ist die Freibürgschaft territorialisirt, nicht rein persönlich</i>', 'cf. 24, 1. For the author the frankpledge is territorial, not purely personal')
FC = D('<i>den Plural bestätigt</i> Wl art. 8 <i>gegen den Retractator, dem Kemble</i> Saxons 250 <i>folgt</i>', 'Wl art. 8 confirms the plural, against the Retractator, whom Kemble, Saxons 250, follows')
FF = D('Richter', 'judge')
FG = D('<i>vgl.</i> 20, 3, <i>woraus Retr. schöpft; Eidesformel theilweise in</i> Wl art. 8', 'cf. 20, 3, from which the Retr. draws; the oath formula partly in Wl art. 8')
CLAUSES = [
 {'code': 'ECf', 'n': '20.3', 'page': 646, 'erkl': ['capitalis', 'tribus'],
  'text': 'Si autem infra supradictum{1} terminum inueniri non poterit, quia in omni friborge{2} unus erat{3} capitalis, quem{4} ipsi uocabant{5} friborges{6} heued{7}, ipse capitalis acciperet{8} duos de melioribus in{9} suo friborge{10} et de tribus{f:a} friborgis{11} propinquioribus uicinis suis accipiat de unoquoque{12} capitalem{13} et duos{14} similiter{15} de melioribus, si poterit{16} eos habere{17}, et se{f:b} duodecimo{18} expurget se et friborgum{19} suum, si facere poterit, de forisfacto{20} et fuga{21} supradicti malefactoris.',
  'notes': {'f:a': FA, 'f:b': D('<i>vgl.</i> Leis Wl 3; Wl art. 8', 'cf. Leis Wl 3; Wl art. 8'),
            1: D('pred. <i>Ad</i>', 'pred. Ad'), 2: D('-ghe <i>Rl;</i> fridb. <i>S;</i> -burga <i>Hr;</i> friþborga <i>Ad;</i> fridborga <i>Cl</i>', '-ghe Rl; fridb. S; -burga Hr; friþborga Ad; fridborga Cl'), 3: D('erit <i>Ad Do</i>', 'erit Ad Do'), 4: D('quod <i>Do</i>', 'quod Do'),
            5: D('-cant <i>Ad Do</i>', '-cant Ad Do'), 6: D('-ghes <i>Rl;</i> -ge <i>Hk Hr;</i> fridborg <i>S;</i> friþborge <i>Ad;</i> fridb. <i>Do</i>', '-ghes Rl; -ge Hk Hr; fridborg S; friþborge Ad; fridb. Do'), 7: D('-et <i>Hr;</i> haued <i>Ad</i>', '-et Hr; haued Ad'),
            8: D('-piet <i>Hr Ad</i>', '-piet Hr Ad'), 9: D('de sua friþborga <i>Ad Do</i>', 'de sua friþborga Ad Do'), 10: D('-ghe <i>Rl;</i> -go <i>Hr;</i> fridb. <i>S</i>', '-ghe Rl; -go Hr; fridb. S'), 11: D('-ghis <i>Rl;</i> fridb. <i>S;</i> friþb. <i>Ad</i>', '-ghis Rl; fridb. S; friþb. Ad'),
            12: D('unaquaque <i>Ad Do</i>', 'unaquaque Ad Do'), 13: D('friþborgum <i>fügt zu Ad Do</i>', 'Ad Do add friþborgum'), 14: D('s. d. <i>S</i>', 's. d. S'), 15: D('<i>fehlt Ad Do</i>', 'lacking in Ad Do'), 16: D('e. p. <i>Hr</i>', 'e. p. Hr'), 17: D('<i>fehlt Hk</i>', 'lacking in Hk'),
            18: D('-mum <i>Hk;</i> et friþborgam suam XII<sup>a</sup> persona exp., si <i>Ad Do</i>', '-mum Hk; et friþborgam suam XIIa persona exp., si Ad Do'), 19: D('-ghum <i>Rl</i>', '-ghum Rl'), 20: D('foref. <i>Rl</i>', 'foref. Rl'), 21: D('supradicta fuga m. <i>Ad Do</i>', 'supradicta fuga m. Ad Do')}},
 {'code': 'ECf', 'n': '20.4', 'page': 646, 'erkl': ['dampnum'],
  'text': 'Quod si facere{17} non poterit{22}, restaurarent{f:c}{23} dampnum, quod ipse{f:d} fecerat{24}, de proprio forisfactoris{25}, quantum durauerit, et de suo{f:e}; et erga iusticiam{f:f} emendent{26}, secundum{27} quod legaliter iudicatum fuerit eis.',
  'notes': {'f:c': FC, 'f:d': D('Missethäter, <i>wie</i> 20, 2', 'the wrongdoer, as at 20, 2'), 'f:e': D('<i>Vermögen aller Freibürgen</i>', 'the property of all the members of the frankpledge'), 'f:f': FF,
            17: D('<i>fehlt Hk</i>', 'lacking in Hk'), 22: D('-runt <i>Ad Do</i>', '-runt Ad Do'), 23: D('-urent <i>Hk Hr Ad Do;</i> -aret <i>S</i>', '-urent Hk Hr Ad Do; -aret S'), 24: D('-cit <i>Ad</i>', '-cit Ad'),
            25: D('foref. <i>Rl;</i> -facti <i>Hk</i>', 'foref. Rl; -facti Hk'), 26: D('-det <i>Hr</i>', '-det Hr'), 27: D('sec.—sacramentum <i>überspringt Do</i>', 'Do skips sec.—sacramentum')}},
 {'code': 'ECf', 'n': '20.5', 'page': 646,
  'text': 'Et tamen{28} sacramentum, quod non potuerunt{29} complere per uicinos{f:g}, per se ipsos nouem{30} iurent: se{31} immunes.',
  'notes': {'f:g': FG, 28: D('tantum <i>Rl S;</i> cum <i>Hr</i>', 'tantum Rl S; cum Hr'), 29: D('poterunt <i>Ad</i>', 'poterunt Ad'), 30: D('XX <i>Ad Do</i>', 'XX Ad Do'), 31: D('esse <i>fügt zu S</i>', 'S adds esse')}},
 {'code': 'ECf', 'n': '20.6', 'page': 646,
  'text': 'Et si aliquando{32} potuerint{33} eum{34} recuperare, aut{35} adducent eum ad iusticiam{f:f}, si potuerint{36}, aut{37} dicent iusticie{f:f}, ubi sit.',
  'notes': {'f:f': FF, 32: D('quando <i>Hk</i>', 'quando Hk'), 33: D('poterint <i>Rl;</i> poterunt <i>Ad</i>', 'poterint Rl; poterunt Ad'), 34: D('<i>fehlt S</i>', 'lacking in S'), 35: D('<i>fehlt S Do</i>', 'lacking in S Do'),
            36: D('poterint <i>Rl Hr;</i> poterunt <i>Ad</i>', 'poterint Rl Hr; poterunt Ad'), 37: D('uel <i>Ad Do</i>', 'uel Ad Do')}},

 {'code': 'ECfRetr', 'n': '20.3', 'page': 646,
  'text': '<b>Sed</b> si infra predictum{1} terminum inueniri non posset, quia in omni friborgo{2} unus erat capitalis, quem uocabant friborges{3} heauod{4}, ipse capitalis <b>sumeret</b> duos de melioribus sui{5} friborgi{6} et de tribus friborgis{7} <b>sibi</b> propinquioribus acciperet de unoquoque capitalem et duos de melioribus <b>uniuscuiusque</b>{8} <b>friborgi</b>{9}, si posset habere{10}, et <b>ita</b>{11}, se duodecimo <b>existente</b>{12}, purgaret{13} se et{14} friborgum{15} suum, si facere posset, de forisfacto et fuga supradicti malefactoris.',
  'notes': {'f:a': FA, 1: D('t. p. <i>Va Ph</i>', 't. p. Va Ph'), 2: D('fritheb. <i>Lb Va;</i> fritheburgo <i>Ph;</i> frithb. <i>Hv Ld;</i> friburgo <i>K</i>', 'fritheb. Lb Va; fritheburgo Ph; frithb. Hv Ld; friburgo K'),
            3: D('frithb. <i>Hv;</i> fritheb. <i>Lb Va;</i> frithes borges <i>Ph</i>', 'frithb. Hv; fritheb. Lb Va; frithes borges Ph'), 4: D('<i>so Va K;</i> heued <i>Cb Hv;</i> heofod <i>Ld;</i> heauot <i>Ph</i>', 'so Va K; heued Cb Hv; heofod Ld; heauot Ph'),
            5: D('suorum frithborgorum <i>Hv</i>', 'suorum frithborgorum Hv'), 6: D('fritheb. <i>Ph Va;</i> frithb. <i>Lb</i>', 'fritheb. Ph Va; frithb. Lb'), 7: D('fritheb. <i>Ph Va;</i> frithb. <i>Hv K Ld;</i> fridb. <i>Lb</i>', 'fritheb. Ph Va; frithb. Hv K Ld; fridb. Lb'),
            8: D('sui <i>Va Ph</i>', 'sui Va Ph'), 9: D('frithb. <i>Hv;</i> fritheb. <i>Ph Va</i>', 'frithb. Hv; fritheb. Ph Va'), 10: D('<i>verb. aus</i> -ret <i>Cb</i>', 'corrected from -ret Cb'), 11: D('inde <i>Va Hv</i>', 'inde Va Hv'),
            12: D('<i>fehlt Hv besser</i>', 'lacking, which is better, in Hv'), 13: D('expurg. <i>ohne</i> se <i>Hv</i>', 'expurg. without se Hv'), 14: D('in <i>Lond</i>', 'in Lond'), 15: D('fridb. <i>Va Ph;</i> frithb. <i>Lb Hv;</i> friðb. <i>Ld</i>', 'fridb. Va Ph; frithb. Lb Hv; friðb. Ld')}},
 {'code': 'ECfRetr', 'n': '20.4', 'page': 646,
  'text': 'Quod{16} si facere non posset, <b>ipse cum friborgo</b>{17} suo damnum restauraret{f:c}{18} de proprio <b>male</b>factoris, quantum duraret{19}; <b>quo deficiente,</b> de suo <b>et friborgi</b>{20} <b>sui perficeret;</b> et erga iusticiam emendarent{21}, secundum quod legaliter iudicatum{22} eis{23} fuisset.',
  'notes': {'f:c': FC, 16: D('Qui <i>Hv;</i> Quid <i>Va K Ld</i>', 'Qui Hv; Quid Va K Ld'), 17: D('frithb. <i>Hv;</i> fridb. <i>Lb Va;</i> fridburgo <i>Ph</i>', 'frithb. Hv; fridb. Lb Va; fridburgo Ph'), 18: D('-uret <i>Va</i>', '-uret Va'), 19: D('distaret <i>Co</i>', 'distaret Co'),
            20: D('fridb. <i>Lb Va Ph;</i> frithb. <i>Hv L</i>', 'fridb. Lb Va Ph; frithb. Hv L'), 21: D('-ret <i>Hv</i>', '-ret Hv'), 22: D('eis iud. <i>Db</i>', 'eis iud. Db'), 23: D('<i>fehlt Cb Hv</i>', 'lacking in Cb Hv')}},
 {'code': 'ECfRetr', 'n': '20.5', 'page': 646,
  'text': '<b>Tandem uero</b> sacramentum, quod non potuerunt <b>ad</b>implere per <b>tres</b>{f:g} <b>friborgos</b>{24} <b>sibi</b> uiciniores, per se{25} ipsos nouem iurarent: sese <b>nullatenus fore</b>{26} <b>culpabiles.</b>',
  'notes': {'f:g': FG, 24: D('-gas <i>Cb;</i> fridb. <i>Lb Va Ph;</i> frithb. <i>Hv</i>', '-gas Cb; fridb. Lb Va Ph; frithb. Hv'), 25: D('semet <i>Lb Va Ph</i>', 'semet Lb Va Ph'), 26: D('esse <i>Cb</i>', 'esse Cb')}},
 {'code': 'ECfRetr', 'n': '20.6', 'page': 646,
  'text': 'Et si quando possent{27} eum recuperare, adducerent <b>illum</b>{28} ad iustitiam{29} aut dicerent iusticie, ubi esset.',
  'notes': {27: D('e. r. p. <i>Hv</i>', 'e. r. p. Hv'), 28: D('<i>fehlt Cb Lb Va Ra Ph Co Db</i>', 'lacking in Cb Lb Va Ra Ph Co Db'), 29: D('iustitiarium <i>Hv</i>', 'iustitiarium Hv')}},
]
