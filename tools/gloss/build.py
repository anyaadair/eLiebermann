"""Iudicium Dei IV and V (Durham Ritual, Gesetze I pp. 409-412): set the Old English interlinear gloss over
the Latin, as Liebermann prints it. tools/gloss/align-IV.json and align-V.json give, for each clause, the
groups [laStart, laEnd, glStart, glEnd] (token ranges, read from the page images): the gloss tokens printed
above those Latin tokens. The separate gloss text (witness Gl), its English crib and the Gl witness go; the
Latin text becomes
  <seg type="glossed"><seg type="base">Latin</seg><gloss xml:lang="ang">Old English</gloss></seg> …
and law.html shows each pair with the gloss above (HTML <ruby>). Run once."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
def toks(x):
    out, cur, depth = [], '', 0
    for ch in x:
        if ch == '<': depth += 1
        if ch == '>': depth -= 1
        if ch.isspace() and depth == 0:
            if cur: out.append(cur); cur = ''
        else: cur += ch
    if cur: out.append(cur)
    return out
align = {}
for f in ('align-IV.json', 'align-V.json'): align.update(json.load(open(os.path.join(HERE, f), encoding='utf-8')))
for fid, groups in align.items():
    p = os.path.join(ROOT, 'oe-laws', fid + '.xml'); s = open(p, encoding='utf-8').read()
    oe = re.search(r'\s*<ab type="liebermannText" xml:lang="ang"[^>]*>([\s\S]*?)</ab>', s)
    if not oe: continue
    la = re.search(r'(<ab type="liebermannText" xml:lang="la"[^>]*)>(<pb[^>]*/>)?([\s\S]*?)</ab>', s)
    lt, gt = toks(la.group(3)), toks(re.sub(r'^<pb[^>]*/>', '', oe.group(1)))
    assert sum(b - a for a, b, _, _ in groups) == len(lt) and sum(d - c for _, _, c, d in groups) == len(gt), fid
    parts = []
    for a, b, c, d in groups:
        base = ' '.join(lt[a:b]); gl = ' '.join(gt[c:d])
        parts.append(f'<seg type="glossed"><seg type="base">{base}</seg><gloss xml:lang="ang">{gl}</gloss></seg>' if gl else base)
    new = la.group(1) + ' ana="#glossed">' + (la.group(2) or '') + ' '.join(parts) + '</ab>'
    s = s[:la.start()] + new + s[la.end():]
    s = s.replace(oe.group(0), '', 1)
    s = re.sub(r'\s*<ab type="translation"[^>]*ana="#fromOldEnglish"[^>]*>[\s\S]*?</ab>', '', s)
    s = re.sub(r'\s*<witness xml:id="wit-gl">[\s\S]*?</witness>', '', s)
    s = s.replace('(Durham Ritual), f. 48v', '(Durham Ritual), f. 48v, with its Old English interlinear gloss', 1)
    s = s.replace('    </revisionDesc>', '      <change when="2026-11-02">The Old English gloss set over the Latin words it glosses, as Liebermann prints it (Gesetze I pp. 409–412), instead of as a separate text; its English crib removed (the crib of the Latin serves for both).</change>\n    </revisionDesc>', 1)
    open(p, 'w', encoding='utf-8').write(s); print(fid, len(groups))
