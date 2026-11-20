/*
 * The top of the page and the side panels.
 * - On a wide screen, on pages with a side panel (Laws, Dictionary, Guides, Bibliography), the
 *   site's heading and menus stay at the top of the window (style.css, .site-top), and the panel
 *   sits just below them. Their height is kept in the CSS variable --site-top-h.
 * - ELiebScroll.toMiddle(el): brings an element to the middle of the space below the heading,
 *   but never so far that the end of the page comes up: the panel stays in place under the
 *   reader's cursor (the reader can still scroll to the end).
 * - A table whose column headings stay in view (the Guides' lists of law codes, manuscripts and
 *   grammatical terms): their height is kept in --sticky-head-h, so that whatever a link jumps to
 *   stops below them as well as below the heading and menus (style.css, scroll-padding-top).
 * - A "Back to top" button on any long page (the Dictionary has its own).
 */
(function () {
    'use strict';
    const top = () => document.querySelector('.site-top');
    // column headings that stay in view under the menus (.glossary thead th { position: sticky })
    const stickyHead = () => {
        const th = document.querySelector('.glossary thead th');
        return th && getComputedStyle(th).position === 'sticky' ? th.closest('thead').offsetHeight : 0;
    };
    const fixed = () => { const t = top(); return (t && getComputedStyle(t).position === 'sticky' ? t.offsetHeight : 0) + stickyHead(); };

    function measure() {
        const t = top(), root = document.documentElement.style;
        if (t) root.setProperty('--site-top-h', t.offsetHeight + 'px');
        root.setProperty('--sticky-head-h', stickyHead() + 'px');
    }

    function toMiddle(el, smooth) {
        if (!el) return;
        const r = el.getBoundingClientRect(), head = fixed();
        let y = window.scrollY + r.top + r.height / 2 - (head + (window.innerHeight - head) / 2);
        const layout = el.closest('.laws-layout, .entry-layout');
        if (layout) y = Math.min(y, window.scrollY + layout.getBoundingClientRect().bottom - window.innerHeight);
        window.scrollTo({ top: Math.max(0, y), behavior: smooth ? 'smooth' : 'auto' });
    }
    // measure: for a script that draws a list and jumps into it straight away (scripts/abbreviations.js)
    window.ELiebScroll = { toMiddle, headHeight: fixed, measure: () => measure() };

    function backToTop() {
        if (document.getElementById('to-top')) return;   // the Dictionary's own
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'to-top';
        b.id = 'to-top';
        b.setAttribute('aria-label', 'Back to the top of the page');
        b.innerHTML = '<span aria-hidden="true">↑</span> Back to top';
        document.body.appendChild(b);
        const check = () => b.classList.toggle('is-shown', window.scrollY > Math.max(1200, window.innerHeight * 1.5));
        addEventListener('scroll', check, { passive: true });
        check();
        b.addEventListener('click', () => {
            const smooth = !matchMedia('(prefers-reduced-motion: reduce)').matches;
            window.scrollTo({ top: 0, behavior: smooth ? 'smooth' : 'auto' });
            b.blur();
        });
    }

    function init() {
        measure();
        if ('ResizeObserver' in window && top()) new ResizeObserver(measure).observe(top());
        // the lists are drawn by a script after the page loads: measure their headings when they come
        if ('MutationObserver' in window && !stickyHead()) {
            const watch = new MutationObserver(() => { if (stickyHead()) { measure(); watch.disconnect(); } });
            watch.observe(document.body, { childList: true, subtree: true });
        }
        addEventListener('resize', measure);
        backToTop();
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
