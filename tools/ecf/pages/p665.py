# Liebermann, Gesetze I p. 665: ECf and ECf retr 35,1a–35,1e
D = lambda de, en: (de, en)
FA = D('35, 1<i>a muss, da</i> quem <i>in</i> 35, 1<i>b den Aetheling meint, Parenthese sein und bezeugt, weil ohne Zusammenhang mit</i> Leges <i>oder dem Bekenner, des Verfs. Interesse für diese</i> terram <i>oder</i> Limézy. <i>Christine erhielt alle oder die meisten Güter (nicht</i> 1058—65, <i>wie Verf. meint) von Wilhelm I. und starb</i> 1095—1100. <i>Ihre Güter erhielt Limézy</i> 1086—93. <i>Sie liegen (ausser Bradwell, Oxfordshire) in Warwickshire, und dorthin, nach Coventry, verlegte Bischof Robert von Limézy</i> 1102 <i>seine Kathedrale. Rudolf starb nach</i> 1114 <i>und vor</i> 1131. <i>Vgl. mein</i> Über Edw. Conf. 10 <i>ff.</i> 21; <i>dazu Round</i> Hist. of Hamps. I 410; Cal. of doc. in France I <i>n.</i> 1278, <i>wo eine von Rudolf bezeugte Urkunde a.</i> 1102—28 <i>steht</i>',
       '35, 1a must be a parenthesis, since quem in 35, 1b means the Ætheling; and, having no connection with the Leges or the Confessor, it attests the author’s interest in this terram or in Limésy. Christine received all or most of her estates (not 1058–65, as the author thinks) from William I and died 1095–1100. Her estates went to Limésy 1086–93. They lie (except Bradwell, Oxfordshire) in Warwickshire, and it was there, to Coventry, that Bishop Robert of Limésy moved his cathedral in 1102. Rudolf died after 1114 and before 1131. Cf. my Über Edw. Conf. 10 ff. 21; also Round, Hist. of Hamps. I 410; Cal. of doc. in France I no. 1278, where there is a charter of 1102–28 witnessed by Rudolf')
FB = D('Eadward Ætheling', 'Edward Ætheling')
FC = D('<i>Vatersbruder</i>', 'father’s brother')
FDd = D('<i>lebte noch nach</i> 1126; <i>Stubbs</i> Will. Malm. II <i>p.</i> cxiv', 'still alive after 1126; Stubbs, Will. Malm. II p. cxiv')
FE = D('<i>diese Absicht combinirt vielleicht Verf. nur; zum</i> Æþeling <i>war Eadgar als eines Königs legitimer Sohnessohn (nicht Sohn) geboren; Ernennung dazu mit daraus folgendem Thronfolgeanspruch (den Zeitgenossen vielmehr aus der Geburt ableiten) erfindet wohl der Verf., wenn er nicht, wie aus dem Folgenden wahrscheinlicher, blosses Nennen meint. [Nicht etwa die Verwandtschaft mit dem ‘ernennenden’ Bekenner will Verf., ‘gleichgültig gegen Abstammung von anderem König’ (HECK) betonen]</i>',
       'the author perhaps only infers this intention; Edgar was born an Æþeling as a king’s legitimate grandson (not son); the author probably invents a nomination to it, with a resulting claim to the succession (which contemporaries rather derive from birth), unless he means mere naming, as is more likely from what follows. [The author does not mean to stress the relationship with the ‘nominating’ Confessor, ‘indifferent to descent from another king’ (HECK)]')
FF = D('<i>Altfranz.</i> doncel; <i>vgl. Littré</i> damoiseau; <i>Skeat</i> damsel. <i>Laut Ducange kann</i> domicellus: Königssohn, <i>doch nicht bloss ihn, bedeuten. — Zum Retr. setzt Co</i> id est damisel <i>mit männlichem Sinn; sonst ist es im Mittelenglischen, wie jetzt</i> damsel, <i>nur Femininum:</i> Jungfer',
       'Old French doncel; cf. Littré, damoiseau; Skeat, damsel. According to Ducange domicellus can mean king’s son, but not only that. — In the Retr. Co adds id est damisel, in a masculine sense; otherwise in Middle English it is, like damsel now, only feminine: maiden')
