#!/usr/bin/env python3
"""Writes the clause files of the Leges Edwardi Confessoris (ECf) and of the ECf retractatus
from the transcriptions in tools/ecf/pages/*.py (one file per page of Liebermann, Gesetze I),
and adds their rows to oe-laws/index.json and oe-laws/codes.json.

A page file defines CLAUSES: a list of dicts
  code     'ECf' or 'ECfRetr'
  n        Liebermann's number as printed in the margin ('Inscr.', 'Prol.', 'Prol. 1', '2,9a' …)
  page     page of Gesetze I (int)
  text     Liebermann's Latin, with markers: {N} numbered textual note N, {f:x} lettered footnote x,
           {*} the asterisk note, <b>..</b> bold (the Retractator's changes), [[pb]] page break
  notes    {N: (German, English)} textual notes; lettered: {'f:x': (German, English)}; '*': (..)
  margin   Liebermann's marginal references (comparisonPrinted), optional
  editorial  editorial remarks, optional
German may contain <i>..</i> for Liebermann's italics (his own words, as against the readings).
Run:  python3 tools/ecf/build_ecf.py
"""
import glob, html, json, os, re, runpy, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NAMES = {'ECf': ('ECf', 'ECf', 'Leges Edwardi Confessoris', '1115–50, probably 1130–35 (Liebermann, I p. 627)'),
         'ECfRetr': ('ECf retr', 'ECfRetr', 'Leges Edwardi Confessoris: retractatus', 'c. 1140–59 (Liebermann, I p. 627)')}
OTHER = {'ECf': 'ECfRetr', 'ECfRetr': 'ECf'}

def slug(n):
    n = n.replace('Inscr.', 'Inscr').replace('Prol.', 'Prol')
    return re.sub(r'[^A-Za-z0-9]+', '-', n).strip('-')

def cit(code, n):
    return NAMES[code][0] + ' ' + n

def inline(s):
    s = s.replace('<i>', '<hi rend="italic">').replace('</i>', '</hi>')
    s = s.replace('<b>', '<hi rend="bold">').replace('</b>', '</hi>')
    s = s.replace('<sp>', '<hi rend="spaced">').replace('</sp>', '</hi>')
    s = s.replace('<sup>', '<hi rend="superscript">').replace('</sup>', '</hi>')
    return s

def note_id(cid, key):
    k = {'*': 'star', '**': 'star2'}.get(key, key)
    k = k.replace('f:', 'fn.').replace('/', '-p')
    return f'{cid}.lnote.la.{k}'

