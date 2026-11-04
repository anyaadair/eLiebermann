"""Nov 2026: Liebermann's K sigla, one entry per manuscript, as in Gesetze I, p. xxxii:
  "K (oder K1) sammt Kb"  = Cotton Claudius A.iii   -> file K1 (also K, Kb)
  "K2, K3 (oder K)"       = Cotton Claudius D.ii     -> file K2 (also K3; Liebermann's K in the London texts)
The old entries K, K3 and Kb are merged into these (their content was the same) and removed.
A file's "also" lists the other sigla that link to it; "also_anchors" keeps old links (#K, #Kb, #K3) working.
In the clause files, a bare K is tied to the right manuscript by the code it is in."""
import json, os, glob, re
D = 'data/manuscripts'
k1 = json.load(open(f'{D}/K1.json', encoding='utf-8')); k2 = json.load(open(f'{D}/K2.json', encoding='utf-8'))
k1['display_label'] = 'K1 (or K), with Kb'; k1['also'] = ['K', 'Kb']; k1['also_anchors'] = ['K', 'Kb']
k2['display_label'] = 'K2, K3 (or K)'; k2['also'] = ['K3']; k2['also_anchors'] = ['K3']
k1['display_fields']['shelfmark'] = 'London, British Library, Cotton MS Claudius A.iii'
k2['display_fields']['shelfmark'] = 'London, British Library, Cotton MS Claudius D.ii (once part of the London Guildhall’s Liber Custumarum)'
k1['display_fields']['laws'] = 'VI Atr, VI Atr Lat, Sacr cor'
k1['display_fields']['notes'].insert(0, {'by': 'Editor', 'text': 'Liebermann’s sigla (Gesetze I, p. xxxii): K1, which he usually calls simply K, for this MS (VI Æthelred, in Old English and Latin, and the coronation oath); Kb for ff. 17–27v, a later part of the same MS with a second text of the coronation oath. In the London texts (Quadripartitus, Leges Henrici, Henry I’s London charter) Liebermann’s K is a different MS, Cotton Claudius D.ii (K2, the next entry).'})
k2['display_fields']['notes'].insert(0, {'by': 'Editor', 'text': 'Liebermann’s sigla (Gesetze I, p. xxxii): K2 for this MS, which in the London texts (Quadripartitus, Leges Henrici, Henry I’s London charter) he calls simply K; K3 for f. 41, a fifteenth-century addition copying Sc. Not to be confused with Cotton Claudius A.iii (K1, the previous entry), which Liebermann also calls K, for VI Æthelred and the coronation oath.'})
for d in (k1, k2): json.dump(d, open(f'{D}/{d["id"]}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for old in ('K', 'K3', 'Kb'):
    p = f'{D}/{old}.json'
    if os.path.exists(p): os.remove(p)
# clause files: which K is meant
A3 = 'London, British Library, Cotton MS Claudius A.iii (Liebermann’s K, also K1)'
D2 = 'London, British Library, Cotton MS Claudius D.ii (Liebermann’s K, also K2)'
n = 0
for f in glob.glob('oe-laws/*.xml'):
    x = open(f, encoding='utf-8').read()
    code = os.path.basename(f).rsplit('_', 1)[0]
    to = ('K1', A3) if code in ('VIAtr', 'VI-Atr-Latin-Paraphrase', 'Prom-Reg') else ('K2', D2) if code in ('Hn', 'HnLond', 'Quadr-I', 'Quadr-Rb') else None
    if not to: continue
    y = re.sub(r'<witness xml:id="wit-k"([^>]*)><abbr>K</abbr> <note type="manuscript">[^<]*</note></witness>',
               lambda m: f'<witness xml:id="wit-k"{re.sub(r" n=\"[^\"]*\"", "", m.group(1))} n="{to[0]}"><abbr>K</abbr> <note type="manuscript">{to[1]}</note></witness>', x)
    if y != x: open(f, 'w', encoding='utf-8').write(y); n += 1
print(n, 'clause files')
