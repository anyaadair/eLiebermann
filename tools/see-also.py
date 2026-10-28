#!/usr/bin/env python3
"""
Makes the "See also" links of dictionary entries from Liebermann's own
cross-references.

    python3 tools/see-also.py --dry-run          # report only
    python3 tools/see-also.py                    # change the entries
    python3 tools/see-also.py --only a aa abbod  # just these entries

Liebermann sends the reader to another entry in two ways, and both are found
in the text of an entry (the <dictScrap type="liebermann">):

  s. WORD       "siehe": the headword, or a comma-separated list of
                headwords, straight after the italic abbreviation
                ("læde s. lad", "Genetivus ... s. asittan, aslacian").
  ... s. d.     "siehe dort": the word or words just before it, in roman
                type, between the italic German words ("ā geschrieben aa
                s. d." sends the reader to aa), and past a translation in
                brackets ("habban (erhalten) s. d." sends the reader to habban).

Each one found becomes <xr type="see"><ref target="entry:ID">headword</ref></xr>.
How a word is matched to an entry, in order:
  - the headword exactly, ignoring accents, or as one of the spellings a
    bracketed headword stands for (g[e]noh is genoh or gnoh);
  - a ~ is filled in from the entry's own headword(s): under [-feald], anf~ is
    anfeald; under hunteontig, hund~ is hundteontig;
  - a prefix or suffix with no entry of its own (heah-, -sceatt) goes to the
    word itself (heah, sceatt);
  - otherwise one usual spelling difference (ceapman / ceapmon, i / ie / y);
  - where several entries share the headword: the one numbered by a following
    I or II ("s. ure n. II"), else the one in the same language or with the
    same F / L mark, else all of them, told apart by Liebermann's first gloss.
A word in a list may have a part in round brackets, an optional part:
(sulh)æcer stands for æcer and sulhæcer, healf(marc) for healf and healfmarc,
þær(on, ~to) for þær, þæron and þærto; each word it stands for is linked.
Words cited in another form than their headword (ricsare for ricsares) are
matched by hand in FORMS.
Links a person has checked and found wrong are listed in SKIP. The report says
what was linked by a guess (to check) and what could not be linked, and why.
An entry is never linked to itself.

Existing "See also" links are kept, with one exception: a link to the entry d
is removed when the entry has "s. d." in it, since the programming that made
it read "s. d." as "see d". (They were all mistakes.)

The other kinds of cross-reference (s. o. "siehe oben", s. u. "siehe unten",
s. n., s. z., s. d. u., s. d. n.) are counted in the report but not linked.

With --compare it makes the "Compare" links instead, from Liebermann's
"vgl." / "Vgl." (vergleiche, compare): the headword or comma-separated
headwords straight after it ("vgl. heafod n. 3", "Vgl. soinus, sonet"),
matched in the same way, become <xr type="compare">…</xr>, listed after the
See links. A pointer to a section ("n. 3", "n. II") after the word is not
part of the headword. Report: docs/compare-report.md.

Writes docs/see-also-report.md (use --no-report to skip). Needs only Python 3.
Safe to run again.
"""
import argparse
import collections
import json
import glob
import html
import os
import re
import sys
import unicodedata

SIEHE = {'siehe': 'after', 'sieheDort': 'before'}      # kinds that are linked, and where the target is
OTHER = ('sieheOben', 'sieheUnten', 'sieheNummer', 'sieheZu', 'sieheDN', 'sieheDortUnter')

ABBR = re.compile(r'(?P<open><hi rend="italic">)?<ref type="abbreviation" target="gram:(?P<kind>siehe\w*)"><abbr>(?P<text>[^<]*)</abbr></ref>')
XRTYPE = 'see'
COMPARE = False
DERIV = False      # --derivatives: Liebermann's "Der." (Derivativa und Composita)
ORTH = re.compile(r'<orth>(.*?)</orth>', re.S)
SCRAP = re.compile(r'(<dictScrap type="liebermann">)(.*?)(</dictScrap>)', re.S)
SEE = re.compile(r'^[ \t]*<xr type="see"><ref target="entry:([^"]*)">.*?</ref></xr>[ \t]*\n', re.M)
SEE_ANY = re.compile(r'^[ \t]*<xr type="see"><ref target="entry:[^"]*">.*?</ref></xr>[ \t]*\n', re.M)
SEE_BEFORE = re.compile(r'^[ \t]*<xr type="(?:see|compare)"><ref target="entry:[^"]*">.*?</ref></xr>[ \t]*\n', re.M)
WORD = re.compile(r"[^\s,;:|(){}\[\]*_«»⟦⟧<>=+/]+")
# A word in a list after "s." or "vgl." may have a part in round brackets, which
# Liebermann uses for an optional part: (sulh)æcer is æcer and sulhæcer;
# healf(marc) is healf and healfmarc; þær(on, ~to) is þær, þæron and þærto.
BRACKET = r"\((?:[^()\s,]+(?:,\s*[^()\s,]+)*)\)"
TOKEN = re.compile(r"(?:" + BRACKET + r"|[^\s,;:|(){}\[\]*_«»⟦⟧<>=+/])+")

