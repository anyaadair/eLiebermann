"""Add Dictionary of Old English links to entries: sure and likely matches,
and the editor's choices saved on the review page (which win).

python3 tools/doe/apply.py out.json [decisions-folder]

Run from the repository root. decisions-folder holds the review page's saved
choices, one JSON file per entry ({"ids": [...]}; an empty list = no link),
as written by ArtifactData list with out_dir (…/decisions/<entry>.json).
It only adds links; a link already in an entry is never removed.

The links are written with the DOE's address for individual subscribers;
entry.html takes only the E-number from it and builds the address each
reader has chosen (institutional or individual).
"""
import json, glob, os, re, sys, datetime, html

out_path = sys.argv[1]
dec_dir = sys.argv[2] if len(sys.argv) > 2 else None
R = json.load(open(out_path, encoding='utf-8'))['results']
dec = {}
if dec_dir:
    for f in glob.glob(os.path.join(dec_dir, '**', '*.json'), recursive=True):
        d = json.load(open(f, encoding='utf-8'))
        dec[os.path.basename(f)[:-5]] = d.get('data', d)
today = datetime.date.today().isoformat()
heads = {}
for r in R:
    for c in r['candidates']:
        heads[c['id']] = c['headword']

changed = added = 0
for r in R:
    e = r['id']
    if r['xref']:
        continue  # cross-reference entries point to another headword, which has the links
    if e in dec:
        ids, checked = dec[e].get('ids') or [], True
    elif r['grade'] in ('sure', 'likely'):
        ids, checked = [c['id'] for c in r['candidates']], False
    else:
        continue
    p = f'entries/{e}.xml'
    s = open(p, encoding='utf-8').read()
    have = set(re.findall(r'<xr type="doe"><ref target="[^"]*\?(E\d+)"', s))
    new = [i for i in ids if i not in have]
    if not new:
        continue
    lines = ''.join(
        f'        <xr type="doe"><ref target="https://indiv.dictionary.doe.utoronto.ca/doe/?{i}">'
        f'{html.escape(heads.get(i) or r["headword"], quote=False)}</ref></xr>\n' for i in new)
    xrs = list(re.finditer(r'^        <xr type="(bosworthToller|doe)">.*\n', s, re.M))
    if xrs:
        at = xrs[-1].end()
    else:
        m = re.search(r'^        <xr type="(wiktionary|lawCode)">', s, re.M) or re.search(r'^\s*</entry>', s, re.M)
        if not m:
            print('no place for the link in', e)
            continue
        at = m.start()
    s = s[:at] + lines + s[at:]
    how = 'chosen by the editor on the review page' if checked else f'guessed from the DOE headword list, {r["how"]}; not yet checked'
    note = (f'      <change when="{today}">Link to the Dictionary of Old English added '
            f'({", ".join(new)}; {html.escape(how, quote=False)}).</change>\n')
    m = re.search(r'^    </revisionDesc>', s, re.M)
    if m:
        s = s[:m.start()] + note + s[m.start():]
    open(p, 'w', encoding='utf-8').write(s)
    changed += 1
    added += len(new)
print('entries', changed, 'links', added, 'decisions used', sum(1 for r in R if r['id'] in dec))
