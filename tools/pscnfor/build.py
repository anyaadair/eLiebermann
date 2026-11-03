"""Liebermann's footnotes to Pseudo-Cnut De foresta (Gesetze I pp. 620-626) into oe-laws/PsCnFor_*.xml.
Transcribed from the page images into tools/pscnfor/pNNN.json: per clause, the Latin with the marks ({1}, {f:a})
and the notes printed on that page. Liebermann sometimes prints a mark again to refer back to a note: the note is
copied into every file whose text has the mark. Volume III notes (Erklaerungen) already in the files are kept; where
a vol. III note has the same letter as a vol. I note of the clause, the one mark serves both.
Also replaces the witness "Lat" by the manuscripts of note a (Ho, St, Cii; Ho 2). Run once: python3 tools/pscnfor/build.py"""
import glob, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')

def conv(s):
    s = (s or '').replace('&', '&amp;')
    for t, r in (('i', 'italic'), ('b', 'bold'), ('sup', 'superscript')):
        s = s.replace(f'<{t}>', f'\x01{r}\x02').replace(f'</{t}>', '\x03')
    s = s.replace('<', '&lt;').replace('>', '&gt;')
    return s.replace('\x01', '<hi rend="').replace('\x02', '">').replace('\x03', '</hi>')

pages = {}
for f in sorted(glob.glob(os.path.join(HERE, 'p6*.json'))):
    for c in json.load(open(f, encoding='utf-8')):
        pages.setdefault(c['file'], []).append(c)
notes_by_page = {}
for segs in pages.values():
    for c in segs:
        for k, v in c['notes'].items(): notes_by_page[(c['page'], k)] = v

WIT = ('<witness xml:id="wit-ho-st-cii"><abbr>Ho, St, Cii</abbr> <note type="manuscript">Liebermann’s text, from Ho (William Harrison’s Description of England, prefixed to Holinshed’s Chronicles, London, 1577), St (London, British Library, Stowe MS 414) and Cii (Cambridge, University Library, MS Ii.6.53)</note></witness>\n'
       '          <witness xml:id="wit-ho"><abbr>Ho</abbr> <note type="manuscript">Holinshed’s Chronicles (London, 1577): William Harrison’s Description of England</note></witness>\n'
       '          <witness xml:id="wit-ho2"><abbr>Ho 2</abbr> <note type="manuscript">the reprint of Holinshed’s Chronicles, 1587</note></witness>\n'
       '          <witness xml:id="wit-st"><abbr>St</abbr> <note type="manuscript">London, British Library, Stowe MS 414, late 16th century</note></witness>\n'
       '          <witness xml:id="wit-cii"><abbr>Cii</abbr> <note type="manuscript">Cambridge, University Library, MS Ii.6.53, c. 1570</note></witness>')

def nid(fid, k): return f'{fid}.lnote.la.fn.{k[2:]}' if k.startswith('f:') else f'{fid}.lnote.la.{k}'
report = []
for fid, segs in pages.items():
    p = os.path.join(ROOT, 'oe-laws', fid + '.xml'); s = open(p, encoding='utf-8').read()
    m = re.search(r'(<ab type="liebermannText"[^>]*>)(.*?)(</ab>)', s, re.S); old = m.group(2)
    # vol. III marks already in the text: (n, target, the word before it)
    erkl = []
    for pm in re.finditer(r'<ptr type="liebermannNote" n="([^"]*)" target="#([^"]*erkl[^"]*)"/>', old):
        before = re.sub(r'<[^>]+>', '', old[:pm.start()]); w = re.findall(r'[\w’]+', before)
        erkl.append((pm.group(1), pm.group(2), w[-1] if w else None, len(w)))
    body, used = '', []
    for c in segs:
        t = c['text']
        def mark(mm):
            k = mm.group(1); used.append((c['page'], k))
            return f'<ptr type="liebermannNote" n="{k[2:] if k.startswith("f:") else k}" target="#{nid(fid, k)}"/>'
        t = re.sub(r'\{([^}]+)\}', mark, t)
        t = re.sub(r'\[\[pb:(\d+)\]\]', r'<pb n="\1" ed="#liebermann"/>', t)
        if not body: t = f'<pb n="{c["page"]}" ed="#liebermann"/>' + t if not t.startswith('<pb') else t
        body += t
    letters = {k[2:] for _, k in used if k.startswith('f:')}
    # put back the vol. III marks not covered by a vol. I letter
    for n, tgt, word, idx in erkl:
        if n in letters: report.append(f'{fid}: vol. III {n} shares the vol. I mark'); continue
        ptr = f'<ptr type="liebermannNote" n="{n}" target="#{tgt}"/>'
        if word is None:
            body = re.sub(r'^((?:<pb[^>]*/>)?)', lambda mm: mm.group(1) + ptr, body, count=1); continue
        cnt = 0; pos = None
        for w in re.finditer(r'(<[^>]+>)|([\w’]+)', body):
            if w.group(1): continue
            cnt += 1
            if cnt == idx: pos = w.end(); break
        if pos is None: pos = len(body); report.append(f'{fid}: vol. III {n} put at end')
        while body[pos:].startswith('<ptr'): pos = body.index('/>', pos) + 2
        body = body[:pos] + ptr + body[pos:]
    s = s[:m.start(2)] + body + s[m.end(2):]
    # the notes, before the vol. III ones
    new = ''
    for pg, k in dict.fromkeys(used):
        x = nid(fid, k)
        if f'xml:id="{x}"' in s: continue
        de, en = notes_by_page[(pg, k)]
        new += (f'        <note type="liebermannNote" subtype="textual" xml:id="{x}" n="{k[2:] if k.startswith("f:") else k}" source="#liebermann"><bibl><biblScope unit="volume">1</biblScope>'
                f'<biblScope unit="page">{pg}</biblScope></bibl><seg type="original" xml:lang="de">{conv(de)}</seg><seg type="translation" xml:lang="en" source="#claude">{conv(en)}</seg></note>\n')
    i = s.find('        <note type="liebermannNote"')
    if i < 0: i = s.rindex('      </div>\n    </body>')
    s = s[:i] + new + s[i:]
    # witnesses
    s = re.sub(r'<witness xml:id="wit-lat"><abbr>Lat</abbr></witness>', WIT, s).replace('corresp="#wit-lat"', 'corresp="#wit-ho-st-cii"')
    if 'xml:id="claude"' not in s:
        s = s.replace('        </listBibl>', '          <bibl xml:id="claude" type="translation">English renderings of Liebermann’s German notes, created for this database in 2026 with Claude, a large language model made by Anthropic. They are cribs to help the reader with Liebermann’s German, and should not be treated as separate translations</bibl>\n        </listBibl>', 1)
    open(p, 'w', encoding='utf-8').write(s)
print('\n'.join(report)); print(len(pages), 'files')
