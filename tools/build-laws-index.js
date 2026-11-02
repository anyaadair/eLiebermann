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
            glossLabel = eds[ed] || ed || 'Translator not recorded';
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
    const xml = fs.readFileSync(path.join(dir, c.file), 'utf8');
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

fs.writeFileSync(path.join(repo, 'data', 'laws.json'),
    '[\n' + clauses.map(c => JSON.stringify(c)).join(',\n') + '\n]\n');
console.log(`data/laws.json: ${clauses.length} clauses`);

// data/laws-brief.json: every clause's id, law code, citation and the opening of its
// text, for the neighbouring clauses in the sidebar of a clause page.
const brief = clauses.map(c => [c.id, c.code, c.citation, c.oe.length > 70 ? c.oe.slice(0, 70).replace(/\s+\S*$/, '') + '…' : c.oe]);
fs.writeFileSync(path.join(repo, 'data', 'laws-brief.json'), JSON.stringify(brief));
console.log(`data/laws-brief.json: ${brief.length} clauses`);

// data/laws-text.json: what the Laws page's word search looks in, clause by
// clause, each text kept apart so the reader can choose where to look. Loaded
// only when a word search is made. For each clause id:
//   t: the original texts, [language, label ("Liebermann, MS H", "Robertson"), text]
//   e: the English translations, [translator id, text] ("claude" is the English of Liebermann's German)
//   g: Liebermann's German translation
//   n: the notes (Liebermann's textual notes, Erklärungen and footnotes, in German and
//      English; the modern editors' and translators' notes)
const NOTE_TYPES = /^(?:liebermannNote|editorNote|translator|textual)$/;
const textIndex = {};
catalogue.forEach(c => {
    const xml = fs.readFileSync(path.join(dir, c.file), 'utf8');
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
fs.writeFileSync(path.join(repo, 'data', 'laws-text.json'), JSON.stringify(textIndex));
console.log(`data/laws-text.json: ${Object.keys(textIndex).length} clauses`);

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
    const ALIASES = { 'InstCn': 'In(Cn)' };
    const siglumHref = sig => { let k = sigKey(sig); k = ALIASES[k] || k; return siglumIndex[k] || siglumIndex[sigKey(sig.replace(/\s*\([^)]*\)\s*$/, ''))] || ''; };
    const siglumParts = sig => {
        const parts = sig.split(/,\s*/);
        const linkable = parts.length > 1 && parts.every(p => siglumHref(p)) ? parts : [sig];
        return linkable.map(p => [p, siglumHref(p) || null]);
    };
    // Names for works a clause file lists without naming (as law.html SOURCE_NAMES)
    const SOURCE_NAMES = { liebermann: 'Liebermann', 'liebermann-erkl': 'Liebermann', 'wormald-mel': 'Wormald', 'wormald-ppmel': 'Wormald', 'rabin-doml': 'Rabin', 'whitelock-cs': 'Whitelock' };
    const pageNo = s => /^\d+$/.test(s) ? parseInt(s, 10) : null;
    const byCode = {};
    catalogue.forEach(c => {
        const xml = fs.readFileSync(path.join(dir, c.file), 'utf8');
        const k = byCode[c.code] = byCode[c.code] || { sources: new Map(), mss: new Map(), dates: {} };
        const names = editors(xml);
        for (const m of xml.matchAll(/<bibl xml:id="([^"]+)"([^>]*)>([\s\S]*?)<\/bibl>/g)) {
            const [, id, attrs, inner] = m;
            const page = (inner.match(/<biblScope unit="page">([^<]*)<\/biblScope>/) || [])[1] || '';
            const s = k.sources.get(id);
            if (!s) k.sources.set(id, { id, name: id === 'claude' ? 'LLM' : names[id] || SOURCE_NAMES[id] || id.charAt(0).toUpperCase() + id.slice(1),
                type: attr(attrs, 'type'), bibl: inner.trim(), first: page, last: page });
            else if (page) { if (!s.first) s.first = page; s.last = page; }
        }
        for (const m of xml.matchAll(/<witness xml:id="([^"]+)"[^>]*>([\s\S]*?)<\/witness>/g)) {
            const abbr = decode((m[2].match(/<abbr>([\s\S]*?)<\/abbr>/) || [])[1] || m[2]);
            const name = decode((m[2].match(/<note[^>]*>([\s\S]*?)<\/note>/) || [])[1] || '');
            if (!k.mss.has(abbr)) k.mss.set(abbr, { abbr, name, parts: siglumParts(abbr) });
            else if (!k.mss.get(abbr).name && name) k.mss.get(abbr).name = name;
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
        out[code.code] = { sources, mss: [...k.mss.values()], link };
    });
    fs.writeFileSync(path.join(repo, 'data', 'code-sources.json'), JSON.stringify(out));
    console.log(`data/code-sources.json: ${Object.keys(out).length} law codes` + (unlinked.length ? `; names with no reference in the clause files: ${unlinked.join('; ')}` : ''));
}
