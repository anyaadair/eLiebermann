#!/usr/bin/env python3
"""
Writes Liebermann's marginal cross-references ("Vgl.") into the clause files
from data/vgl-readings.json: readings of notes that the archive.org scan cuts
off in the gutter, made from a printed copy.

    python3 tools/add-vgl.py --dry-run   # report only
    python3 tools/add-vgl.py             # write the clause files

Each reading is
    {"clause": "III As 4", "page": "170", "printed": "Vgl. II As. 23",
     "refs": ["II As 23"], "by": "Anya Adair", "date": "2026-10-27"}
with optional "remark" (an editor's remark, shown in square brackets after the
references; clauses named in "link" are linked) and optional "how" (how the note was read, for the clause's history; by default
"read from a printed copy by <by>")
with optional "link": {"V As 3.1": "VAs_3-b"} where a reference needs its
clause file named. For the clause it writes, as laws-from-database.py does:
  <note type="comparison">         the references, linked to their clauses
  <note type="comparisonPrinted">  the note as printed
and drops <note type="comparisonIncomplete"> unless the reading has "[?]".
On each clause compared it adds the clause to <note type="comparedBy"
source="#liebermann">, and takes it off any clause the old note linked to and
the new one does not. A line goes into the clause's revisionDesc. Running it
again changes nothing.

The spreadsheet these notes first came from (OE_Laws_Database, columns BA-BC)
is not in the repository: copy the readings into it, or a rebuild from it
will undo them.
"""
import argparse
import html
import importlib.util
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('lc', os.path.join(REPO, 'tools', 'link-citations.py'))
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)

COMPARED_BY = re.compile(r'[ \t]*<note type="comparedBy" source="#liebermann">(.*?)</note>\n')
REF = re.compile(r'<ref target="clause:([^"]+)">([^<]*)</ref>')


