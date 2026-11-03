"""Liebermann's lower-case sigla for manuscripts he infers but nobody has seen: "Posited by Liebermann"
(data/manuscripts.json). "Lost" only for manuscripts known to have existed; no tag for texts and
collections that survive in copies. Later scholarship (Wormald, Sisam, O'Brien) noted where it differs."""
import json
p = 'data/manuscripts.json'
s = open(p, encoding='utf-8').read()
lines = s.split('\n')
POS = lambda what: f'Posited by Liebermann: {what}, inferred from the readings they share. No such manuscript survives.'
W_L = ('Wormald (1999, pp. 261–2, after Sisam and Flower): the texts Lambarde printed came from transcripts made by '
       'Laurence Nowell in the 16th century, not from lost medieval manuscripts.')
SISAM = ('Sisam showed (and Wormald 1999, p. 261, accepts) that Lambarde’s texts of I As, As Alm, Norðleod, Mirce and Að are '
         '“translations of the Quadripartitus into Elizabethan Anglo-Saxon”: there Ld agrees with Quadr. because it was translated from it.')
E_ = {
 'adg':  (POS('a common source of A and dg'), '[posited] A common source of A and dg for II–III Edgar, posited by Liebermann.'),
 'adow': (POS('a common source of Ad, Ck, Do, No, Wo and Ed'), '[posited] A common source of ECf to 34,1a, posited by Liebermann behind manuscripts Ad, Ck, Do, No, Wo and Ed.'),
 'aq':   (POS('a common source of A and the Quadripartitus'), '[posited] A common source of A and the Quadripartitus for Cnut’s laws, posited by Liebermann. Wormald (1999, p. 351) doubts that any such stemma can be drawn for Cnut’s code, which attracted variants from every side; he prefers to speak of a “post-conquest vulgate”.'),
 'cis':  (POS('a common source of Cii and St'), '[posited] A common source of Cii and St for the Pseudo-Cnut forest law, posited by Liebermann.'),
 'dg':   (POS('a common source of D and G'), '[posited] A common source of D and G (for III Eg meaning G 2) for I As, III Eg and V and VIII Atr, posited by Liebermann, who calls it a collector (“Sammler dg”). Cf. adg.'),
 'dhu':  (POS('a common source of Di and Ip Hunt'), '[posited] A common source of Di and Ip Hunt for the Instituta Cnuti, posited by Liebermann. O’Brien (2003): the same common source appears in O’Brien’s family tree as β.'),
 'doi':  (POS('a common source of D, O and the Instituta Cnuti'), '[posited] A common source of D, O and the Instituta Cnuti for these tracts, as against the other class followed by H and lq, posited by Liebermann.'),
 'gls':  (POS('a common source of G and ls'), '[posited] A common source of G and ls for Alfred–Ine and II–III Edgar, posited by Liebermann. Wormald (1999, p. 265) finds Liebermann’s account of the manuscripts of Alfred’s law-book too flawed to reproduce.'),
 'hb':   (POS('a common source of H and B'), '[posited] A common source of H and B for Alfred–Ine, Blas and Forf, EGu, II As, Swer, Wer, I–II Ew, I–II Em, I Atr, Wif, the charm against cattle theft and Becwæð, posited by Liebermann, who calls it a collector (“Sammler hb”); in his view it had already introduced prepositions into Ine and probably contained the Wessex genealogy.'),
 'hd':   (POS('a common source of hrl, Ps Cn for and dhu'), '[posited] A common source for In Cn of hrl, of Ps Cn for and of dhu, posited by Liebermann. O’Brien (2003): O’Brien’s family tree has no such shared source of H and Di: H (γ), Di with the Huntingdon copies (β) and T with Cb (δ) each come separately from the original (α).'),
 'hlq':  (POS('a common source of H, l and the Quadripartitus'), '[posited] A common source of H, l and the Quadripartitus, posited by Liebermann. On l, see that entry.'),
 'hq':   (POS('a common source of H and the Quadripartitus'), '[posited] A common source of H and the Quadripartitus, posited by Liebermann.'),
 'hrl':  (POS('a common source of H and Rl'), '[posited] An early-12th-century common source of H and Rl for CHn cor (cf. Harley 1757), Wl art and In Cn, posited by Liebermann; for In Cn he derives it from hd. O’Brien (2003): O’Brien argues that Rl was copied from H, so for the Instituta there was no hrl.'),
 'lq':   ('Posited by Liebermann: his siglum for the readings Ld and the Quadripartitus share, which he also treats as their lost common source. No such manuscript survives.', None),
 'ls':   (POS('a common source of Ld and So'), '[posited] A common source of Ld and So for Alfred–Ine and II Edgar, posited by Liebermann and derived by him from gls. On Lambarde’s sources, see l.'),
 'osq':  (POS('a common source of Ot and sq'), '[posited] A common source of Ot and sq for II Æthelstan, posited by Liebermann.'),
 'rv':   (POS('a common source of Ra and Vi'), '[posited] A common source of Ra and Vi for the Tripartita, posited by Liebermann.'),
 'sp':   (POS('a common source of S and Pl'), '[posited] A common source of S and Pl for ECf (with rubrics from ECf retr), Libertas Londoniensis, Instituta Cnuti (Ip Hunt class) and the Tripartita (Wl art, Genealogia Normannica continued to John), posited by Liebermann. O’Brien (2003): O’Brien’s family tree has the same common source of S and Pl (his ι), and below it a second lost manuscript (π) behind Pl, Vincent 98 and Harley 785.'),
 'sq':   (POS('a common source of So and the Quadripartitus'), '[posited] A common source of So and the Quadripartitus for II Æthelstan, posited by Liebermann and derived by him from osq.'),
 'tcb':  (POS('a common source of T and Cb'), '[posited] A common source of T and Cb for the Instituta Cnuti, posited by Liebermann. O’Brien (2003): the same common source appears in O’Brien’s family tree as δ.'),
}
IL = {'Vorlage für I und L[ateinischen Übersetzer der Leis Wl]':
        (POS('a common source of I (Pseudo-Ingulf) and the Latin translator L of the Leis Willelme'), '[posited] A common source of Leis Wl used, in Liebermann’s view, by I (Pseudo-Ingulf) and by the Latin translator L; posited by Liebermann.'),
      'Andere Hs. il, für Cn Vorlage von l und In Cn':
        (POS('a common source of l and the Instituta Cnuti'), '[posited] A different source also called il, posited by Liebermann: for Cnut the source of l and of In Cn, close to aq. On l, see that entry.')}
