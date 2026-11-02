# Brief: English crib of the ritual texts in Liebermann's *Gesetze der Angelsachsen*

You are making an English **crib** (a reading aid) of texts Liebermann prints in *Die Gesetze der Angelsachsen* I (1903): excommunication formulas (Excom), ordeal rituals (Iudicium Dei), and the ritual for the judicial duel (Duel). Most are Latin; some passages are Old English (glosses or versions of the Latin, mostly in the ordeal texts). The crib will be shown on each clause page of the eLiebermann website, labelled as made with an LLM (Claude, 2026), beside the original.

## Input
Your batch file is a JSON list, in reading order. Each item:
`{"key": "IudDeiIV_2#0", "citation": "Iud Dei IV 2", "lang": "la", "ms": "Du", "text": "…"}`
- `key` = clause file id + "#" + the number of the text within that clause. Several texts in one clause (same citation, different `ms`) are parallel versions, often a Latin text and its Old English gloss or version: translate each one separately, each faithful to its own wording.
- `lang` is the database's tag and is sometimes wrong (a Latin rubric tagged "ang"). Translate the text in whatever language it is actually in, and report the real language in your output.
- The texts are cut into Liebermann's clauses, often in the middle of a sentence. Translate exactly the portion given: do not complete or anticipate a sentence that runs on into the next item, and do not repeat the end of the previous item. Read the neighbouring items so the sense and construction run on correctly.

## How to translate
- **Semi-literal but accurate.** Keep close to the original's word order and structure where English allows, so a reader can follow the Latin (or Old English) word by word, but write correct, readable English. Do not paraphrase or modernise the theology.
- **Use the established English of Anglo-Latin legal, liturgical and canon-law formulae**, consistently across the whole batch. For example:
  - *Exorcizo te, creatura aquae* → "I exorcise you, creature of water"; *Adiuro te* → "I adjure you"; *coniuro* → "I conjure".
  - *in nomine Patris et Filii et Spiritus sancti* → "in the name of the Father and of the Son and of the Holy Spirit".
  - *Ex auctoritate Dei omnipotentis* → "By the authority of God almighty".
  - *excommunicamus et anathematizamus* → "we excommunicate and anathematise"; *a liminibus sanctae matris ecclesiae sequestramus* → "we separate him from the thresholds of holy mother Church"; *maledictus sit* → "may he be cursed"; *anathema sit* → "let him be anathema"; *nisi resipuerit / ad satisfactionem venerit* → "unless he comes to his senses / comes to make amends (satisfaction)".
  - *famulus tuus* → "your servant"; *hic homo*, *iste* → "this man"; *ille*, *N.* standing for a name → "N.".
  - *iudicium Dei* → "the judgment of God", "the ordeal" only where the text clearly means the procedure; *purgatio* → "purgation"; *reus* → "guilty"; *innocens* → "innocent"; *furtum* → "theft"; *homicidium* → "homicide".
  - Collect endings: *Per Dominum nostrum …* or just *Per* → "Through [our Lord …]" (keep it as short as the original: *Per* alone → "Through …").
  - *Kyrie eleison* → "Kyrie eleison (Lord, have mercy)" the first time in a text, then "Kyrie eleison".
  - Psalms, antiphons and other chants named by their opening words: give the Latin incipit in italics, then the English and the psalm number in the Vulgate numbering: "the psalm <i>Deus in nomine tuo</i> ('Save me, O God, by thy name', Ps. 53)". Do this once per text; after that the Latin incipit alone is enough.
  - Biblical quotations: translate from the Latin as given (do not substitute a Bible version), close to Douay-Rheims in wording.
- Address God and the elements as "you" (not "thou").
- Keep Liebermann's square brackets [ ] (his additions) around the corresponding English words. Keep "etc." and "N." as they are. Where the text is corrupt or the construction genuinely unclear, give the likeliest sense and add "[?]" after the doubtful word; mention it in your final reply.
- Old English: translate the Old English itself (not the Latin it glosses), as literally as good English allows. Report the language as "ang".
- Anglo-Norman French, if any: report as "xno".
- Output plain text. The only markup allowed is `<i>…</i>` for Latin (or other foreign) words left untranslated, such as chant incipits.

## Output
Write a JSON object to the output file named in your task: `{ key: {"en": "English crib", "lang": "la" | "ang" | "xno"} }` with an entry for **every** key in your batch. Write the file as you go (every 30 items or so) so work is not lost. When finished, reply only with: the number of items written, and a short list of places where the text was doubtful or where you made a choice the editor should know about.
