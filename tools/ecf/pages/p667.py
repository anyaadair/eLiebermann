# Liebermann, Gesetze I pp. 666–667: ECf and ECf retr 36,2 (begins p. 666) – 36,4 (36,5 runs on: see p668.py)
D = lambda de, en: (de, en)
FA = D('<i>der, wie nach</i> Ine 21 <i>zum Beweise nähere, Todtschläger</i>', 'the killer, who, as by Ine 21, is nearer to the proof')
FB = D('gesteht', 'confesses')
FC = D('Urtheilfinder', 'judgement-finders')
FDd = D('<i>Umstand des Gerichts, welches jenen hingerichtet hatte (wohl nicht Eideshelfer oder Zeugen, die gegen ihn ausgesagt hatten)</i>', 'the bystanders of the court which had executed him (probably not oath-helpers or witnesses who had testified against him)')
FE = D('<i>Klagepfand, als Strafgeld dem Richter für falsche Klage verfallen</i>', 'the pledge given with the claim, forfeit to the judge as a fine for a false claim')
FF = D('<i>vgl.</i> 2, 9. 8, 2. <i>Der weltliche Richter hat bereits</i> (36, 2) <i>Pfand empfangen</i>', 'cf. 2, 9. 8, 2. The secular judge has already (36, 2) received a pledge')
NP = lambda ks: {k: 667 for k in ks}
CLAUSES = [
 {'code': 'ECf', 'n': '36.2', 'page': 666, 'pages': [667],
  'text': 'Et si{27} isti decem et octo uelint{28} derationari{29} cum illo qui prius fecerat clamorem et dederat{30} [[pb:667]]uadimonium{1}, det quisque eorum uadimonium cum gladio et inueniat plegios{2} tales, qui possint reddere forisfacturam{3}, id est weram{4} suam, si non possint{5} dirationari{6}. Et tunc interfector det uadimonium suum et inueniat plegios, quod iuste interfectus est{7} et iuste iacet inter latrones secundum legem sicut latro.',
  'notepages': NP(range(1, 8)),
  'notes': {27: D('<i>fehlt Cl</i>', 'lacking in Cl'), 28: D('uellent <i>Hk S;</i> uolunt <i>Hr</i>', 'uellent Hk S; uolunt Hr'), 29: D('dir. <i>Hr;</i> disrationare <i>S</i>', 'dir. Hr; disrationare S'), 30: D('-rit <i>Hr</i>', '-rit Hr'),
            1: D('uad., d. q. e. <i>überspringt Cl</i>', 'Cl skips uad., d. q. e.'), 2: D('t. p. <i>Cl</i>', 't. p. Cl'), 3: D('-factum <i>Hk</i>', '-factum Hk'),
            4: D('gue. <i>Hk;</i> guerram <i>Rl;</i> war. <i>S;</i> werram <i>Hr Cl</i>', 'gue. Hk; guerram Rl; war. S; werram Hr Cl'), 5: D('<i>geändert</i> -sunt <i>Rl;</i> -sunt <i>S</i>', 'altered to -sunt Rl; -sunt S'), 6: D('der. <i>Hk Cl;</i> -re <i>S</i>', 'der. Hk Cl; -re S'), 7: D('sit <i>Cl</i>', 'sit Cl')}},
 {'code': 'ECf', 'n': '36.3', 'page': 667,
  'text': 'Et tunc primum{8} dicat{f:a}, quo latrocinio et qua ratione interfectus sit. Et si cognouerit{f:b}{9}, quod fuit captus uiuus, nominet iusticiarium et iudices{f:c} et testes{f:d} de uicinis legales. Et si ipsi warantizauerint{10} eum, quod iuste sit{11} facta iusticia de eo pro{12} suo latrocinio, quietus erit interfector; et ipsi qui fecerunt{13} clamorem, dabunt{14} sua{15} uadimonia{f:e}.',
  'notes': {'f:a': FA, 'f:b': FB, 'f:c': FC, 'f:d': FDd, 'f:e': FE, 8: D('primo <i>Cl</i>', 'primo Cl'), 9: D('-uit <i>Cl</i>', '-uit Cl'),
            10: D('-zia. <i>Rl;</i> -zabunt <i>S;</i> guarentizent <i>Hk;</i> warent. <i>Hr</i>', '-zia. Rl; -zabunt S; guarentizent Hk; warent. Hr'), 11: D('f. sit <i>Hk Cl</i>', 'f. sit Hk Cl'), 12: D('super <i>Cl</i>', 'super Cl'),
            13: D('-rat <i>Hk</i>', '-rat Hk'), 14: D('emendent <i>S;</i> emendet <i>Hk</i>', 'emendent S; emendet Hk'), 15: D('u. sua <i>Hk</i>', 'u. sua Hk')}},
 {'code': 'ECf', 'n': '36.4', 'page': 667,
  'text': 'Quodsi interfectori{16} defecerint iudices{f:c} et testes{f:d}, et diracionatum{17} fuerit, quod iniuste sit{18} interfectus, interfector dabit uadimonium iusticie{f:f} episcopi et fideiussores.',
  'notes': {'f:c': FC, 'f:d': FDd, 'f:f': FF, 16: D('sibi <i>Hk Hr;</i> ibi <i>S</i>', 'sibi Hk Hr; ibi S'), 17: D('derat. <i>Hk</i>', 'derat. Hk'), 18: D('i. sit <i>S; fehlt Hr</i>', 'i. sit S; lacking in Hr')}},

 {'code': 'ECfRetr', 'n': '36.2', 'page': 666, 'pages': [667],
  'text': '<b>Quod</b>si isti decem et octo{32} uelint dirationari{33} cum illo qui <sp>primitus</sp> clamorem fecerat{34} et <b>qui</b>{35} uadimonium de[[pb:667]]derat, det <b>unus</b>quisque eorum uadimonium{1} <b>suum</b> cum gladio et <b>postea</b> inueniat plegios tales, qui possint reddere forisfacturam, id est were{2} suam{3}, <b>nisi</b> possint{4} dirationari{5} <b>quod dicunt.</b> Tunc <b>demum</b>{6} interfector suum{7} det uadimonium et inueniat plegios{8}, quod iuste interfectus est{9} et <b>merito</b> iacet inter latrones secundum legem sicut latro.',
  'notepages': NP(range(1, 10)),
  'notes': {32: D('XVI <i>Va;</i> XVIII <i>Hv;</i> nouendecim <i>nur Hv’s Ed. Savile</i>', 'XVI Va; XVIII Hv; nouendecim only Hv’s editor Savile'), 33: D('-tiocinari <i>Cb Lb</i>', '-tiocinari Cb Lb'),
            34: D('-rit et qui uadium dederit <i>Hv</i>', '-rit et qui uadium dederit Hv'), 35: D('<i>fehlt Lb Ph Db Lond</i>', 'lacking in Lb Ph Db Lond'),
            1: D('uadium <i>Hv;</i> suum uadium <i>Lond</i>', 'uadium Hv; suum uadium Lond'), 2: D('werre <i>Hv</i>', 'werre Hv'), 3: D('suum <i>Hv Ph Lond</i>', 'suum Hv Ph Lond'), 4: D('possunt <i>Hv</i>', 'possunt Hv'),
            5: D('-tiocinari <i>Cb Lb</i>', '-tiocinari Cb Lb'), 6: D('deinde <i>Hv</i>', 'deinde Hv'), 7: D('det s. u. suum <i>Cb; fehlt Db;</i> det s. uadium <i>Hv</i>', 'det s. u. suum Cb; lacking in Db; det s. uadium Hv'), 8: D('-ium <i>Hv</i>', '-ium Hv'), 9: D('sit <i>Hv</i>', 'sit Hv')}},
 {'code': 'ECfRetr', 'n': '36.3', 'page': 667,
  'text': 'Et tunc{10} primum <b>ostendat,</b> quo{11} latrocinio et qua ratione interfectus sit{12}. <b>Quod</b>si <b>re</b>cognouerit, quod uiuus captus <b>sit,</b> nominet iusticiarium{13} et iudices{14} et de uicinis testes{15} legales. <b>Qui</b> si warantizauerint{16}, quod <b>recte</b>{17} sit{18} facta iusticia de <b>ipso secundum</b> <sp>suum</sp>{19} latrocinium, quietus erit{20} interfector <b>illius;</b> ipsi <b>uero</b> qui clamorem{21} fecerant, <b>emendent</b> sua uadimonia.',
  'notes': {'f:a': FA, 'f:b': FB, 'f:c': FC, 'f:d': FDd, 'f:e': FE, 10: D('tum <i>Lb Va; fehlt K, wo</i> primo', 'tum Lb Va; lacking in K, where primo'), 11: D('quod <i>Hv</i>', 'quod Hv'), 12: D('est <i>Lond</i>', 'est Lond'),
            13: D('-ciam <i>Hv</i>', '-ciam Hv'), 14: D('-cem <i>Lond</i>', '-cem Lond'), 15: D('l. t. <i>Hv</i>', 'l. t. Hv'), 16: D('-rit <i>Va</i>', '-rit Va'), 17: D('sit r. i. f. de illo <i>Hv</i>', 'sit r. i. f. de illo Hv'),
            18: D('f. sit <i>Lond</i>', 'f. sit Lond'), 19: D('<i>fehlt Lond</i>', 'lacking in Lond'), 20: D('sit <i>Lb Va Ph</i>', 'sit Lb Va Ph'), 21: D('uadimonia dederunt <i>Hv</i>', 'uadimonia dederunt Hv')}},
 {'code': 'ECfRetr', 'n': '36.4', 'page': 667,
  'text': 'Quodsi{22} interfectori defecerint iudices et testes, et dirationatum fuerit, quod [in]iuste{23} sit interfectus, interfector dabit uadimonium{24} iusticie episcopi et fideiussores <b>inueniet</b>{25} <b>rectum prosequendi.</b>',
  'notes': {'f:c': FC, 'f:d': FDd, 'f:f': FF, 22: D('Super <i>statt</i> Quodsi — defecerint <i>Lond</i>', 'Super instead of Quodsi — defecerint Lond'), 23: D('iuste <i>Hss;</i> iniuste <i>nur Ph</i>', 'iuste MSS; iniuste only Ph'),
            24: D('uadium <i>Hv</i>', 'uadium Hv'), 25: D('<i>fehlt Hv</i>', 'lacking in Hv')},
  'editorial': ['The square brackets in “[in]iuste” are Liebermann’s: the manuscripts read “iuste”, only Ph “iniuste” (note 23).']},
]