OTHER = {
 'l':   ('Lambarde’s source for Ld, which Liebermann took to be a lost medieval manuscript', '[lost] The source from which Lambarde printed (Ld). Liebermann took it to be a lost medieval manuscript (“mittelalterliche Zwischenstufe”). ' + W_L + ' For Cnut, Lambarde’s copy was Nowell’s transcript of Harley 55 (B), emended from A, Corpus 383 and the Quadripartitus; Wormald finds Liebermann’s stemma “spot on, except that the lost manuscript, ‘l’, was Nowell’s transcript”. Compare hlq, il, ls, lq.'),
 'ry':  (None, '[lost] The manuscript used for Rymer’s Foedera (ed. 1816, I 3) for William’s episcopal-courts writ, now lost.'),
 'MsLond': (None, 'The original of the London collection Leges Anglorum (c. 1210), which survives in copies; Liebermann’s Lond is the reading where K, Co, Or, Gi, Sl, Tw (or at least the first three) agree. Gi, Sl and Tw are known only from variants cited by 17th/18th-century editors. It contained the Expositio vocabulorum and Numerus provinciarum, then texts from the Quadripartitus with interpolated historical connections and supposed laws of London invention (incl. Pseudo-Ine, Pseudo-Alfred), then from the Tripartita the rubric list, Wl art retr, ECf retr with London interpolations and the Genealogia Normannica, and finally Henry I’s laws with his coronation charter and London charter.'),
 'Tripartita': (None, 'STRIP'), 'West': (None, 'STRIP'), 'm': ('The latest recension of the Quadripartitus (a version surviving in M, Hk and Br)', 'STRIP'),
 'anderesL': (None, 'STRIP'),
}
LQ_NOTE = ('[posited] Posited by Liebermann. In a footnote to I As Prol. (Gesetze I, p. 147, note *) he explains: “What Ld and Quadr. have in common I call lq.” '
  'So in his German translation, words in round brackets followed by lq, e.g. “(meines lq)”, are words found in both Ld and Quadr. but not in the other manuscripts; and in his notes, “lq’s reading” is the reading the two share. '
  'In his introduction (pp. xxiv, xxxiv) he goes further and treats lq as a lost collection (“Sammelband”) from which both Lambarde’s source l and the Quadripartitus drew, for Alfred–Ine, AGu, I–II Edward, I and V Æthelstan, Æthelstan’s Alms ordinance, II–III Edgar, II Æthelred, Dunsæte, Norðleod, Mirce and Að; '
  'on this site it is also cited in his notes to EGu, II As, I–II Em and Geþyncðo. ' + SISAM + ' On Lambarde’s sources generally, see l. Cf. hlq.')
out = []; seen = set()
for ln in lines:
    st = ln.strip()
    if not st.startswith('{'): out.append(ln); continue
    comma = st.endswith(',')
    r = json.loads(st.rstrip(','))
    a = r['Anchor']
    if a == 'il':
        en, no = IL[r['German Expansion']]; r['English Translation'] = en; r['Notes'] = no; seen.add(a)
    elif a in E_:
        en, no = E_[a]; r['English Translation'] = en; r['Notes'] = no or LQ_NOTE; seen.add(a)
    elif a in OTHER:
        en, no = OTHER[a]
        if en: r['English Translation'] = en
        r['Notes'] = r['Notes'].replace('[lost] ', '', 1) if no == 'STRIP' else no
        seen.add(a)
    elif '[lost]' in r.get('Notes', '') or r.get('English Translation', '').startswith('Lost manuscript'):
        raise SystemExit('unclassified: ' + a)
    out.append(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + (',' if comma else ''))
missing = (set(E_) | set(OTHER) | {'il'}) - seen
assert not missing, missing
s2 = '\n'.join(out); json.loads(s2)
open(p, 'w', encoding='utf-8').write(s2)
print('ok')
