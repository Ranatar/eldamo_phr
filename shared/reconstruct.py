"""Reconstruction of a word's form for another period (docs/period-reconstruction-plan.md).

A period is (branch, era, stage): Quenya or Sindarin; Tolkien's late, middle
or early conception; a stage of the language (0 = the primitive form as Eldamo
writes it, before the rules of Primitive Elvish; s >= 1 = the form at the end
of that stage's rules).

Routes, chosen by source and target:

* forward   -- same branch and era, later stage: the sound laws (sequencer);
* backward  -- same branch and era, earlier stage: candidates from learnt
               correspondences, each verified by running the laws forward;
               directly between the two stages and through the primitive form;
* sideways  -- other branch, same era (a cognate): back to the primitive form
               in one branch, forward in the other;
* across    -- other era (Tolkien's conceptions): Eldamo's own links between
               the pages first (combine, deprecated), then the form unchanged if
               the target language allows it, then re-etymologization (Strack's
               method for Neo-Eldarin): back to the primitive form, over to the
               other conception's primitive, forward by its laws. Such forms are
               marked as neologisms.

Every variant carries its route, the rules applied and what supports it:
an attested form of Eldamo, an Eldamo link, a verified reconstruction.
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from . import backform as BF
from .compound import origins
from .interpreter import comparable, is_vowel, join, phonemes
from .orthography import to_phonetic
from .roots import root_phonetic
from .sequencer import Sequencer, _replays

LIMIT = 8
ROOT_BONUS = 2.0
# a candidate whose run, kept open as a stem, gives the word's attested stem (Q. polë, poli-:
# ✶poli, not ✶pole) is marked; weighting it up (×10) gains nothing over the roots on Eldamo's
# primitives of words with stems (reports/reconstruction.md, «Основы слов»), so the weight is 1
STEM_BONUS = 1.0
STEM_TRIAL = 10.0
NO_HINTS = {'roots': (), 'stems': (), 'starts': ()}
PHONOTACTIC_PENALTY = 0.2
SEARCH = {'beam': 150, 'options': 6, 'min_share': 0.02}   # wider than for word formation: no Eldamo primitive to fall back on
WIDE = {'beam': 300, 'options': 10, 'min_share': 0.005}   # when SEARCH finds nothing: rarer correspondences (S. -b < -kwā)
NEAR_STOP = {'the', 'and', 'for', 'with', 'from', 'that', 'one', 'not', 'into', 'being', 'thing', 'person', 'make',
             'made', 'something', 'someone', 'kind', 'sort', 'state', 'act', 'very'}
EQUIV = [set('kgxɣhq'), set('tdθðþ'), set('pbɸβfv'), set('mṃ'), set('nŋñṇ'), set('l'), set('r'), set('sz'), set('w'),
         set('jy')]


# --------------------------------------------------------------------------
# normalized derivations: the form at the end of every stage

def normalize(data: dict, seq: Sequencer) -> list:
    """For each replayable derivation whose replay reaches the attested form:
    {'derivation', 'word', 'era', 'forms': {stage: form}}. Stage 0 is the start
    (Eldamo's primitive form); later stages are the forms after the last rule
    of that stage in the reproducing replay."""
    out = []
    langs = seq.langs
    for d, variants in _replays(data, seq):
        target = comparable(d['steps'][-1]['after'])
        hit = next((v for v in variants if comparable(v['form']) == target), None)
        if hit is None:
            continue
        codes = [s['lang'] for s in d['steps']]
        era = langs[codes[0]]['era']
        first, last = langs[codes[0]]['stage'], langs[codes[-1]]['stage']
        forms = {max(first - 1, 0): d['start']}
        current = d['start']
        by_stage = {}
        for rid, _before, after in hit['trace']:
            if after is not None:
                current = after
                by_stage[seq.by_id[rid].stage] = current
        cur = d['start']
        for s in range(first, last + 1):
            cur = by_stage.get(s, cur)
            if s > 0:
                forms[s] = cur
        forms[last] = d['steps'][-1]['after']
        out.append({'derivation': d['id'], 'word': d['word'], 'era': era, 'forms': forms,
                    'main': hit is variants[0]})
    return out


# --------------------------------------------------------------------------
# helpers

def _skeleton(root_form: str) -> list:
    """Consonant classes of a root: MBAR -> [m, b, r] as equivalence classes."""
    f = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰√()\-]', '', root_form).lower()
    f = f.replace('kh', 'x').replace('th', 'θ').replace('ph', 'f').replace('gw', 'g').replace('kw', 'k')
    out = []
    for ch in f:
        cls = next((i for i, c in enumerate(EQUIV) if ch in c), None)
        if cls is not None:
            out.append(cls)
    return out


def _classes(form: str) -> list:
    out = []
    for p in phonemes(comparable(form)):
        if is_vowel(p):
            continue
        b = p[0]
        cls = next((i for i, c in enumerate(EQUIV) if b in c), None)
        if cls is not None:
            out.append(cls)
    return out


def _class_of(p: str):
    b = p[0]
    return next((i for i, c in enumerate(EQUIV) if b in c), b)


def hint_weight(r: dict) -> float:
    return (ROOT_BONUS if r.get('root') else 1.0) * (STEM_BONUS if r.get('stem') else 1.0)


def root_match(form: str, roots: list) -> bool:
    """The consonants of a root appear in order in the form (by sound class)."""
    cs = _classes(form)
    for r in roots:
        sk = _skeleton(r)
        if not sk:
            continue
        it = iter(cs)
        if all(any(c == k for c in it) for k in sk):
            return True
    return False


def _runs(form: str):
    """(initial consonants, [medial clusters], final consonants) of a form."""
    ph = phonemes(comparable(form))
    vowels = [i for i, p in enumerate(ph) if is_vowel(p)]
    if not vowels:
        return ''.join(ph), [], ''
    initial = ''.join(ph[:vowels[0]])
    final = ''.join(ph[vowels[-1] + 1:])
    medial = []
    for a, b in zip(vowels, vowels[1:]):
        if b - a > 2:
            medial.append(''.join(ph[a + 1:b]))
    return initial, medial, final


def gloss_words(gloss: str | None) -> set:
    """Content words of a gloss, cut as the atlas cuts long glosses (80 characters)."""
    g = gloss or ''
    if len(g) > 80:
        g = g[:77]
    return {w for w in re.findall(r'[a-z]+', g.lower()) if len(w) >= 3 and w not in NEAR_STOP}


def phoneme_distance(a: str, b: str) -> int:
    """Edit distance between two forms counted in phonemes (kw, ŋg are one)."""
    x, y = phonemes(comparable(a).strip('-')), phonemes(comparable(b).strip('-'))
    prev = list(range(len(y) + 1))
    for i in range(1, len(x) + 1):
        cur = [i] + [0] * len(y)
        for j in range(1, len(y) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x[i - 1] != y[j - 1]))
        prev = cur
    return prev[-1]


class Phonotactics:
    """Initial consonant groups, medial clusters and final consonants of a
    language's words; a reconstructed form with an unseen one is flagged."""

    def __init__(self, forms: list):
        self.initials, self.clusters, self.finals = Counter(), Counter(), Counter()
        for f in forms:
            i, ms, fin = _runs(f)
            self.initials[i] += 1
            self.finals[fin] += 1
            for m in ms:
                self.clusters[m] += 1

    def problems(self, form: str, min_count: int = 2) -> list:
        i, ms, fin = _runs(form)
        out = []
        if len(phonemes(i)) > 1 and self.initials[i] < min_count:
            out.append(f'начало {i}-')
        for m in ms:
            if self.clusters[m] < min_count:
                out.append(f'сочетание {m}')
        if fin and self.finals[fin] < min_count:
            out.append(f'конец -{fin}')
        return out


def stage_table(normal: list, era: str, src: int, dst: int, exclude=frozenset()) -> dict:
    """Correspondences 'form at stage dst <- form at stage src' from the
    normalized derivations (dst < src)."""
    pairs = [(n['forms'][dst], n['forms'][src]) for n in normal
             if n['era'] == era and src in n['forms'] and dst in n['forms'] and n['derivation'] not in exclude]
    return BF.learn_pairs(pairs)


def phonotactic_forms(lexicon: dict, branch: str, code: str) -> list:
    return [to_phonetic(e['form'], branch).strip('-') for e in lexicon.values()
            if e['lang'] == code and not e.get('neo') and ' ' not in e['form']]


def export(data: dict) -> dict:
    """Tables for app/wordform.js: stage correspondences for every pair of
    stages of an era, phonotactics of the latest language of each era."""
    from .app import _key
    langs = data['meta']['languages']
    normal = data['stages']
    lexicon = {e['id']: e for e in data['lexicon']}
    branch = data['summary']['branch']
    tables, pts = {}, {}
    for era in sorted({l['era'] for l in langs}):
        stages = sorted(l['stage'] for l in langs if l['era'] == era)
        for src in stages:
            for dst in stages:
                if dst < src:
                    t = stage_table(normal, era, src, dst)
                    tables[f'{era}|{src}|{dst}'] = {_key(k): c.most_common() for k, c in t.items()}
        last = next(l for l in langs if l['era'] == era and l['stage'] == max(stages))
        pt = Phonotactics(phonotactic_forms(lexicon, branch, last['code']))
        pts[last['code']] = {'initials': dict(pt.initials), 'clusters': dict(pt.clusters), 'finals': dict(pt.finals)}
    return {'tables': tables, 'phonotactics': pts}


# --------------------------------------------------------------------------
# context

class Context:
    """Everything reconstruction needs for both branches."""

    def __init__(self, branches: dict):
        self.data = branches
        self.seq = {b: Sequencer(d) for b, d in branches.items()}
        self.lexicon = {b: {e['id']: e for e in d['lexicon']} for b, d in branches.items()}
        self.normal = {b: d.get('stages') or normalize(d, self.seq[b]) for b, d in branches.items()}
        self._tables = {}
        self._phonotactics = {}
        self.reverse_links = defaultdict(list)    # target id -> [(source id, tag)]
        for b, lex in self.lexicon.items():
            for e in lex.values():
                if e['speech'] == 'root':
                    continue
                for tag, ls in e.get('links', {}).items():
                    for x in ls:
                        self.reverse_links[x['id']].append((e['id'], tag))

    # -- languages ---------------------------------------------------------
    def langs(self, branch: str) -> dict:
        return self.seq[branch].langs

    def code(self, branch: str, era: str, stage: int) -> str | None:
        return next((l['code'] for l in self.langs(branch).values() if l['era'] == era and l['stage'] == stage), None)

    def last_stage(self, branch: str, era: str) -> int:
        return max(l['stage'] for l in self.langs(branch).values() if l['era'] == era)

    def entry(self, wid: str):
        for b, lex in self.lexicon.items():
            if wid in lex:
                return b, lex[wid]
        return None, None

    # -- learnt tables -----------------------------------------------------
    def table(self, branch: str, era: str, src: int, dst: int, exclude=frozenset()) -> dict:
        key = (branch, era, src, dst, exclude)
        if key not in self._tables:
            self._tables[key] = stage_table(self.normal[branch], era, src, dst, exclude)
        return self._tables[key]

    def phonotactics(self, branch: str, code: str) -> Phonotactics:
        if (branch, code) not in self._phonotactics:
            self._phonotactics[(branch, code)] = Phonotactics(phonotactic_forms(self.lexicon[branch], branch, code))
        return self._phonotactics[(branch, code)]

    def near_words(self, branch: str, code: str, prim: str, gloss: str, limit: int = 3) -> list:
        """Attested words of a language whose Eldamo primitive form is the given
        one or one sound away from it, and whose meaning shares a word with the
        gloss: Q. erinqua < ✶eriŋkwā 'single, alone' ~ S. ereb < ✶erikwā."""
        words = gloss_words(gloss)
        if not words or len(phonemes(comparable(prim))) < 4:
            return []
        era = self.langs(branch)[code]['era']
        out = []
        for e in self.lexicon[branch].values():
            if e['lang'] != code or e.get('neo') or e['speech'] == 'root':
                continue
            shared = words & gloss_words(e.get('gloss'))
            if not shared:
                continue
            dist = min((phoneme_distance(prim, o) for o in origins(e, era)), default=9)
            if dist <= 1:
                out.append((dist, -len(shared), e['form'], e))
        out.sort(key=lambda t: t[:3])
        return [(e, d) for d, _, _, e in out[:limit]]

    # -- routes ------------------------------------------------------------
    def forward(self, branch: str, era: str, form: str, src: int, dst: int) -> list:
        """[(form, trace)] main reading first."""
        seq = self.seq[branch]
        rules = seq.sequence(era, src + 1 if src > 0 else 0, dst)
        return [(v['form'], v['trace']) for v in seq.run(form, rules)]

    seed_roots = True
    use_elements = True

    def _root_seeds(self, seq, add, branch, era, form, src, starts, found):
        """Primitive forms that begin with the word's root: the root (without a final vowel)
        put in place of the beginning of a found candidate, up to the consonant of the root's
        last consonant's class (Q. hyarma: ✶j̊arma -> √KHYAR + -ma = ✶kʰjarma). Kept only when
        the laws lead from it to the form; the beginning of a form is where the backward search
        guesses most (hy- < kʰj- or sj-), and the root says which it was."""
        target = comparable(form)
        for rp in starts[:3]:
            rph = phonemes(rp)
            while rph and is_vowel(rph[-1]):
                rph = rph[:-1]
            last = next((p for p in reversed(rph) if not is_vowel(p)), None)
            if last is None:
                continue
            cls = _class_of(last)
            for r in found[:4]:
                cph = phonemes(comparable(r['form']))
                j = next((i for i, p in enumerate(cph) if not is_vowel(p) and _class_of(p) == cls), None)
                if j is None:
                    continue
                f0 = r['form']
                # a stem or an affix keeps its hyphens (fara- < ✶spara-)
                seed = ('-' if f0.startswith('-') else '') + ''.join(rph + cph[j + 1:]) + ('-' if f0.endswith('-') and len(f0) > 1 else '')
                if comparable(seed) == comparable(f0):
                    continue
                for f, trace in self.forward(branch, era, seed, 0, src)[:4]:
                    if comparable(f) == target:
                        add(seed, r['p'], trace, 'root ' + rp)
                        break

    def stem_match(self, branch: str, era: str, form: str, src: int, dst: int, stems) -> bool:
        """The form at stage src, run to stage dst as a stem (not the end of a word), gives one
        of the word's stems, with or without its last vowel (Ambar, ambar- < ✶ambara)."""
        outs = set()
        for f, _ in self.forward(branch, era, form.rstrip('-') + '-', src, dst)[:6]:
            ph = phonemes(comparable(f).strip('-'))
            outs.add(''.join(ph))
            if ph and is_vowel(ph[-1]):
                outs.add(''.join(ph[:-1]))
        return any(s in outs for s in stems)

    def backward(self, branch: str, era: str, form: str, src: int, dst: int, hints=NO_HINTS, exclude=frozenset(),
                 limit: int = LIMIT) -> list:
        """[{'form', 'p', 'trace', 'root', 'stem', 'via'}]: forms at stage dst that give `form`
        at stage src; directly and, for dst > 0, through the primitive form. hints: the word's
        roots and its stems at stage src (_hints)."""
        seq = self.seq[branch]
        out = {}
        roots, stems = hints['roots'], hints['stems']

        def add(f, p, trace, via):
            k = comparable(f)
            rec = {'form': f, 'p': p, 'trace': trace, 'via': via, 'root': bool(roots) and root_match(f, roots)}
            if k not in out or out[k]['p'] < p:
                out[k] = rec

        first = dst + 1 if dst > 0 else 0
        for search in (SEARCH, WIDE):
            self._backward(seq, add, branch, era, form, src, dst, first, exclude, limit, search)
            if out:
                break
        if dst == 0 and hints.get('starts') and self.seed_roots and out:
            self._root_seeds(seq, add, branch, era, form, src, hints['starts'], sorted(out.values(), key=lambda r: -r['p']))
        for r in out.values():
            r['stem'] = bool(stems) and self.stem_match(branch, era, r['form'], dst, src, stems)
        ranked = sorted(out.values(), key=lambda r: -(r['p'] * hint_weight(r)))
        return ranked[:limit]

    def _backward(self, seq, add, branch, era, form, src, dst, first, exclude, limit, search):
        found = BF.backform(seq, self.table(branch, era, src, dst, exclude), form, era, src, limit=limit,
                            first_stage=first, **search)
        for f in found:
            add(f['primitive'], math.exp(f['logp']) * (1.0 if f['main'] else 0.5), f['trace'], 'direct')
        if dst > 0:
            prims = BF.backform(seq, self.table(branch, era, src, 0, exclude), form, era, src, limit=4, **search)
            for f in prims:
                # the form at stage dst on the very run that gave `form`
                trace = [t for t in f['trace'] if seq.by_id[t[0]].stage <= dst]
                g = next((t[2] for t in reversed(trace) if t[2] is not None), f['primitive'])
                add(g, math.exp(f['logp']) * (1.0 if f['main'] else 0.5), trace, 'primitive ' + f['primitive'])


# --------------------------------------------------------------------------
# the entry point

def _stage_form(ctx: Context, branch: str, entry: dict, era: str, stage: int) -> list:
    """Attested forms of a word at a stage of its own branch and era: its own
    form at its language's stage, its derivation forms, its primitive forms."""
    code = ctx.code(branch, era, stage)
    out = []
    if code and entry['lang'] == code:
        out.append(to_phonetic(entry['form'], branch).strip())
    if stage == 0:
        out += _origins(entry, era)
    elif code:
        out += list(entry.get('stages', {}).get(code, ()))
    return list(dict.fromkeys(f for f in out if f))


def _origins(entry: dict, era: str) -> list:
    """Primitive forms of a word; a verb stem (fara-) or an affix (-ima) keeps its hyphen,
    so that the laws of word ends do not act on it."""
    f = (entry.get('form') or '').strip()
    lead, trail = f.startswith('-'), f.endswith('-') and len(f) > 1
    return [('-' if lead and not o.startswith('-') else '') + o + ('-' if trail and not o.endswith('-') else '')
            for o in origins(entry, era)]


def _hints(ctx: Context, branch: str, entry: dict | None, era: str, stage: int) -> dict:
    """What the word tells besides its form: its roots, and its stems (Q. nér, ner-; lindë,
    lindi-) when the form is that of the word's own language. Verbs and affixes are given as
    stems already."""
    if entry is None:
        return NO_HINTS
    roots = [r['form'] for r in entry.get('roots', ())]
    # the roots the word begins with: its own, or those of its first element
    starts = [root_phonetic(r['form']) for r in entry.get('roots', ()) if r.get('part', 0) == 0]
    stems = []
    f = (entry.get('form') or '').strip()
    if entry.get('stems') and entry['lang'] == ctx.code(branch, era, stage) and not f.endswith('-') and not f.startswith('-'):
        for x in entry['stems']:
            x = re.sub(r'[*()]', '', x).strip().rstrip('-')
            if x:
                stems.append(''.join(phonemes(comparable(to_phonetic(x, branch).strip()).strip('-'))))
    return {'roots': roots, 'stems': list(dict.fromkeys(stems)), 'starts': [x for x in dict.fromkeys(starts) if x]}


def reconstruct(ctx: Context, src: tuple, dst: tuple, form: str | None = None, word: str | None = None,
                limit: int = LIMIT, use_links: bool = True, exclude=frozenset(), spelled: bool = False) -> list:
    """Variants of the form at dst = (branch, era, stage), from the form at src.

    Either `word` (an Eldamo page id) or `form` (in Eldamo's phonetic notation;
    with spelled=True, in Tolkien's spelling of the latest stage) gives the source. Returns
    [{'form', 'score', 'route', 'marks', 'steps'}], most probable first."""
    sb, se, ss = src
    db, de, ds = dst
    entry = None
    if word:
        _, entry = ctx.entry(word)
    if form is None:
        if entry is None:
            return []
        forms = _stage_form(ctx, sb, entry, se, ss)
        if not forms and entry['lang'] == ctx.code(sb, se, ss):
            forms = [to_phonetic(entry['form'], sb)]
        if not forms:
            return []
        form = forms[0]
    elif spelled:
        form = to_phonetic(form, sb).strip()
    hints = _hints(ctx, sb, entry, se, ss)
    results = {}

    def add(f, score, route, marks, steps):
        k = comparable(f)
        rec = {'form': f.replace('+', ''), 'score': score, 'route': route, 'marks': marks, 'steps': steps}
        if k not in results or results[k]['score'] < score:
            results[k] = rec

    # attested in Eldamo: the word's own forms at the target period
    if entry is not None and (db, de) == (sb, se):
        for f in _stage_form(ctx, db, entry, de, ds):
            add(f, 10.0, 'засвидетельствовано', ['attested'], [])

    if (db, de) == (sb, se):
        _within(ctx, add, sb, se, form, ss, ds, hints, exclude)
    elif de == se:
        _sideways(ctx, add, src, dst, form, entry, hints, exclude, use_links)
    else:
        _across(ctx, add, src, dst, form, entry, hints, exclude, use_links)

    # a form the target language does not allow (initial group, cluster, ending
    # unseen in its words) is kept but ranked down
    if dst_code_has_words(ctx, db, de, ds):
        pt = ctx.phonotactics(db, ctx.code(db, de, ds))
        for r in results.values():
            if {'attested', 'link', 'near-cognate'} & set(r['marks']):
                continue
            problems = pt.problems(r['form'])
            if problems:
                r['score'] *= PHONOTACTIC_PENALTY
                if 'phonotactics' not in r['marks']:
                    r['marks'] = r['marks'] + ['phonotactics']
                    r['problems'] = problems
    ranked = sorted(results.values(), key=lambda r: -r['score'])
    total = sum(r['score'] for r in ranked) or 1.0
    for r in ranked:
        r['score'] = round(r['score'] / total, 3)
    return ranked[:limit]


def dst_code_has_words(ctx: Context, branch: str, era: str, stage: int) -> bool:
    """Phonotactics are known for the latest stage of an era (its words are in the lexicon)."""
    return stage == ctx.last_stage(branch, era) and ctx.code(branch, era, stage) is not None


def _within(ctx, add, branch, era, form, ss, ds, hints, exclude, base_score=1.0, route_prefix='', marks=()):
    if ds == ss:
        add(form, base_score, route_prefix + 'та же стадия', list(marks), [])
    elif ds > ss:
        for k, (f, trace) in enumerate(ctx.forward(branch, era, form, ss, ds)[:4]):
            add(f, base_score * (1.0 if k == 0 else 0.5 / k), route_prefix + 'вперёд по законам',
                list(marks) + (['main'] if k == 0 else []), trace)
    else:
        found = ctx.backward(branch, era, form, ss, ds, hints, exclude)
        # hints reorder the candidates but never lift them above 0.9 of the base score
        top = max((r['p'] * hint_weight(r) for r in found), default=1.0) or 1.0
        for r in found:
            p = base_score * 0.9 * r['p'] * hint_weight(r) / top
            how = 'напрямую' if r['via'] == 'direct' else 'по корню' if r['via'].startswith('root') else 'через праформу'
            add(r['form'], p, route_prefix + 'назад: ' + how,
                list(marks) + ['reconstructed'] + (['root'] if r['root'] else []) + (['stem'] if r['stem'] else []),
                r['trace'])


ELEMENTS_SCORE = 1.9     # below an attested word of the target language (link 5, near cognate 2-3), above the laws (1.0)


def _counterparts(ctx, wid: str, branch: str, code: str) -> list:
    """Words of the target language Eldamo links to a word as cognates, either way."""
    _, e = ctx.entry(wid)
    if e is None:
        return []
    ids = [x['id'] for x in e.get('links', {}).get('cognate', ())]
    ids += [w for w, tag in ctx.reverse_links.get(wid, []) if tag == 'cognate']
    out = []
    for i in dict.fromkeys(ids):
        b2, e2 = ctx.entry(i)
        if b2 == branch and e2 is not None and e2['lang'] == code:
            out.append(i)
    return out


def _by_elements(ctx, add, entry, era, db, ds):
    """A compound or derivative of the other branch built again from the cognates of its
    elements by the word formation of the target language (shared/compound.py): S. Adanel =
    Adan + -iel¹, cognates Q. Atan + -iel -> Q. Atanel, Ataniel. The word is built at the latest
    stage, when every element has a cognate there; for an earlier stage it is taken back from
    it by the laws (✶atanel, not the ✶ataneli of the Sindarin form read backwards)."""
    els = entry.get('elements') or []
    last = ctx.last_stage(db, era)
    code = ctx.code(db, era, last)
    if len(els) < 2 or code is None or not all(x.get('id') for x in els):
        return
    ids = []
    for x in els:
        c = _counterparts(ctx, x['id'], db, code)
        if not c:
            return
        ids.append(c[0])
    from . import affixes, compound, junctions
    if (db, 'wf') not in ctx._tables:
        data = ctx.data[db]
        ctx._tables[(db, 'wf')] = ({e['id']: e for e in data['lexicon']},
                                   junctions.learn(data['junctions']['cases']),
                                   affixes.learn(data['affixes']['cases']))
    lex, table, model = ctx._tables[(db, 'wf')]
    vs = compound.predict(lex, ctx.seq[db], ids, era, last, table=table, affix_model=model)
    top = max((v['score'] for v in vs), default=0) or 1.0
    names = ' + '.join(lex[i]['form'] for i in ids)
    if ds == last:
        for v in vs[:4]:
            add(v['form'], ELEMENTS_SCORE * v['score'] / top, f'по когнатам составляющих: {names}', ['elements'], [])
        return
    # an earlier stage: back from the word so built, so that the stages agree with it
    for v in vs[:2]:
        _within(ctx, add, db, era, v['form'], last, ds, NO_HINTS, frozenset(), base_score=ELEMENTS_SCORE * v['score'] / top,
                route_prefix=f'по когнатам составляющих: {names}, затем ', marks=['elements'])


def _sideways(ctx, add, src, dst, form, entry, hints, exclude, use_links=True):
    sb, era, ss = src
    db, _, ds = dst
    if use_links and entry is not None:
        # Eldamo's own cognates in the target branch
        linked = [x['id'] for x in entry.get('links', {}).get('cognate', ())]
        linked += [wid for wid, tag in ctx.reverse_links.get(entry['id'], []) if tag == 'cognate']
        for wid in dict.fromkeys(linked):
            b2, e2 = ctx.entry(wid)
            l2 = ctx.langs(db).get(e2['lang']) if e2 is not None and b2 == db else None
            if l2 is None or l2['era'] != era:
                continue
            f2 = to_phonetic(e2['form'], db).strip()
            if l2['stage'] == ds:
                add(f2, 5.0, f'когнат по связи Eldamo: {e2["form"]}', ['link'], [])
            elif l2['stage'] < ds:
                _within(ctx, add, db, era, f2, l2['stage'], ds, _hints(ctx, db, e2, era, l2['stage']), exclude, base_score=4.0,
                        route_prefix=f'когнат по связи Eldamo {e2["form"]}, затем ', marks=['link'])
    if entry is not None and ctx.use_elements:
        _by_elements(ctx, add, entry, era, db, ds)
    prims = []
    if entry is not None:
        prims = [(f, 1.0, ['primitive-attested']) for f in _origins(entry, era)]
    if not prims:
        if ss == 0:
            prims = [(form, 1.0, [])]
        else:
            found = ctx.backward(sb, era, form, ss, 0, hints, exclude)
            top = max((r['p'] * hint_weight(r) for r in found), default=1.0) or 1.0
            prims = [(r['form'], r['p'] * hint_weight(r) / top, ['reconstructed'])
                     for r in found[:5]]
    for prim, w, marks in prims:
        _within(ctx, add, db, era, prim, 0, ds, NO_HINTS, exclude, base_score=w,
                route_prefix=f'через праформу {prim}: ', marks=marks + ['cognate'])
    # attested words of the target language with a near primitive form and a shared meaning
    code = ctx.code(db, era, ds)
    if entry is not None and code is not None and ds == ctx.last_stage(db, era):
        for prim, _, _ in prims[:2]:
            for e2, dist in ctx.near_words(db, code, prim, entry.get('gloss', '')):
                start = origins(e2, era)[0]
                add(to_phonetic(e2['form'], db).strip(), 3.0 if dist == 0 else 2.0,
                    f'слово Eldamo {e2["form"]} «{e2.get("gloss", "")}» с {"той же" if dist == 0 else "близкой"} праформой {start}',
                    ['near-cognate'], [])


def _across(ctx, add, src, dst, form, entry, hints, exclude, use_links):
    sb, se, ss = src
    db, de, ds = dst
    dst_code = ctx.code(db, de, ds)
    # (a) Eldamo's links between conceptions
    if use_links and entry is not None:
        linked = []
        for tag, ls in entry.get('links', {}).items():
            if tag in ('combine', 'deprecated', 'see'):
                linked += [(x['id'], tag) for x in ls]
        linked += ctx.reverse_links.get(entry['id'], [])
        for wid, tag in linked:
            b2, e2 = ctx.entry(wid)
            if e2 is None or b2 != db or e2['speech'] == 'root':
                continue
            l2 = ctx.langs(db).get(e2['lang'])
            if l2 is None or l2['era'] != de:
                continue
            f2 = to_phonetic(e2['form'], db).strip()
            if l2['stage'] == ds:
                add(f2, 5.0, f'связь Eldamo ({tag}): {e2["form"]}', ['link'], [])
            else:
                _within(ctx, add, db, de, f2, l2['stage'], ds, _hints(ctx, db, e2, de, l2['stage']), exclude, base_score=4.0,
                        route_prefix=f'связь Eldamo ({tag}) {e2["form"]}, затем ', marks=['link'])
    # (b) unchanged, when the target language allows the form
    if ss == ctx.last_stage(sb, se) and ds == ctx.last_stage(db, de) and sb == db and dst_code:
        add(form, 1.0, 'без изменений', ['unchanged'], [])
    # (c) re-etymologization: primitive of the source conception -> laws of the target one
    prims = []
    if entry is not None:
        prims = [(f, 1.0) for f in _origins(entry, se)]
    if not prims:
        if ss == 0:
            prims = [(form, 1.0)]
        else:
            found = ctx.backward(sb, se, form, ss, 0, hints, exclude)
            top = max((r['p'] * hint_weight(r) for r in found), default=1.0) or 1.0
            prims = [(r['form'], r['p'] * hint_weight(r) / top) for r in found[:4]]
    for prim, w in prims:
        _within(ctx, add, db, de, prim, 0, ds, NO_HINTS, exclude, base_score=0.6 * w,
                route_prefix=f'переэтимологизация через праформу {prim}: ', marks=['neologism'])


# --------------------------------------------------------------------------
# evaluation on Eldamo (reports/reconstruction.md)

def _evaluation_jobs(ctx: Context, sample: int) -> tuple[list, dict]:
    """The cases of evaluate(), drawn in a fixed order from one random generator: [(path, kind,
    params)] and the constant fields of each group. A case does not depend on any other, so the
    cases can run in any order and in several processes with the same result."""
    import random
    rnd = random.Random(11)
    jobs, fixed = [], {}
    # A: backward from the last stage of an era to each earlier stage
    for b in ctx.data:
        for era in ('late', 'middle', 'early'):
            last = ctx.last_stage(b, era)
            norm = [n for n in ctx.normal[b] if n['era'] == era and last in n['forms']]
            held = norm[1::2]
            exclude = frozenset(n['derivation'] for n in held)
            for t in range(last):
                path = (b, f'{era}: {last} -> {t}')
                fixed[path] = {}
                cases = [n for n in held if t in n['forms']]
                for n in rnd.sample(cases, min(sample, len(cases))):
                    jobs.append((path, 'stage', ((b, era, last), (b, era, t), n['forms'][last], n['forms'][t], exclude)))
    # B: cognates with the same primitive form, Q <-> S (late)
    starts = defaultdict(dict)
    for b in ctx.data:
        last = ctx.last_stage(b, 'late')
        for n in ctx.normal[b]:
            if n['era'] == 'late' and 0 in n['forms'] and last in n['forms']:
                starts[comparable(n['forms'][0])][b] = n['forms'][last]
    pairs = [(v['quenya'], v['sindarin']) for v in starts.values() if 'quenya' in v and 'sindarin' in v]
    for (sb, db), idx in ((('quenya', 'sindarin'), (0, 1)), (('sindarin', 'quenya'), (1, 0))):
        path = (f'cognates {sb} -> {db}',)
        fixed[path] = {'pairs': len(pairs)}
        for pr in rnd.sample(pairs, min(sample, len(pairs))):
            jobs.append((path, 'cognate', ((sb, 'late', ctx.last_stage(sb, 'late')),
                                           (db, 'late', ctx.last_stage(db, 'late')), pr[idx[0]], pr[idx[1]])))
    # B': Eldamo's cognate links Q. <-> S. (late), from the word and from its form alone
    for sb, db, sc, dc in (('quenya', 'sindarin', 'q', 's'), ('sindarin', 'quenya', 's', 'q')):
        lex, other = ctx.lexicon[sb], ctx.lexicon[db]
        pairs = [(e['id'], x['id']) for e in lex.values() if e['lang'] == sc and not e.get('neo')
                 for x in e.get('links', {}).get('cognate', ()) if x['id'] in other and other[x['id']]['lang'] == dc]
        pairs = list(dict.fromkeys(pairs))
        path = (f'cognate links {sc} -> {dc}',)
        fixed[path] = {'pairs': len(pairs)}
        for a, t in rnd.sample(pairs, min(sample, len(pairs))):
            jobs.append((path, 'link', (sb, db, a, t)))
    # C: conceptions, without using the link being tested
    for b, src_code, dst_code in (('quenya', 'mq', 'q'), ('sindarin', 'n', 's'), ('quenya', 'eq', 'q'),
                                  ('sindarin', 'g', 's')):
        lex = ctx.lexicon[b]
        pairs = []
        for e in lex.values():
            if e['lang'] != src_code or e.get('neo'):
                continue
            for tag in ('combine', 'deprecated'):
                for x in e.get('links', {}).get(tag, ()):
                    t = lex.get(x['id'])
                    if t is not None and t['lang'] == dst_code:
                        pairs.append((e['id'], t['id']))
        pairs = list(dict.fromkeys(pairs))
        path = (f'conceptions {src_code} -> {dst_code}',)
        fixed[path] = {'pairs': len(pairs)}
        for a, t in rnd.sample(pairs, min(sample, len(pairs))):
            jobs.append((path, 'conception', (b, src_code, dst_code, a, t)))
    # D: stems -- words with a stem and an Eldamo primitive, backward to the primitive with and
    # without the stem (Q. lindë, lindi- < ✶lindi)
    for b, code in (('quenya', 'q'), ('quenya', 'mq'), ('sindarin', 's'), ('sindarin', 'n')):
        era = ctx.langs(b)[code]['era']
        words = sorted((e for e in ctx.lexicon[b].values() if e['lang'] == code and not e.get('neo')
                        and _hints(ctx, b, e, era, ctx.langs(b)[code]['stage'])['stems'] and origins(e, era)),
                       key=lambda e: e['id'])
        path = (f'stems {code}',)
        fixed[path] = {'words': len(words)}
        for e in rnd.sample(words, min(sample, len(words))):
            jobs.append((path, 'stem', (b, code, e['id'])))
    # E': compounds of one branch with a cognate in the other: rebuilt from the cognates of the
    # elements (_by_elements), without the word's own link
    for sb, db, sc, dc in (('quenya', 'sindarin', 'q', 's'), ('sindarin', 'quenya', 's', 'q')):
        lex, other = ctx.lexicon[sb], ctx.lexicon[db]
        pairs = []
        for e in lex.values():
            if e['lang'] != sc or e.get('neo') or len(e.get('elements') or []) < 2:
                continue
            for x in e.get('links', {}).get('cognate', ()):
                if x['id'] in other and other[x['id']]['lang'] == dc:
                    pairs.append((e['id'], x['id']))
        pairs = sorted(dict.fromkeys(pairs))
        path = (f'compounds {sc} -> {dc}',)
        fixed[path] = {'pairs': len(pairs)}
        for a, t in rnd.sample(pairs, min(sample, len(pairs))):
            jobs.append((path, 'compound', (sb, db, a, t)))
    # E: roots -- words with a root and an Eldamo primitive, backward to the primitive with and
    # without primitive forms begun by the root (Context._root_seeds)
    for b, code in (('quenya', 'q'), ('quenya', 'mq'), ('sindarin', 's'), ('sindarin', 'n')):
        era = ctx.langs(b)[code]['era']
        words = sorted((e for e in ctx.lexicon[b].values() if e['lang'] == code and not e.get('neo')
                        and e['speech'] != 'root' and e.get('roots') and origins(e, era)), key=lambda e: e['id'])
        path = (f'root seeds {code}',)
        fixed[path] = {'words': len(words)}
        for e in rnd.sample(words, min(sample, len(words))):
            jobs.append((path, 'seed', (b, code, e['id'])))
    return jobs, fixed


def _evaluation_case(ctx: Context, kind: str, params: tuple) -> dict:
    """Counts of one case of evaluate()."""
    st = Counter()
    if kind == 'stage':
        src, dst, form, want, exclude = params
        got = [comparable(v['form']) for v in reconstruct(ctx, src, dst, form=form, exclude=exclude)]
        want = comparable(want)
        st.update(cases=1, found=bool(got), first=bool(got) and got[0] == want, any=want in got)
    elif kind == 'cognate':
        src, dst, form, want = params
        got = [comparable(v['form']) for v in reconstruct(ctx, src, dst, form=form)]
        want = comparable(want)
        st.update(cases=1, first=bool(got) and got[0] == want, any=want in got)
    elif kind == 'link':
        sb, db, a, t = params
        lex, other = ctx.lexicon[sb], ctx.lexicon[db]
        want = comparable(to_phonetic(other[t]['form'], db).strip('-'))
        src = (sb, 'late', ctx.last_stage(sb, 'late'))
        dst = (db, 'late', ctx.last_stage(db, 'late'))
        st['cases'] += 1
        # by the word: its Eldamo primitive and near attested words, but not the link being tested
        for key, kw in (('word', {'word': a, 'use_links': False}),
                        ('form', {'form': to_phonetic(lex[a]['form'], sb).strip('-')})):
            got = [comparable(v['form']) for v in reconstruct(ctx, src, dst, **kw)]
            st[key + '_first'] += bool(got) and got[0] == want
            st[key + '_any'] += want in got
    elif kind == 'conception':
        b, src_code, dst_code, a, t = params
        lex, langs = ctx.lexicon[b], ctx.langs(b)
        sl, dl = langs[src_code], langs[dst_code]
        want = comparable(to_phonetic(lex[t]['form'], b).strip('-'))
        vs = reconstruct(ctx, (b, sl['era'], sl['stage']), (b, dl['era'], dl['stage']), word=a, use_links=False)
        got = [comparable(v['form']) for v in vs]
        st.update(cases=1, identity=comparable(to_phonetic(lex[a]['form'], b).strip('-')) == want,
                  first=bool(got) and got[0] == want, any=want in got)
    elif kind == 'stem':
        b, code, wid = params
        e = ctx.lexicon[b][wid]
        l = ctx.langs(b)[code]
        era, stage = l['era'], l['stage']
        hints = _hints(ctx, b, e, era, stage)
        want = {comparable(o).strip('-') for o in origins(e, era)}
        form = to_phonetic(e['form'], b).strip()
        found = ctx.backward(b, era, form, stage, 0, hints, frozenset(e.get('derivations', ())))
        plain = sorted(found, key=lambda r: -(r['p'] * (ROOT_BONUS if r['root'] else 1.0)))
        trial = sorted(found, key=lambda r: -(r['p'] * (ROOT_BONUS if r['root'] else 1.0)
                                              * (STEM_TRIAL if r['stem'] else 1.0)))
        st['cases'] += 1
        st['gold_stem'] += any(ctx.stem_match(b, era, o, 0, stage, hints['stems']) for o in origins(e, era))
        for key, ranked in (('plain', plain), ('stem', trial)):
            got = [comparable(r['form']).strip('-') for r in ranked]
            st[key + '_first'] += bool(got) and got[0] in want
            st[key + '_any'] += any(g in want for g in got)
    elif kind == 'compound':
        sb, db, a, t = params
        want = comparable(to_phonetic(ctx.lexicon[db][t]['form'], db).strip('-'))
        src = (sb, 'late', ctx.last_stage(sb, 'late'))
        dst = (db, 'late', ctx.last_stage(db, 'late'))
        st['cases'] += 1
        for key, on in (('plain', False), ('elements', True)):
            ctx.use_elements = on
            try:
                vs = reconstruct(ctx, src, dst, word=a, use_links=False)
            finally:
                ctx.use_elements = True
            got = [comparable(v['form']).strip('-') for v in vs]
            st[key + '_first'] += bool(got) and got[0] == want
            st[key + '_any'] += want in got
            if on:
                st['built'] += any('elements' in v['marks'] for v in vs)
    elif kind == 'seed':
        b, code, wid = params
        e = ctx.lexicon[b][wid]
        l = ctx.langs(b)[code]
        era, stage = l['era'], l['stage']
        hints = _hints(ctx, b, e, era, stage)
        want = {comparable(o).strip('-') for o in origins(e, era)}
        form = to_phonetic(e['form'], b).strip()
        st['cases'] += 1
        for key, seed in (('plain', False), ('seed', True)):
            ctx.seed_roots = seed
            try:
                got = [comparable(r['form']).strip('-') for r in
                       ctx.backward(b, era, form, stage, 0, hints, frozenset(e.get('derivations', ())))]
            finally:
                ctx.seed_roots = True
            st[key + '_first'] += bool(got) and got[0] in want
            st[key + '_any'] += any(g in want for g in got)
    return dict(st)


_EVAL_CTX = None


def _evaluation_worker(job):
    path, kind, params = job
    return path, _evaluation_case(_EVAL_CTX, kind, params)


def evaluate(ctx: Context, sample: int = 80, processes: int | None = None) -> dict:
    """Reconstruction checked on Eldamo (reports/reconstruction.md). The cases run in
    `processes` processes (default: the number of CPUs; 1 runs them here); where processes
    cannot be forked (Windows), they run here."""
    import multiprocessing as mp
    import os
    global _EVAL_CTX
    jobs, fixed = _evaluation_jobs(ctx, sample)
    if processes is None:
        processes = int(os.environ.get('QUETTAMIN_JOBS') or os.cpu_count() or 1)
    _EVAL_CTX = ctx
    try:
        if processes > 1 and 'fork' in mp.get_all_start_methods():
            with mp.get_context('fork').Pool(processes) as pool:
                done = pool.map(_evaluation_worker, jobs, chunksize=1)
        else:
            done = [_evaluation_worker(j) for j in jobs]
    finally:
        _EVAL_CTX = None
    totals = {path: Counter() for path in fixed}
    for path, counts in done:
        totals[path].update(counts)
    out = {}
    for path, st in totals.items():
        rec = {k: v for k, v in st.items()}
        rec.update(fixed[path])
        if len(path) == 2:
            out.setdefault(path[0], {})[path[1]] = rec
        else:
            out[path[0]] = rec
    return out
