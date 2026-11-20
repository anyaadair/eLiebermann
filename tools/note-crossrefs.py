#!/usr/bin/env python3
"""
Liebermann's cross-references in his notes to a law (Gesetze I, the footnotes), in two kinds
(decided with Anya, Nov 2026):

1. Every clause he cites in a note becomes a link inside the note, where it stands
   ("vgl. 87, 9; Hl 12 ff.; Ine 6, 5"): <ref target="clause:…">87, 9</ref>, in his German and in the
   English crib. Nothing is added to the clause's cross-references for these.
2. Those that say how the text was made also go into the clause's cross-references, as
   Liebermann's (source "#liebermann-notes"), with a back-link on the other clause:
     aus X / vielleicht aus X      (X another law)   "from" / "perhaps from"    -> source
     wiederholt aus N                                 "repeats"                  -> source
     wiederholt N                                     "repeated in"              -> used in
     aufgenommen in N                                 "taken up in"              -> used in
     wie N                                            "as in"                    -> compare
     gegen N                                          "as against"               -> contrast
   Not: "vgl." alone (a reference for the reader), lists of parallels, "gebessert aus" (an
   emendation), his subject index ("Gl Ungehorsam 3"), other books ("Ivo Decr. V 296").

    python3 tools/note-crossrefs.py Hn --dry-run [--report out.json]
    python3 tools/note-crossrefs.py Hn

Bare numbers ("87, 9") are clauses of the law itself; after another law's name they are that
law's ("Ine 13, 1 ff. 34" is Ine 34) until a semicolon and another name. A citation is linked
only if the clause is found in the database. Running it again changes nothing.
"""
import glob
import html
import importlib.util
import json
import os
import re
import sys

spec = importlib.util.spec_from_file_location('lc', os.path.join(os.path.dirname(__file__), 'link-citations.py'))
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)

CODE = sys.argv[1]
DRY = '--dry-run' in sys.argv
REPORT = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None

clauses = lc.Clauses('oe-laws/index.json', 'data/markLaw.json')
# Liebermann's spellings of the laws, without full stops ("II Cn." is II Cn, "E Cf." ECf)
SPELL = {}
for anchor, sp in clauses.spellings.items():
    for s in sp:
        k = re.sub(r'[.\s]+', ' ', s).strip()
        if len(k) >= 2 and re.match(r'^[A-ZÆ]', k) and k not in ('Gl', 'S', 'Z', 'Q', 'L', 'In', 'Lat'):
            SPELL.setdefault(k, anchor)
SPELL.update({'E Cf': 'ECf', 'ECf': 'ECf', 'Hn': 'Hn'})
names = sorted(SPELL, key=len, reverse=True)
NAME = r'(?P<name>' + '|'.join(re.escape(n).replace(r'\ ', r'\.?\s') for n in names) + r')\.?'
NUM = r'\d{1,3}(?:,\s?\d{1,3})?[a-z]{0,2}'
FF = r'(?:\s?ff?\.)?'
SELF = {'Hn': 'Hn'}.get(CODE, CODE)
# read wrongly: Liebermann's "wie 34. 3. 35, 1" (Hn 76,4b) is 34, 3 and 35, 1
EXCLUDE = {('Hn_76-4b', 'Hn_34'), ('Hn_76-4b', 'Hn_3')}

CUES_DE = r'vgl\.|wie|wiederholt aus|wiederholt|aufgenommen in|aus|auch|s\.|gegen|=|so|zu|nach|und|u\.|in|dagegen|cf\.|as|repeated in|repeated from|repeats|taken up in|from|also|see|against|and'


def find(anchor, num):
    num = re.sub(r',\s?', ',', num)
    spelling = sorted(clauses.spellings.get(anchor, [anchor]), key=len)[0] if anchor != 'Hn' else 'Hn'
    how, cid = clauses.find(anchor, spelling + ' ' + num)
    return cid


