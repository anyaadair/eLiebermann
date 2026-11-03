"""The manuscripts of the Instituta Cnuti in the clause files (Nov 2026).
1. Wherever "Inst. Cn." is listed among a clause's manuscripts, add the manuscripts Liebermann names for it
   (his footnote to In Cn Inscr., printed on Af 15: H Rl T Cb Di Lb S Pl Ct), to be linked to the Manuscripts list.
2. The In Cn clause files listed "Lat", "H Di" and "IpHunt" with no description: "Lat" was this database's
   placeholder for Liebermann's edited Latin text; "H Di" and "IpHunt" are his two column heads for the
   inscription only. They now list Liebermann's text (In Cn), then the nine manuscripts, by name."""
import glob, json, re
SIGLA = 'H Rl T Cb Di Lb S Pl Ct'.split()
ms = {r['Gesetze Text']: r['English Translation'] for r in json.load(open('data/manuscripts.json', encoding='utf-8'))}
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;')
INST = ('<witness xml:id="wit-inst-cn"><abbr>Inst. Cn.</abbr> <note type="manuscript">Instituta Cnuti (Latin translation of '
        'Anglo-Saxon laws, c. 1100), as printed by Liebermann</note> <note type="sigla">' + ' '.join(SIGLA) + '</note></witness>')
n1 = n2 = 0
for f in sorted(glob.glob('oe-laws/*.xml')):
    x = open(f, encoding='utf-8').read(); y = x
    if '/InCn_' in f:
        m = re.search(r'([ \t]*)<listWit>.*?</listWit>', y, re.S)
        ind = m.group(1); i2 = ind + '  '
        inscr = 'corresp="#wit-hdi"' in y
        wl = []
        if 'corresp="#wit-lat"' in y:
            wl.append('<witness xml:id="wit-lat"><abbr>In Cn</abbr> <note type="manuscript">Instituta Cnuti (Latin translation of '
                      'Anglo-Saxon laws, c. 1100): Liebermann’s edited text, from the manuscripts listed below</note></witness>')
        if inscr:
            wl.append('<witness xml:id="wit-hdi"><abbr>H, Di</abbr> <note type="manuscript">The heading as in H and Di '
                      '(Liebermann’s column “HDi”)</note></witness>')
            wl.append('<witness xml:id="wit-iphunt"><abbr>Ip Hunt</abbr> <note type="manuscript">The heading as in the copy '
                      'inserted into Henry of Huntingdon’s Historia Anglorum (Liebermann’s column “IpHunt”)</note></witness>')
        for s in SIGLA:
            wl.append(f'<witness xml:id="wit-{s.lower()}"><abbr>{s}</abbr> <note type="manuscript">{esc(ms[s])}</note></witness>')
        y = y[:m.start()] + ind + '<listWit>\n' + ''.join(i2 + w + '\n' for w in wl) + ind + '</listWit>' + y[m.end():]
        n2 += 1
    else:
        y = re.sub(r'<witness xml:id="wit-inst-cn"[^>]*>.*?</witness>', INST, y)
        if y != x: n1 += 1
    if y != x: open(f, 'w', encoding='utf-8').write(y)
print('Inst. Cn. with its manuscripts:', n1, 'files; In Cn files:', n2)
