"""Nor Grið on one page (Nov. 2026, Anya Adair): the nine one-line files NorGrith_Line-1, NorGrith_2 … _9 are
joined into oe-laws/NorGrith_Lines-1-9.xml. Liebermann's text keeps its manuscript lines (<seg type="line">)
and his bracketed clause numbers of the older editions (<milestone unit="clause">); Rabin's text and translation
are divided into his clauses 1–4 (<seg type="part">). Liebermann's footnotes of Gesetze I p. 473 are
transcribed afresh from the page (the line files had notes from other texts). The old ids stay in
oe-laws/index.json as "parts" with a "line", so links to them open this page with that line highlighted.
Run once (Nov. 2026; the line files it reads are gone, and the joined file has since been edited by hand).
"""
import json, os, re
L = 'oe-laws/'
head = open(L + 'NorGrith_Line-1.xml', encoding='utf-8').read()
src = {i: open(L + f'NorGrith_{i}.xml', encoding='utf-8').read() for i in ['Line-1', '2', '3', '4', '5', '6', '7', '8', '9']}
def notes(i, *ids):
    out = []
    for nid in ids:
        m = re.search(r'\s*<note type="liebermannNote"[^>]*xml:id="%s"[^>]*>.*?</note>' % re.escape(nid), src[i], re.S)
        out.append(m.group(0).strip())
    return out
I = lambda t: '<hi rend="italic">' + t + '</hi>'
SP = lambda t: '<hi rend="italic spaced">' + t + '</hi>'
def ln(nid, n, de, en, sub='textual'):
    return (f'<note type="liebermannNote" subtype="{sub}" xml:id="{nid}" n="{n}" source="#liebermann"><bibl><biblScope unit="volume">1</biblScope>'
            f'<biblScope unit="page">473</biblScope></bibl><seg type="original" xml:lang="de">{de}</seg><seg type="translation" xml:lang="en" source="#claude">{en}</seg></note>')
P = lambda n, t='oe': f'<ptr type="liebermannNote" n="{n}" target="#NorGrith_Lines-1-9.lnote.{t}.{n}"/>'
M = lambda n: f'<milestone unit="clause" n="{n}"/>'
lines = [
    M(1) + ' ⁊' + P('b') + ' on Norðhymbra lage is s<hi rend="italic">anctu</hi>s Petrus',
    '[cyric]frið' + P('1') + ' ⁊ s<hi rend="italic">anctu</hi>s Wilfriðus ⁊ s<hi rend="italic">anctu</hi>s',
    '[Iohann]es binnan cyricwagum þreo',
    '[hundr]ed æt cwicum men' + P('2') + ', ⁊ æt deadu<hi rend="italic">m</hi>',
    '[botlea]s' + P('3') + '. ' + M(2) + ' ⁊ oðera stowa grið is læsse',
    '[mæ]r[þ]e' + P('4') + ' áá' + P('5') + ' be stowe mæþe. ' + M(3) + ' [⁊]',
    '[<hi rend="italic">?</hi>preost]e cyricgangas syndan forbodene' + P('c'),
    'wifum ⁊ wæpnu<hi rend="italic">m</hi>. ' + M(4) + ' ⁊ cyricgrið dyre' + P('6') + P('d'),
    'æghwar be mæðe ofer ealle ðam rice.',
]
oe = ('<ab type="liebermannText" xml:lang="ang" source="#liebermann" n="Lines 1–9" corresp="#wit-g"><pb n="473" ed="#liebermann"/>' + P('a')
      + ' '.join(f'<seg type="line" n="{k}">{t}</seg>' for k, t in enumerate(lines, 1)) + '</ab>')
D = lambda n, t='de1': f'<ptr type="liebermannNote" n="{n}" target="#NorGrith_Line-1.lnote.{t}.{n}"/>'
de = ('<ab type="translation" xml:lang="de" source="#liebermann"><pb n="473" ed="#liebermann"/>' + M(1) + '<ptr type="liebermannNote" n="1" target="#NorGrith_Line-1.lnote.de.1"/> '
      'Und im Northumbrer-Recht beträgt [Busse für Verletzung von] Kirchenfrieden des H. Petrus' + D('a') + ' und des H. Wilfrid' + D('b')
      + ' und<ptr type="liebermannNote" n="2" target="#NorGrith_Line-1.lnote.de.2"/> des H. Johann' + D('c') + ' innerhalb der Kirchenmauern' + D('d')
      + ' 3<ptr type="liebermannNote" n="3" target="#NorGrith_Line-1.lnote.de.3"/> ‘Hundert’' + D('e') + ' beim lebend [gebliebenen verletzten] Menschen, und bei getödtetem [ist die That durch Geld] unabbüssbar' + D('f') + '. '
      + M(2) + '<ptr type="liebermannNote" n="0" target="#NorGrith_2.lnote.de.0"/> Und der Friedensschutz anderer [Kirchen]orte ist von geringerer Ehrenhöhe immer gemäss dem Range des Ortes. '
      + M(3) + ' Und einem Priester [?] sind Kirchgänge verboten [mit<ptr type="liebermannNote" n="1" target="#NorGrith_6.lnote.de.1"/>] Weibern und Waffen. '
      + M(4) + ' Und Kirchen-Friedenschutz schätze [man] hoch überall nach dem Range [der Kirche] über das ganze Reich hin.</ab>')