# Words Liebermann cites in another form than their headword, checked by hand:
# (entry, word as cited) -> the entry it means.
FORMS = {
    ('a-6', 'ricsare'): 'ricsares',        # headword is the plural
    ('a-6', 'mæstan'): 'maest',            # weak form of mæst (which points on to micel)
    ('a-6', 'tæcean'): 'taecan',           # a form listed under tæcan
    ('a-6', 'healfmarc'): 'healfmearc',
    ('a-6', 'heall'): 'healle',            # headword is the dative
    ('a-6', 'healm'): 'healme',            # headword is the dative
    ('a-6', 'Westsaxones'): 'Westseax-e',  # Latin form of the name
    ('a-6', 'wealdes'): 'gewealdes',       # "(unge)wealdes": no entry wealdes; editor's note on the entry
    ('Abkurzungen', 'm'): 'm',             # "man(n) durch m s. d.": the OE abbreviation m̃, not Latin or French m
    ('Abkurzungen', 'sanct'): 'sancte',    # "sca, sce, scs s. sanct": the entry is sancte
    ('thaet-2', 'for'): 'for',             # "s. be, for, to": the preposition, not for (denn)
    ('thaet-2', 'oð'): 'od-3',             # "vgl. oð (n. I C) þæt": the preposition oð
    ('Accusativ', 'Genetiv'): 'Genetivus', # "s. Genetiv, Dativ"
    ('ea', 'lafe'): 'laf',                 # "von ā: s. lafe": a form of laf
    ('ea', 'botettan'): 'boteatan',
    ('ae-4', 'ablendan'): 'ablendad',      # the only form in the laws, ablendað
    ('ae-4', 'lenden'): 'lendenbraede', ('ae-4', 'lenden-'): 'lendenbraede',
    ('ae-4', 'nemnan'): 'nemne', ('numer', 'nemnan'): 'nemne',   # the verb, entered under its only form, nemne (op 3)
    ('ae-4', 'utoðberstan'): 'utodberste',
    ('ae-4', 'geeahtian'): 'geeahtige',
    ('ae-4', 'freondleast'): 'freondleaste',
    ('ae-4', 'sceapætere'): 'sc-ea-paetere',
    ('ae-4', 'unliegne'): 'unl-ie-gen',
    ('ae-4', 'healm'): 'healme', ('haelm', 'healm'): 'healme',   # no entry healm: the phrase to healme ⁊ to heorðe (editor's notes)
    ('aefen', 'freolsæ~'): 'freolsaefenan',
}

# "habban (erhalten) s. d.": Liebermann's translation in brackets between the word and its s. d.
GLOSS = re.compile(r'\s*\(<hi rend="italic">[^<>()]*</hi>\)\s*$')
# "z. B." (zum Beispiel) straight after "s." or "vgl.": the list follows it
ZB = re.compile(r'\s*(?:</hi>\s*)?(?:<hi rend="italic">\s*)?<ref type="abbreviation" target="gram:zumBeispiel"><abbr>z\. B\.</abbr></ref>(?:</hi>)?')

# What targets() found for each word it read, for linking the words in the
# text (tools/link-headwords.py): [(kind, n-th abbreviation, raw token, [(segment, ids)])]
INLINE = []

# "þas (unter þes)", "mæn (unter mann)", "dæð (3. sg. unter don)", "eart [unter eom]": Liebermann sends the reader to
# the word after "unter" (under), where the form is entered. The list is read on past the bracket,
# and the word after "unter" is linked instead of the form. UNTER is the italic "unter" in the
# markup; UNTER_FORMS records, per entry, the forms so replaced, whose old links are taken off.
UNTER = re.compile(r'<hi rend="italic">((?:[^<]|<(?!/?hi\b)[^>]*>){0,200}?\bunter)</hi>'
                   # and, read through in the same way inside a list, "ofslæhð (s. ofslean)" and "eligere n. 2, …"
                   r'|(?<=\()<hi rend="italic">(<ref type="abbreviation" target="gram:siehe"><abbr>s\.</abbr></ref>)</hi>(?=\s*[^\s()<]+\))'
                   r'|<hi rend="italic">(<ref type="abbreviation" target="gram:Nummer"><abbr>n\.</abbr></ref>)</hi>(?=\s*(?:[IVX]+|\d+)[a-z]?\s*,)')
UNTER_BRACKET = re.compile(r'\s*[(\[](?:[^()\[\]]*?\s)?(?:unter|s\.)\s+([^\s()\[\],;<]+)[)\]]|\s+unter\s+([^\s\[\],;<]+(?:\([^()\s]+\))?[^\s\[\],;<()]*)')
# "eligere n. 2, electio": a pointer to a numbered meaning, after a word in a list
SECTION_IN_LIST = re.compile(r',?\s+n\.\s*(?:[IVX]+|\d+)[a-z]?(?=\s*,)')
UNTER_FORMS = collections.defaultdict(set)
KIND = ['']    # the kind of cross-reference being read ("siehe", "sieheDort" …), for resolve()


def read(path):
    with open(path, encoding='utf-8', newline='') as f:
        return f.read()


def fold(s):
    s = unicodedata.normalize('NFD', s.lower()).replace('ð', 'þ')
    return ''.join(c for c in s if not unicodedata.combining(c))


# Links the tool would make that a person has checked and found wrong:
# (entry, target). The near spellings and stems are guesses, and these missed.
SKIP = {
    ('Pars', 'helm'), ('ae-4', 'helm'), ('haelm', 'helm'),        # healm is not helm
    ('Consonanten', 'l'), ('l-2', 'l'),                          # ll: the double letter
    ('maector', 'mete'),                                         # mæte is not mete
    ('fiht', 'f-re-ht'), ('fyht', 'f-re-ht'),                    # feoht is not freht
    ('Fremdwort-Declination', 'tu-sc'), ('Fremdwort-Declination', 'te'),
    ('cs', 'g-o-s'), ('gar', 'waru'),
    ('Abkurzungen', 'm-2'), ('Abkurzungen', 'm-3'),                # the Latin and French m, not the OE m̃
    ('thaet-2', 'i'),                                            # "se I [s. d.]": the numeral of se I (linked by hand), not the letter i
    ('Aed', 'Aead'), ('Ed', 'Aead'), ('e-3', 'Aead'),                # "Ead-": the Ead- words, not the pointer Æad-
    ('thaet-2', 'for-2'),                                        # "be, for, to": the preposition, not for (denn)
}

ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}
SECTION = re.compile(r'^\s*(?:<lbl[^>]*>[^<]*</lbl>\s*)?<hi rend="bold">(I|II|III|IV|V)</hi>\)')


def spellings(hw):
    """The forms a headword with Liebermann's brackets stands for:
    g[e]noh -> genoh, gnoh; aw[ie]rdan -> awierdan, awrdan, awirdan, awerdan;
    mon(n)- -> monn-, mon-."""
    parts = re.split(r'(\[[^\]]*\]|\([^)]*\))', hw)
    forms = ['']
    for part in parts:
        if re.fullmatch(r'\[[^\]]*\]|\([^)]*\)', part or ''):
            inner = part[1:-1]
            opts = {inner}
            if part.startswith('('):
                opts.add('')                # heal(swa): healswa or heal
            elif len(inner) > 1 and inner.isalpha():
                opts.update(inner)          # [ie]: ie, i or e
            else:
                opts.add('')                # g[e]noh: genoh or gnoh
            forms = [f + o for f in forms for o in opts]
        else:
            forms = [f + part for f in forms]
        if len(forms) > 64:
            break
    return {f for f in forms if f}


