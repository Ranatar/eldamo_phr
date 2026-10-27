"""Lexicon of a branch: the words that word formation starts from.

One entry per Eldamo word page (homonyms stay apart: Ambar "world" and
ambar "fate", stem ambart-, are different entries). Each entry carries:

* stems       -- @stem and every <ref> marked <inflect form="stem">;
* elements    -- the <element> parts of a compound, resolved to word pages
                 where the language and form identify one;
* parents     -- the <deriv l v> links of the word (root or earlier word);
* roots       -- primitive roots reached through parents;
* primitive   -- written primitive forms (<deriv v> inside refs, often with
                 morpheme hyphens: Aika-nār-) and the phonetic start forms of
                 attested derivations (<rule-start stage>);
* stages      -- for every branch language: the forms an attested derivation
                 of the word reaches at the end of that language's rules;
* links       -- combine / deprecated / cognate / see links to other pages.

Words deleted by Tolkien (mark "-") are left out; references marked "-"
contribute nothing. Neologisms (Neo-Quenya, Neo-Sindarin, Neo-Primitive and
mark "!") are kept with neo=True: the generator may use them as analogues
only on request.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

from .languages import BRANCHES, languages
from .model import deleted_mark, index
from .orthography import primitive_phonetic
from .source import root, word_url

SKIP_SPEECH = {'phonetic-rule', 'phoneme', 'grammar', 'phonetic-group', 'phonetics', 'text', 'phrase'}
NEO = {'nq', 'ns', 'np'}
EXTRA = {'quenya': ('nq', 'np', 'van'), 'sindarin': ('ns', 'np', 'norths')}
SUPERSCRIPT = re.compile(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+$')
# Eldamo's links between word pages: an earlier conception merged into a later
# word (combine) or replaced by it (deprecated), a cognate in another language,
# a word to compare (see)
LINK_TAGS = ('combine', 'deprecated', 'cognate', 'see')


def bare(form: str | None) -> str:
    """Form without homonym number: lië¹ -> lië."""
    return SUPERSCRIPT.sub('', (form or '').strip())


class Words:
    """Every non-rule word page of the XML, by (language, form)."""

    def __init__(self):
        self.by_key = defaultdict(list)
        self.by_v = defaultdict(list)
        self.by_id = {}
        for w in root().iter('word'):
            if w.get('speech') in SKIP_SPEECH or not w.get('page-id'):
                continue
            self.by_id[w.get('page-id')] = w
            self.by_v[w.get('v')].append(w.get('page-id'))
            self.by_key[(w.get('l'), w.get('v'))].append(w.get('page-id'))
            b = bare(w.get('v'))
            if b != w.get('v'):
                self.by_key[(w.get('l'), b)].append(w.get('page-id'))

    def find(self, lang: str | None, form: str | None) -> list:
        ids = self.by_key.get((lang, form)) or self.by_key.get((lang, bare(form))) or []
        return list(dict.fromkeys(ids))

    def get_word(self, el, context_lang: str | None) -> list:
        """Eldamo's c:get-word (common.xq): the word an <element>, <deriv>, <cognate>... names
        by its form; with @l in that language, else the only word of that form, else
        a word of the language the reference inherits."""
        ids = self.by_v.get(el.get('v')) or []
        if el.get('l'):
            ids = [i for i in ids if self.by_id[i].get('l') == el.get('l')]
        elif len(ids) != 1:
            ids = [i for i in ids if self.by_id[i].get('l') == context_lang]
        return list(dict.fromkeys(ids))

    def ref(self, source: str | None):
        """Eldamo's c:get-ref: (word id, <ref>) for the one reference at this place of a
        source (VT42/10.1912); None when there is none or several."""
        if getattr(self, '_sources', None) is None:
            self._sources = defaultdict(list)
            for pid, w in self.by_id.items():
                for r in w.findall('ref'):
                    if r.get('source'):
                        self._sources[r.get('source')].append((pid, r))
        hits = self._sources.get(source, []) if source else []
        return hits[0] if len(hits) == 1 else None

    def cognates(self, pid: str) -> list:
        """Eldamo's Cognates section (CustomFunctions.allReferenceCognates, allWordCognates):
        everything joined by <cognate> links, transitively, through the references of
        the word (<cognate source>) and through the word itself (<cognate l v>)."""
        if getattr(self, '_cognates', None) is None:
            self._cognates = self._cognate_sets()
        return self._cognates.get(pid, [])

    def _cognate_sets(self) -> dict:
        up = {}

        def find(x):
            while up.setdefault(x, x) != x:
                up[x] = up[up[x]]
                x = up[x]
            return x

        def union(a, b):
            up[find(a)] = find(b)

        self.ref(None)                                   # builds the source index
        for pid, w in self.by_id.items():
            for r in w.findall('ref'):
                if self.ref(r.get('source')) is None:
                    continue                             # only "valid" references (unique source)
                for c in r.findall('cognate'):
                    if self.ref(c.get('source')) is not None:
                        union(('ref', r.get('source')), ('ref', c.get('source')))
            for c in w.findall('cognate'):
                for i in self.by_key.get((c.get('l'), c.get('v')), []):
                    union(('word', pid), ('word', i))
        groups = defaultdict(set)
        for node in list(up):
            groups[find(node)].add(node)
        out = defaultdict(list)
        for members in groups.values():
            words = {(n[1] if n[0] == 'word' else self.ref(n[1])[0]) for n in members}
            for a in words:
                lang = self.by_id[a].get('l')
                out[a] = sorted(b for b in words if b != a and self.by_id[b].get('l') != lang)
        return out

    def find_loose(self, lang: str | None, form: str | None) -> list:
        """By a loose key (_loose): for forms written in a source's spelling."""
        if getattr(self, '_loose', None) is None:
            self._loose = defaultdict(list)
            for pid, w in self.by_id.items():
                if not deleted_mark(w.get('mark')):
                    self._loose[(w.get('l'), _loose(w.get('v')))].append(pid)
        return list(dict.fromkeys(self._loose.get((lang, _loose(form)), [])))


