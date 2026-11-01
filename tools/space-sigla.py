#!/usr/bin/env python3
"""Space manuscript sigla that Liebermann prints run together in his notes ("MHkBr" -> "M Hk Br").

Only the notes (type="liebermannNote") are touched, never the texts. Sigla come from
data/manuscripts.json; forms that only look like run-together sigla (MS, EHR, Roman
numerals, OHG...) are listed in SKIP. Run with --apply to write; without it, it reports. Done once, November 2026."""
import re,glob,json,sys
S=sorted({r['Gesetze Text'] for r in json.load(open('data/manuscripts.json')) if re.fullmatch(r'[A-Z][a-z]?\d?',r['Gesetze Text'])},key=len,reverse=True)
alt='|'.join(map(re.escape,S))
SKIP=set('MS MSS BT EHR HEL MAT RG DRA MA DRG DB SS SB GDR HECK THORPE RL KELHAM BARTSCH FOERSTER RQ RA TO HIS AA IVa QC EF AC AIC AB BC DG AG GG OHG ME MLG MHG LG'.split())
pat=re.compile(r'(?<![\w&])((?:%s){2,})(?![\w;])'%alt)
def split(k): return ' '.join(re.findall(alt,k))
apply='--apply' in sys.argv
seen={};files=0
CH='      <change when="2026-11-01">Manuscript sigla that Liebermann prints run together in his notes (“MHkBr”, “HB”) spaced for reading (“M Hk Br”, “H B”).</change>\n'
for f in sorted(glob.glob('oe-laws/*.xml')):
    t=open(f,encoding='utf-8').read(); changed=False
    def fixseg(m):
        global changed
        seg=m.group(0)
        parts=re.split(r'(<[^>]+>)',seg)
        for i,p in enumerate(parts):
            if p.startswith('<'): continue
            def r(mm):
                k=mm.group(1)
                if k in SKIP or (k=='TR' and 'IudDei' in f) or re.fullmatch(r'[IVXLCDM]+',k): return k
                seen[k]=seen.get(k,0)+1; return split(k)
            parts[i]=pat.sub(r,p)
        return ''.join(parts)
    # only Liebermann's notes, both German original and English translation segs
    new=re.sub(r'<note type="liebermannNote"[\s\S]*?</note>',fixseg,t)
    if new!=t:
        files+=1
        if apply:
            if CH.strip() not in new:
                i=new.rfind('</change>'); j=new.index('\n',i)+1; new=new[:j]+CH+new[j:]
            open(f,'w',encoding='utf-8').write(new)
for k,v in sorted(seen.items(),key=lambda x:-x[1]): print(k,'->',split(k),v)
print(files,'files',sum(seen.values()),'changes')
