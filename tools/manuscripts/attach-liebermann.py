"""Nov 2026: Liebermann's own words for each manuscript, from his "Verzeichniss der einzelnen Handschriften"
(Gesetze I, pp. xviii–xlii), transcribed diplomatically from the page images (bold, italics, spaced type,
footnotes) and proofread a second time against them, with an English crib made with an LLM.
The transcription is kept whole in tools/manuscripts/liebermann-xviii-xlii.json; here each entry is put into
the file(s) of the manuscript(s) it describes, as "liebermann"."entry". Liebermann's misprints are kept as
printed, with an editor's note. His cross-references ("Alet s. Rj") and his lists of collections ("Cotton",
"Harley im British Museum") become entries of their own."""
import json, glob, os, re
D = 'data/manuscripts'
E = []
for i in range(1, 6): E += json.load(open(f'/home/claude/wormald/mss/lieb-{i}-proofed.json', encoding='utf-8'))
# misprints: keep what Liebermann printed
def restore(e, old, new, note):
    assert old in e['text_de'], (old, e['sigla'])
    e['text_de'] = e['text_de'].replace(old, new, 1)
    e.setdefault('editor_notes', []).append(note)
h = next(e for e in E if e['sigla'] == ['Harley'])
restore(h, 'f. 3b <b>Hl</b>; <b>Wi</b>, u. S. 3. 9. 12', 'f. 3b <b>Hl</b>; <b>Wl</b>, u. S. 3. 9. 12',
        'n. 1866: Liebermann prints Wl, a misprint for Wi (Wihtred): the pages, 3, 9 and 12, are those of Abt, Hl and Wi.')
g = next(e for e in E if e['sigla'] == ['Haug'])
restore(g, 'zu 1135 auf <b>CHn cor</b>', 'zu 1135 auf <b>CHu cor</b>', 'Liebermann prints CHu cor, with the n turned upside down: read CHn cor.')
for e in E:
    e['doubts'] = re.sub(r'[^.]*transcribed CHn cor[^.]*\.( Editor to decide[^.]*\.)?', '', e.get('doubts', '')).strip()
json.dump(E, open('tools/manuscripts/liebermann-xviii-xlii.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

files = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(f'{D}/*.json')}
bysig = {}
for i, d in files.items():
    for s in [d['label'], (d.get('liebermann') or {}).get('siglum', '')] + d.get('also', []):
        if s: bysig.setdefault(s, set()).add(i)
def heading(e): return re.sub(r'<[^>]+>', '', e['heading_de']).strip()
OVERRIDE = {  # heading as printed -> files
 'Alb': ['Alb'], 'Br': ['Br', 'Brco', 'Brti'], 'El': ['MsEl'], '°Gi': ['Gi'], 'Gl': ['Gl'], '°Gl[asgow]': ['Glas'],
 '°L': ['L'], 'anderes L': ['anderesL'], 'Lond': ['MsLond'], 'Lond früherer Editoren s. Gi': ['Gi'],
 'Ma[lmesbir.]': ['Malm'], 'Otho': ['Otho'], 'Q': ['MsQ'], 'Quadr[ipartitus]': ['Q'], 'ry': ['ry'], '°Ry': ['Ry'], '°Rym': ['Rym'],
 'Vt (= Cv) Vt 2': ['Vt', 'Cv', 'Vt2'], 'I': ['I', 'il', 'il-2'], 'G': ['G', 'G2'],
}
NEWLAB = {'Additional': 'Additional', 'Alet s. Rj': 'Alet', 'bh s. hb': 'bh', 'Cambridge (vgl. Corpus)': 'Cambridge', 'Corpus': 'Corpus',
          'Cotton': 'Cotton', 'Harley im British Museum:': 'Harley', 'Hunt[ingdon] s. Ip Hunt': 'Hunt', 'Junius 65 s. Oxford': 'Junius 65', 'Oxford': 'Oxford'}
placed, made = {}, []
for k, e in enumerate(E):
    hd = heading(e)
    if hd in OVERRIDE: targets = OVERRIDE[hd]
    elif 'K2' in e['sigla']: targets = ['K2']
    elif e['sigla'][:1] == ['K']: targets = ['K1']
    elif hd in NEWLAB:
        lab = NEWLAB[hd]; nid = 'Lieb-' + re.sub(r'[^A-Za-z0-9]', '', lab)
        cross = ' s. ' in hd
        files[nid] = {'id': nid, 'order': 0, 'anchor': nid, 'label': lab, 'status': 'cross-reference' if cross else 'collection', 'display': True,
                      'liebermann': {'siglum': lab}, 'wormald': [], 'others': [],
                      'display_fields': {'shelfmark': ('Liebermann’s cross-reference: ' + re.sub(r'<[^>]+>', '', e['heading_en'])) if cross else f'Liebermann’s list of the {lab} MSS he uses and their sigla',
                                         'dates': [], 'laws': '', 'laws_note': None, 'notes': []},
                      'link_automatically': 'no'}
        targets = [nid]; made.append(nid)
    else:
        targets = sorted(set().union(*[bysig.get(s, set()) | bysig.get(s.strip('°'), set()) for s in e['sigla']]))
    assert targets and all(t in files for t in targets), (hd, targets)
    entry = {k2: e[k2] for k2 in ('page', 'pages', 'column', 'heading_de', 'heading_en', 'text_de', 'text_en', 'notes', 'unseen') if k2 in e}
    entry['editor_notes'] = e.get('editor_notes', [])
    entry['transcription'] = {'doubts': e.get('doubts', ''), 'proof_notes': e.get('proof_notes', '')}
    for t in targets:
        L = files[t].setdefault('liebermann', {})
        L.setdefault('entries', [])
        L['entries'].append(entry)
        placed.setdefault(t, []).append(hd)
# a cross-reference that only points elsewhere goes after the main entry (Gi)
for t, d in files.items():
    ents = d.get('liebermann', {}).get('entries', [])
    if len(ents) > 1: ents.sort(key=lambda x: ' s. ' in re.sub(r'<[^>]+>', '', x['heading_de']))
# new entries in alphabetical place
key = lambda d: re.sub(r'[^a-z0-9]', '', d['label'].lower())
order = sorted(files.values(), key=lambda d: (key(d), d['label'][:1].islower(), d['order']))
for i, d in enumerate(order): d['order'] = i + 1
for i, d in files.items():
    json.dump(d, open(f'{D}/{i}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
multi = {t: v for t, v in placed.items() if len(v) > 1}
print(len(E), 'entries;', len(placed), 'files given Liebermann’s text; new files:', made, '; files with two entries:', multi)
print('displayed files without Liebermann’s text:', sorted(i for i, d in files.items() if d.get('display') and i not in placed))
