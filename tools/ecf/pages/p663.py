# Liebermann, Gesetze I pp. 662–663: ECf 34,2b (begins p. 662) – 34,3; ECf retr 34,2b–34,2e (retr 34,3 runs on: see p664.py)
D = lambda de, en: (de, en)
STAR3 = D('cui cognomen erat Hirenside, id est Latus ferreum <i>fügt zu Pl S;</i> Irenes. hoc est L. f. <i>fügt zu Lond; beide vielleicht aus Will. Malm.</i> II 179', 'Pl S add cui cognomen erat Hirenside, id est Latus ferreum; Lond adds Irenes. hoc est L. f.; both perhaps from Will. Malm. II 179')
STAR = D('Harefot (Herewod <i>K</i>), filius Chnuti et Elwyne <i>Lond;</i> Haral. <i>S Hr</i>', 'Harefot (Herewod K), filius Chnuti et Elwyne Lond; Haral. S Hr')
STAR2 = D('qui XVI (septem decim <i>Co</i>) annis regnauit† et <i>fügt zu Lond</i>', 'Lond adds qui XVI (septem decim Co) annis regnauit† et')
FG = D('9 <i>Monat</i>, 1 <i>Woche</i>', '9 months, 1 week')
FH62 = D('<i>fünf Kämpfe zählt auch</i> Annal. Anglosax.', 'the Annal. Anglosax. also count five battles')
FA = D('<i>ob richtig?</i>', 'correct?')
FB = D('<i>anders</i> Flor. Wigorn.', 'differently Flor. Wigorn.')
FC = D('<i>Cnuts Vaterschaft bezweifeln</i> Ann. Anglosax., Flor., Encom. Emmae', 'Cnut’s paternity is doubted by the Ann. Anglosax., Florence, and the Encom. Emmae')
FD = D('<i>vielmehr</i> IV', 'rather IV')
FE = D('<i>nicht (mit Hk und einer Retr.-Classe)</i> Ricardi [II.] <i>zu bessern, laut des Irrthums auch</i> 35, 2. Ducem <i>setzt Retr., weil im</i> 12. <i>Jh. der Grafentitel für die Normandie verschwand.</i>',
       'not to be corrected (with Hk and one class of the Retr.) to Ricardi [II], given the same error also at 35, 2. The Retr. puts ducem because in the 12th century the title of count for Normandy disappeared.')
FEE = D('<i>erst Heinrich III. nannte</i> 1239 <i>seinen Thronfolger wieder</i> Eadward', 'not until 1239 did Henry III again name his heir Edward')
FF = D('<i>vielmehr</i> III', 'rather III')
FG3 = D('4 + 38 + 1 + 18 + 5 + 2 = 68', '4 + 38 + 1 + 18 + 5 + 2 = 68')
FH = D('<i>wie oben</i> 34, 1<i>b</i>', 'as above, 34, 1b')
FI = D('<i>den Retr. beeinflusst vielleicht Will. Malm.</i> Reg. II 183: Cnut leges ab antiquis regibus, et maxime Ethelredo, latas obseruari precepit, in quarum custodiam etiam nunc sub nomine regis Edwardi iuratur, non quod ille statuerit, sed quod obseruarit',
       'the Retr. is perhaps influenced by Will. Malm., Reg. II 183: Cnut leges ab antiquis regibus, et maxime Ethelredo, latas obseruari precepit, in quarum custodiam etiam nunc sub nomine regis Edwardi iuratur, non quod ille statuerit, sed quod obseruarit')
