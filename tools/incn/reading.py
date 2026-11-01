#!/usr/bin/env python3
"""Builds data/incn-reading.json: the Instituta Cnuti in the translator's own order, for instituta.html.

Liebermann prints each passage of the Instituta only once: beside the law it translates (I and II Cnut,
II Edgar, Alfred, Mirce, Hadbot, Geþyncðo …), or, where there is none, in full on Gesetze I pp. 612–615,
whose list of the work's chapters points to the rest ("Si quis latro — — librum pęnitentialem; o. S. 343–47").
This walks that list (the InCn clause files, in order) and puts in each pointer's place the Latin
passages it points to, taken from the clause files where they are printed.

    python3 tools/incn/reading.py      (after tools/incn/add_columns.py)
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAWS = os.path.join(ROOT, 'oe-laws')

# Liebermann's list, p. 612–613: each pointer and where it points (code anchor, first and last clause,
# as in the clause files; the right-hand margin of p. 612–613)
POINTERS = {
    'InCn_I-Prol-I-5-2d': ('ICn', 'Prol.', '5.2d'),
    'InCn_I-5-2e': ('Af', '20', '20'),
    'InCn_I-5-3-9': ('ICn', '5.3', '9'),
    'InCn_I-9a-b-c': ('IIEg', '4', '4.3'),
    'InCn_I-12': ('ICn', '12', '12'),
    'InCn_I-12a-b': ('ICn', '11', '11.1'),
    'InCn_I-12c': ('IIEg', '1.1', '1.1'),
    'InCn_I-12d': ('ICn', '10', '10.1'),
    'InCn_I-13-17-3': ('ICn', '13', '17.3'),
    'InCn_I-19': ('ICn', '19', '19'),
    'InCn_I-22-22-6': ('ICn', '22', '22.6'),
    'InCn_II-Prol-II-4a': ('IICn', 'Prol.', '4a'),
    'InCn_II-5-9': ('IICn', '5', '9'),
    'InCn_II-12-15-1a': ('IICn', '12', '15.1a'),
    'InCn_II-15-2-37': ('IICn', '15.2', '37'),
    'InCn_II-39-42': ('IICn', '39', '42'),
    'InCn_II-44-50-1': ('IICn', '44', '50.1'),
    'InCn_II-52': ('IICn', '52', '52'),
    'InCn_II-52a': ('IICn', '52.1', '52.1'),
    'InCn_II-53-59': ('IICn', '53', '59'),
    'InCn_II-59a-b-c': ('Af', '15', '17'),
    'InCn_II-59d-e-f-g-h-i': ('Af', '38', '39.2'),
    'InCn_II-60-66': ('IICn', '60', '66'),
    'InCn_II-69-80-1': ('IICn', '69', '80.1'),
    'InCn_II-82-83-2': ('IICn', '82', '83.2'),
    'InCn_III-5-8': ('Af', '29', '31.1'),
    'InCn_III-9-39': ('Af', '44', '77'),
    'InCn_III-41': ('Af', '23', '23.2'),
    'InCn_III-42-43-4': ('Mirce', '1', '4'),
    'InCn_III-45-1-45-3': ('Had', '1', '9.1'),
    'InCn_III-60-63-1': ('Gethinctho', '1', '8'),
}

def num(c):
    """sortable key of a clause number within its range check: '15.2a' -> ((15,''),(2,'a'))"""
    out = []
    for part in c.replace(',', '.').split('.'):
        m = re.match(r'(\d+)([a-z]*)', part)
        out.append((int(m.group(1)), m.group(2)) if m else (-1, part))
    return out

def in_range(c, a, b):
    if c == a or c == b:
        return True
    if not re.match(r'\d', c):
        return a == c
    if not re.match(r'\d', a):           # "Prol." … : everything up to b
        return num(c) <= num(b) or c.startswith(b + '.')
    return num(a) <= num(c) and (num(c) <= num(b) or c.startswith(b + '.') or c.startswith(b) and re.match(r'[a-z]', c[len(b):] or '0'))

def ab_of(path, inst):
    s = open(path, encoding='utf-8').read()
    if inst:
        m = re.findall(r'<ab type="liebermannText"[^>]*corresp="#wit-in(?:st-cn)?"[^>]*>(.*?)</ab>', s, re.S)
    else:
        m = re.findall(r'<ab type="liebermannText"[^>]*>(.*?)</ab>', s, re.S)
    return m

SIGLA = {'HDi': 'H Di', 'IpHunt': 'Ip Hunt (Interpolator of Henry of Huntingdon)'}

def witnesses(path):
    """the sigla of Liebermann's texts in a clause file, in order"""
    s = open(path, encoding='utf-8').read()
    abbr = dict(re.findall(r'<witness xml:id="([^"]+)"><abbr>([^<]*)</abbr>', s))
    return [abbr.get(w, w) for w in re.findall(r'<ab type="liebermannText"[^>]*corresp="#([^"]+)"', s)]

