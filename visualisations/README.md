# Visualisation Tools

Interactive pictures of the TEI, in the site's **Visualisation Tools** section (main menu, between Editorial Principles and About): `https://anyaadair.github.io/eLiebermann/visualisations/`. They began as standalone experiments in `experiments/`; those addresses now forward here. Each page is a site page (the site's layout, menu and footer) with its CSS, JavaScript and data inline. The CSS is scoped under `.viz` and uses the site's colours and type. Only [D3](https://d3js.org/) 7.9.0 (and, for the map, [Leaflet](https://leafletjs.com/) 1.9.4 with OpenStreetMap tiles) comes from a CDN (cdnjs). The overview, `index.html`, is written by hand and groups the tools under three headings: Borrowing and reuse; Time, place and manuscripts; Words and subjects.

| Page | What it shows | Made from |
|---|---|---|
| [law-code-borrowing.html](law-code-borrowing.html) | Which law codes borrow from which: arcs between codes in the order of the kings, or a force network. Filter by kind of link (source, compare, contrast) and by scholar; click a code or an arc to list the clause pairs. | `<note type="comparison">` and `<note type="comparedBy">` in `oe-laws/`, with `data/comparison-terms.json` for the kind |
| [shared-vocabulary.html](shared-vocabulary.html) | Law codes joined by the Wörterbuch headwords they share (Jaccard overlap, closest neighbours only). Search a headword to light up the codes that cite it; click a code for its closest codes and most distinctive words. | `<xr type="lawCode">` in `entries/` |
| [manuscripts-and-codes.html](manuscripts-and-codes.html) | Law codes on a time axis at the date they were made, joined to the manuscripts and early prints that carry them at the date they were written. Click a code or manuscript to follow it. | `<witness>` in `oe-laws/`, dated from `data/manuscripts.json` |
| [subjects-together.html](subjects-together.html) | Subject keywords joined when they are tagged on the same clauses more often than chance (lift), each keeping its strongest partners. | `<keywords>` in `oe-laws/`, `data/subject-groups.json` |
| [reuse-chains.html](reuse-chains.html) | A tree from one clause: later clauses that take it up to the right, earlier ones it draws on to the left. | the same comparison notes as the borrowing page |
| [dating-the-codes.html](dating-the-codes.html) | One bar per scholar per law code (range, likely date, open-ended), sortable by disagreement. Not a network. | `dates` in `oe-laws/codes.json` |
| [where-codes-were-made.html](where-codes-were-made.html) | A Leaflet map of the places where codes were issued, with a time slider. Coordinates are in `PLACES` in `build.py`. Not a network. | `<creation><placeName>` (`places` in `oe-laws/codes.json`) |
| [headword-crossrefs.html](headword-crossrefs.html) | Liebermann's *s.*, *vgl.* and *Der.* as a network of word families, one to three steps out from a headword. | `<xr type="see|compare|derivative">` in `entries/` |



## Making the pages again

The pages are made from `templates/` by `build.py`, which reads the TEI and puts the data where each template says `/*DATA*/null`:

```sh
python3 visualisations/build.py
```

Run it from the repository root after the entries or clauses change. It needs only Python 3. Edit the templates, not the generated pages. Each template starts with the page's front matter and wraps its content in `{% raw %}` so the site build leaves the inline data alone.
