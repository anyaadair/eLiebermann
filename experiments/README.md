# Experiments: network visualisations

Standalone pages that try out pictures of the TEI. Nothing on the site links to them. Each page is a single HTML file with its CSS, JavaScript and data inline; only [D3](https://d3js.org/) 7.9.0 comes from a CDN (cdnjs). Open a file straight from disk, or at `https://anyaadair.github.io/eLiebermann/experiments/` once merged.

| Page | What it shows | Made from |
|---|---|---|
| [law-code-borrowing.html](law-code-borrowing.html) | Which law codes borrow from which: arcs between codes in the order of the kings, or a force network. Filter by kind of link (source, compare, contrast) and by scholar; click a code or an arc to list the clause pairs. | `<note type="comparison">` and `<note type="comparedBy">` in `oe-laws/`, with `data/comparison-terms.json` for the kind |
| [shared-vocabulary.html](shared-vocabulary.html) | Law codes joined by the Wörterbuch headwords they share (Jaccard overlap, closest neighbours only). Search a headword to light up the codes that cite it; click a code for its closest codes and most distinctive words. | `<xr type="lawCode">` in `entries/` |
| [headword-crossrefs.html](headword-crossrefs.html) | Liebermann's *s.*, *vgl.* and *Der.* as a network of word families, one to three steps out from a headword. | `<xr type="see|compare|derivative">` in `entries/` |

`index.html` lists them.

## Making the pages again

The pages are made from `templates/` by `build.py`, which reads the TEI and puts the data where each template says `/*DATA*/null`:

```sh
python3 experiments/build.py
```

Run it from the repository root after the entries or clauses change. It needs only Python 3. Edit the templates, not the generated pages.
