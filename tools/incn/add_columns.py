#!/usr/bin/env python3
"""Adds Liebermann's Instituta Cnuti column to the clause files of the laws it translates.

Liebermann prints most of the Instituta Cnuti (In Cn) as a Latin column beside the Old English
law it translates (Gesetze I; Alfred pp. 59–89 and elsewhere). Each tools/incn/pages/pNNN.py holds
one printed page's In Cn column, as a list COLUMNS of dicts:

  clause   the clause file it belongs to ('Af_23')
  incn     the In Cn chapter, as Liebermann numbers it in the column ('III 41'), optional
  page     the page of Gesetze I
  text     the Latin, with these marks:
             {N} {*} {f:x}  Liebermann's note numbers (notes below)
             <b>…</b>       his bold type (differs in content from the source)
             <sp>…</sp>     his spaced type (differs on purpose in form)
             <sm>…</sm>     his smaller type (word for word from the source)
             (…)            his round brackets: the other recension; wrapped in <seg type="recension">
             <i>…</i>       italic
  notes    {key: (German, English)}

Safe to re-run: the column (ab corresp="#wit-inst-cn") and its notes (xml:id …lnote.incn.…) are replaced.

    python3 tools/incn/add_columns.py
"""
import re, glob, os, runpy

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIT = ('          <witness xml:id="wit-inst-cn"><abbr>Inst. Cn.</abbr> <note type="manuscript">Instituta Cnuti '
       '(Latin translation of Anglo-Saxon laws, c. 1100), as printed by Liebermann</note></witness>\n')

def inline(s):
    s = amp(s)
    s = re.sub(r'\(([^()]*)\)', r'<seg type="recension">(\1)</seg>', s)
    for t, r in (('i', 'italic'), ('b', 'bold'), ('sp', 'spaced'), ('sm', 'small')):
        s = s.replace(f'<{t}>', f'<hi rend="{r}">').replace(f'</{t}>', '</hi>')
    return s

def amp(s):
    return re.sub(r'&(?![a-zA-Z]+;|#\d+;)', '&amp;', s)

def note_inline(s):
    s = amp(s)
    for t, r in (('i', 'italic'), ('b', 'bold'), ('sp', 'spaced'), ('sm', 'small')):
        s = s.replace(f'<{t}>', f'<hi rend="{r}">').replace(f'</{t}>', '</hi>')
    return s

def nid(cid, key):
    k = {'*': 'star', '**': 'star2', '***': 'star3', '†': 'dagger'}.get(key, key)
    return f'{cid}.lnote.incn.' + k.replace('f:', 'fn.').replace('/', '-p')

def shown(key):
    return (key[2:] if key.startswith('f:') else key).split('/')[0]

def build_ab(col):
    cid = col['clause']
    def mark(m):
        k = m.group(1)
        return f'<ptr type="liebermannNote" n="{shown(k)}" target="#{nid(cid, k)}"/>'
    body = re.sub(r'\{([^}]+)\}', mark, inline(col['text']))
    body = re.sub(r'\[\[pb:(\d+)\]\]', r'<pb n="\1" ed="#liebermann"/>', body)
    n = f' n="{col["incn"]}"' if col.get('incn') else ''
    return (f'        <ab type="liebermannText" xml:lang="la" source="#liebermann"{n} corresp="#wit-inst-cn">'
            f'<pb n="{col["page"]}" ed="#liebermann"/>{body}</ab>\n')

def build_notes(col):
    out = []
    for key, (de, en) in col.get('notes', {}).items():
        key = str(key)
        pg = col.get('notepages', {}).get(key, col['page'])
        out.append(f'        <note type="liebermannNote" subtype="textual" xml:id="{nid(col["clause"], key)}" n="{shown(key)}" source="#liebermann">'
                   f'<bibl><biblScope unit="volume">1</biblScope><biblScope unit="page">{pg}</biblScope></bibl>'
                   f'<seg type="original" xml:lang="de">{note_inline(de)}</seg>'
                   f'<seg type="translation" xml:lang="en" source="#claude">{note_inline(en)}</seg></note>\n')
    return ''.join(out)

def apply(col):
    path = os.path.join(ROOT, 'oe-laws', col['clause'] + '.xml')
    s = open(path, encoding='utf-8').read()
    # remove an earlier run's column and notes
    s = re.sub(r'        <ab type="liebermannText"[^>]*corresp="#wit-inst-cn">.*?</ab>\n', '', s, flags=re.S)
    s = re.sub(r'        <note type="liebermannNote"[^>]*xml:id="[^"]*\.lnote\.incn\.[^"]*".*?</note>\n', '', s, flags=re.S)
    s = re.sub(r'      <change when="[^"]*" type="incn">.*?</change>\n', '', s)
    if 'xml:id="wit-inst-cn"' not in s:
        i = s.index('</listWit>')
        i = s.rindex('\n', 0, i) + 1
        s = s[:i] + WIT + s[i:]
    # the column goes after Liebermann's last Latin text (Q), or else after his last text
    abs_ = list(re.finditer(r'        <ab type="liebermannText"[^>]*>.*?</ab>\n', s, flags=re.S))
    lat = [m for m in abs_ if 'xml:lang="la"' in m.group(0)]
    at = (lat or abs_)[-1].end()
    s = s[:at] + build_ab(col) + s[at:]
    # notes after the last Liebermann textual note, else before </div>
    notes = list(re.finditer(r'        <note type="liebermannNote" subtype="textual".*?</note>\n', s, flags=re.S))
    at = notes[-1].end() if notes else s.rindex('      </div>')
    s = s[:at] + build_notes(col) + s[at:]
    chg = (f'      <change when="2026-11-01" type="incn">Liebermann’s Instituta Cnuti column (Gesetze I p. {col["page"]}) added by Claude, '
           f'with his notes and his kinds of type; read from the page images; to be checked against the print.</change>\n')
    i = s.index('    </revisionDesc>')
    s = s[:i] + chg + s[i:]
    open(path, 'w', encoding='utf-8').write(s)

def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'incn', 'pages', 'p*.py'))):
        for col in runpy.run_path(f)['COLUMNS']:
            apply(col); n += 1
    print(n, 'columns')

if __name__ == '__main__':
    main()
