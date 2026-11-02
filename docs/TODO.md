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

## bocland: Latin translations (suggestion #31)

The links go to the right clauses: the Instituta (In Cn), Quadripartitus (Q) and Consiliatio (Cons Cn) texts are columns on those clause pages. Two things are wrong:

- [ ] **Highlighting.** After "— Erklärt als allodium …", every link highlights *boclondum* instead of the Latin word Liebermann gives (allodium, testamentalis, libera terra, hereditatis, hereditate, feudum). Proposed: in his translation passages ("übersetzt X Q", "Erklärt als X … In", "X übsnd"), highlight the Latin word X. This applies across the dictionary, so it would be tested on every entry first.
- [ ] **Label.** The citation list calls the Instituta's own clause "II Cn 15,1b". II Cnut has no 15,1b: it is one of the translator's additions. Proposed: list it as "In Cn II 15,1b".

Waiting for Anya's go-ahead (see the comment on suggestion #31).

## "Cons" unlinked in about 180 entries

- [ ] Liebermann's "Cons" after a citation (for example "Hu 8 Cons", "II Cn 45,3 Cons") means the Consiliatio Cnuti's text of that passage. It is linked in *purgamen* (pull request #152) but is plain text in about 180 other entries, while "In" (Instituta) is linked everywhere. Link them all to the Consiliatio Cnuti, as "In" is, and check that the citations around them still link.
