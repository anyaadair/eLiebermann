"""Add each Latin text to "Laws in it" of every manuscript now listed as one of its sources (data/manuscripts.json)."""
import json, re, sys
sys.path.insert(0, 'tools/latin-mss')
src = open('tools/latin-mss/apply.py', encoding='utf-8').read()
SPEC = eval(re.search(r'SPEC = (\{.*?\n\})', src, re.S).group(1), {'QUADR': 'Lond; K; Co; Or; Dm; T; R; M; Hk; Br'})
CODE = {'Hn': 'Hn', 'QuadrDed': 'Quadr', 'QuadrArg': 'Quadr', 'Quadr-I': 'Quadr', 'Quadr-Rb': 'Quadr', 'Quadr-II-Praef': 'Quadr', 'QuadrII': 'Quadr',
        'ConsCn': 'Cons Cn', 'LibLond': 'Lib Lond', 'CHnCor': 'CHn cor', 'WlEp': 'Wl ep', 'Prom-Reg': 'Sacr cor', 'Duel': 'Duel', 'ExcomII': 'Excom',
        'HnLond': 'Hn Lond', 'InCn': 'In Cn'}
want = {}
for pre, (abbr, title, sig, _) in SPEC.items():
    code = CODE.get(pre) or ('Iud Dei' if pre.startswith('IudDei') else None)
    for t in sig.split('; '):
        s, _, anc = t.partition('=')
        if s == 'Q': continue
        want.setdefault((s, anc), set()).add(code)
p = 'data/manuscripts.json'; lines = open(p, encoding='utf-8').read().split('\n'); out = []; added = []
key = lambda s: re.sub(r'[\s.]', '', s)
for ln in lines:
    st = ln.strip()
    if st.startswith('{'):
        c = st.endswith(','); r = json.loads(st.rstrip(','))
        for (s, anc), codes in want.items():
            if (anc and r['Anchor'] == anc) or (not anc and key(r['Gesetze Text']) == key(s) and r['Anchor'] not in ('ElLond',) and not (s == 'Gl' and r['Anchor'] == 'Glas')):
                have = [x.strip() for x in (r.get('Laws in it') or '').split(',') if x.strip()]
                new = [x for x in sorted(codes) if x not in have]
                if new and not r.get('Notes', '').startswith('[posited]'):
                    r['Laws in it'] = ', '.join(have + new); added.append(r['Gesetze Text'] + ': ' + ', '.join(new))
        ln = json.dumps(r, ensure_ascii=False, separators=(',', ':')) + (',' if c else '')
    out.append(ln)
s = '\n'.join(out); json.loads(s); open(p, 'w', encoding='utf-8').write(s)
print(len(added)); print('\n'.join(added))
