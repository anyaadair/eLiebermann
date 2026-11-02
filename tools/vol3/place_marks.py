"""Place Liebermann's marks for vol. III notes that are already in the clause files but have no pointer in
the text (tools/vol3/marks-*.json, read from the page images of vol. I). One object per mark:
  id     the note's xml:id;  file  (optional) the file holding the text, if not the note's own
  text   "de" (his German) or "la" (his own text);  ab  a string the <ab …> start tag must contain
  after  the word the mark follows (null: at the start);  occurrence;  n  (optional) the mark as printed
  none   true if vol. I prints no mark (nothing is done)
A pointer already standing after the word with the same number, but pointing nowhere ("#missing") or
to a note that is not in this file, is pointed at the note instead of adding a second one.
Run: python3 tools/vol3/place_marks.py marks-A marks-B …"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
def fold(w):
    w = unicodedata.normalize('NFD', w.lower()).replace('ae', 'e').replace('ę', 'e').replace('v', 'u').replace('j', 'i')
    return re.sub(r'[^a-zæðþ0-9]', '', w)
stats = {'placed': 0, 'retargeted': 0, 'none': 0, 'skipped': []}
for name in sys.argv[1:]:
    for x in json.load(open(os.path.join(HERE, name + '.json'), encoding='utf-8')):
        if x.get('none'): stats['none'] += 1; continue
        nid = x['id']; fid = x.get('file') or nid.split('.lnote')[0]
        p = os.path.join(ROOT, 'oe-laws', fid + '.xml')
        own = os.path.join(ROOT, 'oe-laws', nid.split('.lnote')[0] + '.xml')
        note = re.search(r'xml:id="' + re.escape(nid) + r'" n="([^"]*)"', open(own, encoding='utf-8').read())
        if not note: stats['skipped'].append((nid, 'note not found')); continue
        n = x.get('n') or note.group(1)
        if 'xml:id=' in (x.get('ab') or '') or x.get('text') == 'note':
            stats['skipped'].append((nid, 'mark inside a footnote')); continue
        s = open(p, encoding='utf-8').read()
        pat = r'<ab type="translation" xml:lang="de" source="#liebermann"[^>]*>' if x['text'] == 'de' else r'<ab type="liebermannText"[^>]*>'
        ms = [m for m in re.finditer(pat, s) if not x.get('ab') or x['ab'] in m.group(0)]
        if not ms: stats['skipped'].append((nid, 'no text block')); continue
        st = ms[0].end(); en = s.index('</ab>', st); ab = s[st:en]
        target = f'#{nid}' if fid == nid.split('.lnote')[0] else f'#{nid}'
        if f'target="{target}"' in ab and not x.get('repeat'): 
            # printed twice: a second entry for the same note goes in too
            pass
        if not x.get('after'):
            pos = re.match(r'(<pb[^>]*/>)?', ab).end()
        else:
            want = fold(x['after']); cnt = 0; pos = None
            for w in re.finditer(r'(<[^>]+>)|([\w’\'\[\]-]+)', ab):
                if w.group(1): continue
                if fold(w.group(2)) == want:
                    cnt += 1
                    if cnt == (x.get('occurrence') or 1): pos = w.end(); break
            if pos is None: stats['skipped'].append((nid, 'word not found: ' + x['after'])); continue
        # a pointer with this number already after the word, pointing nowhere or elsewhere: point it here
        done = False; q = pos
        while True:
            m = re.match(r'\s*<ptr type="liebermannNote" n="([^"]*)" target="([^"]*)"[^>]*/>', ab[q:])
            if not m: break
            tid = m.group(2).lstrip('#')
            if m.group(1) == n and (tid == 'missing' or f'xml:id="{tid}"' not in s):
                a = q + m.start(2); ab = ab[:a] + target + ab[a + len(m.group(2)):]; done = True; stats['retargeted'] += 1; break
            q += m.end()
        if not done:
            ab = ab[:q] + f'<ptr type="liebermannNote" n="{n}" target="{target}"/>' + ab[q:]; stats['placed'] += 1
        s = s[:st] + ab + s[en:]
        if '2026-11-02">Liebermann’s marks for his Erklärungen' not in s:
            s = s.replace('    </revisionDesc>', '      <change when="2026-11-02">Liebermann’s marks for his Erklärungen (Gesetze III) placed in the text, from the page images of vol. I.</change>\n    </revisionDesc>', 1)
        open(p, 'w', encoding='utf-8').write(s)
print({k: v if k != 'skipped' else len(v) for k, v in stats.items()})
for s in stats['skipped']: print('  skipped', *s)
