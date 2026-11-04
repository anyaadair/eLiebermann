"""Build data/manuscripts.json (what the site reads: the Manuscripts guide, sigla links, pop-ups) from the
files in data/manuscripts/, one per entry. Edit those files, then run:  python3 tools/manuscripts/build.py

Each entry in data/manuscripts.json keeps the old flat fields (Anchor, Gesetze Text, German Expansion,
English Translation, Date (Liebermann), Laws in it, Notes, Liebermann I, page), so that everything that
already reads the file still works, and adds what the guide now shows, by source:
  "Dates":     [{by, text, ref}]  (Liebermann's and Wormald's)
  "Laws note": {by, text, ref}    (where Wormald shows the contents differ from Liebermann's list)
  "Notes by":  [{by, kind?, text, ref}]
Only entries with "display": true are included.
"""
import json, os, re, glob
DIR = 'data/manuscripts'
SUP = {'med': 'ᵐᵉᵈ', 'in': 'ⁱⁿ', 'ex': 'ᵉˣ'}
DIG = str.maketrans('0123456789/', '⁰¹²³⁴⁵⁶⁷⁸⁹ᐟ')
def sup(t):
    """Palaeographers' date notation as printed: s. xi^med -> s. xiᵐᵉᵈ, s. xii^3/4 -> s. xii³ᐟ⁴."""
    if not t: return t
    t = re.sub(r'\^(med|in|ex)\b', lambda m: SUP[m.group(1)], t)
    return re.sub(r'\^(\d(?:/\d)?)', lambda m: m.group(1).translate(DIG), t)
def clean(n):
    return {k: sup(v) if isinstance(v, str) else v for k, v in n.items()}

files = sorted((json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(DIR, '*.json'))), key=lambda d: d['order'])
out = []
for d in files:
    if not d.get('display', True): continue
    L, D = d.get('liebermann') or {}, d['display_fields']
    status = d.get('status', '')
    notes = [clean(n) for n in D.get('notes', []) if n.get('text')]
    row = {
        'Anchor': d['anchor'],
        'Gesetze Text': d['label'],
        'German Expansion': L.get('description_de', ''),
        'English Translation': D.get('shelfmark', ''),
        'Date (Liebermann)': L.get('date', ''),
        'Laws in it': D.get('laws', ''),
        # the flat Notes: the status tag the guide's filters read, then every note with its author (for searching)
        'Notes': (f'[{status}] ' if status else '') + ' '.join(f'{n["by"]}: {n["text"]}' for n in notes),
        'Liebermann I, page': L.get('page', ''),
        'Dates': [clean(x) for x in D.get('dates', [])],
        'Laws note': clean(D['laws_note']) if D.get('laws_note') else None,
        'Notes by': notes,
    }
    if d.get('link_automatically'): row['Link automatically'] = d['link_automatically']
    if d.get('link_to'): row['Link to'] = d['link_to']   # a siglum that is really listed elsewhere (Q: the List of Law Codes)
    # one manuscript, several sigla (Liebermann's K1, K and Kb): the heading shown, and the old anchors kept
    if d.get('display_label'): row['Label'] = d['display_label']
    if d.get('also_anchors'): row['Also anchors'] = d['also_anchors']
    if d.get('also'): row['Also'] = d['also']
    out.append({k: v for k, v in row.items() if v not in (None, [], '') or k in ('Anchor', 'Gesetze Text', 'English Translation', 'Notes')})
    # each other siglum as a row of its own marked "Alias of", so that sigla link and pop up everywhere;
    # the guide does not show these rows
    for a in d.get('also', []):
        out.append({'Anchor': d['anchor'], 'Gesetze Text': a, 'English Translation': D.get('shelfmark', ''), 'Notes': '', 'Alias of': d['label'],
                     **({'Link automatically': d['link_automatically']} if d.get('link_automatically') else {})})
with open('data/manuscripts.json', 'w', encoding='utf-8') as f:
    f.write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in out) + '\n]\n')
print(len(out), 'entries written to data/manuscripts.json from', len(files), 'files')
