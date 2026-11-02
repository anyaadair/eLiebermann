"""Make the DOE review page from match.py's output.

python3 tools/doe/build.py out.json tools/doe/page-template.html doe-matches.html

Cross-reference entries are left out: they only point to another headword,
which carries the links (as with Bosworth-Toller).
"""
import json, sys
R = json.load(open(sys.argv[1], encoding='utf-8'))['results']
rows = []
for r in R:
    if r['xref']:
        continue
    rows.append({'e': r['id'], 'hw': r['headword'], 's': r['snippet'], 'g': r['grade'], 't': r['how'],
                 'x': r['existing'], 'b': sorted(set(r['bt']))[:6],
                 'o': [{'id': c['id'], 'hw': c['headword']} for c in r['candidates']][:8]})
d = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
t = open(sys.argv[2], encoding='utf-8').read()
open(sys.argv[3], 'w', encoding='utf-8').write(t.replace('__DATA__', d))
print(len(rows), 'rows,', len(d) // 1000, 'KB')
