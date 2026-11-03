"""Liebermann's edited Latin texts and their manuscripts (Nov 2026).

"Lat" was not Liebermann's siglum: it was this database's placeholder for a Latin text that Liebermann prints
as one edited text from several manuscripts. On each such text's own clause pages it becomes the text's own
siglum (Hn, Quadr, Duel …), described as Liebermann's edited text, followed by every manuscript he names for it,
each listed by name (type="source"). Elsewhere, Q and Cons. Cn. get the list of their manuscripts in a
<note type="sigla">, as Inst. Cn. already has. Each list is taken from the note named in SPEC (Liebermann's
first note on the text); where he gives no list, from the manuscripts his notes cite ("cited").
A siglum written "Gl=Glas" is shown as Gl but linked to the entry Glas (Gl means another manuscript elsewhere).
"""
import glob, json, re
ms = {}
for r in json.load(open('data/manuscripts.json', encoding='utf-8')):
    ms.setdefault(r['Anchor'], r)
by_sig = {}
for r in json.load(open('data/manuscripts.json', encoding='utf-8')):
    by_sig[re.sub(r'[\s.]', '', r['Gesetze Text'])] = r       # last wins, as on the site
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;')
QUADR = 'Lond; K; Co; Or; Dm; T; R; M; Hk; Br'
# prefix: (abbr, title, sigla, note id giving the list or 'cited')
SPEC = {
 'Hn':             ('Hn', 'Leges Henrici primi', 'Sc; Hg; Lond; K; Co; Or; Sl; Tw; Gi; Rs', 'Hn_Inscr.lnote.oe.a'),
 'QuadrDed':       ('Quadr Ded', 'Quadripartitus, Dedication', 'Dm; M; Jl', 'QuadrDed_1.lnote.oe.c'),
 'QuadrArg':       ('Quadr Arg', 'Quadripartitus, Argumentum', 'Dm; T; Hk; Co', 'QuadrArg_Inscr.lnote.oe.6'),
 'Quadr-I':        ('Quadr', 'Quadripartitus, Book I', QUADR, 'QuadrDed_Inscr.lnote.oe.a'),
 'Quadr-Rb':       ('Quadr', 'Quadripartitus, rubrics', QUADR, 'QuadrDed_Inscr.lnote.oe.a'),
 'Quadr-II-Praef': ('Quadr', 'Quadripartitus, Preface to Book II', 'T; Ip Ml; Cs; Ht; He', 'Quadr-II-Praef_Inscr.lnote.la.4'),
 'QuadrII':        ('Quadr', 'Quadripartitus, Book II', 'T; M; Hk; Br', 'cited'),
 'ConsCn':         ('Cons Cn', 'Consiliatio Cnuti', 'Hr; Cb; Hk', 'ConsCn_Inscr.lnote.oe.a'),
 'LibLond':        ('Lib Lond', 'Libertas Londoniensis', 'Ai; Pl; S; Ord; Horn; Alb=AlbLond; Co', 'LibLond_1.lnote.oe.a'),
 'CHnCor':         ('CHn cor', 'Coronation charter of Henry I', 'H; Rl; Haug; Dm; Q; Sc; Hg; Alb; Gl=Glas; Lond; Hl; Cust; S', 'CHnCor_Prol.lnote.oe.d'),
 'WlEp':           ('Wl ep', 'William I’s writ on the bishops’ courts', 'Lp; Lc; Ry=RyWlEp; Insp; Gra', 'WlEp_Prol.lnote.oe.1'),
 'Prom-Reg':       ('Sacr cor', 'Latin form of the coronation oath (the liturgical ordo)', 'P; El; Os; K; Ch', 'cited'),
 'Duel':           ('Duel', 'Blessing for a judicial duel', 'Tr; Mg; Hm; Ym; Sr; Ta; Gl; Et', 'Duel_Inscr.lnote.oe.a'),
 'ExcomII':        ('Excom II', 'Excommunicatio II', 'Cn; Et; Mm', 'ExcomII_Inscr.lnote.oe.b'),
 'IudDeiI':        ('Iud Dei I', 'Iudicium Dei I', 'Ps; Pt; Rj; Ch; Vt; Ci; Ca; H; Co', 'IudDeiI_Inscr.lnote.oe.b'),
 'IudDeiII':       ('Iud Dei II', 'Iudicium Dei II', 'Ps; Pt; Rj; Ch; Vt; Ci; Ca; H', 'IudDeiI_Inscr.lnote.oe.b'),
 'IudDeiIII':      ('Iud Dei III', 'Iudicium Dei III', 'Ps; Pt; Rj; Ch; Vt; Ci; Ca; H', 'IudDeiI_Inscr.lnote.oe.b'),
 'IudDeiVII':      ('Iud Dei VII', 'Iudicium Dei VII (Latin)', 'Ci; Vt', 'IudDeiVII_Inscr.lnote.oe.a'),
 'IudDeiIX':       ('Iud Dei IX', 'Iudicium Dei IX', 'Rj; Ch; Vt', 'IudDeiI_Inscr.lnote.oe.b'),
 'IudDeiX':        ('Iud Dei X', 'Iudicium Dei X', 'Al; Ma; Bc', 'IudDeiX_Inscr.lnote.oe.a'),
 'IudDeiXI':       ('Iud Dei XI', 'Iudicium Dei XI', 'Ll; Tb; Vt 2; Tr; Mg', 'IudDeiXI_Inscr.lnote.oe.a'),
 'IudDeiXII':      ('Iud Dei XII', 'Iudicium Dei XII', 'Ll; Tb; Vt 2; Tr; Mg', 'IudDeiXII_Inscr.lnote.oe.a'),
 'IudDeiXIII':     ('Iud Dei XIII', 'Iudicium Dei XIII', 'Vt 2; Tr; Mg', 'IudDeiXIII_Inscr.lnote.oe.a'),
 'IudDeiXIV':      ('Iud Dei XIV', 'Iudicium Dei XIV', 'Vt 2; Tr; Mg; Ma', 'IudDeiXIV_1.lnote.oe.a'),
 'HnLond':         ('Hn Lond', 'Henry I’s charter for London', 'Lond; K; Co; Or; Gi; Tw; Sl; Cc; Horn; Cus; Cust; El=ElLond; E IV; Po', 'HnLond_Prol.lnote.oe.a'),
 'InCn':           ('In Cn', 'Instituta Cnuti', 'H; Rl; T; Cb; Di; Lb; S; Pl; Ct', 'Af_15.lnote.incn.star'),
}
def where(note_id):
    if note_id == 'cited': return 'the manuscripts his notes cite'
    f = 'oe-laws/' + note_id.split('.')[0] + '.xml'
    x = open(f, encoding='utf-8').read()
    m = re.search(r'xml:id="' + re.escape(note_id) + r'"[^>]*n="([^"]*)".*?<bibl>(.*?)</bibl>', x, re.S)
    assert m, note_id
    vol = re.search(r'unit="volume">([^<]*)', m.group(2)).group(1); pg = re.search(r'unit="page">([^<]*)', m.group(2)).group(1)
    return f'the manuscripts he names in Gesetze {"I" * int(vol) if vol.isdigit() else vol}, p. {pg}, note {m.group(1)}'
