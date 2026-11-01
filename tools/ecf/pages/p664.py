# Liebermann, Gesetze I pp. 663–664: ECf retr 34,3 (begins p. 663); ECf and ECf retr 35–35,1; Lond 35,1 A–A 2
D = lambda de, en: (de, en)
STAR2_663 = D('qui XVI (septem decim <i>Co</i>) annis regnauit† et <i>fügt zu Lond</i>', 'Lond adds qui XVI (septem decim Co) annis regnauit† et')
FH = D('<i>wie oben</i> 34, 1<i>b</i>', 'as above, 34, 1b')
FI = D('<i>den Retr. beeinflusst vielleicht Will. Malm.</i> Reg. II 183: Cnut leges ab antiquis regibus, et maxime Ethelredo, latas obseruari precepit, in quarum custodiam etiam nunc sub nomine regis Edwardi iuratur, non quod ille statuerit, sed quod obseruarit',
       'the Retr. is perhaps influenced by Will. Malm., Reg. II 183: Cnut leges ab antiquis regibus, et maxime Ethelredo, latas obseruari precepit, in quarum custodiam etiam nunc sub nomine regis Edwardi iuratur, non quod ille statuerit, sed quod obseruarit')
FA = D('<i>falls in der Überschrift des Retr.</i> Dauid <i>ursprünglich fehlte, so meinte sie unter Margaretens Söhnen die <sp>regierenden</sp> Könige von Schottland [oder den gegenwärtigen] und entstand, da deren letzter, David,</i> 1153 <i>starb, vor</i> 1153',
       'if Dauid was originally lacking in the Retr.’s heading, then the heading meant, among Margaret’s sons, the reigning kings of Scotland [or the present one], and it was written before 1153, since the last of them, David, died in 1153')
FB = D('Jaroslaw I. <i>von Kiew, in Französischen Quellen</i> Bullesclot, Juriscloht, Jeresclauus, Georgius sclauus: Coll. Teruan. <i>bei Sdralek</i> Wolfenbüttl. Fragm. 178. 186; Hist. Franc. (<i>Duchesne</i> IV 87C); <i>mein</i> Über Edw. Conf. 38. <i>Vor Cnut floh über Schweden nach Russland auch Olaf der Heilige; Metcalfe</i> Passio Olavi 16',
       'Jaroslav I of Kiev, in French sources Bullesclot, Juriscloht, Jeresclauus, Georgius sclauus: Coll. Teruan. in Sdralek, Wolfenbüttl. Fragm. 178. 186; Hist. Franc. (Duchesne IV 87C); my Über Edw. Conf. 38. Olaf the Saint also fled from Cnut to Russia by way of Sweden; Metcalfe, Passio Olavi 16')
FC = D('<i>vielmehr in Ungarn: Agathe</i>', 'rather in Hungary: Agatha')
FCC = D('† 1093', '† 1093')
STAR = D('<sp>Ireneside</sp> <i>fügt zu Lond</i> (<i>s. o.</i> 34, 2<i>b</i>)', 'Lond adds Ireneside (see above, 34, 2b)')
STAR2 = D('domina Albanie <i>statt</i> r. S. <i>Lond, damit Schottland von England abhängig scheine; wie</i> 35, 1 A 2', 'domina Albanie instead of r. S. Lond, so that Scotland should appear dependent on England; as in 35, 1 A 2')
STAR3 = D('<i>hier interpolirt Lond:</i> [35, 1 A–A 2]', 'here Lond interpolates: [35, 1 A–A 2]')
WHOLE = 'The starred notes (*, **, ***) are printed across the whole page; they are given with both columns.'
MARG = lambda w, d: f'Liebermann prints “{w}” and gives in the outer margin of the ECf retr column the date {d}.'
LOND_ED = 'This passage is not part of ECf or ECf retr: it is one of the additions of the London collection (Leges Anglorum s. XIII in. Londoniis collectae), which Liebermann prints across the page after ECf 35, 1 as an insertion into ECf retr. 35, 1 (35, 1 A). The dictionary cites it as “ECf 35,1 A …”, so it is kept with ECf here.'
SMALL = 'Liebermann prints some words here in smaller type ({w}); they are taken over from {src}, which his margin names ({m}).'
LD = D('<i>fehlt Ld</i>', 'lacking in Ld')
def L(n, text, notes, margin, small, extra=()):
    return {'code': 'ECf', 'n': n.replace(',', '.').replace('. ', '.'), 'page': 664, 'keys': ['ECf ' + n, 'ECf ' + n.replace(', ', ',')],
            'text': text, 'notes': notes, 'margin': margin, 'editorial': [LOND_ED] + ([SMALL.format(w=small[0], src=small[1], m='; '.join(margin))] if small[0] else []) + list(extra)}