def respellings(word):
    """Common spelling differences between Liebermann's cross-references and
    his headwords (ceapman / ceapmon, cierr / cyrr, ...): one change at a time."""
    swaps = [('an', 'on'), ('on', 'an'), ('ie', 'i'), ('ie', 'y'), ('i', 'ie'), ('y', 'ie'), ('i', 'y'), ('y', 'i'),
             ('æ', 'e'), ('e', 'æ'), ('ea', 'e'), ('eo', 'e'), ('io', 'eo'), ('eo', 'io'), ('u', 'o'), ('o', 'u'),
             ('c', 'k'), ('k', 'c'), ('nn', 'n'), ('ll', 'l'), ('n', 'nn'), ('l', 'll'), ('tt', 't'), ('t', 'tt'),
             ('mm', 'm'), ('ss', 's'), ('dd', 'd'), ('gg', 'g')]
    out = set()
    for a, b in swaps:
        for m in re.finditer(re.escape(a), word):
            out.add(word[:m.start()] + b + word[m.end():])
    # a verb in -cean, -gean: feccean / feccan, (ge)þencean / þencan
    if re.search(r'[cg]ean$', word):
        out.add(word[:-3] + 'an')
    out.discard(word)
    return out


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Index:
    """Headword -> entry ids, for every file in entries/."""
    def __init__(self, directory):
        self.hw = {}
        self.exact = collections.defaultdict(list)
        self.folded = collections.defaultdict(list)
        self.variant = collections.defaultdict(list)
        self.lang = {}
        self.section = {}
        self.pointer = set()
        self.mark = {}
        self.gloss = {}
        self.spelling = set()      # entries for a spelling (a letter or letters): <usg type="dom">spelling</usg>
        self.grammatical = set()   # Liebermann's grammatical entries (Declination, Genetivus …)
        self.text = {}             # each entry's text, plain
        self.xref = {}             # an entry that only sends the reader to another (type="xref"): -> that entry's id
        for path in sorted(glob.glob(os.path.join(directory, '*.xml'))):
            text = read(path)
            m = ORTH.search(text)
            if not m:
                continue
            id_ = os.path.basename(path)[:-4]
            lm = re.search(r'<entry xml:lang="([^"]*)"', text)
            self.lang[id_] = lm.group(1) if lm else ''
            sm = SCRAP.search(text)
            if '<usg type="dom">spelling</usg>' in text:
                self.spelling.add(id_)
            if re.search(r'<entry [^>]*type="grammatical"', text):
                self.grammatical.add(id_)
            if re.search(r'<entry [^>]*type="xref"', text):
                xm = re.search(r'<xr type="see"><ref target="entry:([^"]+)"', text)
                self.xref[id_] = xm.group(1) if xm else ''
            self.text[id_] = html.unescape(re.sub(r'<[^>]+>', '', sm.group(2))) if sm else ''
            nm = SECTION.match(sm.group(2)) if sm else None
            # Liebermann's first italic word after the headword ("vb", "Recht"),
            # to tell apart entries that share a headword
            for gm in re.finditer(r'<hi rend="italic">(.*?)</hi>', sm.group(2) if sm else ''):
                g = html.unescape(re.sub(r'<[^>]+>', '', gm.group(1))).strip(' ,;:.[]()')
                if len(re.sub(r'\W', '', g)) < 2 or g.startswith('s.') or g in ('s', 'vgl'):
                    continue
                self.gloss[id_] = g if len(g) <= 24 else g[:22].rsplit(' ', 1)[0] + '…'
                break
            # Liebermann's L / F before a headword (Latin, French)
            lb = re.match(r'\s*<lbl type="language">([^<]*)</lbl>', sm.group(2)) if sm else None
            self.mark[id_] = lb.group(1).strip() if lb else ''
            # an entry that is only a pointer elsewhere ("hwirfe s. hwier~")
            if sm:
                body = re.sub(r'<hi rend="bold">.*?</hi>', '', sm.group(2), count=1)
                # "Æad-, Æalf- s. …": a second headword after the first
                body = re.sub(r'^(\s*,\s*<hi rend="bold">.*?</hi>)+', '', body)
                body = html.unescape(re.sub(r'<[^>]+>', '', body)).strip(' ,')
                if body.startswith('s.') and len(body) < 60:
                    self.pointer.add(id_)
            # an entry joined from Liebermann's numbered sections (þæt I–IV) is
            # one entry: it is not labelled by its first section
            if nm and not re.search(r'<hi rend="bold">(?:II|III|IV|V)</hi>\)', sm.group(2)[nm.end():]):
                self.section[id_] = nm.group(1)
            hw = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
            self.hw[id_] = hw
            # Names that are not in the text of the laws are headed [Wiht]; a
            # reference to them has no brackets.
            plain = re.sub(r'^\[(.*)\]$', r'\1', hw)
            # one entry with two headwords ("æfwerdelsan, æfw[i]erdlan"): each
            # headword is looked up on its own as well
            heads = [plain] + ([h for h in re.split(r',\s*', plain) if h] if re.search(r'\w,\s+\w', plain) else [])
            for head in heads:
                if id_ not in self.exact[head]:
                    self.exact[head].append(id_)
                if id_ not in self.folded[fold(head)]:
                    self.folded[fold(head)].append(id_)
                for form in spellings(head):
                    if form != head and id_ not in self.variant[fold(form)]:
                        self.variant[fold(form)].append(id_)

    def gram_xrefs(self):
        """Grammatical headwords that Liebermann's abbreviations list also has, so that they
        are linked to it in the text: "s. Decl.", "vgl. Gleitlaut". -> {abbreviation anchor:
        [entry ids]}, for the words of four letters or more (not the labels ac, pl, sg)."""
        if hasattr(self, '_gx'):
            return self._gx
        self._gx, self.gram_text, self.gram_anchor = {}, {}, {}
        override = {'FremdworterDeclination': 'Fremdwort-Declination'}
        rows = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'markforward.json'), encoding='utf-8'))
        for r in rows:
            text, exp = r.get('Gesetze Text', '').strip(), (r.get('German Expansion') or '').strip()
            if len(re.sub(r'\W', '', text)) < 4 or not exp:
                continue
            ids = sorted(i for i in self.grammatical if self.hw[i].lower() == exp.lower() or i == override.get(r['Anchor']))
            if ids:
                self._gx[r['Anchor']] = ids
                self.gram_text[text.rstrip('.')] = ids
                self.gram_anchor[text] = r['Anchor']
        return self._gx

    def lookup(self, word):
        """Every entry with this headword (exactly, then ignoring accents, then
        as one of the spellings a bracketed headword stands for)."""
        for table, key in ((self.exact, word), (self.folded, fold(word)), (self.variant, fold(word))):
            if table.get(key):
                return list(table[key])
        return []

    def label(self, id_):
        hw = re.sub(r'^\[(.*)\]$', r'\1', self.hw.get(id_, id_))
        return hw + (' ' + self.section[id_] if id_ in self.section else '')

    def find(self, word, lang='', numeral='', mark=None, self_entry=''):
        """-> (list of ids, why not / how)"""
        ids = self.lookup(word)
        how = ''
        if not ids:
            # A prefix or suffix (heah-, -sceatt) with no entry of its own: the
            # entry for the word itself.
            bare = word.strip('-')
            if bare != word and len(bare) > 2:
                ids = self.lookup(bare)
                how = 'linked to the word without the hyphen' if ids else ''
        if not ids and word.endswith('-') and not word.startswith('-') and len(re.sub(r'\W', '', word)) >= 3 and lang != 'de':
            # "Aelf-": no entry of that name, but words beginning so; the first of them
            # (Ælfgifu), from which the reader can go on with "Next". Only within the
            # entry's own language, and a capital only finds names.
            key = lambda h: re.sub(r'[\u0300-\u036f]', '', unicodedata.normalize('NFD', re.sub(r'[\[\]()\-~]', '', h))).lower().replace('æ', 'ae').replace('ð', 'þ')
            pre = key(word)
            cap = word.lstrip('[(')[:1].isupper()
            # "(woruld)gew- " in the entry -wuna: the prefix and this entry's word (gewuna)
            own = key(self.hw.get(self_entry, '')) if self_entry else ''
            whole = [i for i, h in self.hw.items() if own and key(h) == pre + own and self.lang.get(i) == lang]
            if len(whole) == 1:
                return whole, 'the prefix and this entry\'s word'
            starts = sorted((key(h), i) for i, h in self.hw.items()
                            if i not in self.pointer and key(h).startswith(pre) and self.lang.get(i) == lang
                            and re.sub(r'^[\[\(]+', '', h)[:1].isupper() == cap)
            if starts and self_entry in self.pointer and len(starts) <= 12:
                # an entry that only sends the reader on ("Æad-, Æalf- s. Ead-, Ælf-"): every
                # word that begins so (Eadbald, Eadgar, Eadmund, Eadweard); the first in the text
                return [i for _, i in starts], 'every word that begins so (a word ending in "-"), from an entry that only points'
            if starts:
                return [starts[0][1]], 'the first word that begins so (a word ending in "-")'
        if not ids and re.fullmatch(r'[A-ZÄÖÜ][a-zäöü]{2,}\.?', word):
            # "s. Decl.": a grammatical headword abbreviated (Declination)
            stem = word.rstrip('.')
            g = [i for i in self.grammatical if self.hw[i].startswith(stem)]
            if len(g) == 1:
                return g, 'a grammatical headword, abbreviated: ' + self.hw[g[0]]
        if not ids:
            cands = sorted({i for r in respellings(fold(word)) for i in self.lookup(r) if i not in self.pointer})
            if len(cands) == 1:
                return cands, 'linked by a near spelling: ' + self.hw[cands[0]]
            if cands:
                return [], 'no entry with this headword; near spellings: ' + ', '.join(cands)
            return [], 'no entry with this headword (yet)'
        if len(ids) == 1:
            return ids, how
        if numeral:
            pick = [i for i in ids if self.section.get(i) == numeral]
            if len(pick) == 1:
                return pick, how
        same = [i for i in ids if self.lang.get(i) == lang]
        if len(same) == 1:
            return same, how
        if same:
            ids = same
        if mark is not None:
            same = [i for i in ids if self.mark.get(i, '') == mark]
            if len(same) == 1:
                return same, how
            if same:
                ids = same
        return ids, 'several entries have this headword, all linked: ' + ', '.join(ids)


