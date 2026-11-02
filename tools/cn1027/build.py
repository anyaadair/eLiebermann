"""Liebermann's text of Cnut's letter of 1027 (Gesetze I, pp. 276-277), added to the clause files
oe-laws/Cn1027_*.xml: his Latin (from Florence of Worcester, with Ox and Ma), his footnotes with an
English rendering, and his marginal references. Read from the page images twice (November 2026).

Markup in TEXT: {n} = footnote n on the clause's page (p. 276, or p. 277 for clauses 9-17);
{n@277} = footnote n of p. 277 inside clause 8, which runs over the page; {*}, {**}, {***} = the
starred notes at the head; |277| = the page break. Liebermann's superscript letters refer to his
Erklaerungen (Gesetze II/III), not available here, and are left out.
In NOTES, _..._ is italic (Liebermann's German and the sigla)."""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
L = os.path.join(ROOT, 'oe-laws')

TEXT = {
 'Inscr': "{*}{**}Cnuto{1} rex totius Anglię et Denemarcię{2} et{***} Norreganorum{3} et partis Suanorum{4} Æthelnotho{5} metropolitano et Alfrico Eboracensi archiepiscopo{6} omnibusque episcopis et primatibus et toti genti Anglorum tam nobilibus quam plebeiis salutem.",
 '1': "Notifico uobis me nouiter isse Romam, oratum pro redemptione peccaminum meorum et pro salute regnorum quique meo subiacent regimini populorum.",
 '2': "Hanc quidem profectionem Deo iam olim deuoueram, sed pro negotiis regni et causis impedientibus huc usque perficere{7} non poteram.",
 '3': "Nunc autem ipsi Deo meo omnipotenti ualde humiliter gratias ago, quod{8} mihi{6} concessit in uita mea sanctos{9} apostolos suos{6} Petrum et Paulum et omne sanctuarium, quod intra{10} urbem Romam aut extra addiscere potui, expetere et secundum desiderium meum presentialiter uenerari et adorare.",
 '4': "Ob{11} id ergo maxime hoc patraui, quia a sapientibus didici, sanctum Petrum apostolum magnam potestatem a{12} Domino{13} accepisse ligandi atque{14} soluendi clauigerumque esse cęlestis regni, et ideo specialius{15} eius patrocinium apud Deum{16} diligenter{6} expetere ualde utile duxi.",
 '5': "Sit autem uobis notum, quia magna congregatio nobilium in ipsa pascali solennitate{17} ibi cum domino papa Iohanne et imperatore Cuonrado{18} erat, scilicet omnes principes gentium a monte Gargano usque ad istud proximum mare, qui omnes me et honorifice suscepere et donis{19} pretiosis honorauere; maxime autem ab imperatore donis uariis et muneribus pretiosis honoratus sum, tam in uasis aureis et argenteis quam in palliis et uestibus ualde pretiosis.",
 '6': "Locutus sum igitur cum ipso imperatore et domino papa et principibus qui ibi erant de necessitatibus totius populi uniuersi{6} regni{6} mei, tam Anglorum{20} quam Danorum, ut eis concederetur lex equior et pax securior in uia Romam adeundi, et ne tot clausuris per uiam artentur{21} et propter thelon{22} iniustum fatigentur; annuitque postulatis imperator et Rodulfus{23} rex, qui maxime ipsarum clausurarum dominatur; cunctique principes edictis{24} firmauerunt, ut homines mei, tam mercatores quam alii orandi causa{25} uiatores, absque omni angaria clausurarum et theloneariorum{26} firma{27} pace et{28} iusta lege securi Romam eant et redeant.",
 '7': "Conquestus sum iterum coram domino papa et mihi ualde displicere causabar{29}, quod mei archiepiscopi in tantum angariabantur immensitate pecuniarum, quae ab eis expetebatur{30}, dum pro pallio accipiendo secundum{31} morem apostolicam sedem expeterent; decretumque est, ne id deinceps fiat.",
 '8': "Cuncta enim{32} que a domino papa et ab ipso{6} imperatore et a rege Rodulfo{33} ceterisque principibus, per quorum terras nobis transitus est ad Romam, pro mee gentis utilitate postulabam, libentissime{34} |277|annuerunt{1@277} et concessa sacramento{2@277} etiam firmauerunt sub testimonio quattuor archiepiscoporum et uiginti episcoporum et innumere multitudinis ducum et nobilium, qui{3@277} ibi aderant.",
 '9': "Quapropter Deo omnipotenti gratias magnificas reddo, quia omnia que desideraueram, prout mente decreueram, prospere perfeci uotisque meis ad uelle satisfeci.",
 '10': "Nunc itaque notum{4} sit omnibus uobis, quia ipsi Deo omnipotenti{5} supplex deuoui uitam meam amodo in omnibus iustificare et regna mihi subdita populosque iuste et pie regere equumque iudicium per omnia{6} obseruare; et si quid per mee iuuentutis intemperantiam aut neglegentiam hactenus preter id quod iustum erat actum est, totum Deo auxiliante deinceps{5} dispono emendare.",
 '11': "Idcirco{7} obtestor et precipio meis consiliariis, quibus regni consilia credidi, ne ullo modo aut propter meum timorem aut alicuius potentis personę fauorem aliquam iuiustitiam amodo consentiant uel patiantur{8} pullulare in omni regno meo.",
 '12': "Precipio etiam omnibus uicecomitibus et prepositis uniuersi regni mei, sicut meam amicitiam{9} aut suam salutem habere uolunt, ut nulli homini nec diuiti nec pauperi uim iniustam inferant, sed omnibus tam nobilibus quam ignobilibus et{9=10} diuitibus et pauperibus sit fas iusta lege potiundi, a qua nec propter fauorem regium aut{11} alicuius potentis personam nec propter mihi congregandam{12} pecuniam ullo modo deuietur{13}; quia nulla mihi necessitas est, ut iniqua exactione mihi{14} pecunia congregetur.",
 '13': "Ego itaque uobis{15} notum fieri uolo, quod eadem uia qua exiui regrediens, Danemarciam{16} eo, pacem et firmum pactum omnium Danorum consilio cum{17} eis gentibus et populis compositurus, qui nos et regno{18} et uita priuare, si eis possibile{19} esset, uolebant, sed non poterant{20}, Deo scilicet uirtutem eorum destruente, qui nos sua benigna{21} pietate{22} in regno et honore conseruet omniumque inimicorum nostrorum potentiam et{23} fortitudinem deinceps dissipet et adnichilet!",
 '14': "Composita denique pace cum gentibus quę in circuitu nostro sunt, dispositoque et pacato{24} omni regno nostro{25} hic in oriente, ita ut a nulla parte bellum aut inimicitias aliquorum timere habeamus, quam citius hac estate apparatum nauigii procurare{26} potero, Angliam uenire dispono.",
 '15': "Hanc autem epistolam iccirco{27} premisi, ut de mea prosperitate omnis populus regni mei letificetur, quia, ut uos ipsi scitis, nunquam memet ipsum nec meum laborem abstinui nec adhuc abstinebo impendere pro omnis populi mei necessaria utilitate.",
 '16': "Nunc igitur precipio{28} et obtestor omnes meos{29} episcopos et regni prepositos per fidem, quam Deo{30} et mihi debetis, quatinus faciatis, ut, antequam ego{31} Angliam ueniam, omnia{32} debita, quę Deo{31} secundum legem antiquam debemus, sint persoluta, scilicet elemosinę{33} pro aratris et^* decimę animalium ipsius{34} anni procreatorum et^** denarii quos Rome{35} ad Sanctum Petrum debemus{36} siue ex urbibus siue ex uillis et mediante Augusto decimę frugum^* et in festiuitate sancti Martini^† primitię seminum ad ęcclesiam, sub cuius parrochia quisque deget{37}, que Anglice{38} ciricsceatt{39} nominantur.{40}",
 '17': "Hec et his{41} similia si, dum uenero, non erunt{42} persoluta, regia exactio{43} secundum leges, in quem culpa cadit, districte absque uenia comparabit. Ualete.{5}",
}
P277 = {'9', '10', '11', '12', '13', '14', '15', '16', '17'}

