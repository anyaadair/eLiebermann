"""Write each law code's titles into oe-laws/codes.json:
  liebermannTitle  [title from Liebermann's table of contents, page, running head where different]
  titles           [[title, [who, …]], …]: Liebermann first, then the editions in order of publication,
                   one entry per wording (editors who use the same wording share it), as for the dates.
Run: python3 tools/titles/build.py  (sources: tools/titles/liebermann.py and tools/titles/editions.json)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from liebermann import TOC
ROOT = os.path.join(HERE, '..', '..')
P = os.path.join(ROOT, 'oe-laws', 'codes.json')
ED = json.load(open(os.path.join(HERE, 'editions.json'), encoding='utf-8'))
WHO = {'Attenborough': ('Attenborough, p. ', 1922), 'Robertson': ('Robertson, p. ', 1925), 'Whitelock': ('Whitelock, EHD p. ', 1979),
       'Rabin 2015': ('Rabin, Political Writings p. ', 2015), 'Rabin': ('Rabin, Legal Writings p. ', 2020),
       'Jurasinski and Oliver': ('Jurasinski and Oliver, p. ', 2021)}
codes = json.load(open(P, encoding='utf-8'))
for c in codes:
    t = TOC.get(c['code'])
    titles = []
    if t:
        c['liebermannTitle'] = [t[0], t[1]] + ([t[2]] if t[2] and t[2] != t[0] else [])
        titles.append([t[0], ['Liebermann, I p. ' + t[1]]])
    else:
        c.pop('liebermannTitle', None)
    for e in sorted((e for e in ED if e['code'] == c['code']), key=lambda e: WHO[e['editor']][1]):
        who = WHO[e['editor']][0] + str(e['page'])
        same = next((x for x in titles[1:] if x[0] == e['title']), None)
        if same: same[1].append(who)
        else: titles.append([e['title'], [who]])
    if titles: c['titles'] = titles
    else: c.pop('titles', None)
open(P, 'w', encoding='utf-8').write('[\n' + ',\n'.join(json.dumps(c, ensure_ascii=False, separators=(',', ':')) for c in codes) + '\n]\n')
print(sum(1 for c in codes if c.get('titles')), 'codes with titles')
