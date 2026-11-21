#!/usr/bin/env python3
"""Builds data/conscn-reading.json: the Consiliatio Cnuti in the translator's own order, for consiliatio.html.

Liebermann prints the Consiliatio only in pieces: beside I and II Cnut, which it translates (numbered to
match), beside VIII Æthelred, Be blaserum, Forfang and the Hundred Ordinance, which it adds; and on
Gesetze I pp. 618–619 a list of its chapters, giving in full only what is printed nowhere else (the title,
the prooemium, II 19.2a–d, II 22.1b, II 84.4e–6) and pointing to the rest ("— — perquirendi; s. o. S. 309—323").
This walks that list (the ConsCn clause files, in order) and puts in each pointer's place the Latin it
points to, from the clause files where it is printed. Beside each passage is the English crib of the
Old English it translates (from Liebermann's German), where there is one.

    python3 tools/conscn/reading.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAWS = os.path.join(ROOT, 'oe-laws')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'incn'))
from reading import in_range, clean, notes_of   # the Instituta builder's helpers

COLUMN = r'<ab type="liebermannText" xml:lang="la"[^>]*corresp="#wit-cons(?:-cn)?"[^>]*>(.*?)</ab>'

# Liebermann's pointers (pp. 618–619) and where they point: (code anchor, first, last clause; page) —
# None for a whole code; a page limits VIII Æthelred to the passages on that page.
POINTERS = {
    'ConsCn_I-Prol-Epil': ('ICn', None, None, None),
    'ConsCn_II-Prol-19-2': ('IICn', 'Prol.', '19.2', None),
    'ConsCn_II-20-22-1a': ('IICn', '20', '22.1a', None),
    'ConsCn_II-22-2-84-4b': ('IICn', '22.2', '84.4b', None),
    'ConsCn_II-84-4c-d': ('VIIIAtr', None, None, '267'),
    'ConsCn_II-84-4f': ('VIIIAtr', None, None, '268'),
    'ConsCn_III-1': ('Blas', None, None, None),
    'ConsCn_III-2': ('Forf', None, None, None),
    'ConsCn_III-3-3-9': ('Hu', None, None, None),
}
# Books I and II are numbered like I and II Cnut, so a Cnut passage takes its Cnut number
NUMBERED = {'ICn': 'I', 'IICn': 'II'}


def english(s, latin_first=False):
    """(English, 'la' or 'oe'): a crib of the Latin itself where there is one (the passages only in the list),
    otherwise the crib of the Old English source, made from Liebermann's German"""
    kinds = [('claude-crib', 'la'), ('claude', 'oe')] if latin_first else [('claude', 'oe')]
    for src, of in kinds:
        m = re.search(r'<ab type="translation" xml:lang="en" source="#' + src + r'"[^>]*>(.*?)</ab>', s, re.S)
        if m:
            return clean(m.group(1)), of
    return '', ''


def main():
    rows = [json.loads(l.strip().rstrip(',')) for l in open(os.path.join(LAWS, 'index.json'), encoding='utf-8') if l.strip().startswith('{')]
    by_anchor = {}
    for r in rows:
        by_anchor.setdefault(r['anchor'], []).append(r)
    out = []
    for r in by_anchor['ConsCn']:
        if r['id'] == 'ConsCn_Title':
            continue
        label = r['clause'].replace('—', '–')
        if r['id'] in POINTERS:
            anchor, a, b, page = POINTERS[r['id']]
            got = 0
            for c in by_anchor.get(anchor, []):
                if a and not in_range(c['clause'], a, b):
                    continue
                path = os.path.join(LAWS, c['file'])
                s = open(path, encoding='utf-8').read()
                for x in re.findall(COLUMN, s, re.S):
                    pg = (re.search(r'<pb n="(\d+)"', x) or [None, ''])[1]
                    if page and pg != page:
                        continue
                    num = NUMBERED.get(anchor)
                    out.append({'cons': (num + ' ' + c['clause']) if num else label, 'id': c['id'], 'source': c['citation'],
                                'printed': 'beside', 'page': pg, 'text': clean(x), **dict(zip(('en', 'enOf'), english(s))),
                                'notes': notes_of(path, clean(x))})
                    got += 1
            if not got:
                print('nothing found for', r['id'])
        else:
            path = os.path.join(LAWS, r['file'])
            s = open(path, encoding='utf-8').read()
            xs = re.findall(r'<ab type="liebermannText"[^>]*>(.*?)</ab>', s, re.S)
            text = clean(xs[0]) if xs else ''
            out.append({'cons': label, 'id': r['id'], 'source': '', 'printed': 'list',
                        'page': (re.search(r'<pb n="(\d+)"', xs[0]) or [None, ''])[1] if xs else '', 'text': text,
                        **dict(zip(('en', 'enOf'), english(s, True))), 'notes': notes_of(path, text)})
    json.dump({'_about': 'The Consiliatio Cnuti in the translator’s order, assembled by tools/conscn/reading.py from the clause files '
               '(“beside”: printed by Liebermann beside the law it translates; “list”: printed in his list, Gesetze I pp. 618–619). '
               '“en” is an English crib: of the Latin itself (enOf “la”) or of the Old English source, from Liebermann’s German (enOf “oe”).',
               'passages': out},
              open(os.path.join(ROOT, 'data', 'conscn-reading.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(out), 'passages;', sum(1 for p in out if p['en']), 'with English')


if __name__ == '__main__':
    main()