en = ('<ab type="translation" xml:lang="en" source="#claude" ana="#fromGerman">' + M(1) + ' And in Northumbrian law [the compensation for breach of] the church-peace of St Peter and of St Wilfrid and of St John within the church walls is 3 ‘hundreds’ for a person [injured but] still living, and for one killed [the deed is] beyond compensation [by money]. '
      + M(2) + ' And the peace-protection of other [church] places is of lesser dignity, always according to the rank of the place. '
      + M(3) + ' And for a priest [?] church-goings [with] women and weapons are forbidden. '
      + M(4) + ' And let [one] value church peace-protection highly everywhere, according to the rank [of the church], throughout the whole kingdom.</ab>')
R = lambda n, t: f'<seg type="part" n="{n}">{t}</seg>'
rab = ('<ab type="editionText" xml:lang="ang" source="#rabin-doml" n="1–4" corresp="#wit-g"><pb n="32" ed="#rabin-doml"/>'
       + R(1, 'And on Norðhymbra lage is sanctus Petrus cyricfrið and sanctus Wilfriðus and sanctus Iohannes binnan cyricwagum þreo hundred æt cwicum men, and æt deadum botleas.') + ' '
       + R(2, 'And oðera stowa grið is læsse mærþe, aa be stowe mæþe.') + ' '
       + R(3, 'And preoste cyricgangas syndan forbodene wifum and wæpnum.') + ' '
       + R(4, 'And cyricgrið dyre æghwar be mæðe ofer ealle ðam rice.') + '</ab>')
rabt = ('<ab type="translation" xml:lang="en" source="#rabin-doml" corresp="#wit-g"><pb n="33" ed="#rabin-doml"/>'
        + R(1, 'And according to the law of the Northumbrians, the compensation owed for a violation of Church sanctuary at Saint Peter’s, Saint Wilfrid’s, and within the walls of Saint John’s is three hundred if the victim is alive, but it cannot be compensated for if he is dead.') + ' '
        + R(2, 'And the sanctuary protection of other locations is less in scale, always according to the status of the site.') + ' '
        + R(3, 'And a priest is forbidden from attending church with women or weapons.') + ' '
        + R(4, 'And Church sanctuary is to be respected everywhere according to its degree over the entire kingdom.') + '</ab>')
# Rabin's notes, each once, in order
rn, seen = [], set()
for i in src:
    for m in re.finditer(r'<note type="(textual|translator)" source="#rabin-doml">(.*?)</note>', src[i]):
        t = m.group(2)
        if t in seen or 'covers the rows' in t or ('Saint Peter’s' in t and 'compensated' in t and 'Beverly. Saint' in t): continue
        seen.add(t); rn.append(m.group(0))
