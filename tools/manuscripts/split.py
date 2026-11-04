"""One-off (Nov 2026): turn the Manuscripts guide (data/manuscripts.json) into one file per entry in
data/manuscripts/, adding what Wormald says about each manuscript (MEL I, ch. 4, pp. 162–263; research
records in tools/manuscripts/wormald-mel-ch4.json, checked against the page images).

Each file keeps every source apart:
  "liebermann": what Liebermann says (siglum, his German description, date, laws, Gesetze I page, and the
                English summary of his description that the guide showed)
  "wormald":    Wormald's research records (all fields, for reference; not all are displayed)
  "others":     other scholars' notes (O'Brien, Robertson …), as the guide had them
  "display":    what the guide shows: shelfmark, dates (by whom), the laws note, the notes (by whom)
tools/manuscripts/build.py makes data/manuscripts.json (what the site reads) from these files.
"""
import json, re, os
SRC = 'data/manuscripts.json'
OUT = 'data/manuscripts'
rows = json.load(open(SRC, encoding='utf-8'))
W = json.load(open('tools/manuscripts/wormald-mel-ch4.json', encoding='utf-8'))
MEL = 'Wormald, MEL'

def rec(pat):
    m = [x for x in W if re.search(pat, x['shelfmark'])]
    assert len(m) == 1, (pat, len(m)); return m[0]