def clean(x):
    x = re.sub(r'<ptr [^>]*/>', '', x)
    x = re.sub(r'<pb [^>]*/>', '', x)
    return x.strip()

def main():
    rows = [json.loads(l.strip().rstrip(',')) for l in open(os.path.join(LAWS, 'index.json'), encoding='utf-8') if l.strip().startswith('{')]
    by_anchor = {}
    for r in rows:
        by_anchor.setdefault(r['anchor'], []).append(r)
    cols = json.load(open(os.path.join(ROOT, 'data', 'incn-columns.json'), encoding='utf-8'))['columns']
    incn_of = {}
    for k, ids in cols.items():
        for i in ids:
            incn_of.setdefault(i, k)
    out = []
    for r in by_anchor['InCn']:
        if r['clause'].startswith('Rb'):
            continue
        if r['id'] in POINTERS:
            anchor, a, b = POINTERS[r['id']]
            got = 0
            for c in by_anchor.get(anchor, []):
                if not in_range(c['clause'], a, b):
                    continue
                abs_ = ab_of(os.path.join(LAWS, c['file']), True)
                for x in abs_:
                    out.append({'incn': r['clause'].replace('—', '–'), 'id': c['id'], 'source': c['citation'], 'printed': 'beside',
                                'page': (re.search(r'<pb n="(\d+)"', x) or [None, ''])[1], 'text': clean(x)})
                    got += 1
            if not got:
                print('nothing found for', r['id'], anchor, a, b)
        else:
            xs = ab_of(os.path.join(LAWS, r['file']), False)
            if len(xs) > 1:
                # several manuscripts' versions printed side by side (In Cn Inscr.: H Di | Ip Hunt)
                sig = witnesses(os.path.join(LAWS, r['file']))
                text = ''.join(f'<seg type="parallel"><label>{SIGLA.get(w, w)}</label>{clean(x)}</seg>' for w, x in zip(sig, xs))
            else:
                text = clean(xs[0]) if xs else ''
            out.append({'incn': r['clause'], 'id': r['id'], 'source': '', 'printed': 'list',
                        'page': (re.search(r'<pb n="(\d+)"', xs[0]) or [None, ''])[1] if xs else '', 'text': text})
    rub = []
    for r in by_anchor['InCn']:
        if r['clause'].startswith('Rb'):
            for x in ab_of(os.path.join(LAWS, r['file']), False)[:1]:
                rub.append({'incn': r['clause'], 'id': r['id'], 'text': clean(x)})
    try:
        crib = json.load(open(os.path.join(ROOT, 'data', 'incn-crib.json'), encoding='utf-8'))['crib']
    except OSError:
        crib = {}
    for p in out:
        p['en'] = crib.get(p['id'] + '|' + p['incn'], '')
    for r in rub:
        r['en'] = crib.get(r['id'], '')
    missing = [p['id'] for p in out if not p['en']] + [r['id'] for r in rub if not r['en']]
    if missing:
        print('no English crib for', len(missing), 'passages, e.g.', missing[:5])
    json.dump({'_about': 'The Instituta Cnuti in the translator’s order, assembled by tools/incn/reading.py from the clause files '
               '(“beside”: printed by Liebermann beside the law it translates; “list”: printed in his list, Gesetze I pp. 612–615).',
               'passages': out, 'rubrics': rub},
              open(os.path.join(ROOT, 'data', 'incn-reading.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(out), 'passages,', len(rub), 'rubrics')

if __name__ == '__main__':
    main()