N276 = {
 '*': ("_Angelsächsisches Original fehlt._", "_The Old English original is lost._"),
 '**': ("_Aus_ Fl[orentius Wigorn. _ed. Mon. Germ., SS._ XIII 126, _verglichen mit_ Ox (_Hs. Oxford Corpus_ 157, _p._ 329, _freundlichst collationirt von Miss Parker_) _vom Anfang_ 12. _Jhs._] _und_ Ma [Willelmus Malmesbur. II 183, _ed. Stubbs p._ 221].",
        "_From_ Fl[orence of Worcester, _ed. Mon. Germ., SS._ XIII 126, _compared with_ Ox (_MS Oxford, Corpus_ 157, _p._ 329, _most kindly collated by Miss Parker_) _of the beginning of the_ 12_th cent._] _and_ Ma [William of Malmesbury II 183, _ed. Stubbs p._ 221]."),
 '***': ("et N. et p. S. _für_ 1027 _sachlich falsch_ [_vgl. S._ 278 A***; ‘_Prätensionstitel_’ BRESSLAU; _vielleicht nicht original_].",
         "et N. et p. S. _is wrong in fact for_ 1027 [_cf. p._ 278 A***; ‘_title of pretension_’ BRESSLAU; _perhaps not original_]."),
 '1': ("_so_ Ma; Canutus _Fl_ [_original wohl_ Cnut]", "_so_ Ma; Canutus _Fl_ [_the original probably_ Cnut]"),
 '2': ("-rchia _Ma_", None), '3': ("-giae _Ma_", None), '4': ("Swauorum _Ma_", None),
 '5': ("Aiel., Ail., Al. _Ma_, Athel. _Ox_", None),
 '6': ("_fehlt Ma_", "_lacking in Ma_"),
 '7': ("n. po. pe. _Ma_", None), '8': ("qui _Fl_", None), '9': ("beatos _Ma_", None), '10': ("infra _Ox_", None),
 '11': ("Et ideo max. _Ma_", None), '12': ("ac. a D. _Ma_", None), '13': ("Deo _Ox_", None), '14': ("et _Ma_", None),
 '15': ("-liter _Ma_", None), '16': ("Dominum _Mon. Germ._", None), '17': ("sollempn. _Ma_", None), '18': ("Con. _Ma_", None),
 '19': ("magnificis d. h. _Ma_", None), '20': ("Angli q. Dani _Ma_", None), '21': ("arct. _Ma_", None),
 '22': ("in. theloneum _Ma_", None),
 '23': ("Rodbertus _Ox; Pseudo-Ingulf_ [_nach Thorpe_ Chron. Flor. Wig. I 187 _auch Hs. Bodley_ 297; _dagegen_ Rudolphus _Hs. Lambeth_ 42]; _vgl. unten_ 8",
        "Rodbertus _Ox; Pseudo-Ingulf_ [_according to Thorpe_, Chron. Flor. Wig. I 187, _also MS Bodley_ 297; _but_ Rudolphus _MS Lambeth_ 42]; _cf. below_ 8"),
 '24': ("-ctis (-ctisque, -ctum) firmarunt _Ma;_ edictisque _Ox_", None),
 '25': ("gratia _Ma_", None), '26': ("-neorum cum fi. _Ma Ingulf_", None), '27': ("firmaque _Ox_", None),
 '28': ("et i. l. s. _fehlt Ma_", "et i. l. s. _lacking in Ma_"), '29': ("dixi _Ma_", None), '30': ("-bantur _Ma_", None),
 '31': ("-ndo _Ox_", None), '32': ("ea _Mon._", None),
 '33': ("Rodberto _Ox; Ingulf_ [_Bodley; dagegen_ Rudolpho _Lambeth_]; _vgl. o._ 6", "Rodberto _Ox; Ingulf_ [_Bodley; but_ Rudolpho _Lambeth_]; _cf. above_ 6"),
 '34': ("-nter _Ma_", None),
}
N277 = {
 '1': ("-ere et . . firmauere _Ox_", None), '2': ("e. s. _Ma_", None),
 '3': ("quae aderat _ohne_ ibi _Ma_", "quae aderat _without_ ibi _Ma_"),
 '4': ("s. n. _ohne_ o. u. _Ma_", "s. n. _without_ o. u. _Ma_"),
 '5': ("_fehlt Ma_", "_lacking in Ma_"),
 '6': ("omnes _Ox und Ma später Edition_", "omnes _Ox and the later edition of Ma_"),
 '7': ("Icc. _Ma_", None), '8': ("faciant _Ma_", None), '9': ("uolunt h. am. aut su. sa. _Ma_", None),
 '10': ("et d. et p. _fehlt Ma_", "et d. et p. _lacking in Ma_"), '11': ("nec propter al. _Ma_", None),
 '12': ("congerendam _Ma Ingulf_", None), '13': ("deuient _Ma Ing._", None), '14': ("p. m. congeratur _Ma Ing._", None),
 '15': ("quod u. n. f. uolo, ea. _Fl;_ n. u. _Ma_", None), '16': ("-rchiam uado _Ma Ing._", None),
 '17': ("comp. cum eis g., quae nos _Ma Ing. ohne_ et po.", "comp. cum eis g., quae nos _Ma Ing. without_ et po."),
 '18': ("uita et r. _Ma_", None), '19': ("e. p. _Ma_", None), '20': ("potuerunt _Ma_", None), '21': ("benignitate _Ma_", None),
 '22': ("bonitate _eine Fl.-Hs. nach_ Mon. Britan. 597", "bonitate _one MS of Fl, according to_ Mon. Britan. 597"),
 '23': ("et f. d. d. et _fehlt Ma_", "et f. d. d. et _lacking in Ma_"), '24': ("parato uel pacato _Ma_", None),
 '25': ("meo _Ingulf_", None), '26': ("habere _Ma_", None), '27': ("iam _Ma_", None),
 '28': ("p. et _fehlt Ma_", "p. et _lacking in Ma_"), '29': ("e. m. _Ma_", None), '30': ("mihi d. et Deo _Ma_", None),
 '31': ("_fehlt Ma_", "_lacking in Ma_"), '32': ("omnium _Ma_", None), '33': ("-na _Ma_", None), '34': ("ipso anno _Ma_", None),
 '35': ("Romam _Ma_", None), '36': ("debetis _Ma_", None), '37': ("degit _eine Fl.-Hs. Ma_", "degit _one MS of Fl, Ma_"),
 '38': ("-cę _Ox_", None),
 '39': ("cyrce(cyrc-, chirch-, kyrke-, scyre-, scyri-)sceat (-scat, -scet, -scot) _Ma_", None),
 '40': ("-natur _Ma_", None), '41': ("alia si, cum uen. _Ma_", None), '42': ("fuerint _eine Fl.-Hs._", "fuerint _one MS of Fl_"),
 '43': ("-ione _Ox Ma_", None),
}
# Liebermann's right margin, for the record: the clause files already carry these references
# (comparison / comparisonPrinted), which agree with the print. Dates of events are kept as editorial notes.
MARGIN = {
 '12': ([('IEw_Prol', 'I Ew Prol.'), ('IIEw_8', 'II Ew 8')], 'Vgl. I Ew Pr. II 8'),
 '13': ([('Cn1020_6', 'Cn 1020 6')], 'Vgl. 1020, 6'),
 '14': ([('Cn1020_6', 'Cn 1020 6')], 'ebd. [Vgl. 1020, 6]'),
 '15': ([('Cn1020_4', 'Cn 1020 4')], 'ebd. 4 [Cn 1020, 4]'),
 '16': ([('Cn1020_8', 'Cn 1020 8'), ('IIEg_2-3', 'II Eg 2.3'), ('IIEg_3', 'II Eg 3'), ('IIEg_4', 'II Eg 4'), ('IIEg_2-2', 'II Eg 2.2')],
        'Vgl. 1020, 8; Vgl. II Eg. 2, 3; *ebd. 3 [at et* decimę animalium and at frugum*]; **ebd. 4 [at et** denarii]; ebd. 2, 2'),
 '17': ([('IVEg_1-5', 'IV Eg 1.5')], 'Vgl. IV Eg. 1, 5'),
}
DATES = {'3': '1027', '5': '1027, März', '13': '1026', '14': '1027', '16': '† [11. Nov.] (at sancti Martini†)'}
EDNOTES = {
 '11': "Liebermann prints “iuiustitiam”, a misprint for iniustitiam.",
 '12': "Liebermann prints the note number 9 twice here (amicitiam⁹ … et⁹ diuitibus); the second belongs to his note 10 (“et d. et p. fehlt Ma”), and is linked to it.",
}

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def it(s): return re.sub(r'_([^_]+)_', r'<hi rend="italic">\1</hi>', esc(s))

