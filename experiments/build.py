#!/usr/bin/env python3
"""Builds the standalone network experiments in this folder.

Each page is one HTML file with its CSS, JS and data inline; only D3 comes
from a CDN. The pages are made from the templates in templates/ by putting
the data where the template says /*DATA*/. Run from the repository root:

    python3 experiments/build.py

and open experiments/*.html in a browser (no server needed).

The pages are experiments: nothing on the site links to them.
"""
import json
import re
import glob
import os
from collections import Counter, defaultdict
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

SCHOLARS = {
    'liebermann': 'Liebermann', 'liebermann-erkl': 'Liebermann',
    'wormald-mel': 'Wormald', 'wormald-ppmel': 'Wormald',
    'rabin-doml': 'Rabin', 'whitelock': 'Whitelock', 'whitelock-cs': 'Whitelock',
    'jurasinski-and-oliver': 'Jurasinski and Oliver', 'robertson': 'Robertson',
    'attenborough': 'Attenborough', 'kennedy': 'Kennedy', 'oliver': 'Oliver',
    'jurasinski-sanctuary': 'Jurasinski',
}


def load(path):
    with open(os.path.join(REPO, path), encoding='utf-8') as f:
        return json.load(f)


def plain(s):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', s))).strip()


def first_year(date):
    """The first year in a free-text date ('c. 890–c. 940', '25 Dec. 1027–34')."""
    m = re.search(r'\b(\d{3,4})\b', date or '')
    return int(m.group(1)) if m else None


def codes_list():
    codes = load('oe-laws/codes.json')
    out = []
    for i, c in enumerate(codes):
        out.append({
            'code': c['code'], 'name': c.get('name', ''), 'group': c.get('group', ''),
            'king': c.get('king', ''), 'date': plain(c.get('date', '')),
            'year': first_year(c.get('date', '')), 'clauses': c.get('clauses', 0),
            'order': i, 'anchor': c.get('anchor', ''),
        })
    return out


def clause_codes():
    return {row['id']: row['code'] for row in load('oe-laws/index.json')}


# ------------------------------------------------------------ 1. borrowing

def borrowing():
    codes = codes_list()
    of = clause_codes()
    cit = {row['id']: row['citation'] for row in load('oe-laws/index.json')}
    terms = {k: v for k, v in load('data/comparison-terms.json').items() if not k.startswith('_')}
    links = {}   # (from clause, to clause, scholar) -> {kind, labels}
    for f in sorted(glob.glob(os.path.join(REPO, 'oe-laws', '*.xml'))):
        cid = os.path.basename(f)[:-4]
        if cid not in of:
            continue
        xml = open(f, encoding='utf-8').read()
        for m in re.finditer(r'<note type="(comparison|comparedBy)"([^>]*)>(.*?)</note>', xml, re.S):
            typ, attrs, body = m.groups()
            src = re.search(r'source="#([^"\s]+)', attrs)
            scholar = SCHOLARS.get(src.group(1), src.group(1).title()) if src else 'Unattributed'
            label = re.search(r'<label>(.*?)</label>', body, re.S)
            label = plain(label.group(1)) if label else ''
            kind = terms.get(label, 'compare') if typ == 'comparison' else 'compare'
            for t in re.findall(r'target="clause:([^"]+)"', body):
                if t not in of or t == cid:
                    continue
                a, b = (cid, t) if typ == 'comparison' else (t, cid)
                # a source link points from the borrower to its source; turn it round
                # so every directed link runs from the older text to the one that used it
                if kind == 'source':
                    a, b = b, a
                key = (a, b, scholar)
                if key not in links:
                    links[key] = {'kind': kind, 'labels': set()}
                if label:
                    links[key]['labels'].add(label)
                if kind in ('source', 'usedIn') and links[key]['kind'] not in ('source', 'usedIn'):
                    links[key]['kind'] = kind
    # one row per clause pair per scholar
    pairs = []
    for (a, b, scholar), v in links.items():
        kind = 'source' if v['kind'] in ('source', 'usedIn') else v['kind']
        pairs.append([cit.get(a, a), cit.get(b, b), of[a], of[b], scholar, kind, '; '.join(sorted(v['labels']))[:120], a, b])
    used = {p[2] for p in pairs} | {p[3] for p in pairs}
    return {
        'codes': [c for c in codes if c['code'] in used],
        'groups': list(dict.fromkeys(c['group'] for c in codes if c['code'] in used)),
        'pairs': pairs,
    }


