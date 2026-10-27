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
import unicodedata
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
        self.by_id = {}
        for w in root().iter('word'):
            if w.get('speech') in SKIP_SPEECH or not w.get('page-id'):
                continue
            self.by_id[w.get('page-id')] = w
            self.by_key[(w.get('l'), w.get('v'))].append(w.get('page-id'))
            b = bare(w.get('v'))
            if b != w.get('v'):
                self.by_key[(w.get('l'), b)].append(w.get('page-id'))

    def find(self, lang: str | None, form: str | None) -> list:
        ids = self.by_key.get((lang, form)) or self.by_key.get((lang, bare(form))) or []
        return list(dict.fromkeys(ids))

    def by_source(self, source: str | None) -> list:
        """Word pages with a reference to this exact place of a source (VT42/10.1912)."""
        if getattr(self, '_sources', None) is None:
            self._sources = defaultdict(list)
            for pid, w in self.by_id.items():
                for ref in w.findall('ref'):
                    if ref.get('source') and _live(ref):
                        self._sources[ref.get('source')].append((pid, ref.get('v')))
        return self._sources.get(source, []) if source else []

    def find_loose_any(self, form: str | None) -> list:
        """Word pages of any language with this form (loose key)."""
        self.find_loose(None, form)
        key = _loose(form)
        return list(dict.fromkeys(i for (lang, k), ids in self._loose.items() if k == key for i in ids))

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


def _variants(form: str | None) -> set:
    """Comparable spellings of a written form: diacritics, homonym numbers,
    hyphens and brackets dropped, c/k, qu/kw, y/i unified; 'an(a)' gives an and
    ana, 'mazgō/ŭ' gives each alternative."""
    out = set()
    for alt in bare(form).split('/'):
        alt = unicodedata.normalize('NFD', alt.lower())
        alt = ''.join(ch for ch in alt if not unicodedata.combining(ch))
        alt = re.sub(r'[-\[\]*†#?!\s]', '', alt)
        alt = alt.replace('qu', 'kw').replace('q', 'kw').replace('c', 'k').replace('y', 'i')
        out.add(re.sub(r'[()]', '', alt))
        out.add(re.sub(r'\([^)]*\)', '', alt))
    return {x for x in out if x}


def same_form(word_form: str | None, form: str | None) -> bool:
    """A derivation or reference is about the word itself, not about another
    form of it (fara- 'hunt' and its gerund farálë; Adan and the plural Edain)."""
    return bool(_variants(word_form) & _variants(form))


def _ref_link(W: Words, lang, form, tag=None) -> dict:
    """_link for an element written inside a <ref>: exact form first, then the loose key."""
    rec = _link(W, lang, form, tag)
    if not (rec.get('id') or rec.get('candidates')):
        ids = W.find_loose(lang, form)
        if len(ids) == 1:
            rec['id'] = ids[0]
        elif ids:
            rec['candidates'] = ids
    rec['from_ref'] = True
    return rec


def _ref_cognates(W: Words, pid: str, w) -> list:
    """Cognates Eldamo records inside a <ref> of the word (most of them: 5021 against
    1479 on the page itself). They carry no language but the source place of the
    cognate, and the cognate word has a reference to the same place: Q. erinqua
    <cognate v="ereb" source="VT42/10.1912"/>, S. ereb <ref v="ereb" source="VT42/10.1912">."""
    out, seen = [], set()
    for ref in w.findall('ref'):
        if not _live(ref):
            continue
        for c in ref.findall('cognate'):
            if not _live(c):
                continue
            hits = [i for i, v in W.by_source(c.get('source')) if i != pid and same_form(c.get('v'), v)]
            if not hits:
                # no reference at that place: a word of that form, if there is only one
                hits = [i for i in W.find_loose_any(c.get('v')) if i != pid]
                if len(hits) != 1:
                    continue
            for i in dict.fromkeys(hits):
                if i not in seen and _live(W.by_id[i]):
                    seen.add(i)
                    x = W.by_id[i]
                    out.append({'lang': x.get('l'), 'form': x.get('v'), 'id': i, 'from_ref': True})
    return out


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
            'gloss': w.get('gloss') or w.get('ngloss') or '',
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
            elements = [_ref_link(W, e.get('l') or lang, e.get('v'), e.get('form')) for e in _ref_elements(w)]
        if elements:
            entry['elements'] = elements
        links = {}
        for tag in LINK_TAGS:
            found = [x for x in (_link(W, el.get('l'), el.get('v')) for el in w.findall(tag)) if x.get('id')]
            if found:
                links[tag] = [{'lang': x['lang'], 'form': x['form'], 'id': x['id']} for x in found]
        ref_cognates = _ref_cognates(W, pid, w)
        if ref_cognates:
            have = {x['id'] for x in links.get('cognate', ())}
            links.setdefault('cognate', []).extend(x for x in ref_cognates if x['id'] not in have)
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
                    if same_form(w.get('v'), ref.get('v')) or not ref.get('v'):
                        own.append(d.get('v'))
        if own:
            # origins written for another form of the word (a gerund, a plural) are not its own
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
            # derivations of another form of the word (fara- 'hunt': farálë < ✶pʰáralē)
            # tell nothing about the word's own primitive form or stage forms
            other = [d for d in ders if d.get('form') and not same_form(w.get('v'), d['form'])]
            if other:
                entry['other_forms'] = [{'form': d['form'], 'start': d['start'], 'derivation': d['id']} for d in other]
            ders = [d for d in ders if d not in other]
        if ders:
            entry['starts'] = list(dict.fromkeys(d['start'] for d in ders if d['start']))
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
