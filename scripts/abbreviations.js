/*
 * eLiebermann: the Guides pages. The lists of law codes, manuscripts, grammatical
 * terms and authors and works cited (lawAbb.html, msAbb.html, gramAbb.html and
 * bibAbb.html), and How to Read a Dictionary Entry (guide.html).
 *
 * Each page has the Laws pages' layout: a panel on the left (<aside id="guide-panel">,
 * filled in here) and the page on the right. A list page names its data file and kind on
 * #content-container: data-source="data/markLaw.json" data-kind="law" | "ms" | "gram" | "works".
 * guide.html has no list: its panel finds words on the page and lists its sections.
 *
 * Rows with the same Anchor are spellings of one abbreviation; entry pages link to the
 * Anchor (lawAbb.html#Ine, gramAbb.html#Gegensatz, bibAbb.html#CitASC).
 */
(function () {
    'use strict';
    const root = () => window.SITE_ROOT || '';
    const $ = id => document.getElementById(id);
    const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    // titles in <i>…</i> (data/bibliography.json): escaped, then only the italics let through
    const italics = s => esc(s).replace(/&lt;i&gt;/g, '<i>').replace(/&lt;\/i&gt;/g, '</i>');
    const plain = s => String(s == null ? '' : s).replace(/<[^>]+>/g, '');
    // for searching: lower case, no accents; æ = ae, þ/ð = th
    const fold = s => plain(s).toLowerCase().replace(/[æǣǽ]/g, 'ae').replace(/[þðꝥ]/g, 'th').replace(/ß/g, 'ss')
        .normalize('NFD').replace(/[̀-ͯ]/g, '');
    // an abbreviation as typed: "II As", "IIAs" and "ii as." are the same
    const squash = s => fold(s).replace(/[\s.]+/g, '');

    const GUIDES = [
        ['guide.html', 'How to Read a Dictionary Entry'],
        ['lawAbb.html', 'Law Codes'],
        ['msAbb.html', 'Manuscripts'],
        ['gramAbb.html', 'Grammatical Terms and Abbreviations'],
        ['bibAbb.html', 'Authors and Works Cited'],
        ['forewords.html', 'Liebermann’s Forewords']
    ];

    // What each list shows and searches.
    const KINDS = {
        law: { noun: ['law code', 'law codes'], field: 'Gesetze Text', label: 'Abbreviation',
            fields: ['Gesetze Text', 'German Expansion', 'English Translation', 'Notes: Information & Editions'],
            // Liebermann's order ignores the numeral of a code: I As, II As … under A
            letter: r => (String(r['Gesetze Text']).replace(/^(?:[IVX]+a?)\s+/, '').match(/\p{L}/u) || ['#'])[0].toUpperCase() },
        ms: { noun: ['manuscript', 'manuscripts'], field: 'Gesetze Text', label: 'Siglum',
            fields: ['Gesetze Text', 'German Expansion', 'English Translation', 'Date (Liebermann)', 'Laws in it', 'Notes'],
            letter: r => (String(r['Gesetze Text']).match(/\p{L}/u) || ['#'])[0].toUpperCase() },
        gram: { noun: ['term', 'terms'], field: 'Gesetze Text', label: 'Term',
            fields: ['Gesetze Text', 'German Expansion', 'Modern German', 'English Translation', 'Notes: Grammatical'],
            letter: r => /^\d/.test(String(r['Gesetze Text']).trim()) ? '#' : (fold(r['Gesetze Text']).match(/[a-z]/) || ['#'])[0].toUpperCase() },
        works: { noun: ['work', 'works'], field: 'Short Title', label: 'Author or title',
            fields: ['Short Title', 'Full Citation', 'Gesetze Text', 'Notes'],
            letter: r => (fold(r['Short Title']).match(/[a-z]/) || ['#'])[0].toUpperCase() }
    };

    const state = { q: '', where: 'start', show: 'all', open: false };
    let kind, K, groups = [], container;

    // ---------------------------------------------------------------- the panel
    function panel(listPage) {
        const aside = $('guide-panel');
        if (!aside) return;
        const here = location.pathname.split('/').pop() || 'guide.html';
        const title = (GUIDES.find(g => g[0] === here) || [, document.title.split(' · ')[0]])[1];
        aside.innerHTML = `
            <h2 class="laws-panel__title">${esc(title)}</h2>
            <p class="panel-help panel-intro" id="gp-count">&nbsp;</p>
            <div class="panel-sec">
                <label class="sidebar-label" for="gp-q">${listPage ? 'Search this list' : 'Find on this page'}</label>
                <input type="search" id="gp-q" autocomplete="off" placeholder="${listPage ? esc(listPage.placeholder) : 'e.g. semicolon, Seite, G 2'}">
                ${listPage ? `
                <div class="panel-sub">Look in</div>
                <div class="kind-pills kind-pills--small" id="gp-where" role="group" aria-label="Where to look">
                    <button type="button" class="kind-pill" data-where="start" aria-pressed="true">${esc(K.label)}</button>
                    <button type="button" class="kind-pill" data-where="all" aria-pressed="false">Everything</button>
                </div>
                <p class="panel-help" id="gp-help"></p>` : `
                <div class="find-status" id="gp-status" hidden>
                    <span id="gp-found" aria-live="polite"></span>
                    <button type="button" class="find-step" id="gp-prev" title="Previous match" aria-label="Previous match">↑</button>
                    <button type="button" class="find-step" id="gp-next" title="Next match" aria-label="Next match">↓</button>
                </div>
                <p class="panel-help">Marks the words on the page; Enter or ↓ goes to the next.</p>`}
            </div>
            ${listPage && listPage.filters ? `<div class="panel-sec">${listPage.filters}</div>` : ''}
            <div class="panel-sec">
                <div class="sidebar-label">${listPage ? 'Jump to' : 'On this page'}</div>
                <div id="gp-jump"></div>
            </div>
            <div class="panel-sec">
                <div class="sidebar-label">Guides</div>
                <ul class="sidebar-links">${GUIDES.filter(g => g[0] !== here).map(g => `<li><a href="${root()}${g[0]}">${esc(g[1])}</a></li>`).join('')}</ul>
            </div>`;
    }

    // ---------------------------------------------------------------- list pages
    function listPage() {
        container = $('content-container');
        kind = container.dataset.kind || 'gram';
        K = KINDS[kind];
        const filters = kind === 'ms' ? `
                <div class="sidebar-label">Show</div>
                <div class="kind-pills kind-pills--small" id="gp-show" role="group" aria-label="Which manuscripts to show">
                    <button type="button" class="kind-pill" data-show="all" aria-pressed="true">All</button>
                    <button type="button" class="kind-pill" data-show="extant" aria-pressed="false">Surviving</button>
                    <button type="button" class="kind-pill" data-show="lost" aria-pressed="false">Lost (reconstructed)</button>
                </div>
                <label class="panel-check"><input type="checkbox" id="gp-open"> Show Liebermann’s description and notes for every manuscript</label>`
            : kind === 'law' ? `
                <div class="sidebar-label">Details</div>
                <label class="panel-check"><input type="checkbox" id="gp-open"> Show the manuscripts, editions and notes for every code</label>` : '';
        const placeholder = { law: 'e.g. II As, Wergeld, Cnut', ms: 'e.g. H, Textus Roffensis, Cotton', gram: 'e.g. dt, Gegensatz, plural', works: 'e.g. Birch, Schmid, Chronicle' }[kind];
        panel({ placeholder, filters });
        $('gp-help').textContent = { law: 'Abbreviation: codes whose abbreviation begins with what you type (II As, IIAs). Everything: also the German, the English and the notes.',
            ms: 'Siglum: sigla that begin with what you type. Everything: also the library, the laws and the notes.',
            gram: 'Term: Liebermann’s abbreviations and terms that begin with what you type. Everything: also the German and the English.',
            works: 'Author or title: works whose short title begins with what you type. Everything: the full citations and notes too.' }[kind];

        fetch(root() + container.dataset.source)
            .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
            .then(rows => {
                // rows with the same Anchor together, in the order of the file (the manuscripts'
                // two lost "il" stay apart: each is its own manuscript)
                const byAnchor = new Map();
                rows.forEach((r, i) => {
                    const key = kind === 'ms' ? r.Anchor + (byAnchor.has(r.Anchor) && byAnchor.get(r.Anchor)[0]['German Expansion'] !== r['German Expansion'] ? '#' + i : '') : r.Anchor;
                    if (!byAnchor.has(key)) byAnchor.set(key, []);
                    byAnchor.get(key).push(r);
                });
                groups = [...byAnchor.entries()].map(([key, rs]) => ({ key, anchor: rs[0].Anchor, rows: rs, letter: K.letter(rs[0]) }));
                // the grammatical terms in alphabetical order (the file is in no order); Ä under A
                if (kind === 'gram') groups.sort((a, b) => fold(a.rows[0]['Gesetze Text']).replace(/[^a-z0-9]/g, '').localeCompare(fold(b.rows[0]['Gesetze Text']).replace(/[^a-z0-9]/g, ''), 'de', { numeric: true }));
                if (kind === 'works') groups.sort((a, b) => fold(a.rows[0]['Short Title']) < fold(b.rows[0]['Short Title']) ? -1 : 1).forEach(g => { g.letter = K.letter(g.rows[0]); });
                readUrl();
                bind();
                draw();
                if (location.hash) {
                    const anchor = decodeURIComponent(location.hash.slice(1));
                    const el = document.getElementById(anchor);
                    if (el) { el.scrollIntoView(); el.classList.add('is-target'); } else forward(anchor);
                }
            })
            .catch(() => { container.innerHTML = '<p class="notice error">The list could not be loaded.</p>'; });
    }

    // Entries link manuscript sigla to the law code list (lawAbb.html#H). If the anchor isn't here
    // but is on the list named by data-elsewhere ("data/manuscripts.json msAbb.html"), go there.
    function forward(anchor) {
        const [file, page] = (container.dataset.elsewhere || '').split(' ');
        if (!file || !page) return;
        fetch(root() + file).then(r => r.json()).then(rows => {
            if (rows.some(r => r.Anchor === anchor)) location.replace(root() + page + '#' + encodeURIComponent(anchor));
        }).catch(() => {});
    }

    function bind() {
        let t;
        $('gp-q').addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { state.q = $('gp-q').value; draw(); writeUrl(); }, 120); });
        $('gp-where').addEventListener('click', e => { const b = e.target.closest('[data-where]'); if (!b) return; state.where = b.dataset.where; draw(); writeUrl(); });
        if ($('gp-show')) $('gp-show').addEventListener('click', e => { const b = e.target.closest('[data-show]'); if (!b) return; state.show = b.dataset.show; draw(); writeUrl(); });
        if ($('gp-open')) $('gp-open').addEventListener('change', () => {
            state.open = $('gp-open').checked;
            container.querySelectorAll('details.gl-more').forEach(d => { d.open = state.open; });
        });
        $('gp-jump').addEventListener('click', e => {
            const a = e.target.closest('a[data-letter]');
            if (!a) return;
            e.preventDefault();
            const el = document.getElementById('letter-' + a.dataset.letter);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
    function readUrl() {
        const p = new URLSearchParams(location.search);
        state.q = p.get('q') || '';
        state.where = p.get('in') === 'all' ? 'all' : 'start';
        state.show = ['extant', 'lost'].includes(p.get('show')) ? p.get('show') : 'all';
        $('gp-q').value = state.q;
    }
    function writeUrl() {
        const p = new URLSearchParams();
        if (state.q) p.set('q', state.q);
        if (state.where === 'all') p.set('in', 'all');
        if (state.show !== 'all') p.set('show', state.show);
        const s = p.toString();
        history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash);
    }

    const lost = r => /^\[lost\]/.test(r.Notes || '') || /^Lost manuscript/.test(r['English Translation'] || '');
    function rowMatches(r) {
        const q = state.q.trim();
        if (!q) return true;
        if (state.where === 'start') {
            const s = squash(q);
            return squash(r[K.field]).startsWith(s) || (kind === 'works' && squash(r['Gesetze Text']).startsWith(s));
        }
        const words = fold(q).split(/\s+/).filter(Boolean);
        const text = fold(K.fields.map(f => r[f] || '').join(' '));
        return words.every(w => text.includes(w));
    }
    function shownGroups() {
        return groups.map(g => {
            let rows = g.rows;
            if (kind === 'ms' && state.show !== 'all') rows = rows.filter(r => (state.show === 'lost') === lost(r));
            const hit = rows.filter(rowMatches);
            // a group is shown whole when any of its spellings matches
            return hit.length ? Object.assign({}, g, { rows: kind === 'gram' ? rows : rows }) : null;
        }).filter(Boolean);
    }

    function draw() {
        document.querySelectorAll('[data-where]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.where === state.where)));
        document.querySelectorAll('[data-show]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.show === state.show)));
        const list = shownGroups();
        const n = K.noun;
        $('gp-count').textContent = list.length === groups.length ? `${groups.length} ${n[1]}` : `${list.length} of ${groups.length} ${n[1]}`;
        const letters = [...new Set(list.map(g => g.letter))];
        const all = [...new Set(groups.map(g => g.letter))];
        $('gp-jump').innerHTML = `<div class="letter-jump">${all.map(l => letters.includes(l)
            ? `<a href="#letter-${esc(l)}" data-letter="${esc(l)}">${esc(l)}</a>` : `<span>${esc(l)}</span>`).join('')}</div>`;
        if (!list.length) { container.innerHTML = `<p class="muted">Nothing matches “${esc(state.q)}”${state.where === 'start' ? `. <button type="button" class="link-button" id="gp-try-all">Look in everything</button>` : ''}.</p>`; const b = $('gp-try-all'); if (b) b.onclick = () => { state.where = 'all'; draw(); writeUrl(); }; return; }
        container.innerHTML = ({ law: drawLaw, ms: drawMs, gram: drawGram, works: drawWorks })[kind](list);
        if (state.open) container.querySelectorAll('details.gl-more').forEach(d => { d.open = true; });
    }

    // a letter heading, as a row of the table (so the columns run on unbroken)
    const letterRow = (l, cols) => `<tr class="gl-letter" id="letter-${esc(l)}"><th colspan="${cols}" scope="rowgroup">${esc(l)}</th></tr>`;
    function withLetters(list, cols, rowsOf) {
        let html = '', last = '';
        list.forEach(g => {
            if (g.letter !== last) { html += letterRow(g.letter, cols); last = g.letter; }
            html += rowsOf(g);
        });
        return html;
    }

    // Law codes: one table, one line a code; the other spellings under the abbreviation; the
    // manuscripts, editions and notes folded away under the English name.
    function drawLaw(list) {
        return `<table class="glossary glossary--law">
            <colgroup><col class="c-abbr"><col class="c-de"><col class="c-en"><col class="c-page"></colgroup>
            <thead><tr><th scope="col">Abbreviation</th><th scope="col">Liebermann’s German</th><th scope="col">English</th><th scope="col" class="num" title="Where the text begins in Liebermann, Gesetze I">Gesetze I, p.</th></tr></thead>
            <tbody>${withLetters(list, 4, g => {
                const r = g.rows[0];
                const also = [...new Set(g.rows.slice(1).map(x => x['Gesetze Text']))];
                const note = r['Notes: Information & Editions'];
                return `<tr id="${esc(g.anchor)}">
                    <td class="gl-term">${esc(r['Gesetze Text'])}${also.length ? `<span class="gl-also">also ${also.map(esc).join(', ')}</span>` : ''}</td>
                    <td class="gl-de">${esc(r['German Expansion'])}</td>
                    <td class="gl-en">${esc(r['English Translation'])}${note ? `<details class="gl-more"><summary>Manuscripts, editions and notes</summary><p>${esc(note)}</p></details>` : ''}</td>
                    <td class="num">${esc(r['Notes: Start page in Liebermann Vol. I'] || '')}</td>
                </tr>`;
            })}</tbody></table>`;
    }

    // Manuscripts: siglum, library and shelfmark, Liebermann's date, the laws in it; his German
    // description and notes folded away.
    function drawMs(list) {
        const seen = new Set();
        return `<table class="glossary glossary--ms">
            <colgroup><col class="c-abbr"><col class="c-en"><col class="c-date"><col class="c-laws"><col class="c-page"></colgroup>
            <thead><tr><th scope="col">Siglum</th><th scope="col">Manuscript</th><th scope="col">Date (Liebermann)</th><th scope="col">Laws in it</th><th scope="col" class="num" title="Where Liebermann describes it, Gesetze I">Gesetze I, p.</th></tr></thead>
            <tbody>${withLetters(list, 5, g => g.rows.map(r => {
                const id = seen.has(g.anchor) ? '' : ` id="${esc(g.anchor)}"`;
                seen.add(g.anchor);
                const tag = lost(r) ? '<span class="gl-tag">lost</span>' : /^\[not seen/.test(r.Notes || '') ? '<span class="gl-tag">not seen by Liebermann</span>' : '';
                const notes = String(r.Notes || '').replace(/^\[[^\]]*\]\s*/, '');
                const more = [r['German Expansion'] ? `<p><span class="muted">Liebermann:</span> <span lang="de">${esc(r['German Expansion'])}</span></p>` : '', notes ? `<p>${esc(notes)}</p>` : ''].join('');
                return `<tr${id}>
                    <td class="gl-term">${esc(r['Gesetze Text'])}</td>
                    <td class="gl-en">${esc(r['English Translation'])}${tag}${more ? `<details class="gl-more"><summary>Description and notes</summary>${more}</details>` : ''}</td>
                    <td class="gl-date">${esc(r['Date (Liebermann)'] || '')}</td>
                    <td class="gl-laws">${esc(r['Laws in it'] || '')}</td>
                    <td class="num">${esc(r['Liebermann I, page'] || '')}</td>
                </tr>`;
            }).join(''))}</tbody></table>`;
    }

    // Grammatical terms: a group of spellings under a heading row; a term with one spelling is a
    // single row (its term in bold is its heading). Notes in a row of their own under the group.
    function drawGram(list) {
        return `<table class="glossary glossary--gram">
            <colgroup><col class="c-abbr"><col class="c-de"><col class="c-en"></colgroup>
            <thead><tr><th scope="col">As printed</th><th scope="col">German</th><th scope="col">English</th></tr></thead>
            ${withLetters(list, 3, g => {
                const notes = [...new Set(g.rows.map(r => r['Notes: Grammatical']).filter(Boolean))];
                const multi = g.rows.length > 1;
                const de = r => `<span lang="de">${esc(r['German Expansion'])}</span>${r['Modern German'] ? `<span class="modern-german">today: ${esc(r['Modern German'])}</span>` : ''}`;
                return `<tbody class="gl-group${multi ? ' gl-group--multi' : ''}" id="${esc(g.anchor)}">
                    ${multi ? `<tr class="gl-head"><th colspan="3" scope="rowgroup">${esc(g.rows[0]['German Expansion'])}<span class="gl-head-en">${esc(g.rows[0]['English Translation'])}</span></th></tr>` : ''}
                    ${g.rows.map(r => `<tr><td class="gl-term">${esc(r['Gesetze Text'])}</td><td class="gl-de">${de(r)}</td><td class="gl-en">${esc(r['English Translation'])}</td></tr>`).join('')}
                    ${notes.length ? `<tr class="gl-note"><td></td><td colspan="2">${notes.map(esc).join(' ')}</td></tr>` : ''}
                </tbody>`;
            }).replace(/<tr class="gl-letter"([^>]*)>([\s\S]*?)<\/tr>/g, '<tbody class="gl-letter-body"><tr class="gl-letter"$1>$2</tr></tbody>')}
            </table>`;
    }

    // Authors and works cited: one entry per work, alphabetical, with the forms Liebermann prints.
    function drawWorks(list) {
        let html = '', last = '';
        list.forEach(g => {
            if (g.letter !== last) { html += `<h2 class="gl-letter-h" id="letter-${esc(g.letter)}">${esc(g.letter)}</h2>`; last = g.letter; }
            const r0 = g.rows[0];
            const forms = [...new Set(g.rows.map(r => String(r['Gesetze Text']).trim()))];
            const note = (g.rows.find(r => r.Notes) || {}).Notes;
            html += `<section class="bib-work" id="${esc(g.anchor)}">
                <h3>${esc(r0['Short Title'])}</h3>
                <p class="bib-full">${italics(r0['Full Citation'])}</p>
                <p class="small"><span class="muted">As printed in the Gesetze:</span> ${forms.map(f => `<span class="term">${esc(f)}</span>`).join(' · ')}</p>
                ${note ? `<p class="small bib-note"><span class="muted">Note:</span> ${italics(note)}</p>` : ''}
            </section>`;
        });
        return html;
    }

    // ---------------------------------------------------------------- How to read an entry
    function guidePage() {
        panel(null);
        const main = document.querySelector('.laws-main');
        $('gp-count').textContent = 'Liebermann’s system, explained';
        const secs = [...main.querySelectorAll('section[id] > h2')];
        $('gp-jump').innerHTML = `<ul class="sidebar-links">${secs.map(h => `<li><a href="#${esc(h.parentElement.id)}">${esc(h.textContent)}</a></li>`).join('')}</ul>`;
        let marks = [], at = -1, t;
        const clear = () => { main.querySelectorAll('mark.gp-mark').forEach(m => { m.replaceWith(document.createTextNode(m.textContent)); }); main.normalize(); marks = []; at = -1; };
        const go = i => {
            if (!marks.length) return;
            at = (i + marks.length) % marks.length;
            marks.forEach((m, k) => m.classList.toggle('is-current', k === at));
            marks[at].scrollIntoView({ block: 'center', behavior: 'smooth' });
            $('gp-found').textContent = `${at + 1} of ${marks.length}`;
        };
        const find = () => {
            clear();
            const q = $('gp-q').value.trim();
            $('gp-status').hidden = !q;
            if (!q) return;
            const fq = fold(q);
            const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement.closest('script, style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
            const nodes = [];
            while (walker.nextNode()) nodes.push(walker.currentNode);
            nodes.forEach(node => {
                const text = node.nodeValue;
                // fold letter by letter so positions in the folded text match the original
                const f = [...text].map(ch => fold(ch) || ch);
                const flat = f.join('');
                let i = flat.indexOf(fq);
                if (i < 0) return;
                const map = []; f.forEach((s, k) => { for (let j = 0; j < s.length; j++) map.push(k); });
                const chars = [...text];
                const parts = [];
                let from = 0;
                while (i >= 0) {
                    const a = map[i], b = map[i + fq.length - 1] + 1;
                    parts.push([from, a, b]);
                    from = b;
                    i = flat.indexOf(fq, i + fq.length);
                }
                const frag = document.createDocumentFragment();
                parts.forEach(([s, a, b]) => {
                    frag.appendChild(document.createTextNode(chars.slice(s, a).join('')));
                    const m = document.createElement('mark');
                    m.className = 'gp-mark';
                    m.textContent = chars.slice(a, b).join('');
                    frag.appendChild(m);
                    marks.push(m);
                });
                frag.appendChild(document.createTextNode(chars.slice(from).join('')));
                node.replaceWith(frag);
            });
            marks = [...main.querySelectorAll('mark.gp-mark')];
            if (marks.length) go(0); else $('gp-found').textContent = 'Not found';
        };
        $('gp-q').addEventListener('input', () => { clearTimeout(t); t = setTimeout(find, 200); });
        $('gp-q').addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); go(e.shiftKey ? at - 1 : at + 1); } });
        $('gp-next').addEventListener('click', () => go(at + 1));
        $('gp-prev').addEventListener('click', () => go(at - 1));
    }

    document.addEventListener('DOMContentLoaded', () => {
        if ($('content-container')) listPage(); else guidePage();
    });
})();
