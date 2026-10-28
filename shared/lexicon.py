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
from .root_checks import consonants_match, same_first_consonant, same_onset
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

    def merged_into(self, pid: str) -> list:
        """Pages whose <combine> names this one: the same word of another conception, merged
        into it (ᴹQ. sar into Q. sar), in document order."""
        return self._back('combine').get(pid, [])

    def replaced_by(self, pid: str) -> list:
        """Pages whose <deprecated> names this one: words it replaced."""
        return self._back('deprecated').get(pid, [])

    def _back(self, tag: str) -> dict:
        cache = self.__dict__.setdefault('_backlinks', {})
        if tag not in cache:
            out = defaultdict(list)
            for pid, w in self.by_id.items():
                els = w.findall(tag)[:1] if tag == 'combine' else w.findall(tag)
                for el in els:
                    for t in self.get_word(el, w.get('l'))[:1]:
                        if t != pid and pid not in out[t]:
                            out[t].append(pid)
            cache[tag] = out
        return cache[tag]

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


def _is_root(w) -> bool:
    """A root page: speech="root", or a primitive form written in capitals (Eldamo 0.8.13
    files N√GAWAK, ᴱ✶ƷAWAKA and ᴱ√OWO as nouns)."""
    if w.get('speech') == 'root':
        return True
    letters = re.sub(r'[^\w]|[\d_¹²³⁴⁵⁶⁷⁸⁹⁰]', '', w.get('v') or '')
    return w.get('l') in ('p', 'mp', 'ep', 'np') and bool(letters) and letters.isupper()


def _live_in(el, w) -> bool:
    """A part of a word page counts unless Tolkien rejected it, or the word itself is rejected
    as well (N. carth, merged into S. carth: its rejected references still give ᴹ√KAR)."""
    return _live(el) or not _live(w)


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
    refs = [r for r in w.findall('ref') if _live_in(r, w) and r.findall('element')]
    if not refs:
        return []
    own = [r for r in refs if _loose(r.get('v')) == _loose(w.get('v'))]
    return [e for e in (own or refs)[0].findall('element') if _live_in(e, w)]


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
        cls = [c.get('form') for c in w.findall('class') if c.get('form', '').endswith(('verb', 'formative', 'causative', 'stem'))]
        if cls:
            entry['verb_class'] = cls[0]
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
        own = []
        for ref in w.findall('ref'):
            if not _live(ref):
                continue
            for d in ref.findall('deriv'):
                if _live(d) and d.get('v') and not ref.findall('inflect'):
                    own.append(d.get('v'))
        if own:
            # origins written for an inflected form of the word (fara-: farále 'you hunt') are not its own
            entry['written_origins'] = list(dict.fromkeys(own))
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


def _derived_from(W: Words, w, elements: bool = True) -> list:
    """Ids of the words a word derives from, as Eldamo's Derivations section finds them
    (word-page.xq, print-derivations): its own <deriv> (c:get-word) and every <deriv> inside
    its references that points to a reference of another word by @source (c:get-ref),
    as Q. lár < ᴹ√DAR; and, with `elements`, roots named as elements."""
    out = []
    for d in w.findall('deriv'):
        if _live_in(d, w):
            out += W.get_word(d, w.get('l'))
    for ref in w.findall('ref'):
        if not _live_in(ref, w) or W.ref(ref.get('source')) is None:
            continue
        for d in ref.findall('deriv'):
            if not _live_in(d, w):
                continue
            hit = W.ref(d.get('source'))
            if hit:
                out.append(hit[0])
            elif d.get('v'):
                # a written primitive form that names no reference: the root of that form, if
                # there is one (N. carth < ᴹ√KAR); with a reference it is followed above, and
                # the form alone would add a homonymous root of another conception
                for code in ('p', 'mp', 'ep', 'np'):
                    roots = [i for i in W.find(code, d.get('v')) if _is_root(W.by_id[i])]
                    if roots:
                        out.append(roots[0])
                        break
        # roots named as elements inside the references (Q. parma: PAR¹ beside its √PAR²)
        for el in ref.findall('element'):
            hit = W.ref(el.get('source')) if _live_in(el, w) else None
            if hit and _is_root(W.by_id[hit[0]]):
                out.append(hit[0])
    # a root among the elements is the word's root (Q. firya: √PHIR + -ya); the roots of
    # word elements belong to the parts of a compound and are not followed
    for el in w.findall('element') if elements else ():
        if _live_in(el, w):
            out += [i for i in W.get_word(el, w.get('l')) if _is_root(W.by_id[i])]
    return list(dict.fromkeys(out))


