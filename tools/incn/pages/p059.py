# Gesetze I p. 59: In Cn II 59a–c, beside Alfred 15–17
D = lambda de, en: (de, en)
STAR = D('<i>Vgl.</i> Transactions R. Historical Soc., N.S. VII (1893), 77. — <i>Hss.:</i> H (<i>Textus Roffensis</i>) <i>um</i> 1140; Rl (<i>Oxford, Bodley Rawlinson C</i> 641) <i>um</i> 1200; T (<i>Titus A</i> 27) <i>um</i> 1225; Cb (<i>Paris, Bibl. nat., Latin</i> 4771, <i>einst Colbert</i>) <i>um</i> 1160; Di (<i>Oxford, Bodley Digby</i> 13) <i>um</i> 1170; Lb (<i>Lambeth</i> 118) <i>um</i> 1200; S (<i>British Mus. Harley</i> 746) <i>um</i> 1300; Pl (<i>Phillipps</i> 8078, <i>seit</i> 1895 <i>bei H. S. Nichols &amp; Co. zu London</i>) <i>um</i> 1300; Ct (<i>Cambridge, Trinity Coll. R</i> 5, 42) <i>um</i> 1350.',
         'Cf. Transactions R. Historical Soc., N.S. VII (1893), 77. — Manuscripts: H (Textus Roffensis) c. 1140; Rl (Oxford, Bodley Rawlinson C 641) c. 1200; T (Titus A 27) c. 1225; Cb (Paris, Bibl. nat., Latin 4771, formerly Colbert’s) c. 1160; Di (Oxford, Bodley Digby 13) c. 1170; Lb (Lambeth 118) c. 1200; S (British Mus. Harley 746) c. 1300; Pl (Phillipps 8078, since 1895 with H. S. Nichols & Co. in London) c. 1300; Ct (Cambridge, Trinity Coll. R 5, 42) c. 1350.')
CB5 = D('<i>fehlt Cb</i>', 'lacking in Cb')
COLUMNS = [
 {'clause': 'Af_15', 'incn': 'II 59a', 'page': 59,
  'text': '{*}. . . . Qui ante archiepiscopum pugnauerit{1} aut arma{2} extraxerit, <b>quadraginta</b> solidos emendet; <sp>et</sp>{3} qui hoc{4} ante episcopum uel comitem <sp>fecerit</sp>, <b>uiginti</b> sol. emendet.{5}',
  'notes': {'*': STAR, 1: D('<i>fehlt Di Lb S</i>', 'lacking in Di Lb S'), 2: D('trax. arma <i>Lb</i>', 'trax. arma Lb'),
            3: D('et—emendet <i>am unteren Rande H, fehlt Di Lb S</i>', 'et—emendet in the lower margin H, lacking in Di Lb S'), 4: D('ante e. uel c. hoc <i>Cb</i>', 'ante e. uel c. hoc Cb'), 5: CB5}},
 {'clause': 'Af_16', 'incn': 'II 59b', 'page': 59,
  'text': 'Si quis uaccam aut equam, <sp>quam Angli uocant stodmere</sp>, et uitulum uel{6} pullum <sp>cum eis furatus fuerit, pullum soluat</sp> <b>duodecim denariis</b> <sp>et uitulum similiter</sp> et matres secundum pretium earum.',
  'notes': {6: D('et <i>H Di;</i> uel p. <i>fehlt Lb S</i>', 'et H Di; uel p. lacking in Lb S')}},
 {'clause': 'Af_17', 'incn': 'II 59c', 'page': 59,
  'text': 'Si quis commendauerit <sp>aliquem</sp>{5} <sp>hominem alicui homini</sp> <b>non parenti</b>, et ipse{5} <sp>commendatus perierit in ipsa commendatione</sp>, et aliquis eum calumniauerit, <sp>quod dolositate eius</sp>{7} <sp>perierit</sp>, purget se . . . .',
  'notes': {5: CB5, 7: D('sua <i>Cb</i>', 'sua Cb')}},
]
