#!/usr/bin/env python3
"""Add an English crib, made with an LLM (Claude, 2026), to law clauses that have no translation.

The crib of each text goes into its clause file as
    <ab type="translation" xml:lang="en" source="#claude-crib" ana="#fromLatin" corresp="#wit-…">…</ab>
beside the text it renders (same corresp, i.e. the same manuscript), and the file's header names it:
a respStmt ("LLM (Latin)", by the language) and a bibl xml:id="claude-crib" saying what it is.
ana is #fromLatin, #fromOldEnglish or #fromFrench: law.html labels the crib "English crib of the Latin" etc.

Input: JSON files of the form { "ClauseId#k": {"en": "…", "lang": "la"|"ang"|"xno"} }, where k counts the
clause file's texts (ab type liebermannText or editionText) from 0. "en" is plain text; <i>…</i> marks
untranslated Latin (chant incipits) and becomes <hi rend="italic">. A text the database tags "ang" that the
translator found to be Latin is retagged "la".

    python3 tools/add-crib.py CRIB.json [CRIB.json …]          # the cribs of the ritual texts etc.
    python3 tools/add-crib.py --incn                             # the Instituta Cnuti crib (data/incn-crib.json)

A clause that already has a translation is left alone, so running it again changes nothing.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAWS = os.path.join(ROOT, 'oe-laws')
FROM = {'la': '#fromLatin', 'ang': '#fromOldEnglish', 'xno': '#fromFrench'}
LANG_NAME = {'la': 'Latin', 'ang': 'Old English', 'xno': 'Anglo-Norman French'}
TEXT_AB = re.compile(r'<ab type="(?:liebermannText|editionText)"([^>]*)>.*?</ab>', re.S)
RESP_TMPL = '<respStmt><resp>English crib of the text</resp><name ref="#claude-crib">LLM ({})</name></respStmt>'
SHORT = {'la': 'Latin', 'ang': 'Old English', 'xno': 'French'}
TAIL = ' Square brackets mark Liebermann’s additions to the text or, now and then, words supplied for the sense; “[?]” marks a doubtful reading'


def resp(langs):
    """The crib's name, by the language it renders: "LLM (Latin)" (Anya, Nov 2026)."""
    return RESP_TMPL.format(' and '.join(SHORT[l] for l in ('la', 'ang', 'xno') if l in langs))


def bibl(langs, incn):
    def say(literal, of, short, extra):
        return (f'A {literal} English rendering of the {of}, created for this database in 2026 with Claude, a large '
                f'language model made by Anthropic. It is a crib to help the reader with the {short}, and should not be '
                'treated as a separate translation. ' + extra)
    if incn:
        what = say('relatively literal', 'Latin text of the Instituta Cnuti', 'Latin',
                   'Liebermann’s kinds of type (bold, spaced, smaller type, round brackets) are carried over onto the English words that render the marked Latin')
    else:
        names = [LANG_NAME[l] for l in ('la', 'ang', 'xno') if l in langs]
        of = names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]
        short = ' and '.join(SHORT[l] for l in ('la', 'ang', 'xno') if l in langs)
        what = say('semi-literal', of + (' texts' if len(names) > 1 else ' text'), short, TAIL.strip())
    return '<bibl xml:id="claude-crib" type="translation">' + what + '</bibl>'


def plain_to_tei(text):
    s = html.escape(text, quote=False)
    return s.replace('&lt;i&gt;', '<hi rend="italic">').replace('&lt;/i&gt;', '</hi>')


def add(fid, items, incn=False):
    """items: [(k or None, tei_text, lang)]. Returns the number of cribs written (0 if skipped)."""
    path = os.path.join(LAWS, fid + '.xml')
    s = open(path, encoding='utf-8').read()
    if '<ab type="translation"' in s:
        return 0
    texts = list(TEXT_AB.finditer(s))
    # an entry that only points to where Liebermann prints a passage in full ("Et si quis … — — commendauit;
    # o. S. 61") is never translated (Anya Adair, Nov 2026)
    if any('— —' in m.group(0) for m in texts):
        return 0
    lines, langs, retag = [], set(), []
    for k, tei_text, lang in items:
        attrs = texts[k].group(1) if k is not None and k < len(texts) else (texts[0].group(1) if len(texts) == 1 else '')
        cor = re.search(r'corresp="(#[^"]+)"', attrs)
        tagged = re.search(r'xml:lang="([^"]+)"', attrs)
        if k is not None and tagged and tagged.group(1) == 'ang' and lang == 'la':
            retag.append(k)
        langs.add(lang)
        lines.append('        <ab type="translation" xml:lang="en" source="#claude-crib" ana="' + FROM[lang] + '"'
                     + (' corresp="' + cor.group(1) + '"' if cor else '') + '>' + tei_text + '</ab>')
    # Latin texts the database tagged as Old English
    for k in sorted(retag, reverse=True):
        m = texts[k]
        s = s[:m.start()] + m.group(0).replace('xml:lang="ang"', 'xml:lang="la"', 1) + s[m.end():]
    end = s.rfind('\n      </div>\n    </body>')
    if end < 0:
        raise SystemExit(fid + ': no end of clause found')
    s = s[:end] + '\n' + '\n'.join(lines) + s[end:]
    # the header: who made it, and what it is
    t = s.rfind('</respStmt>', 0, s.find('</titleStmt>'))
    if t < 0:
        raise SystemExit(fid + ': no respStmt')
    t += len('</respStmt>')
    s = s[:t] + '\n        ' + resp(langs) + s[t:]
    lb = s.find('</listBibl>')
    if lb < 0:
        raise SystemExit(fid + ': no listBibl')
    s = s[:lb] + '  ' + bibl(langs, incn) + '\n        ' + s[lb:]
    open(path, 'w', encoding='utf-8').write(s)
    return len(lines)


def main(argv):
    done = files = retagged = 0
    if argv == ['--incn']:
        crib = json.load(open(os.path.join(ROOT, 'data', 'incn-crib.json'), encoding='utf-8'))['crib']
        by = {}
        for key, val in crib.items():
            fid = key.split('|')[0]
            if fid.startswith('InCn_'):
                by.setdefault(fid, []).append((None, val, 'la'))
        for fid, items in sorted(by.items()):
            n = add(fid, items, incn=True)
            done += n
            files += bool(n)
    else:
        by = {}
        for f in argv:
            for key, v in json.load(open(f, encoding='utf-8')).items():
                fid, k = key.split('#')
                by.setdefault(fid, []).append((int(k), plain_to_tei(v['en'].strip()), v.get('lang', 'la')))
        for fid, items in sorted(by.items()):
            n = add(fid, sorted(items))
            done += n
            files += bool(n)
    print('cribs added:', done, 'in', files, 'clause files')


if __name__ == '__main__':
    main(sys.argv[1:])