def build(cid, key):
    page = '277' if key in P277 else '276'
    text = esc(TEXT[key])
    used = []
    def ptr(m):
        raw = m.group(1)
        if raw in ('*', '**', '***'):
            used.append(('276', raw, raw)); nid = {'*': 'star', '**': 'star2', '***': 'star3'}[raw]
            return f'<ptr type="liebermannNote" n="{raw}" target="#{cid}.lnote.oe.{nid}"/>'
        shown, _, real = raw.partition('=')
        n, _, pg = (real or shown).partition('@')
        pg = pg or page
        shown = shown.split('@')[0]
        used.append((pg, n, shown))
        suffix = '' if pg == page else '-p' + pg
        return f'<ptr type="liebermannNote" n="{shown}" target="#{cid}.lnote.oe.{n}{suffix}"/>'
    text = re.sub(r'\{([^}]+)\}', ptr, text)
    text = re.sub(r'\^(\*\*|\*|†)', r'<hi rend="superscript">\1</hi>', text)
    text = text.replace('|277|', '<pb n="277" ed="#liebermann"/>')
    ab = f'<ab type="liebermannText" xml:lang="la" source="#liebermann" corresp="#wit-fl"><pb n="{"276" if key not in P277 else "277"}" ed="#liebermann"/>{text}</ab>'
    notes = []
    seen = set()
    for pg, n, shown in used:
        if (pg, n) in seen: continue
        seen.add((pg, n))
        de, en = (N277 if pg == '277' else N276)[n]
        en = en or de
        nid = {'*': 'star', '**': 'star2', '***': 'star3'}.get(n, n) + ('' if pg == page or n in ('*', '**', '***') else '-p' + pg)
        notes.append(f'<note type="liebermannNote" subtype="textual" xml:id="{cid}.lnote.oe.{nid}" n="{n}" source="#liebermann"><bibl><biblScope unit="volume">1</biblScope><biblScope unit="page">{pg}</biblScope></bibl><seg type="original" xml:lang="de">{it(de)}</seg><seg type="translation" xml:lang="en" source="#claude">{it(en)}</seg></note>')
    extra = []
    if key in MARGIN and False:   # the clause files already have these (from the spreadsheet), checked against the print
        refs, printed = MARGIN[key]
        extra.append('<note type="comparison" source="#liebermann" n="' + page + '">' + '; '.join(f'<ref target="clause:{t}">{esc(l)}</ref>' for t, l in refs) + '</note>')
        extra.append(f'<note type="comparisonPrinted" source="#liebermann">{esc(printed)}</note>')
    ed = ["Liebermann’s text transcribed from Gesetze I p. " + ('276–277' if key == '8' else page) + " (November 2026; read twice from the page images and against the text layer). His superscript letters, which refer to his Erklärungen, are left out."]
    if key in DATES: ed.append(f"In Liebermann’s margin, the date: {DATES[key]}.")
    if key in EDNOTES: ed.append(EDNOTES[key])
    return ab, notes, extra, ed

