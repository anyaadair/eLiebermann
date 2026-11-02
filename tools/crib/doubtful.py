#!/usr/bin/env python3
"""Rewrite the list of doubtful readings in the LLM crib ("[?]") in docs/TODO.md, between the markers
<!-- crib-doubtful --> and <!-- /crib-doubtful -->: one line per law text, linking each clause."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = 'https://anyaadair.github.io/eLiebermann/law.html?id='
index = json.load(open(os.path.join(ROOT, 'oe-laws', 'index.json'), encoding='utf-8'))
groups, total = {}, 0
for c in index:
    s = open(os.path.join(ROOT, 'oe-laws', c['file']), encoding='utf-8').read()
    if any('[?]' in m for m in re.findall(r'<ab type="translation"[^>]*source="#claude-crib"[^>]*>(.*?)</ab>', s, re.S)):
        groups.setdefault(c['legalText'] or c['code'], []).append(c)
        total += 1
lines = [f'{total} clauses have a crib that marks a doubtful reading with “[?]”, mostly a corrupt or unusual word in the Latin; a look at the scan may settle some.', '']
for name, cs in groups.items():
    lines.append(f'- [ ] **{name}** ({len(cs)}): ' + ', '.join(f'[{c["citation"]}]({SITE}{c["id"]})' for c in cs))
block = '<!-- crib-doubtful -->\n' + '\n'.join(lines) + '\n<!-- /crib-doubtful -->'
path = os.path.join(ROOT, 'docs', 'TODO.md')
todo = open(path, encoding='utf-8').read()
todo = re.sub(r'<!-- crib-doubtful -->.*?<!-- /crib-doubtful -->', lambda m: block, todo, flags=re.S)
open(path, 'w', encoding='utf-8').write(todo)
print(total, 'clauses with doubtful readings')
