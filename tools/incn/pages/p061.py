# Gesetze I p. 61: In Cn III 40 beside Alfred 19–19,2 (also printed in full on p. 613); In Cn I 5,2e beside Alfred 20
D = lambda de, en: (de, en)
LBS = lambda r: D(f'{r} <i>Lb S</i>', f'{r} Lb S')
COLUMNS = [
 {'clause': 'Af_19', 'incn': 'III 40', 'page': 61,
  'text': 'Si quis alii{1} arma sua prestiterit, et <sp>ille cui prestita sunt</sp> inde hominem occiderit,',
  'notes': {1: LBS('alicui')}},
 {'clause': 'Af_19-1', 'incn': 'III 40', 'page': 61,
  'text': 'ipse qui arma praestitit{2} tertiam partem pretii et forisfacturę persoluat,',
  'notes': {2: LBS('-terit')}},
 {'clause': 'Af_19-2', 'incn': 'III 40', 'page': 61,
  'text': 'aut se{3} <sp>purget</sp>, quod non fuit <sp>consilium nec uoluntas eius</sp> . . . . . .',
  'notes': {3: D('p. se <i>Cb</i>', 'p. se Cb')}},
 {'clause': 'Af_20', 'incn': 'I 5.2e', 'page': 61,
  'text': 'Si quis commendauerit alterius{4} monacho pecuniam <b>aut aliquid tale</b>{5} <sp>ad custodiendum</sp> sine licentia <b>prelati</b> sui, et <sp>monachus illud perdiderit, sit illi perditum qui</sp> sine licentia <b>prelati</b> <sp>eius</sp>{6} <sp>monacho commendauit</sp> . . . .',
  'notes': {4: D('alicui <i>T</i>', 'alicui T'), 5: D('aliud <i>Cb</i>', 'aliud Cb'), 6: D('sui <i>Lb S;</i> <i>fehlt Cb</i>', 'sui Lb S; lacking in Cb')},
  'editorial': ['In the column of the Instituta Cnuti Liebermann labels this passage “I 5, 2a”; in his list of its chapters (Gesetze I, p. 612) it is I 5, 2e, its place after I Cnut 5, 2d. It is given here as In Cn I 5.2e.']},
]
