"""Add Liebermann's Erklaerungen (Gesetze III, 1916) to the clause files, from JSON lists made from the page
images (tools/vol3/NAME.json). One object per note mark:
  file      clause file id (oe-laws/FILE.xml)
  text      "de": Liebermann's German translation (numbered notes); "la": his own text (lettered notes)
  ab        optional: a string the text's <ab ...> start tag must contain (e.g. 'corresp="#wit-inst-cn"')
  n         the number or letter as printed (null: a note on the whole clause)
  after     the word the mark follows, as in the file (null or "HEADING": at the start)
  occurrence  which occurrence of that word (default 1)
  page, column  of vol. III;  de, en  the note and an English rendering (<i>, <sup> allowed)
A note already in the file (same xml:id) is left alone, and so is a mark already there. A placeholder
editorial note "Liebermann's upright (roman) letter X after "W" …" (ECf) is removed when its note is added.
Run: python3 tools/vol3/add_notes.py NAME [NAME …]"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
ERKL = '<bibl xml:id="liebermann-erkl" type="commentary"><author>Felix Liebermann</author>, <title>Die Gesetze der Angelsachsen</title>, vol. <biblScope unit="volume">3</biblScope>: <title>Einleitung zu jedem Stück; Erklärungen zu einzelnen Stellen</title> (Halle: Niemeyer, 1916)</bibl>'
CLAUDE = '<bibl xml:id="claude" type="translation">English renderings of Liebermann’s German notes, created for this database in 2026 with Claude, a large language model made by Anthropic. They are cribs to help the reader with Liebermann’s German, and should not be treated as separate translations</bibl>'
ALIAS = {'canutus': 'cnuto', 'angliae': 'anglie'}

def fold(w):
    w = unicodedata.normalize('NFD', w.lower()).replace('ae', 'e').replace('ę', 'e').replace('v', 'u').replace('j', 'i')
    return re.sub(r'[^a-zæðþ0-9]', '', w)

def conv(s):
    s = (s or '').replace('&', '&amp;').replace('<i>', '\x01').replace('</i>', '\x02').replace('<sup>', '\x03').replace('</sup>', '\x04')
    s = s.replace('<', '&lt;').replace('>', '&gt;')
    return s.replace('\x01', '<hi rend="italic">').replace('\x02', '</hi>').replace('\x03', '<hi rend="superscript">').replace('\x04', '</hi>')

def slug(n): return re.sub(r'[^A-Za-z0-9]', '_', str(n)) if n else 'clause'

def run(name):
    notes = json.load(open(os.path.join(HERE, name + '.json'), encoding='utf-8'))
    by = {}
    for x in notes:
        if 'file' not in x: x['file'] = x['prefix'] + '_' + x['clause']
        by.setdefault(x['file'], []).append(x)
    added = 0
    for fid, xs in by.items():
        p = os.path.join(ROOT, 'oe-laws', fid + '.xml')
        s = open(p, encoding='utf-8').read()
        changed = False
        for x in xs:
            text = x.get('text', 'de')
            kind = 'de' if text == 'de' else 'oe'
            xid = f'{fid}.lnote.de.{slug(x["n"])}' if text == 'de' else f'{fid}.lnote.oe.erkl-{slug(x["n"])}'
            if text == 'de' and f'xml:id="{xid}"' in s and 'source="#liebermann-erkl"' not in s.split(f'xml:id="{xid}"')[1][:80]:
                xid = f'{fid}.lnote.de.erkl-{slug(x["n"])}'     # a textual note with this number exists
            ref = f'<ptr type="liebermannNote" n="{x["n"] or "*"}" target="#{xid}"/>'
            pat = (r'<ab type="translation" xml:lang="de" source="#liebermann"[^>]*>' if text == 'de' else r'<ab type="liebermannText"[^>]*>')
            ms = [m for m in re.finditer(pat, s) if not x.get('ab') or x['ab'] in m.group(0)]
            if not ms: print(f'  ! {fid}: no {text} text'); continue
            st = ms[0].end(); en = s.index('</ab>', st); ab = s[st:en]
            if f'target="#{xid}"' not in ab:
                if not x.get('after') or x['after'] == 'HEADING':
                    pos = re.match(r'(<pb[^>]*/>)?', ab).end()
                else:
                    want = fold(ALIAS.get(x['after'].lower(), x['after'])); cnt = 0; pos = None
                    for w in re.finditer(r'(<[^>]+>)|([\w’\'-]+)', ab):
                        if w.group(1): continue
                        if fold(w.group(2)) == want:
                            cnt += 1
                            if cnt == (x.get('occurrence') or 1): pos = w.end(); break
                    if pos is None:
                        # a word broken by markup or punctuation: look in the plain text
                        print(f'  ! {fid}: "{x["after"]}" ({x.get("occurrence") or 1}) not found; mark put at the end'); pos = len(ab)
                    while ab[pos:].startswith('<ptr'): pos = ab.index('/>', pos) + 2
                ab = ab[:pos] + ref + ab[pos:]
                s = s[:st] + ab + s[en:]; changed = True
            if f'xml:id="{xid}"' not in s:
                sub = 'erklaerung' if text == 'de' else 'textual'
                note = (f'        <note type="liebermannNote" subtype="{sub}" xml:id="{xid}" n="{x["n"] or "*"}" source="#liebermann-erkl"><bibl><biblScope unit="volume">3</biblScope>'
                        f'<biblScope unit="page">{x["page"]}</biblScope><biblScope unit="column">{x.get("column") or 1}</biblScope></bibl>'
                        f'<seg type="original" xml:lang="de">{conv(x["de"])}</seg><seg type="translation" xml:lang="en" source="#claude">{conv(x["en"])}</seg></note>\n')
                i = s.rindex('      </div>\n    </body>')
                s = s[:i] + note + s[i:]; added += 1; changed = True
                # the placeholder for this letter (ECf), now replaced by the note
                if x.get('n'):
                    s = re.sub(r'\s*<note type="editorial">Liebermann’s upright \(roman\) letter ' + re.escape(str(x['n'])) + r' after “[^”]*” refers to his explanatory notes[^<]*</note>', '', s, count=1)
        if not changed: continue
        if 'xml:id="liebermann-erkl"' not in s: s = s.replace('        </listBibl>', '          ' + ERKL + '\n        </listBibl>', 1)
        if 'xml:id="claude"' not in s: s = s.replace('        </listBibl>', '          ' + CLAUDE + '\n        </listBibl>', 1)
        s = s.replace('    </revisionDesc>', '      <change when="2026-11-02">Liebermann’s Erklärungen (Gesetze III, 1916) added, with his note marks in the text (read from the page images of vols. I and III).</change>\n    </revisionDesc>', 1)
        open(p, 'w', encoding='utf-8').write(s)
    print(name, 'notes added:', added)

for name in sys.argv[1:]: run(name)
