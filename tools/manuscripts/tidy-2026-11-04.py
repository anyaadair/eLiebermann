"""4 Nov 2026 tidy of the Manuscripts guide files (data/manuscripts/):
1. Folios in our English text in the modern form, recto/verso: Liebermann's "f. 89b" -> "f. 89v" ("a" -> "r").
   His German (liebermann.description_de) is left as he printed it. Manuscripts numbered by page (most
   Corpus Christi College, Cambridge MSS) keep "p."/"pp.".
2. The list in alphabetical order of siglum (ignoring case, spaces and full stops); entries with the same
   siglum keep their order (B, B1, B2; L, then L for "Latin version").
3. "Q": a new entry for the Quadripartitus, pointing to the List of Law Codes; Liebermann's other Q (Cotton
   Vespasian D.xv, for Excom XII) is no longer what a bare "Q" links to.
4. "book" -> "MS" in the AGu clause files' manuscript descriptions (see ms-wording.py)."""
import json, glob, os, re, unicodedata
DIR = 'data/manuscripts'
def folios(t):
    if not isinstance(t, str): return t
    return re.sub(r'\b(ff?\.\s?)([\dabr–v-]+(?:\s?–\s?[\dab]+)?)', lambda m: m.group(1) + re.sub(r'(\d)b\b', r'\1v', re.sub(r'(\d)a\b', r'\1r', m.group(2))), t)
files = {f: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(DIR, '*.json'))}
for f, d in files.items():
    D = d['display_fields']
    D['shelfmark'] = folios(D.get('shelfmark', ''))
    for x in D.get('dates', []): x['text'] = folios(x['text'])
    if D.get('laws_note'): D['laws_note']['text'] = folios(D['laws_note']['text'])
    for x in D.get('notes', []): x['text'] = folios(x['text'])
    if d.get('liebermann', {}).get('notes'): d['liebermann']['notes'] = folios(d['liebermann']['notes'])
    for o in d.get('others', []): o['text'] = folios(o['text'])
# 3. Q
q = os.path.join(DIR, 'Q.json')
files[q] = {
    'id': 'Q', 'order': 0, 'anchor': 'Q', 'label': 'Q', 'status': '', 'display': True, 'link_to': 'lawAbb.html#Quadr',
    'link_automatically': 'no',
    'liebermann': {'siglum': 'Q'}, 'wormald': [], 'others': [],
    'display_fields': {
        'shelfmark': 'Quadripartitus: not a manuscript, but the Latin translation of the laws (c. 1110), which survives in several MSS',
        'dates': [], 'laws': '', 'laws_note': None,
        'notes': [{'by': 'Editor', 'text': 'Liebermann’s Q is the Quadripartitus, the early twelfth-century Latin translation of the Old English laws. It is listed with the law codes, where its own MSS are given. In Excom XII alone, Liebermann’s Q is a manuscript, Cotton Vespasian D.xv (the next entry).'}],
    },
}
mq = os.path.join(DIR, 'MsQ.json')
files[mq]['link_automatically'] = 'no'
files[mq]['display_fields']['notes'].append({'by': 'Editor', 'text': 'Only in Excom XII does Liebermann’s Q mean this manuscript; everywhere else Q is the Quadripartitus (the previous entry).'})
# 2. order
def key(d):
    s = unicodedata.normalize('NFKD', d['label']).lower()
    return re.sub(r'[^a-z0-9]', '', s)
ds = sorted(files.items(), key=lambda kv: (key(kv[1]), kv[1]['label'][:1].islower(), 0 if kv[0] == q else 1, kv[1]['order']))
for i, (f, d) in enumerate(ds): d['order'] = i + 1
for f, d in files.items():
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 4. the AGu witnesses; Excom XII's Q is Vespasian D.xv (not the Quadripartitus); Leis Wl's L is the Latin translation
for f in glob.glob('oe-laws/*.xml'):
    x = open(f, encoding='utf-8').read(); y = x.replace('the second copy in the book)', 'the second copy in the MS)').replace('the first copy in the book)', 'the first copy in the MS)')
    if '/ExcomXII_' in f:
        y = re.sub(r'<witness xml:id="wit-q"><abbr>Q</abbr> (<note type="manuscript">[^<]*</note>) <note type="sigla">[^<]*</note></witness>', r'<witness xml:id="wit-q" n="MsQ"><abbr>Q</abbr> \1</witness>', y)
    if '/LeisWl_' in f:
        y = y.replace('<witness xml:id="wit-l">', '<witness xml:id="wit-l" n="anderesL">')
    if y != x: open(f, 'w', encoding='utf-8').write(y)
print('ok')
