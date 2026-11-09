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
    text = re.sub(r'\bpp?\.\s*[\d–-]+', '', date or '')      # page numbers in the references
    m = re.search(r'\b(\d{3,4})\b', text)
    if m:
        return int(m.group(1))
    m = re.search(r'\b(\d{1,2})(?:st|nd|rd|th) century', text)
    return (int(m.group(1)) - 1) * 100 + 50 if m else None


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


ROMAN = {'viii': 8, 'ix': 9, 'x': 10, 'xi': 11, 'xii': 12, 'xiii': 13, 'xiv': 14, 'xv': 15, 'xvi': 16, 'xvii': 17, 'xviii': 18}


def ms_year(text):
    """A rough year for a manuscript date: 'c. 1210', 's. xi¹', 's. xiiᵐᵉᵈ', '14th century'."""
    if not text:
        return None
    m = re.search(r'\b(\d{4})\b', text)
    if m:
        return int(m.group(1))
    m = re.search(r'\bs\.\s*(x{0,1}v?i{0,3}x?v?i{0,3})\s*([¹²]|ⁱⁿ|ᵐᵉᵈ|ᵉˣ|/)?', text)
    if m and m.group(1) in ROMAN:
        start = (ROMAN[m.group(1)] - 1) * 100
        return start + {'¹': 25, '²': 75, 'ⁱⁿ': 10, 'ᵐᵉᵈ': 50, 'ᵉˣ': 90, '/': 95}.get(m.group(2), 50)
    m = re.search(r'\b(\d{1,2})(?:st|nd|rd|th)[ -]century', text)
    if m:
        return (int(m.group(1)) - 1) * 100 + 50
    m = re.search(r'\b(\d{1,2})/(\d{1,2})th century', text)
    if m:
        return int(m.group(1)) * 100
    return None


def clause_files():
    """Each clause file's id, code and text, once."""
    of = clause_codes()
    for f in sorted(glob.glob(os.path.join(REPO, 'oe-laws', '*.xml'))):
        cid = os.path.basename(f)[:-4]
        if cid in of:
            yield cid, of[cid], open(f, encoding='utf-8').read()


# ------------------------------------------------------------ 4. manuscripts

def ms_name(text):
    t = plain(text)
    return re.split(r'\s+\(|:\s', t)[0].strip().rstrip(',')


def ms_kind(text):
    t = plain(text)
    if re.search(r'edited (?:Latin )?text|as edited by|as printed by|^(Quadripartitus|Instituta Cnuti|Consiliatio Cnuti|Latin translation)', t):
        return 'version'
    if re.search(r'\blost\b|known only', t):
        return 'lost'
    if re.search(r'\bprint|\breprint|Archaionomia|Foedera|Holinshed|\bedition\b|glossary to', t):
        return 'print'
    return 'ms'


def manuscripts():
    codes = codes_list()
    mss_list = load('data/manuscripts.json')
    by_siglum = defaultdict(list)
    for m in mss_list:
        by_siglum[m['Gesetze Text'].strip()].append(m)
    nodes = {}
    links = Counter()
    for cid, code, xml in clause_files():
        for w in re.finditer(r'<witness xml:id="[^"]+"[^>]*>(.*?)</witness>', xml, re.S):
            n = re.search(r'<note type="manuscript">(.*?)</note>', w.group(1), re.S)
            if not n:
                continue
            name = ms_name(n.group(1))
            siglum = plain(re.sub(r'<note.*', '', w.group(1), flags=re.S))
            if name not in nodes:
                nodes[name] = {'name': name, 'full': plain(n.group(1))[:300], 'kind': ms_kind(n.group(1)), 'sigla': set(), 'year': None, 'date': ''}
            nodes[name]['sigla'].add(siglum)
            links[(name, code)] += 1
    # dates from the Manuscripts list, matched by siglum and by the law codes it holds
    for v in nodes.values():
        for s in v['sigla']:
            base = re.sub(r'\s*\(.*$', '', s).strip()
            for m in by_siglum.get(base, []):
                ds = m.get('Dates') or ([{'by': 'Liebermann', 'text': m.get('Date (Liebermann)', '')}] if m.get('Date (Liebermann)') else [])
                for d in ds:
                    y = ms_year(d.get('text', ''))
                    if y and not v['year']:
                        v['year'], v['date'] = y, f"{d.get('by', '')}: {d.get('text', '')}"[:160]
                if v['year']:
                    break
            if v['year']:
                break
        v['sigla'] = sorted(v['sigla'])
    used = {c for _, c in links}
    return {
        'codes': [c for c in codes if c['code'] in used],
        'groups': list(dict.fromkeys(c['group'] for c in codes if c['code'] in used)),
        'mss': sorted(nodes.values(), key=lambda v: (v['year'] or 9999, v['name'])),
        'links': [[a, b, n] for (a, b), n in links.items()],
    }