O = lambda n, de_, en_: ln(f'NorGrith_Lines-1-9.lnote.oe.{n}', n, de_, en_)
oenotes = [
    O('a', I('Hs. Nero A I f.') + ' 96' + I('v., hinter') + ' VIII Atr. 5, 2, ' + I('o. S.') + ' 264<hi rend="superscript">5</hi>, ' + I('Hand um') + ' 1070. '
        + I('Rasuren, Abnützung und Chemikalien machen den Text theilweise unlesbar. Ich sah einst, als E. M.') + ' ' + SP('Thompson') + ' '
        + I('Hydrosulphur freundlich anwendete, mehr als') + ' 1901; ' + I('was mir April') + ' 1902 ' + I('G. F.') + ' ' + SP('Warner') + ' ' + I('gütig mittheilte, notire ich dankend.'),
        'MS Nero A I f. 96v, after VIII Atr. 5,2, above p. 264 n. 5, hand of c. 1070. Erasures, wear and chemicals make the text partly illegible. When E. M. Thompson kindly applied hydrosulphur, I once saw more than in 1901; what G. F. Warner kindly told me in April 1902 I record with thanks.'),
    O('b', I('Die Hs. lautet Südenglisch und bringt das Stück, laut des Beginnes mit') + ' and, ' + I('als Fortsetzung zu') + ' cyricgriðe on Engla lage ('
        + I('VIII Atr. Inscr.') + '; 5, 2); ' + I('der Text entstand also nicht vor') + ' 1014, ' + I('bewahrt aber Formen noch des frühen XI. Jhs. Der Inhalt kann hinaufdatiren bis c.') + ' 933 ('
        + I('das XI. Jh. knüpfte nämlich die Kathedralprivilegien Ripons und Beverleys an Æthelstan’s Schottenzug); allein den Stil beeinflussen Æthelred’s II. Gesetze. Diesen das Stück mit Hs.') + ' G '
        + I('als Schluss von') + ' VIII Atr. ' + I('zuzuweisen, verbietet die andere Hs. von') + ' VIII Atr. (' + I('o. S.') + ' 264 ' + I('Sp.') + ' 1), '
        + I('und wohl auch die Ähnlichkeit der') + ' §§ 2. 4 ' + I('mit') + ' VIII Atr. 1. 4, 1. 5, 2',
        'The MS reads in Southern English and gives the piece, since it begins with <hi rend="italic">and</hi>, as a continuation of <hi rend="italic">cyricgriðe on Engla lage</hi> (VIII Atr. Inscr.; 5,2); so the text did not originate before 1014, but still keeps forms of the early 11th century. The content may date back to c. 933 (for the 11th century linked the cathedral privileges of Ripon and Beverley to Æthelstan’s Scottish campaign); but the style is influenced by Æthelred II’s laws. Assigning the piece, as MS G does, to VIII Atr. as its end is ruled out by the other MS of VIII Atr. (above p. 264 col. 1), and probably also by the likeness of §§ 2, 4 to VIII Atr. 1, 4, 1, 5, 2'),
    O('c', I('ergänze') + ' mid', 'supply <hi rend="italic">mid</hi>'),
    O('d', I('ergänze') + ' man', 'supply <hi rend="italic">man</hi>'),
    O('1', '[' + I('Eingeklammertes') + '] ' + I('von mir ergänzt'), '[What is in square brackets] supplied by me'),
    O('2', 'm ' + I('erkennt nicht') + ' <hi rend="italic smallcaps">Warner</hi>', 'Warner does not make out the m'),
    O('3', 'l ' + I('erkennt') + ' <hi rend="italic smallcaps">War.</hi>', 'Warner makes out the l'),
    O('4', 'e ' + I('nicht zu erkennen; Buchstabe') + ' 3 ' + I('oder') + ' 2 ' + I('eher') + ' t? ' + I('W.'), 'e cannot be made out; letter 3 or 2 rather t? W[arner]'),
    O('5', I('unlesbar W.'), 'illegible W[arner]'),
    O('6', I('nur') + ' d, ' + I('dahinter eher') + ' e ' + I('erkennt W. Vielleicht') + ' deore', 'Warner makes out only d, and after it rather e. Perhaps <hi rend="italic">deore</hi>'),
]
# Liebermann's footnotes to his German (vol. I) and his Erklärungen (vol. III)
denotes = notes('Line-1', 'NorGrith_Line-1.lnote.de.1')
fix = {'a': ('des Doms zu York, bezw. Ripon und Beverley', 'of the minster at York, or of Ripon and of Beverley respectively'),
       'b': ('† 709', 'died 709'), 'c': ('† 721', 'died 721')}
for k in 'abc':
    denotes.append(ln(f'NorGrith_Line-1.lnote.de1.{k}', k, *fix[k], sub='translationFootnote'))
denotes += notes('Line-1', 'NorGrith_Line-1.lnote.de.2', 'NorGrith_Line-1.lnote.de1.d', 'NorGrith_Line-1.lnote.de.3', 'NorGrith_Line-1.lnote.de1.e', 'NorGrith_Line-1.lnote.de1.f')
denotes += notes('2', 'NorGrith_2.lnote.de.0') + notes('6', 'NorGrith_6.lnote.de.1')
editorial = ('<note type="editorial">Liebermann prints this short text line by line as it stands in its only manuscript, G (Cotton Nero A.i, f. 96v, in a hand of about 1070), '
             'and numbers the lines 1–9 (“Zeile”); the dictionary cites it by these lines (“Nor grið Z. 6”). Within the lines he gives, in square brackets, the clause numbers [1]–[4] of the earlier editions; '
             'his German translation follows those clauses. Here the whole text is on one page: the manuscript lines are numbered in the margin, and the old clause numbers stand in the text as small grey numbers. '
             'A link to one line opens the page with that line highlighted. Rabin’s text and translation are divided into his clauses 1–4, which are the same as the old clauses. '
             'Square brackets in the Old English are Liebermann’s supplements (his note 1); most of his readings of the damaged letters come from G. F. Warner (1902).</note>')