def build(cl, all_ids):
    code, n, page = cl['code'], cl['n'], cl['page']
    cid = f'{code}_{slug(n)}'
    pages = sorted({page} | set(cl.get('pages', [])))
    text = cl['text']
    def mark(m):
        key = m.group(1)
        shown = (key[2:] if key.startswith('f:') else key).split('/')[0]
        return f'<ptr type="liebermannNote" n="{shown}" target="#{note_id(cid, key)}"/>'
    body = re.sub(r'\{([^}]+)\}', mark, inline(text))
    body = body.replace('[[pb]]', '')
    body = f'<pb n="{page}" ed="#liebermann"/>' + re.sub(r'\[\[pb:(\d+)\]\]', r'<pb n="\1" ed="#liebermann"/>', body)
    notes = []
    for key, (de, en) in cl['notes'].items():
        key = str(key)
        sub = 'textual'   # lettered footnotes too, as in Hn: the site shows only 'textual' notes for an untranslated Latin text
        shown = (key[2:] if key.startswith('f:') else key).split('/')[0]
        pg = cl.get('notepages', {}).get(key, page)
        notes.append(f'<note type="liebermannNote" subtype="{sub}" xml:id="{note_id(cid, key)}" n="{shown}" source="#liebermann">'
                     f'<bibl><biblScope unit="volume">1</biblScope><biblScope unit="page">{pg}</biblScope></bibl>'
                     f'<seg type="original" xml:lang="de">{inline(de)}</seg><seg type="translation" xml:lang="en" source="#claude">{inline(en)}</seg></note>')
    other = f'{OTHER[code]}_{slug(n)}'
    extra = []
    if other in all_ids:
        extra.append(f'<note type="comparison" source="#liebermann" n="{page}"><label>printed alongside</label> <ref target="clause:{other}">{cit(OTHER[code], n)}</ref></note>')
    for m in cl.get('margin', []):
        extra.append(f'<note type="comparisonPrinted" source="#liebermann">{inline(m)}</note>')
    ed = ['Liebermann’s text transcribed from Gesetze I p. ' + '–'.join(map(str, [pages[0], pages[-1]] if len(pages) > 1 else pages)) +
          ' (November 2026): read from the page images and checked against the scan’s own text layer, differences settled against the page' +
          ('; the words in bold are the Retractator’s changes to ECf, as Liebermann prints them' if code == 'ECfRetr' and '<b>' in text else '') + '.']
    if cl.get('erkl'):
        ws = cl['erkl']
        q = ', '.join('“' + w + '”' for w in ws)
        ed.append(f'Liebermann’s upright (roman) letter a after {q} refers to his explanatory notes, the Erklärungen (printed as Gesetze III; his note on p. 627 calls it “Band II”), which are not yet added here.')
    ed += cl.get('editorial', [])
    for e in ed:
        extra.append(f'<note type="editorial">{inline(e)}</note>')
    name = NAMES[code]
    pg_attr = f'p. <biblScope unit="page">{pages[0]}</biblScope>' if len(pages) == 1 else f'pp. <biblScope unit="page">{pages[0]}–{pages[-1]}</biblScope>'
    keys = cl.get('keys', [f'{name[1]} {n}'])
    tei = f'''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="{cid}">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>{cit(code, n)}</title>
        <respStmt><resp>Edition of the text</resp><name ref="#liebermann">Liebermann</name></respStmt>
        <respStmt><resp>Transcription of the text, and transcription and English translation of Liebermann’s notes</resp><name ref="#claude">Claude</name></respStmt>
      </titleStmt>
      <publicationStmt>
        <publisher>eLiebermann: An Online Dictionary of Pre-Conquest English Law</publisher>
        <idno type="slug">{cid}</idno>
        <idno type="citation">{cit(code, n)}</idno>
        <idno type="lawCode">{name[0]}</idno>
        <idno type="lawCodeAnchor">{name[1]}</idno>
        <idno type="clause">{n}</idno>
{chr(10).join(f'        <idno type="citationKey">{k}</idno>' for k in keys)}
      </publicationStmt>
      <sourceDesc>
        <bibl type="legalText"><title>{name[2]}</title></bibl>
        <listBibl type="sources">
          <bibl xml:id="liebermann" type="edition"><author>Felix Liebermann</author>, <title>Die Gesetze der Angelsachsen</title>, vol. <biblScope unit="volume">1</biblScope> (Halle: Niemeyer, 1903), {pg_attr}</bibl>
          <bibl xml:id="claude" type="translation">A semi-literal English rendering of Liebermann’s German, made for this database in 2026 with Claude, a large language model (LLM) made by Anthropic. It is a crib to help the reader with Liebermann’s German, not a separate translation</bibl>
        </listBibl>
      </sourceDesc>
    </fileDesc>
    <encodingDesc>
      <listPrefixDef>
        <prefixDef ident="law" matchPattern="(.+)" replacementPattern="lawAbb.html#$1"/>
        <prefixDef ident="clause" matchPattern="(.+)" replacementPattern="law.html?id=$1"/>
        <prefixDef ident="gram" matchPattern="(.+)" replacementPattern="gramAbb.html#$1"/>
        <prefixDef ident="entry" matchPattern="(.+)" replacementPattern="entry.html?id=$1"/>
      </listPrefixDef>
    </encodingDesc>
    <profileDesc>
      <creation><date>{name[3]}</date><note type="promulgation">{name[3]}</note></creation>
    </profileDesc>
    <revisionDesc>
      <change when="2026-11-01">Transcribed from Liebermann, Gesetze I, by Claude; to be checked against the print.</change>
    </revisionDesc>
  </teiHeader>
  <text>
    <body>
      <div type="clause" n="{n}">
        <head><ref type="lawCode" target="law:{name[1]}">{name[0]}</ref> {n}</head>
        <ab type="liebermannText" xml:lang="la" source="#liebermann" n="{cit(code, n)}">{body}</ab>
        {(chr(10) + '        ').join(extra + notes)}
      </div>
    </body>
  </text>
</TEI>
'''
    ids = set(re.findall(r'xml:id="([^"]+)"', tei))
    for t in re.findall(r'<ptr [^>]*target="#([^"]+)"', tei):
        assert t in ids, (cid, t)
    return cid, tei, pages[0], keys