# ------------------------------------------------------------ 5. subjects

def subjects():
    groups = load('data/subject-groups.json')
    field_of = {}
    for sec in groups.get('sections', []):
        for g in sec.get('groups', []):
            for t in g.get('terms', []) + ([g['broad']] if g.get('broad') else []):
                field_of.setdefault(t, [sec.get('title', sec.get('field')), g.get('name', '')])
        for t in sec.get('general', []):
            field_of.setdefault(t, [sec.get('title', sec.get('field')), 'General'])
    terms, index, clauses = [], {}, []
    fields = {'offence-legal-event': 'Legal matters', 'people': 'People', 'locations': 'Places'}
    for cid, code, xml in clause_files():
        mine = []
        for n, body in re.findall(r'<keywords n="([^"]+)">(.*?)</keywords>', xml, re.S):
            for t in re.findall(r'<term>([^<]*)</term>', body):
                t = plain(t)
                if not t:
                    continue
                if t not in index:
                    index[t] = len(terms)
                    sec, grp = field_of.get(t, [fields.get(n, n), 'Other'])
                    terms.append([t, fields.get(n, n), grp])
                mine.append(index[t])
        if mine:
            clauses.append([cid, code, sorted(set(mine))])
    return {'terms': terms, 'clauses': clauses, 'general': [t for sec in groups.get('sections', []) for t in sec.get('general', [])]}


# ------------------------------------------------------------ 6. reuse chains

def snippet(xml, kinds, lang=None):
    for m in re.finditer(r'<ab type="(%s)"([^>]*)>(.*?)</ab>' % kinds, xml, re.S):
        if lang and f'xml:lang="{lang}"' not in m.group(2):
            continue
        body = re.sub(r'<note.*?</note>|<pb[^>]*/>|<ptr[^>]*/>', '', m.group(3), flags=re.S)
        t = plain(body)
        if t:
            return t[:140] + ('…' if len(t) > 140 else '')
    return ''


def chains():
    b = borrowing()
    need = {p[7] for p in b['pairs']} | {p[8] for p in b['pairs']}
    cit = {row['id']: row['citation'] for row in load('oe-laws/index.json')}
    clauses = {}
    for cid, code, xml in clause_files():
        if cid in need:
            clauses[cid] = [cit.get(cid, cid), code,
                            snippet(xml, 'liebermannText|editionText'),
                            snippet(xml, 'translation', 'en')]
    return {'codes': b['codes'], 'groups': b['groups'], 'clauses': clauses,
            'pairs': [[p[7], p[8], p[4], p[5], p[6]] for p in b['pairs']]}


# ------------------------------------------------------------ 7. dates

def date_range(text):
    """Years in a free-text date, as (low, high, likely, open_start, open_end)."""
    t = text.replace('×', '–')
    years = []
    likely = []
    for m in re.finditer(r'(\d{3,4})(s?)(?:\s*[–-]\s*(?:c\.\s*)?(\d{1,4}))?', t):
        y = int(m.group(1))
        lo, hi = y, y
        if m.group(2):          # 990s
            hi = y + 9
        if m.group(3):
            tail = m.group(3)
            hi = int(str(y)[:len(str(y)) - len(tail)] + tail) if len(tail) < len(str(y)) else int(tail)
            if hi < lo:
                hi = lo
        years += [lo, hi]
        before = t[:m.start()]
        if re.search(r'(probably|perhaps|\?)\s*(c\.\s*)?$', before) or t[m.end():m.end() + 1] == '?':
            likely += [lo, hi]
    if re.search(r'^early (\d{3})00s', t):
        y = int(re.search(r'(\d{3})00s', t).group(1)) * 100
        years = [y, y + 30]
    if not years:
        return None
    lo, hi = min(years), max(years)
    if lo < 500 or hi > 1300:
        return None
    return {
        'lo': lo, 'hi': hi,
        'likely': [min(likely), max(likely)] if likely and (min(likely), max(likely)) != (lo, hi) else None,
        'openStart': bool(re.match(r'\s*(well\s+)?before\b', text)),
        'openEnd': bool(re.match(r'\s*(not before|after)\b', text)),
    }


