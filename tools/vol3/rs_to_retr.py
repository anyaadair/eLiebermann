"""Move the readings of manuscript Rs from the ECf notes to the retractatus (ECf retr) clauses.
Liebermann, Gesetze III p. 340 (Einleitung zu ECf, 1): he collated the London manuscript Rs (c. 1205) only
in 1913 "und bringe hier zu den Erklärungen ihre Varianten gegen Retr" — so these readings, appended to
his notes on ECf, are variants against the retractatus text; their superscript numbers are the footnote
numbers of the retr column. Each run of readings ending in "Rs" (separated from the note by " — ") is cut
from the ECf note and added to the ECf retr clause of the same number as a note on the whole clause.
Clauses of the London collection (11,1 A, 32 A–E …) have no retr text: their Rs readings stay."""
import glob, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SEP = re.compile(r'\s+—\s+')
plain = lambda x: re.sub(r'<[^>]+>', '', x).strip()
def reading(x):   # a manuscript reading: footnote numbers, abbreviations; not a sentence of German comment
    t = plain(x)
    prose = len(re.findall(r'\b(der|die|das|des|dem|den|und|ist|wohl|meint|nicht|also|auch|wird|war|als|eine?r?)\b', t))
    return ('superscript' in x or re.search(r'\w\d', t)) and not re.search(r'\b(S\. Gl|Vgl\.|vgl\.|Einl\.|Wb|Gl )', t) and prose < 2
moved = []; left = []
for p in sorted(glob.glob(os.path.join(ROOT, 'oe-laws', 'ECf_*.xml'))):
    cl = os.path.basename(p)[4:-4]; rp = os.path.join(ROOT, 'oe-laws', f'ECfRetr_{cl}.xml')
    if not os.path.exists(rp): continue
    s = open(p, encoding='utf-8').read(); r = open(rp, encoding='utf-8').read(); out = []
    def fix(m):
        note = m.group(0)
        de = re.search(r'(<seg type="original" xml:lang="de">)([\s\S]*?)(</seg>)', note)
        en = re.search(r'(<seg type="translation"[^>]*>)([\s\S]*?)(</seg>)', note)
        if not re.search(r'\bRs\b', plain(de.group(2))): return note
        ds = SEP.split(de.group(2)); es = SEP.split(en.group(2))
        if len(ds) != len(es): left.append((cl, 'German and English do not divide alike')); return note
        take = set()
        for i, x in enumerate(ds):
            if re.search(r'\bRs\b', plain(x)) and (re.search(r'\bRs\b[.\s\[\]\w]*$', plain(x)) or plain(x).startswith('Rs liest')):
                take.add(i); j = i - 1
                while j > 0 and reading(ds[j]) and j not in take: take.add(j); j -= 1
        if not take: left.append((cl, plain(de.group(2))[-90:])); return note
        whole = len(take) == len(ds)   # the note is nothing but the reading: it moves as a whole
        rd = ' — '.join(ds[i] for i in sorted(take)); re_ = ' — '.join(es[i] for i in sorted(take))
        out.append((m.group(1), rd, re_, note))
        if whole: return ''
        k = [i for i in range(len(ds)) if i not in take]
        note = note.replace(de.group(0), de.group(1) + ' — '.join(ds[i] for i in k) + de.group(3), 1)
        note = note.replace(en.group(0), en.group(1) + ' — '.join(es[i] for i in k) + en.group(3), 1)
        return note
    s2 = re.sub(r'<note type="liebermannNote"[^>]*xml:id="([^"]+)"[^>]*source="#liebermann-erkl">[\s\S]*?</note>', fix, s)
    if not out: continue
    add = ''
    for i, (nid, rd, re_, note) in enumerate(out):
        bib = re.search(r'<bibl>[\s\S]*?</bibl>', note).group(0)
        xid = f'ECfRetr_{cl}.lnote.oe.erkl-rs' + (f'-{i+1}' if i else '')
        add += (f'        <note type="liebermannNote" subtype="textual" xml:id="{xid}" n="Rs" source="#liebermann-erkl">{bib}'
                f'<seg type="original" xml:lang="de">{rd}</seg><seg type="translation" xml:lang="en" source="#claude">{re_}</seg></note>\n')
        moved.append((cl, plain(rd)[:80]))
    i = r.rindex('      </div>\n    </body>'); r = r[:i] + add + r[i:]
    if 'xml:id="liebermann-erkl"' not in r:
        erkl = re.search(r'<bibl xml:id="liebermann-erkl"[\s\S]*?</bibl>', s).group(0)
        r = r.replace('        </listBibl>', '          ' + erkl + '\n        </listBibl>', 1)
    if 'xml:id="claude"' not in r:
        r = r.replace('        </listBibl>', '          ' + re.search(r'<bibl xml:id="claude"[\s\S]*?</bibl>', s).group(0) + '\n        </listBibl>', 1)
    chg = '      <change when="2026-11-02">{}</change>\n    </revisionDesc>'
    r = r.replace('    </revisionDesc>', chg.format('Readings of MS Rs (Liebermann, Gesetze III, notes to ECf) moved here: they are variants against the retractatus (III p. 340).'), 1)
    s2 = s2.replace('    </revisionDesc>', chg.format('Readings of MS Rs moved from this note to ECf retr ' + cl.replace('-', ',') + ', the text they are variants of (Gesetze III p. 340).'), 1)
    open(p, 'w', encoding='utf-8').write(s2); open(rp, 'w', encoding='utf-8').write(r)
print(len(moved), 'readings moved;', len(left), 'left in place')
for x in left: print('  left', *x)
for x in moved[:12]: print('  moved', *x)
