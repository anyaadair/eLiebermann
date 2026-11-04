"""Nov 2026: in the guide's commentary, "MS"/"MSS" for a manuscript, not "book"/"books" (Anya's preference).
Names and kinds of book are kept: law-book (a text), Gospel-book/gospel book, service book, holy book, the Red Book
of the Exchequer, Printed Books, Commonplace-book, book list, Henry of Huntingdon's book XII. Applied to what the
guide shows and to the commentary fields of Wormald's records (never to quotations, doubts or checking notes)."""
import json, glob, re
KEEP_BEFORE = r'(?<!law-)(?<!Gospel-)(?<!gospel )(?<!service )(?<!holy )(?<!Red )(?<!Printed )(?<!Commonplace-)(?<!Hunt\. )'
def ms(t):
    if not isinstance(t, str): return t
    t = re.sub(r'\bliturgical books\b', 'liturgical MSS', t)
    t = re.sub(r'\b([Aa]) (larger |small |single |Jumièges |Worcester |luxury )?book\b(?! list)', lambda m: ('An' if m.group(1) == 'A' else 'an') + ' ' + (m.group(2) or '') + 'MS' if not m.group(2) or m.group(2)[0] not in 'lsJWl' else m.group(1) + ' ' + m.group(2) + 'MS', t)
    t = re.sub(KEEP_BEFORE + r'\bbooks\b', 'MSS', t)
    t = re.sub(KEEP_BEFORE + r'\bbook\b(?! list| XII| of the Exchequer)', 'MS', t)
    return t
FIELDS = ('overview', 'liebermann_superseded', 'wormald_origin', 'other_contents', 'laws')
n = 0
for f in glob.glob('data/manuscripts/*.json'):
    d = json.load(open(f, encoding='utf-8')); before = json.dumps(d, ensure_ascii=False)
    D = d['display_fields']
    D['shelfmark'] = ms(D.get('shelfmark', ''))
    for x in D.get('dates', []): x['text'] = ms(x['text'])
    if D.get('laws_note'): D['laws_note']['text'] = ms(D['laws_note']['text'])
    for x in D.get('notes', []): x['text'] = ms(x['text'])
    if d.get('liebermann', {}).get('notes'): d['liebermann']['notes'] = ms(d['liebermann']['notes'])
    for o in d.get('others', []): o['text'] = ms(o['text'])
    for w in d.get('wormald', []):
        for k in FIELDS:
            if k in w: w[k] = ms(w[k])
    if json.dumps(d, ensure_ascii=False) != before:
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); n += 1
print(n, 'files changed')