MARG = lambda w, d: f'Liebermann prints “{w}” and gives in the outer margin of the ECf retr column the dates {d}.'
WHOLE = lambda s: f'The note{"s" if len(s) > 4 else ""} {s} {"are" if len(s) > 4 else "is"} printed across the whole page; given with both columns.'
CLAUSES = [
 {'code': 'ECf', 'n': '34.2b', 'page': 662, 'pages': [663],
  'text': '{20}Post {21}Ædelredum{22} filius eius Eadmundus{***} IX{23} fere{f:g} mensibus* regnauit, in quibus uiriliter quinquies{f:h} contra Danorum regem Chnutum{24} dimicauit. Peracto uero{25} ultimo bello, concordiam inter se fecerunt regnumque{26} Anglie diuise[[pb:663]]runt{1}: dimidium Chnuto{2} et dimidium Eadmundo{3}, ea conditione{4}, ut{5}, si{f:a} quis eorum superuiueret, alius{6} totum possideret, nec{f:b} interim aliquis eorum coronaretur. Sed hac{7} conuentione, cunctis primatibus{8} Anglie consentientibus, firmata{9}, post{10} primum{f:a} mensem Eadmundus ex hac luce, pro{11} dolor, subtrahitur.',
  'notepages': {k: 663 for k in ['f:a', 'f:b', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]},
  'notes': {'***': STAR3, 'f:g': FG, 'f:h': FH62, 'f:a': FA, 'f:b': FB,
            20: D('Regnum Eadmundi [Ed. <i>S</i>] Hireneside [Hyrn. <i>Pl</i>], filii [<i>fehlt Pl</i>] Ældredi regis [<i>fehlt S</i>] <i>überschr. Pl S</i>', 'heading in Pl S: Regnum Eadmundi [Ed. S] Hireneside [Hyrn. Pl], filii [lacking in Pl] Ældredi regis [lacking in S]'),
            21: D('hunc <i>fügt zu Hk</i>', 'Hk adds hunc'), 22: D('Ad. <i>Rl;</i> Ed. <i>Hk;</i> Ældr. <i>S</i>', 'Ad. Rl; Ed. Hk; Ældr. S'), 23: D('f. IX <i>Hk</i>', 'f. IX Hk'), 24: D('Can. <i>Hk</i>', 'Can. Hk'),
            25: D('quinto b. ul. <i>Hk</i>', 'quinto b. ul. Hk'), 26: D('regnum quoque <i>S</i>, Diuisio regni inter Chnutum et Edmundum <i>überschr. S</i>', 'regnum quoque S, with the heading Diuisio regni inter Chnutum et Edmundum S'),
            1: D('dimis. <i>Hr</i>', 'dimis. Hr'), 2: D('Can. <i>Hk</i>', 'Can. Hk'), 3: D('Ed. <i>meist Hk</i>', 'Ed. mostly Hk'), 4: D('diuisione <i>Hk</i>', 'diuisione Hk'), 5: D('quod <i>Hk Hr</i>', 'quod Hk Hr'),
            6: D('eorum <i>fügt zu S</i>', 'S adds eorum'), 7: D('<i>fehlt Rl S</i>', 'lacking in Rl S'), 8: D('A. p. <i>Hk</i>', 'A. p. Hk'), 9: D('form. <i>Hk</i>', 'form. Hk'), 10: D('Edm. po. pr. me. <i>Hk</i>', 'Edm. po. pr. me. Hk'), 11: D('p. d. <i>fehlt Hr</i>', 'p. d. lacking in Hr')},
  'editorial': ['Liebermann prints a small raised asterisk after “mensibus” (not one of his starred notes) and gives in the outer margin of the ECf retr column the date 1016.',
                'Liebermann’s numbering of the notes in the ECf column starts again at 1 on p. 663: the notes 1–11 are on p. 663, the notes 20–26 on p. 662.',
                'Liebermann puts his note a both after “si” and after “primum”.',
                WHOLE('(***)')]},
 {'code': 'ECf', 'n': '34.2c', 'page': 663,
  'text': '{12}Et{13} Chnutus{14} totum{15} suscepit Anglie{16} principatum{17}; regnauitque fere X{18} et VIII annis†.',
  'notes': {12: D('Regnum Chnuti regis <i>überschreibt Pl S</i>', 'Pl S head it Regnum Chnuti regis'), 13: D('<i>fehlt Hk S Hr</i>', 'lacking in Hk S Hr'), 14: D('uero <i>fügt zu S Hr;</i> Can. <i>Hk</i>', 'S Hr add uero; Can. Hk'),
            15: D('su. totius <i>Hk</i>', 'su. totius Hk'), 16: D('regnum A. et princ. <i>Hr</i>', 'regnum A. et princ. Hr'), 17: D('regnum <i>S</i>', 'regnum S'), 18: D('XXVII <i>Hr</i>', 'XXVII Hr')},
  'editorial': [MARG('†', '†1016–35')]},
 {'code': 'ECf', 'n': '34.2d', 'page': 663,
  'text': '{19}Quo mortuo, Haroldus{*}, falso{f:c} pene ab omnibus putatus{20} filius{21} eius, successit et{22} quinque{f:d} annis regnauit††.',
  'notes': {'*': STAR, 'f:c': FC, 'f:d': FD, 19: D('Regnum Haraldi <i>überschr. Pl S</i>', 'Pl S head it Regnum Haraldi'), 20: D('f. e. p. <i>Hk</i>', 'f. e. p. Hk'), 21: D('f. e. <i>fehlt S</i>', 'f. e. lacking in S'),
            22: D('ei annisque XV r. <i>Hr;</i> et <i>fehlt S</i>', 'ei annisque XV r. Hr; et lacking in S')},
  'editorial': [MARG('††', '††1035–39'), WHOLE('(*)')]},
 {'code': 'ECf', 'n': '34.2e', 'page': 663,
  'text': '{23}Post quem{24} Hardecnutus{25}, filius Chnuti{2} ex{27} Alueua{28}-Emma{29}, sorore{30} Rodberti{f:e}{31} comitis Normannorum{32} et matre{33} Eadwardi{34} regis{35}, duobus{f:f} annis XII ebdomadibus minus regnauit†. Et sic completi sunt LX{36} et VIII anni{f:g} dimissis legibus.',
  'notes': {'f:e': FE, 'f:f': FF, 'f:g': FG3, 2: D('Can. <i>Hk</i>', 'Can. Hk'),
            23: D('Regnum Hardechnuti, filii Chnuti regis <i>überschr. Pl S</i>', 'Pl S head it Regnum Hardechnuti, filii Chnuti regis'), 24: D('quam <i>S</i>', 'quam S'),
            25: D('-chn. <i>Rl S;</i> Chuti Aluene etiam sororis <i>Hr</i>', '-chn. Rl S; Chuti Aluene etiam sororis Hr'), 27: D('et <i>Hk</i>', 'et Hk'), 28: D('Alfu. <i>S;</i> Alueue <i>Hk; fehlt Rl</i>', 'Alfu. S; Alueue Hk; lacking in Rl'),
            29: D('Emme <i>Hk;</i> Iunia <i>S</i> [<i>statt</i> Imma]', 'Emme Hk; Iunia S [instead of Imma]'), 30: D('sororis <i>Hk</i>', 'sororis Hk'), 31: D('<sp>Ricardi</sp> <i>Hk</i>', 'Ricardi Hk'), 32: D('-nnie <i>Rl S</i>', '-nnie Rl S'),
            33: D('matris <i>Rl Hk Hr</i>', 'matris Rl Hk Hr'), 34: D('r. Ædw. <i>Hk</i>', 'r. Ædw. Hk'), 35: D('<i>fehlt Hr</i>', 'lacking in Hr'), 36: D('XLVII a. et fere duo menses <i>Hk</i>', 'XLVII a. et fere duo menses Hk')},
  'editorial': ['After “Chnuti” Liebermann prints the note number 2 (“Can. Hk”, as for “Chnuto” in 34, 2b), and there is no note 26 in the ECf column of this page; it is linked here as printed.',
                MARG('†', '†1039–42') + ' Beside the end of this sentence in the ECf retr column he gives the dates 975–1042, for the 68 years.']},
 {'code': 'ECf', 'n': '34.3', 'page': 663,
  'text': '{37}Sed{38} postquam Eadwardus{39} rex uenit ad regnum, consilio baronum regni legem{f:h} dimissam{40}, quia honesta uidebatur eis, et{41} quia auus eius eam constituerat, fecit eam reparare et confirmare; et sic uocata{f:i} est lex regis Ædwardi, que{42} dimissa erat a morte Eadgari{43}{**}, aui sui, usque ad suum{44} tempus.',
  'notes': {'f:h': FH, 'f:i': FI, '**': STAR2,
            37: D('De legum reparacione et confirmacione <i>Rubrik Hr</i>', 'rubric in Hr: De legum reparacione et confirmacione'), 38: D('Hec <i>Hr</i>', 'Hec Hr'), 39: D('Ædw. <i>Hk S</i>', 'Ædw. Hk S'), 40: D('omi. <i>S</i>', 'omi. S'),
            41: D('set <i>Hr</i>', 'set Hr'), 42: D('prius <i>fügt zu S Hr</i>', 'S Hr add prius'), 43: D('Edg. <i>Hk</i>', 'Edg. Hk'), 44: D('t. s. <i>S</i>', 't. s. S')},
  'editorial': ['Beside the beginning of this clause in the ECf retr column Liebermann gives the date 1042 in the margin, and beside the starred note (**) the dates †959–75.', WHOLE('(**)')]},

 {'code': 'ECfRetr', 'n': '34.2b', 'page': 662, 'pages': [663],
  'text': 'Post{29} Ethelredum{30} <b>uero</b> Eadmundus{21}{***}, filius eius, regnauit fere nouem mensibus*, in quibus uiriliter contra Danorum regem Chnutum{31} quinquies dimicauit. Ultimo uero bello peracto, concordes <b>ad</b>{3} <b>inuicem effecti</b>{32} sunt, regnumque <b>per medium</b>{33} diuiserunt; <b>et (una</b>{34}<b>)</b> <sp>medietas</sp> [[pb:663]]Anglie Cnuto{1/663}, <sp>medietas</sp>{2/663} <b>altera cessit</b> Eadmundo{3/663}, <b>eo tenore</b> ut{4/663}, si quis eorum <b>alterum</b> superuiueret, <b>regnum superstes</b> totum possideret, nec interim{5/663} <b>alteruter</b> coronaretur. Firmata{6/663} <b>igitur taliter, uniuersis</b> Anglie primatibus{7/663} <sp>assensum</sp> <b>prebentibus, inter</b> se conuentione{8/663}, primum{9/663} post mensem{10/663} Eadmundus ex hac luce, pro dolor, subtrahitur.',
  'notepages': {k: 663 for k in ['f:a', 'f:b'] + [f'{i}/663' for i in range(1, 11)]},
  'notes': {'***': STAR3, 'f:g': FG, 'f:h': FH62, 'f:a': FA, 'f:b': FB,
            29: D('ipsum <i>fügt zu Lond</i>', 'Lond adds ipsum'), 30: D('Aldr. <i>Hv K;</i> Aeldr. <i>Co;</i> Ath. <i>Lb;</i> Adel. <i>übr.</i>', 'Aldr. Hv K; Aeldr. Co; Ath. Lb; Adel. the others'), 21: D('Ed. <i>stets Cb</i>', 'Ed. always Cb'),
            31: D('Chu. <i>Cb;</i> Cn. <i>Lb Ph</i>', 'Chu. Cb; Cn. Lb Ph'), 3: D('<i>fehlt Hv</i>', 'lacking in Hv'), 32: D('facti <i>Ph</i>', 'facti Ph'), 33: D('dimid. <i>Hv</i>', 'dimid. Hv'), 34: D('<i>fehlt Cb Lb Hv Lond</i>', 'lacking in Cb Lb Hv Lond'),
            '1/663': D('<i>fehlt Hv;</i> Chuto <i>Cb</i>', 'lacking in Hv; Chuto Cb'), '2/663': D('et a. m. <i>Hv</i>', 'et a. m. Hv'), '3/663': D('Ed. <i>Cb</i>', 'Ed. Cb'), '4/663': D('quod <i>Hv</i>', 'quod Hv'),
            '5/663': D('<i>fehlt Va K</i>', 'lacking in Va K'), '6/663': D('Firmatis <i>Hv</i>', 'Firmatis Hv'), '7/663': D('inter se <i>fügt zu Cb</i>', 'Cb adds inter se'), '8/663': D('-onem factam, post <i>Hv</i>', '-onem factam, post Hv'),
            '9/663': D('-mus <i>Va;</i> primo <i>Co; fehlt Hv</i>', '-mus Va; primo Co; lacking in Hv'), '10/663': D('messem <i>Lond;</i> rex <i>fügt zu Cb</i>', 'messem Lond; Cb adds rex')},
  'editorial': ['Liebermann’s numbering of the notes in the ECf retr column starts again at 1 on p. 663: the notes 1–10 to the part of this clause on p. 663 are distinct from the notes on p. 662.',
                'Liebermann prints a small raised asterisk after “mensibus” (not one of his starred notes) and gives in the outer margin the date 1016.', WHOLE('(***)')]},
 {'code': 'ECfRetr', 'n': '34.2c', 'page': 663,
  'text': '{11}Cnutus totum{13} <b>deinde</b> suscepit{14} Anglie principatum; regnauitque fere <sp>octodecim</sp> annis†.',
  'notes': {11: D('<i>roth Cb;</i> Chn. <i>Va Co;</i> Chn. uero inde to. <i>Hv</i>', 'in red Cb; Chn. Va Co; Chn. uero inde to. Hv'), 13: D('d. t. <i>Cb;</i> dei. su. to. <i>Lond</i>', 'd. t. Cb; dei. su. to. Lond'),
            14: D('regnum su. A.; regnauitque <i>Hr</i>', 'regnum su. A.; regnauitque Hr')},
  'editorial': ['There is no note 12 in the ECf retr column of this page: Liebermann’s numbering goes from 11 to 13.', MARG('†', '†1016–35')]},
 {'code': 'ECfRetr', 'n': '34.2d', 'page': 663,
  'text': 'Quo <b>defuncto,</b> Haraldus{15}{*}, falso{16} pene{17} ab omnibus putatus filius{18}, successit{19} et quinque annis regnauit††.',
  'notes': {'*': STAR, 'f:c': FC, 'f:d': FD, 15: D('Harol. <i>Cb</i>', 'Harol. Cb'), 16: D('<i>fehlt Lond;</i> f. p. <i>fehlt Hv, wo</i> illius', 'lacking in Lond; f. p. lacking in Hv, where illius'),
            17: D('<i>so Cb;</i> fi. (pius <i>Lb Va Ph</i>) pe. ab o. pu. s. <i>übr.</i>', 'so Cb; fi. (pius Lb Va Ph) pe. ab o. pu. s. the others'), 18: D('<i>aus K Co; fehlt Lb</i>', 'from K Co; lacking in Lb'), 19: D('regnum suscepit <i>Hv</i>', 'regnum suscepit Hv')},
  'editorial': [MARG('††', '††1035–39'), WHOLE('(*)')]},
 {'code': 'ECfRetr', 'n': '34.2e', 'page': 663,
  'text': 'Post quem Hardecnutus{20}, filius Chnuti <b>et</b> Eluiue{21}-<sp>Emme</sp>, sororis Rodberti{22} Normannorum{23} <b>ducis</b>{f:e} et <sp>matris</sp> regis{24} <b>ultimi</b>{f:ee} Eadwardi{25}, regnauit† duobus annis, ebdomadibus{26} duodecim minus. <sp>Sicque</sp> completi sunt LXVIII{27} anni, <b>in quibus</b> lege <b>predicte</b>{28} <b>fuerant</b>{29} <b>penitus</b>{30} <b>pretermisse.</b>',
  'notes': {'f:e': FE, 'f:ee': FEE, 'f:f': FF, 'f:g': FG3,
            20: D('-chn. <i>Va Hv; die Buchstaben</i> cnu <i>roth Cb</i>', '-chn. Va Hv; the letters cnu in red Cb'), 21: D('<i>fehlt Cb Lond;</i> id est <i>fügt zu Hv</i>', 'lacking in Cb Lond; Hv adds id est'), 22: D('<sp>Ricardi</sp> <i>Lb Va</i>', 'Ricardi Lb Va'),
            23: D('<i>fehlt Va</i>', 'lacking in Va'), 24: D('Edw. r. ult. <i>Cb</i>', 'Edw. r. ult. Cb'), 25: D('id est sancti <i>fügt zu Co</i>', 'Co adds id est sancti'), 26: D('<i>so Cb;</i> -adis <i>übr.</i>', 'so Cb; -adis the others'),
            27: D('quadraginta octo <i>Hv</i>', 'quadraginta octo Hv'), 28: D('<i>aus Cb Lb Hv</i>', 'from Cb Lb Hv'), 29: D('-runt <i>Lb;</i> pret. erant <i>Hv</i>', '-runt Lb; pret. erant Hv'), 30: D('<i>fehlt Hr</i>', 'lacking in Hr')},
  'editorial': [MARG('regnauit†', '†1039–42') + ' Beside “pretermisse” he gives the dates 975–1042, for the 68 years.',
                'Liebermann’s note 30 in this column reads “fehlt Hr”; Hr is a manuscript of ECf, not of the Retractator, so this may be a misprint for Hv.']},
]
