# Liebermann, Gesetze I pp. 661–662: ECf and ECf retr 34,1a (begins p. 661) – 34,2a (34,2b runs on: see p663.py)
D = lambda de, en: (de, en)
STAR = D('Thomas uero archiepiscopus§ et Mauricius episcopus scripserunt propriis manibus omnia ista predicta per preceptum predicti regis Willelmi <i>interpolirt Lond.</i> — §) Cantuariensis <i>fügt zu Ld</i> [<i>fehlerhaft</i>]; <i>die beiden Namen beginnen die Zeugenliste einer Urkunde Wilhelms I., die in der Gildhalle copirt war</i> (Lib. custum. 28); <i>daher wohl bringt sie der Londoner hier anachronistisch: Thomas von York sass</i> 1070—1100, <i>Morix von London</i> 1086—1107. <i>Diess verschlimmert der Lichfielder o. S.</i> 627*',
         'Lond interpolates Thomas uero archiepiscopus§ et Mauricius episcopus scripserunt propriis manibus omnia ista predicta per preceptum predicti regis Willelmi. — §) Ld adds Cantuariensis [wrongly]; the two names begin the witness list of a charter of William I which had been copied in the Guildhall (Lib. custum. 28); that is probably why the Londoner brings them in here, anachronistically: Thomas of York sat 1070–1100, Maurice of London 1086–1107. The Lichfield man makes this worse, above p. 627*')
STAR2 = D('Unrad <i>fügt zu Lond. Vgl. Plummer</i> Two Saxon chron. II 168', 'Lond adds Unrad. Cf. Plummer, Two Saxon chron. II 168')
FB = D('<i>dass dem XI. Jahrh. Eadgars Recht als Ideal galt, weiss Verf. vielleicht aus Will. Malm.</i> Reg. II 148; <i>er missverstand vielleicht dessen Satz</i> III 254: Cnutone defuncto, indigenæ sibi antiquum ius uendica[bant]. <i>Er verkennt, dass Æthelred II. und Cnut Eadgars Recht wiederholten und citirten. Ebenso</i> 34, 3',
       'that in the 11th century Edgar’s law counted as an ideal the author knows perhaps from Will. Malm., Reg. II 148; he perhaps misunderstood that author’s sentence III 254: Cnutone defuncto, indigenæ sibi antiquum ius uendica[bant]. He fails to recognise that Æthelred II and Cnut repeated and cited Edgar’s law. Likewise 34, 3')
