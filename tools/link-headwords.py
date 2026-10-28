#!/usr/bin/env python3
"""
Links the words in Liebermann's text that send the reader to another entry:
the words after "s." (siehe), before "s. d." (siehe dort), after "vgl."
(vergleiche) and after "Der." (Derivativa und Composita). Each becomes

    <ref type="entry" target="entry:ID">word</ref>

and the entry page shows it as a link to that entry, with a preview of it
when the pointer rests on it. A word with Liebermann's brackets is linked part
by part: in "(sulh)æcer", "sulh" goes to sulhæcer and "æcer" to æcer; in
"þær(on, ~to)", "þær", "on" and "~to" go to þær, þæron and þærto.

The words are found and matched to entries exactly as for the "See also" and
"Compare" lists (tools/see-also.py), so the links in the text and the lists
under the entry agree. A word is linked only when it matches one entry; a
word that matches none, or several, stays plain text.

    python3 tools/link-headwords.py --dry-run     # report only
    python3 tools/link-headwords.py               # every entry
    python3 tools/link-headwords.py a-6 aa        # just these

A word linked by hand, where Liebermann does not use "s." or "vgl."
(<ref type="entry" subtype="manual" target="entry:ID">), is left as it is.

Run it after tools/see-also.py (all three kinds: plain, --compare, --derivatives), and then tools/update-entries.js
on the changed entries, so the numbered meanings get the links too. Running
it again changes nothing.
"""
import argparse
import glob
import importlib.util
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('see_also', os.path.join(REPO, 'tools', 'see-also.py'))
sa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sa)

SIEHE_ABBR = sa.ABBR
VGL_ABBR = re.compile(r'(?P<open><hi rend="italic">)?<ref type="abbreviation" target="gram:(?P<kind>vergleiche)"><abbr>(?P<text>[^<]*)</abbr></ref>')
DER_ABBR = re.compile(r'(?P<open><hi rend="italic">)?<ref type="abbreviation" target="gram:(?P<kind>Derivativ)"><abbr>(?P<text>[^<]*)</abbr></ref>')


def mode(which):
    """Set see-also.py to read "s." (see), "vgl." (compare) or "Der." (derivatives)."""
    sa.COMPARE, sa.DERIV = which == 'vgl', which == 'der'
    if which == 'vgl':
        sa.SIEHE, sa.OTHER, sa.ABBR = {'vergleiche': 'after'}, (), VGL_ABBR
    elif which == 'der':
        sa.SIEHE, sa.OTHER, sa.ABBR = {'Derivativ': 'after'}, (), DER_ABBR
    else:
        sa.SIEHE = {'siehe': 'after', 'sieheDort': 'before'}
        sa.OTHER = ('sieheOben', 'sieheUnten', 'sieheNummer', 'sieheZu', 'sieheDN', 'sieheDortUnter')
        sa.ABBR = SIEHE_ABBR


def wrap_token(token, segments):
    """The token with each segment that matches one entry made a link."""
    out, at = '', 0
    for seg, ids in segments:
        k = token.find(seg, at)
        if k < 0:
            continue
        out += token[at:k]
        if len(ids) == 1 and re.search(r'[^\W\d_]', seg):
            out += '<ref type="entry" target="entry:%s">%s</ref>' % (ids[0], seg)
        else:
            out += seg
        at = k + len(seg)
    return out + token[at:]


def link(scrap, entry_id, index):
    """-> the text with the cross-referenced words linked, and the number of links."""
    plain = sa.strip_entry_links(scrap)
    # what each abbreviation's words matched: (kind, n) -> [(token, segments)]
    found = {}
    for which in ('s', 'vgl', 'der'):
        mode(which)
        sa.INLINE.clear()
        sa.targets(plain, entry_id, index)
        for kind, n, tok, segs in sa.INLINE:
            found.setdefault((which, n), []).append((tok, segs, kind))
    mode('s')
    if not found:
        return plain, 0
    # Put the links in, abbreviation by abbreviation, from the end so that the
    # positions found earlier stay right.
    edits = []
    for which, regex in (('s', SIEHE_ABBR), ('vgl', VGL_ABBR), ('der', DER_ABBR)):
        for n, m in enumerate(regex.finditer(plain)):
            items = found.get((which, n))
            if not items:
                continue
            kind = items[0][2]
            if kind == 'sieheDort':
                # the words before "s. d.": the text after the last tag before it
                # (past a translation in brackets: "habban (erhalten) s. d.")
                gloss = sa.GLOSS.search(plain[:m.start()])
                end = gloss.start() if gloss else m.start()
                start = plain.rfind('>', 0, end) + 1
            else:
                start = m.end()
                if plain.startswith('.', start) and which == 'vgl':
                    start += 1
                if plain.startswith(':', start) and which == 'der':
                    start += 1
                zb = sa.ZB.match(plain, start)
                if zb:
                    start = zb.end()
                if plain.startswith('</hi>', start):
                    start += 5
                # the list runs to the next tag, past an editor's note marker
                nxt = re.compile(r'<(?!ptr type="editorNote")').search(plain, start)
                end = nxt.start() if nxt else len(plain)
            node = plain[start:end]
            new, at = '', 0
            for tok, segs, _ in items:
                k = node.find(tok, at)
                if k < 0:
                    continue
                new += node[at:k] + wrap_token(tok, segs)
                at = k + len(tok)
            new += node[at:]
            if new != node:
                edits.append((start, end, new))
    # Two lists can share a stretch of text ("…, d, th s. d."): keep the first
    # edit of any that overlap, so no link is written into another.
    kept, last = [], -1
    for start, end, new in sorted(edits):
        if start >= last:
            kept.append((start, end, new))
            last = end
    count = 0
    for start, end, new in sorted(kept, reverse=True):
        count += new.count('<ref type="entry"')
        plain = plain[:start] + new + plain[end:]
    return plain, count


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--entries', default=os.path.join(REPO, 'entries'))
    args = ap.parse_args()
    index = sa.Index(args.entries)
    paths = [os.path.join(args.entries, i + '.xml') for i in args.ids] if args.ids else sorted(glob.glob(os.path.join(args.entries, '*.xml')))
    changed, links = [], 0
    for path in paths:
        text = sa.read(path)
        m = sa.SCRAP.search(text)
        if not m:
            continue
        entry_id = os.path.basename(path)[:-4]
        new_scrap, n = link(m.group(2), entry_id, index)
        links += n
        if new_scrap != m.group(2):
            changed.append(entry_id)
            if not args.dry_run:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(text[:m.start(2)] + new_scrap + text[m.end(2):])
    print('%d entries; %d words linked; %d entries %s' % (len(paths), links, len(changed), 'would change' if args.dry_run else 'changed'))
    if len(changed) <= 40:
        print(' '.join(changed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
