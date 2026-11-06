"""Liebermann cites the London text of the Willelmi articuli retractati as "Wl art Lond retr 6" (also
"retr Lond 6"). The entries had it as three separate code references (Wl art, Lond, retr), so the citations
were not linked. This joins them into one reference to Wl art retr and links each citation in the list to its
clause (WlArtRetr_6; Insc -> WlArtRetr_Inscr). Run once (Nov. 2026):  python3 tools/link-wl-art-lond-retr.py"""
import glob, os, re
R = lambda code, text: '<ref type="lawCode" target="law:%s">%s</ref>' % (code, text)
A = R('WlArt', 'Wl art') + ' ' + R('Lond', 'Lond') + ' ' + R('retr', 'retr')
B = R('retr', 'retr') + ' ' + R('Lond', 'Lond')
XR = re.compile(r'<ref target="law:Lond">Lond (retr )?(Insc|\d+[a-z]?(?:,\d+[a-z]?)*)</ref>')
files = set(os.path.basename(f)[:-4] for f in glob.glob('oe-laws/WlArtRetr_*.xml'))
changed = 0
for p in sorted(glob.glob('entries/*.xml')):
    s = open(p, encoding='utf-8').read()
    if A not in s and B not in s: continue
    o = s
    s = s.replace(A, R('WlArtRetr', 'Wl art Lond retr')).replace(B, R('WlArtRetr', 'retr Lond'))
    def link(m):
        n = m.group(2)
        cid = 'WlArtRetr_' + ('Inscr' if n == 'Insc' else n.replace(',', '-'))
        if cid not in files: return m.group(0)
        return '<ref target="clause:%s">Wl art Lond retr %s</ref>' % (cid, n)
    s = XR.sub(link, s)
    if s != o:
        s = s.replace('</revisionDesc>', '  <change when="2026-11-06">“Wl art Lond retr” (the London text of Wl art retr) made one code reference, and its citations linked (tools/link-wl-art-lond-retr.py).</change>\n    </revisionDesc>', 1)
        open(p, 'w', encoding='utf-8').write(s); changed += 1
print(changed, 'entries')
