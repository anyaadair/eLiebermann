#!/usr/bin/env python3
"""
Adds a scholar's cross-references to the clause files from a CSV in the layout of the laws
spreadsheet's sheet "Cross-references" (Scholar, Work, Page, Clause, Linked clause, Relation,
Words, Remark), for links gathered after the files were built:

    python3 tools/add-cross-references.py data/cross-references/jurasinski-sanctuary.csv [--dry-run]

Each row gives, at the clause, <note type="comparison" source="#ID" n="PAGE"><label>Relation</label>
<ref target="clause:…">Linked clause</ref> <quote>Words</quote></note>, and at the linked clause the
back-link <note type="comparedBy" …> with the same label and words. A linked "clause" that is not in
the laws database (a penitential, a saga, Exodus) is written as plain text, with no back-link.
The work is added to each file's sources (as a study) if it is not there yet. Safe to run again:
notes already there are not added twice.

The work must be listed in WORKS below (and in XR_WORKS in tools/laws-from-database.py, so that
the same rows pasted into the spreadsheet give the same notes when the files are rebuilt).
"""
import csv
import json
import re
import sys
from xml.sax.saxutils import escape

WORKS = {   # Work (as in the CSV) -> (source id, name, reference)
    'Jurasinski, Sanctuary': ('jurasinski-sanctuary', 'Jurasinski, Sanctuary',
                              'Stefan Jurasinski, ‘Sanctuary, House-Peace, and the Traditionalism of Alfred’s Laws’, '
                              '<title>The Journal of Legal History</title> 31 (2010), 129–47'),
}
XREF = re.compile(r'[ \t]*<note type="(?:comparison|comparisonPrinted|comparisonIncomplete|comparedBy)"[^>]*>.*</note>\n')


def norm(c):
    c = re.split(r'\s*[–—]\s*', c.strip())[0]
    c = re.sub(r'(?<=[A-Za-z])\.(?=\s)', '', c)          # "Af El. 13" -> "Af El 13"
    return re.sub(r'\s+', ' ', c.replace(',', '.'))


def main():
    path = next(a for a in sys.argv[1:] if not a.startswith('--'))
    dry = '--dry-run' in sys.argv
    index = json.load(open('oe-laws/index.json', encoding='utf8'))
    by_cit = {}
    for r in index:
        by_cit.setdefault(norm(r['citation']), r['id'])
    files = {}

    def load(cid):
        if cid not in files:
            files[cid] = open('oe-laws/%s.xml' % cid, encoding='utf8').read()
        return files[cid]

    def add_source(cid, sid, name, ref):
        x = load(cid)
        if 'xml:id="%s"' % sid not in x:
            x = x.replace('        </listBibl>', '          <bibl xml:id="%s" type="study">%s</bibl>\n        </listBibl>' % (sid, ref), 1)
            resp = '        <respStmt><resp>Cross-references to other clauses</resp><name ref="#%s">%s</name></respStmt>\n' % (sid, escape(name))
            m = list(re.finditer(r'[ \t]*<respStmt><resp>Cross-references to other clauses</resp>.*\n', x))
            at = m[-1].end() if m else x.index('      </titleStmt>')
            x = x[:at] + resp + x[at:]
        files[cid] = x

    def add_note(cid, note):
        x = load(cid)
        if note.strip() in x:
            return False
        div = x.index('<div type="clause"')
        m = list(XREF.finditer(x, div))
        if m:
            at = m[-1].end()
        else:
            n = re.search(r'[ \t]*<note type="(?!manuscript)', x[div:])
            at = div + n.start() if n else x.index('      </div>', div)
        files[cid] = x[:at] + note + x[at:]
        return True

    added = back = 0
    problems = []
    for row in csv.DictReader(open(path, encoding='utf8')):
        if row['Work'] not in WORKS:
            problems.append('work not listed: ' + row['Work'])
            continue
        sid, name, ref = WORKS[row['Work']]
        fid = by_cit.get(norm(row['Clause']))
        if not fid:
            problems.append('clause not in the database: ' + row['Clause'])
            continue
        tid = by_cit.get(norm(row['Linked clause']))
        page = (' n="%s"' % escape(row['Page'], {'"': '&quot;'})) if row['Page'] else ''
        label = ('<label>%s</label> ' % escape(row['Relation'])) if row['Relation'] else ''
        quote = (' <quote>%s</quote>' % escape(row['Words'])) if row['Words'] else ''
        target = ('<ref target="clause:%s">%s</ref>' % (tid, escape(row['Linked clause']))) if tid else escape(row['Linked clause'])
        add_source(fid, sid, name, ref)
        added += add_note(fid, '        <note type="comparison" source="#%s"%s>%s%s%s</note>\n' % (sid, page, label, target, quote))
        if tid:
            add_source(tid, sid, name, ref)
            back += add_note(tid, '        <note type="comparedBy" source="#%s"%s>%s<ref target="clause:%s">%s</ref>%s</note>\n' % (
                sid, page, label, fid, escape(row['Clause']), quote))
    if not dry:
        for cid, x in files.items():
            open('oe-laws/%s.xml' % cid, 'w', encoding='utf8').write(x)
    print('%d cross-references and %d back-links added, in %d files%s' % (added, back, len(files), ' (dry run)' if dry else ''))
    for p in problems:
        print('  ' + p)


if __name__ == '__main__':
    main()
