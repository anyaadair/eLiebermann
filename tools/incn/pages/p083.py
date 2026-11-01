# Gesetze I p. 83: In Cn III 18–27 beside Alfred 54–63
D = lambda de, en: (de, en)
EM7 = D('<i>fehlt Cb Lb S</i>', 'lacking in Cb Lb S')
CB11 = D('<i>fehlt Cb</i>', 'lacking in Cb')
U15 = D('unguis <i>S</i>', 'unguis S')
CB16 = D('<i>nur Cb</i>', 'only Cb')
U20 = D('unguis <i>Di S</i>', 'unguis Di S')
X27 = D('XXX <i>Cb</i>', 'XXX Cb')
CS29 = D('<i>fehlt Cb S</i>', 'lacking in Cb S')
COLUMNS = [
 {'clause': 'Af_54', 'incn': 'III 18', 'page': 83,
  'text': 'Si quis lacertum{1} alicui fregerit, quindecim sol. emendet.{2}',
  'notes': {1: D('a. l. <i>Cb T</i>', 'a. l. Cb T'), 2: D('<i>aus H Di; fehlt übrigen</i>', 'from H Di; lacking in the others')}},
 {'clause': 'Af_55', 'incn': 'III 19', 'page': 83,
  'text': 'Si quis fregerit{3} alicui <sp>utraque</sp>{4} <sp>brachia</sp>, triginta sol. emend.{5}',
  'notes': {3: D('a. f. <i>Cb</i>', 'a. f. Cb'), 4: D('<i>fehlt Di</i>', 'lacking in Di'), 5: D('<i>aus H Di; fehlt Cb Lb S</i>', 'from H Di; lacking in Cb Lb S')}},
 {'clause': 'Af_56', 'incn': 'III 20', 'page': 83,
  'text': 'Et{6} <sp>qui</sp> pollicem <sp>absciderit</sp>, triginta sol. emend.{7}',
  'notes': {6: D('<i>fehlt Cb;</i> si <i>fügt zu Ct;</i> Si quis p. <i>S</i>', 'lacking in Cb; Ct adds si; Si quis p. S'), 7: EM7}},
 {'clause': 'Af_56-1', 'incn': 'III 20', 'page': 83,
  'text': 'Si{8} <sp>quis</sp> ungulam{9} pollicis{10} <sp>absciderit</sp>{11}, quinque sol. emend.{7}',
  'notes': {7: EM7, 8: D('Et <i>statt</i> si q. <i>Cb</i>', 'Et instead of si q. Cb'), 9: D('unguem <i>S</i>', 'unguem S'), 10: D('eius <i>Cb</i>', 'eius Cb'), 11: CB11}},
 {'clause': 'Af_57', 'incn': 'III 21', 'page': 83,
  'text': 'Secundus digitus <sp>nominatur</sp>{12} index <sp>siue</sp> demonstratorius; <sp>pretium eius est</sp>{13} quindecim sol.{14}; ungule{15} eius <b>V</b> sol.',
  'notes': {12: D('<i>fehlt S</i>', 'lacking in S'), 13: D('<i>fehlt H Lb T S</i>', 'lacking in H Lb T S'), 14: D('solidi <i>H;</i> et <i>fügt zu Cb</i>', 'solidi H; Cb adds et'), 15: U15},
  'editorial': ['Liebermann prints “V” in bold: Alfred has 3 shillings for this nail.']},
 {'clause': 'Af_58', 'incn': 'III 22', 'page': 83,
  'text': 'Tertius digitus <sp>qui nominatur impudicus: eius pretium est</sp>{16} duodecim sol. et ungulę{15} eius{11} duo sol.{17}',
  'notes': {11: CB11, 15: U15, 16: CB16, 17: D('solidi <i>H</i>', 'solidi H')}},
 {'clause': 'Af_59', 'incn': 'III 23', 'page': 83,
  'text': '<sp>Quartus anularis; pretium</sp>{18} <sp>eius</sp> XVII{19} sol. et{16} ungulę{20} eius quatuor sol.',
  'notes': {16: CB16, 18: D('e. p. <i>T</i>', 'e. p. T'), 19: D('XVIII <i>Cb</i>', 'XVIII Cb'), 20: U20}},
 {'clause': 'Af_60', 'incn': 'III 24', 'page': 83,
  'text': 'Quintus auricularis{21}; eius{22} pretium nouem sol. et{16} ungule{20} eius{11} unius{23} sol. <b>(XII den.)</b>.',
  'notes': {11: CB11, 16: CB16, 20: U20, 21: D('digitus aur. nominatur; eius pr. XI sol. <i>T</i>', 'digitus aur. nominatur; eius pr. XI sol. T'), 22: D('p. e. <i>Cb</i>', 'p. e. Cb'),
            23: D('<i>nur</i> u. s. <i>H Di; nur</i> XII d. <i>Cb Lb S</i>', 'only u. s. H Di; only XII d. Cb Lb S')}},
 {'clause': 'Af_61', 'incn': 'III 25', 'page': 83,
  'text': 'Si quis uulneratur in ilio (id{24} est grin), triginta solidis emendetur.{25}',
  'notes': {24: D('i. g. <i>nur H übergeschr.</i>', 'i. g. only H, above the line'), 25: D('-det <i>Di; fehlt Cb</i>', '-det Di; lacking in Cb')}},
 {'clause': 'Af_61-1', 'incn': 'III 25', 'page': 83,
  'text': 'Quodsi ultra fuerit{26} perforatum, <sp>ad utrumque foramen</sp> XX{27} sol., <sp>id est pro uno foramine</sp> XX{27} <sp>sol. et pro alio similiter</sp>.{28}',
  'notes': {26: D('p. f. <i>Cb</i>', 'p. f. Cb'), 27: X27, 28: D('sim. pro a. <i>Lb S</i>', 'sim. pro a. Lb S')}},
 {'clause': 'Af_62', 'incn': 'III 26', 'page': 83,
  'text': 'Si femur hominis perforatum fuerit, triginta sol. emend.{29};',
  'notes': {29: CS29}},
 {'clause': 'Af_62-1', 'incn': 'III 26', 'page': 83,
  'text': 'et si fractum fuerit, similiter.', 'notes': {}},
 {'clause': 'Af_63', 'incn': 'III 27', 'page': 83,
  'text': 'Si tibia perforata fuerit sub genu, duodecim sol. emend.{29}',
  'notes': {29: CS29}},
]