body = ('      <div type="clause" n="Lines 1–9">\n        <head><ref type="lawCode" target="law:NorGrith">Nor Grið</ref> Lines 1–9</head>\n'
        + '\n'.join('        ' + x for x in [oe, rab, de, en, rabt,
            '<note type="comparison" source="#liebermann" n="473"><ref target="clause:VIIIAtr_1-1">VIII Atr 1.1</ref>; <ref target="clause:VIIIAtr_4">VIII Atr 4</ref>; <ref target="clause:VIIIAtr_4-1">VIII Atr 4.1</ref></note>',
            '<note type="comparisonPrinted" source="#liebermann">VIII Atr. 1, 1. 4. 4, 1</note>',
            editorial] + rn + oenotes + denotes)
        + '\n      </div>')
s = re.sub(r'      <div type="clause".*?      </div>', lambda m: body, head, flags=re.S)
s = s.replace('NorGrith_Line-1"', 'NorGrith_Lines-1-9"', 1)  # TEI xml:id
s = s.replace('<title>Nor Grið Line 1</title>', '<title>Nor Grið Lines 1–9</title>')
s = s.replace('<idno type="slug">NorGrith_Line-1</idno>', '<idno type="slug">NorGrith_Lines-1-9</idno>')
s = s.replace('<idno type="citation">Nor Grið Line 1</idno>', '<idno type="citation">Nor Grið Lines 1–9</idno>')
s = s.replace('<idno type="clause">Line 1</idno>', '<idno type="clause">Lines 1–9</idno>')
s = s.replace('<idno type="citationKey">NorGrith line1</idno>', ''.join(f'<idno type="citationKey">NorGrith {k}</idno>' for k in ['line%d' % i for i in range(1, 10)]))
s = re.sub(r'<witness xml:id="wit-g-b"><abbr>G\(B\)</abbr> <note type="manuscript">[^<]*</note></witness>',
           '<witness xml:id="wit-g" rend="bold"><abbr>G</abbr> <note type="manuscript">London, British Library, Cotton Nero A.i, f. 96v, in the second of the two MSS bound together in the volume (Part B, ff. 70–177, the Wulfstan collection), after VIII Atr; a hand of about 1070 (Liebermann)</note></witness>', s)
s = s.replace('</revisionDesc>', '  <change when="2026-11-06">The nine one-line pages (NorGrith_Line-1, NorGrith_2 … 9) joined into this one page, with Liebermann’s manuscript lines and bracketed clause numbers marked and Rabin’s text and translation by his clauses 1–4. Liebermann’s footnotes of Gesetze I p. 473 transcribed afresh from the page: the line files had notes belonging to other texts (Iudex and others) (Anya Adair).</change>\n    </revisionDesc>')
open(L + 'NorGrith_Lines-1-9.xml', 'w', encoding='utf-8').write(s)
for i in src: os.remove(L + f'NorGrith_{i}.xml')
# the catalogue: one row, with the old line ids as its parts
rows = open(L + 'index.json', encoding='utf-8').read().split('\n')
keep, first = [], None
for r in rows:
    if '"anchor":"NorGrith"' in r:
        d = json.loads(r.rstrip(','))
        if first is None:
            first = len(keep); base = d
            keep.append(None)
        continue
    keep.append(r)
row = {k: base[k] for k in base}
row.update(id='NorGrith_Lines-1-9', file='NorGrith_Lines-1-9.xml', citation='Nor Grið Lines 1–9', clause='Lines 1–9',
           citationKeys=['NorGrith line%d' % i for i in range(1, 10)] + ['NorGrith %d' % i for i in range(1, 10)],
           parts=[{'id': 'NorGrith_Line-1' if i == 1 else f'NorGrith_{i}', 'clause': f'Line {i}', 'line': str(i)} for i in range(1, 10)])
keep[first] = json.dumps(row, ensure_ascii=False, separators=(',', ':')) + ','
open(L + 'index.json', 'w', encoding='utf-8').write('\n'.join(keep))
print('written')
