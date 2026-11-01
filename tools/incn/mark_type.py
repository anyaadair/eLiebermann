#!/usr/bin/env python3
"""Marks Liebermann's kinds of type in Instituta Cnuti texts already in the clause files.

tools/incn/marks/pNNN.py (one per printed page) hold a list MARKS of
    (clause id, kind, phrase)            kind: 'b' bold, 'sp' spaced, 'sm' smaller type
    (clause id, kind, phrase, n)         n: the n-th occurrence of the phrase (1 = first; default 1)
The phrase is the printed words (a leading '-' when it starts inside a word broken at a line end), without Liebermann's note numbers; it is found in the clause's In Cn
text (ab corresp #wit-inst-cn or #wit-in; in an InCn_ file, Liebermann's text) with markup and note
pointers ignored, and each stretch of text inside it is wrapped in <hi rend="…">. Marks already
there are left alone, so the script is safe to re-run.

    python3 tools/incn/mark_type.py            (then tools/incn/reading.py)
"""
import glob, os, re, runpy, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REND = {'b': 'bold', 'sp': 'spaced', 'sm': 'small'}

def norm(c):
    return c.lower().replace('ę', 'e').replace('ƿ', 'w')

def mark_ab(ab, kind, phrase, nth):
    """ab: inner XML of the <ab>. Returns new inner XML, or None if the phrase is not found."""
    toks = re.split(r'(<[^>]+>)', ab)
    # plain text with a map back to (token index, char index)
    plain, where = [], []
    for ti, t in enumerate(toks):
        if t.startswith('<'):
            continue
        for ci, ch in enumerate(t):
            plain.append(ch); where.append((ti, ci))
    text = ''.join(plain)
    inner = phrase.startswith('-')        # '-rant …': starts inside a word (a word broken at the line end)
    words = phrase.lstrip('-').split()
    pat = ('' if inner else r'(?<![\w])') + r'\s*'.join(re.escape(norm(w)) for w in words) + (r'(?![\w])' if re.match(r'\w', words[-1][-1]) else '')
    ms = list(re.finditer(pat, norm(text)))
    if len(ms) < nth:
        return None
    m = ms[nth - 1]
    a, b = m.start(), m.end()
    # stretches per text token
    spans = {}
    for k in range(a, b):
        ti, ci = where[k]
        lo, hi = spans.get(ti, (ci, ci))
        spans[ti] = (min(lo, ci), max(hi, ci))
    rend = REND[kind]
    for ti, (lo, hi) in spans.items():
        t = toks[ti]
        seg = t[lo:hi + 1]
        if not seg.strip():
            continue
        # already inside the same rend?
        before = ''.join(toks[:ti])
        opens = re.findall(r'<hi rend="([^"]+)">|</hi>', before)
        stack = []
        for o in re.finditer(r'<hi rend="([^"]+)">|</hi>', before):
            if o.group(0) == '</hi>':
                stack and stack.pop()
            else:
                stack.append(o.group(1))
        if rend in stack:
            continue
        toks[ti] = t[:lo] + f'<hi rend="{rend}">' + seg + '</hi>' + t[hi + 1:]
    return ''.join(toks)

def apply(cid, kind, phrase, nth=1):
    path = os.path.join(ROOT, 'oe-laws', cid + '.xml')
    s = open(path, encoding='utf-8').read()
    if cid.startswith('InCn_'):
        pat = r'(<ab type="liebermannText"[^>]*>)(.*?)(</ab>)'
    else:
        pat = r'(<ab type="liebermannText"[^>]*corresp="#wit-in(?:st-cn)?"[^>]*>)(.*?)(</ab>)'
    found = [False]
    def fix(m):
        if found[0]:
            return m.group(0)
        new = mark_ab(m.group(2), kind, phrase, nth)
        if new is None:
            return m.group(0)
        found[0] = True
        return m.group(1) + new + m.group(3)
    t = re.sub(pat, fix, s, flags=re.S)
    if not found[0]:
        return False
    if t != s:
        if 'type="incn-type"' not in t:
            i = t.index('    </revisionDesc>')
            t = t[:i] + ('      <change when="2026-11-01" type="incn-type">Liebermann’s bold, spaced and smaller type in the Instituta Cnuti text '
                         'marked by Claude from the page images; to be checked against the print.</change>\n') + t[i:]
        open(path, 'w', encoding='utf-8').write(t)
    return True

def main():
    bad = 0; n = 0
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, 'tools', 'incn', 'marks', 'p*.py')))
    for f in files:
        for m in runpy.run_path(f)['MARKS']:
            n += 1
            if not apply(*m):
                print('NOT FOUND', os.path.basename(f), m); bad += 1
    print(n, 'marks,', bad, 'not found')

if __name__ == '__main__':
    main()