def esc(s):
    return html.escape(s, quote=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--readings', default=os.path.join(REPO, 'data', 'vgl-readings.json'))
    args = ap.parse_args()

    index = json.load(open(os.path.join(REPO, 'oe-laws', 'index.json'), encoding='utf-8'))
    by_citation = {c['citation']: c for c in index}
    order = {c['id']: i for i, c in enumerate(index)}
    clauses = lc.Clauses(os.path.join(REPO, 'oe-laws', 'index.json'), os.path.join(REPO, 'data', 'markLaw.json'))
    spellings = sorted(((s, a) for a, ss in clauses.spellings.items() for s in ss), key=lambda x: -len(x[0]))
    files = {}

    def load(cid):
        if cid not in files:
            files[cid] = open(os.path.join(REPO, 'oe-laws', cid + '.xml'), encoding='utf-8').read()
        return files[cid]

    def resolve(ref, links):
        if ref in links:
            return links[ref]
        for s, a in spellings:
            if ref == s or ref.startswith(s + ' '):
                rest = re.sub(r'(?<=\d)\.(?=\d)', ',', ref[len(s):].strip())
                rest = re.sub(r'^Pr\.?\s*(?=\d)', 'Pro ', rest)
                how, cid = clauses.find(a, (s + ' ' + rest).strip())
                return cid
        return None

    def set_compared_by(target, cid, citation, add):
        x = load(target)
        m = COMPARED_BY.search(x)
        refs = REF.findall(m.group(1)) if m else []
        refs = [r for r in refs if r[0] != cid]
        if add:
            refs.append((cid, citation))
            refs.sort(key=lambda r: order.get(r[0], 1e9))
        line = '        <note type="comparedBy" source="#liebermann">%s</note>\n' % '; '.join(
            '<ref target="clause:%s">%s</ref>' % r for r in refs) if refs else ''
        if m:
            x = x[:m.start()] + line + x[m.end():]
        elif line:
            # after Liebermann's own comparison notes, else before the other scholars' notes
            mm = list(re.finditer(r'<note type="comparison(?:Printed|Incomplete)?"(?: source="#liebermann")?[^>]*>.*?</note>\n', x))
            mm = [n for n in mm if 'source="#liebermann"' in n.group(0) or 'comparisonIncomplete' in n.group(0)]
            if mm:
                at = mm[-1].end()
            else:
                n = re.search(r'[ \t]*<note type="(?:comparison|comparedBy|editorial|translator)"', x) or re.search(r'[ \t]*</div>', x)
                at = n.start()
            x = x[:at] + line + x[at:]
        files[target] = x

    readings = json.load(open(args.readings, encoding='utf-8'))
    report = []
    for r in readings:
        c = by_citation.get(r['clause'])
        if not c:
            report.append('NOT FOUND: clause %s' % r['clause'])
            continue
        cid = c['id']
        x = load(cid)
        old = re.search(r'[ \t]*<note type="comparison" source="#liebermann"[^>]*>(.*?)</note>\n', x)
        old_targets = {t for t, _ in REF.findall(old.group(1))} if old else set()
        items, new_targets = [], []
        for ref in r['refs']:
            tid = resolve(ref, r.get('link', {}))
            if tid == cid:
                tid = None
            if re.search(r'\d|Pr', ref) and not tid:
                report.append('%s: no clause file for "%s" (left unlinked)' % (r['clause'], ref))
            items.append('<ref target="clause:%s">%s</ref>' % (tid, esc(ref)) if tid else esc(ref))
            if tid:
                new_targets.append(tid)
        remark = ''
        if r.get('remark'):
            # an eLiebermann editor's remark on the note, in square brackets, its clauses linked
            remark = esc(r['remark'])
            for t, tid in r.get('link', {}).items():
                if esc(t) in remark:
                    remark = remark.replace(esc(t), '<ref target="clause:%s">%s</ref>' % (tid, esc(t)))
                    new_targets.append(tid)
            remark = ' [%s]' % remark
        block = '        <note type="comparison" source="#liebermann" n="%s">%s%s</note>\n' % (r['page'], '; '.join(items), remark)
        block += '        <note type="comparisonPrinted" source="#liebermann">%s</note>\n' % esc(r['printed'])
        if '[?]' in r['printed']:
            block += '        <note type="comparisonIncomplete">Some of Liebermann’s notes here are cut off in the gutter of the scan used, and are still to be completed.</note>\n'
        # replace the old notes (all of them, in whatever form) with the new ones, where the first stood
        OLD = re.compile(r'[ \t]*<note type="comparison(?:Printed)?" source="#liebermann"(?:[^>]*/>|[^>]*>.*?</note>)\n|[ \t]*<note type="comparisonIncomplete">.*?</note>\n')
        m = OLD.search(x)
        if m:
            at = m.start()
            x = OLD.sub('', x)
            x = x[:at] + block + x[at:]
        else:
            n = re.search(r'[ \t]*<note type="(?:comparedBy|comparison|editorial|translator)"', x) or re.search(r'[ \t]*</div>', x)
            x = x[:n.start()] + block + x[n.start():]
        how = r.get('how') or 'read from a printed copy by %s' % r['by']
        change = '      <change when="%s">Liebermann’s marginal cross-reference (Gesetze I p. %s) %s: “%s”.</change>\n' % (
            r['date'], r['page'], esc(how), esc(r['printed']))
        x = re.sub(r'[ \t]*<change when="[^"]*">Liebermann’s marginal cross-reference \(Gesetze I p\. [^)]*\) (?:read|confirmed)[^<]*</change>\n', '', x)
        if change.strip() not in x:
            x = x.replace('    </revisionDesc>', change + '    </revisionDesc>', 1)
        files[cid] = x
        for t in old_targets - set(new_targets):
            set_compared_by(t, cid, c['citation'], False)
        for t in new_targets:
            set_compared_by(t, cid, c['citation'], True)
        report.append('%s: %s -> %s' % (r['clause'], r['printed'], ', '.join(new_targets) or '(no links)'))

    changed = 0
    for cid, x in files.items():
        path = os.path.join(REPO, 'oe-laws', cid + '.xml')
        if open(path, encoding='utf-8').read() != x:
            changed += 1
            if not args.dry_run:
                open(path, 'w', encoding='utf-8').write(x)
    print('\n'.join(report))
    print('%d clause files %s' % (changed, 'would change' if args.dry_run else 'changed'))


if __name__ == '__main__':
    main()