def dates():
    rows = []
    for c in load('oe-laws/codes.json'):
        ds = []
        for text, refs in c.get('dates', []):
            r = date_range(text)
            for ref in (refs or ['Liebermann' if not ds else '']):
                who = (ref.split(',')[0].strip() if ref else '') or 'Unattributed'
                ds.append({'by': who, 'ref': ref, 'text': plain(text), **(r or {})})
        if any('lo' in d for d in ds):
            rows.append({'code': c['code'], 'name': c.get('name', ''), 'group': c.get('group', ''), 'king': c.get('king', ''),
                         'reign': c.get('reign', ''), 'dates': ds})
    return {'codes': rows, 'groups': list(dict.fromkeys(r['group'] for r in rows))}


# ------------------------------------------------------------ 8. places

# Where each place is. Uncertain identifications are marked; the label is the text's own.
PLACES = {
    'Winchester': (51.0632, -1.3080, ''),
    'Enham': (51.2380, -1.4700, 'King’s Enham, near Andover, Hampshire'),
    '?King’s Enham': (51.2380, -1.4700, 'King’s Enham, near Andover, Hampshire (uncertain)'),
    'Oxford': (51.7520, -1.2577, ''),
    '?Bath Abbey': (51.3811, -2.3590, 'uncertain'),
    'Bath': (51.3811, -2.3590, ''),
    'Grately': (51.1700, -1.6000, 'Hampshire'),
    'London': (51.5114, -0.0900, 'the City'),
    'Andover': (51.2110, -1.4920, 'Hampshire'),
    'Wihtbordesstan': (None, None, 'unidentified'),
    'Wantage, Wessex': (51.5880, -1.4260, 'Oxfordshire (formerly Berkshire)'),
    'Westminster': (51.4995, -0.1248, ''),
    'Exeter': (50.7184, -3.5339, 'Devon'),
    'Woodstock, Mercia': (51.8480, -1.3540, 'Oxfordshire'),
    'Woodstock': (51.8480, -1.3540, 'Oxfordshire'),
    '?Archenfield, on the Wye': (51.9300, -2.7500, 'Ergyng, south-west Herefordshire (uncertain)'),
    'Ðunresfeld': (51.1700, -0.1500, 'perhaps Thunderfield, near Horley, Surrey (uncertain)'),
    'Culinton (?Colyton, Devonshire)': (50.7390, -3.0690, 'Colyton, Devon (uncertain)'),
    'Reading': (51.4543, -0.9781, 'Berkshire'),
    'Kingston, if 978–9': (51.4123, -0.3007, 'Kingston upon Thames (if 978–9)'),
}


def places():
    codes = {c['code']: c for c in codes_list()}
    out = []
    for c in load('oe-laws/codes.json'):
        for place, refs in c.get('places', []):
            lat, lng, note = PLACES.get(place, (None, None, ''))
            k = codes[c['code']]
            out.append({'code': c['code'], 'name': c.get('name', ''), 'group': c.get('group', ''), 'date': k['date'],
                        'year': k['year'], 'place': place, 'refs': refs, 'lat': lat, 'lng': lng, 'note': note,
                        'clauses': k['clauses']})
    return {'rows': out, 'groups': list(dict.fromkeys(r['group'] for r in out))}


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
    write('manuscripts.html', 'manuscripts-and-codes.html', manuscripts())
    write('subjects.html', 'subjects-together.html', subjects())
    write('chains.html', 'reuse-chains.html', chains())
    write('dates.html', 'dating-the-codes.html', dates())
    write('places.html', 'where-codes-were-made.html', places())
