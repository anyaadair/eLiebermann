/*
 * The search panel on the left of the law code and clause pages (the Laws page has its
 * own, larger one): bubbles, suggestion lists, matches in context, and the highlighting
 * of the kind of search in use. Needs scripts/eliebermann.js and scripts/law-search.js.
 *
 *   LawPanel.pills(el, [[key, label]], isOn(key), onClick(key))
 *   LawPanel.suggestBox(input, listEl, typed => [{ value, html }], pick(value))
 *   LawPanel.kwic(text, [[start, end]], lang)        -> HTML, the matches marked
 *   LawPanel.watch(panel, used)                      highlights the section in use
 *   LawPanel.fields(textEntry, where)                -> [[label, text, lang]] from data/laws-text.json
 */
(function () {
    'use strict';
    const esc = s => ELieb.escapeXml(s);

    function pills(el, items, isOn, onClick) {
        el.innerHTML = items.map(([k, label, title]) => `<button type="button" class="kind-pill" data-k="${esc(k)}" aria-pressed="${isOn(k)}"${title ? ` title="${esc(title)}"` : ''}>${esc(label)}</button>`).join('');
        el.onclick = e => { const b = e.target.closest('[data-k]'); if (b) onClick(b.dataset.k); };
    }

    function suggestBox(input, list, items, pick) {
        let shown = [], active = -1;
        const close = () => { list.hidden = true; active = -1; };
        const draw = () => {
            shown = items(input.value.trim());
            if (!shown.length) { close(); return; }
            list.innerHTML = shown.map((x, i) => `<li role="option" aria-selected="${i === active}"><a href="#" data-i="${i}">${x.html}</a></li>`).join('');
            list.hidden = false;
        };
        input.addEventListener('input', () => { active = -1; draw(); });
        input.addEventListener('focus', draw);
        input.addEventListener('blur', () => setTimeout(close, 150));
        input.addEventListener('keydown', e => {
            if (list.hidden) { if (e.key === 'Enter' && shown.length) { e.preventDefault(); pick(shown[0].value); } return; }
            if (e.key === 'ArrowDown') { e.preventDefault(); active = (active + 1) % shown.length; draw(); }
            else if (e.key === 'ArrowUp') { e.preventDefault(); active = active <= 0 ? shown.length - 1 : active - 1; draw(); }
            else if (e.key === 'Escape') close();
            else if (e.key === 'Enter') { e.preventDefault(); pick(shown[Math.max(0, active)].value); close(); }
        });
        list.addEventListener('mousedown', e => e.preventDefault());
        list.addEventListener('click', e => { const a = e.target.closest('[data-i]'); if (a) { e.preventDefault(); pick(shown[+a.dataset.i].value); close(); } });
        return { refresh: draw };
    }

    // The matching words in context: about a dozen words either side of the first match.
    function kwic(text, ranges, lang) {
        const first = ranges.reduce((a, b) => (b[0] < a[0] ? b : a));
        let s = Math.max(0, first[0] - 90), e = Math.min(text.length, first[1] + 110);
        if (s > 0) s = text.indexOf(' ', s) + 1 || s;
        if (e < text.length) e = text.lastIndexOf(' ', e) > first[1] ? text.lastIndexOf(' ', e) : e;
        const inside = ranges.filter(r => r[0] >= s && r[1] <= e).sort((a, b) => a[0] - b[0]);
        let out = '', at = s;
        inside.forEach(([a, b]) => { if (a < at) return; out += esc(text.slice(at, a)) + '<mark>' + esc(text.slice(a, b)) + '</mark>'; at = b; });
        out += esc(text.slice(at, e));
        const l = lang && !/^(en|de|notes)$/.test(lang) ? ELieb.langAttr(lang) : '';
        return `${s > 0 ? '… ' : ''}<span${l}>${out}</span>${e < text.length ? ' …' : ''}`;
    }

    // The section of the panel in use (something typed in it, or the cursor in it) stands out;
    // the sections that apply to every search too; the other kinds of search fade a little.
    function watch(panel, used) {
        let focused = '';
        const mark = () => {
            const u = used();
            const on = m => u[m] || focused === m;
            const any = Object.keys(u).some(on);
            panel.querySelectorAll('.panel-sec--method').forEach(el => {
                el.classList.toggle('is-active', on(el.dataset.method));
                el.classList.toggle('is-idle', any && !on(el.dataset.method));
            });
            panel.querySelectorAll('.panel-sec--shared').forEach(el => el.classList.toggle('is-shared', any));
        };
        panel.querySelectorAll('.panel-sec--method').forEach(el => {
            el.addEventListener('focusin', () => { focused = el.dataset.method; mark(); });
            el.addEventListener('focusout', () => setTimeout(() => { if (!el.contains(document.activeElement) && focused === el.dataset.method) { focused = ''; mark(); } }, 0));
        });
        return mark;
    }

    const TRANSLATORS = { robertson: 'Robertson', whitelock: 'Whitelock', attenborough: 'Attenborough', rabin: 'Rabin',
        'jurasinski-and-oliver': 'Jurasinski and Oliver', oliver: 'Oliver', kennedy: 'Kennedy', gobbitt: 'Gobbitt',
        wormald: 'Wormald', claude: 'English of Liebermann’s German', unattributed: 'Translator not recorded' };
    const WHERE = [['orig', 'Original texts'], ['en', 'English translations'], ['de', 'Liebermann’s German'], ['notes', 'Notes']];
    function fields(t, where) {
        const out = [];
        if (!t) return out;
        if (where.has('orig')) t.t.forEach(([lang, label, text]) => out.push([label, text, lang]));
        if (where.has('en')) t.e.forEach(([src, text]) => out.push([(TRANSLATORS[src] || src) + ' (English)', text, 'en']));
        if (where.has('de') && t.g) out.push(['Liebermann (German)', t.g, 'de']);
        if (where.has('notes') && t.n) out.push(['Notes', t.n, 'notes']);
        return out;
    }

    let textsLoading = null, dictLoading = null;
    const root = () => window.SITE_ROOT || '';
    const loadTexts = () => textsLoading || (textsLoading = fetch(root() + 'data/laws-text.json').then(r => r.ok ? r.json() : {}).catch(() => ({})));
    const loadDict = () => dictLoading || (dictLoading = fetch(root() + 'data/dict-citations.json').then(r => r.ok ? r.json() : {}).catch(() => ({})));

    window.LawPanel = { pills, suggestBox, kwic, watch, fields, WHERE, loadTexts, loadDict };
})();