def words(text, backwards=False):
    """The list of words in a stretch of plain text, where the words are
    separated by commas: 'ea, o' -> ['ea', 'o']. Going forwards it stops at the
    first thing that is not a word or comma; going backwards, at the last."""
    out = []
    words.left = words.right = ''
    words.unter = []
    if not backwards:
        rest = text
        while True:
            m = re.match(r'\s*(' + TOKEN.pattern + ')', rest)
            if not m or not re.search(r'[^\W\d_~-]', re.sub(BRACKET, '', m.group(1)) or m.group(1)):
                break
            out.append(m.group(1))
            rest = rest[m.end():]
            sm2 = SECTION_IN_LIST.match(rest)
            if sm2:
                rest = rest[sm2.end():]
            um = UNTER_BRACKET.match(rest)
            if um:
                # "þas (unter þes)": the word after "unter" stands for the form
                to = um.group(1) or um.group(2)
                if re.search(r'\bauch\s+unter', um.group(0)):
                    out.append(to)          # "man [auch unter manige]": both
                else:
                    words.unter.append((out[-1], to))
                    out[-1] = to
                rest = rest[um.end():]
            if DERIV:
                # "aberan (aberendlic)": the word in brackets is a derivative too
                pm = re.match(r'\s+\(([^()\s,]+)\)', rest)
                if pm and re.search(r'[^\W\d_]', pm.group(1)):
                    out.append(pm.group(1))
                    rest = rest[pm.end():]
                # "ofa~; uta~", "midb~ | æðelboren": the list goes on
                if re.match(r'\s*[;|]\s*(?=[^\W\d_~(])', rest):
                    rest = re.sub(r'^\s*[;|]', ',', rest)
            # "[vgl. æwe; æwum]": in a bracketed vgl. list, a last word after ";" belongs to it
            if COMPARE and re.match(r'\s*;\s*[^\W\d_][\w\-]*\s*(?:\]|$)', rest):
                rest = re.sub(r'^\s*;', ',', rest)
            if not re.match(r'\s*,\s*(?=\S)', rest) or re.match(r'\s*,\s*[\[]', rest):
                break
            rest = re.sub(r'^\s*,', '', rest)
        words.right = rest
        return out
    rest = text.rstrip()
    # "den[arius] s. d.": an abbreviation with Liebermann's expansion in square brackets
    m = re.search(r'(?<![^\s|;,])([^\W\d_]+(?:\[[^\W\d_]+\][^\W\d_]*)+)[\s.;:,]*$', rest) or \
        re.search('(' + WORD.pattern + r')[\s.;:,]*$', rest)
    if m:
        out.append(m.group(1))
        rest = rest[:m.start()]
        while re.search(r',\s*$', rest):          # more words in the same comma-separated list
            m = re.search('(' + WORD.pattern + r')\s*,\s*$', rest)
            if not m:
                break
            out.append(m.group(1))
            rest = rest[:m.start()]
        words.left = rest                           # what is in front of the list
    return out[::-1]


