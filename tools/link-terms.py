#!/usr/bin/env python3
"""
Links words of Liebermann's German (his italic) to the list of grammatical terms and
abbreviations (data/markforward.json), in every entry's text:

    <ref type="abbreviation" target="gram:ANCHOR"><abbr>word</abbr></ref>

    python3 tools/link-terms.py "in Flexion" Flexion --dry-run
    python3 tools/link-terms.py "vor vocal. Anlaut" vocal. unter

Each word given is looked up by its "Gesetze Text" in data/markforward.json. Only text in
italic and not already inside a link is touched; the longest words are linked first, so
"vor vocal. Anlaut" is one link, not three. A word must stand on its own (not inside a longer
word: Flexion is not linked in Flexionsendungen).

"unter" is linked only where it ends the italic and a headword link follows ("[unter deveir]"),
so that it is not linked in Liebermann's definitions.

Afterwards run tools/update-entries.js on the entries changed (the numbered senses are
copied from the text), then tools/link-citations.py --letter all.
"""
import argparse
import glob
import json
import os
import re
import sys

ONLY_BEFORE_HEADWORD = {'unter'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('words', nargs='+')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--entries', default='entries')
    args = ap.parse_args()
    rows = json.load(open('data/markforward.json', encoding='utf8'))
    anchor = {}
    for w in args.words:
        hit = [r for r in rows if r['Gesetze Text'] == w]
        if not hit:
            sys.exit('not on the list: ' + w)
        anchor[w] = hit[0]['Anchor']
    words = sorted(anchor, key=len, reverse=True)
    pattern = re.compile('|'.join(
        ('(?<![\\w])' if re.match(r'\w', w) else '') + re.escape(w).replace('\\ ', '\\s+') + ('(?![\\w])' if re.search(r'\w$', w) else '')
        for w in words))
    changed = {}
    for path in sorted(glob.glob(os.path.join(args.entries, '*.xml'))):
        xml = open(path, encoding='utf8').read()
        m = re.search(r'(<dictScrap type="liebermann">)([\s\S]*?)(</dictScrap>)', xml)
        if not m:
            continue
        scrap = m.group(2)
        count = [0]

        def italic(mi):
            inner, after = mi.group(1), scrap[mi.end():]
            parts = re.split(r'(<ref\b[\s\S]*?</ref>|<[^>]+>)', inner)
            out = []
            for i, part in enumerate(parts):
                if i % 2 or not part:
                    out.append(part)
                    continue
                last_text = all(not p.strip() or p.startswith('<') for p in parts[i + 1:])

                def link(mw):
                    w = re.sub(r'\s+', ' ', mw.group(0))
                    key = next((k for k in words if re.sub(r'\s+', ' ', k) == w), None)
                    if key in ONLY_BEFORE_HEADWORD:
                        # the very end of the italic, with a headword link straight after it
                        if not (last_text and not part[mw.end():].strip() and re.match(r'\s*<ref type="entry"', after)):
                            return mw.group(0)
                    count[0] += 1
                    return '<ref type="abbreviation" target="gram:%s"><abbr>%s</abbr></ref>' % (anchor[key], mw.group(0))
                out.append(pattern.sub(link, part))
            return '<hi rend="italic">' + ''.join(out) + '</hi>'

        new = re.sub(r'<hi rend="italic">((?:(?!</?hi\b)[\s\S])*?)</hi>', italic, scrap)
        if count[0]:
            changed[os.path.basename(path)[:-4]] = count[0]
            if not args.dry_run:
                open(path, 'w', encoding='utf8').write(xml[:m.start(2)] + new + xml[m.end(2):])
    print('%d links in %d entries%s' % (sum(changed.values()), len(changed), ' (dry run)' if args.dry_run else ''))
    print(' '.join(sorted(changed)))


if __name__ == '__main__':
    main()