def _element_ids(W: Words, w) -> list:
    """Word pages of a word's elements in order, roots among them included: its own
    <element> (c:get-word), else those inside its references (by @source, else by form)."""
    out = []
    for el in w.findall('element'):
        if _live_in(el, w) and el.get('v') != '?':
            out += W.get_word(el, w.get('l'))[:1]
    if not out:
        for el in _ref_elements(w):
            if el.get('v') == '?':
                continue
            hit = W.ref(el.get('source'))
            out += [hit[0]] if hit else W.get_word(el, w.get('l'))[:1]
    return list(dict.fromkeys(out))


def _root_rec(W: Words, rid: str) -> dict:
    q = W.by_id[rid]
    return {'lang': q.get('l'), 'form': q.get('v'), 'id': rid}


def _real(group: list) -> list:
    return [r for r in group if not r.get('gap')]


def _gap(W: Words, eid: str) -> dict:
    """An element without a root, shown in its place among the roots: its primitive form
    when it derives from one (S. -iel < ✶-iel), else itself."""
    w = W.by_id[eid]
    for d in _derived_from(W, w):
        q = W.by_id[d]
        if not _is_root(q) and q.get('l') in ('p', 'mp', 'ep'):
            return {'gap': True, 'lang': q.get('l'), 'form': q.get('v'), 'id': d, 'element': eid}
    return {'gap': True, 'lang': w.get('l'), 'form': w.get('v'), 'id': eid, 'element': eid}


PRIMITIVE_LANGS = ('p', 'mp', 'ep')
ROOT_DEPTH = 7          # steps through elements and derivations (S. Arthedain > Adan > Q. Atan > atta > √ATATA)


def _branch_of(lang: str | None) -> str | None:
    for b, d in BRANCHES.items():
        if any(l[0] == lang for l in d['languages'] if l[0] not in PRIMITIVE_LANGS):
            return b
    return {'nq': 'quenya', 'ns': 'sindarin', 'norths': 'sindarin', 'van': 'quenya'}.get(lang, lang)


def _part_groups(W: Words, pid: str, memo: dict, depth: int = ROOT_DEPTH) -> list:
    """[[root]] per element of a word, in order: a root named as an element (named), else the
    element's own groups (_root_groups; a compound element adds its parts). An element with
    no root gives a group with only a gap (_gap)."""
    if depth <= 0 or pid not in W.by_id:
        return []
    groups = []
    for eid in _element_ids(W, W.by_id[pid]):
        if _is_root(W.by_id[eid]):
            groups.append([dict(_root_rec(W, eid), named=True)])
            continue
        sub = _root_groups(W, eid, memo, depth - 1)
        sub = [[r if r.get('gap') else dict(r, via=r.get('via') or 'element', named=False) for r in g] for g in sub]
        groups.extend(sub if any(_real(g) for g in sub) else [[_gap(W, eid)]])
    return groups


def _merge_groups(found: list) -> list:
    """Several sources of the same rank: the one with most parts; one of the same shape adds
    its roots as alternatives part by part."""
    found = sorted(found, key=lambda g: -len(g))
    out = [list(x) for x in found[0]]
    for g in found[1:]:
        if len(g) == len(out):
            for k, x in enumerate(g):
                out[k] += [r for r in x if r.get('gap') or all(r.get('id') != y.get('id') for y in out[k])]
    return out


def _via(groups: list, via: str) -> list:
    return [[dict(r, via=via, named=False) if not r.get('gap') else r for r in g] for g in groups]


