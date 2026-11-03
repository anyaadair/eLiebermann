"""Redirect-only entries: where Liebermann prints only the opening and closing words of a passage
("Et si quis commendauerit alterius monacho — — commendauit; o. S. 61") and sends the reader to the
place where he prints it in full. Writes data/redirects.json:
  {clause id: {"to": [{"id", "label", "page"}], "pages": ["61"]}}
- "to": the clauses where the passage is printed in full: for the Instituta Cnuti from its reading order
  (data/incn-reading.json, made by tools/incn/reading.py); for the Consiliatio Cnuti from the range in
  its label, over the clauses of I Cnut, II Cnut and the Hundred Ordinance that carry its text;
- "pages": the pages of Gesetze I he names ("o. S. 61", "s. o. S. 279—307"), for the others.
Run after either of those changes: python3 tools/redirects/build.py"""
import json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
idx = json.load(open(os.path.join(ROOT, 'oe-laws/index.json'), encoding='utf-8'))
cit = {r['id']: r['citation'] for r in idx}
def read(r): return open(os.path.join(ROOT, 'oe-laws', r['file']), encoding='utf-8').read()
def text(s):
    m = re.search(r'<ab type="liebermannText"[^>]*>(.*?)</ab>', s, re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
dash = lambda s: s.replace('—', '–')

def pages(t):
    """Pages of Gesetze I named after the — —: "o. S. 61", "s. o. S. 279—307", "S. 402 f." (not another book's)."""
    tail = t[t.rindex('— —') + 3:]
    out = []
    for m in re.finditer(r'S\.\s*(\d+)(?:\s*[—–-]\s*(\d+))?', tail):
        before = tail[max(0, m.start() - 30):m.start()]
        if re.search(r'Ed\.|Quadripartitus|Eadmer|Rule|Epist', before): continue
        out.append(m.group(1) + ('–' + m.group(2) if m.group(2) else ''))
    return out

reading = json.load(open(os.path.join(ROOT, 'data/incn-reading.json'), encoding='utf-8'))['passages']
consrows = {}   # code -> [rows in order] that carry the Consiliatio's text
for r in idx:
    if r['code'] in ('I Cn', 'II Cn', 'Hu') and 'corresp="#wit-cons-cn"' in read(r):
        consrows.setdefault(r['code'], []).append(r)

def num(x): return x.replace('.', '-')
def cons_targets(label):
    m = re.match(r'^(I|II|III) (.+?)\s*—\s*(.+)$', label)
    if not m: return []
    part, a, b = m.groups()
    code = {'I': 'I Cn', 'II': 'II Cn', 'III': 'Hu'}[part]
    rows = consrows.get(code, [])
    if part == 'I' and a == 'Prol' and b.startswith('Epil'): return rows
    if part == 'III': return rows          # III 3–3.9: the Hundred Ordinance, which it translates
    ids = [r['id'] for r in rows]
    pre = 'IICn_'
    try: i, j = ids.index(pre + num(a)), ids.index(pre + num(b))
    except ValueError: return []
    return rows[i:j + 1]

out = {}
for r in idx:
    if r['code'] not in ('In Cn', 'Cons Cn', 'Quadr I', 'Quadr Rb', 'Quadr II') and not r['code'].startswith(('Iud Dei', 'Hn')): continue
    t = text(read(r))
    if '— —' not in t: continue
    to = []
    if r['code'] == 'In Cn':
        to = [{'id': p['id'], 'label': cit.get(p['id'], p['source']), 'page': p.get('page', '')} for p in reading
              if p['printed'] == 'beside' and dash(p['incn']) == dash(r['clause']) and p['id'] != r['id']]
    elif r['code'] == 'Cons Cn':
        to = [{'id': x['id'], 'label': x['citation'], 'page': x.get('page', '')} for x in cons_targets(r['clause'])]
    out[r['id']] = {'to': to, 'pages': pages(t)}
json.dump(out, open(os.path.join(ROOT, 'data/redirects.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(out), 'redirect entries;', sum(1 for v in out.values() if v['to']), 'with links to the full text;',
      sum(1 for v in out.values() if not v['to'] and not v['pages']), 'with neither')
for k, v in out.items():
    if not v['to'] and not v['pages']: print('  neither:', k)
