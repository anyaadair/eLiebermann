"""Guess Dictionary of Old English links for eLiebermann's Old English entries.

python3 -I tools/doe/match.py DOE-LIST.txt [DOE-LIST2.txt ...] --out out.json

Each DOE list is the tab-separated "E00946<TAB>abbod" text copied from a DOE
browse page (see README.md). Only entries whose headword falls inside the
alphabetical span of the lists are matched; the rest are left alone.

Grades: sure, likely, unsure (several DOE headwords fit), none.
"""
import sys, re, glob, json, os, unicodedata, itertools, collections

args = sys.argv[1:]
out_path = args[args.index('--out') + 1] if '--out' in args else 'doe-out.json'
lists = [a for a in args if a != '--out' and a != out_path]
ENTRIES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'entries')


# ---------- spelling (as tools/bosworth-toller/match.py) ----------
def base(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('ð', 'þ').replace('ƿ', 'w').replace('ǽ', 'æ').replace('k', 'c')
    return re.sub(r'[^a-zæþ]', '', s)


def loose(s):
    s = base(s)
    s = s.replace('ie', 'i').replace('y', 'i').replace('io', 'eo')
    s = re.sub(r'(.)\1', r'\1', s)
    s = s.replace('cg', 'g')
    s = re.sub(r'(nis|nys|nes)$', 'nes', s)
    s = re.sub(r'ian$', 'an', s)
    s = re.sub(r'ig$', 'i', s)
    return s


def lieb_variants(hw):
    """g[e]aldor -> {galdor, gealdor}; (ge)witnes."""
    parts = re.split(r'(\[[^\]]*\]|\([^)]*\))', hw.strip())
    opts = [['', p[1:-1]] if p[:1] in '[(' and p[-1:] in '])' else [p] for p in parts]
    return {''.join(c) for c in itertools.islice(itertools.product(*opts), 64)}


def verb_guesses(f):
    """Liebermann often heads an entry with the form in the laws.
    Anya's rule: -að / -eð (3rd person) -> -an / -ian. Also other verb forms."""
    out = set()
    for end, reps in (('að', ('an', 'ian')), ('eð', ('an', 'ian')), ('aþ', ('an', 'ian')), ('eþ', ('an', 'ian')),
                      ('iað', ('ian',)), ('iaþ', ('ian',)), ('ige', ('ian',)), ('ie', ('ian',)),
                      ('ode', ('ian',)), ('ede', ('an',)), ('od', ('ian',)), ('ed', ('an',)),
                      ('en', ('an',)), ('e', ('an', 'ian'))):
        if f.endswith(end) and len(f) - len(end) >= 3:
            for r in reps:
                out.add(f[:-len(end)] + r)
    return out


NOUN_ENDINGS = ['ena', 'um', 'an', 'ra', 're', 'ne', 'es', 'as', 'a', 'e', 'u', 'o']
def noun_guesses(f):
    out = set()
    for end in NOUN_ENDINGS:
        if f.endswith(end) and len(f) - len(end) >= 3:
            st = f[:-len(end)]
            out.update({st, st + 'e', st + 'u', st + 'a'})
    return out


# ---------- DOE list ----------
doe = []
for path in lists:
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line or '\t' not in line:
            continue
        eid, hw = line.split('\t', 1)
        doe.append((eid.strip(), hw.strip()))
def xform(s):
    return re.sub(r'cs|sc|x', 'x', loose(s))


by_base, by_loose, by_x = (collections.defaultdict(list) for _ in range(3))
for eid, hw in doe:
    b = base(hw)
    if b:
        by_base[b].append((eid, hw))
        by_loose[loose(hw)].append((eid, hw))
        by_x[xform(hw)].append((eid, hw))
lo, hi = min(base(h) for _, h in doe if base(h)), max(base(h) for _, h in doe if base(h))
# The lists are in the DOE's order, not strict alphabetical; take the span from first and last.
first, last = base(doe[0][1]), base(doe[-1][1])
span_lo, span_hi = first, last


def in_span(b):
    return b and span_lo <= b <= span_hi and not b.startswith('æ')


# ---------- eLiebermann entries ----------
def text(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', x)).strip()


results = []
for path in sorted(glob.glob(os.path.join(ENTRIES, '*.xml'))):
    xml = open(path, encoding='utf-8').read()
    if not re.search(r'<entry[^>]*xml:lang="ang"', xml):
        continue
    eid = os.path.basename(path)[:-4]
    orths = [text(o) for o in re.findall(r'<orth[^>]*>(.*?)</orth>', xml, re.S)[:1]]
    if not orths:
        continue
    hw = orths[0]
    heads = [h.strip() for h in hw.split(',') if h.strip()]
    if any(h.lstrip('[(').startswith('-') for h in heads):
        continue  # affixes and word-parts
    # "and-", "al-": a word-part. Match it only to a DOE word-part ("an-", "arce-").
    part = all(h.rstrip(')]').endswith('-') or h.endswith('(-)') for h in heads)
    keys = set()
    for h in heads:
        keys |= {base(v) for v in lieb_variants(h)}
    keys.discard('')
    if not any(in_span(k) for k in keys):
        continue
    is_xref = 'type="xref"' in xml
    has = re.findall(r'type="doe"><ref target="[^"]*\?(E\d+)"', xml)
    bt = [re.sub(r'\s*\(Supplement\)', '', text(t)) for t in
          re.findall(r'type="bosworthToller"><ref[^>]*>(.*?)</ref>', xml, re.S)]

    def hits(table, ks):
        found = {}
        for k in ks:
            for e in table.get(k, []):
                if part != e[1].endswith(('-', '~')):
                    continue
                found[e[0]] = e[1]
        return found

    grade, how, found = 'none', '', {}
    steps = [
        ('same spelling', by_base, keys),
        ('spelling variant (i/y/ie, double letters, -ian/-an)', by_loose, {loose(k) for k in keys}),
        ('same as the Bosworth-Toller headword', by_base, {base(b) for b in bt}),
        ('Bosworth-Toller headword, spelling variant', by_loose, {loose(b) for b in bt}),
        ('verb form (-að/-eð → -an/-ian …)', by_base, set().union(*[verb_guesses(k) for k in keys])),
        ('verb form, spelling variant', by_loose, {loose(g) for k in keys for g in verb_guesses(k)}),
        ('without ge-', by_base, {k[2:] for k in keys if k.startswith('ge') and len(k) > 5}),
        ('x / cs / sc (acsian = āxian)', by_x, {xform(k) for k in keys}),
        ('inflected noun/adjective form', by_base, set().union(*[noun_guesses(k) for k in keys])),
    ]
    for i, (label, table, ks) in enumerate(steps):
        found = hits(table, ks)
        if found:
            how = label
            if len(found) > 1:
                grade = 'unsure'
            elif i == 0:
                grade = 'sure'
            elif i <= 7:  # the Bosworth-Toller links are guesses too: never more than likely
                grade = 'likely'
            else:
                grade = 'unsure'
            break
    body = re.search(r'<entry[^>]*>(.*?)</entry>', xml, re.S)
    body = re.sub(r'<(orth|xr)\b.*?</\1>', ' ', body.group(1), flags=re.S) if body else ''
    results.append({'id': eid, 'headword': hw, 'xref': is_xref, 'bt': bt, 'existing': has, 'snippet': text(body)[:160],
                    'grade': grade, 'how': how,
                    'candidates': [{'id': k, 'headword': v} for k, v in found.items()]})

json.dump({'span': [span_lo, span_hi], 'doe_count': len(doe), 'results': results},
          open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
c = collections.Counter(r['grade'] for r in results)
print(f'DOE headwords: {len(doe)}  span {span_lo} … {span_hi}')
print(f'entries in span: {len(results)}  ', dict(c))