def _root_groups(W: Words, pid: str, memo: dict, depth: int = ROOT_DEPTH) -> list:
    """The roots of a word as parts: [[root]], each part a list of alternatives, gaps
    included (_gap). Records carry via: '' (named by the word's own derivation or as its
    element), 'element' (a root of an element), 'source' (a root of a word of another
    language it derives from: S. Adan < Q. Atan), 'combine' (of the same word of another
    conception merged into it), 'see', 'deprecated' (of a word it replaced).

    1. Two or more elements with roots: the roots by element (Q. palantír = √PAL + √TIR;
       S. randir = √RAN + √N(D)ER, though its derivation names RAN alone). A root the
       derivations name fills an element without one when it begins with the same consonant
       (S. huorn = hû¹ + orn, a reference names KHUG for hû).
    2. Roots its derivations name (Q. lár < ᴹ√DAR); several are alternatives (S. galadh <
       ✶galadā < √GALAD/√GAL²), and so are the roots of the one intermediate form another
       derivation goes through (S. fân < √PHAN, and < ✶phanā < √PHAY).
    3. One element with roots: that element and the rest as gaps (Q. firya = √PHIR + -ya).
    4. The roots of the words it derives from that are not roots, followed the same way: a
       primitive word keeps its roots as the word's own (S. arthor < ✶artaurē = √RĀ/ARA +
       √TUR), a word of another language gives them via 'source'.
    5. The roots of the same word of other conceptions merged into it (combine: NQ. helissar
       = helin + sar, sar < ᴹQ. sar < ᴹ√SAR); 6. of the page its <see> names; 7. of a word it
       replaced (deprecated), when the two begin alike and the roots' consonants are in this
       word (shared/root_checks.py). The order is that of neo-roots (neo_roots.py)."""
    key = (pid, depth)
    if key in memo:
        return memo[key]
    memo[key] = []                       # a cycle gives nothing
    out = []
    if pid in W.by_id and depth > 0:
        w = W.by_id[pid]
        parts = _part_groups(W, pid, memo, depth)
        real = [g for g in parts if _real(g)]
        derived = _derived_from(W, w, elements=False)
        direct = [_root_rec(W, d) for d in derived if _is_root(W.by_id[d])]
        found = []
        for d in derived:
            q = W.by_id[d]
            if _is_root(q):
                continue
            g = _root_groups(W, d, memo, depth - 1)
            if not any(_real(x) for x in g):
                continue
            if q.get('l') not in PRIMITIVE_LANGS and _branch_of(q.get('l')) != _branch_of(w.get('l')):
                g = [[dict(r, via='source') if not r.get('gap') else r for r in x] for x in g]
            found.append(g)
        inter = _merge_groups(found) if found else []
        if len(real) == 1 and direct and len(parts) > 1:
            used = {r['id'] for g in real for r in _real(g)}
            filled = []
            for g in parts:
                if _real(g) or g[0].get('element') not in W.by_id:
                    filled.append(g)
                    continue
                e = W.by_id[g[0]['element']]
                form = e.get('v') or ''
                if form.startswith('-') or form.endswith('-') and e.get('speech') in ('pref', 'suf'):
                    filled.append(g)             # an affix is not a root's stand-in
                    continue
                fit = [dict(r, via='element', named=False) for r in direct
                       if r['id'] not in used and same_first_consonant(form, r['form'])]
                filled.append(fit or g)
            if sum(1 for g in filled if _real(g)) >= 2:
                parts, real = filled, [g for g in filled if _real(g)]
        if len(real) >= 2:
            out = parts
        elif direct:
            alts = list(direct)
            if len(inter) == 1:
                alts += [r for r in _real(inter[0]) if all(r['id'] != x['id'] for x in alts)]
            out = [alts]
        elif real:
            out = parts
        elif inter:
            out = inter
        else:
            for tag, ids in (('combine', W.merged_into(pid)),
                             ('see', [i for el in w.findall('see') for i in W.get_word(el, w.get('l'))[:1]]),
                             ('deprecated', W.replaced_by(pid))):
                found = []
                for x in ids:
                    if x == pid or x not in W.by_id:
                        continue
                    xw = W.by_id[x]
                    if tag == 'deprecated':
                        if not same_onset(xw.get('v'), w.get('v')):
                            continue
                        if _is_root(xw):
                            if not same_first_consonant(xw.get('v'), w.get('v')):
                                continue
                            g = [[_root_rec(W, x)]]
                        else:
                            g = _root_groups(W, x, memo, depth - 1)
                        # every part's roots must be found in this word
                        if not any(_real(p) for p in g) or any(
                                _real(p) and not [r for r in _real(p) if consonants_match(w.get('v'), r['form'], w.get('l'))]
                                for p in g):
                            continue
                        g = [[r for r in p if r.get('gap') or consonants_match(w.get('v'), r['form'], w.get('l'))] for p in g]
                    elif _is_root(xw):
                        g = [[_root_rec(W, x)]]
                    else:
                        g = _root_groups(W, x, memo, depth - 1)
                    if any(_real(p) for p in g):
                        found.append(_via(g, tag))
                if found:
                    out = _merge_groups(found)
                    break
    memo[key] = out
    return out