# --- which Wormald records belong to which guide entry (anchor), and as which part
WREC = {
 'E': [('', r'MS 173')], 'Ot': [('', r'^London, British Library, Cotton MS Otho B')], 'F': [('', r'Nero E\.i')],
 'MsA': [('Part A (ff. 1–4)', r'Harley MS 55, ff\. 1'), ('Part B (Cnut)', r'Harley MS 55\(B\)')],
 'K1': [('', r'Claudius A\.iii')], 'York': [('', r'^York Gospels')],
 'G': [('Part A', r'Nero A\.i\(A\)'), ('Part B (ff. 70–177)', r'Nero A\.i, part B')],
 'D': [('', r'MS 201')], 'C': [('', r'MS 265')], 'O': [('', r'MS 190')], 'X': [('', r'Junius 121')],
 'B': [('', r'MS 383')], 'Dm': [('', r'Domitian')], 'M': [('', r'Lat\. 420')], 'R': [('', r'Royal MS 11')],
 'Hk': [('', r'Additional MS 49366')], 'T': [('', r'Titus A\.xxvii')], 'Rs': [('', r'Lat\. MS 155')], 'Ai': [('', r'Lat\. MS 155')],
 'K2': [('', r'Claudius D\.ii')], 'Co': [('', r'MSS 70 \+ 258')], 'Or': [('', r'Oriel')], 'MsLond': [('', r'Leges Anglorum Londoniis')],
 'Br': [('', r'Brompton')], 'H': [('', r'^Textus Roffensis')], 'Rl': [('', r'Rawlinson C 641')], 'Jl': [('', r'Julius C\.ii')],
 'Vr': [('', r'Regin')], 'Bu': [('', r'Burney')], 'Otho': [('', r'Otho A\.x')], 'Ld': [('', r'Archaionomia \(London')],
 'l': [('', r'posited lost source')], 'So': [('', r'Lit\. B\.2')],
}
# --- Wormald's dates, in short (palaeographers' notation), with the pages
WDATE = {
 'E': ('laws 930s, in two hands; the book Winchester, s. xᵐᵉᵈ, at Canterbury after 1001', 'pp. 164, 166'),
 'Ot': ('1001×1012 (Table 4.1: 1001×1015); its Bede s. xᵐᵉᵈ', 'pp. 164, 173'),
 'F': ('s. x/xi', 'pp. 164, 182'),
 'MsA': ('Part A (ff. 1–4) s. xi¹; Part B (Cnut) s. xiiᵐᵉᵈ', 'pp. 164–5, 186, 253'),
 'K1': ('s. x/xi–xi¹; VI Atr s. xi¹', 'pp. 164, 191'),
 'York': ('Gospels s. x/xi; Cnut’s letter and the Wulfstan tracts 1020×1023', 'pp. 164, 195–7'),
 'G': ('Part A s. xiᵐᵉᵈ (about 1066); Part B s. xiⁱⁿ', 'pp. 164–5, 198, 224'),
 'D': ('s. xiᵐᵉᵈ (its first scribe s. xiⁱⁿ)', 'pp. 164, 206'),
 'C': ('s. xiᵐᵉᵈ', 'pp. 164, 211'),
 'O': ('Part I s. xi¹; Part II s. xiᵐᵉᵈ; Excom III s. xiiⁱⁿ', 'pp. 164, 220–2'),
 'X': ('s. xi³ᐟ⁴', 'p. 222'),
 'B': ('s. xi/xii', 'pp. 165, 233'),
 'Dm': ('s. xii²ᐟ⁴', 'p. 237'), 'M': ('s. xiiᵐᵉᵈ', 'p. 237'), 'R': ('s. xii³ᐟ⁴', 'p. 237'), 'Hk': ('s. xii³ᐟ⁴', 'p. 237'),
 'T': ('s. xii/xiii', 'p. 237'), 'Rs': ('s. xiiiⁱⁿ', 'p. 237'), 'Ai': ('s. xiiiⁱⁿ', 'p. 237'),
 'K2': ('s. xiv¹', 'p. 237'), 'Co': ('s. xiv¹', 'p. 238'), 'Or': ('s. xiv¹', 'p. 238'),
 'MsLond': ('reign of John', 'p. 238'), 'Br': ('14th century', 'p. 243 n. 322'),
 'H': ('1123–4, one scribe', 'pp. 165, 245'),
 'Vr': ('s. xi¹', 'pp. 165, 257'), 'Bu': ('s. xi²', 'pp. 165, 257 n. 357'),
 'Ld': ('1568', 'p. 262 n. 384'), 'So': ('16th century, in Laurence Nowell’s hand', 'p. 262 n. 380'),
}
# --- where the laws in it verifiably differ from Liebermann's list (Wormald's word; pages)
WLAWS = {
 'Ot': ('Nowell’s transcript of 1562 shows the book also held Ymb Æwbricas and a complete, variant text of II As; V As and Iudex, which Nowell also copied, came from another, lost manuscript (Nw2), not from Otho.', 'pp. 173–8'),
 'MsA': ('two separate books: Part A (ff. 1–4) holds II–III Eg; Part B holds I–II Cn only.', 'pp. 185–6, 253–5'),
 'G': ('two separate books. Part A: I–II Cn, II–III Eg, Romscot, Iudex, and Alfred’s rubric list and preface, the text breaking off within the preface (p. 226; Table 4.1 has “Af–Ine”). Part B: I As, I Em, II–III Eg (largely lost with a missing bifolium), V Atr (twice), Grið, VIII Atr (Pr.–5:2 only) and Norðgrið.', 'pp. 198–203, 224–8'),
 'D': ('the text Liebermann prints from D beside VI Atr (from VI Atr 16) is Cn 1018, Wulfstan’s text for the agreement of 1018; his Table 4.3 lists no separate text of I–II Cn in D.', 'p. 334 n. 327; pp. 204–5, 208, 346–7'),
 'C': ('Liebermann did not print the excommunication formulae in this manuscript (his Excom texts come from other manuscripts).', 'p. 211 n. 196'),
 'O': ('Excom III is an early-twelfth-century addition; when Mirce, Að and Had were added is uncertain.', 'pp. 222–3 (Table 4.5)'),
 'B': ('II–III Eg and I Cn to 17:1 are sixteenth-century transcripts bound in; II As and Af–Ine are incomplete through lost leaves; the book also has a charm for stolen cattle. Of the two copies of AGu, the one on pp. 83–4 is Liebermann’s B (this site’s B1) and the one on p. 6 his B 2 (Gesetze I, p. 126; Wormald p. 236).', 'pp. 229–36 (Table 4.6)'),
 'Dm': ('its Quadripartitus, now two quires, breaks off in Alfred’s laws.', 'pp. 237, 240 (Table 4.7)'),
 'M': ('the opening (I–II Cn and Af) is lost; the settlement of 1153 between Stephen and Henry was added at the end.', 'pp. 240–1 (Table 4.7)'),
 'R': ('his Table 4.7 lists also Argumentum 32 and III and V As.', 'pp. 240–1 (Table 4.7)'),
 'Hk': ('Leis Wl, ECf and Cons Cn were added later by other scribes, and the Argumentum in the 16th century.', 'pp. 240–1 (Table 4.7)'),
 'T': ('Wl art is not part of the original, and Inst Cn is in another scribe’s hand.', 'pp. 240–1 (Table 4.7)'),
 'Rs': ('Rs and Ai are parts of one manuscript, Rylands Lat. 155 + BL Add. 14252, a copy of the London collection.', 'p. 237'),
 'Ai': ('Ai and Rs are parts of one manuscript, Rylands Lat. 155 + BL Add. 14252, a copy of the London collection.', 'p. 237'),
 'H': ('also a fragment of IV As (continuing V As), Excom VIII and IX and canon-law excerpts; Blas and Forf 1 were added by the scribe after the main copying.', 'pp. 246–7 (Table 4.8), 249'),
 'Vr': ('only the prologue and three clauses of X Atr survive.', 'pp. 256–7'),
 'Bu': ('Ine only (from the end of Ine Prol. to Ine 23); Alfred’s laws would have stood in the lost part of the book.', 'pp. 257–8'),
}
# --- shelfmarks Wormald shows to be out of date or incomplete (Liebermann's kept in the file)
SHELF = {
 'M': 'Manchester, John Rylands Library, MS Lat. 420 (in 1903 at Keswick Hall, Norwich, owned by the Gurney family)',
 'Hk': 'London, British Library, Additional MS 49366 (formerly Holkham Hall, MS 228)',
 'Co': 'Cambridge, Corpus Christi College, MS 70 (with MS 258, part of the same book)',
 'So': 'Canterbury, Cathedral Library, Lit. MS B.2 (Liebermann: B 2 no. 8): a transcript in Laurence Nowell’s hand, later owned by William Somner',
 'Rs': 'Manchester, John Rylands Library, MS Latin 155 (with BL, Additional MS 14252, Liebermann’s Ai: one book)',
 'Ai': 'London, British Library, Additional MS 14252 (with Manchester, John Rylands Library, MS Latin 155, Rs: one book)',
 'G': 'London, British Library, Cotton MS Nero A.i (two books bound together: Part A, laws; Part B, ff. 70–177, a Wulfstan collection)',
 'MsA': 'London, British Library, Harley MS 55 (two books bound together: Part A, ff. 1–4; Part B, Cnut)',
}
# Liebermann's B1/B2: which copy is which (Wormald p. 236; Table 4.6; the AGu clause files)
B12 = {'B1': 'Cambridge, Corpus Christi College, MS 383, pp. 83–4 (the second copy in the book)',
       'B2': 'Cambridge, Corpus Christi College, MS 383, p. 6 (the first copy in the book)'}

