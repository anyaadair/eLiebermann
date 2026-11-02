# To do

Open jobs on eLiebermann, for Anya and Claude. Tick a box (change `[ ]` to `[x]`) when a job is done, or ask Claude to. The marginal notes have their own list: [MARGINAL-NOTES-TODO.md](MARGINAL-NOTES-TODO.md).

## For Anya: check against the scan

Citations that may be misprints in the *Wörterbuch*, or slips in the transcription. Each one is listed under the entry as "Not yet in the laws database" until it is checked. Pull request #152 found them.

- [ ] **wedd**, "III Atr 12,7": III Æthelred has no 12,7. The words are in III Atr 12 (*lecge … wedd*) and III Atr 7 (*to wedde*), so the print may read "12. 7" (two citations).
- [ ] **Antithese**, "II Cn 8,4" (*don ⁊ forgan*): II Cnut has no 8,4. *forgan* is in II Cn 84, so it may be "84".
- [ ] **li**, "Wl art Fz 1,1" (*la terre Insc; mere 1,1*): the laws database has no Wl art Fz 1,1, only clause 1. Check whether Liebermann's 1,1 is part of clause 1.
- [ ] **Dene**, "ECf 10,33", and **cheminus**, "ECf 12,13": no such ECf clauses; probably misprints (left from the ECf transcription).

## Works cited in the notes to the laws: citations to check

