"""A "Title" clause for a law code, where Liebermann prints a title of his own above the text (his bracketed
heading, e.g. "ᵃ[Consiliatio ᵇ Cnuti.]"; not the manuscripts' own heading, which is Inscr.). The new clause
holds the title as printed, with his note marks where he prints them, and the notes on the title, moved from
the clause they had been put with. Pilot, Nov 2026: Cons Cn, In Cn, Lib Lond, Ps Cn for."""
import json, re, sys
# code: (first clause file, title as printed with marks {a}, page, language, [(file, note n, vol, page) to move])
SPEC = {
 'Cons Cn':   ('ConsCn_Inscr',  '{a}[<hi rend="italic">Consiliatio</hi>{b} <hi rend="italic">Cnuti.</hi>]', '618', 'la', [('ConsCn_Inscr', 'a', '1', '618'), ('ConsCn_Inscr', 'b', '1', '618')]),
 'In Cn':     ('InCn_Inscr',    '{a}[<hi rend="italic">Instituta</hi>{1} <hi rend="italic">Cnuti aliorumque regum Anglorum.</hi>]', '612', 'la', [('InCn_Inscr', 'a', '1', '612'), ('InCn_Inscr', '1', '1', '612')]),
 'Lib Lond':  ('LibLond_1',     '{a}[<hi rend="italic">Libertas</hi>{b} <hi rend="italic">Londoniensis.</hi>]', '673', 'la', [('LibLond_1', 'a', '1', '673'), ('LibLond_1', 'b', '1', '673')]),
 'Ps Cn for': ('PsCnFor_Inscr', '[<hi rend="italic">Pseudo-Cnut De foresta.</hi>]', '620', 'la', []),
}
idx = json.load(open('oe-laws/index.json', encoding='utf-8'))
for code, (first, title, page, lang, moves) in SPEC.items():
    src = open(f'oe-laws/{first}.xml', encoding='utf-8').read()
    slug = first.rsplit('_', 1)[0] + '_Title'
    anchor = re.search(r'<idno type="lawCodeAnchor">([^<]*)', src).group(1)
    # the notes to move, out of their files
    moved = []
    for f, n, vol, pg in moves:
        x = open(f'oe-laws/{f}.xml', encoding='utf-8').read()
        m = [mm for mm in re.finditer(r'\s*<note type="liebermannNote"[^>]*xml:id="([^"]*)" n="' + re.escape(n) + r'"[^>]*><bibl><biblScope unit="volume">' + vol + r'</biblScope><biblScope unit="page">' + pg + r'</biblScope>.*?</note>(?=\s*<(?:note|ab|/div))', x, re.S)]
        assert len(m) == 1, (f, n, len(m))
        old_id = m[0].group(1)
        assert f'target="#{old_id}"' not in x, ('note is pointed to', f, n)
        note = m[0].group(0).strip().replace(f'xml:id="{old_id}"', f'xml:id="{slug}.lnote.oe.{n}"')
        moved.append(note)
        x = x[:m[0].start()] + x[m[0].end():]
        open(f'oe-laws/{f}.xml', 'w', encoding='utf-8').write(x)
    text = re.sub(r'\{(\w+)\}', lambda m: f'<ptr type="liebermannNote" n="{m.group(1)}" target="#{slug}.lnote.oe.{m.group(1)}"/>', title)
    # header from the first clause, with this clause's names
    head = src.split('<text>')[0]
    head = head.replace(f'xml:id="{first}"', f'xml:id="{slug}"')
    cit_old = re.search(r'<idno type="citation">([^<]*)', head).group(1)
    clause_old = re.search(r'<idno type="clause">([^<]*)', head).group(1)
    cit = f'{code} Title'
    head = (head.replace(f'<title>{cit_old}</title>', f'<title>{cit}</title>').replace(f'<idno type="slug">{first}</idno>', f'<idno type="slug">{slug}</idno>')
                .replace(f'<idno type="citation">{cit_old}</idno>', f'<idno type="citation">{cit}</idno>').replace(f'<idno type="clause">{clause_old}</idno>', '<idno type="clause">Title</idno>'))
    head = re.sub(r'<idno type="citationKey">[^<]*</idno>', f'<idno type="citationKey">{anchor} title</idno>', head)
    head = re.sub(r'<listWit>.*?</listWit>\s*', '', head, flags=re.S)
    head = re.sub(r'<revisionDesc>.*?</revisionDesc>', f'<revisionDesc>\n      <change when="2026-11-04">New clause: Liebermann’s own title for the text (Gesetze I, p. {page}), with the notes he attaches to it, moved here from {first.split("_",1)[1].replace("-", ".")}.</change>\n    </revisionDesc>', head, flags=re.S)
    body = f'''<text>
    <body>
      <div type="clause" n="Title">
        <head><ref type="lawCode" target="law:{anchor}">{code}</ref> Title</head>
        <ab type="liebermannText" xml:lang="{lang}" source="#liebermann" n="{cit}"><pb n="{page}" ed="#liebermann"/>{text}</ab>
        <note type="editorial">Liebermann’s own title for the text, printed in square brackets above it (Gesetze I, p. {page}); it is not in the manuscripts, whose own heading, where there is one, is the Inscr.</note>
''' + ''.join('        ' + n + '\n' for n in moved) + '''      </div>
    </body>
  </text>
</TEI>
'''
    open(f'oe-laws/{slug}.xml', 'w', encoding='utf-8').write(head + body)
    i = next(k for k, c in enumerate(idx) if c['code'] == code)
    if not any(c['id'] == slug for c in idx):
        new = dict(idx[i]); new.update({'id': slug, 'file': slug + '.xml', 'citation': cit, 'clause': 'Title', 'citationKeys': [f'{anchor} title'], 'page': page})
        new.pop('sheetRow', None); new['source'] = 'tools/titles/make-title.py (Nov 2026)'
        idx.insert(i, new)
    print(code, '->', slug, len(moved), 'notes moved')
open('oe-laws/index.json', 'w', encoding='utf-8').write('[\n' + ',\n'.join(json.dumps(c, ensure_ascii=False, separators=(',', ':')) for c in idx) + '\n]\n')