def citations(plain):
    """-> [(start, end, anchor, num, cue, external)] in a note's plain text."""
    out = []
    i = 0
    run_re = re.compile(r'(?:(?P<cue>(?<![\w.])(?:' + CUES_DE + r'))\s+)?(?:' + NAME + r'\s)?(?P<num>' + NUM + r')(?![\d\w])' + FF)
    for m in re.finditer(run_re, plain):
        pass
    # a scanner, left to right
    pos = 0
    code = None
    cue = ''
    while pos < len(plain):
        m = re.compile(r'(?:(?<![\w.])(?P<cue>' + CUES_DE + r')\s+(?:vielleicht\s+)?)?' + NAME + r'\s?(?P<num>' + NUM + r')(?![\d\w])').search(plain, pos)
        b = re.compile(r'(?<![\w.,])(?P<cue>' + CUES_DE + r')\s+(?:z\. B\.\s+)?(?P<num>\d{1,3}(?:,\s?\d{1,3})[a-z]{0,2}|\d{1,3}[a-z]?(?=\s?ff?\.|[;.,)\]]|$))(?![\d\w])').search(plain, pos)
        # the earlier of a named citation and a bare one after a cue
        cand = [x for x in (m, b) if x]
        if not cand:
            break
        x = min(cand, key=lambda y: y.start('num'))
        if x is m:
            name = re.sub(r'[.\s]+', ' ', x.group('name')).strip()
            anchor = SPELL.get(name)
        else:
            anchor = SELF
        before = plain[max(0, x.start() - 25):x.start()]
        cue = (x.group('cue') or '').strip()
        near = plain[max(0, x.start('num') - 40):x.start('num')].split(';')[-1]
        lead = 'perhaps' if ('vielleicht' in near or plain[x.end('num'):x.end('num') + 1] == '?') else 'probably' if 'wohl' in near else ''
        if cue == 'aus' and 'dagegen' in near:
            cue = 'aus (of another clause)'
        # not an emendation's source, a page, a book
        if anchor and not re.search(r'(gebessert|verbessert|bessere|S\.|p\.)\s*$', before.strip() + ' ' if not cue else before):
            out.append([x.start('num'), x.end('num'), anchor, x.group('num'), cue, anchor != SELF, lead])
        pos = x.end('num')
        # its run: ". 92, 3a", "; 6, 1", " ff. 34", "= II Cn 30, 7"
        while True:
            r = re.compile(r'(?:\s?ff?\.)?\s*([.;]|\s?=)\s*(?:' + NAME + r'\s?)?(?P<num>' + NUM + r')(?![\d\w])(?!\s?(?:Jh|Z\.|S\.|sol|den|Pfund|Denar|Tage|Jahr))').match(plain, pos)
            if not r:
                break
            if r.group('name'):
                anchor = SPELL.get(re.sub(r'[.\s]+', ' ', r.group('name')).strip())
                if r.group(1).strip() != '=':
                    cue = ''
            elif r.group(1) == ';':
                pass
            num = r.group('num')
            # Liebermann's "92, 15; 19" is 92, 15 and 92, 19: after a clause with a comma, a semicolon and a
            # bare number name another subsection of the same clause
            prev = out[-1] if out else None
            if r.group(1) == ';' and not r.group('name') and ',' not in num and prev and ',' in prev[3] and prev[2] == anchor:
                num = prev[3].split(',')[0] + ', ' + num
            if anchor:
                out.append([r.start('num'), r.end('num'), anchor, num, cue if r.group(1) != ';' else ('' if cue in ('wie', 'gegen') else cue), anchor != SELF, lead])
            pos = r.end('num')
    return out


def label_for(cue, external, lead):
    if cue == 'aus' and external:
        return (lead + ' from') if lead else 'from'
    if cue == 'wiederholt aus' and not external:
        return 'repeats'
    if cue == 'wiederholt' and not external:
        return 'repeated in'
    if cue == 'aufgenommen in' and not external:
        return 'taken up in'
    if cue == 'wie' and not external:
        return 'as in'
    if cue == 'gegen':
        return 'as against'
    return None


def plain_map(xml):
    """the text of a piece of TEI, and for each character its place in the XML"""
    chars, where = [], []
    i = 0
    while i < len(xml):
        if xml[i] == '<':
            j = xml.index('>', i)
            i = j + 1
            continue
        if xml[i] == '&':
            j = xml.index(';', i)
            chars.append(html.unescape(xml[i:j + 1]))
            where.append(i)
            i = j + 1
            continue
        chars.append(xml[i])
        where.append(i)
        i += 1
    return ''.join(chars), where


def link_seg(seg, cits_for_seg, here):
    """wrap each citation's number in <ref>, inside one text run only (not across tags)"""
    plain, where = plain_map(seg)
    edits = []
    found = []
    for s, e, anchor, num, cue, ext, lead in cits_for_seg(plain):
        # a letter in italic straight after ("12<hi>b</hi>"): part of the number
        tail = re.match(r'([a-z]{1,2})(?![\w])', plain[e:])
        full = num + (tail.group(1) if tail and not re.search(r'[a-z]$', num) else '')
        cid = find(anchor, full)
        if not cid or cid == here or (here, cid) in EXCLUDE:
            continue
        xs, xe = where[s], where[e - 1] + 1
        if '<' in seg[xs:xe]:
            xe = xs + seg[xs:xe].index('<')
            if xe <= xs:
                continue
        edits.append((xs, xe, cid))
        found.append(dict(cue=cue, external=ext, lead=lead, anchor=anchor, num=full, clause=cid, ctx=plain[max(0, s - 50):e + 15]))
    for xs, xe, cid in sorted(edits, reverse=True):
        if seg[max(0, xs - 40):xs].endswith('">') and 'target="clause:' in seg[max(0, xs - 80):xs]:
            continue
        seg = seg[:xs] + '<ref target="clause:' + cid + '">' + seg[xs:xe] + '</ref>' + seg[xe:]
    return seg, found


