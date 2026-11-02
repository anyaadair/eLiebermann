/*
 * eLiebermann: shows a site page kept as TEI in pages/ (Home, About), so
 * its text can be edited like any entry. The page's element names the file:
 *   <div id="site-page" data-page="Home"></div>
 */
document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('site-page');
    if (!el) return;
    const root = window.SITE_ROOT || '';
    fetch(root + 'pages/' + encodeURIComponent(el.dataset.page) + '.xml')
        .then(r => { if (!r.ok) throw new Error(r.status); return r.text(); })
        .then(text => {
            const doc = new DOMParser().parseFromString(text, 'application/xml');
            const body = doc.getElementsByTagNameNS(ELieb.TEI_NS, 'body')[0];
            let html = ELieb.renderTei(body, root);
            // The first heading is the page title.
            html = html.replace(/<h2>(.*?)<\/h2>/, '<h1>$1</h1>');
            el.innerHTML = html;
            // data-numbered: number the sections 1, 2 … and their subheadings
            // 1.1, 1.2 … (Editorial Principles), so a new section needs no renumbering.
            if (el.hasAttribute('data-numbered')) {
                let sec = 0, sub = 0;
                el.querySelectorAll('h2, h3').forEach(h => {
                    const n = h.tagName === 'H2' ? `${++sec}` : `${sec}.${++sub}`;
                    if (h.tagName === 'H2') sub = 0;
                    h.insertAdjacentHTML('afterbegin', `<span class="section-number">${n}</span> `);
                });
            }
            // Elements marked data-section="N" (e.g. a search box) belong at
            // the end of the Nth section of the page text.
            const sections = el.querySelectorAll('section');
            document.querySelectorAll('[data-section]').forEach(node => {
                const target = sections[Number(node.dataset.section) - 1];
                if (target) target.appendChild(node);
            });
        })
        .catch(() => { el.innerHTML = '<p class="notice error">This page’s text couldn’t be loaded.</p>'; });
});
