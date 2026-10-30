#!/usr/bin/env node
/*
 * Writes data/entries.json: one line per dictionary entry, for the
 * Dictionary page's list and search. Runs on every deploy (see
 * .github/workflows/static.yml), so entries added to entries/ appear in the
 * list without anything else to update. Needs no npm packages.
 *
 *   node tools/build-index.js
 */
const fs = require('fs');
const path = require('path');

const repo = path.resolve(__dirname, '..');
const dir = path.join(repo, 'entries');

const decode = s => s
    .replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();

const pick = (xml, re) => { const m = xml.match(re); return m ? m[1] : ''; };

// Other spellings Liebermann gives after a headword ("acquietare, adq~"), written
// out by hand in data/headword-variants.json, so a search finds either.
let variants = {};
try { variants = JSON.parse(fs.readFileSync(path.join(repo, 'data', 'headword-variants.json'), 'utf8')); } catch (e) { /* none */ }

const entries = fs.readdirSync(dir)
    .filter(f => f.endsWith('.xml'))
    .map(f => {
        const xml = fs.readFileSync(path.join(dir, f), 'utf8');
        const scrap = pick(xml, /<dictScrap[^>]*>([\s\S]*?)<\/dictScrap>/);
        const hw = decode(pick(xml, /<orth>([\s\S]*?)<\/orth>/));
        const text = decode(scrap);
        // Short summary for the list: the start of Liebermann's text after the
        // headword. (An English translation, if any, is not shown for now.)
        const t = text.replace(/^[LF]\s+/, '');
        const at = t.indexOf(hw);
        const rest = (at >= 0 ? t.slice(at + hw.length) : t).replace(/^[\s,.;:]+/, '');
        const snippet = rest.length > 110 ? rest.slice(0, 110).replace(/\s+\S*$/, '') + '…' : rest;
        return {
            id: f.replace(/\.xml$/, ''),
            hw,
            lang: pick(xml, /<entry[^>]*xml:lang="([^"]+)"/) || 'ang',
            page: pick(xml, /<biblScope unit="page">([^<]*)<\/biblScope>/),
            gloss: snippet,
            // a spelling, not a word (<usg type="dom">spelling</usg>): badged in the list
            spelling: /<usg type="dom">spelling<\/usg>/.test(xml),
            // an entry that only sends the reader to another headword (type="xref"): badged too
            xref: /<entry[^>]*type="xref"/.test(xml),
            // other spellings to search under (data/headword-variants.json)
            also: Array.isArray(variants[f.replace(/\.xml$/, '')]) ? variants[f.replace(/\.xml$/, '')] : undefined,
            text
        };
    })
    .sort((a, b) => a.id.localeCompare(b.id));

fs.mkdirSync(path.join(repo, 'data'), { recursive: true });
fs.writeFileSync(path.join(repo, 'data', 'entries.json'),
    '[\n' + entries.map(e => JSON.stringify(e)).join(',\n') + '\n]\n');
console.log(`data/entries.json: ${entries.length} entries`);

// A small list of every entry's id, headword and language (and 1 for a
// spelling entry, and then any other spellings to search under), for the previous and next links and the sidebar of each
// entry page (the page sorts it into Liebermann's order, as the Dictionary
// page does), and the sidebar's headword search.
fs.writeFileSync(path.join(repo, 'data', 'entry-order.json'),
    '[\n' + entries.map(e => JSON.stringify(e.also ? [e.id, e.hw, e.lang, e.spelling ? 1 : 0, e.also] : e.spelling ? [e.id, e.hw, e.lang, 1] : [e.id, e.hw, e.lang])).join(',\n') + '\n]\n');
console.log(`data/entry-order.json: ${entries.length} entries`);

// data/dict-citations.json: which law clauses each dictionary entry cites (its
// citation list, clause links only), for the Laws page's "Dictionary word" search
// and the "Dictionary entries citing this clause" list on each clause page.
// { entryId: [headword, language, [clause ids]] }
const cites = {};
fs.readdirSync(dir).filter(f => f.endsWith('.xml')).forEach(f => {
    const xml = fs.readFileSync(path.join(dir, f), 'utf8');
    const ids = [...new Set([...xml.matchAll(/<xr type="lawCode"[^>]*><ref target="clause:([^"]+)"/g)].map(m => m[1]))];
    if (!ids.length) return;
    const id = f.replace(/\.xml$/, '');
    const e = entries.find(x => x.id === id);
    cites[id] = [e ? e.hw : id, e ? e.lang : 'ang', ids];
});
fs.writeFileSync(path.join(repo, 'data', 'dict-citations.json'), JSON.stringify(cites));
console.log(`data/dict-citations.json: ${Object.keys(cites).length} entries`);