_LOOSE = str.maketrans('āēīōūáéíóúâêîôûäëïöüǭ', 'aeiouaeiouaeiouaeiouo')


def _loose(form: str | None) -> str:
    """Loose key for element forms written inside a <ref> in the source's
    spelling: tultā- ~ tulta-, kalta- ~ calta-, ima ~ -ima."""
    return bare(form).lower().strip('- ').translate(_LOOSE).replace('k', 'c')


_WORDS = None


def words() -> Words:
    global _WORDS
    if _WORDS is None:
        _WORDS = Words()
    return _WORDS


def _live(el) -> bool:
    return not deleted_mark(el.get('mark'))


def _stems(w) -> list:
    out = []
    if w.get('stem'):
        out.append(w.get('stem'))
    for ref in w.findall('ref'):
        if not _live(ref):
            continue
        for inf in ref.findall('inflect'):
            if 'stem' in (inf.get('form') or '').split():
                out.append(ref.get('v'))
    return list(dict.fromkeys(s for s in out if s))


def _link(W: Words, lang, form, tag=None) -> dict:
    ids = W.find(lang, form)
    rec = {'lang': lang, 'form': form}
    if tag:
        rec['tag'] = tag
    if len(ids) == 1:
        rec['id'] = ids[0]
    elif ids:
        rec['candidates'] = ids
    return rec


def _ref_element(W: Words, e, lang: str) -> dict:
    """An <element> written inside a <ref>: its @source is the place of the element's
    own reference (c:get-ref), which belongs to the element word; else by form."""
    hit = W.ref(e.get('source'))
    if hit is not None:
        x = W.by_id[hit[0]]
        rec = {'lang': x.get('l'), 'form': x.get('v'), 'id': hit[0]}
    else:
        rec = _link(W, e.get('l') or lang, e.get('v'))
        if not (rec.get('id') or rec.get('candidates')):
            ids = W.find_loose(e.get('l') or lang, e.get('v'))
            if len(ids) == 1:
                rec['id'] = ids[0]
            elif ids:
                rec['candidates'] = ids
    if e.get('form'):
        rec['tag'] = e.get('form')
    rec['from_ref'] = True
    return rec


