"""Add lq (Liebermann's lost common exemplar of Ld and the Quadripartitus) to the manuscripts of every
clause whose Liebermann notes or German translation cite it; and his vol. I footnote defining it (I As Prol.)."""
import re, glob
pat = re.compile(r'(?<![^\W\d_])lq(?![^\W\d_])')
WIT = ('<witness xml:id="wit-lq"><abbr>lq</abbr> <note type="manuscript">Lost manuscript: the common source of Ld and the '
       'Quadripartitus, reconstructed by Liebermann from what the two share</note></witness>')
n = 0
for f in sorted(glob.glob('oe-laws/*.xml')):
    x = open(f, encoding='utf-8').read()
    if 'wit-lq' in x: continue
    body = re.sub(r'<revisionDesc>.*?</revisionDesc>', '', x, flags=re.S)
    parts = re.findall(r'<note type="liebermannNote".*?</note>', body, re.S) + re.findall(r'<ab type="translation" xml:lang="de".*?</ab>', body, re.S)
    if not any(pat.search(re.sub('<[^>]+>', ' ', p)) for p in parts): continue
    i = x.rfind('</witness>')
    assert i > 0, f
    j = i + len('</witness>')
    indent = re.search(r'\n([ \t]*)<witness[^\n]*$', x[:j]).group(1)
    x = x[:j] + '\n' + indent + WIT + x[j:]
    open(f, 'w', encoding='utf-8').write(x); n += 1
print('witness added to', n, 'files')

# I As Prol.: the footnote under the German column of Gesetze I, p. 147, to "lq*" in line 2.
f = 'oe-laws/IAs_Prol.xml'
x = open(f, encoding='utf-8').read()
if 'IAs_Prol.lnote.de1.star' not in x:
    note = ('<note type="liebermannNote" subtype="translationFootnote" xml:id="IAs_Prol.lnote.de1.star" n="*" source="#liebermann">'
            '<bibl><biblScope unit="volume">1</biblScope><biblScope unit="page">147</biblScope></bibl>'
            '<seg type="original" xml:lang="de"><hi rend="italic">Das Ld und Quadr. Gemeinsame nenne ich</hi> lq.</seg>'
            '<seg type="translation" xml:lang="en" source="#claude">What Ld and Quadr. have in common I call lq.</seg></note>')
    old = '<note type="liebermannNote" subtype="erklaerung" xml:id="IAs_Prol.lnote.de.star"'
    assert x.count(old) == 1
    x = x.replace(old, note + '\n        ' + old)
    # the star now opens both notes: the footnote (vol. I) and the explanation (vol. III, "Z. 2*")
    old = 'target="#IAs_Prol.lnote.de.star"'
    assert x.count(old) == 1
    x = x.replace(old, 'target="#IAs_Prol.lnote.de1.star #IAs_Prol.lnote.de.star"')
    open(f, 'w', encoding='utf-8').write(x)
    print('footnote added')
