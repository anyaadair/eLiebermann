"""Make the DOE review page from match.py's output.

python3 tools/doe/build.py out.json tools/doe/page-template.html doe-matches.html [decisions-folder]

Cross-reference and spelling entries get no links (match.py leaves them
out). Entries that already have a DOE link are left out too, and so are
entries with a saved choice (decisions-folder, as for apply.py), including
"no link", so the page shows only what is still to decide.
"""
import json, sys, glob, os
D = json.load(open(sys.argv[1], encoding='utf-8'))
R = D['results']
decided = set()
if len(sys.argv) > 4:
    decided = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(sys.argv[4], '**', '*.json'), recursive=True)}
rows = []
for r in R:
    if r['xref'] or r['existing']:
        continue  # already linked on the site (by hand, or in an earlier round)
    if r['id'] in decided:
        continue  # the editor has already chosen (a link, or none)
    if r['grade'] == 'none' and r['headword'].lstrip('[(').strip()[:1].isupper():
        continue  # names: the DOE has no entries for them (Anya, Nov 2026)
    rows.append({'e': r['id'], 'hw': r['headword'], 's': r['snippet'], 'g': r['grade'], 't': r['how'],
                 'x': r['existing'], 'b': sorted(set(r['bt']))[:6],
                 'o': [{'id': c['id'], 'hw': c['headword']} for c in r['candidates']][:8]})
d = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
t = open(sys.argv[2], encoding='utf-8').read()
L = D.get('letters') or [D['span'][0][:1].upper()]
t = t.replace('__LETTERS__', ', '.join(L[:-1]) + ' and ' + L[-1] if len(L) > 1 else L[0])
open(sys.argv[3], 'w', encoding='utf-8').write(t.replace('__DATA__', d))
print(len(rows), 'rows,', len(d) // 1000, 'KB')