def _gloss(w) -> str:
    """Eldamo's c:get-gloss for a page without @gloss: its one nested word's gloss,
    else the gloss its references agree on (inflected forms and corrections aside)."""
    if w.get('gloss') or w.get('ngloss'):
        return w.get('gloss') or w.get('ngloss')
    refs = w.findall('ref')
    if not refs:
        nested = [x.get('gloss') for x in w.findall('word') if x.get('gloss')]
        if len(nested) == 1:
            return nested[0]
    glosses = [r.get('gloss') for r in refs if r.get('gloss') and not r.findall('inflect') and not r.findall('correction')
               and (not deleted_mark(r.get('mark')) or deleted_mark(w.get('mark')))]
    if glosses and len({g.lower() for g in glosses}) == 1:
        return glosses[0]
    return ''


def _inflected(W: Words, source: str | None) -> bool:
    """The reference at this source is an inflected form of the word (<inflect>)."""
    hit = W.ref(source)
    return hit is not None and bool(hit[1].findall('inflect'))


def _ref_elements(w) -> list:
    """Elements Eldamo records only inside a <ref> (the word page has none of
    its own): from the ref with the word's own form, else the first ref with elements."""
    refs = [r for r in w.findall('ref') if _live(r) and r.findall('element')]
    if not refs:
        return []
    own = [r for r in refs if _loose(r.get('v')) == _loose(w.get('v'))]
    return [e for e in (own or refs)[0].findall('element') if _live(e)]


def build_lexicon(branch: str, derivations: list) -> list:
    ix, W = index(), words()
    langs = languages(branch)
    keep = set(langs) | set(EXTRA.get(branch, ()))
    by_word = defaultdict(list)
    for d in derivations:
        if d['word'] and not d['deleted']:
            by_word[d['word']].append(d)
    entries = []
    for pid, w in W.by_id.items():
        lang = w.get('l')
        if lang not in keep or not _live(w):
            continue
        parent = ix.parent.get(w)
        entry = {
            'id': pid,
            'lang': lang,
            'form': w.get('v'),
            'gloss': _gloss(w),
            'speech': w.get('speech') or '',
            'mark': w.get('mark') or '',
            'url': word_url(pid),
        }
        if lang in NEO or '!' in entry['mark']:
            entry['neo'] = True
        if parent is not None and parent.tag == 'word' and parent.get('page-id'):
            entry['under'] = parent.get('page-id')   # nested page: an earlier or later version
        stems = _stems(w)
        if stems:
            entry['stems'] = stems
        elements = [_link(W, e.get('l'), e.get('v'), e.get('form')) for e in w.findall('element') if _live(e)]
        if not elements:
            # some pages record their elements only inside a reference, in the source's spelling
            elements = [_ref_element(W, e, lang) for e in _ref_elements(w) if e.get('v') != '?']
        if elements:
            entry['elements'] = elements
        links = {}
        for tag in LINK_TAGS:
            if tag == 'cognate':
                continue
            found = [x for x in (_link(W, el.get('l'), el.get('v')) for el in w.findall(tag)) if x.get('id')]
            if found:
                links[tag] = [{'lang': x['lang'], 'form': x['form'], 'id': x['id']} for x in found]
        # cognates as Eldamo's page shows them: through the word and its references, transitively
        cognates = [i for i in W.cognates(pid) if _live(W.by_id[i])]
        if cognates:
            links['cognate'] = [{'lang': W.by_id[i].get('l'), 'form': W.by_id[i].get('v'), 'id': i} for i in cognates]
        if links:
            entry['links'] = links
        parents = [_link(W, d.get('l'), d.get('v')) for d in w.findall('deriv') if _live(d)]
        if parents:
            entry['parents'] = parents
        primitive, own = [], []
        for ref in w.findall('ref'):
            if not _live(ref):
                continue
            for d in ref.findall('deriv'):
                if _live(d) and d.get('v'):
                    primitive.append(d.get('v'))
                    if not ref.findall('inflect'):
                        own.append(d.get('v'))
        if own:
            # origins written for an inflected form of the word (fara-: farále 'you hunt') are not its own
            entry['written_origins'] = list(dict.fromkeys(own))
        if primitive:
            # an origin written as a root (MBAR) names the word's root
            proto = ('mp', 'p') if langs.get(lang, {}).get('era') == 'middle' else ('p', 'mp')
            for v in dict.fromkeys(primitive):
                for code in proto:
                    hits = [i for i in W.find(code, v) if W.by_id[i].get('speech') == 'root']
                    if hits:
                        entry.setdefault('origin_roots', []).append({'lang': code, 'form': v, 'id': hits[0]})
                        break
        ders = by_word.get(pid, [])
        if ders:
            entry['derivations'] = [d['id'] for d in ders]
            # derivations of an inflected form of the word (Eldamo: a <ref> with <inflect>;
            # fara- 'to hunt': farále 'you hunt' < ✶pʰáralē, Adan: Edain) tell nothing
            # about the word's own primitive form or stage forms
            other = [d for d in ders if _inflected(W, d.get('source'))]
            if other:
                entry['other_forms'] = [{'form': d['form'], 'start': d['start'], 'derivation': d['id']} for d in other]
            ders = [d for d in ders if d not in other]
        if ders:
            entry['starts'] = list(dict.fromkeys(d['start'] for d in ders if d['start']))
            # steps Eldamo gives without a rule ('?'): buzbō > buspō > puspō (b > p?) > pupso
            unruled = []
            for d in ders:
                prev = d['start']
                for st in d['steps']:
                    if st['status'].startswith('unknown_rule') and [st['lang'], prev, st['after']] not in unruled:
                        unruled.append([st['lang'], prev, st['after']])
                    prev = st['after']
            if unruled:
                entry['unruled'] = unruled
            stages = defaultdict(list)
            for d in ders:
                last = {}
                for s in d['steps']:
                    if s['lang'] in langs and s['after']:
                        last[s['lang']] = s['after']
                for code, form in last.items():
                    if form not in stages[code]:
                        stages[code].append(form)
            if stages:
                entry['stages'] = dict(stages)
        entries.append(entry)
    _resolve_roots(entries, W)
    _proto_forms(entries, W)
    entries.sort(key=lambda e: (e['lang'], bare(e['form']).lower(), e['id']))
    return entries