def expand(word):
    """The parts of a word as written, each with the word it stands for:
    (sulh)æcer -> [('sulh', 'sulhæcer'), ('æcer', 'æcer')];
    þær(on, ~to) -> [('þær', 'þær'), ('on', 'þæron'), ('~to', 'þærto')];
    a word with no brackets -> [(word, word)]."""
    parts = re.split('(' + BRACKET + ')', word)
    if len(parts) == 1:
        return [(word, word)]
    plain = [p for p in parts if not re.fullmatch(BRACKET, p)]
    base = ''.join(plain)
    out = []
    for n, p in enumerate(parts):
        if not p:
            continue
        if not re.fullmatch(BRACKET, p):
            out.append((p, base))
            continue
        before = ''.join(x for x in parts[:n] if not re.fullmatch(BRACKET, x))
        after = ''.join(x for x in parts[n + 1:] if not re.fullmatch(BRACKET, x))
        for alt in re.split(r',\s*', p[1:-1]):
            if '~' in alt:
                form = alt.replace('~', before) + after
            else:
                form = before + alt + after
            out.append((alt, form))
    return out


def clean(token):
    return token.strip().rstrip('.,;:')


def headwords(scrap, index, entry_id):
    """The entry's own headword(s), for filling in a ~: the orth, and any other
    bold words before Liebermann's first abbreviation ("wys, wyssian")."""
    out = [index.hw.get(entry_id, '')]
    head = scrap.split('<ref type="abbreviation"', 1)[0]
    out += [html.unescape(re.sub(r'<[^>]+>', '', h)) for h in re.findall(r'<hi rend="bold">(.*?)</hi>', head)]
    forms = []
    for h in out:
        h = h.strip().strip('[]').strip().rstrip(',').strip('-')
        if h and not re.fullmatch(r'[IVX]+|\d+[a-z]?', h):
            for f in spellings(h) | {re.sub(r'[\[\]()]', '', h)}:
                if f not in forms:
                    forms.append(f)
    return forms


def tilde(word, h):
    """Liebermann's ~ stands for letters of the headword h: under [-feald],
    anf~ is anfeald; under Bernaba, Bar~ is Barnaba; under ciepemon, ~nna is
    ciepemonna; under hunteontig, hund~ is hundteontig. -> the possible
    spellings, the likeliest (where a letter is shared) first. The ~ always
    stands for at least one letter."""
    pre, _, post = word.partition('~')
    first, second = [], []
    if not pre and not post:
        return [], []
    if pre and post:
        return [pre + h + post], []
    for k in range(1, len(h)):
        if pre:
            stands, shared = len(h) - k, pre[-1].lower() == h[k - 1].lower()
            cand = pre + h[k:]
        else:
            stands, shared = k, post[0].lower() == h[k].lower()
            cand = h[:k] + post
        # the ~ stands for a fair part of the headword: two letters at least
        # where a letter is shared, more than half the word where none is
        if shared and stands >= min(2, len(h) - 1):
            first.append(cand)
        elif not shared and 2 * stands > len(h):
            second.append(cand)
    if pre:
        second.append(pre + h)
    return first, second


def resolve(word, index, lang, numeral, heads, entry_id=''):
    """-> (ids, why/how, shown)"""
    if '~' in word:
        picked, seen, tried = [], [], []
        for h in heads:
            got = tilde(word, h)
            # where no likely spelling is a headword, try them with the usual
            # spelling differences (ungielde -> ung[i]lde) before the less likely ones
            got = (got[0], sorted({r for c in got[0] for r in respellings(c)}), got[1])
            for n, group in enumerate(got):
                found = {}
                for cand in group:
                    tried.append(cand)
                    ids = [i for i in index.lookup(cand) if i != entry_id and not (n == 1 and i in index.pointer)]
                    if ids:
                        found.setdefault(tuple(ids), cand)
                if len(found) == 1:
                    picked.append(list(found.values())[0])
                    break
                if found:
                    seen += list(found.values())
                    break
        picked = list(dict.fromkeys(picked))
        # several headwords, several readings: keep those in the entry's own language
        same = [c for c in picked if any(index.lang.get(i) == lang for i in index.lookup(c))]
        if same:
            picked = same
        if picked and len(picked) <= 3:
            ids, whys = [], []
            for cand in picked:
                got, why = index.find(cand, lang, numeral, index.mark.get(entry_id, ''))
                got = [i for i in got if i != entry_id] or [i for i in index.lookup(cand) if i != entry_id]
                ids += [i for i in got if i not in ids]
            return ids, '~ read as ' + ', '.join(picked), ' / '.join(picked)
        if seen:
            return [], 'only the start or end of a word: ~ could be ' + ', '.join(seen), word
        return [], 'only the start or end of a word: no entry for it', word
    if re.search(r'\d', word):
        return [], 'a number, not a headword', word
    index.gram_xrefs()
    if word.rstrip('.') in index.gram_text:
        # "s. Decl.", "vgl. Gleitlaut": the grammatical entry (of two, the one in the
        # entry's own language: Artikel, not the French Artikel)
        ids = index.gram_text[word.rstrip('.')]
        pick = [i for i in ids if index.mark.get(i, '') == index.mark.get(entry_id, '')] or ids
        return pick[:1], 'a grammatical entry, linked to the abbreviations list in the text', word
    if entry_id in index.spelling and KIND[0] == 'sieheDort' and re.fullmatch(r'[a-zæðþƿȝ]{1,3}', fold(word)):
        # From a spelling entry, "a, æ, e, eo s. d." are the spelling entries for those
        # letters in the same language ("a-", "-e", "-eo-"); of several, the one that lists
        # spellings "von" (for) this entry's letters
        forms = {word, word + '-', '-' + word, '-' + word + '-'}
        cands = [i for i in index.spelling if i != entry_id and index.lang.get(i) == lang
                 and fold(index.hw[i]).replace(',', ' ').split() and
                 any(fold(f) in [fold(x) for x in re.split(r'[,\s]+', index.hw[i]) if x] for f in forms)]
        if len(cands) > 1:
            own = re.sub(r'[^a-zæðþ]', '', fold(index.hw.get(entry_id, '')).split(',')[0])
            pick = [i for i in cands if re.search(r'\bvon\s+' + re.escape(own) + r'\b', fold(index.text.get(i, '')))]
            if pick:
                cands = pick
        if cands:
            # what the word found before this rule (the word a, the French e …) comes off the list
            UNTER_FORMS[entry_id].update(i for i in index.find(word, lang, numeral, index.mark.get(entry_id, ''))[0] if i not in cands)
            UNTER_FORMS[entry_id].update(i for i in index.lookup(word) if i not in cands)
            return cands, 'the spelling entry for these letters, from a spelling entry', word
    ids, why = index.find(word, lang, numeral, index.mark.get(entry_id, ''), entry_id)
    return ids, why, word