def main():
    for key in TEXT:
        cid = 'Cn1027_' + key
        p = os.path.join(L, cid + '.xml')
        s = open(p, encoding='utf-8').read()
        if 'type="liebermannText"' in s:
            print('already has Liebermann text:', cid); continue
        ab, notes, extra, ed = build(cid, key)
        head_end = s.index('</head>') + len('</head>')
        s = s[:head_end] + '\n        ' + ab + s[head_end:]
        body_close = s.index('      </div>\n    </body>')
        add = ''.join('        ' + x + '\n' for x in extra + [f'<note type="editorial">{esc(t)}</note>' for t in ed] + notes)
        s = s[:body_close] + add + s[body_close:]
        # Robertson's text is Latin, not Old English
        s = s.replace('<ab type="editionText" xml:lang="ang" source="#robertson"', '<ab type="editionText" xml:lang="la" source="#robertson"')
        if 'xml:id="wit-fl"' not in s:
            s = s.replace('        <listWit>\n', '        <listWit>\n          <witness xml:id="wit-fl" rend="bold"><abbr>Fl</abbr> <note type="manuscript">Florence (John) of Worcester, Chronicon, ed. MGH SS XIII 126: Liebermann’s text</note></witness>\n', 1)
        s = s.replace('<respStmt><resp>Edition of the text</resp>', '<respStmt><resp>Edition of the text</resp><name ref="#liebermann">Liebermann</name></respStmt>\n        <respStmt><resp>Transcription of Liebermann’s text and notes</resp><name ref="#claude">Claude</name></respStmt>\n        <respStmt><resp>Edition of the text</resp>', 1)
        if 'xml:id="claude"' not in s:
            s = s.replace('        </listBibl>', '          <bibl xml:id="claude" type="translation">English renderings of Liebermann’s German notes, made for this database in 2026 with Claude, a large language model (LLM) made by Anthropic</bibl>\n        </listBibl>', 1)
        s = s.replace('    </revisionDesc>', '      <change when="2026-11-02">Liebermann’s Latin text, footnotes and marginal references added from Gesetze I pp. 276–277; Robertson’s text marked as Latin.</change>\n    </revisionDesc>', 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('added', cid)

if __name__ == '__main__':
    main()
