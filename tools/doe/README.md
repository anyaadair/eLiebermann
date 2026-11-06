# Dictionary of Old English links

Scripts that guess links from eLiebermann's Old English entries to the *Dictionary of Old English* (DOE, A–Le) and add `<xr type="doe">` links (shown under "Other dictionaries" on each entry page). Python 3 only.

## The DOE's headword lists

The DOE gives no data file, but its browse pages list every headword with its entry number. For each letter, open the DOE's list of words beginning with that letter, scroll to the bottom (some letters have a second page), open the Console (Mac Chrome: Cmd + Option + J) and run:

```js
copy([...document.querySelectorAll('li.doe-result')].map(li => li.id.replace('doe-','') + '\t' + li.querySelector('.doe-oesp').textContent.trim()).join('\n'))
```

Paste the result into a plain-text file and save it in `lists/` (`A.txt`, `Æ.txt`, `B.txt` …). Each line is `E00946<TAB>abbod`. Æ is a letter of its own in the DOE.

## Steps

1. **Match**: `python3 -I tools/doe/match.py tools/doe/lists/A.txt --out out.json` (several lists may be given). Only entries whose headword falls between the first and last word of the lists are matched. Grades:
    - *sure*: the same word once hyphens, length marks, ð/þ and Liebermann's square brackets are ignored;
    - *likely*: a spelling variant (i/y/ie, double letters, -ian/-an), Liebermann's verb form traced to the infinitive (-að/-eð → -an/-ian, Anya's rule), x/cs/sc (acsian = āxian), æw- for ǣ- (æwbryce = ǣ-bryce), rg/rh and -cean/-can (burg = burh, borh = borg, betæcean = be-tǣcan), or the headword of the entry's Bosworth-Toller link (those are guesses too, so never more than likely);
    - *unsure*: more than one DOE entry fits (ac / āc), or only an inflected noun form matches;
    - *none*.
   Word-parts ("and-") are matched only to DOE word-parts ("an-"). A headword with a capital (perhaps a name: Bocland, the place) is never more than unsure. A bracket at the start of a headword ([on]butan) is kept, so it is not matched to the second part alone. Cross-reference and spelling entries are never matched: they get no dictionary links. Run all the lists together, so that a word can match in another letter (ærcediacon → arce-dīacon); each list's first and last word set its range (ignoring ge· words, which the DOE files under their stem, and suffixes like -lac), compared in the DOE's alphabet (æ after a, þ after t). DOE suffixes (-lac, -lǣwe) are never matched. A verb-form guess that competes with a noun or adjective (læwed: lǣwan or lǣwede) is unsure. cg and g are not treated as one (l[i]eg is not lecg).
2. **Review page**: `python3 tools/doe/build.py out.json tools/doe/page-template.html doe-matches.html`, published on claude.ai as *DOE Matches* with the `db` capability. The editor's choices are saved in the collection `decisions` (one document per entry: `{"ids": [...]}`; an empty list means no link). An E-number can be typed in when no guess is right.
3. **Apply**: save the choices with ArtifactData `list` (`out_dir`), then `python3 -I tools/doe/apply.py out.json <folder with decisions/*.json>` from the repository root. Adds links for sure and likely matches and for every entry with a saved choice (which wins), with a line in the entry's revision history. It only adds links; removing one is done by hand. Cross-reference entries are skipped.

## Two addresses

The DOE has one address for institutional subscribers (`dictionary.doe.utoronto.ca`) and one for individual subscribers (`indiv.dictionary.doe.utoronto.ca`). The entry files keep an address, but entry.html uses only its entry number and builds the address the reader chose under "I use the DOE through" (remembered in the browser as `eLiebermann.doeAccess`; institutional at first).