def _resolve_roots(entries: list, W: Words) -> None:
    """roots: primitive roots reached by following parent links (at most 4 steps)."""
    for e in entries:
        roots, frontier, seen = [], list(e.get('parents', ())), set()
        for _ in range(4):
            nxt = []
            for p in frontier:
                pid = p.get('id')
                if not pid or pid in seen:
                    continue
                seen.add(pid)
                w = W.by_id.get(pid)
                if w is None:
                    continue
                if w.get('speech') == 'root':
                    roots.append({'lang': w.get('l'), 'form': w.get('v'), 'id': pid})
                else:
                    nxt += [_link(W, d.get('l'), d.get('v')) for d in w.findall('deriv') if _live(d)]
            frontier = nxt
        for r in e.pop('origin_roots', ()):
            if all(r['id'] != x['id'] for x in roots):
                roots.append(r)
        if roots:
            e['roots'] = roots


PROTO = ('p', 'mp')


def _proto_forms(entries: list, W: Words) -> None:
    """proto_forms: primitive word forms (not roots) the word is linked to -- its
    own form for a Primitive Elvish word, or a parent page in Primitive Elvish
    (Q. -mo < ✶-mō). Used when the word has no derivation."""
    for e in entries:
        out = []
        if e['lang'] in PROTO and e['speech'] != 'root':
            out.append(e['form'])
        for p in e.get('parents', ()):
            w = W.by_id.get(p.get('id')) if p.get('id') else None
            if w is not None and w.get('l') in PROTO and w.get('speech') != 'root' and w.get('v'):
                out.append(w.get('v'))
        if out:
            e['proto_forms'] = list(dict.fromkeys(primitive_phonetic(f) for f in out))
        if e.get('written_origins'):
            e['written_origins'] = list(dict.fromkeys(primitive_phonetic(f) for f in e['written_origins']))


def summary(entries: list) -> dict:
    c = Counter()
    for e in entries:
        c['entries'] += 1
        for k in ('stems', 'elements', 'parents', 'roots', 'derivations', 'stages'):
            if e.get(k):
                c[k] += 1
        if e.get('neo'):
            c['neo'] += 1
        if e.get('elements') and e.get('derivations'):
            c['compounds_with_derivations'] += 1
    by_form = Counter((e['lang'], bare(e['form'])) for e in entries)
    c['homonym_forms'] = sum(1 for v in by_form.values() if v > 1)
    return dict(c)


if __name__ == '__main__':
    import sys
    from .pipeline import build_branch
    for b in sys.argv[1:] or BRANCHES:
        lex = build_lexicon(b, build_branch(b)['derivations'])
        print(b, summary(lex))
