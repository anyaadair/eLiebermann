/*
 * "Suggest a change": the box at the foot of an entry page opens into a short form,
 * which is sent to a Cloudflare Worker (tools/suggest-worker/worker.js) that opens an
 * Issue in the private repository anyaadair/eLiebermann-suggestions.
 *
 *   SuggestChange.attach(box, { headword, page, section: 'dictionary' })
 *
 * Needs scripts/eliebermann.js.
 */
(function () {
    'use strict';
    // Where the form is sent, and the public key of the robot check (Cloudflare Turnstile).
    const ENDPOINT = 'https://eliebermann-suggest.notamargaret8.workers.dev/';
    const TURNSTILE_SITE_KEY = '0x4AAAAAAFsVIUpYsQELn2Q2';

    // what the suggestion is about: one or more
    const KINDS = [['link', 'Missing/wrong link(s)'], ['dict', 'Add/correct dictionary link(s)'], ['other', 'Something else']];
    const DICTS = [['bt', 'Bosworth–Toller', /^(www\.)?bosworthtoller\.com$|^bosworth\.ff\.cuni\.cz$/],
        // any address of the DOE, e.g. https://indiv.dictionary.doe.utoronto.ca/doe/?E00946 (an entry opened in its own tab)
        ['doe', 'Dictionary of Old English', /(^|\.)doe\.utoronto\.ca$|^doe\.artsci\.utoronto\.ca$|^tapor\.library\.utoronto\.ca$/]];
    const esc = s => ELieb.escapeXml(s);
    let turnstileLoading = null;
    const loadTurnstile = () => turnstileLoading || (turnstileLoading = new Promise((ok, fail) => {
        const s = document.createElement('script');
        s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
        s.async = true; s.onload = ok; s.onerror = fail;
        document.head.appendChild(s);
    }));

    function attach(box, info) {
        const intro = box.innerHTML;
        const open = () => {
            box.classList.add('suggest-change--open');
            box.innerHTML = `
                <form class="suggest-form" novalidate>
                    <h2 class="suggest-form__title">Suggest a change to <em>${esc(info.headword)}</em></h2>
                    <p class="small muted">Your suggestion goes to the editors, who check it before anything on the site changes.</p>

                    <fieldset class="suggest-form__part">
                        <legend>What is it about? <span class="muted">(choose one or more)</span></legend>
                        <div class="kind-pills kind-pills--small" role="group" aria-label="What kind of change">${KINDS.map(([k, label]) =>
                            `<button type="button" class="kind-pill" data-kind="${k}" aria-pressed="false">${esc(label)}</button>`).join('')}</div>
                        <label class="suggest-form__label" for="sg-text">Which word or number, and what should it be?</label>
                        <textarea id="sg-text" rows="4" maxlength="4000" placeholder="For example: “spreek” should link to spræc. · “1,1” should link to I Cn 1,1. · The “B” after 32 is not a manuscript."></textarea>
                    </fieldset>

                    <fieldset class="suggest-form__part suggest-form__links">
                        <legend>Add a link to another dictionary</legend>
                        <p class="small muted">Find the word in <a href="https://bosworthtoller.com/search?q=${encodeURIComponent(info.headword.replace(/[\[\]()]/g, ''))}" target="_blank" rel="noopener">Bosworth–Toller</a> or the <a href="https://doe.artsci.utoronto.ca/" target="_blank" rel="noopener">Dictionary of Old English</a>, and paste the address of its page here. (In the DOE, open the entry in a tab of its own to get its address, e.g. https://indiv.dictionary.doe.utoronto.ca/doe/?E00946.)</p>
                        <div class="suggest-form__rows"></div>
                        <button type="button" class="link-button" data-add-link>+ Add another link</button>
                    </fieldset>

                    <fieldset class="suggest-form__part suggest-form__who">
                        <legend>About you <span class="muted">(optional)</span></legend>
                        <label>Your name, for the credit <input type="text" id="sg-name" maxlength="120" autocomplete="name"></label>
                        <label>Your email, if you would like a reply <input type="email" id="sg-email" maxlength="200" autocomplete="email"></label>
                        <p class="small muted">Your email is seen only by the editors.</p>
                    </fieldset>
                    <label class="suggest-form__hp" aria-hidden="true">Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
                    <div class="suggest-form__robot"></div>

                    <p class="suggest-form__status" aria-live="polite"></p>
                    <div class="suggest-form__buttons">
                        <button type="submit" class="button">Send the suggestion</button>
                        <button type="button" class="button button--quiet" data-cancel>Cancel</button>
                    </div>
                </form>`;
            const form = box.querySelector('form');
            const rows = form.querySelector('.suggest-form__rows');
            const addRow = () => {
                const row = document.createElement('div');
                row.className = 'suggest-form__row';
                row.innerHTML = `<select aria-label="Dictionary">${DICTS.map(([k, n]) => `<option value="${k}">${esc(n)}</option>`).join('')}</select>
                    <input type="url" placeholder="https://bosworthtoller.com/…" aria-label="Address of the dictionary’s page for this word">
                    <button type="button" class="link-button" data-remove title="Take this link away" aria-label="Take this link away">✕</button>`;
                rows.appendChild(row);
            };
            addRow();
            form.addEventListener('click', e => {
                const k = e.target.closest('[data-kind]');
                if (k) k.setAttribute('aria-pressed', String(k.getAttribute('aria-pressed') !== 'true'));
                if (e.target.closest('[data-add-link]')) addRow();
                if (e.target.closest('[data-remove]')) { const r = e.target.closest('.suggest-form__row'); if (rows.children.length > 1) r.remove(); else r.querySelector('input').value = ''; }
                if (e.target.closest('[data-cancel]')) close();
            });
            form.addEventListener('change', e => {
                if (e.target.matches('select')) e.target.nextElementSibling.placeholder = e.target.value === 'bt' ? 'https://bosworthtoller.com/…' : 'https://indiv.dictionary.doe.utoronto.ca/doe/?E…';
            });
            let token = '';
            if (TURNSTILE_SITE_KEY) loadTurnstile().then(() => {
                window.turnstile.render(form.querySelector('.suggest-form__robot'), { sitekey: TURNSTILE_SITE_KEY, callback: t => { token = t; } });
            }).catch(() => {});
            const status = form.querySelector('.suggest-form__status');
            form.addEventListener('submit', e => {
                e.preventDefault();
                let kinds = [...form.querySelectorAll('[data-kind][aria-pressed="true"]')].map(b => b.dataset.kind);
                const text = form.querySelector('#sg-text').value.trim();
                const links = [], bad = [];
                rows.querySelectorAll('.suggest-form__row').forEach(r => {
                    const url = r.querySelector('input').value.trim();
                    if (!url) return;
                    const dict = DICTS.find(x => x[0] === r.querySelector('select').value);
                    let host = '';
                    try { host = new URL(url).hostname; } catch (err) { /* not an address */ }
                    if (dict && dict[2].test(host)) links.push({ dict: dict[0], url }); else bad.push(url);
                });
                status.className = 'suggest-form__status';
                if (bad.length) { status.classList.add('is-error'); status.textContent = `This doesn’t look like an address in the dictionary chosen beside it: ${bad[0]}`; return; }
                if (links.length && !kinds.includes('dict')) kinds = kinds.concat('dict');
                if (!text && !links.length) { status.classList.add('is-error'); status.textContent = 'Please describe the change, or add a dictionary link.'; return; }
                if (TURNSTILE_SITE_KEY && !token) { status.classList.add('is-error'); status.textContent = 'Please wait for the robot check below to finish, then send again.'; return; }
                const send = form.querySelector('[type=submit]');
                send.disabled = true;
                status.textContent = 'Sending…';
                fetch(ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        section: info.section || 'dictionary', headword: info.headword, page: info.page,
                        kinds, text, links,
                        name: form.querySelector('#sg-name').value.trim(), email: form.querySelector('#sg-email').value.trim(),
                        website: form.querySelector('[name=website]').value, turnstile: token
                    })
                }).then(r => r.json().catch(() => ({})).then(d => ({ ok: r.ok && d.ok, d })))
                    .then(({ ok, d }) => {
                        if (!ok) throw new Error(d.error || 'The suggestion could not be sent.');
                        box.innerHTML = `<div class="suggest-thanks"><p><strong>Thank you!</strong> Your suggestion has reached the editors.</p><button type="button" class="button button--quiet" data-again>Suggest something else</button></div>`;
                        box.querySelector('[data-again]').addEventListener('click', open);
                    })
                    .catch(err => {
                        send.disabled = false;
                        status.classList.add('is-error');
                        status.textContent = (err && err.message && !/fetch/i.test(err.message) ? err.message : 'The suggestion could not be sent.') + ' Please try again in a moment.';
                        if (window.turnstile && TURNSTILE_SITE_KEY) { try { window.turnstile.reset(); token = ''; } catch (x) { /* none */ } }
                    });
            });
            form.querySelector('[data-kind]').focus();
        };
        const close = () => { box.classList.remove('suggest-change--open'); box.innerHTML = intro; bind(); };
        const bind = () => { const b = box.querySelector('[data-open-suggest]'); if (b) b.addEventListener('click', open); };
        bind();
    }

    window.SuggestChange = { attach };
})();