# ------------------------------------------------------------ entries

def entries():
    out = []
    for f in sorted(glob.glob(os.path.join(REPO, 'entries', '*.xml'))):
        xml = open(f, encoding='utf-8').read()
        eid = os.path.basename(f)[:-4]
        hw = re.search(r'<orth>(.*?)</orth>', xml, re.S)
        lang = re.search(r'<entry[^>]*xml:lang="([^"]+)"', xml)
        scrap = re.search(r'<dictScrap type="liebermann">(.*?)</dictScrap>', xml, re.S)
        gloss = ''
        # the first italic stretch that is Liebermann's German, not a grammatical label
        for m in re.finditer(r'<hi rend="italic">(.*?)</hi>', scrap.group(1) if scrap else '', re.S):
            if '<ref' in m.group(1):
                continue
            t = plain(m.group(1)).strip(' ,;:|')
            if len(t) > 3:
                gloss = t
                break
        out.append({
            'id': eid, 'hw': plain(hw.group(1)) if hw else eid,
            'lang': lang.group(1) if lang else 'ang',
            'gloss': gloss[:60],
            'spelling': '<usg type="dom">spelling</usg>' in xml,
            'xml': xml,
        })
    return out


# ------------------------------------------------------------ 2. vocabulary

def vocabulary(ents):
    codes = codes_list()
    of = clause_codes()
    words = []
    by_code = defaultdict(set)
    for e in ents:
        cited = Counter()
        for t in re.findall(r'<xr type="lawCode"><ref target="clause:([^"]+)"', e['xml']):
            if t in of:
                cited[of[t]] += 1
        if not cited:
            continue
        i = len(words)
        words.append([e['id'], e['hw'], e['lang'], e['gloss'], {c: n for c, n in cited.items()}])
        for c in cited:
            by_code[c].add(i)
    keep = [c for c in codes if len(by_code[c['code']]) >= 3]
    for c in keep:
        c['words'] = len(by_code[c['code']])
    return {'codes': keep, 'groups': list(dict.fromkeys(c['group'] for c in keep)), 'words': words}


# ------------------------------------------------------------ 3. cross-references

def crossrefs(ents):
    ids = {e['id'] for e in ents}
    nodes = {}
    edges = set()
    for e in ents:
        for kind, t in re.findall(r'<xr type="(see|compare|derivative)"><ref target="entry:([^"]+)"', e['xml']):
            if t not in ids or t == e['id']:
                continue
            edges.add((e['id'], t, kind))
    used = {a for a, _, _ in edges} | {b for _, b, _ in edges}
    idx = {}
    node_list = []
    for e in ents:
        if e['id'] in used:
            idx[e['id']] = len(node_list)
            node_list.append([e['id'], e['hw'], e['lang'], e['gloss'], 1 if e['spelling'] or e['lang'] == 'de' else 0])
    kinds = {'see': 0, 'compare': 1, 'derivative': 2}
    return {'nodes': node_list, 'edges': sorted([idx[a], idx[b], kinds[k]] for a, b, k in edges)}


def write(template, out, data):
    src = open(os.path.join(HERE, 'templates', template), encoding='utf-8').read()
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = src.replace('/*DATA*/null', payload)
    with open(os.path.join(HERE, out), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{out}: {len(html) // 1024} KB')


if __name__ == '__main__':
    write('borrowing.html', 'law-code-borrowing.html', borrowing())
    ents = entries()
    write('vocabulary.html', 'shared-vocabulary.html', vocabulary(ents))
    write('crossrefs.html', 'headword-crossrefs.html', crossrefs(ents))
