# Gesetze I p. 79: In Cn III 9–11 beside Alfred 44–46
D = lambda de, en: (de, en)
EM11 = D('<i>hier und im Folgenden abgekürzt H; was bald</i> emendet, <i>bald</i> emendetur <i>auflöst Di; fehlt Cb</i>', 'abbreviated here and in what follows H; which Di expands now as emendet, now as emendetur; lacking in Cb')
COLUMNS = [
 {'clause': 'Af_44', 'incn': 'III 9', 'page': 79,
  'text': '<sp>Emendatio uulnerati capitis est</sp>{1}: si ossa <b>sine</b> <sp>foramine</sp> sunt{2}, XXX sol.',
  'notes': {1: D('talis <i>fügt zu Cb</i>', 'Cb adds talis'), 2: D('<i>aus Cb; fehlt übrigen</i>', 'from Cb; lacking in the others')}},
 {'clause': 'Af_44-1', 'incn': 'III 9', 'page': 79,
  'text': '<sp>Et si exterior</sp>{3} <sp>os sit perforatum</sp>{4}, XV sol.',
  'notes': {3: D('-rius <i>S Ct;</i> or <i>übergeschr. H</i>', '-rius S Ct; or written above the line H'), 4: D('<i>so Cb;</i> for. <i>übrige</i>', 'so Cb; for. the others')}},
 {'clause': 'Af_45', 'incn': 'III 10', 'page': 79,
  'text': 'Si infra capillos uulnus fuerit <sp>unius uncię</sp> longum{5}, unum{6} sol. (emen)det.{7}',
  'notes': {5: D("long' <i>H T</i>", "long' H T"), 6: D('XII den. <i>Lb S Ct</i>', 'XII den. Lb S Ct'), 7: D('emendet <i>Cb;</i> det <i>H Di T; fehlt S Ct</i>', 'emendet Cb; det H Di T; lacking in S Ct')}},
 {'clause': 'Af_45-1', 'incn': 'III 10', 'page': 79,
  'text': 'Si extra capillos fuerit{8} <sp>et eiusdem magnitudinis, duo</sp>{9} solidi <sp>sint</sp>{10} emendatio.',
  'notes': {8: D('f. et <i>fehlt Cb</i>', 'f. et lacking in Cb'), 9: D('duos sol. <i>Cb</i>', 'duos sol. Cb'), 10: D('sit <i>T;</i> s. e. <i>fehlt Cb Lb S</i>', 'sit T; s. e. lacking in Cb Lb S')}},
 {'clause': 'Af_46', 'incn': 'III 11', 'page': 79,
  'text': "Si cui auris <sp>absciditur</sp>, XXX sol. emend'.{11}",
  'notes': {11: EM11}},
]