# --- manuscripts Wormald discusses that are not in Liebermann's list
NEW = [  # id, label (siglum column), pattern, display?, Wormald date, laws (Wormald)
 ('Add43703', 'Add. 43703', r'^London, British Library, Additional MS 43703', True, ('1562, corrected and glossed later', 'p. 173'),
  'Nowell’s transcript of almost all of Otho B.xi (II As, Af–Ine, Ymb Æwbricas and the rest), with V As, Iudex and the end of II As from a second, lost manuscript (Nw2)'),
 ('Nw2', 'Nw2', r'^Lost manuscript used by Laurence Nowell as', True, None, 'V As, Iudex, the end of II As; probably also Af–Ine'),
 ('LitE2', 'Lit. E.2', r'Lit\. MS E\.2', True, ('16th century, in Laurence Nowell’s hand', 'p. 261 n. 375'), 'I–II Cn'),
 ('Davis59', 'Davis 59', r'Henry Davis', True, ('16th century, in Laurence Nowell’s hand', 'p. 262 n. 381'), 'Af'),
 ('UC170', 'UC 170/529', r'170/529', True, ('16th century, in Laurence Nowell’s hand', 'p. 238 n. 305'), 'Quadripartitus (from Hk)'),
 ('VetA3', 'Vet. A.3 c.196', r'Vet\. A\.3', True, ('notes of 1811; the lost leaf s. xii', 'pp. 165, 260'), 'II–III Eg (readings of a lost leaf)'),
 ('Quadr-work', 'Quadripartitus', r'^Quadripartitus', False, None, ''),
 ('OffaBible', 'Offa Bible', r'Offa Bible', False, None, ''),
 ('TiberiusAii', 'Tiberius A.ii', r'Tiberius A\.ii', False, None, ''),
 ('SidneySussex', 'Sidney Sussex pontifical', r'Sidney Sussex', False, None, ''),
 ('Copenhagen1595', 'Copenhagen 1595', r'Copenhagen', False, None, ''),
 ('Barlow37', 'Barlow 37', r'Barlow 37', False, None, ''),
 ('Rouen1382', 'Rouen 1382', r'MS 1382', False, None, ''),
 ('Bodley718', 'Bodley 718', r'Bodley 718', False, None, ''),
 ('TiberiusBv', 'Tiberius B.v', r'Tiberius B\.v', False, None, ''),
 ('LambardeBodl', 'Lambarde (Bodl.)', r'Jur\. Seld', False, None, ''),
 ('LambardeHuntington', 'Lambarde (Huntington)', r'Huntington Library', False, None, ''),
]