def entry(tok):
    t, _, anc = tok.partition('=')
    r = ms.get(anc) if anc else by_sig.get(re.sub(r'[\s.]', '', t))
    return t, anc, r
def wit(tok, ind):
    t, anc, r = entry(tok)
    if t == 'Q':
        return f'<witness xml:id="wit-q" type="source"><abbr>Q</abbr> <note type="manuscript">Quadripartitus (Latin translation, c. 1114), as edited by Liebermann</note></witness>'
    assert r, tok
    wid = 'wit-' + re.sub(r'[^a-z0-9]', '', t.lower())
    n = f' n="{anc}"' if anc else ''
    return f'<witness xml:id="{wid}" type="source"{n}><abbr>{t}</abbr> <note type="manuscript">{esc(r["English Translation"])}</note></witness>'
SIGLA_Q = '<note type="sigla">' + QUADR + '</note>'
SIGLA_CONS = '<note type="sigla">Hr; Cb; Hk</note>'
counts = {}
for f in sorted(glob.glob('oe-laws/*.xml')):
    x = open(f, encoding='utf-8').read(); y = x
    pre = f.split('/')[1].rsplit('_', 1)[0]
    if pre.startswith('InCn_'): pre = 'InCn'
    spec = SPEC.get(pre) or (SPEC['InCn'] if f.split('/')[1].startswith('InCn_') else None)
    if spec and 'corresp="#wit-lat"' in y:
        abbr, title, sig, src = spec
        m = re.search(r'([ \t]*)<listWit>(.*?)</listWit>', y, re.S)
        ind = m.group(1); old = m.group(2)
        kept = [w for w in re.findall(r'<witness[^>]*>.*?</witness>', old) if 'xml:id="wit-lat"' not in w]
        have = {re.sub(r'<[^>]+>', '', re.search(r'<abbr>(.*?)</abbr>', w).group(1)).strip() for w in kept if '<abbr>' in w}
        lat = re.search(r'<witness xml:id="wit-lat"[^>]*>.*?</witness>', old).group(0)
        if pre == 'Erc':
            new_lat = lat.replace('<witness xml:id="wit-lat"><abbr>Lat</abbr>', '<witness xml:id="wit-lat" type="edited"><abbr>Bede</abbr>')
            srcs = []
        else:
            new_lat = (f'<witness xml:id="wit-lat" type="edited"><abbr>{abbr}</abbr> <note type="manuscript">{title}: Liebermann’s edited '
                       f'Latin text, from {where(src)}, listed below</note></witness>')
            srcs = [wit(t, ind) for t in sig.split('; ') if entry(t)[0] not in have]
        # the In Cn files already list the nine manuscripts (tools/incn/manuscripts.py): mark them as its sources
        kept = [re.sub(r'^<witness xml:id="([^"]+)">', r'<witness xml:id="\1" type="source">', w)
                if re.search(r'<abbr>(' + '|'.join(re.escape(t.split('=')[0]) for t in sig.split('; ')) + r')</abbr>', w) and ' type=' not in w.split('>')[0] else w for w in kept]
        ws = [new_lat] + kept + srcs
        y = y[:m.start()] + ind + '<listWit>\n' + ''.join(ind + '  ' + w + '\n' for w in ws) + ind + '</listWit>' + y[m.end():]
    # Q and Cons. Cn. among another text's manuscripts: their own manuscripts
    y = re.sub(r'(<witness xml:id="wit-q"(?! type="source")[^>]*><abbr>Q[^<]*</abbr> <note type="manuscript">[^<]*</note>)(</witness>)', r'\1 ' + SIGLA_Q + r'\2', y)
    y = re.sub(r'(<witness xml:id="wit-cons-cn"[^>]*><abbr>Cons\. Cn\.</abbr>(?: <note type="manuscript">[^<]*</note>)?)(</witness>)', r'\1 ' + SIGLA_CONS + r'\2', y)
    y = y.replace('<note type="sigla">H Rl T Cb Di Lb S Pl Ct</note>', '<note type="sigla">H; Rl; T; Cb; Di; Lb; S; Pl; Ct</note>')
    if y != x:
        open(f, 'w', encoding='utf-8').write(y); counts[pre] = counts.get(pre, 0) + 1