def targets(scrap, entry_id, index):
    """Every cross-reference in an entry's text:
    [(kind, shown text, [ids], why not / how)]"""
    found = []
    lang = index.lang.get(entry_id, '')
    # A headword that is also a law code (Ine, Wiht ...) is linked as one in the
    # text; for finding the word, that link is only the word.
    scrap = re.sub(r'<ref type="lawCode" target="[^"]*">([^<]*)</ref>', r'\1', scrap)
    scrap = strip_entry_links(scrap)
    scrap = unwrap_gram_xrefs(scrap, index)
    # an editor's note marker in a list (<ptr type="editorNote"/>) is not part of the text
    scrap = re.sub(r'<ptr type="editorNote"[^>]*/>', '', scrap)
    heads = headwords(scrap, index, entry_id)
    for abbr_n, m in enumerate(ABBR.finditer(scrap)):
        kind = m.group('kind')
        KIND[0] = kind
        if kind in OTHER:
            found.append((kind, m.group('text'), [], 'not linked: ' + kind))
            continue
        if kind not in SIEHE:
            continue
        after = ''
        if SIEHE[kind] == 'after':
            tail = scrap[m.end():]
            if COMPARE and tail.startswith('.'):
                tail = tail[1:]                 # "vgl</abbr></ref>.": the full stop is outside the link
            if DERIV and tail.startswith(':'):
                tail = tail[1:]                 # "Der.</abbr></ref>:": the colon is outside the link
            # "s. z. B. and, hand": the words come after Liebermann's "z. B." (for example)
            zb = ZB.match(tail)
            if zb:
                tail = ' ' + tail[zb.end():]
            if tail.startswith('</hi>'):
                tail = tail[5:]
            # an italic "unter" inside the list ("þas (<hi>unter</hi> þes)") does not end it
            tail = UNTER.sub(lambda m: re.sub(r'<[^>]+>', '', m.group(1) or m.group(2) or m.group(3)), tail)
            node = re.split(r'<', tail, maxsplit=1)[0]
            if not node[:1].isspace():
                found.append((kind, '', [], 'nothing follows'))
                continue
            toks = words(node)
            for form, _ in words.unter:
                ids, _, _ = resolve(clean(html.unescape(form)), index, lang, '', heads, entry_id)
                UNTER_FORMS[entry_id].update(ids)
            after = words.right + tail[len(node):]
        else:
            head = scrap[:m.start()]
            gloss = GLOSS.search(head)
            if gloss:
                head = head[:gloss.start()] + ' '
            node = re.split(r'>', head[::-1], maxsplit=1)[0][::-1] if '>' in head else head
            before = head[:len(head) - len(node)]
            # "pares [s. d.]": the bracket belongs to the s. d.
            node = re.sub(r'\[\s*$', '', node)
            toks = words(html.unescape(node), backwards=True)
            if len(toks) > 1 and before.endswith('</hi>') and re.search(r'<hi rend="bold">[^<]*</hi>$', before) \
                    and node.lstrip().startswith(toks[0]):
                toks = toks[1:]     # "hereditaria terra, bocland": terra belongs to the headword
        # "s. ure n. II", "s. riht II": which of several entries
        plain_after = html.unescape(re.sub(r'<[^>]+>', '', after))
        if COMPARE:
            # "vgl. heafod n. 3", "vgl. oð (n. I C) þæt": a pointer to a section is not part of the word
            sec = re.match(r'\s*\(?n\.\s*[IVX\d][\w ,]*\)?', plain_after)
            if sec and toks:
                words.right = re.sub(r'^\s*\(?n\.\s*[IVX\d][\w ,]*\)?', '', html.unescape(re.sub(r'<[^>]+>', '', words.right)))
                nm2 = re.match(r'\s*\(?n\.\s*(I{1,3}|IV|V)\b', plain_after)
                plain_after = (' ' + nm2.group(1)) if nm2 else ''
        nm = re.match(r'\s*(?:n\.\s*)?(I{1,3}|IV|V)\b(?!\s*\))', plain_after)
        numeral = nm.group(1) if nm else ''
        if nm:
            words.right = words.right[len(words.right) - len(words.right.lstrip()):]
            words.right = re.sub(r'^\s*(?:n\.\s*)?(I{1,3}|IV|V)\b', '', words.right)
        phrase = bool(toks) and (
            (SIEHE[kind] == 'after' and not numeral and re.match(r"\s+[^\W\d_]", words.right)) or
            (SIEHE[kind] == 'before' and re.search(r"[^\W\d_][\w'’.]*\s+$", words.left)))
        if not toks:
            found.append((kind, '', [], 'no word found'))
        elif phrase:
            found.append((kind, ' '.join(toks), [], 'part of a longer phrase, not a single headword'))
            toks = []
        if COMPARE and toks:
            right = html.unescape(re.sub(r'<[^>]+>', '', words.right))
            if re.match(r'\s+\d', right) or right.startswith('('):
                # "vgl. Ine 75": a citation; "ma(a)nsceaða": the word goes on
                found.append((kind, ' '.join(toks), [], 'a citation or a longer word, not a headword'))
                toks = []
        for i, tok in enumerate(toks):
            word = clean(html.unescape(tok))
            if not word:
                continue
            if COMPARE and len(word.strip('-')) <= 1:
                found.append((kind, word, [], 'a single letter, not a headword'))
                continue
            segments, seen_forms = [], {}
            # "den[arius]": the word written out, linked as a whole
            parts = [(word, word.replace('[', '').replace(']', ''))] if re.search(r'\w\[\w+\]', word) else expand(word)
            for seg, form in parts:
                if form not in seen_forms:
                    if (entry_id, form) in FORMS:
                        ids, why, shown = [FORMS[(entry_id, form)]], 'checked by hand: ' + FORMS[(entry_id, form)], form
                    else:
                        ids, why, shown = resolve(form, index, lang, numeral if i == len(toks) - 1 else '', heads, entry_id)
                    if any((entry_id, x) in SKIP for x in ids):
                        ids = [x for x in ids if (entry_id, x) not in SKIP]
                        why = why or 'checked and found wrong'
                    if entry_id in ids:
                        ids = [x for x in ids if x != entry_id]
                        why = why or 'this entry itself'
                    seen_forms[form] = ids
                    found.append((kind, shown, ids, why))
                segments.append((seg, seen_forms[form]))
            INLINE.append((kind, abbr_n, tok, segments))
    return found