FC = D('<i>das Folgende aus einer unbekannten Zeittafel. Die Zahlenfehler begeht Verf. selbst (nicht etwa ein Abschreiber) laut S.</i> 663<i>g</i>', 'what follows is from an unknown chronological table. The errors in the numbers are the author’s own (not, say, a copyist’s), according to p. 663, note g')
FD = D('<i>vielmehr</i> III', 'rather III')
FE = D('d. n. s. <i>vielleicht aus Will. Malm.</i> Reg. II 162', 'd. n. s. perhaps from Will. Malm., Reg. II 162')
FF = D('<i>die gläubigen Engländer trennt der also wohl fremde Verf. von sich</i>', 'the author, who is thus probably a foreigner, separates the believing English from himself')
DAG = ('Liebermann prints “†” after “{w}” and gives in the outer margin of the ECf retr column the dates {d}{x}.')
CUT = ' (the last figures are cut off in the scan used here)'
AST = ('Liebermann prints a small raised asterisk after “{w}” (not one of his starred notes) and gives in the outer margin of the ECf retr column the dates {d}.')
NP662 = lambda *ks: {k: 662 for k in ks}
CLAUSES = [
 {'code': 'ECf', 'n': '34.1a', 'page': 661, 'pages': [662],
  'text': 'Et hoc{1} etiam{29} precati sunt eum{30} pro anima regis Eadwardi{31}, qui sibi concesserat regnum, et cuius erant leges, nec{32} aliorum exterorum. Tan[[pb:662]]dem consilio et precatu{f:a} baronum{1/662} adquieuit.{*} Et sic{2/662} auctorizate sunt leges regis Eadwardi{3/662}. [<i>Ad Do Wo Ck No Ed 1:</i> auctoritate leges sunt confirmate in Eo qui uiuit et regnat per infinita seculorum{4/662} secula. Amen!{5/662}]',
  'notepages': NP662('f:a', '*', '1/662', '2/662', '3/662', '4/662', '5/662'),
  'notes': {1: D('<i>fehlt Ad Do</i>', 'lacking in Ad Do'), 29: D('<i>fehlt Hk Ad Do</i>', 'lacking in Hk Ad Do'), 30: D('ut <i>fügt zu S</i>', 'S adds ut'), 31: D('Ædw. <i>Hk S</i>', 'Ædw. Hk S'),
            32: D('ut non legibus al. suas permutaret leges. Tandem <i>Ad Do Ed 1</i>', 'ut non legibus al. suas permutaret leges. Tandem Ad Do Ed 1'),
            'f:a': D('<i>Barone, um</i> 1070 <i>wesentlich Normannen, bitten ihren Normannischen Herrn um Angelsächsisches Recht!</i>', 'barons, around 1070 essentially Normans, ask their Norman lord for Anglo-Saxon law!'),
            '*': STAR,
            '1/662': D('suorum <i>fügt zu Ad Do Wo</i>', 'Ad Do Wo add suorum'), '2/662': D('<i>fehlt Hr</i>', 'lacking in Hr'), '3/662': D('Ædw. <i>Hk S</i>', 'Ædw. Hk S'),
            '4/662': D('secula seculorum <i>Do No</i>', 'secula seculorum Do No'),
            '5/662': D('<i>enden Ad Do.</i> Explicit <i>fügt zu Wo;</i> Finitur (finito <i>em.</i>) libro, reddatur gratia Christo <i>fügt zu No</i>', 'Ad Do end here. Wo adds Explicit; No adds Finitur (finito emended) libro, reddatur gratia Christo')},
  'editorial': ['Liebermann’s numbering of the notes in the ECf column starts again at 1 on p. 662: the notes 1–5 to the part of this clause on p. 662 are distinct from the notes 1 and 29–32 on p. 661.',
                'After “Et sic” Liebermann prints the rest of the sentence in two columns side by side: on the left “auctorizate sunt leges regis Eadwardi”, and on the right, headed “Ad Do Wo Ck No Ed 1”, the ending of those manuscripts. The right-hand column is given here in square brackets after the left-hand one.',
                'The note on the London collection’s interpolation (*) is printed across the whole page; it is given with both columns.']},
 {'code': 'ECf', 'n': '34.1b', 'page': 662,
  'text': 'Que prius adinuente et{6} constitute fuerunt tempore regis Eadgari{f:b}{7}, aui sui; sed post mortem eius dimisse sunt annis{f:c} LX{8} et VIII†.',
  'notes': {'f:b': FB, 'f:c': FC, 6: D('et c. <i>fehlt Hk Ed 2</i>', 'et c. lacking in Hk Ed 2'), 7: D('Ædg. <i>Hk S</i>', 'Ædg. Hk S'), 8: D('XLVII <i>Hk Ed. 2;</i> XLVIII <i>Hr</i>', 'XLVII Hk Ed. 2; XLVIII Hr')},
  'editorial': [DAG.format(w='VIII', d='975–10…', x=CUT)]},
 {'code': 'ECf', 'n': '34.2', 'page': 662,
  'text': '{9}Eadwardus{10}, filius eius natus de uxore{11}, regnauit IIII{f:d} annis*, XVI ebdomadibus{12} minus{13}. Quo occiso{14} innocenter{15} dolo{f:e} nouerce sue, propter innocentem uitam suam, castam et elemosinis plenam, interfectionem eius pro martyrio reputauerunt{f:f} ei et uocauerunt sanctum.',
  'notes': {'f:d': FD, 'f:e': FE, 'f:f': FF,
            9: D('Regnum Aedwardi [Ed. <i>S</i>], filii Aedgari [Edwardi <i>S</i>] regis <i>Überschrift Pl S</i>', 'heading in Pl S: Regnum Aedwardi [Ed. S], filii Aedgari [Edwardi S] regis'),
            10: D('Edw. <i>Hk;</i> Aed. <i>S</i>', 'Edw. Hk; Aed. S'), 11: D('sua <i>fügt zu Hk</i>', 'Hk adds sua'), 12: D('-dis <i>S</i>', '-dis S'), 13: D('<i>fehlt Hk</i>', 'lacking in Hk'),
            14: D('innocente occ. <i>Hk</i>', 'innocente occ. Hk'), 15: D('-te <i>S Hr</i>', '-te S Hr')},
  'editorial': [AST.format(w='annis', d='975–78')]},
 {'code': 'ECf', 'n': '34.2a', 'page': 662,
  'text': '{16}Post hunc {17}Ædelredus{18}, frater eius{**}, regnum{19} suscepit, regnauitque in multis periculis XXX et VIII annis†.',
  'notes': {'**': STAR2, 16: D('Regnum Ældredi, fratris Eadwardi <i>überschreibt Pl S</i>', 'Pl S head it Regnum Ældredi, fratris Eadwardi'), 17: D('<i>fehlt Hr</i>', 'lacking in Hr'),
            18: D('Ad. <i>Rl;</i> Ældr. <i>S</i>', 'Ad. Rl; Ældr. S'), 19: D('s. r. <i>Hk Hr</i>', 's. r. Hk Hr')},
  'editorial': [DAG.format(w='annis', d='978–10…', x=CUT), 'The note on the London collection’s addition (**) is printed across the whole page; it is given with both columns.']},

 {'code': 'ECfRetr', 'n': '34.1a', 'page': 661, 'pages': [662],
  'text': '<b>Rege uero ad flectendum ingrato existente, tandem</b>{36} eum <b>prosecuti</b>{37} sunt deprecantes, <b>quatinus</b> pro anima regis Eadwardi{38}, qui sibi{39} <b>post diem suum</b> con[[pb:662]]cesserat <b>coronam et</b> regnum, et cuius erant leges, nec{1} aliorum <sp>extraneorum</sp>, <b>exaudiendo</b>{2} <b>concederet eis</b>{3} <b>sub legibus perseuerare paternis</b>{4}. <b>Unde</b> consilio <b>habito,</b> precatu baronum tandem adquieuit.{*} Et{5} <b>ex illo</b>{6} <b>igitur</b>{7} <b>die multa</b>{3} auctoritate <b>uenerate</b>{9} <b>per uniuersam</b>{10} <b>Angliam, confirmate</b>{11} <b>et corroborate (et</b>{12} <b>obseruate)</b> sunt <b>pre ceteris patrie legibus</b> leges regis{13} Eadwardi{14}.',
  'notepages': NP662('*', 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14),
  'notes': {36: D('<i>fehlt Dc</i>', 'lacking in Dc'), 37: D('pers. <i>Co</i>', 'pers. Co'), 38: D('Ed. <i>Cb;</i> Æd. <i>Hv</i>', 'Ed. Cb; Æd. Hv'), 39: D('ei <i>Hv</i>', 'ei Hv'),
            '*': STAR,
            1: D('ne <i>Cb</i>', 'ne Cb'), 2: D('cogeret quam sub <i>nur Hv’s Ed. Sarile</i>', 'cogeret quam sub only Hv’s editor Sarile'), 3: D('<i>fehlt Hv</i>', 'lacking in Hv'), 4: D('patriis <i>Hv</i>', 'patriis Hv'),
            5: D('<i>fehlt Cb Ph Hv</i>', 'lacking in Cb Ph Hv'), 6: D('illa <i>Hv</i>', 'illa Hv'), 7: D('ergo <i>Hv</i>', 'ergo Hv'), 9: D('et <i>fügt zu Lond</i>', 'Lond adds et'),
            10: D('-sum regnum <i>Lond</i>', '-sum regnum Lond'), 11: D('conf. et <i>aus Cb; fehlt übr.</i>', 'conf. et from Cb; lacking in the others'), 12: D('et obs. <i>fehlt Cb</i>', 'et obs. lacking in Cb'),
            13: D('Æd. r. <i>Hv</i>', 'Æd. r. Hv'), 14: D('sancti <i>fügt zu Co</i>', 'Co adds sancti')},
  'editorial': ['After “multa” Liebermann prints the note number 3 (“fehlt Hv”), not 8, and no word in the text carries his note 8; the 3 is linked here as printed, and note 8 is given below.',
                'Liebermann’s note 8 in the ECf retr column of p. 662 reads: “8) uisa <i>Hv</i>” (uisa Hv).',
                'The note on the London collection’s interpolation (*) is printed across the whole page; it is given with both columns.']},
 {'code': 'ECfRetr', 'n': '34.1b', 'page': 662,
  'text': 'Que prius inuente et constitute fuerunt{16} tempore regis{3} Eadgari{17}, aui sui; <b>uerum</b> post mortem <b>ipsius</b> dimisse{16} sunt annis{19} <b>circiter</b>{20} sexaginta octo†.',
  'notes': {'f:b': FB, 'f:c': FC, 3: D('<i>fehlt Hv</i>', 'lacking in Hv'), 16: D('-rant <i>Cb Va;</i> erant in <i>Hv</i>', '-rant Cb Va; erant in Hv'),
            17: D('Ed ar, <i>dahinter Rasur Cb;</i> Æd. <i>stets Hv</i>', 'Ed ar, followed by an erasure Cb; Æd. always Hv'), 18: D('d. s. <i>fehlt Hv;</i> dem. <i>Cb K</i>', 'd. s. lacking in Hv; dem. Cb K'),
            19: D('c. annos <i>Hv</i>', 'c. annos Hv'), 20: D('an. VIII circ., <i>am Rande</i> LX <i>Cb</i>', 'an. VIII circ., with LX in the margin Cb')},
  'editorial': ['Liebermann prints the note number 16 twice in this sentence, after “fuerunt” and after “dimisse”, and there is no note 15 in this column; his note 16 (“-rant Cb Va; erant in Hv”) fits “fuerunt”, and the second 16 is probably a misprint for 18 (“d. s. fehlt Hv; dem. Cb K”, i.e. dimisse sunt), which no word in the text otherwise carries. Both are linked here to note 16 as printed, and note 18 is given as well.',
                DAG.format(w='octo', d='975–10…', x=CUT)]},
 {'code': 'ECfRetr', 'n': '34.2', 'page': 662,
  'text': 'Eadwardus{21} <b>enim,</b> filius eius <b>heres</b>{22}<b>, scilicet</b> de{23} uxore <b>legitima</b> natus, regnauit{24} annis quatuor*, ebdomadibus{25} sexdecim minus. Quo occiso innocente sue dolo nouerce, propter innocentem uitam <b>eius,</b> castam et elemosinis plenam, interfectionem{26} eius <b>immeritam</b> pro martyrio reputauerunt{27} ei et sanctum <b>habuerunt.</b>',
  'notes': {'f:d': FD, 'f:e': FE, 'f:f': FF, 21: D('Ed. <i>stets Cb</i>', 'Ed. always Cb'), 22: D('herilis <i>Cb Hv</i>', 'herilis Cb Hv'), 23: D('na. de l. u. <i>Cb</i>', 'na. de l. u. Cb'),
            24: D('regnum tenuit <i>Cb</i>', 'regnum tenuit Cb'), 25: D('ebdomadis <i>Va</i>', 'ebdomadis Va'), 26: D('-nis <i>Va</i>', '-nis Va'), 27: D('ei comput. <i>Cb</i>', 'ei comput. Cb')},
  'editorial': [AST.format(w='quatuor', d='975–78')]},
 {'code': 'ECfRetr', 'n': '34.2a', 'page': 662,
  'text': 'Post <b>ipsum</b> Ethelredus{28}{**}, frater eius, regnum suscepit <b>et</b> regnauit in multis <b>aduersitatibus et</b> periculis triginta octo annis†.',
  'notes': {'**': STAR2, 28: D('Aeld. <i>Co;</i> Adelred <i>Lb;</i> Aldr. <i>übr.</i>', 'Aeld. Co; Adelred Lb; Aldr. the others')},
  'editorial': [DAG.format(w='annis', d='978–10…', x=CUT), 'The note on the London collection’s addition (**) is printed across the whole page; it is given with both columns.']},
]