def note_main_pages(r):
    p = r.get('pages', '')
    return re.split(r';', p)[0].strip()

def wnotes(anchor):
    out = []
    for part, pat in WREC.get(anchor, []):
        r = rec(pat)
        lab = ('on ' + part + ': ') if part else ''
        if r.get('overview'): out.append({'by': 'Wormald', 'ref': f'{MEL}, pp. {note_main_pages(r)}' if not note_main_pages(r).startswith('p') else f'{MEL}, {note_main_pages(r)}', 'text': lab + r['overview']})
        if r.get('liebermann_superseded'): out.append({'by': 'Wormald', 'kind': 'correction', 'text': r['liebermann_superseded']})
    # one note per manuscript where the same record serves two entries is fine (Rs, Ai)
    seen, uniq = set(), []
    for n in out:
        if n['text'] not in seen: seen.add(n['text']); uniq.append(n)
    return uniq

SPLIT = re.compile(r'\s(?=(?:O’Brien \((?:2003|God’s)|Wormald \(1999|Sisam showed|On Lambarde’s sources))')
def split_notes(anchor, notes):
    status = (re.match(r'\[[^\]]*\]', notes) or [''])[0]
    body = notes[len(status):].strip()
    parts = SPLIT.split(body)
    lie, others = parts[0].strip(), []
    for p in parts[1:]:
        by = 'O’Brien' if p.startswith('O’Brien') else 'Wormald' if p.startswith('Wormald') else 'Sisam' if p.startswith('Sisam') else 'Editor'
        others.append({'by': by, 'text': p.strip()})
    if anchor == 'Rs':
        others.insert(0, {'by': 'Editor', 'text': lie}); lie = ''
    if anchor == 'B' and 'database’s sigla' in lie:
        others.insert(0, {'by': 'Editor', 'text': 'Corpus 383 has the Treaty of Alfred and Guthrum twice. Liebermann prints both copies side by side, headed “B, p. 83” and “B 2, p. 6” (Gesetze I, p. 126); this site calls the first B1. So B1 is the copy on pp. 83–4, and B2 the copy on p. 6, which comes first in the book.'}); lie = ''
    if anchor in ('Vincent98', 'Harley785'):
        others.insert(0, {'by': 'O’Brien', 'text': lie}); lie = ''
    return status.strip('[]'), lie, others

def fname(anchor, n):
    base = re.sub(r'[^A-Za-z0-9_-]', '_', anchor)
    return base + ('' if n == 0 else f'-{n + 1}')

