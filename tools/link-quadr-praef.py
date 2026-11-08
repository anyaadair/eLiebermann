"""Liebermann cites the preface of Quadripartitus II as "Quadr II Præf 12" (and "Quadr Arg 27. II Præf 12").
"Præf" is linked to the abbreviations list, and the number after it was never linked to its clause. This links
each such number by hand (<ref type="clause">) to Quadr-II-Praef_N, and adds it to the entry's citation list.
Run once (Nov. 2026):  python3 tools/link-quadr-praef.py"""
import glob, os, re
PRAEF = r'<ref type="abbreviation" target="gram:Praefatio"><abbr>Pr[æa]e?f</abbr></ref>'
files = set(os.path.basename(f)[:-4] for f in glob.glob('oe-laws/Quadr-II-Praef_*.xml'))
total = 0
for p in sorted(glob.glob('entries/*.xml')):
    s = open(p, encoding='utf-8').read()
    if not re.search(PRAEF, s): continue
    new = []
    def link(m):
        n = m.group(3)
        cid = 'Quadr-II-Praef_' + ('Insc' if m.group(2) else n.replace(',', '-'))
        if m.group(2): cid = 'Quadr-II-Praef_' + n.replace(',', '-')   # "Præf Insc. 14": the clause is 14
        if cid not in files: return m.group(0)
        cit = 'Quadr II Præf ' + n
        if cit not in new: new.append((cit, cid))
        return '%s %s<ref type="clause" target="clause:%s" n="%s">%s</ref>' % (m.group(1), m.group(2) or '', cid, cit, n)
    o = s
    s = re.sub('(' + PRAEF + r') (Insc\. )?(\d+(?:,\d+)?)(?![\d,])', link, s)
    if s == o: continue
    s = s.replace('</ref> <ref type="clause"', '</ref> <ref type="clause"')
    items = ''.join('\n        <xr type="lawCode"><ref target="clause:%s">%s</ref></xr>' % (cid, cit) for cit, cid in dict(new).items() if 'clause:%s"' % cid not in o)
    m = list(re.finditer(r'\n\s*<xr type="lawCode">.*?</xr>', s))
    if m and items: s = s[:m[-1].end()] + items + s[m[-1].end():]
    elif items:
        i = s.find('</dictScrap>', s.find('<dictScrap type="senses">')) if '<dictScrap type="senses">' in s else -1
        print('no citation list in', p)
    s = s.replace('</revisionDesc>', '  <change when="2026-11-08">Citations of the preface of Quadr II (“Præf 12”) linked to their clauses (tools/link-quadr-praef.py).</change>\n    </revisionDesc>', 1)
    open(p, 'w', encoding='utf-8').write(s); total += 1
print(total, 'entries')
