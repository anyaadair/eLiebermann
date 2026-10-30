#!/usr/bin/env node
/*
 * Liebermann prints u, but the site's font (EB Garamond) draws u as V in text
 * whose language is given as Latin (and some browsers do the same for French).
 * This check runs before every deploy (.github/workflows/static.yml) and stops
 * it if a change would bring the V back:
 *   - style.css must keep the rule that switches the font's language forms off;
 *   - no page or script may set lang= to Latin or French directly: use
 *     ELieb.setLang(el, lang) or ELieb.langAttr(lang), which write data-lang.
 *
 *   node tools/check-u-not-v.js
 */
const fs = require('fs');
const path = require('path');
const repo = path.resolve(__dirname, '..');
const problems = [];

const css = fs.readFileSync(path.join(repo, 'style.css'), 'utf8');
if (!/:root,\s*:root \*\s*\{[^}]*font-feature-settings:\s*"locl" 0/.test(css)) {
    problems.push('style.css: the rule ":root, :root * { font-feature-settings: "locl" 0; … }" is missing');
}

const LANGS = '(?:la|lat|xno|fro|frm|fr)';
const bad = [
    new RegExp(`(?<!xml:)\\blang\\s*=\\s*["']${LANGS}(?:-[\\w-]*)?["']`),   // lang="la" in markup
    new RegExp(`\\.lang\\s*=\\s*["']${LANGS}(?:-[\\w-]*)?["']`),          // el.lang = 'la'
    /\.lang\s*=\s*(?=[^\s=])(?!['"](?:de|en|ang)['"])/,                   // el.lang = someVariable
    /setAttribute\(\s*['"]lang['"]/,                                       // el.setAttribute('lang', …)
    /(?<!xml:)\blang="\$\{/                                                  // `lang="${…}"` in a template
];
const files = [];
const walk = dir => fs.readdirSync(dir, { withFileTypes: true }).forEach(d => {
    const p = path.join(dir, d.name);
    if (d.isDirectory()) { if (!/^(?:node_modules|_site|\.git|entries|oe-laws|tei|data|docs|StatutaVetera|tools)$/.test(d.name)) walk(p); }
    else if (/\.(?:html|js)$/.test(d.name)) files.push(p);
});
walk(repo);
files.forEach(f => {
    fs.readFileSync(f, 'utf8').split('\n').forEach((line, i) => {
        if (/check-u-not-v: ok/.test(line) || /^\s*(?:\/\/|\*|\/\*)/.test(line)) return;
        if (bad.some(re => re.test(line))) problems.push(`${path.relative(repo, f)}:${i + 1}: sets lang directly (use ELieb.setLang / ELieb.langAttr): ${line.trim().slice(0, 120)}`);
    });
});

if (problems.length) {
    console.error('u would be drawn as V:\n  ' + problems.join('\n  '));
    process.exit(1);
}
console.log(`check-u-not-v: ok (${files.length} files)`);
