# To do

Open jobs on eLiebermann, for Anya and Claude. Tick a box (change `[ ]` to `[x]`) when a job is done, or ask Claude to. The marginal notes have their own list: [MARGINAL-NOTES-TODO.md](MARGINAL-NOTES-TODO.md).

## For Anya: check against the scan

Citations that may be misprints in the *Wörterbuch*, or slips in the transcription. Each one is listed under the entry as "Not yet in the laws database" until it is checked. Pull request #152 found them.

- [ ] **wedd**, "III Atr 12,7": III Æthelred has no 12,7. The words are in III Atr 12 (*lecge … wedd*) and III Atr 7 (*to wedde*), so the print may read "12. 7" (two citations).
- [ ] **Antithese**, "II Cn 8,4" (*don ⁊ forgan*): II Cnut has no 8,4. *forgan* is in II Cn 84, so it may be "84".
- [ ] **li**, "Wl art Fz 1,1" (*la terre Insc; mere 1,1*): the laws database has no Wl art Fz 1,1, only clause 1. Check whether Liebermann's 1,1 is part of clause 1.
- [ ] **Dene**, "ECf 10,33", and **cheminus**, "ECf 12,13": no such ECf clauses; probably misprints (left from the ECf transcription).

## bocland: Latin translations (suggestion #31)

The links go to the right clauses: the Instituta (In Cn), Quadripartitus (Q) and Consiliatio (Cons Cn) texts are columns on those clause pages. Two things are wrong:

- [ ] **Highlighting.** After "— Erklärt als allodium …", every link highlights *boclondum* instead of the Latin word Liebermann gives (allodium, testamentalis, libera terra, hereditatis, hereditate, feudum). Proposed: in his translation passages ("übersetzt X Q", "Erklärt als X … In", "X übsnd"), highlight the Latin word X. This applies across the dictionary, so it would be tested on every entry first.
- [ ] **Label.** The citation list calls the Instituta's own clause "II Cn 15,1b". II Cnut has no 15,1b: it is one of the translator's additions. Proposed: list it as "In Cn II 15,1b".

Waiting for Anya's go-ahead (see the comment on suggestion #31).

## "Cons" unlinked in about 180 entries

- [ ] Liebermann's "Cons" after a citation (for example "Hu 8 Cons", "II Cn 45,3 Cons") means the Consiliatio Cnuti's text of that passage. It is linked in *purgamen* (pull request #152) but is plain text in about 180 other entries, while "In" (Instituta) is linked everywhere. Link them all to the Consiliatio Cnuti, as "In" is, and check that the citations around them still link.
