"""Liebermann's vol. I footnotes added to clause files that lacked them (Cn 1020, pp. 273-275; Quadripartitus
I, its rubric lists and the Book II preface, pp. 535-543). Transcribed from the page images into
tools/vol1notes/pNNN.json: one object per mark as printed, {page, file, n, after | before, occurrence, de, en};
a mark printed again for the same note has no de/en and takes the note of its first printing on that page
(copied into each file whose text has the mark). The mark is put after (or before) that word of the file's
Liebermann text; markup in the text is kept. Safe to run again: a note or mark already there is left alone.
Run: python3 tools/vol1notes/add.py"""
import glob, json, os, re, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
CLAUDE = '<bibl xml:id="claude" type="translation">English renderings of Liebermann’s German notes, created for this database in 2026 with Claude, a large language model made by Anthropic. They are cribs to help the reader with Liebermann’s German, and should not be treated as separate translations</bibl>'

def fold(w): return re.sub(r'[^a-z0-9æðþęđ]', '', unicodedata.normalize('NFC', w.lower()))
def conv(s):
    s = (s or '').replace('&', '&amp;')
    for t, r in (('i', 'italic'), ('b', 'bold'), ('sup', 'superscript')):
        s = s.replace(f'<{t}>', f'\x01{r}\x02').replace(f'</{t}>', '\x03')
    s = s.replace('<', '&lt;').replace('>', '&gt;')
    return s.replace('\x01', '<hi rend="').replace('\x02', '">').replace('\x03', '</hi>')
SLUG = {'*': 'star', '**': 'star2', '†': 'dagger', '††': 'dagger2'}
def nid(fid, lang, n):
    k = SLUG.get(n, re.sub(r'[^A-Za-z0-9]', '_', n))
    return f'{fid}.lnote.{lang}.{"fn." if re.fullmatch(r"[a-z]+", n) else ""}{k}'

marks = []
for f in sorted(glob.glob(os.path.join(HERE, 'p*.json'))): marks += json.load(open(f, encoding='utf-8'))
first = {}
for m in marks:
    if m.get('de'): first.setdefault((m['page'], m['n']), (m['de'], m['en']))
added = notes = 0; problems = []
by = {}
for m in marks: by.setdefault(m['file'], []).append(m)
for fid, ms in by.items():
    p = os.path.join(ROOT, 'oe-laws', fid + '.xml'); s = open(p, encoding='utf-8').read()
    am = re.search(r'(<ab type="liebermannText"[^>]*>)(.*?)(</ab>)', s, re.S)
    lang = 'oe' if 'xml:lang="ang"' in am.group(1) else 'la'
    ab = am.group(2); new_notes = []
    for m in ms:
        n = m['n']; x = nid(fid, lang, n)
        ptr = f'<ptr type="liebermannNote" n="{n}" target="#{x}"/>'
        # italic, bold and spaced type inside a word (Liebermann's expansions: arceb<hi>iscopas</hi>) do not split it
        masked = re.sub(r'</?hi[^>]*>', lambda t: '\x00' * len(t.group(0)), ab)
        words = [w for w in re.finditer(r'(<[^>]+>)|([^\s<>—–,;:.!?()\[\]‘’“”]+)', masked) if w.group(2)]
        if 'before' in m:
            if m['before'] == '':
                pos = re.match(r'(?:<pb[^>]*/>|<ptr[^>]*/>)*', ab).end()
            else:
                hits = [w for w in words if fold(w.group(2)) == fold(m['before'])]
                if len(hits) < (m.get('occurrence') or 1): problems.append(f'{fid}: before "{m["before"]}" not found'); continue
                w = hits[(m.get('occurrence') or 1) - 1]; pos = w.start()
                # before an opening bracket the word follows
                while pos > 0 and ab[pos - 1] in '([': pos -= 1
        else:
            hits = [w for w in words if fold(w.group(2)) == fold(m['after'])]
            if len(hits) < (m.get('occurrence') or 1): problems.append(f'{fid}: after "{m["after"]}" not found'); continue
            pos = hits[(m.get('occurrence') or 1) - 1].end()
            while masked[pos - 1] == '\x00' and not ab[:pos].endswith('</hi>'): pos -= 1   # not inside a tag
            while ab[pos:].startswith('<ptr'): pos = ab.index('/>', pos) + 2
        # the same mark at the same place already there
        if ab[max(0, pos - 200):pos + 200].count(ptr) and f'target="#{x}"' in ab and ptr in ab[pos - len(ptr):pos + len(ptr)]: pass
        else: ab = ab[:pos] + ptr + ab[pos:]; added += 1
        if f'xml:id="{x}"' not in s and x not in [y for y, _ in new_notes]:
            de, en = first.get((m['page'], n), (None, None))
            if de is None: problems.append(f'{fid}: no note text for {n} p. {m["page"]}'); continue
            new_notes.append((x, f'        <note type="liebermannNote" subtype="textual" xml:id="{x}" n="{n}" source="#liebermann"><bibl><biblScope unit="volume">1</biblScope>'
                                 f'<biblScope unit="page">{m["page"]}</biblScope></bibl><seg type="original" xml:lang="de">{conv(de)}</seg>'
                                 f'<seg type="translation" xml:lang="en" source="#claude">{conv(en)}</seg></note>\n'))
    s = s[:am.start(2)] + ab + s[am.end(2):]
    if new_notes:
        i = s.find('        <note type="liebermannNote"')
        if i < 0: i = s.rindex('      </div>\n    </body>')
        s = s[:i] + ''.join(t for _, t in new_notes) + s[i:]; notes += len(new_notes)
        if 'xml:id="claude"' not in s: s = s.replace('        </listBibl>', '          ' + CLAUDE + '\n        </listBibl>', 1)
    open(p, 'w', encoding='utf-8').write(s)
print(added, 'marks,', notes, 'notes in', len(by), 'files')
for x in problems: print('  !', x)
