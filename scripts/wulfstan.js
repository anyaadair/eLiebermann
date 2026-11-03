// Archbishop Wulfstan's part in the law codes (data/wulfstan.json): three badges, each naming
// the scholar whose view it is (Rabin), for the law-code pages, the clause pages, the list
// of law codes and the Laws search.
//   composed  "Composed by Wulfstan"
//   reworked  "Edited or Reworked by Wulfstan"
//   disputed  "Attributed to Wulfstan (disputed)"
// A badge opens to say what the scholar says, and where. A "secondary" view (Wormald) never makes
// a badge of its own: Rabin's view names the badge, and Wormald's is shown inside it, even where
// he differs.
// Other people connected with a code (data/associations.json: Archbishop Wulfhelm, Dunstan) have
// badges of their own, in other colours, beside the Wulfstan ones.
(function () {
    'use strict';
    const ORDER = ['composed', 'reworked', 'disputed'];
    let loading = null;
    let data = { kinds: {}, sources: {}, codes: {}, clauses: {} };
    let others = { kinds: {}, sources: {}, codes: {} };
    const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

    function load(root) {
        const get = f => fetch((root || '') + 'data/' + f).then(r => r.ok ? r.json() : null).catch(() => null);
        if (!loading) loading = Promise.all([get('wulfstan.json'), get('associations.json')])
            .then(([d, a]) => { if (d) data = d; if (a) others = a; return data; });
        return loading;
    }
    const primary = v => !v.secondary;
    const codeViews = code => data.codes[code] || [];
    const clauseViews = id => data.clauses[id] || [];
    // The kinds a clause has: its law code's, and its own (a clause Wulfstan probably added); Rabin's only.
    function kindsOf(code, id) {
        const s = new Set();
        codeViews(code).concat(id ? clauseViews(id) : []).filter(primary).forEach(v => s.add(v.kind));
        return s;
    }
    // "xiv–xv" -> "pp. xiv–xv"; "xv; p. 405" -> "p. xv; p. 405"
    const pageText = p => String(p).split(/;\s*/).map(x => /^pp?\. /.test(x) ? x : (/[–,]/.test(x) ? 'pp. ' : 'p. ') + x).join('; ');
    // a secondary view: "Wormald agrees: …", "Wormald differs: …", or "Wormald: …"
    function lead(v) {
        if (!v.secondary) return esc(v.note);
        const m = /^(Agrees|Differs)\b(:?)\s*([\s\S]*)$/.exec(v.note);
        return m ? `<strong>${esc(v.by)} ${m[1].toLowerCase()}${m[2]}</strong> ${esc(m[3])}` : `<strong>${esc(v.by)}:</strong> ${esc(v.note)}`;
    }
    const line = v => `<p>${lead(v)} <span class="wulf-src">(${esc(v.by)}, ${esc(pageText(v.page))}${v.of ? ', on ' + esc(v.of) : ''})</span></p>`;
    // One badge per kind; inside, each view of that kind (and the secondary views): the scholar's
    // words, then name and page. The summary names only the scholars whose view the badge is.
    function badge(kind, views, opts, extra, set) {
        set = set || data;
        const label = set.kinds[kind] || kind;
        const by = [...new Set(views.map(v => v.by))];
        const all = views.concat(extra || []);
        const works = [...new Set(all.map(v => v.by))].map(b => set.sources[b] || data.sources[b]).filter(Boolean).map(esc).join('; ');
        if (opts && opts.plain) return `<span class="wulf-badge wulf-badge--${kind}" title="${esc(label + ' (' + by.join(', ') + ')')}">${esc(opts.short ? (SHORT[kind] || label) : label)}</span>`;
        return `<details class="wulf-badge wulf-badge--${kind}"><summary>${esc(label)} <span class="wulf-by">${esc(by.join(', '))}</span></summary>` +
            `<div class="wulf-badge__body">${all.map(line).join('')}${works ? `<p class="wulf-src">${works}</p>` : ''}</div></details>`;
    }
    const SHORT = { composed: 'By Wulfstan', reworked: 'Reworked by Wulfstan', disputed: 'Wulfstan?' };   // in the narrow clause-number column
    // The badges of other people connected with the code (Wulfhelm, Dunstan)
    function otherBadges(code, opts) {
        const views = others.codes[code] || [];
        return [...new Set(views.map(v => v.kind))].map(k => badge(k, views.filter(v => v.kind === k), opts, null, others)).join(opts && opts.plain ? ' ' : '');
    }
    // The badges for a law code (id empty), or for a clause: the code's and the clause's own,
    // one badge per kind (a clause's own view joins its code's when they are the same kind).
    function badges(code, id, opts) {
        const views = codeViews(code).concat((id ? clauseViews(id) : []).map(v => Object.assign({ of: 'this clause' }, v)));
        const main = views.filter(primary), second = views.filter(v => !primary(v));
        const kinds = ORDER.filter(k => main.some(v => v.kind === k));
        const wulf = kinds.map((k, i) => badge(k, main.filter(v => v.kind === k), opts, i === 0 ? second : null)).join('');
        const rest = otherBadges(code, opts);
        return wulf || rest ? `<div class="wulf-badges">${wulf}${rest}</div>` : '';
    }
    // Only a clause's own badges (in a list of clauses, where the code's badge is already shown).
    function clauseBadges(id, opts) {
        const views = clauseViews(id).filter(primary);
        if (!views.length) return '';
        return ORDER.filter(k => views.some(v => v.kind === k)).map(k => badge(k, views.filter(v => v.kind === k), Object.assign({ plain: true }, opts))).join(' ');
    }
    // A law code's badges, small and inline (the list of law codes)
    function codeBadges(code) {
        const views = codeViews(code).filter(primary);
        return [ORDER.filter(k => views.some(v => v.kind === k)).map(k => badge(k, views.filter(v => v.kind === k), { plain: true })).join(' '), otherBadges(code, { plain: true })].filter(Boolean).join(' ');
    }
    window.Wulfstan = { load, kindsOf, badges, clauseBadges, codeBadges, ORDER, kinds: () => data.kinds };
})();
