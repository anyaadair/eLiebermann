# Liebermann, Gesetze I pp. 669–670: ECf and ECf retr 39,1 (begins p. 669) – 39,2, the end of the text
# (The Anhang on pp. 670–672, the chapter list of 'Rubricator II', is not included here.)
D = lambda de, en: (de, en)
FH = D('Stadtrecht', 'town law')
FI = D('<i>andere Bürger als Fleischer schlachten nur vor dem Winter zum Einpökeln; in Schleswig</i> post festum s. Martini non est opus fideiussore pro pecoribus; <i>Steenstrup</i> Danelag 376', 'citizens other than butchers slaughter only before the winter, for salting; in Schleswig post festum s. Martini non est opus fideiussore pro pecoribus; Steenstrup, Danelag 376')
FA = D('<i>Subject ist</i> ciues, <i>nicht</i> macerarii <i>aus</i> 39', 'the subject is ciues, not macerarii from 39')
FB = D('<i>d. i. Verfasser (unter Wilhelms I. Maske?), nicht die angebliche Angelsächs. Jury von</i> 1070 <i>im Prolog und</i> 34, 1', 'i.e. the author (in the mask of William I?), not the alleged Anglo-Saxon jury of 1070 in the Prologue and 34, 1')
FC = D('<i>bestehen bleiben die älteren drei Cautelen seit</i> Hl 16, <i>vor Einführung der Gewährbürgen:</i> auf offenem Markt, mit Kaufzeugen und nicht ohne die Verkäufer zu kennen', 'the three older safeguards, in force since Hl 16, before the introduction of warrantor-sureties, remain: in the open market, with witnesses to the purchase, and not without knowing the sellers')
FD = D('<i>Ablat. absol.:</i> wenn nur ihr Einkauf auf öffentlichem Markt gekauft war', 'ablative absolute: provided only that their purchase was bought in the public market')
STAR = D('Et concessum est <i>fügt Texthand nachträglich zu Cb; folgt</i> De latronibus, <i>oben c.</i> 36, <i>Lond; folgt</i> Geneal. Normann. <i>Cb Oh Pe Hy Ld 1 Cu Hv Lb Ra Vi Rc Va La Ba Ph; über Gr vgl. u. S.</i> 672<i>b</i>; Expliciunt leges sancti Edwardi, primo adinuente per Edgarum, auum suum, et per Willelmum conquestorem Anglie confirmate et prius tempore Cnutonis regis approbate <i>fügt zu Db L</i> [<i>Erwähnung Cnuts widerspricht</i> ECf. 34, 1<i>b</i>; 3, <i>aber vgl. S.</i> 618<i>f</i>]',
         'the text hand adds Et concessum est later in Cb; De latronibus, above c. 36, follows in Lond; the Geneal. Normann. follows in Cb Oh Pe Hy Ld 1 Cu Hv Lb Ra Vi Rc Va La Ba Ph; on Gr cf. below, p. 672, note b; Db L add Expliciunt leges sancti Edwardi, primo adinuente per Edgarum, auum suum, et per Willelmum conquestorem Anglie confirmate et prius tempore Cnutonis regis approbate [the mention of Cnut contradicts ECf 34, 1b; 3, but cf. p. 618, note f]')