FFF = D('<i>vgl. Retr.</i> 30, 4<i>a</i>', 'cf. Retr. 30, 4a')
FG = D('<i>wohl</i> Südengland (<i>nicht mit Coenwulf von Mercien</i> ganz England; <i>Birch</i> Cart. Sax. 288), <i>wie o.</i> 33', 'probably southern England (not, as with Coenwulf of Mercia, all England; Birch, Cart. Sax. 288), as above, 33')
FH = D('<i>das Suffix ist in</i> æþeling <i>nur</i> -ing <i>nicht (wie in</i> hinderling) -ling; <i>den Irrthum des Verfassers veranlasste vielleicht</i> [ge]lic: similitudo <i>oder</i> likning: Abbild. <i>Da Verf. damaliges</i> hinderling (entartet, niedrig, unecht), <i>das auch bei Orm vorkommt, aus Exeter citirt, so hörte er dort Gebürtige; es lebt noch in Devonshire.</i>',
       'the suffix in æþeling is only -ing, not (as in hinderling) -ling; the author’s error was perhaps caused by [ge]lic: similitudo, or likning: image. Since the author quotes the hinderling of his day (degenerate, base, spurious), which also occurs in Orm, from Exeter, he heard people born there; it still lives in Devonshire.')
FI = D('<i>Retr. denkt irrig an</i> hind (rückwärts) <i>oder</i> hinder (hinterer)', 'the Retr. wrongly thinks of hind (backwards) or hinder (rear)')
LOND = D('Item <sp>bonus</sp> rex Edw. dedit C. predicte te. <i>Lond</i>', 'Item bonus rex Edw. dedit C. predicte te. Lond')
CLAUSES = [
 {'code': 'ECf', 'n': '35.1a', 'page': 665,
  'text': '— Cui{f:a} Cristine{1} rex Eadwardus{2} dedit terram quam habuit postea{3} Radulfus de Limisei{4} —.',
  'notes': {'f:a': FA, 1: D('Christiane <i>S Cl</i>', 'Christiane S Cl'), 2: D('Ed. <i>Hk</i>', 'Ed. Hk'), 3: D('<i>fehlt Cl</i>', 'lacking in Cl'), 4: D('Limeseia <i>Hk S;</i> Limes’ <i>Hr;</i> Lyndesey <i>Cl</i>', 'Limeseia Hk S; Limes’ Hr; Lyndesey Cl')}},
 {'code': 'ECf', 'n': '35.1b', 'page': 665,
  'text': 'Propter quem{f:b} misit rex{5} Eadwardus, auunculus{f:c} eius, et fecit eum{6} ad se uenire. Ipse{f:b} autem et uxor eius non longo{7} tempore uixerunt post aduentum eorum. Eadgarum{f:d} uero{8}, filium eius{9}, rex{10} Eadwardus secum retinuit et nutriuit pro filio.',
  'notes': {'f:b': FB, 'f:c': FC, 'f:d': FDd, 5: D('<i>fehlt Hk</i>', 'lacking in Hk'), 6: D('ad se eum <i>Hk;</i> se ad eum <i>Hr</i>', 'ad se eum Hk; se ad eum Hr'), 7: D('multo <i>S</i>', 'multo S'),
            8: D('<i>fehlt Hk S;</i> autem <i>Cl</i>', 'lacking in Hk S; autem Cl'), 9: D('eorum <i>S</i>', 'eorum S'), 10: D('r. E. <i>fehlt Hk S</i>', 'r. E. lacking in Hk S')},
  'editorial': ['Beside this clause, in the outer margin of the ECf retr column, Liebermann gives the date †1057 (the Ætheling’s death).']},
 {'code': 'ECf', 'n': '35.1c', 'page': 665,
  'text': 'Et{11} quia{f:e} heredem{12} putabat{13} eum facere{14}, nominauit{15} aþeling{16}, quod nos{5} dicimus domicellum{f:f}, sed nos de pluribus, quia filios baronum uocamus domicellos, Angli autem{17} nullum{18} preter filios{19} regum{20}.',
  'notes': {'f:e': FE, 'f:f': FF, 5: D('<i>fehlt Hk</i>', 'lacking in Hk'), 11: D('Quia uero her. <i>S</i>', 'Quia uero her. S'), 12: D('<i>fehlt Cl;</i> p. f. e. h. <i>Hr</i>', 'lacking in Cl; p. f. e. h. Hr'), 13: D('-auit <i>Hk</i>', '-auit Hk'),
            14: D('regem <i>fügt zu Cl</i>', 'Cl adds regem'), 15: D('eum <i>fügt zu S Hr</i>', 'S Hr add eum'), 16: D('adþ. <i>Rl;</i> adel. <i>Hk;</i> adl. <i>Hr</i>', 'adþ. Rl; adel. Hk; adl. Hr'), 17: D('uero <i>Hk</i>', 'uero Hk'),
            18: D('nullos <i>Cl</i>', 'nullos Cl'), 19: D('filium <i>Hr</i>', 'filium Hr'), 20: D('regis <i>Cl;</i> uocant <i>fügt zu S</i>', 'regis Cl; S adds uocant')}},
 {'code': 'ECf', 'n': '35.1d', 'page': 665,
  'text': 'Quodsi expressius{f:ff} uolumus dicere, dicemus{21}, quod in quadam parte Saxoniæ{f:g}{22} ‘ling’{23} ymago{f:h} dicebatur{24}, ‘aþel’{25} Anglice{26}: nobilis; quod coniunctum{27} ‘aþeling’{28}, id est{29} nobilis ymago dicitur{30}.',
  'notes': {'f:ff': FFF, 'f:g': FG, 'f:h': FH, 21: D('dicimus <i>Hr</i>', 'dicimus Hr'),
            22: D('<i>so, ausnahmsweise Diphthong bewahrend, Rl;</i> Saxonice terre, <i>aber</i> terre <i>unterstrichen und am Rande dafür</i> lingue <i>Hk</i>', 'so Rl, which exceptionally keeps the diphthong; Saxonice terre Hk, but with terre underlined and lingue in the margin instead'),
            23: D('linx <i>Rl</i>', 'linx Rl'), 24: D('dicitur <i>Hk</i>', 'dicitur Hk'), 25: D('adþel <i>Rl;</i> adela <i>Hk Hr;</i> adelā <i>Cl;</i> ældela <i>S</i>', 'adþel Rl; adela Hk Hr; adelā Cl; ældela S'),
            26: D('Anglie <i>Cl</i>', 'Anglie Cl'), 27: D('sonat <i>fügt zu Cl;</i> scilicet <i>Hr</i>', 'Cl adds sonat; scilicet Hr'), 28: D('ade. <i>Hk;</i> adþ. <i>Rl;</i> adl. <i>Hr;</i> eþel. <i>Cl S</i>', 'ade. Hk; adþ. Rl; adl. Hr; eþel. Cl S'),
            29: D('quod <i>fügt zu Hr</i>', 'Hr adds quod'), 30: D('<i>aus Rl</i>', 'from Rl')}},
 {'code': 'ECf', 'n': '35.1e', 'page': 665,
  'text': 'Unde etiam Occidentales Saxonici{31}, scilicet Execestrenses{32}, habent in{33} prouerbio summi despectus, quod summa ira commotus unus{34} uocat{35} alterum ‘hinderling’, id est ab omni honestate deiectum.',
  'notes': {'f:h': FH, 31: D('-ni <i>Cl</i>', '-ni Cl'), 32: D('-cestre <i>S</i>', '-cestre S'), 33: D('prouerbium <i>Cl</i>', 'prouerbium Cl'), 34: D('uo. alter alt. <i>Cl</i>', 'uo. alter alt. Cl'), 35: D('hoc ad al. hindling <i>Hk</i>', 'hoc ad al. hindling Hk')}},

 {'code': 'ECfRetr', 'n': '35.1a', 'page': 665,
  'text': 'Cui{1} Cristine{2} rex Eadwardus dedit terram quam habuit postea Radulfus de Limesi{3}.',
  'notes': {'f:a': FA, 1: LOND, 2: D('Christiane <i>Hv</i>', 'Christiane Hv'),
            3: D('Lindeseye <i>Dc;</i> Limiseia. Fuit enim predicta Christiana soror Edgari Aedeling. Item propter quem Edwardum (Edgarum <i>Co</i>) predictum misit r. E. <i>Lond</i>', 'Lindeseye Dc; Limiseia. Fuit enim predicta Christiana soror Edgari Aedeling. Item propter quem Edwardum (Edgarum Co) predictum misit r. E. Lond')}},
 {'code': 'ECfRetr', 'n': '35.1b', 'page': 665,
  'text': 'Propter quem misit rex Eadwardus, auunculus{4} eius, et fecit eum uenire{5} ad se†. <b>Qui postquam</b> uenit{6}, non <b>multum</b> <sp>postea</sp>{7} <sp>uixit</sp>, et uxor <b>illius</b>{8} <b>in breui temporis</b>{6} <b>curriculo defuncta est.</b> Rex <b>uero</b> Eadwardus Eadgarum, filium <b>eorum,</b> secum retinuit et{9} pro filio nutriuit.',
  'notes': {'f:b': FB, 'f:c': FC, 'f:d': FDd, 4: D('ei. au. <i>Cb</i>', 'ei. au. Cb'), 5: D('uenisse <i>Hv</i>', 'uenisse Hv'), 6: D('<i>fehlt Ph</i>', 'lacking in Ph'), 7: D('<i>fehlt Lond</i>', 'lacking in Lond'),
            8: D('eius <i>Va Ph</i>', 'eius Va Ph'), 9: D('et p. f. n. <i>fehlt Cb</i>', 'et p. f. n. lacking in Cb')},
  'editorial': ['Liebermann prints “†” after “ad se” and gives in the outer margin the date †1057.']},
 {'code': 'ECfRetr', 'n': '35.1c', 'page': 665,
  'text': '{10}Et quia <b>cogitabat</b> heredem{11} <b>(suum</b>{12}<b>)</b> eum facere, nominauit{13} adeling{14}, quod{15} nos dicimus{16} domicellum{f:f}, sed{17} nos <b>indiscrete</b> de pluribus <b>dicimus</b>{18}<b>,</b> quia baronum filios uocamus domicellos, Angli <b>uero</b> nullum <b>nisi natos</b> regum.',
  'notes': {'f:e': FE, 'f:f': FF, 10: D('Quod etheling dicitur domicillus <i>roth am Rande Cb</i>', 'Quod etheling dicitur domicillus in red in the margin Cb'), 11: D('e. h. <i>Hv;</i> ipsum h. <i>Co</i>', 'e. h. Hv; ipsum h. Co'),
            12: D('<i>fehlt Cb Lb Ph Hv Lond</i>', 'lacking in Cb Lb Ph Hv Lond'), 13: D('eum <i>fügt zu Hv</i>', 'Hv adds eum'), 14: D('ed. <i>Cb Ph</i>', 'ed. Cb Ph'), 15: D('quem <i>Cb Lb Va</i>', 'quem Cb Lb Va'),
            16: D('<i>fehlt Co</i>', 'lacking in Co'), 17: D('<i>Schluss von</i> 35, 1<i>c fehlt Dc</i>', 'the end of 35, 1c is lacking in Dc'), 18: D('dominis, q. barones <i>ohne</i> f. <i>Hv</i>', 'dominis, q. barones without f. Hv')}},
 {'code': 'ECfRetr', 'n': '35.1d', 'page': 665,
  'text': 'Quodsi expressius uolumus dicere, in quadam{19} <b>regione</b> Saxonie{20} ling ymago <b>dicitur,</b> adel{21} Anglice: nobilis <b>Latine;</b> quod <b>simul</b> coniunctum{22} <b>sonat</b> nobilis ymago: adeling{23}.',
  'notes': {'f:ff': FFF, 'f:g': FG, 'f:h': FH, 19: D('q. r. <i>fehlt Hv</i>', 'q. r. lacking in Hv'), 20: D('Saxonica <i>Hv;</i> Saxonum l. im. <i>Cb</i>', 'Saxonica Hv; Saxonum l. im. Cb'), 21: D('adela <i>Cb Hv Lond</i>', 'adela Cb Hv Lond'),
            22: D('c. s. n. y. a. <i>fehlt Ph</i>', 'c. s. n. y. a. lacking in Ph'), 23: D('ed. <i>Lb Va Hv;</i> ead. <i>K;</i> aedel. <i>Co.</i>', 'ed. Lb Va Hv; ead. K; aedel. Co.')}},
 {'code': 'ECfRetr', 'n': '35.1e', 'page': 665,
  'text': 'Unde{24} etiam Occidentales Saxones{25}, scilicet{26} Execestrenses{27}, habent in prouerbio summi despectus hinderling{28}, id est ab{29} omni honestate{30} deiectum{31} <b>uel retrocedens</b>{f:i} <b>imago.</b>',
  'notes': {'f:h': FH, 'f:i': FI, 24: D('<i>am Rande</i> Quid sit hinderling <i>roth Cb;</i> U. et <i>Va</i>', 'in the margin Quid sit hinderling in red Cb; U. et Va'), 25: D('-ni <i>Cb;</i> -nidi <i>Lb K;</i> -nidj <i>Va</i>', '-ni Cb; -nidi Lb K; -nidj Va'),
            26: D('<i>fehlt Hv</i>', 'lacking in Hv'), 27: D('Exces. <i>Va;</i> Cestr. <i>Hv;</i> Exceces. <i>Co</i>', 'Exces. Va; Cestr. Hv; Exceces. Co'), 28: D('edeling <i>Hv</i>', 'edeling Hv'), 29: D('<i>fehlt K</i>', 'lacking in K'),
            30: D('potestate <i>Cb</i>', 'potestate Cb'), 31: D('-tus <i>Hv</i>', '-tus Hv')}},
]