def unwrap_gram_xrefs(scrap, index):
    """The text with a grammatical headword that is linked to the abbreviations list, straight
    after "s.", "vgl." or "s. d." ("s. <ref …gram:Declination>Decl.</ref>"), as plain text, so
    that it is read as a cross-reference to that entry."""
    gx = index.gram_xrefs()
    pat = re.compile(r'(target="gram:(?:siehe|vergleiche|sieheDort)"><abbr>[^<]*</abbr></ref>\.?(?:</hi>)?\s*(?:<hi rend="italic">)?)'
                     r'<ref type="abbreviation" target="gram:([^"]+)"><abbr>([^<]*)</abbr></ref>')
    return pat.sub(lambda m: m.group(1) + m.group(3) if m.group(2) in gx and m.group(3).rstrip('.') in index.gram_text else m.group(0), scrap)


def rewrap_gram_xrefs(scrap, index):
    """Undo unwrap_gram_xrefs(): the word links to the abbreviations list again. Where it
    became a link to its entry, that link goes on a small arrow after it ("s. Decl.↗"),
    so the reader has both."""
    index.gram_xrefs()
    if not index.gram_anchor:
        return scrap
    prefix = r'(target="gram:(?:siehe|vergleiche|sieheDort)"><abbr>[^<]*</abbr></ref>\.?(?:</hi>)?\s*(?:<hi rend="italic">)?)'
    def jump(m):
        text = m.group(3) + m.group(4)
        anchor = index.gram_anchor.get(text) or index.gram_anchor.get(m.group(3))
        if not anchor:
            return m.group(0)
        shown = text if text in index.gram_anchor else m.group(3)
        rest = m.group(4) if shown == m.group(3) else ''
        return m.group(1) + '<ref type="abbreviation" target="gram:%s"><abbr>%s</abbr></ref>%s<ref type="entry" subtype="jump" target="entry:%s"/>' % (anchor, shown, rest, m.group(2))
    scrap = re.sub(prefix + r'<ref type="entry" target="entry:([^"]+)">([^<]*)</ref>(\.?)', jump, scrap)
    words = '|'.join(sorted(map(re.escape, index.gram_anchor), key=len, reverse=True))
    pat = re.compile(r'(target="gram:(?:siehe|vergleiche|sieheDort)"><abbr>[^<]*</abbr></ref>\.?(?:</hi>)?\s*(?:<hi rend="italic">)?)(' + words + r')(?![\w.])')
    return pat.sub(lambda m: m.group(1) + '<ref type="abbreviation" target="gram:%s"><abbr>%s</abbr></ref>' % (index.gram_anchor[m.group(2)], m.group(2)), scrap)


def strip_entry_links(scrap):
    """The text without the links on cross-referenced words (tools/link-headwords.py).
    A link made by hand (<ref type="entry" subtype="manual" …>) is kept."""
    scrap = re.sub(r'<ref type="entry" subtype="jump"[^>]*/>', '', scrap)
    return re.sub(r'<ref type="entry" target="[^"]*">(.*?)</ref>', r'\1', scrap)


def labels(final, index):
    """The text of each link; where two would read the same, an entry that only sends
    the reader on is named by where it sends him ("e for et"), and of the rest, if
    more than one is left, each gets Liebermann's first gloss: aveir (vb), aveir (sbst)."""
    base = [index.label(i) for i in final]
    out = list(base)
    for n, l in enumerate(base):
        if base.count(l) < 2:
            continue
        same = [final[k] for k, x in enumerate(base) if x == l]
        if final[n] in index.xref and index.xref[final[n]]:
            out[n] = l + ' for ' + re.sub(r'^\[(.*)\]$', r'\1', index.hw.get(index.xref[final[n]], index.xref[final[n]]))
        elif len([i for i in same if i not in index.xref]) > 1:
            g = index.gloss.get(final[n])
            out[n] = l + (' (' + g + ')' if g else '')
    return [esc(l) for l in out]


def block_labels_ok(text, final, index):
    shown = re.findall(r'<xr type="%s"><ref target="entry:[^"]*">(.*?)</ref></xr>' % XRTYPE, text)
    return shown == labels(final, index)