CLAUSES = [
 {'code': 'ECf', 'n': '35', 'page': 664,
  'text': '{f:a}Iste supradictus Eadmundus{*}{1} habuit filium{2} quendam, qui uocatus est{3} Eadwardus{4}. Qui, mortuo†† patre, timore regis{5} Cnuti{6} aufugit{7} de ista{8} terra usque ad{9} terram Rugorum, quam nos uocamus Russeiam{10}. Quem rex ipsius{11} terre, Malesclodus{f:b} nomine, ut audiuit et intellexit, quis{12} et unde esset{3}, honeste{14} retinuit eum{15}.',
  'notes': {'f:a': FA, 'f:b': FB, '*': STAR, 1: D('Edm. <i>Hk</i>', 'Edm. Hk'), 2: D('que. f. <i>Cl</i>', 'que. f. Cl'), 3: D('<i>fehlt Cl</i>', 'lacking in Cl'), 4: D('Ædw. <i>Hk</i>', 'Ædw. Hk'),
            5: D('r. C. <i>fehlt S;</i> Cn. r. <i>Hr Cl</i>', 'r. C. lacking in S; Cn. r. Hr Cl'), 6: D('Can. <i>Hk;</i> Chunti <i>Rl</i>', 'Can. Hk; Chunti Rl'), 7: D('aff. <i>Hr</i>', 'aff. Hr'), 8: D('t. i. <i>Hk Hr</i>', 't. i. Hk Hr'),
            9: D('in <i>Hr</i>', 'in Hr'), 10: D('Ruffe. <i>Cl</i>', 'Ruffe. Cl'), 11: D('illius <i>Hr</i>', 'illius Hr'), 12: D('esset <i>fügt zu Hk S Hr Cl</i>', 'Hk S Hr Cl add esset'), 14: D('qui h. e. r. <i>S</i>', 'qui h. e. r. S'), 15: D('<i>fehlt Cl Hr</i>', 'lacking in Cl Hr')},
  'editorial': ['Liebermann prints his note letter a before “Iste”, level with the heading of ECf retr 35, to which his note a refers.',
                'There is no note 13 in the ECf column of this page: Liebermann’s numbering goes from 12 to 14.', MARG('mortuo††', '††1016'), WHOLE]},
 {'code': 'ECf', 'n': '35.1', 'page': 664,
  'text': 'Et ipse Ædwardus{16} accepit ibi{f:c} uxorem ex{17} nobili genere, de qua ortus est ei Eadgarus{18} aðeling{19} et Margareta{f:cc} regina{**} Scotie et Cristina{20} soror eius.{***}',
  'notes': {'f:c': FC, 'f:cc': FCC, '**': STAR2, '***': STAR3, 16: D('Ed. <i>Hk S Hr</i>', 'Ed. Hk S Hr'), 17: D('<i>fehlt S Hr Cl</i>', 'lacking in S Hr Cl'), 18: D('Ed. <i>Hk;</i> Æd. <i>S</i>', 'Ed. Hk; Æd. S'),
            19: D('adþe. <i>Rl;</i> eþe. <i>S;</i> ade. <i>Cl Hr</i>', 'adþe. Rl; eþe. S; ade. Cl Hr'), 20: D('-iana <i>Hr;</i> Christiana <i>S Cl</i>', '-iana Hr; Christiana S Cl')},
  'editorial': [WHOLE]},
 L('35, 1 A', 'Fuitque{1} predicta Margareta generosa{f:d} ualde et optima, scilicet ex parte patris ex nobili genere et sanguine regum Anglorum-Britonum{f:e}{2}, ex parte uero matris ex genere et sanguine regum Rugorum; sanctissimisque{3} antecessoribus suis in bonis et laudabilibus et{4} insignibus{5} actibus consimilis, preclara effulsit.',
   {'f:d': D('<i>ausser Margaretens Heiligkeit weiss der Londoner hier nichts Eigenes; er verficht weibliche Thronfolge: Eleonore von Bretagne, nicht Johann, hätte</i> de iure <i>England erben müssen; der Schottenkönig sei</i> uerus heres ultimi Edwardi; <i>mein</i> Über Leg. Angl. <i>S.</i> 66. 69',
              'apart from Margaret’s sanctity the Londoner knows nothing of his own here; he champions female succession: Eleanor of Brittany, not John, ought de iure to have inherited England; the King of Scots, he says, is uerus heres ultimi Edwardi; my Über Leg. Angl. pp. 66. 69'),
    'f:e': D('<i>der Chronist von Lewes componirt</i> Norm(an)-Angli; <i>hinter</i> Liber de Hyda <i>p.</i> 296', 'the chronicler of Lewes composes Norm(an)-Angli; after Liber de Hyda p. 296'),
    1: D('Fuit autem M. p. <i>Ld</i>', 'Fuit autem M. p. Ld'), 2: D('et Bryt. <i>Ld</i>', 'et Bryt. Ld'), 3: D('-mis <i>Co Or Ld</i>', '-mis Co Or Ld'), 4: D('ac <i>Co;</i> et i. <i>fehlt Ld</i>', 'ac Co; et i. lacking in Ld'), 5: D('-gnis <i>K</i>', '-gnis K')},
   ['ECf. retr. 35. 35, 1'], ('“ex genere”, “Rugorum”', 'ECf retr 35 and 35, 1')),
 L('35, 1 A 1', 'Erat enim de iure post decessum Eadgari{6} æðeling, fratris sui, uerus heres ultimi† regis Edwardi de corona tocius regni predicti{7}. Sed instinctu{8}, petitione et uoluntate boni regis Edwardi, propinqui{f:f} [ue]stri{9}, aliter mutatum est: qui uobis{10} coronam tocius regni predicti dedit et regnum predictum uobis{11} iurare fecit; qui peroptime equitatem et scientiam et{12} iustitiam probitatemque uestram{13} nouit.',
   {'f:f': D('<i>wie o.</i> 32 A 8', 'as above, 32 A 8'), 6: D('Ed. ad. <i>K;</i> Ed. athelinge <i>Ld</i>', 'Ed. ad. K; Ed. athelinge Ld'), 7: D('dedit <i>fügt zu Co Or</i>', 'Co Or add dedit'), 8: D('et <i>fügt zu K</i>', 'K adds et'),
    9: D('nostri <i>Hss.</i>', 'nostri MSS'), 10: D('c. nobis <i>Ld</i>', 'c. nobis Ld'), 11: D('nobis <i>Or Ld</i>', 'nobis Or Ld'), 12: LD, 13: D('nostram <i>Co Or Ld;</i> ueram <i>K</i>', 'nostram Co Or Ld; ueram K')},
   ['ebd. 34, 2e', '34, 1a'], ('“Eadgari æðeling”, “ultimi regis Edwardi”, “regis Edwardi”, “coronam”, “regni”', 'ECf retr 34, 2e and 34, 1a'),
   ['The dagger after “ultimi” refers to Liebermann’s marginal reference “ebd. 34, 2e” (ECf retr 34, 2e).', 'In “[ue]stri” the square brackets are Liebermann’s: the manuscripts read “nostri” (note 9).']),
 L('35, 1 A 2', 'Princeps uero Albanie duxit eam in uxorem casu fortuito. Picti enim Albanie{12} a Picto† duce uocantur, Scotti uero Albanie a Scotto{f:g} duce nuncupantur{12}. Est enim Albania pars†† monarchie regni huius, quod olim uocabatur regnum Britannie. Dicuntur{14} enim et uocantur Britones a Bruto rege, qui Troianus fuit, ex quo regnum uniuersum nomen suscepit. Britones enim quasi{15} Bruti Troiani sunt; et uenerunt et exierunt olim a Troia{f:h} magna.',
   {'f:g': D('<i>nicht bei</i> Galfr.', 'not in Geoffrey'), 'f:h': D('<i>o.</i> 32 B 12<i>a stellte der Londoner nur</i> London <i>als Trojas Fortsetzung dar</i>', 'above, 32 B 12a, the Londoner presented only London as Troy’s continuation'),
    12: LD, 14: D('Di.—magna <i>fehlt Ld</i>', 'Di.—magna lacking in Ld'), 15: D('qui <i>K</i>', 'qui K')},
   ['Galf. Mon. VI 5', 'I 16'], ('', ''),
   ['The dagger after “Picto” and the double dagger after “pars” refer to Liebermann’s marginal references: † Galf. Mon. VI 5, †† I 16 (Geoffrey of Monmouth).', 'Liebermann prints his note 12 (“fehlt Ld”) three times in this passage.']),

 {'code': 'ECfRetr', 'n': '34.3', 'page': 663, 'pages': [664],
  'text': 'Sed postquam rex Eadwardus{3} uenit ad regnum, consilio baronum <b>Anglie</b>{31} legem LXVIII{27} <sp>annis</sp> <b>sopitam excitauit, excitatam</b> <sp>reparauit</sp>, <b>reparatam decorauit</b>{32}<b>, decoratam</b> <sp>confirmauit</sp>; <b>confirmata uero</b> uocata{23} est lex Eadwardi{33} regis, <b>non</b>{f:i} <b>quod</b>{34} <b>ipse primus</b>{35} <b>adinuenisset</b>{36} <b>eam, sed, cum pretermissa fuisset et</b>{37} <b>obliuioni penitus tradita</b>{38} <b>a diebus</b> aui sui <b>regis</b>{30} Eadgari{**}<b>, qui primus</b>{39} <b>inuentor eius fuisse dicitur,</b> usque ad sua tempora, <b>uidelicet</b>{40} <b>ut predictum est,</b> LXVIII annis{41} <b>post dies</b> [[pb:664]]<b>ipsius</b> Eadgari†, <b>ipse</b>{1/664} Eadwardus, quia <b>iusta erat</b>{2/664} et honesta, <b>a</b>{3/664} <b>profunda</b>{4/664} <b>abysso extraxit</b>{5/664} <b>eam</b>{6/664} <b>et renouauit et</b>{1/664} <b>ut suam obseruandam</b>{7/664} <b>contradidit</b>{8/664}<b>.</b>',
  'notepages': {f'{i}/664': 664 for i in range(1, 9)},
  'notes': {'f:h': FH, 'f:i': FI, '**': STAR2_663, 3: D('Ed. <i>Cb</i>', 'Ed. Cb'), 23: D('<i>fehlt Va</i>', 'lacking in Va'), 27: D('quadraginta octo <i>Hv</i>', 'quadraginta octo Hv'), 30: D('<i>fehlt Hr</i>', 'lacking in Hr'),
            31: D('l. A. <i>Dc</i>', 'l. A. Dc'), 32: D('d. d. <i>fehlt Dc</i>', 'd. d. lacking in Dc'), 33: D('Ed. <i>Cb;</i> r. E. <i>Lb Va Dc Ph Lond</i>', 'Ed. Cb; r. E. Lb Va Dc Ph Lond'), 34: D('quia <i>Hv</i>', 'quia Hv'),
            35: D('inuen. e. pr. <i>Hv</i>', 'inuen. e. pr. Hv'), 36: D('aduen. <i>Co</i>', 'aduen. Co'), 37: D('<i>fehlt Hv;</i> et o. p. t. <i>fehlt Dc</i>', 'lacking in Hv; et o. p. t. lacking in Dc'), 38: D('data <i>Hr;</i> dedita <i>übr.</i>', 'data Hr; dedita the others'),
            39: D('prius <i>Hv</i>', 'prius Hv'), 40: D('scil., ut supra di. est, octodecim <i>Hv</i>', 'scil., ut supra di. est, octodecim Hv'), 41: D('anni <i>Co</i>', 'anni Co'),
            '1/664': D('<i>fehlt Hv</i>', 'lacking in Hv'), '2/664': D('et hon. erat <i>Hv</i>', 'et hon. erat Hv'), '3/664': D('et <i>Va Ph</i>', 'et Va Ph'), '4/664': D('-do <i>Cb</i>', '-do Cb'),
            '5/664': D('eam ex. <i>Lond</i>', 'eam ex. Lond'), '6/664': D('et eam reuocauit ut <i>Hv</i>', 'et eam reuocauit ut Hv'), '7/664': D('conseru. <i>Cb</i>', 'conseru. Cb'), '8/664': D('trad. <i>Hv</i>', 'trad. Hv')},
  'editorial': ['Liebermann’s numbering of the notes in the ECf retr column starts again at 1 on p. 664: the notes 1–8 to the part of this clause on p. 664 are distinct from the notes on p. 663.',
                'Beside the beginning of this clause Liebermann gives the date 1042 in the margin; beside the starred note (**, printed across p. 663) the dates †959–75; and beside “Eadgari†” on p. 664 the date †975.',
                'Liebermann’s note 30 (“fehlt Hr”) names a manuscript of ECf, not of the Retractator; it may be a misprint for Hv.',
                'The note on the London collection’s addition (**) is printed across the whole of p. 663; it is given with both columns.']},
 {'code': 'ECfRetr', 'n': '35', 'page': 664,
  'text': '<b>De</b>{9} <b>aduentu s. Margarete, matris</b>{f:a} <b>regis</b>{10} <b>Scotie, et Ædgari æþeling</b>{11}<b>, fratris eius, in Angliam, de quo sanctus Edwardus rex heredem suum facere uoluit. (Quomodo</b>{12} <b>s. M-a, mater</b>{f:a} Dauid{13} <b>r. S., cum patre et matre, sorore et fratre Eadgaro edelingo, de—her. regni sui f. u., in A. uenit.)</b>{14} Iste <b>(uero</b>{15}<b>) prefatus</b> Eadmundus{*} habuit{16} quendam filium Eadwardum <b>nomine.</b> Qui <b>mox</b>{17}, patre†† mortuo, timore regis{18} Cnuti aufugit ad <b>regnum</b> Rugorum{19}, <b>quod nos melius</b> uocamus{20} Russiam. Quem{21} rex terre, Malesclodus{22} nomine, ut <b>cognouit,</b> quis esset, honeste retinuit.',
  'notes': {'f:a': FA, 'f:b': FB, '*': STAR, 9: D('<i>so Pl S;</i> Quomodo—uenit <i>übr.; Überschrift fehlt Cb Lond</i>', 'so Pl S; Quomodo—uenit the others; the heading is lacking in Cb Lond'),
            10: D('regi <i>Pl;</i> Scotorum <i>Ba</i>', 'regi Pl; Scotorum Ba'), 11: D('ædþ. <i>Pl;</i> æde. <i>S</i>', 'ædþ. Pl; æde. S'), 12: D('Quod <i>Va</i>', 'Quod Va'), 13: D('r. D. <i>Va Hv</i>', 'r. D. Va Hv'),
            14: D('et postea Willelmum ducem heredem suum fecit, eo quod de Ædgaro facere nequiuit <i>fügt zu Pl S</i> [<i>vgl. Rubrik</i> 35, 2]', 'Pl S add et postea Willelmum ducem heredem suum fecit, eo quod de Ædgaro facere nequiuit [cf. the rubric of 35, 2]'),
            15: D('<i>aus Lb Ba; fehlt übrigen</i>', 'from Lb Ba; lacking in the others'), 16: D('-uerit <i>Ph</i>', '-uerit Ph'), 17: D('<i>fehlt Dc</i>', 'lacking in Dc'), 18: D('C. r. <i>Ph</i>', 'C. r. Ph'),
            19: D('Rog. <i>Dc;</i> Dog. <i>Hv</i>', 'Rog. Dc; Dog. Hv'), 20: D('dicimus <i>Dc</i>', 'dicimus Dc'), 21: D('Quoniam <i>Lond</i>', 'Quoniam Lond'), 22: D('-chlodus <i>Va;</i> -clotus <i>Lond;</i> -scoldus <i>Cb Hv</i>', '-chlodus Va; -clotus Lond; -scoldus Cb Hv')},
  'editorial': ['The heading has two forms: “De aduentu … facere uoluit” in Pl S, and “Quomodo … in A. uenit” in the other manuscripts (note 9); Liebermann prints the second in brackets after the first. In it “Dauid” is printed in ordinary type.',
                MARG('patre††', '††1016'), WHOLE]},
 {'code': 'ECfRetr', 'n': '35.1', 'page': 664,
  'text': '<b>Qui de</b> nobili <sp>progenie ibidem</sp> <b>duxit</b> uxorem, de qua <b>natus</b> est ei Eadgarus edeling{23} et Margareta, <b>que fuit</b>{f:cc} <b>postea</b>{17} regina{**} Scotie{24}, et Cristina{25}, soror eius.{***}',
  'notes': {'f:c': FC, 'f:cc': FCC, '**': STAR2, '***': STAR3, 17: D('<i>fehlt Dc</i>', 'lacking in Dc'), 23: D('eadel. <i>K;</i> eadling <i>Co;</i> ad. <i>Hv</i>', 'eadel. K; eadling Co; ad. Hv'),
            24: D('Scotcie <i>Cb</i>', 'Scotcie Cb'), 25: D('Chr. <i>Lb Va;</i> Christiana <i>Hv Lond</i>', 'Chr. Lb Va; Christiana Hv Lond')},
  'editorial': [WHOLE, 'The London collection’s interpolation (***) follows on this page as 35, 1 A–A 2 (cited as ECf 35,1 A …).']},
]
