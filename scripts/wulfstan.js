// Archbishop Wulfstan's part in the law codes (data/wulfstan.json): three badges, each naming
// the scholar whose view it is (so far Rabin), for the law-code pages, the clause pages, the list
// of law codes and the Laws search.
//   composed  "Composed by Wulfstan"
//   reworked  "Edited or Reworked by Wulfstan"
//   disputed  "Attributed to Wulfstan (disputed)"
// A badge opens to say what the scholar says, and where.
(function () {
    'use strict';
    const ORDER = ['composed', 'reworked', 'disputed'];
    let loading = null;
    let data = { kinds: {}, sources: {}, codes: {}, clauses: {} };
    const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

    function load(root) {
        if (!loading) loading = fetch((root || '') + 'data/wulfstan.json')
            .then(r => r.ok ? r.json() : null).catch(() => null)
            .then(d => { if (d) data = d; return data; });
        return loading;
    }
    const codeViews = code => data.codes[code] || [];
    const clauseViews = id => data.clauses[id] || [];
    // The kinds a clause has: its law code's, and its own (a clause Wulfstan probably added).
    function kindsOf(code, id) {
        const s = new Set();
        codeViews(code).concat(id ? clauseViews(id) : []).forEach(v => s.add(v.kind));
        return s;
    }
    // "xiv–xv" -> "pp. xiv–xv"; "xv; p. 405" -> "p. xv; p. 405"
    const pageText = p => String(p).split(/;\s*/).map(x => /^pp?\. /.test(x) ? x : (/–/.test(x) ? 'pp. ' : 'p. ') + x).join('; ');
    // One badge per kind; inside, each view of that kind: the scholar's words, then name and page.
    function badge(kind, views, opts) {
        const label = data.kinds[kind] || kind;
        const by = [...new Set(views.map(v => v.by))];
        const lines = views.map(v => `<p>${esc(v.note)} <span class="wulf-src">(${esc(v.by)}, ${esc(pageText(v.page))}${v.of ? ', on ' + esc(v.of) : ''})</span></p>`).join('');
        const works = by.map(b => data.sources[b]).filter(Boolean).map(esc).join('; ');
        if (opts && opts.plain) return `<span class="wulf-badge wulf-badge--${kind}" title="${esc(label + ' (' + by.join(', ') + ')')}">${esc(opts.short ? SHORT[kind] : label)}</span>`;
        return `<details class="wulf-badge wulf-badge--${kind}"><summary>${esc(label)} <span class="wulf-by">${esc(by.join(', '))}</span></summary>` +
            `<div class="wulf-badge__body">${lines}${works ? `<p class="wulf-src">${works}</p>` : ''}</div></details>`;
    }
    const SHORT = { composed: 'By Wulfstan', reworked: 'Reworked by Wulfstan', disputed: 'Wulfstan?' };   // in the narrow clause-number column
    // The badges for a law code (id empty), or for a clause: the code's and the clause's own,
    // one badge per kind (a clause's own view joins its code's when they are the same kind).
    function badges(code, id, opts) {
        const views = codeViews(code).map(v => v).concat((id ? clauseViews(id) : []).map(v => Object.assign({ of: 'this clause' }, v)));
        if (!views.length) return '';
        return `<div class="wulf-badges">${ORDER.filter(k => views.some(v => v.kind === k))
            .map(k => badge(k, views.filter(v => v.kind === k), opts)).join('')}</div>`;
    }
    // Only a clause's own badges (in a list of clauses, where the code's badge is already shown).
    function clauseBadges(id, opts) {
        const views = clauseViews(id);
        if (!views.length) return '';
        return ORDER.filter(k => views.some(v => v.kind === k)).map(k => badge(k, views.filter(v => v.kind === k), Object.assign({ plain: true }, opts))).join(' ');
    }
    // A law code's badges, small and inline (the list of law codes)
    function codeBadges(code) {
        const views = codeViews(code);
        return ORDER.filter(k => views.some(v => v.kind === k)).map(k => badge(k, views.filter(v => v.kind === k), { plain: true })).join(' ');
    }
    window.Wulfstan = { load, kindsOf, badges, clauseBadges, codeBadges, ORDER, kinds: () => data.kinds };
})();
