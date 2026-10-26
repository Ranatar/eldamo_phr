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
        if elements:
            entry['elements'] = elements
        links = {}
        for tag in LINK_TAGS:
            found = [x for x in (_link(W, el.get('l'), el.get('v')) for el in w.findall(tag)) if x.get('id')]
            if found:
                links[tag] = [{'lang': x['lang'], 'form': x['form'], 'id': x['id']} for x in found]
        if links:
            entry['links'] = links
        parents = [_link(W, d.get('l'), d.get('v')) for d in w.findall('deriv') if _live(d)]
        if parents:
            entry['parents'] = parents
        primitive = []
        for ref in w.findall('ref'):
            if not _live(ref):
                continue
            for d in ref.findall('deriv'):
                if _live(d) and d.get('v'):
                    primitive.append(d.get('v'))
        if primitive:
            entry['written_origins'] = list(dict.fromkeys(primitive))
            # an origin written as a root (MBAR) names the word's root
            proto = ('mp', 'p') if langs.get(lang, {}).get('era') == 'middle' else ('p', 'mp')
            for v in entry['written_origins']:
                for code in proto:
                    hits = [i for i in W.find(code, v) if W.by_id[i].get('speech') == 'root']
                    if hits:
                        entry.setdefault('origin_roots', []).append({'lang': code, 'form': v, 'id': hits[0]})
                        break
        ders = by_word.get(pid, [])
        if ders:
            entry['derivations'] = [d['id'] for d in ders]
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
            e['proto_forms'] = list(dict.fromkeys(out))


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
