"""Add Liebermann's Erklaerungen (Gesetze III, 1916) to clause files from a JSON list made from the page
images (tools/vol3/CODE.json): one object per note, {clause, n, after, occurrence, page, column, de, en,
doubt}. A pointer goes after the word `after` in the text the note belongs to (Liebermann's German
translation for numbered notes, his Latin text for lettered notes); after=null or "HEADING" puts it at
the start. Run: python3 tools/vol3/add_notes.py cn1020 Cn1020 de   |   ... cn1027 Cn1027 la"""
import json, os, re, sys, unicodedata
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
name, prefix, target = sys.argv[1:4]
notes = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name + '.json'), encoding='utf-8'))
ERKL = '<bibl xml:id="liebermann-erkl" type="commentary"><author>Felix Liebermann</author>, <title>Die Gesetze der Angelsachsen</title>, vol. <biblScope unit="volume">3</biblScope>: <title>Einleitung zu jedem Stück; Erklärungen zu einzelnen Stellen</title> (Halle: Niemeyer, 1916)</bibl>'

def fold(w):   # Robertson's spelling against Liebermann's: v/u, ae/ę, case, accents
    w = unicodedata.normalize('NFD', w.lower()).replace('ae', 'e').replace('ę', 'e').replace('v', 'u').replace('j', 'i')
    return re.sub(r'[^a-zæðþ]', '', w)
ALIAS = {'canutus': 'cnuto', 'angliae': 'anglie'}

def conv(s):
    s = s.replace('&', '&amp;').replace('<i>', '\x01').replace('</i>', '\x02').replace('<sup>', '\x03').replace('</sup>', '\x04')
    s = s.replace('<', '&lt;').replace('>', '&gt;')
    return s.replace('\x01', '<hi rend="italic">').replace('\x02', '</hi>').replace('\x03', '<hi rend="superscript">').replace('\x04', '</hi>')

by = {}
for x in notes: by.setdefault(x['clause'], []).append(x)
pat_ab = r'<ab type="translation" xml:lang="de" source="#liebermann"[^>]*>' if target == 'de' else r'<ab type="liebermannText"[^>]*>'
for clause, xs in by.items():
    cid = f'{prefix}_{clause}'
    p = os.path.join(ROOT, 'oe-laws', cid + '.xml')
    s = open(p, encoding='utf-8').read()
    m = re.search(pat_ab + r'([\s\S]*?)</ab>', s)
    if not m: sys.exit('no text in ' + cid)
    ab = m.group(1)
    kind = 'de' if target == 'de' else 'oe'
    # insertion points: positions in ab (outside tags) after the word
    inserts = []
    for x in xs:
        nid = x['n'] or 'clause'
        ref = f'<ptr type="liebermannNote" n="{x["n"] or "*"}" target="#{cid}.lnote.{kind}.erkl-{nid}"/>' if target == 'la' else f'<ptr type="liebermannNote" n="{x["n"]}" target="#{cid}.lnote.de.{nid}"/>'
        if not x['after'] or x['after'] == 'HEADING':
            pb = re.match(r'(<pb[^>]*/>)?', ab).end(); inserts.append((pb, ref, x)); continue
        want = fold(ALIAS.get(x['after'].lower(), x['after']))
        cnt = 0; pos = None
        for w in re.finditer(r'(<[^>]+>)|([\w’\'-]+)', ab):
            if w.group(1): continue
            if fold(w.group(2)) == want:
                cnt += 1
                if cnt == (x['occurrence'] or 1): pos = w.end(); break
        if pos is None: sys.exit(f'{cid}: "{x["after"]}" ({x["occurrence"]}) not found')
        # after a footnote pointer that already follows the word
        while ab[pos:].startswith('<ptr'):
            pos = ab.index('/>', pos) + 2
        inserts.append((pos, ref, x))
    for pos, ref, x in sorted(inserts, key=lambda t: -t[0]):
        ab = ab[:pos] + ref + ab[pos:]
    s = s[:m.start(1)] + ab + s[m.end(1):]
    # the notes, one per number (a number printed twice gets one note)
    done = set(); add = ''
    for x in xs:
        nid = x['n'] or 'clause'
        if nid in done: continue
        done.add(nid)
        xid = f'{cid}.lnote.{kind}.erkl-{nid}' if target == 'la' else f'{cid}.lnote.de.{nid}'
        if f'xml:id="{xid}"' in s: sys.exit('already there: ' + xid)
        sub = 'textual' if target == 'la' else 'erklaerung'
        add += (f'        <note type="liebermannNote" subtype="{sub}" xml:id="{xid}" n="{x["n"] or "*"}" source="#liebermann-erkl"><bibl><biblScope unit="volume">3</biblScope>'
                f'<biblScope unit="page">{x["page"]}</biblScope><biblScope unit="column">{x["column"]}</biblScope></bibl>'
                f'<seg type="original" xml:lang="de">{conv(x["de"])}</seg><seg type="translation" xml:lang="en" source="#claude">{conv(x["en"])}</seg></note>\n')
    i = s.index('      </div>\n    </body>')
    s = s[:i] + add + s[i:]
    if 'xml:id="liebermann-erkl"' not in s:
        s = s.replace('        </listBibl>', '          ' + ERKL + '\n        </listBibl>', 1)
    if 'xml:id="claude"' not in s:
        s = s.replace('        </listBibl>', '          <bibl xml:id="claude" type="translation">English renderings of Liebermann’s German notes, made for this database in 2026 with Claude, a large language model (LLM) made by Anthropic</bibl>\n        </listBibl>', 1)
    s = s.replace('    </revisionDesc>', '      <change when="2026-11-02">Liebermann’s Erklärungen (Gesetze III, 1916) added, with his note marks in the text (read from the page images of vols. I and III).</change>\n    </revisionDesc>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print(cid, len(done))
