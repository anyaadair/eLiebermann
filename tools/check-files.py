#!/usr/bin/env python3
"""Checks that the site's files can be read, before a change goes live.

Runs on every pull request (.github/workflows/check.yml) and before every deploy
(.github/workflows/static.yml). It stops with a list of problems if:
  - an XML file in entries/, oe-laws/, tei/ or pages/ is not well-formed (an
    unclosed tag, a stray &, a missing quote): such a page shows only "not found";
  - a JSON file in data/ or oe-laws/ cannot be read;
  - oe-laws/index.json lists a clause file that does not exist, lists a clause
    twice, or leaves a clause file out;
  - a dictionary entry links to an entry (entry:…) or a clause (clause:…) that
    does not exist, or a clause file links to a clause that does not exist.

    python3 tools/check-files.py
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
problems = []

# XML: well-formed
xml_files = {d: sorted(glob.glob(d + '/*.xml')) for d in ('entries', 'oe-laws', 'tei', 'pages')}
for files in xml_files.values():
    for f in files:
        try:
            ET.parse(f)
        except ET.ParseError as e:
            problems.append('%s: not well-formed XML (%s)' % (f, e))

# JSON: readable (the lists written on deploy are not in the repository, so are not here)
for f in sorted(glob.glob('data/*.json') + glob.glob('oe-laws/*.json')):
    try:
        with open(f, encoding='utf-8') as fh:
            json.load(fh)
    except ValueError as e:
        problems.append('%s: not valid JSON (%s)' % (f, e))

# The clause catalogue and the clause files agree
try:
    with open('oe-laws/index.json', encoding='utf-8') as fh:
        catalogue = json.load(fh)
except (OSError, ValueError):
    catalogue = []
clause_ids = set()
listed = set()
for row in catalogue:
    if row['id'] in clause_ids:
        problems.append('oe-laws/index.json: clause %s is listed twice' % row['id'])
    clause_ids.add(row['id'])
    clause_ids.update(p['id'] for p in row.get('parts', []))
    listed.add(row['file'])
    if not os.path.exists(os.path.join('oe-laws', row['file'])):
        problems.append('oe-laws/index.json: %s is listed, but oe-laws/%s does not exist' % (row['id'], row['file']))
for f in xml_files['oe-laws']:
    if os.path.basename(f) not in listed:
        problems.append('%s: not listed in oe-laws/index.json, so the site cannot show it' % f)

# Links between entries and clauses
entry_ids = {os.path.basename(f)[:-4] for f in xml_files['entries']}
for f in xml_files['entries'] + xml_files['oe-laws']:
    with open(f, encoding='utf-8') as fh:
        text = fh.read()
    for target in sorted(set(re.findall(r'target="clause:([^"]+)"', text))):
        if target not in clause_ids:
            problems.append('%s: links to clause:%s, which is not in oe-laws/index.json' % (f, target))
    if f.startswith('entries/'):
        for target in sorted(set(re.findall(r'target="entry:([^"#]+)', text))):
            if target not in entry_ids:
                problems.append('%s: links to entry:%s, but entries/%s.xml does not exist' % (f, target, target))

checked = sum(len(v) for v in xml_files.values())
if problems:
    print('check-files: %d problem%s' % (len(problems), '' if len(problems) == 1 else 's'))
    for p in problems:
        print('  ' + p)
    sys.exit(1)
print('check-files: ok (%d XML files, %d clauses in the catalogue)' % (checked, len(catalogue)))
