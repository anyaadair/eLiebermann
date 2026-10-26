#!/usr/bin/env python3
"""
Links one law code wherever Liebermann's text in an entry cites it but it is
not yet linked, using its spelling and Anchor from data/markLaw.json.

    python3 tools/link-law-code.py Gethinctho --dry-run   # report only
    python3 tools/link-law-code.py Gethinctho WiLad       # link these codes

Entries are linked when they are imported, so a code added to markLaw.json
afterwards (as Geþyncðo and Wl lad were) stays unlinked in entries that
already exist. This catches them up. In the text of each entry (the
<dictScrap type="liebermann">) a spelling of the code becomes
    <ref type="lawCode" target="law:Gethinctho">Geþyncðo</ref>
except inside italic (Liebermann's German), bold (headwords), an existing
link or an abbreviation. Run tools/update-entries.js on the changed entries
and then tools/link-citations.py, so the clause numbers link too.
"""
import argparse
import glob
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'ref', 'abbr', 'hi:italic', 'hi:bold'}
TAG = re.compile(r'<(/?)([A-Za-z]+)([^>]*?)(/?)>')


def link_text(text, patterns):
    """Links the code spellings in text (a run of characters with no tags)."""
    out, count = text, 0
    for pat, spelling, anchor in patterns:
        out, n = pat.subn(lambda m: '<ref type="lawCode" target="law:%s">%s</ref>' % (anchor, m.group(0)), out)
        count += n
    return out, count


def link_scrap(scrap, patterns):
    out, stack, at, count = [], [], 0, 0
    for m in TAG.finditer(scrap):
        text = scrap[at:m.start()]
        if text and not any(s in SKIP for s in stack):
            text, n = link_text(text, patterns)
            count += n
        out.append(text)
        out.append(m.group(0))
        closing, name, attrs, selfclosing = m.group(1), m.group(2), m.group(3), m.group(4)
        if name == 'hi':
            r = re.search(r'rend="([^"]*)"', attrs)
            name = 'hi:' + (r.group(1) if r else '')
        if selfclosing:
            pass
        elif closing:
            if stack:
                stack.pop()
        else:
            stack.append(name)
        at = m.end()
    text = scrap[at:]
    if text and not any(s in SKIP for s in stack):
        text, n = link_text(text, patterns)
        count += n
    out.append(text)
    return ''.join(out), count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('anchors', nargs='+', help='Anchors in data/markLaw.json, e.g. Gethinctho')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    rows = json.load(open(os.path.join(REPO, 'data/markLaw.json'), encoding='utf-8'))
    patterns = []
    for anchor in args.anchors:
        spellings = sorted({' '.join(r['Gesetze Text'].split()) for r in rows if r['Anchor'] == anchor}, key=len, reverse=True)
        if not spellings:
            raise SystemExit('No row with Anchor %s in data/markLaw.json' % anchor)
        for s in spellings:
            body = r'\s+'.join(re.escape(w) for w in s.split())
            patterns.append((re.compile(r'(?<![\w])' + body + r'(?![\w])'), s, anchor))
    changed, total = [], 0
    for path in sorted(glob.glob(os.path.join(REPO, 'entries', '*.xml'))):
        xml = open(path, encoding='utf-8').read()
        n_file = 0

        def fix(m):
            nonlocal n_file
            body, n = link_scrap(m.group(2), patterns)
            n_file += n
            return m.group(1) + body + m.group(3)
        new = re.sub(r'(<dictScrap type="liebermann">)([\s\S]*?)(</dictScrap>)', fix, xml)
        if n_file:
            changed.append(os.path.basename(path)[:-4])
            total += n_file
            if not args.dry_run:
                open(path, 'w', encoding='utf-8').write(new)
    print('%d citations %s in %d entries' % (total, 'would be linked' if args.dry_run else 'linked', len(changed)))
    print(' '.join(changed))


if __name__ == '__main__':
    main()
