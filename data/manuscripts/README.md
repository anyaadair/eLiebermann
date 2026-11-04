# The Manuscripts guide: one file per entry

Each file here is one line of the Manuscripts guide (msAbb.html): a manuscript, a transcript, an early print or a manuscript Liebermann posited. The files hold more than the guide shows, kept apart by source. The guide itself reads `data/manuscripts.json`, which is **built from these files**:

    python3 tools/manuscripts/build.py

So to change the guide, edit the file here, then run the build. Don't edit `data/manuscripts.json` by hand: the build overwrites it.

## What a file contains

| Field | What it is |
|---|---|
| `id` | The file's name. |
| `anchor` | The link name used across the site (`msAbb.html#G`). |
| `label` | The siglum shown in the guide's first column. |
| `order` | The file's place in the list. |
| `status` | Empty, `lost` (known to have existed), `posited` (inferred by Liebermann), `not seen by Liebermann`, or `not in Liebermann` (known from Wormald only). |
| `display` | `true` if the entry appears in the guide. A few research files are kept but not shown. |
| `liebermann` | What Liebermann says (Gesetze I, pp. xviii–xlii): his `siglum`, his German `description_de`, the `shelfmark_as_given`, his `date`, the `laws` in it, the Gesetze I `page`, and the guide's English summary of his description (`notes`). |
| `wormald` | Patrick Wormald's research records, from *The Making of English Law* I (1999), ch. 4, pp. 162–263. There is one record for each part of the manuscript he treats separately (Nero A.i and Harley 55 have two). Each record keeps every field from the research spreadsheet (`Wormald-manuscripts.xlsx`, Nov. 2026): his siglum and shelfmark, date, origin, laws, other contents, the draft note (`overview`), where he supersedes Liebermann, his pages, a short checking quotation, doubts, and the checking notes. Page numbers are MEL's printed pages. |
| `others` | Other scholars' notes as the guide had them: O'Brien on the Instituta Cnuti, Robertson, and the editor's remarks. |
| `display_fields` | What the guide shows: the `shelfmark`; the `dates`, each with who says it and where; the `laws` and a `laws_note` where Wormald shows the contents differ; and the `notes`, each with `by` (Liebermann, Wormald, O'Brien, Editor), `ref`, and `kind: "correction"` where Wormald corrects Liebermann. |

## Tools that used to write `data/manuscripts.json` directly

Before Nov. 2026, `tools/lq`, `tools/latin-mss` and `tools/manuscripts/split.py` edited `data/manuscripts.json` directly. Their results are now in these files. Make any further changes here.