About 340 works that Liebermann cites in his notes to the laws were added to [Authors and Works Cited](https://anyaadair.github.io/eLiebermann/bibAbb.html) in November 2026, with full citations. Some still have something uncertain: a work not identified, a publisher or series number not confirmed, or a question only the printed *Gesetze* can answer.

- [ ] **Go through the list in [CITATIONS-TO-CHECK.md](CITATIONS-TO-CHECK.md).** To find it: on GitHub, open the repository, then the `docs` folder, then `CITATIONS-TO-CHECK.md` (it is next to this file). It has three parts: (1) three questions to check against the scan, (2) works not identified or with no library record, (3) works with one detail to check. Each item links to its entry on the site and to clauses where Liebermann cites it. On the site, the same doubts are in each entry's Note, marked *to check*. When you settle one, tell Claude what you found, and it will correct the entry and tick the box.

## English crib of the texts with no translation

About 3,170 clauses had no translation at all, nearly all Latin. An English crib, made with an LLM (Claude, 2026) and labelled so on the clause pages, is being added in batches with `tools/add-crib.py`, following `tools/crib/BRIEF.md` (texts extracted with `tools/crib/extract.py`).

- [x] Excommunication formulas (Excom I–XIII), ordeal rituals (Iud Dei I–XVI), Duel: 723 texts, Latin and Old English (November 2026).
- [x] Instituta Cnuti: the existing crib (`data/incn-crib.json`) put on its 207 clause pages. The 31 In Cn clauses that are only Liebermann's pointers ("Si quis … — — …; o. S. 295") have none.
- [x] Ps. Cnut de foresta, Libertas Londoniensis, VI Atr Latin paraphrase, Wl art (French and retractatus), Wl Edmr, Cons Cn, App AGu, and the stray Old English rubrics (CHn cor, Af Rb).
- [x] Quadripartitus (Dedicatio, Argumentum, Liber I titles and rubrics, Liber II).
- [x] Leges Edwardi Confessoris and its retractatus.
- [ ] Leges Henrici Primi.

**For Anya: doubtful readings in the crib.**

<!-- crib-doubtful -->
85 clauses have a crib that marks a doubtful reading with “[?]”, mostly a corrupt or unusual word in the Latin; a look at the scan may settle some.

- [ ] **Æthelred II** (2): [VI Atr Lat 2](https://anyaadair.github.io/eLiebermann/law.html?id=VI-Atr-Latin-Paraphrase_2), [VI Atr Lat 5.3](https://anyaadair.github.io/eLiebermann/law.html?id=VI-Atr-Latin-Paraphrase_5-3)
- [ ] **Attributed to William I** (6): [Wl art retr 10](https://anyaadair.github.io/eLiebermann/law.html?id=WlArtRetr_10), [Wl art retr 14.2](https://anyaadair.github.io/eLiebermann/law.html?id=WlArtRetr_14-2), [Wl art Frz 3.1](https://anyaadair.github.io/eLiebermann/law.html?id=Wl-art-Frz_3-1), [Wl art Frz 5](https://anyaadair.github.io/eLiebermann/law.html?id=Wl-art-Frz_5), [Wl art Frz 8.2](https://anyaadair.github.io/eLiebermann/law.html?id=Wl-art-Frz_8-2), [Wl art Frz 10](https://anyaadair.github.io/eLiebermann/law.html?id=Wl-art-Frz_10)
- [ ] **Iudicium Dei I: cold-water ordeal ritual** (2): [Iud Dei I 21.3](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiI_21-3), [Iud Dei I 21.5](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiI_21-5)
- [ ] **Iudicium Dei II: fire (hot-iron) ordeal ritual** (1): [Iud Dei II 4.2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiII_4-2)
- [ ] **Iudicium Dei III: ordeal of the consecrated morsel** (3): [Iud Dei III 1.3](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIII_1-3), [Iud Dei III 3](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIII_3), [Iud Dei III 3.1](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIII_3-1)
- [ ] **Iudicium Dei IV: cauldron (hot-water) ordeal ritual, from Kent and Northumbria (Latin with Old English gloss)** (3): [Iud Dei IV 2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIV_2), [Iud Dei IV 4.4](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIV_4-4), [Iud Dei IV 4.5](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIV_4-5)
- [ ] **Iudicium Dei V: fire ordeal ritual, from Kent and Northumbria (Latin with Old English gloss)** (3): [Iud Dei V 1.6](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiV_1-6), [Iud Dei V 2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiV_2), [Iud Dei V 2.3](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiV_2-3)
- [ ] **Iudicium Dei VII: cold-water ordeal ritual (Latin and Old English)** (1): [Iud Dei VII 13A](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiVII_13A)
- [ ] **Iudicium Dei IX: iron ordeal ritual** (3): [Iud Dei IX 2.2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIX_2-2), [Iud Dei IX 3.7](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIX_3-7), [Iud Dei IX 4](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiIX_4)
- [ ] **Iudicium Dei X: cold-water ordeal ritual** (2): [Iud Dei X 19.3](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiX_19-3), [Iud Dei X 21.1](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiX_21-1)
- [ ] **Iudicium Dei XI: iron ordeal ritual** (1): [Iud Dei XI 5.2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiXI_5-2)
- [ ] **Iudicium Dei XII: cauldron (hot-water) ordeal ritual** (2): [Iud Dei XII 4.2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiXII_4-2), [Iud Dei XII 17.2](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiXII_17-2)
- [ ] **Iudicium Dei XIII: cold-water ordeal ritual** (1): [Iud Dei XIII 11.1](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiXIII_11-1)
- [ ] **Iudicium Dei XIV: ordeal of the consecrated morsel** (2): [Iud Dei XIV 4](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiXIV_4), [Iud Dei XIV 6.1](https://anyaadair.github.io/eLiebermann/law.html?id=IudDeiXIV_6-1)
- [ ] **Excommunicatio I: formula of excommunication** (2): [Excom I 11](https://anyaadair.github.io/eLiebermann/law.html?id=ExcomI_11), [Excom I 20](https://anyaadair.github.io/eLiebermann/law.html?id=ExcomI_20)
- [ ] **Excommunicatio IV: formula of excommunication** (1): [Excom IV 12](https://anyaadair.github.io/eLiebermann/law.html?id=ExcomIV_12)
- [ ] **Excommunicatio VI: formula of excommunication** (1): [Excom VI 15](https://anyaadair.github.io/eLiebermann/law.html?id=ExcomVI_15)
- [ ] **Excommunicatio VIII: formula of excommunication** (1): [Excom VIII 25](https://anyaadair.github.io/eLiebermann/law.html?id=ExcomVIII_25)
- [ ] **Quadripartitus: Dedicatio** (10): [Quadr Ded 1](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_1), [Quadr Ded 11](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_11), [Quadr Ded 13](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_13), [Quadr Ded 14](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_14), [Quadr Ded 16](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_16), [Quadr Ded 20](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_20), [Quadr Ded 21](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_21), [Quadr Ded 27](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_27), [Quadr Ded 30](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_30), [Quadr Ded 34](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrDed_34)
- [ ] **Quadripartitus: Argumentum** (5): [Quadr Arg 5](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrArg_5), [Quadr Arg 11](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrArg_11), [Quadr Arg 12](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrArg_12), [Quadr Arg 15](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrArg_15), [Quadr Arg 22](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrArg_22)
- [ ] **Quadripartitus, Liber I: titles of the laws** (1): [Quadr I IV Atr](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-I_IV-Atr)
- [ ] **Quadripartitus, Liber I: rubric lists** (5): [Quadr Rb II Cn 51](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-Rb_II-Cn-51), [Quadr Rb Hundred 8](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-Rb_Hundred-8), [Quadr Rb VI As 8](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-Rb_VI-As-8), [Quadr Rb VI As 8.9](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-Rb_VI-As-8-9), [Quadr Rb EGu 12](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-Rb_EGu-12)
- [ ] **Quadripartitus, Liber II: Praefatio** (3): [Quadr II Praef 4](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-II-Praef_4), [Quadr II Praef 11](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-II-Praef_11), [Quadr II Praef 13](https://anyaadair.github.io/eLiebermann/law.html?id=Quadr-II-Praef_13)
- [ ] **Quadripartitus, Liber II** (1): [Quadr II 17.4](https://anyaadair.github.io/eLiebermann/law.html?id=QuadrII_17-4)
- [ ] **Consiliatio Cnuti** (2): [Cons Cn II 22.1b](https://anyaadair.github.io/eLiebermann/law.html?id=ConsCn_II-22-1b), [Cons Cn III 1](https://anyaadair.github.io/eLiebermann/law.html?id=ConsCn_III-1)
- [ ] **Pseudo-Cnut, Constitutiones de foresta** (4): [Ps Cn for 6](https://anyaadair.github.io/eLiebermann/law.html?id=PsCnFor_6), [Ps Cn for 13](https://anyaadair.github.io/eLiebermann/law.html?id=PsCnFor_13), [Ps Cn for 13.1](https://anyaadair.github.io/eLiebermann/law.html?id=PsCnFor_13-1), [Ps Cn for 33](https://anyaadair.github.io/eLiebermann/law.html?id=PsCnFor_33)
- [ ] **Libertas Londoniensis** (2): [Lib Lond 8.1](https://anyaadair.github.io/eLiebermann/law.html?id=LibLond_8-1), [Lib Lond 8.3](https://anyaadair.github.io/eLiebermann/law.html?id=LibLond_8-3)
- [ ] **Leges Edwardi Confessoris** (10): [ECf 13.1 A](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_13-1-A), [ECf 26](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_26), [ECf 32 B 5](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_32-B-5), [ECf 32 B 11](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_32-B-11), [ECf 32 B 13](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_32-B-13), [ECf 32 C 1](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_32-C-1), [ECf 32 D 3](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_32-D-3), [ECf 32 D 5](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_32-D-5), [ECf 33](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_33), [ECf 34.2b](https://anyaadair.github.io/eLiebermann/law.html?id=ECf_34-2b)
- [ ] **Leges Edwardi Confessoris: retractatus** (5): [ECf retr 8.2a](https://anyaadair.github.io/eLiebermann/law.html?id=ECfRetr_8-2a), [ECf retr 33](https://anyaadair.github.io/eLiebermann/law.html?id=ECfRetr_33), [ECf retr 38.1a](https://anyaadair.github.io/eLiebermann/law.html?id=ECfRetr_38-1a), [ECf retr 39.1a](https://anyaadair.github.io/eLiebermann/law.html?id=ECfRetr_39-1a), [ECf retr 39.2](https://anyaadair.github.io/eLiebermann/law.html?id=ECfRetr_39-2)
<!-- /crib-doubtful -->

## bocland: Latin translations (suggestion #31)

The links go to the right clauses: the Instituta (In Cn), Quadripartitus (Q) and Consiliatio (Cons Cn) texts are columns on those clause pages. Two things are wrong:

- [ ] **Highlighting.** After "— Erklärt als allodium …", every link highlights *boclondum* instead of the Latin word Liebermann gives (allodium, testamentalis, libera terra, hereditatis, hereditate, feudum). Proposed: in his translation passages ("übersetzt X Q", "Erklärt als X … In", "X übsnd"), highlight the Latin word X. This applies across the dictionary, so it would be tested on every entry first.
- [ ] **Label.** The citation list calls the Instituta's own clause "II Cn 15,1b". II Cnut has no 15,1b: it is one of the translator's additions. Proposed: list it as "In Cn II 15,1b".

Waiting for Anya's go-ahead (see the comment on suggestion #31).

## "Cons" unlinked in about 180 entries

- [ ] Liebermann's "Cons" after a citation (for example "Hu 8 Cons", "II Cn 45,3 Cons") means the Consiliatio Cnuti's text of that passage. It is linked in *purgamen* (pull request #152) but is plain text in about 180 other entries, while "In" (Instituta) is linked everywhere. Link them all to the Consiliatio Cnuti, as "In" is, and check that the citations around them still link.
