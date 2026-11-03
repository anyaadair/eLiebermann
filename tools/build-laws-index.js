#!/usr/bin/env node
/*
 * Writes data/laws.json: one line per clause file in oe-laws/, for the Laws
 * page's list and search. Runs on every deploy (see
 * .github/workflows/static.yml), like tools/build-index.js. Needs no npm
 * packages.
 *
 *   node tools/build-laws-index.js
 */
const fs = require('fs');
const path = require('path');

const repo = path.resolve(__dirname, '..');
const dir = path.join(repo, 'oe-laws');

const decode = s => s
    .replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
const pick = (xml, re) => { const m = xml.match(re); return m ? decode(m[1]) : ''; };
const idno = (xml, type) => pick(xml, new RegExp('<idno type="' + type + '">([^<]*)</idno>'));
const ab = (xml, type, lang) => [...xml.matchAll(new RegExp('<ab type="' + type + '"([^>]*)>([\\s\\S]*?)</ab>', 'g'))]
    .filter(m => !lang || new RegExp('xml:lang="' + lang + '"').test(m[1]))
    .map(m => decode(m[2])).filter(Boolean);
// English translations, the modern editors' first and the English of Liebermann's German last.
const english = xml => {
    const all = [...xml.matchAll(/<ab type="translation"([^>]*)>([\s\S]*?)<\/ab>/g)]
        .filter(m => !/xml:lang="de"/.test(m[1]));
    return all.filter(m => !/ana="#fromGerman"/.test(m[1])).concat(all.filter(m => /ana="#fromGerman"/.test(m[1])))
        .map(m => decode(m[2])).filter(Boolean);
};
// The summary line of a clause on its law code page: Liebermann's first text
// (his leftmost column, i.e. the first manuscript he prints), or else the first
// edition's text; and Claude's English of Liebermann's German, or else the
// first other English translation. Each comes with a short label of its source.
const sigla = xml => {
    const out = {};
    for (const m of xml.matchAll(/<witness xml:id="([^"]+)"[^>]*>\s*<abbr>([\s\S]*?)<\/abbr>/g)) out[m[1]] = decode(m[2]);
    return out;
};
const editors = xml => {
    const out = {};
    for (const m of xml.matchAll(/<respStmt><resp>[^<]*<\/resp><name ref="#([^"]+)">([^<]*)<\/name><\/respStmt>/g)) out[m[1]] = decode(m[2]);
    return out;
};
const firstAb = (xml, types) => {
    for (const type of types) {
        for (const m of xml.matchAll(new RegExp('<ab type="' + type + '"([^>]*)>([\\s\\S]*?)</ab>', 'g'))) {
            const text = decode(m[2]);
            if (text) return { attrs: m[1], text };
        }
    }
    return null;
};
// An interlinear gloss (<seg type="glossed"> in Iud Dei IV, V): for the index, the Latin alone, and the gloss as an
// Old English text of its own (so that its words are found by a search)
const unGloss = xml => {
    if (!xml.includes('type="glossed"')) return xml;
    const gloss = [];
    const out = xml.replace(/<seg type="glossed"><seg type="base">([\s\S]*?)<\/seg><gloss xml:lang="ang">([\s\S]*?)<\/gloss><\/seg>/g, (m, base, gl) => { gloss.push(gl); return base; });
    return out.replace(/(<ab type="liebermannText" xml:lang="la"[^>]*>[\s\S]*?<\/ab>)/, '$1<ab type="supplementaryText" xml:lang="ang">' + gloss.join(' ') + '</ab>');
};
const attr = (attrs, name) => { const m = attrs.match(new RegExp(name + '="([^"]*)"')); return m ? m[1] : ''; };
const summary = xml => {
    const wits = sigla(xml), eds = editors(xml);
    const t = firstAb(xml, ['liebermannText', 'editionText', 'selectedText']);
    let oe = '', oeLabel = '', oeLang = '';
    if (t) {
        oe = t.text;
        oeLang = attr(t.attrs, 'xml:lang');
        const ed = attr(t.attrs, 'source').replace(/^#/, '');
        const sig = wits[attr(t.attrs, 'corresp').replace(/^#/, '')];
        oeLabel = (eds[ed] || ed || 'Unknown') + (sig ? (/^Q\b/.test(sig) ? ', ' : ', MS ') + sig : '');
    }
    const fromGerman = [...xml.matchAll(/<ab type="translation"([^>]*)>([\s\S]*?)<\/ab>/g)]
        .filter(m => /ana="#fromGerman"/.test(m[1])).map(m => decode(m[2])).filter(Boolean);
    let gloss = '', glossLabel = '';
    if (fromGerman.length) {
        gloss = fromGerman[0];
        glossLabel = 'LLM, from Liebermann’s German';
    } else {
        const other = [...xml.matchAll(/<ab type="translation"([^>]*)>([\s\S]*?)<\/ab>/g)]
            .filter(m => !/xml:lang="de"/.test(m[1])).find(m => decode(m[2]));
        if (other) {
            gloss = decode(other[2]);
            const ed = attr(other[1], 'source').replace(/^#/, '');
            // The LLM's crib of a text with no other translation (tools/add-crib.py)
            const crib = { '#fromLatin': 'Latin', '#fromOldEnglish': 'Old English', '#fromFrench': 'French' }[attr(other[1], 'ana')];
            glossLabel = crib ? 'LLM (' + crib + ')' : eds[ed] || ed || 'Translator not recorded';
        }
    }
    return { oe, oeLabel, oeLang, gloss, glossLabel };
};
// Liebermann prints the clause number at the head of his German in some codes ("2, 1. Wer einen …",
// "App. AGu. 1. Wenn …"), and the English crib copies it: left out of the summary when it is this clause's number.
const LEAD_NUMBER = /^\s*(?:[A-Z][A-Za-z.\s]{0,20}?\.\s*)?(\d+[a-z]?(?:\s*,\s*\d+[a-z]?)*)\.\s+/;
const withoutNumber = (text, clause) => {
    const m = LEAD_NUMBER.exec(text || '');
    return m && m[1].replace(/\s*,\s*/g, '.') === String(clause || '').trim() ? text.slice(m[0].length) : text;
};
const terms = (xml, n) => {
    const k = xml.match(new RegExp('<keywords n="' + n + '">([\\s\\S]*?)</keywords>'));
    return k ? [...k[1].matchAll(/<term>([^<]*)<\/term>/g)].map(m => decode(m[1])).filter(Boolean) : [];
};

const catalogue = JSON.parse(fs.readFileSync(path.join(dir, 'index.json'), 'utf8'));
// Full names of the law codes (oe-laws/codes.json, written by tools/laws-from-database.py).
const codesFile = path.join(dir, 'codes.json');
const codeNames = {};
if (fs.existsSync(codesFile)) JSON.parse(fs.readFileSync(codesFile, 'utf8')).forEach(c => { codeNames[c.code] = c.name; });
const clauses = catalogue.map(c => {
    const xml = unGloss(fs.readFileSync(path.join(dir, c.file), 'utf8'));
    const sum = summary(xml);
    return {
        id: c.id,
        citation: c.citation,
        code: c.code,
        anchor: c.anchor,
        clause: c.clause,
        law: c.legalText,
        name: codeNames[c.code] || c.legalText,
        page: c.page,
        date: pick(xml, /<note type="promulgation">([\s\S]*?)<\/note>/),
        offences: terms(xml, 'offence-legal-event'),
        people: terms(xml, 'people'),
        places: terms(xml, 'locations'),
        // The summary text and English for lists (see summary() above).
        oe: sum.oe,
        oeLabel: sum.oeLabel,
        oeLang: sum.oeLang,
        // the languages of the clause's original texts (ang, la, xno), for the language filter
        langs: [...new Set([...xml.matchAll(/<ab type="(?:liebermannText|editionText|selectedText|supplementaryText)"([^>]*)>/g)].map(m => attr(m[1], 'xml:lang')).filter(Boolean))],
        text: ab(xml, 'liebermannText').concat(ab(xml, 'editionText'), ab(xml, 'selectedText'), ab(xml, 'supplementaryText')).join(' '),
        gloss: withoutNumber(sum.gloss, c.clause),
        glossLabel: sum.glossLabel,
        en: english(xml).concat(ab(xml, 'secondTranslation'), ab(xml, 'supplementaryTranslation')).join(' '),
        row: c.sheetRow
    };
});   // in the order of oe-laws/index.json, which is the order of the spreadsheets

// The lists leave out the full texts (text) and all the English (en), which only the
// word search needs, and it reads data/laws-text.json: they kept only the English of a
// clause with no crib (gloss), shortened, for the line under its citation.
const listRow = c => {
    const { text, en, ...row } = c;
    if (!c.gloss && en) row.en = en.length > 300 ? en.slice(0, 300).replace(/\s+\S*$/, '') + '…' : en;
    return row;
};
fs.writeFileSync(path.join(repo, 'data', 'laws.json'),
    '[\n' + clauses.map(c => JSON.stringify(listRow(c))).join(',\n') + '\n]\n');
console.log(`data/laws.json: ${clauses.length} clauses`);

// data/laws-text.json: what the Laws page's word search looks in, clause by
// clause, each text kept apart so the reader can choose where to look. Loaded
// only when a word search is made. For each clause id:
//   t: the original texts, [language, label ("Liebermann, MS H", "Robertson"), text]
//   e: the English translations, [translator id, text] ("claude" is the English of Liebermann's German)
//   g: Liebermann's German translation
//   n: the notes (Liebermann's textual notes, Erklärungen and footnotes, in German and
//      English; the modern editors' and translators' notes): not in data/laws-text.json
//      but in data/laws-notes.json ({ id: notes }), loaded only for a search in the notes,
//      as they are half the text; data/laws-text/<prefix>.json has them together, one law code each.
const NOTE_TYPES = /^(?:liebermannNote|editorNote|translator|textual)$/;
const textIndex = {};
catalogue.forEach(c => {
    const xml = unGloss(fs.readFileSync(path.join(dir, c.file), 'utf8'));
    const wits = sigla(xml), eds = editors(xml);
    const t = [], e = [], g = [], n = [];
    for (const m of xml.matchAll(/<ab type="(liebermannText|editionText|selectedText|supplementaryText|translation|secondTranslation|supplementaryTranslation)"([^>]*)>([\s\S]*?)<\/ab>/g)) {
        const text = decode(m[3]);
        if (!text || /^[.\s…]+$/.test(text)) continue;
        const lang = attr(m[2], 'xml:lang');
        const src = attr(m[2], 'source').replace(/^#/, '');
        if (/ranslation$/.test(m[1])) {
            if (lang === 'de') g.push(text);
            else e.push([src === 'rabin-doml' ? 'rabin' : src, text]);
        } else {
            const sig = wits[attr(m[2], 'corresp').replace(/^#/, '')];
            t.push([lang, (eds[src] || src) + (sig ? (/^Q\b/.test(sig) ? ', ' : ', MS ') + sig : ''), text]);
        }
    }
    for (const m of xml.matchAll(/<note type="(\w+)"[^>]*>([\s\S]*?)<\/note>/g)) {
        if (!NOTE_TYPES.test(m[1])) continue;
        const text = decode(m[2].replace(/<bibl>[\s\S]*?<\/bibl>/g, ' ').replace(/<\/seg>/g, ' · </seg>'));
        if (text) n.push(text);
    }
    textIndex[c.id] = { t, e, g: g.join(' '), n: n.join(' ¶ ') };
});
{
    const main = {}, notes = {};
    Object.entries(textIndex).forEach(([id, { t, e, g, n }]) => { main[id] = { t, e, g }; if (n) notes[id] = n; });
    fs.writeFileSync(path.join(repo, 'data', 'laws-text.json'), JSON.stringify(main));
    fs.writeFileSync(path.join(repo, 'data', 'laws-notes.json'), JSON.stringify(notes));
}
console.log(`data/laws-text.json, data/laws-notes.json: ${Object.keys(textIndex).length} clauses`);

let codeSources = {};
// data/code-sources.json: for each law code page (lawcode.html), the manuscripts, editions,
// translations and studies its clause files name, as at the foot of a clause page, and which of
// them each name in the code's header stands for ("Whitelock, EHD p. 390" -> whitelock).
//   { "Abt": { sources: [{ id, name, type, bibl }], mss: [{ abbr, name, parts: [[text, href]] }],
//              link: { "Whitelock, EHD p. 390": "whitelock", … } } }
// bibl is the TEI of the reference (rendered by the page); its page is the first page of the code
// in that work, or "pp. first–last" across the code's clauses.
{
    const readJson = f => { try { return JSON.parse(fs.readFileSync(path.join(repo, 'data', f), 'utf8')); } catch (e) { return []; } };
    // Manuscript sigla to the lists of manuscripts and law codes, as on the clause pages (law.html siglumLinks)
    const sigKey = s => s.replace(/[\s.]/g, '');
    const siglumIndex = {};
    readJson('markLaw.json').forEach(r => { if (r['Gesetze Text']) siglumIndex[sigKey(r['Gesetze Text'])] = 'lawAbb.html#' + encodeURIComponent(r.Anchor); });
    readJson('manuscripts.json').forEach(r => { if (r['Gesetze Text']) siglumIndex[sigKey(r['Gesetze Text'])] = 'msAbb.html#' + encodeURIComponent(r.Anchor); });
    const ALIASES = { 'InstCn': 'InCn' };
    const siglumHref = sig => { let k = sigKey(sig); k = ALIASES[k] || k; return siglumIndex[k] || siglumIndex[sigKey(sig.replace(/\s*\([^)]*\)\s*$/, ''))] || ''; };
    const siglumParts = sig => {
        const parts = sig.split(/,\s*/);
        const linkable = parts.length > 1 && parts.every(p => siglumHref(p)) ? parts : [sig];
        return linkable.map(p => [p, siglumHref(p) || null]);
    };
    // Names for works a clause file lists without naming (as law.html SOURCE_NAMES)
    const SOURCE_NAMES = { liebermann: 'Liebermann', 'liebermann-erkl': 'Liebermann', 'wormald-mel': 'Wormald', 'wormald-ppmel': 'Wormald', 'rabin-doml': 'Rabin', 'whitelock-cs': 'Whitelock', 'jurasinski-and-oliver': 'Jurasinski and Oliver' };
    const pageNo = s => /^\d+$/.test(s) ? parseInt(s, 10) : null;
    const byCode = {};
    catalogue.forEach(c => {
        const xml = unGloss(fs.readFileSync(path.join(dir, c.file), 'utf8'));
        const k = byCode[c.code] = byCode[c.code] || { sources: new Map(), mss: new Map(), dates: {} };
        const names = editors(xml);
        for (const m of xml.matchAll(/<bibl xml:id="([^"]+)"([^>]*)>([\s\S]*?)<\/bibl>/g)) {
            const [, id, attrs, inner] = m;
            // the LLM's English of Liebermann's German only where a text is from it (not for notes alone)
            if (id === 'claude' && !/<ab [^>]*source="#claude"/.test(xml)) continue;
            const page = (inner.match(/<biblScope unit="page">([^<]*)<\/biblScope>/) || [])[1] || '';
            const s = k.sources.get(id);
            if (!s) k.sources.set(id, { id, name: id === 'claude' ? 'LLM' : names[id] || SOURCE_NAMES[id] || id.charAt(0).toUpperCase() + id.slice(1),
                type: attr(attrs, 'type'), bibl: inner.trim(), first: page, last: page });
            else if (page) { if (!s.first) s.first = page; s.last = page; }
        }
        // Each manuscript's part on these pages: "text" if a text on a clause page is from it (corresp on an
        // <ab>), else "notes" if Liebermann's notes cite it; one the files only list is left out.
        const withText = new Set();
        for (const m of xml.matchAll(/<ab [^>]*corresp="([^"]+)"/g)) m[1].split(/\s+/).forEach(x => withText.add(x.replace(/^#/, '')));
        // (his German translation counts too: lq, the lost source of Ld and Quadr., is cited there)
        const notesText = [...xml.matchAll(/<note type="liebermannNote"[^>]*>[\s\S]*?<seg type="original"[^>]*>([\s\S]*?)<\/seg>/g),
                           ...xml.matchAll(/<ab type="translation" xml:lang="de"[^>]*>([\s\S]*?)<\/ab>/g)].map(m => m[1].replace(/<[^>]+>/g, ' ')).join(' ');
        for (const m of xml.matchAll(/<witness xml:id="([^"]+)"[^>]*>([\s\S]*?)<\/witness>/g)) {
            const abbr = decode((m[2].match(/<abbr>([\s\S]*?)<\/abbr>/) || [])[1] || m[2]);
            const name = decode((m[2].match(/<note(?! type="sigla")[^>]*>([\s\S]*?)<\/note>/) || [])[1] || '');
            const sigla = decode((m[2].match(/<note type="sigla">([\s\S]*?)<\/note>/) || [])[1] || '').split(/\s+/).filter(Boolean).map(x => [x, siglumHref(x) || null]);
            const base = abbr.replace(/\s*\(.*$/, '').trim();
            const role = withText.has(m[1]) ? 'text'
                : base && new RegExp('(^|[^\\p{L}])' + base.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![\\p{L}])', 'u').test(notesText) ? 'notes' : '';
            if (!k.mss.has(abbr)) k.mss.set(abbr, { abbr, name, parts: siglumParts(abbr), role, sigla });
            else {
                const x = k.mss.get(abbr);
                if (!x.name && name) x.name = name;
                if (role === 'text' || (role === 'notes' && !x.role)) x.role = role;
            }
        }
        // "Whitelock, EHD p. 390" in the dates: the clause files say which work (source="#whitelock" n="EHD p. 390")
        for (const m of xml.matchAll(/<(?:date|placeName) source="([^"]*)"(?: n="([^"]*)")?/g)) {
            const ids = m[1].split(/\s+/).map(x => x.replace(/^#/, '')).filter(Boolean);
            const pages = (m[2] || '').split('|');
            ids.forEach((id, j) => {
                const s = k.sources.get(id);
                if (s) k.dates[s.name.split(',')[0] + (pages[j] ? ', ' + pages[j] : '')] = id;
            });
        }
    });
    // every work any clause file lists, with its reference as first given (no pages)
    const allSources = [];
    Object.values(byCode).forEach(k => k.sources.forEach(src => { if (!allSources.some(x => x.id === src.id))
        allSources.push({ id: src.id, name: src.name, type: src.type, bibl: src.bibl.replace(/,?\s*pp?\. <biblScope unit="page">[^<]*<\/biblScope>/, '') }); }));
    const codeList = fs.existsSync(codesFile) ? JSON.parse(fs.readFileSync(codesFile, 'utf8')) : [];
    const out = {}, unlinked = [];
    codeList.forEach(code => {
        const k = byCode[code.code];
        if (!k) return;
        const sources = [...k.sources.values()].map(s => {
            let bibl = s.bibl;
            // the pages the code takes up in the work, where they differ
            const a = pageNo(s.first), b = pageNo(s.last);
            if (a !== null && b !== null && a !== b) bibl = bibl.replace(/\bp\. (<biblScope unit="page">)[^<]*(<\/biblScope>)/, `pp. $1${Math.min(a, b)}–${Math.max(a, b)}$2`);
            return { id: s.id, name: s.name, type: s.type, bibl };
        });
        // Each name in the header: the dates, places and titles ("Whitelock, EHD p. 390") and the editions.
        const labels = new Set(['Liebermann'].concat(code.editors || []));
        [code.dates, code.places, code.titles].forEach(list => (list || []).forEach(([, ns]) => (ns || []).forEach(n => labels.add(n))));
        const link = {};
        const match = (label, pool) => {
            const surname = label.split(',')[0].trim();
            let cands = pool.filter(s => s.name.split(',')[0] === surname || s.id === surname.toLowerCase().replace(/\s+/g, '-'));
            // the work named after the surname, without its pages: "EHD", "MEL", "Political Writings", "I" (a volume)
            const work = label.slice(surname.length).replace(/^\s*,\s*/, '').replace(/\s*\bpp?\.\s*\S+$/, '').trim();
            if (work) {
                const fits = s => {
                    const text = decode(s.bibl);
                    if (/^[IVX]+$/.test(work)) return new RegExp('unit="volume">' + ({ I: 1, II: 2, III: 3 }[work] || 0) + '<').test(s.bibl);
                    if (text.toLowerCase().includes(work.toLowerCase())) return true;
                    // an abbreviation: the capitals of the title, in order ("MEL": The Making of English Law)
                    const title = decode((s.bibl.match(/<title>([\s\S]*?)<\/title>/) || [])[1] || '');
                    const caps = title.replace(/[^A-Z]/g, '');
                    let i = 0; for (const ch of caps) if (ch === work[i]) i++;
                    return /^[A-Z]{2,}$/.test(work) && i === work.length;
                };
                const fitting = cands.filter(fits);
                // a work named that none of the sources is: better no link than the wrong book
                if (fitting.length) cands = fitting; else if (cands.length > 1 || !/^[IVX]+$/.test(work)) cands = cands.filter(s => cands.length === 1 && fits(s));
            }
            if (cands.length > 1) cands = cands.filter(s => s.type === 'edition' || s.type === 'translation').concat(cands.filter(s => s.type !== 'edition' && s.type !== 'translation'));
            return cands[0] || null;
        };
        labels.forEach(label => {
            if (k.dates[label]) { link[label] = k.dates[label]; return; }
            let src = match(label, sources);
            // a work the code's clause files don't list, but another code's do (Rabin, Political Writings): borrowed
            if (!src && (src = match(label, allSources))) sources.push(src);
            if (src) link[label] = src.id; else unlinked.push(code.code + ': ' + label);
        });
        // a manuscript cited in the notes that is already named in a text's label ("Fl, Ox") is not listed twice
        const inText = new Set([...k.mss.values()].filter(m => m.role === 'text').flatMap(m => m.abbr.split(/,\s*/).map(x => x.replace(/\s*\(.*$/, '').trim())));
        out[code.code] = { sources, mss: [...k.mss.values()].filter(m => m.role === 'text' || (m.role === 'notes' && !inText.has(m.abbr.replace(/\s*\(.*$/, '').trim()))), link };
    });
    codeSources = out;
    fs.writeFileSync(path.join(repo, 'data', 'code-sources.json'), JSON.stringify(out));
    console.log(`data/code-sources.json: ${Object.keys(out).length} law codes` + (unlinked.length ? `; names with no reference in the clause files: ${unlinked.join('; ')}` : ''));
}

// One law code at a time, so a page loads only the code it shows. Each file is named by the
// start of its clause ids, before the "_" (Abt_1 -> Abt, ECfRetr_Inscr -> ECfRetr), so that
// a clause page can find its code's file from the clause id alone; a code whose ids start
// in more than one way (Af Rb: Rubric-List_, Rubrics-Af_) has the same file under each.
//   data/laws/<prefix>.json       the law code page (lawcode.html): { rows: its rows of
//                                 data/laws.json, sources: its data/code-sources.json }
//   data/clauses/<prefix>.json    a clause page (law.html): { rows: its rows of
//                                 oe-laws/index.json, brief: { id: the opening of the text,
//                                 for the neighbouring clauses }, dict: { id: [[entry id,
//                                 headword, language]] }, the dictionary entries citing each
//                                 clause, from data/dict-citations.json (tools/build-index.js,
//                                 which runs first; null if it has not) }
//   data/laws-text/<prefix>.json  the word search on the law code page: its part of
//                                 data/laws-text.json, with the notes (n)
{
    const prefixOf = id => id.split('_')[0];
    let dictCites = null;
    try { dictCites = JSON.parse(fs.readFileSync(path.join(repo, 'data', 'dict-citations.json'), 'utf8')); } catch (e) { /* not built */ }
    const citing = {};
    if (dictCites) Object.entries(dictCites).forEach(([entry, [hw, lang, ids]]) => ids.forEach(id => (citing[id] = citing[id] || []).push([entry, hw, lang])));
    const codes = new Map();
    catalogue.forEach((c, i) => {
        const k = codes.get(c.code) || codes.set(c.code, { prefixes: new Set(), cat: [], rows: [] }).get(c.code);
        const p = prefixOf(c.id);
        if (!/^[A-Za-z0-9-]+$/.test(p)) throw new Error(`oe-laws/index.json: clause id ${c.id} does not make a file name`);
        k.prefixes.add(p);
        k.cat.push(c);
        k.rows.push(clauses[i]);
    });
    const owner = {};
    codes.forEach((k, code) => k.prefixes.forEach(p => {
        if (owner[p] && owner[p] !== code) throw new Error(`oe-laws/index.json: clause ids starting ${p}_ are in two law codes, ${owner[p]} and ${code}`);
        owner[p] = code;
    }));
    ['laws', 'clauses', 'laws-text'].forEach(d => {
        const full = path.join(repo, 'data', d);
        fs.rmSync(full, { recursive: true, force: true });
        fs.mkdirSync(full);
    });
    const brief = oe => oe.length > 70 ? oe.slice(0, 70).replace(/\s+\S*$/, '') + '…' : oe;
    codes.forEach((k, code) => {
        const laws = JSON.stringify({ rows: k.rows.map(listRow), sources: codeSources[code] || null });
        const nav = JSON.stringify({
            rows: k.cat.map(c => {
                const row = { id: c.id, file: c.file, citation: c.citation, code: c.code, clause: c.clause, legalText: c.legalText, page: c.page };
                if (c.parts) row.parts = c.parts;
                return row;
            }),
            brief: Object.fromEntries(k.rows.map(r => [r.id, brief(r.oe)])),
            dict: dictCites ? Object.fromEntries(k.cat.filter(c => citing[c.id]).map(c => [c.id, citing[c.id]])) : null
        });
        const text = JSON.stringify(Object.fromEntries(k.cat.map(c => [c.id, textIndex[c.id]])));
        k.prefixes.forEach(p => {
            fs.writeFileSync(path.join(repo, 'data', 'laws', p + '.json'), laws);
            fs.writeFileSync(path.join(repo, 'data', 'clauses', p + '.json'), nav);
            fs.writeFileSync(path.join(repo, 'data', 'laws-text', p + '.json'), text);
        });
    });
    console.log(`data/laws/, data/clauses/, data/laws-text/: ${codes.size} law codes, ${Object.keys(owner).length} files each` + (dictCites ? '' : ' (no data/dict-citations.json: run tools/build-index.js first)'));
}