def anchor_words(s, note_id, n=4):
    """The last few words of the clause text before the note's mark, to say what the note is on."""
    m = re.search(r'<ptr [^>]*target="#' + re.escape(note_id) + '"', s)
    if not m:
        return ''
    before = s[max(0, m.start() - 1500):m.start()]
    before = re.split(r'<(?:p|seg|ab|head)\b[^>]*>', before)[-1]
    t = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', before))).strip()
    t = re.sub(r' ([,.;:])', r'\1', t)
    w = t.split(' ')
    return ('… ' if len(w) > n else '') + ' '.join(w[-n:])


def main():
    report = []
    changed = 0
    files = sorted(glob.glob(f'oe-laws/{CODE}_*.xml'))
    back = {}
    for p in files:
        here = os.path.basename(p)[:-4]
        s = open(p, encoding='utf-8').read()
        new = s
        rels = []
        for nm in list(re.finditer(r'<note type="liebermannNote" subtype="textual"[^>]*>.*?</note>', s, re.S)):
            note = nm.group(0)
            page = (re.search(r'<biblScope unit="page">([^<]*)</biblScope>', note) or [None, ''])[1]
            n2 = note
            segs = {}
            for t in ('original', 'translation'):
                sm = re.search(r'(<seg type="' + t + r'"[^>]*>)(.*?)(</seg>)', n2, re.S)
                if not sm:
                    continue
                newseg, found = link_seg(sm.group(2), citations, here)
                segs[t] = found
                n2 = n2[:sm.start(2)] + newseg + n2[sm.end(2):]
            if n2 != note:
                new = new.replace(note, n2, 1)
            en = re.search(r'<seg type="translation"[^>]*>(.*?)</seg>', note, re.S)
            en_text = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', en.group(1)))).strip() if en else ''
            # only Liebermann's lettered notes, on the content (his numbered notes give the manuscripts' readings,
            # where "wie 70, 5" says that a manuscript reads as in 70, 5)
            lettered = re.match(r'^[a-z]{1,2}$', (re.search(r' n="([^"]*)"', note) or [None, ''])[1]) is not None
            de_text = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', (re.search(r'<seg type="original"[^>]*>(.*?)</seg>', note, re.S) or [None, ''])[1]))).strip()
            nid = (re.search(r'xml:id="([^"]*)"', note) or [None, ''])[1]
            anc = anchor_words(s, nid)
            for f in segs.get('original', []):
                lab = label_for(f['cue'], f['external'], f['lead']) if lettered else None
                if lab == 'as in' and not de_text.startswith('wie '):
                    lab = None
                if (here, f['clause']) in EXCLUDE:
                    lab = None
                if lab:
                    rels.append(dict(clause=here, label=lab, target=f['clause'], page=page, quote=(anc + ': ' if anc and (anc.startswith('…') or len(anc.split()) > 2) else '') + en_text, ctx=f['ctx']))
                report.append(dict(clause=here, target=f['clause'], cue=f['cue'], label=lab, ctx=f['ctx'], page=page, quote=en_text, anchor=anc, de=de_text, note=nid))
        # the cross-references: written once, after the clause's other comparisons
        seen = set()
        lines = []
        for r in rels:
            key = (r['label'], r['target'])
            if key in seen:
                continue
            seen.add(key)
            cit = clauses.citation.get(r['target'], r['target'])
            q = html.escape(r['quote'] if len(r['quote']) <= 220 else r['quote'][:217].rsplit(' ', 1)[0] + ' …', quote=False)
            line = f'        <note type="comparison" source="#liebermann-notes" n="{r["page"]}"><label>{r["label"]}</label> <ref target="clause:{r["target"]}">{html.escape(cit, quote=False)}</ref> <quote>{q}</quote></note>\n'
            if line.strip() not in new:
                lines.append(line)
            back.setdefault(r['target'], []).append((here, r))
        if lines:
            at = new.index('        <note type="editorial">') if '        <note type="editorial">' in new else new.index('        <note type="liebermannNote"')
            new = new[:at] + ''.join(lines) + new[at:]
        if new != s:
            changed += 1
            if not DRY:
                open(p, 'w', encoding='utf-8').write(new)
    # back-links on the clauses referred to
    for target, items in back.items():
        p = f'oe-laws/{target}.xml'
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        add = ''
        for here, r in items:
            cit = clauses.citation.get(here, here)
            q = html.escape(r['quote'] if len(r['quote']) <= 220 else r['quote'][:217].rsplit(' ', 1)[0] + ' …', quote=False)
            line = f'        <note type="comparedBy" source="#liebermann-notes" n="{r["page"]}"><label>{r["label"]}</label> <ref target="clause:{here}">{html.escape(cit, quote=False)}</ref> <quote>{q}</quote></note>\n'
            if line.strip() not in s and line not in add:
                add += line
        if add:
            at = s.index('        <note type="editorial">') if '        <note type="editorial">' in s else (s.index('        <note type="liebermannNote"') if '        <note type="liebermannNote"' in s else s.index('      </div>'))
            s = s[:at] + add + s[at:]
            if not DRY:
                open(p, 'w', encoding='utf-8').write(s)
    print(f'{CODE}: {len(files)} files, {changed} changed; citations linked {len(report)}; cross-references {sum(1 for r in report if r["label"])}')
    if REPORT:
        json.dump(report, open(REPORT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)


main()