def _elvish() -> set:
    """Elvish languages: those under a Primitive Elvish language in Eldamo's language tree
    (Adûnaic, Westron, Khuzdul have "cognates" by borrowing, not by roots)."""
    out = set()

    def walk(el, elvish):
        for x in el.findall('language'):
            mine = elvish or x.get('id') in PRIMITIVE_LANGS + ('np',)
            if mine:
                out.add(x.get('id'))
            walk(x, mine)
    for top in root().iter('language-cat'):
        walk(top, False)
    if not out:
        walk(root(), False)
    return out


def _own_roots(W: Words, pid: str, memo: dict) -> list:
    """All the roots of a word, flat (the cognate check, tests)."""
    return [r for g in _root_groups(W, pid, memo) for r in _real(g)]


def _resolve_roots(entries: list, W: Words) -> None:
    """roots: [{lang, form, id, via?, part?}] from _root_groups; part numbers the parts when
    there are several (elements joined by +, alternatives of one part by /); root_gaps: the
    parts without a root, in their place ({part, lang, form, id}: S. Adanel = √ATATA + ✶-iel).
    When a word has none, the roots of its cognates, if their consonants are found in the
    word (via 'cognate': Q. Perian ← S. Perian = per- + ?, √PER; not S. Gwahaedir, which
    Eldamo links to Q. palantír as the same thing in Sindarin). Roots a <ref><deriv> names
    by form only count as named by the word's derivation (_derived_from)."""
    memo = {}
    for e in entries:
        groups = _root_groups(W, e['id'], memo) if e['id'] in W.by_id else []
        roots, gaps = [], []
        if any(_real(g) for g in groups):
            several = len(groups) > 1
            for k, g in enumerate(groups):
                for r in g:
                    rec = {x: v for x, v in r.items() if x not in ('named', 'gap', 'via', 'part', 'element')}
                    if several:
                        rec['part'] = k
                    if r.get('gap'):
                        gaps.append(rec)
                    else:
                        if r.get('via') and not r.get('named'):
                            rec['via'] = r['via']
                        roots.append(rec)
        else:
            elvish = _elvish()
            for cid in W.cognates(e['id']):
                lang = W.by_id[cid].get('l')
                if cid == e['id'] or lang in PRIMITIVE_LANGS + ('np',) or lang not in elvish:
                    continue
                # roots the cognate itself has only through a loose link say nothing here
                roots += [dict({x: v for x, v in r.items() if x not in ('named', 'gap', 'part', 'element')}, via='cognate')
                          for r in _own_roots(W, cid, memo)
                          if r.get('via') not in ('cognate', 'deprecated') and consonants_match(e['form'], r['form'], e['lang'])]
        out = []
        for r in roots:
            if all(r['id'] != x['id'] or r.get('part') != x.get('part') for x in out):
                out.append(r)
        if out:
            e['roots'] = out
            if gaps:
                e['root_gaps'] = gaps


def primitive_or_form(e: dict) -> str:
    """What a root is compared with in the cognate check of _resolve_roots: the word's
    form in phonetic notation."""
    from .orthography import to_phonetic
    branch = next((b for b, d in BRANCHES.items() if any(l[0] == e['lang'] for l in d['languages'])), 'sindarin')
    return to_phonetic(bare(e.get('form') or ''), branch).strip().strip('-')


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
