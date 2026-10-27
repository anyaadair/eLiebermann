# To do: Liebermann's marginal notes cut off in the scan

Liebermann prints his cross-references (*Vgl. …*) in the right-hand margin of *Gesetze* I. On even (left-hand) pages that margin is the gutter, and the archive.org scan (*diegesetzederang01liebuoft*) cuts into it, so many notes were transcribed incomplete. This list says what is still to check against a printed copy. A survey of every page of the scan in October 2026 found the pages; odd pages are not affected.

**How to complete a page:** photograph it (or read the notes aloud) and give the readings to Claude. They go into `data/vgl-readings.json` and `python3 tools/add-vgl.py` writes them into the clause files, with links both ways. See [OE-LAWS.md](OE-LAWS.md#liebermanns-cross-references-vgl).

## Done
- pp. 170–190 (III As, IV As, VI As, III Em) and pp. 246–274 (V–X Atr, Cn 1020): October 2026, pull request #5.
- p. 394 (Appendix to AGu 1–5), with App AGu 6–7 on p. 395 linked: October 2026.
- pp. 390, 392, 396 (Forfang, Pax, Walreaf, Wergeldzahlung, Swerian): checked in the book; no marginal notes.
- p. 450 (Rect 9, 9.1): checked in the book; the three notes (vgl. 8; vgl. 4, 1; vgl. 21, 4) were already complete.

## Still flagged in the database ("still to be completed")
- [ ] pp. 380, 382, 384: Northumbrian Priests' Law (Northu)
- [ ] p. 386: Ordal
- [ ] p. 400: Becwæð
- [ ] p. 444: Rect
- [ ] p. 462: Mirce
- [ ] pp. 470, 472: Grið
- [ ] p. 476: Iudex
- [ ] p. 484: Wl lad
- [ ] pp. 486, 488: Wl art
- [ ] p. 490: Wl art retr
- [ ] pp. 514, 516: Leis Wl

## Not flagged, but need checking against the book
The notes on these pages were transcribed without any flag, but they are cut at the gutter and some stored readings look truncated (for example "103, 32" on its own at Iud Dei X 19.1, where the page seems to read "Ps. 118, 137; 103, 32"). Most are references to the Bible and canon law, which have no clause pages to link to, so they are shown as plain text.
- [ ] pp. 402–430 (even pages): Iudicium Dei I–XVI (ordeal rituals)
- [ ] pp. 432–440 (even pages): Excommunicatio I–X
- [ ] p. 474: Iudex
- [ ] p. 518: Leis Wl
- [ ] p. 520: Leis Wl / Wl Edmr

## Never transcribed (after p. 528)
None of these texts has any of Liebermann's marginal notes in the database yet, and their even pages are cut at the gutter, so a printed copy is needed from the start.
- [ ] Quadripartitus Ded., Arg., Liber I–II: pp. 532, 534, 540, 542, 544
- [ ] Leges Henrici: pp. 546–610 (worst on 550–568 and 590–610)
- [ ] Instituta Cnuti: pp. 612, 616
- [ ] Consiliatio Cnuti: p. 618
- [ ] Pseudo-Cnut de foresta: pp. 620–626
- [ ] Leges Edwardi Confessoris: pp. 636, 656–664

## Worth knowing
Completing pages turned up notes the first transcription missed or got slightly wrong even where nothing was flagged (IV As 6,2a; X Atr 1; Cn 1020 16), so a page "not flagged" is not a guarantee.