def main():
    clauses = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages', '*.py'))):
        clauses += runpy.run_path(f)['CLAUSES']
    ids = {f"{c['code']}_{slug(c['n'])}" for c in clauses}
    rows = {'ECf': [], 'ECfRetr': []}
    for cl in clauses:
        cid, tei, page, keys = build(cl, ids)
        open(os.path.join(REPO, 'oe-laws', cid + '.xml'), 'w').write(tei)
        name = NAMES[cl['code']]
        rows[cl['code']].append({'id': cid, 'file': cid + '.xml', 'citation': cit(cl['code'], cl['n']), 'code': name[0], 'anchor': name[1],
                                 'clause': cl['n'], 'citationKeys': keys, 'legalText': name[2], 'page': str(page), 'source': 'Liebermann, Gesetze I (transcribed 2026)'})
    def rewrite(path, keep, new_rows, after):
        rows_ = [r for r in json.load(open(path)) if keep(r)]
        last = max(i for i, r in enumerate(rows_) if after(r))
        rows_[last + 1:last + 1] = new_rows
        open(path, 'w').write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in rows_) + '\n]\n')
    # index.json: ECf rows, then ECf retr rows, after the last Hn row (Liebermann prints ECf after Hn)
    rewrite(os.path.join(REPO, 'oe-laws', 'index.json'), lambda r: not re.match(r'ECf(Retr)?_', r['id']),
            rows['ECf'] + rows['ECfRetr'], lambda r: r['id'].startswith('Hn_'))
    codes = []
    for code in ('ECf', 'ECfRetr'):
        name = NAMES[code]
        codes.append({'code': name[0], 'anchor': name[1], 'name': name[2], 'king': '', 'reign': '', 'group': 'Anglo-Latin law books',
                      'date': name[3], 'clauses': len(rows[code]), 'first': rows[code][0]['id'], 'dates': [[name[3], []]],
                      'places': [], 'editors': ['Liebermann'], 'manuscripts': []})
    # codes.json: inserted line by line after Hn (keeps the file's own spacing elsewhere)
    p = os.path.join(REPO, 'oe-laws', 'codes.json')
    lines = [l for l in open(p).read().split('\n') if not re.match(r'\{"code":"ECf( retr)?"', l)]
    at = next(i for i, l in enumerate(lines) if l.startswith('{"code":"Hn"'))
    new = [json.dumps(c, ensure_ascii=False, separators=(',', ':')) for c in codes]
    if lines[at].endswith(','):
        new = [x + ',' for x in new]
    else:   # Hn is the last code
        lines[at] += ','
        new = [x + ',' for x in new[:-1]] + new[-1:]
    lines[at + 1:at + 1] = new
    # no comma after the last code
    end = max(i for i, l in enumerate(lines) if l.startswith('{'))
    lines[end] = lines[end].rstrip(',')
    open(p, 'w').write('\n'.join(lines)); json.load(open(p))
    print({k: len(v) for k, v in rows.items()})

if __name__ == '__main__':
    main()
