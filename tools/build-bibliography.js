#!/usr/bin/env node
/*
 * Writes data/bibliography-uses.json for the Bibliography page (bibliography.html):
 *
 *   works: for each edition, translation or study that the law clause files list
 *          (<listBibl><bibl xml:id="…">), how many clause pages use it and in which
 *          law codes: { "attenborough": { clauses: 696, codes: { "Abt": 107, … } } }
 *   cited: for each work in Liebermann's own citations (data/bibliography.json, linked
 *          from entries as target="bib:Anchor"), the dictionary entries that cite it:
 *          { "CitASC": [["aelmesfeoh", "ælmesfeoh", "ang"], …] }
 *
 * Runs on every deploy after tools/build-index.js and tools/build-laws-index.js (it
 * reads data/laws.json and data/entry-order.json, which they write). Needs no npm packages.
 *
 *   node tools/build-bibliography.js
 */
const fs = require('fs');
const path = require('path');

const repo = path.resolve(__dirname, '..');
const read = f => JSON.parse(fs.readFileSync(path.join(repo, f), 'utf8'));

// clause id → code as printed ("II Em")
const codeOf = {};
read('data/laws.json').forEach(r => { codeOf[r.id] = r.code; });

const works = {};
const lawDir = path.join(repo, 'oe-laws');
fs.readdirSync(lawDir).filter(f => f.endsWith('.xml')).forEach(f => {
    const xml = fs.readFileSync(path.join(lawDir, f), 'utf8');
    const id = f.replace(/\.xml$/, '');
    const code = codeOf[id] || id.replace(/_.*/, '');
    const seen = new Set();
    for (const list of xml.matchAll(/<listBibl[\s\S]*?<\/listBibl>/g)) {
        for (const m of list[0].matchAll(/<bibl\b[^>]*xml:id="([^"]+)"/g)) seen.add(m[1]);
    }
    seen.forEach(b => {
        const w = works[b] || (works[b] = { clauses: 0, codes: {} });
        w.clauses++;
        w.codes[code] = (w.codes[code] || 0) + 1;
    });
});

const hw = {};
read('data/entry-order.json').forEach(r => { hw[r[0]] = [r[1], r[2]]; });
const cited = {};
const entryDir = path.join(repo, 'entries');
fs.readdirSync(entryDir).filter(f => f.endsWith('.xml')).forEach(f => {
    const xml = fs.readFileSync(path.join(entryDir, f), 'utf8');
    const id = f.replace(/\.xml$/, '');
    new Set([...xml.matchAll(/target="bib:([^"]+)"/g)].map(m => m[1])).forEach(a => {
        (cited[a] || (cited[a] = [])).push([id, ...(hw[id] || [id, 'ang'])]);
    });
});

fs.writeFileSync(path.join(repo, 'data', 'bibliography-uses.json'), JSON.stringify({ works, cited }));
console.log(`data/bibliography-uses.json: ${Object.keys(works).length} works on the clause pages, ${Object.keys(cited).length} of Liebermann's citations`);