print(json.dumps(counts))

# Second pass: files that list "Lat" without any text from it (where Liebermann prints the separate copies,
# e.g. CHn cor Prol.): the placeholder goes, and the text's manuscripts are listed as on its other pages.
n2 = 0
for f in sorted(glob.glob('oe-laws/*.xml')):
    y = open(f, encoding='utf-8').read()
    m0 = re.search(r'<witness xml:id="wit-lat"><abbr>Lat</abbr>[^\n]*?</witness>', y)
    if not m0: continue
    pre = f.split('/')[1].rsplit('_', 1)[0]
    if pre == 'Erc':
        y = y.replace('<witness xml:id="wit-lat"><abbr>Lat</abbr>', '<witness xml:id="wit-lat" type="edited"><abbr>Bede</abbr>')
    else:
        abbr, title, sig, src = SPEC[pre]
        m = re.search(r'([ \t]*)<listWit>(.*?)</listWit>', y, re.S)
        ind = m.group(1)
        kept = [w for w in re.findall(r'<witness[^>]*>.*?</witness>', m.group(2)) if 'xml:id="wit-lat"' not in w]
        have = {re.sub(r'<[^>]+>', '', re.search(r'<abbr>(.*?)</abbr>', w).group(1)).strip() for w in kept if '<abbr>' in w}
        ws = kept + [wit(t, ind) for t in sig.split('; ') if entry(t)[0] not in have]
        y = y[:m.start()] + ind + '<listWit>\n' + ''.join(ind + '  ' + w + '\n' for w in ws) + ind + '</listWit>' + y[m.end():]
    open(f, 'w', encoding='utf-8').write(y); n2 += 1
print('unused Lat replaced in', n2, 'files')
# In Cn Inscr.: its nine manuscripts are sources too
f = 'oe-laws/InCn_Inscr.xml'; y = open(f, encoding='utf-8').read()
for t in 'h rl t cb di lb s pl ct'.split():
    y = y.replace(f'<witness xml:id="wit-{t}">', f'<witness xml:id="wit-{t}" type="source">')
open(f, 'w', encoding='utf-8').write(y)
