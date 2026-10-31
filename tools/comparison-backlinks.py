#!/usr/bin/env python3
"""
Copies other scholars' words onto the back-links of the law clauses.

A scholar's cross-reference is written at the clause where the scholar makes it,
    <note type="comparison" source="#whitelock" n="465"><label>inserts</label> <ref target="clause:IIIEg_7">…</ref> <quote>…</quote></note>
and the clause referred to gets a back-link,
    <note type="comparedBy" source="#whitelock" n="465"><ref target="clause:IICn_24-3">II Cn 24.3</ref></note>
This adds the label and quotation of the first to the second, so that a clause page can say
what the scholar said without opening the other clause:
    <note type="comparedBy" source="#whitelock" n="465"><label>inserts</label> <ref …>…</ref> <quote>…</quote></note>

The page is the one written where the scholar made the comment; a back-link whose page differs
is reported (and given that page). Liebermann's back-links are left alone (they carry no words).
Safe to run again. tools/laws-from-database.py writes the same when it builds the files.

    python3 tools/comparison-backlinks.py [--dry-run]
"""
import glob
import os
import re
import sys

DIR = 'oe-laws'
BACK = re.compile(r'<note type="comparedBy" source="#(?!liebermann")([^"]+)"( n="([^"]*)")?>(<ref target="clause:([^"]+)">[\s\S]*?</ref>)</note>')
FWD = re.compile(r'<note type="comparison" source="#([^"]+)"(?: n="([^"]*)")?>(?:<label>([\s\S]*?)</label> )?<ref target="clause:([^"]+)">[\s\S]*?</ref>(?: <quote>([\s\S]*?)</quote>)?</note>')


def main():
    dry = '--dry-run' in sys.argv
    files = {os.path.basename(p)[:-4]: p for p in glob.glob(os.path.join(DIR, '*.xml'))}
    cache = {}

    def forward(fid):
        if fid not in cache:
            p = files.get(fid)
            cache[fid] = [m.groups() for m in FWD.finditer(open(p, encoding='utf8').read())] if p else []
        return cache[fid]

    changed = filled = missing = 0
    mismatch = []
    for cid, p in sorted(files.items()):
        xml = open(p, encoding='utf8').read()

        def fill(m):
            nonlocal filled, missing
            src, page, ref, fid = m.group(1), m.group(3) or '', m.group(4), m.group(5)
            hits = [f for f in forward(fid) if f[0] == src and f[3] == cid]
            if not hits:
                missing += 1
                return m.group(0)
            hit = next((f for f in hits if (f[1] or '') == page), hits[0])
            if (hit[1] or '') != page:
                mismatch.append('%s ← %s (%s): p. %s here, p. %s there' % (cid, fid, src, page or '–', hit[1] or '–'))
            filled += 1
            return '<note type="comparedBy" source="#%s"%s>%s%s%s</note>' % (
                src, (' n="%s"' % hit[1]) if hit[1] else '', ('<label>%s</label> ' % hit[2]) if hit[2] else '',
                ref, (' <quote>%s</quote>' % hit[4]) if hit[4] else '')

        new = BACK.sub(fill, xml)
        if new != xml:
            changed += 1
            if not dry:
                open(p, 'w', encoding='utf8').write(new)
    print('%d back-links given words, in %d files; %d with no matching cross-reference%s' % (filled, changed, missing, ' (dry run)' if dry else ''))
    if mismatch:
        print('Pages that differ (%d):' % len(mismatch))
        print('\n'.join('  ' + x for x in mismatch))


if __name__ == '__main__':
    main()
