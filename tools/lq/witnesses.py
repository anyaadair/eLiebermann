"""Clause-file manuscript lists: Ld, Lond and lq in the wording of data/manuscripts.json (Nov 2026)."""
import glob
R = [
 ('<abbr>Ld</abbr> <note type="manuscript">William Lambarde, Archaionomia (London, 1568) – printed from manuscripts now lost</note>',
  '<abbr>Ld</abbr> <note type="manuscript">William Lambarde, Archaionomia (London, 1568), printed largely from Laurence Nowell’s 16th-century transcripts (Liebermann thought from manuscripts now lost)</note>'),
 ('<note type="manuscript">The lost original of the London collection, Leges Anglorum Londoniis collectae (c. 1210)</note>',
  '<note type="manuscript">The original of the London collection, Leges Anglorum Londoniis collectae (c. 1210), which survives in copies</note>'),
 ('<abbr>lq</abbr> <note type="manuscript">Lost manuscript: the common source of Ld and the Quadripartitus, reconstructed by Liebermann from what the two share</note>',
  '<abbr>lq</abbr> <note type="manuscript">Posited by Liebermann: his siglum for the readings Ld and the Quadripartitus share; in his German translation, “lq” after words in round brackets marks words found in both</note>'),
]
n = 0
for f in glob.glob('oe-laws/*.xml'):
    x = open(f, encoding='utf-8').read(); y = x
    for a, b in R: y = y.replace(a, b)
    if y != x: open(f, 'w', encoding='utf-8').write(y); n += 1
print(n, 'files')
