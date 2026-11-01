# Liebermann, Gesetze I p. 643: ECf and ECf retr 17,1–18b (18,1 runs on: see p644.py)
D = lambda de, en: (de, en)
FA = D('<i>Thronverlust bestimmt dem pflichtvergessenen Herrscher Gregor VII.; vgl. Böhmer</i> Staat und Kirche 416; <i>vielleicht dachte Verf. an Robert von der Normandie</i> 1106 <i>und der Retractor an Stephan</i> 1141 <i>oder</i> 1154', 'Gregory VII decrees loss of the throne for a ruler forgetful of his duty; cf. Böhmer, Staat und Kirche 416; perhaps the author was thinking of Robert of Normandy in 1106, and the Retractator of Stephen in 1141 or 1154')
FB = D('Zacharias (751—52), <i>wie im</i> 16. <i>Jahrh. Va in Retr. bessert; vgl. S.</i> 635<i>b</i>', 'Zacharias (751–52), as Va corrects in the Retr. in the 16th century; cf. p. 635, note b')
FC = D('<i>aus Ado, ed.</i> Maxima bibl. vet. patr. (<i>Lugd.</i> 1677) XVI 804', 'from Ado, ed. Maxima bibl. vet. patr. (Lyon 1677) XVI 804')
FD = D('Childerich III.; <i>vgl. Va zu Retr.</i>', 'Childeric III; cf. Va on the Retr.')
FF = D('vor <i>Verhaftung und Urtheil, wie aus dem Gegensatz zu</i> 18, 1 <i>folgt</i>', 'before arrest and judgement, as follows from the contrast with 18, 1')
FG = D('<i>der König</i> kann, <i>die Kirche</i> muss <i>den Zufluchtsuchenden vor Leibesstrafe schützen; Pollock-M.</i> HEL. II 481', 'the king can, the Church must, protect the one seeking refuge from corporal punishment; Pollock–M., HEL. II 481')
FH = D('<i>vgl.</i> 18, 1a: <i>der König kann von vermögensrechtlichen Verbindlichkeiten nicht lösen</i>', 'cf. 18, 1a: the king cannot release from obligations in property law')
FI = D('<i>vgl.</i> II As. 20, 1. 4; I Atr. 4', 'cf. II As. 20, 1. 4; I Atr. 4')
FK = D('<i>Verf. meint nicht Ächtung Abwesender, also Landes-Abschwörung</i> (<i>s.</i> 18, 2), <i>und da Bürgen davon befreien, nicht den</i> murdritor <i>und</i> traditor. <i>Vgl. a.</i> 1235: quia non potuit inuenire plegios, regnum abiurauit; <i>Palgrave</i> Rise II <i>p.</i> clxxxviii.', 'the author means not the outlawing of the absent, so abjuration of the realm (see 18, 2), and, since sureties free a man from that, not the murdritor and traditor. Cf. a. 1235: quia non potuit inuenire plegios, regnum abiurauit; Palgrave, Rise II p. clxxxviii.')
SMALL = 'Liebermann prints the words taken from Ado of Vienne (“si ita deberent … populum eius”) in smaller type; his margin names the source, “Ado Vienn.”.'
CLAUSES = [
 {'code': 'ECf', 'n': '17.1', 'page': 643,
  'text': 'Sin{1} autem, nomen{2} regis perdit{f:a}, testante Iohanne{f:b} papa. Cui{f:c} Pipinus{3} et Karolus, filius eius, necdum{4} reges, sed principes sub rege{f:d} Francorum{5} stulto{6}, scripserunt, querentes{7}, si ita deberent manere{f:e} reges{8} Francorum{5}, solo{9} regio{10} nomine contenti? A quo responsum est: ‘Illos{11} decet uocari reges qui uigilanter{12} defendunt et regunt ecclesiam Dei et populum eius’{13}, imitati{14} regem psalmigraphum{15} dicentem: ‘Non habitabit{16} in medio domus mee qui{17} facit superbiam’ etc.',
  'margin': ['Ado Vienn.', 'Ps. 100, 7'],
  'notes': {'f:a': FA, 'f:b': FB, 'f:c': FC, 'f:d': FD, 'f:e': D('<i>so Ado;</i> permanere <i>Willkür des Retr.</i>', 'so Ado; permanere is the Retractator’s arbitrary change'),
            1: D('Si <i>Ad Do</i>', 'Si Ad Do'), 2: D('<i>fehlt, Lücke Do</i>', 'lacking, a gap Do'), 3: D('Pep. <i>Hk Ad;</i> Pipp. <i>Hr</i>', 'Pep. Hk Ad; Pipp. Hr'), 4: D('nondum <i>Ad Do</i>', 'nondum Ad Do'), 5: D('Franchor. <i>Hk</i>', 'Franchor. Hk'),
            6: D('Karolo <i>fügt zu Rl</i> [<i>falsch</i>]', 'Rl adds Karolo [wrong]'), 7: D('<i>später übergeschr. Hk;</i> -te se <i>Do</i>', 'written above later Hk; -te se Do'), 8: D('<i>fehlt Ad Do</i>', 'lacking in Ad Do'), 9: D('sub <i>S</i>', 'sub S'),
            10: D('n. r. <i>Hk</i>', 'n. r. Hk'), 11: D('-las <i>Do</i>', '-las Do'), 12: D('-lant <i>S</i>', '-lant S'), 13: D('Dei <i>Hk</i>', 'Dei Hk'), 14: D('-tari <i>Ad</i>', '-tari Ad'), 15: D('spal. <i>Rl;</i> -mogr. <i>Ad</i>', 'spal. Rl; -mogr. Ad'),
            16: D('hereditauit <i>Do, dessen sinnlose Fehler ich fortan nicht notire</i>', 'hereditauit Do, whose senseless errors I shall not record from now on'), 17: D('q. f. s. <i>fehlt Hk</i>', 'q. f. s. lacking in Hk')},
  'editorial': [SMALL]},
 {'code': 'ECf', 'n': '18', 'page': 643,
  'text': 'Tamen si{f:f} aliquis{18} forisfactus requisierit{19} misericordiam, eius{20} timore mortis uel membrorum pro forefacto{21} suo, potest{22} ei condonare, si{f:g} placet, lege{23} sue{24} dignitatis.',
  'notes': {'f:f': FF, 'f:g': FG, 18: D('quis f. sit et r. <i>Ad Do;</i> forefaciens <i>Rl</i>', 'quis f. sit et r. Ad Do; forefaciens Rl'), 19: D('quesierit <i>Hk;</i> requierit <i>Hr</i>', 'quesierit Hk; requierit Hr'),
            20: D('regis <i>Ad Do</i>', 'regis Ad Do'), 21: D('<i>so Rl Hk;</i> forisf. <i>S Ad Do</i>', 'so Rl Hk; forisf. S Ad Do'), 22: D('poterit <i>Hr</i>', 'poterit Hr'), 23: D('leg’ s. dignitati <i>Hk;</i> legi <i>Rl</i>', 'leg’ s. dignitati Hk; legi Rl'), 24: D('d. s. <i>Ad</i>', 'd. s. Ad')}},
 {'code': 'ECf', 'n': '18a', 'page': 643,
  'text': 'Et{25} ipse{f:h} cui fecerit{26} misericordiam{27}, faciat rectum cui prius{28} forisfecerat{29}, in quantum poterit{30} complere, et inueniat fideiussores{f:i} de pace et legalitate tenenda.',
  'notes': {'f:h': FH, 'f:i': FI, 25: D('<i>fehlt Do</i>', 'lacking in Do'), 26: D('fecit <i>Ad Do;</i> m. f. <i>Hr</i>', 'fecit Ad Do; m. f. Hr'), 27: D('miām <i>Rl Hk;</i> iniuriam <i>S Ad Do</i>', 'miām Rl Hk; iniuriam S Ad Do'),
            28: D('f. p. <i>Hr</i>', 'f. p. Hr'), 29: D('foref. <i>Rl</i>', 'foref. Rl'), 30: D('potuerit <i>S</i>', 'potuerit S')}},
 {'code': 'ECf', 'n': '18b', 'page': 643,
  'text': 'Quodsi non poterit, exulabitur{31} a patria{f:k}.',
  'notes': {'f:k': FK, 31: D('-bit <i>Hk S Ad</i>', '-bit Hk S Ad')}},

 {'code': 'ECfRetr', 'n': '17.1', 'page': 643,
  'text': '<b>Quod nisi fecerit, nec</b>{1} <b>regis nomen</b>{2} <b>constabit</b>{3}<b>, uerum,</b> testante{4} papa Iohanne, nomen regis perdit{5}. Cui{6} Pipinus et Karolus, filius eius, necdum reges, sed principes sub rege Francorum{7} stulto{8}, scripserunt, querentes, si ita <b>per</b>manere deberent Francorum{9} reges, solo regio{10} nomine contenti? A quo responsum est: ‘Illos decet uocari reges, qui uigilanter{11} defendunt et regunt ecclesiam Dei et populum eius’, imitati{12} regem psalmigraphum{13} dicentem: ‘Non habitabit in medio domus mee qui facit superbiam’ et cetera{14}.',
  'margin': ['Ps. 100, 7'],
  'notes': {'f:a': FA, 'f:b': FB,
            1: D('nomen r. non in <i>K Co</i>', 'nomen r. non in K Co'), 2: D('in eo <i>fügt zu Lb Lond Ph Sp L</i>', 'Lb Lond Ph Sp L add in eo'), 3: D('u. c. <i>Hv</i>', 'u. c. Hv'),
            4: D('p. Zacharia t. <i>Va;</i> p. I. t. <i>Cb Lb Lond Ph;</i> p. I. atestante <i>Ra;</i> propheta I. t. <i>Hv</i>', 'p. Zacharia t. Va; p. I. t. Cb Lb Lond Ph; p. I. atestante Ra; propheta I. t. Hv'), 5: D('et cetera <i>übergeschr. Cb</i>', 'et cetera written above Cb'),
            6: D('[<i>statt</i> Cui] qui quod regis est non faciat. Audientes autem P. <i>nur Eine spätere Hs. Hv’s;</i> cum <i>fügt zu, aber unterpunctirt Cb</i>', '[instead of Cui] qui quod regis est non faciat. Audientes autem P. only one later MS of Hv’s; Cb adds cum, but dotted for deletion'),
            7: D('hanc diffinitiuam sententiam tam ueraciter quam prudenter de regis nomine a Willelmo notho rege Anglie prolatam ei <i>fügt zu nur Eine spätere Hs. Hv’s</i> [<i>unsinnig</i>]', 'only one later MS of Hv’s adds hanc diffinitiuam sententiam tam ueraciter quam prudenter de regis nomine a Willelmo notho rege Anglie prolatam ei [senseless]'),
            8: D('Childerico <i>fügt zu Va;</i> stulte sc., ab eo q. <i>dieselbe Hs. Hv’s</i>', 'Va adds Childerico; stulte sc., ab eo q. the same MS of Hv’s'), 9: D('r. F. <i>Cb</i>', 'r. F. Cb'), 10: D('no. regis <i>Hv; fehlt Cb</i>', 'no. regis Hv; lacking in Cb'),
            11: D('u. r. et d. <i>Cb;</i> uigilant, d. <i>Hv</i>', 'u. r. et d. Cb; uigilant, d. Hv'), 12: D('-tantes <i>Hv</i>', '-tantes Hv'), 13: D('<i>verbessert</i> -mogr. <i>Cb;</i> -mogr. <i>Va Hv</i>', 'corrected to -mogr. Cb; -mogr. Va Hv'), 14: D('Hec hactenus <i>fügt zu Cb</i>', 'Cb adds Hec hactenus')},
  'editorial': ['Liebermann’s footnotes a and b are printed under the ECf column; they are given here as well.']},
 {'code': 'ECfRetr', 'n': '18', 'page': 643,
  'text': '{15}<b><sp>De reis lege dampnatis ad misericordiam</sp></b>{16} <b><sp>regis recurrentibus.</sp></b> Tamen si quis<b>piam</b>{17} forisfactus <b>poposcerit regis</b> misericordiam pro forisfacto suo, timidus mortis uel membrorum <b>perdendorum,</b> potest ei{18} <b>rex</b> lege sue dignitatis condonare, si <b>uult, etiam mortem promeritam.</b>',
  'notes': {'f:g': FG, 15: D('<i>Überschrift</i> [<i>auch in Pl</i>] <i>fehlt Cb; Rubrik für</i> 18, 1 <i>setzt hierher S;</i> Lex de misericordia regis. Paciens et misericors Dominus: ‘Nolo mortem peccatoris’ etc. [<i>Ezech.</i> 33, 11] <i>Lond, wo dies hinter</i> 15, 7 <i>steht</i>',
                                    'heading [also in Pl] lacking in Cb; S puts the rubric for 18, 1 here; Lex de misericordia regis. Paciens et misericors Dominus: ‘Nolo mortem peccatoris’ etc. [Ezek. 33, 11] Lond, where this stands after 15, 7'),
            16: D('r. m. <i>Hv</i>', 'r. m. Hv'), 17: D('quisquam <i>Va;</i> quisnam <i>Cb K Ph;</i> quis regis mi. pro f. s. pop., etsi sit reus mo. uel me. suorum perd. <i>Hv</i>', 'quisquam Va; quisnam Cb K Ph; quis regis mi. pro f. s. pop., etsi sit reus mo. uel me. suorum perd. Hv'),
            18: D('r. ei <i>Hv Lond</i>', 'r. ei Hv Lond')}},
 {'code': 'ECfRetr', 'n': '18a', 'page': 643,
  'text': 'Ipse <b>tamen malefactor</b>{19} faciat{20} rectum in quantumcunque{21} poterit quibus forisfecit{22}, et <b>tradat</b> fideiussores de pace et legalitate tenenda.',
  'notes': {19: D('-torum <i>Hv</i>', '-torum Hv'), 20: D('r. f. <i>Hv Cb Lond</i>', 'r. f. Hv Cb Lond'), 21: D('<i>verbessert aus</i> quantumque <i>Cb</i>', 'corrected from quantumque Cb'), 22: D('foref. <i>Lb Va;</i> forisfactum fuerit et f. t. <i>Hv</i>', 'foref. Lb Va; forisfactum fuerit et f. t. Hv')}},
 {'code': 'ECfRetr', 'n': '18b', 'page': 643,
  'text': 'Si uero{23} <b>fideiussores defecerint,</b> exulabitur a{24} patria.',
  'notes': {23: D('f. u. d., debet exulari <i>Hv</i>', 'f. u. d., debet exulari Hv'), 24: D('<i>so Cb Db Co;</i> de <i>übr.</i>', 'so Cb Db Co; de the others')}},
]
