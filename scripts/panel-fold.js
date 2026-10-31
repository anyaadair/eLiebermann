/*
 * The left-hand panel on the Laws, Guides and Bibliography pages can be folded away
 * ("‹" at its top) and brought back ("☰" above the text). On a wide screen the choice is
 * remembered in this browser. On a narrow screen (under 60rem) the text always comes
 * first: the panel starts folded and, when brought back, slides in over the text
 * (Escape or a click outside it folds it again).
 */
(function () {
    'use strict';
    const KEY = 'eLiebermann.panel';
    const narrow = window.matchMedia('(max-width: 60rem)');
    const savedClosed = () => { try { return localStorage.getItem(KEY) === 'closed'; } catch (e) { return false; } };
    const save = closed => { try { if (closed) localStorage.setItem(KEY, 'closed'); else localStorage.removeItem(KEY); } catch (e) { /* not kept */ } };

    function init() {
        const layout = document.querySelector('.laws-layout');
        const panel = layout && layout.querySelector(':scope > .laws-panel');
        const main = layout && layout.querySelector(':scope > .laws-main');
        if (!panel || !main) return;
        if (!panel.id) panel.id = 'laws-panel';
        const name = panel.getAttribute('aria-label') || 'Panel';

        const fold = document.createElement('button');
        fold.type = 'button';
        fold.className = 'sidebar-fold panel-fold';
        fold.textContent = '‹';
        fold.title = 'Hide this panel';
        fold.setAttribute('aria-label', 'Hide this panel');
        fold.setAttribute('aria-controls', panel.id);

        const open = document.createElement('button');
        open.type = 'button';
        open.className = 'sidebar-open panel-open';
        open.innerHTML = '<span aria-hidden="true">☰</span> ';
        open.appendChild(document.createTextNode(name));
        open.setAttribute('aria-controls', panel.id);
        main.insertBefore(open, main.firstChild);

        // the Guides pages draw their panel after this runs, so the button is put back if it goes
        const place = () => { if (fold.parentNode !== panel) panel.insertBefore(fold, panel.firstChild); };
        place();
        new MutationObserver(place).observe(panel, { childList: true });

        const set = closed => {
            layout.classList.toggle('panel-closed', closed);
            open.hidden = !closed;
            fold.setAttribute('aria-expanded', String(!closed));
            open.setAttribute('aria-expanded', String(!closed));
        };
        set(narrow.matches || savedClosed());
        narrow.addEventListener('change', () => set(narrow.matches || savedClosed()));
        fold.addEventListener('click', () => { set(true); if (!narrow.matches) save(true); open.focus(); });
        open.addEventListener('click', e => {
            e.stopPropagation();
            set(false);
            if (!narrow.matches) save(false);
            const box = panel.querySelector('input');
            if (box) box.focus();
        });
        // on a narrow screen the panel lies over the text: Escape or a click outside folds it
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && narrow.matches && !layout.classList.contains('panel-closed')) { set(true); open.focus(); }
        });
        document.addEventListener('click', e => {
            if (narrow.matches && !layout.classList.contains('panel-closed') && !panel.contains(e.target)) set(true);
        });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
