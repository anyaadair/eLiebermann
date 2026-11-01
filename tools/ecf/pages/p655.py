# Liebermann, Gesetze I p. 655: ECf and ECf retr 32,3; Lond 32 A–A 8 (an insertion into ECf retr; cited as ECf 32 A …)
D = lambda de, en: (de, en)
LOND_ED = 'This passage is not part of ECf or ECf retr: it is one of the additions of the London collection (Leges Anglorum s. XIII in. Londoniis collectae), which Liebermann prints in smaller type across the page as an insertion into ECf retr. 32 (32 A–E, pp. 655–660). The dictionary cites it as “ECf 32 A …”, so it is kept with ECf here.'
SMALL = 'The words in smaller type in Liebermann’s print ({w}) are taken over from ECf {src}; his margin gives the source.'
STAR = D('<i>hier schaltet Lond in die Retr.</i> 32 A—E, <i>bis S.</i> 660, <i>ein:</i>', 'here Lond inserts 32 A–E into the Retr., up to p. 660:')
FA = D('<i>nicht ganz übernahm der Sheriff das Amt des Angelsächs.</i> ealdorman <i>und nicht jedem</i> ealdor <i>folgte ein</i> gerefa', 'the sheriff did not entirely take over the office of the Anglo-Saxon ealdorman, and not every ealdor was followed by a gerefa')
B = D('Brut. <i>Ld</i>', 'Bryt. Ld')
B = D('Bryt. <i>Ld</i>', 'Bryt. Ld')
LD = D('<i>fehlt Ld</i>', 'lacking in Ld')
FD = D('<i>ähnlich redet er</i> Wl art. retr. 6', 'he speaks similarly at Wl art. retr. 6')
CLAUSES = [
 {'code': 'ECf', 'n': '32.3', 'page': 655,
  'text': 'Et sicut modo uocantur greues{1} qui{2} habent prefecturas{3} super alios{4}, ita{5} tunc temporis uocabantur{f:a} alderman{6}, non propter senectutem sed propter sapientiam{7}.{*}',
  'notes': {'f:a': FA, '*': STAR, 1: D('reues <i>Ad Do</i>', 'reues Ad Do'), 2: D('modo <i>fügt zu Hk</i>', 'Hk adds modo'), 3: D('-ram <i>Hk</i>', '-ram Hk'), 4: D('illos <i>Ad</i> (<i>nicht Do</i>)', 'illos Ad (not Do)'),
            5: D('primi <i>Hk</i>', 'primi Hk'), 6: D('eld. <i>Rl;</i> elderemen <i>S;</i> aldermanni <i>Hk</i>', 'eld. Rl; elderemen S; aldermanni Hk'), 7: D('scientiam <i>Hk</i>', 'scientiam Hk')},
  'editorial': ['Liebermann’s asterisk introduces the London collection’s insertion into the Retr. here, 32 A–E.']},
 {'code': 'ECfRetr', 'n': '32.3', 'page': 655,
  'text': 'Et sicut modo uocantur greue{1} qui super alios prefecturas habent, ita <b>apud Anglos</b>{2} <b>antiquitus</b> uocabantur alderman, <b>quasi seniores,</b> non propter senectutem, <b>cum quidam</b>{3} <b>adolescentes essent,</b> sed propter sapientiam{4}.{*}',
  'notes': {'f:a': FA, '*': STAR, 1: D('greiue <i>Hv</i>', 'greiue Hv'), 2: D('qui <i>fügt zu Hv</i>', 'Hv adds qui'), 3: D('quid’ <i>Co</i>', 'quid’ Co'), 4: D('<i>folgt sofort</i> XXXVI De latronibus <i>Db L</i>', 'XXXVI De latronibus follows at once Db L')}},

 {'code': 'ECf', 'n': '32 A', 'page': 655, 'keys': ['ECf 32 A'],
  'text': 'Et similiter olim apud Britones{1}, temporibus Romanorum, in regno isto{f:b} Britannie{1} uocabantur senatores{f:bb} qui postea temporibus Saxonum, ut predictum est, uocabantur aldermanni, non propter etatem sed propter sapientiam et dignitatem, cum quidem adolescentes essent, iuris periti{1*} et super hoc experti et{2}, ut uerum fatear, non{2} ignari.',
  'margin': ['ECf. 32, 3'],
  'notes': {'f:b': D('<i>vgl.</i> Wl art. retr., Inscr.<i>d</i>', 'cf. Wl art. retr., Inscr., note d'),
            'f:bb': D('<i>er betont auch sonst die</i> Alderman-Würde, <i>die schon Will. fil. Stephani</i> senatoriam dignitatem <i>nennt</i> (<i>bes. das</i> Wardimot <i>o. S.</i> 525<i>b</i>); <i>vgl. über</i> aldermen <i>um</i> 1200 <i>Bateson</i> Engl. hist. rev. 1902, 507', 'he stresses the dignity of alderman elsewhere too, which William fitz Stephen already calls senatoriam dignitatem (esp. the Wardimot, above p. 525, note b); on aldermen around 1200 cf. Bateson, Engl. hist. rev. 1902, 507'),
            1: B, '1*': D('tamen <i>fügt zu Ld</i>', 'Ld adds tamen'), 2: D('Et <i>neuer Satz ohne</i> n. i. <i>Ld</i>', 'Et a new sentence, without n. i. Ld')},
  'editorial': [LOND_ED, SMALL.format(w='uocabantur aldermanni, non propter, sed propter sapientiam, cum quidem adolescentes essent', src='retr. 32, 3 (marked with a dagger)')]},
 {'code': 'ECf', 'n': '32 A 1', 'page': 655, 'keys': ['ECf 32 A 1'],
  'text': 'Habent etiam aldermanni in ciuitatibus regni huius in balliuis{f:c} suis et in burgis{f:d} clausis et muro uallatis et in castellis eandem dignitatem et potestatem et modum, qualem et{3} habent prepositi hundredorum et wapentagiorum{4} in balliuis suis sub uicecomit[ibus{5}] regis per uniuersum regnum.',
  'notes': {'f:c': D('warda <i>heisst</i> 32 B 9 <i>der Bezirk des</i> alderman. <i>Ihn stellt der Londoner in Parallele mit dem</i> hundredes gerefa.', 'at 32 B 9 the alderman’s district is called warda. The Londoner sets him in parallel with the hundredes gerefa.'),
            'f:d': FD, 3: LD, 4: D('-tachi. <i>Ld</i>', '-tachi. Ld'), 5: D('-mite <i>Ld;</i> uic.’ <i>Hss.</i>', '-mite Ld; uic.’ MSS')}, 'editorial': [LOND_ED]},
 {'code': 'ECf', 'n': '32 A 2', 'page': 655, 'keys': ['ECf 32 A 2'],
  'text': 'Debent enim{6} leges et libertates et iura et pacem regis et iustas consuetudines regni et antiquas{f:e}, a bonis predecessoribus approbatas, inuiolabiliter et sine dolo et sine dilatione modis omnibus pro posse suo seruare.',
  'notes': {'f:e': D('<i>ähnlich ebd.</i> 1. 7. 11; <i>u.</i> 32 B 13', 'similarly ibid. 1. 7. 11; below 32 B 13'), 6: D('et <i>fügt zu Ld</i>', 'Ld adds et')}, 'editorial': [LOND_ED]},
 {'code': 'ECf', 'n': '32 A 3', 'page': 655, 'keys': ['ECf 32 A 3'],
  'text': 'Cum aliquid uero inopinatum uel dubium uel malum contra regnum uel contra coronam domini regis forte in balliuis suis subito emerserit, debent statim et{7} incontinenti pulsatis campanis, quod Anglici uocant motbele{8}, congregare et conuocare{f:f} communas{3} omnes et uniuersas{9}, quod Anglici dicunt folkesmoth{10}, scilicet uocatio et congregatio populorum et gentium omnium, quia ibi{11} omnes conuenire debent et uniuersi{f:g}, qui sub protectione et pace domini regis degunt et consistunt in regno predicto.',
  'notes': {'f:f': D('<i>dieser Traum vom Londoner</i> Folcesmot <i>als Reichscentrum, ohne dass König, Adel, Prälaten selbständig daneben treten, entsprang vielleicht aus Bestrebungen der City</i> 1191 <i>ff. Das</i> husting i Lundene <i>identificirt mit</i> witene-imot <i>auch Layamon v.</i> 11542', 'this dream of the London folkmoot as the centre of the realm, without king, nobility or prelates standing independently beside it, perhaps arose from the aspirations of the City from 1191 on. Layamon v. 11542 too identifies the husting i Lundene with the witene-imot'),
            'f:g': D('<i>aus</i> ECf. retr. 15, 7 <i>auch</i> Wl art. retr. 3', 'from ECf. retr. 15, 7, also Wl art. retr. 3'),
            7: D('et i. <i>fehlt Ld</i>', 'et i. lacking in Ld'), 8: D('mothb. <i>Co;</i> motbel <i>ohne</i> cong. et <i>Ld</i>', 'mothb. Co; motbel without cong. et Ld'), 3: LD, 9: D('-sos <i>Ld</i>', '-sos Ld'),
            10: D('folcmote i. e. uoc. <i>Ld</i>', 'folcmote i. e. uoc. Ld'), 11: D('ipsi <i>Or</i>', 'ipsi Or')},
  'editorial': [LOND_ED, 'Liebermann’s letter a after “motbele” is his upright a (Erklärungen).']},
 {'code': 'ECf', 'n': '32 A 4', 'page': 655, 'keys': ['ECf 32 A 4'],
  'text': 'Et ibi prouidere debent indempnitatibus corone regni huius per commune consilium, et ibi prouidendum{f:d} est ad insolentiam maleficorum{12} reprimendam ad utilitatem regni.',
  'notes': {'f:d': FD, 12: D('malefactorum <i>Ld</i>', 'malefactorum Ld')}, 'editorial': [LOND_ED]},
 {'code': 'ECf', 'n': '32 A 5', 'page': 655, 'keys': ['ECf 32 A 5'],
  'text': 'Statutum est enim, quod ibi debent populi{13} omnes et gentes uniuerse singulis annis, semel in anno scilicet, conuenire, scilicet in capite kalendarum Maii, et se fide{f:h} et sacramento non{f:i} fracto ibi in unum et insimul{14} confederare et consolidare sicut coniurati{f:k} fratres ad defendendum regnum contra alienigenas et contra inimicos, una cum domino suo rege, et terras et honores illius omni fidelitate cum eo seruare, et quod illi ut domino suo regi intra et extra regnum uniuersum Britannie{1} fideles esse uolunt.',
  'notes': {'f:h': D('<i>ähnlich ebd.</i> 2. 9. <i>Der Treu- und Friedenseid, in der Grafschaft</i> 1166, 1181, 1195, 1199, 1205 <i>neu verordnet, kommt auch im Londoner Folcesmot vor</i>', 'similarly ibid. 2. 9. The oath of fealty and peace, newly ordained in the shire in 1166, 1181, 1195, 1199, 1205, also occurs in the London folkmoot'),
            'f:i': D('<i>entnommen wohl technischer Rechtssprache, in der es</i> ungestabten Eid <i>bedeutet; der Londoner meint aber</i> unverbrüchlich', 'probably taken from technical legal language, in which it means an oath not sworn with the staff; but the Londoner means unbreakable'),
            'f:k': D('<i>nicht</i> Eidbrüder, <i>sondern</i> geschworene Volksgenossen, <i>auch u.</i> 32 C 1; <i>vgl. o. S.</i> 490<i>n</i>', 'not sworn brothers, but sworn fellow-countrymen, also below 32 C 1; cf. above, p. 490, note n'),
            13: D('<i>so Co Ld;</i> o. p. <i>K</i>', 'so Co Ld; o. p. K'), 14: D('simul <i>Ld</i>', 'simul Ld'), 1: B},
  'editorial': [LOND_ED, 'Liebermann’s letter a after “Maii” is his upright a (Erklärungen).']},
 {'code': 'ECf', 'n': '32 A 6', 'page': 655, 'keys': ['ECf 32 A 6'],
  'text': 'Ita debent facere omnes principes et comites, et simul iurare coram episcopis regni in folkesmoth{15}; et similiter omnes proceres regni et milites et liberi homines uniuersi totius regni Britannie{1} facere debent in pleno folkesmot{16} fidelitatem{f:l} domino regi, ut predictum est, coram episcopis regni.',
  'notes': {'f:l': D('<i>ähnlich</i> Wl art. retr. 2', 'similarly Wl art. retr. 2'), 15: D('folcmote <i>Ld</i>', 'folcmote Ld'), 16: D('-oth <i>K;</i> folcmote <i>Ld</i>', '-oth K; folcmote Ld'), 1: B}, 'editorial': [LOND_ED]},
 {'code': 'ECf', 'n': '32 A 7', 'page': 655, 'keys': ['ECf 32 A 7'],
  'text': 'Hanc legem inuenit Arturus{17}, qui{f:m} quondam fuit inclitissimus rex Britonum{1}, et ita consolidauit et confederauit regnum Britannie{1} uniuersum semper in unum; huius legis{f:n} auctoritate expulit Arturus{17} predictus Saracenos{f:o} et inimicos a regno.',
  'notes': {'f:m': D('<i>den Namen schöpft der Londoner aus</i> Galfr. v. Monmouth, <i>den er</i> 32 D <i>abschreibt</i>', 'the Londoner takes the name from Geoffrey of Monmouth, whom he copies at 32 D'),
            'f:n': D('<i>dieselbe Phrase zu anderer Fabel u.</i> 32 A 14', 'the same phrase for another fable below, 32 A 14'), 'f:o': D('Saracenen <i>nennt Franz. Literatur um</i> 1200 <i>die Heiden aller Länder</i>', 'French literature around 1200 calls the heathen of all lands Saracens'),
            17: D('Arthu. <i>Ld</i>', 'Arthu. Ld'), 1: B}, 'editorial': [LOND_ED]},
 {'code': 'ECf', 'n': '32 A 8', 'page': 655, 'keys': ['ECf 32 A 8'],
  'text': 'Lex enim ista diu sopita fuit et sepulta, donec Edgarus{f:p} rex Anglorum, qui fuit auus Edwardi regis, propinqui uestri{f:q}, illam excitauit et in{18} lucem erexit, et illam per totum regnum firmiter obseruare{19} fecit et precepit.',
  'margin': ['ECf. 34, 3'],
  'notes': {'f:p': D('<i>er sagt von</i> Eadgar <i>aus, was</i> ECf. <i>und</i> 13, 1 A 2 <i>von</i> Eadward III.', 'he says of Edgar what ECf. and 13, 1 A 2 say of Edward III.'), 'f:q': D('<i>ebenso</i> 32 E 6. 35, 1 A 1; Wl art. retr. 4', 'likewise 32 E 6. 35, 1 A 1; Wl art. retr. 4'),
            18: D('er. in lu. <i>Ld</i>', 'er. in lu. Ld'), 19: D('obseruari praec., <i>ohne</i> f. et <i>Ld</i>', 'obseruari praec., without f. et Ld')},
  'editorial': [LOND_ED, SMALL.format(w='Lex, diu sopita, auus Edwardi regis, excitauit, obseruare', src='34, 3')]},
]