NP = lambda ks: {k: 670 for k in ks}
CLAUSES = [
 {'code': 'ECf', 'n': '39.1', 'page': 669, 'pages': [670],
  'text': 'Clamabant etiam ciues et burgenses pro consuetudinibus{f:h} suis{30}, quod circa festum{f:i} sancti† Mar[[pb:670]]tini emebant{f:a/670} animalia sine plegio{1} ad faciendas suas occisiones contra natale{2} Domini†.',
  'notepages': NP(['f:a/670', 1, 2]),
  'notes': {'f:h': FH, 'f:i': FI, 30: D('<i>fehlt Hk Hr</i>', 'lacking in Hk Hr'), 'f:a/670': FA, 1: D('-iis <i>Hk S</i>', '-iis Hk S'), 2: D('-lem <i>Hr</i>', '-lem Hr')},
  'editorial': ['Liebermann prints daggers after “sancti” and after “Domini”; in the outer margin of the ECf retr column he gives the dates †Nov. 11 (St Martin’s day) and †Dec. 25.',
                'Liebermann’s lettering of the notes starts again at a on p. 670: the note a to “emebant” is distinct from the notes h and i on p. 669.']},
 {'code': 'ECf', 'n': '39.2', 'page': 670,
  'text': 'Quas consuetudines iustas et sapienter ductas non auferimus{f:b} eis: tantum{3} in{f:c} mercatis emant{4} cum testibus et{5} cognitione uenditorum.{6}',
  'notes': {'f:b': FB, 'f:c': FC, 3: D('tamen <i>S</i>', 'tamen S'), 4: D('emptis (<i>lies</i> ematis?) <i>Hk S;</i> emptas <i>Hr</i>', 'emptis (read ematis?) Hk S; emptas Hr'), 5: D('et c. u. <i>fehlt Hr</i>', 'et c. u. lacking in Hr'),
            6: D('<i>enden Rl Hk;</i> Expliciunt leges Edwardi et Willelmi regum Anglie <i>fügt zu Hr; folgt gleich wie ferneres Capitel</i> Libertas ciuitatum, <i>d. i.</i> Lib. Lond <i>u. S.</i> 673, <i>Pl S</i>',
                 'Rl Hk end here; Hr adds Expliciunt leges Edwardi et Willelmi regum Anglie; in Pl S there follows at once, as if a further chapter, Libertas ciuitatum, i.e. Lib. Lond, below p. 673')},
  'editorial': ['This is the last clause of ECf.']},

 {'code': 'ECfRetr', 'n': '39.1', 'page': 669, 'pages': [670],
  'text': '<b>Uociferabantur</b>{31} etiam ciues et burgenses et <b>populus</b> pro suis consuetudinibus, <b>eo</b> quod circa{32} festum sancti† Mar[[pb:670]]tini <b>consueuerant</b> animalia <b>in foro mercari</b> sine plegio{1/670} ad suas{2/670} occisiones contra natale† Domini faciendas.',
  'notepages': NP(['f:a/670', '1/670', '2/670']),
  'notes': {'f:h': FH, 'f:i': FI, 'f:a/670': FA, 31: D('Uocificab. <i>Hv</i>', 'Uocificab. Hv'), 32: D('circiter <i>Hv</i>', 'circiter Hv'),
            '1/670': D('-iis <i>Hv</i>', '-iis Hv'), '2/670': D('<i>fehlt Hv</i>', 'lacking in Hv')},
  'editorial': ['Liebermann prints daggers after “sancti” and after “natale”, and gives in the outer margin the dates †Nov. 11 and †Dec. 25.',
                'Liebermann’s numbering of the notes in the ECf retr column starts again at 1 on p. 670.']},
 {'code': 'ECfRetr', 'n': '39.1a', 'page': 670, 'keys': ['ECfRetr 39.1a'],
  'margin': ['Horaz Sat. 28, 77', 'Exod. 32, 17 f.'],
  'text': '<b>Murmur etiam multum</b>{3} <b>super hoc edicto erat in turba; quare, ut</b>{2} <b>estimo, si quereretur</b>{4} <b>ibi</b>{5}<b>, utrum</b>{6} <b>placeret</b>{7}<b>, ut fit</b>{8} <b>in quibusdam congregationibus</b>{9}<b>, sine</b>{10} <b>omni consilio a multis</b>{11} <b>redderetur: ‘non placet!’ Ibi etiam, si adesses, audires† stridere</b>{12} <b>secreta diuisos aure susurros et</b>{13} <b>clamores†† et</b>{14} <b>uociferationes et murmurationes tumultuantium</b>{15} <b>populorum.</b>',
  'notes': {2: D('<i>fehlt Hv</i>', 'lacking in Hv'), 3: D('-tus <i>Hv Ph Lond</i>', '-tus Hv Ph Lond'), 4: D('queratur <i>K</i>', 'queratur K'), 5: D('ubi <i>Lb Va Ph</i>', 'ubi Lb Va Ph'),
            6: D('u. p. <i>fehlt hier Cb Lb Va Ph Lond</i>', 'u. p. lacking here in Cb Lb Va Ph Lond'), 7: D('necne illud decretum <i>fügt zu Hv</i>', 'Hv adds necne illud decretum'), 8: D('sit <i>Lond</i>', 'sit Lond'),
            9: D('‘placet?’ <i>fügt zu Cb Lb Va Ph K</i>', 'Cb Lb Va Ph K add ‘placet?’'), 10: D('communi <i>st.</i> s. o. <i>Hv</i>', 'communi instead of s. o. Hv'), 11: D('responsum <i>am Rande in anderer Tinte Cb</i>', 'responsum in the margin in another ink Cb'),
            12: D('stud. <i>K</i>', 'stud. K'), 13: D('et cl. et u. et mur. <i>fehlt Db</i>', 'et cl. et u. et mur. lacking in Db'), 14: D('et u. <i>fehlt Hv</i>', 'et u. lacking in Hv'), 15: D('tumulan. <i>Lb</i>', 'tumulan. Lb')},
  'editorial': ['This paragraph is wholly the Retractator’s own (all in bold); it has no counterpart in ECf. Liebermann gives it no number of its own: it is numbered 39.1a here so that it can stand as a clause between 39, 1 and 39, 2.',
                'The dagger after “audires” and the double dagger after “clamores” refer to Liebermann’s marginal references: † Horace, Satires (printed “Sat. 28, 77”; the line “stridere secreta diuisos aure susurros” is Satires II 8, 77–78), †† Exodus 32, 17 f.']},
 {'code': 'ECfRetr', 'n': '39.2', 'page': 670,
  'text': '<b>Et laudatum est regi, quatinus</b> consuetudines iustas et sapienter <sp>deductas</sp> non <sp>auferret</sp>{16} eis, tantum in <b>foro regio</b> <sp>empto</sp>{f:d} <sp>mercato</sp> <b>suo</b> cum testibus et cognitione <sp>uendentium</sp>.{*}',
  'notes': {'f:b': FB, 'f:c': FC, 'f:d': FD, '*': STAR, 16: D('auferet <i>Cb</i>', 'auferet Cb')},
  'editorial': ['The starred note (*) is printed across the whole page; it is given here, with the end of the Retractator’s text.', 'This is the last clause of ECf retr. Liebermann’s Anhang on pp. 670–672 (the chapter list of ‘Rubricator II’) is not yet added.']},
]
