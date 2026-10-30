/*
 * eLiebermann suggestions: a Cloudflare Worker.
 *
 * The "Suggest a change" form on the website sends its contents here; this Worker
 * checks them and opens an Issue in a private GitHub repository, so that the
 * website itself never holds a GitHub key.
 *
 * Settings (Cloudflare: the Worker > Settings > Variables and Secrets):
 *   GITHUB_TOKEN      (Secret)  a fine-grained GitHub token: only the suggestions
 *                               repository, permission "Issues: Read and write"
 *   REPO              (Text)    anyaadair/eLiebermann-suggestions
 *   ALLOWED_ORIGINS   (Text)    https://anyaadair.github.io
 *   TURNSTILE_SECRET  (Secret)  optional: the secret key of a Cloudflare Turnstile
 *                               widget (the robot check); without it, no check is made
 */
const KINDS = {
    'link': 'Missing/wrong link(s)',
    'dict': 'Add/correct dictionary link(s)',
    'other': 'Something else'
};
// addresses accepted for a link to another dictionary
const DICTIONARIES = {
    bt: { name: 'Bosworth–Toller', hosts: ['bosworthtoller.com', 'www.bosworthtoller.com', 'bosworth.ff.cuni.cz'] },
    doe: { name: 'Dictionary of Old English', hosts: ['doe.artsci.utoronto.ca', 'tapor.library.utoronto.ca', 'www.doe.utoronto.ca', 'doe.utoronto.ca'] }
};

export default {
    async fetch(request, env) {
        const origin = request.headers.get('Origin') || '';
        const allowed = (env.ALLOWED_ORIGINS || 'https://anyaadair.github.io').split(',').map(s => s.trim());
        const cors = {
            'Access-Control-Allow-Origin': allowed.includes(origin) ? origin : allowed[0],
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Vary': 'Origin'
        };
        const reply = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

        if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
        if (request.method !== 'POST') return new Response('eLiebermann suggestions: this address only receives the website’s form.', { status: 405, headers: cors });
        if (!allowed.includes(origin)) return reply({ ok: false, error: 'This form only works from the eLiebermann website.' }, 403);

        let d;
        try { d = await request.json(); } catch (e) { return reply({ ok: false, error: 'The form could not be read.' }, 400); }
        // a box people can't see: only robots fill it in
        if (d.website) return reply({ ok: true });

        if (env.TURNSTILE_SECRET) {
            const form = new FormData();
            form.append('secret', env.TURNSTILE_SECRET);
            form.append('response', String(d.turnstile || ''));
            form.append('remoteip', request.headers.get('CF-Connecting-IP') || '');
            const check = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form }).then(r => r.json()).catch(() => ({}));
            if (!check.success) return reply({ ok: false, error: 'The robot check did not pass. Please try again.' }, 400);
        }

        const clip = (s, n) => String(s == null ? '' : s).replace(/\r/g, '').trim().slice(0, n);
        const page = clip(d.page, 300);
        const headword = clip(d.headword, 120) || 'an entry';
        const kinds = (Array.isArray(d.kinds) ? d.kinds : []).filter(k => KINDS[k]);
        const text = clip(d.text, 4000);
        const links = (Array.isArray(d.links) ? d.links : []).slice(0, 10).map(l => {
            const dict = DICTIONARIES[l && l.dict];
            let url = clip(l && l.url, 500), host = '';
            try { host = new URL(url).hostname; } catch (e) { return null; }
            return dict && dict.hosts.includes(host) ? { name: dict.name, url, word: clip(l.word, 120) } : null;
        }).filter(Boolean);
        const name = clip(d.name, 120), email = clip(d.email, 200);
        if (!text && !links.length) return reply({ ok: false, error: 'Please describe the change, or add a dictionary link.' }, 400);

        const md = s => s.replace(/[<>]/g, c => (c === '<' ? '&lt;' : '&gt;'));
        const lines = [
            `**Page:** ${md(headword)}${page ? ` — ${page}` : ''}`,
            kinds.length ? `**What:** ${kinds.map(k => KINDS[k]).join(', ')}` : '',
            text ? `\n${md(text)}\n` : '',
            links.length ? '**Links to other dictionaries:**\n' + links.map(l => `- ${l.name}${l.word ? ` (${md(l.word)})` : ''}: ${l.url}`).join('\n') : '',
            '',
            `\n*From:* ${name ? md(name) : 'anonymous'}${email ? ` · ${md(email)}` : ''}`,
            `*Sent:* ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC from the eLiebermann website`
        ].filter(x => x !== '');
        const labels = [d.section === 'laws' ? 'laws' : 'dictionary'];
        if (links.length || kinds.includes('dict')) labels.push('dictionary link');
        if (kinds.includes('link') || kinds.includes('other') || (text && !kinds.length)) labels.push('correction');
        const title = `${headword}: ${kinds.map(k => KINDS[k].toLowerCase()).join(', ') || (links.length ? 'dictionary link' : 'suggestion')}`.slice(0, 200);

        const gh = await fetch(`https://api.github.com/repos/${env.REPO}/issues`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
                'User-Agent': 'eLiebermann-suggestions'
            },
            body: JSON.stringify({ title, body: lines.join('\n'), labels })
        });
        if (!gh.ok) return reply({ ok: false, error: 'The suggestion could not be saved just now. Please try again later.' }, 502);
        const issue = await gh.json();
        return reply({ ok: true, number: issue.number });
    }
};