def update(path, index, write):
    """-> (changed, links added, links removed, found)"""
    text = read(path)
    entry_id = os.path.basename(path)[:-4]
    m = SCRAP.search(text)
    if not m:
        return False, [], [], []
    found = targets(m.group(2), entry_id, index)
    want = []
    for kind, shown, ids, why in found:
        for id_ in ids:
            if id_ not in want:
                want.append(id_)
    existing = SEE.findall(text)
    has_dort = any(k == 'sieheDort' for k, _, _, _ in found)
    # a link checked and found wrong (SKIP) is taken off, though it was there before
    removed = [x for x in existing if (x == 'd' and has_dort and x not in want) or ((entry_id, x) in SKIP and x not in want)
               or (x in UNTER_FORMS[entry_id] and x not in want)]
    kept = [x for x in existing if x not in removed]
    final = want + [x for x in kept if x not in want]
    if final == existing and block_labels_ok(text, final, index):
        return False, [], [], found
    block = ''.join('        <xr type="%s"><ref target="entry:%s">%s</ref></xr>\n' % (XRTYPE, i, l) for i, l in zip(final, labels(final, index)))
    new = SEE.sub('', text)
    if COMPARE or DERIV:
        # after the See links (and, for Der., the Compare links), before the rest
        sees = list((SEE_BEFORE if DERIV else SEE_ANY).finditer(new))
        first_xr = re.search(r'^[ \t]*<xr (?!type="(?:see|compare)")' if DERIV else r'^[ \t]*<xr (?!type="see")', new[sees[-1].end():] if sees else new, re.M)
        if first_xr and sees:
            at = sees[-1].end() + first_xr.start()
            new = new[:at] + block + new[at:]
            first_xr = None
        elif sees:
            at = sees[-1].end(); new = new[:at] + block + new[at:]; first_xr = None
        elif first_xr:
            new = new[:first_xr.start()] + block + new[first_xr.start():]; first_xr = None
        else:
            end = re.search(r'^[ \t]*</entry>', new, re.M)
            if not end:
                return False, [], [], found
            new = new[:end.start()] + block + new[end.start():]
        if write:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(new)
        return True, [x for x in want if x not in existing], removed, found
    first_xr = re.search(r'^[ \t]*<xr ', new, re.M)
    if first_xr:
        new = new[:first_xr.start()] + block + new[first_xr.start():]
    else:
        end = re.search(r'^[ \t]*</entry>', new, re.M)
        if not end:
            return False, [], [], found
        new = new[:end.start()] + block + new[end.start():]
    if write:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(new)
    return True, [x for x in want if x not in existing], removed, found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--only', nargs='*', help='entry ids; the default is every entry')
    ap.add_argument('--entries', default='entries')
    ap.add_argument('--report', default='docs/see-also-report.md')
    ap.add_argument('--no-report', action='store_true')
    ap.add_argument('--show', action='store_true', help='print what was found in each entry')
    ap.add_argument('--compare', action='store_true', help='make the Compare links from "vgl." instead of the See links')
    ap.add_argument('--derivatives', action='store_true', help='make the Derivatives and Compounds links from "Der." instead of the See links')
    args = ap.parse_args()
    if args.compare:
        global SIEHE, OTHER, ABBR, SEE, XRTYPE, COMPARE
        SIEHE, OTHER, XRTYPE, COMPARE = {'vergleiche': 'after'}, (), 'compare', True
        ABBR = re.compile(r'(?P<open><hi rend="italic">)?<ref type="abbreviation" target="gram:(?P<kind>vergleiche)"><abbr>(?P<text>[^<]*)</abbr></ref>')
        SEE = re.compile(r'^[ \t]*<xr type="compare"><ref target="entry:([^"]*)">.*?</ref></xr>[ \t]*\n', re.M)
        if args.report == 'docs/see-also-report.md':
            args.report = 'docs/compare-report.md'
    if args.derivatives:
        global DERIV
        SIEHE, OTHER, XRTYPE, DERIV = {'Derivativ': 'after'}, (), 'derivative', True
        ABBR = re.compile(r'(?P<open><hi rend="italic">)?<ref type="abbreviation" target="gram:(?P<kind>Derivativ)"><abbr>(?P<text>[^<]*)</abbr></ref>')
        SEE = re.compile(r'^[ \t]*<xr type="derivative"><ref target="entry:([^"]*)">.*?</ref></xr>[ \t]*\n', re.M)
        if args.report == 'docs/see-also-report.md':
            args.report = 'docs/derivatives-report.md'

    index = Index(args.entries)
    paths = [os.path.join(args.entries, i + '.xml') for i in args.only] if args.only else sorted(glob.glob(os.path.join(args.entries, '*.xml')))
    tally = collections.Counter()
    problems = collections.defaultdict(list)
    changed = added = removed = 0
    for path in paths:
        ch, add, rem, found = update(path, index, not args.dry_run)
        entry_id = os.path.basename(path)[:-4]
        if args.show:
            for kind, shown, ids, why in found:
                print('  %-12s %-20s -> %s %s' % (entry_id, shown, ','.join(ids) or '-', why))
        changed += ch
        added += len(add)
        removed += len(rem)
        for kind, shown, ids, why in found:
            tally[(kind, 'linked' if ids else 'not linked')] += 1
            if kind in SIEHE and why:
                key = ('linked, ' if ids else 'not linked, ') + re.sub(r'^~ read as.*', '~ filled in from the headword', why.split(':')[0].split(';')[0])
                problems[key].append((entry_id, shown, why))

    lines = ['Entries: %d; changed: %d; links added: %d; wrong links removed: %d' % (len(paths), changed, added, removed)]
    for kind in list(SIEHE) + list(OTHER):
        l, n = tally[(kind, 'linked')], tally[(kind, 'not linked')]
        if l or n:
            lines.append('  %-15s found %5d, linked %5d' % (kind, l + n, l))
    for key, items in sorted(problems.items(), key=lambda kv: -len(kv[1])):
        lines.append('  %-57s %5d' % (key, len(items)))
    print('\n'.join(lines))
    print('(dry run: no files changed)' if args.dry_run else '(entries updated)')

    if not args.no_report and not args.only:
        with open(args.report, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s links made from Liebermann\'s cross-references\n\n' % ('Compare' if COMPARE else 'Derivatives and Compounds' if DERIV else 'See also'))
            f.write('Made by `tools/see-also.py`. It is replaced each time the tool runs.\n\n```\n%s\n```\n\n' % '\n'.join(lines))
            for key, items in sorted(problems.items(), key=lambda kv: -len(kv[1])):
                if 'this entry' in key:
                    continue
                f.write('## %s (%d)\n\n' % (key.capitalize(), len(items)))
                shown = items
                for entry_id, word, why in shown:
                    extra = why.split(': ', 1)[1] if ': ' in why else ''
                    f.write('- **%s**: %s %s%s\n' % (entry_id, 'vgl.' if COMPARE else 'Der.' if DERIV else 's.', word, ' (' + extra + ')' if extra else ''))
                if len(shown) < len(items):
                    f.write('- … and %d more\n' % (len(items) - len(shown)))
                f.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
