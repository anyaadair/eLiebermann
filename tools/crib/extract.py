#!/usr/bin/env python3
"""Extract the texts of clauses with no translation, in reading order, for an LLM crib (see tools/crib/BRIEF.md).

    OUT=/some/folder python3 tools/crib/extract.py "Excom I,Excom II" batch.json

Writes [{key: ClauseId#k, citation, lang, ms, text}] (k counts the clause's texts from 0, as tools/add-crib.py does)."""
import json,re,sys,html
import os
C=os.environ.get('OUT', '.') + '/'
order=[]
idx=json.load(open('oe-laws/index.json'))
codes=sys.argv[1].split(',')
out=[]
for c in idx:
    if c['code'] not in codes: continue
    s=open('oe-laws/'+c['file'],encoding='utf8').read()
    if '<ab type="translation"' in s: continue
    sig={m.group(1):re.sub('<[^>]+>','',m.group(2)) for m in re.finditer(r'<witness xml:id="([^"]+)"[^>]*>\s*<abbr>(.*?)</abbr>',s,re.S)}
    k=0
    for m in re.finditer(r'<ab type="(liebermannText|editionText)"([^>]*)>(.*?)</ab>',s,re.S):
        body=re.sub(r'<note\b.*?</note>','',m.group(3),flags=re.S)
        body=re.sub(r'<(ptr|pb|lb)\b[^>]*/>','',body)
        body=html.unescape(re.sub(r'<[^>]+>','',body))
        body=' '.join(body.split())
        lang=re.search(r'xml:lang="([^"]+)"',m.group(2)); cor=re.search(r'corresp="#([^"]+)"',m.group(2))
        out.append({'key':f"{c['id']}#{k}",'citation':c['citation'],'lang':lang.group(1) if lang else '','ms':sig.get(cor.group(1),'') if cor else '','text':body})
        k+=1
json.dump(out,open(C+sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(out),sum(len(o['text'].split()) for o in out))