files = []
count = {}
for i, r in enumerate(rows):
    a = r['Anchor']; n = count.get(a, 0); count[a] = n + 1
    status, lie_note, others = split_notes(a, r.get('Notes', ''))
    wrecs = [dict(rec(p), part=part) for part, p in WREC.get(a, [])] if n == 0 or a not in ('B', 'il') else []
    for w in wrecs: w.pop('_part', None)
    if wrecs: others = [o for o in others if o['by'] != 'Wormald']
    shelf = r['English Translation']
    if a == 'B' and r['Gesetze Text'] in B12: shelf = B12[r['Gesetze Text']]
    shelf = SHELF.get(a, shelf) if n == 0 else shelf
    d = {
        'id': fname(a, n), 'order': i, 'anchor': a, 'label': r['Gesetze Text'], 'status': status, 'display': True,
        'liebermann': {'siglum': r['Gesetze Text'], 'description_de': r.get('German Expansion', ''), 'shelfmark_as_given': r['English Translation'],
                       'date': r.get('Date (Liebermann)', ''), 'laws': r.get('Laws in it', ''), 'page': r.get('Liebermann I, page', ''), 'notes': lie_note},
        'wormald': wrecs,
        'others': others,
        'display_fields': {
            'shelfmark': shelf,
            'dates': ([{'by': 'Liebermann', 'text': r['Date (Liebermann)'], 'ref': 'Gesetze I, p. ' + r.get('Liebermann I, page', '')}] if r.get('Date (Liebermann)') else [])
                     + ([{'by': 'Wormald', 'text': WDATE[a][0], 'ref': f'{MEL}, {WDATE[a][1]}'}] if a in WDATE and n == 0 else []),
            'laws': r.get('Laws in it', ''),
            'laws_note': ({'by': 'Wormald', 'text': WLAWS[a][0], 'ref': f'{MEL}, {WLAWS[a][1]}'} if a in WLAWS and n == 0 else None),
            'notes': ([{'by': 'Liebermann', 'ref': 'Gesetze I, p. ' + r.get('Liebermann I, page', '') if r.get('Liebermann I, page') else '', 'text': lie_note}] if lie_note else [])
                     + (wnotes(a) if n == 0 else []) + others,
        },
    }
    if r.get('Link automatically'): d['link_automatically'] = r['Link automatically']
    files.append(d)

# new entries: placed alphabetically among the others
labels = [(f['label'].lower(), f['order']) for f in files]
for nid, label, pat, disp, wdate, laws in NEW:
    r = rec(pat)
    pos = max([o for l, o in labels if l <= label.lower()] + [-1]) + 0.5
    d = {
        'id': nid, 'order': pos, 'anchor': nid, 'label': label, 'status': 'not in Liebermann', 'display': disp,
        'liebermann': {}, 'wormald': [{k: v for k, v in dict(r, part='').items() if k != '_part'}], 'others': [],
        'display_fields': {
            'shelfmark': r['shelfmark'],
            'dates': [{'by': 'Wormald', 'text': wdate[0], 'ref': f'{MEL}, {wdate[1]}'}] if wdate else [],
            'laws': '', 'laws_note': {'by': 'Wormald', 'text': laws, 'ref': f'{MEL}, {note_main_pages(r) if note_main_pages(r).startswith("p") else "pp. " + note_main_pages(r)}'} if laws else None,
            'notes': [{'by': 'Wormald', 'ref': f'{MEL}, pp. {note_main_pages(r)}' if not note_main_pages(r).startswith('p') else f'{MEL}, {note_main_pages(r)}', 'text': r['overview']}]
                     + ([{'by': 'Wormald', 'kind': 'correction', 'text': r['liebermann_superseded']}] if r.get('liebermann_superseded') else []),
        },
    }
    files.append(d)

files.sort(key=lambda f: f['order'])
for k, f in enumerate(files): f['order'] = k + 1
os.makedirs(OUT, exist_ok=True)
for f in files:
    json.dump(f, open(os.path.join(OUT, f['id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
used = {id(rec(p)) for ps in WREC.values() for _, p in ps} | {id(rec(p)) for _, _, p, *_ in NEW}
print(len(files), 'files;', sum(f['display'] for f in files), 'displayed; Wormald records unused:', [x['shelfmark'][:40] for x in W if id(x) not in used])
