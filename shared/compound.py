"""Compounds: join elements at a chosen stage and let the later sound laws act.

    predict(lexicon_entries, sequencer, ['id1', 'id2'], era='late', stage=0)

1. Each element is taken at the stage of formation: its attested form at that
   stage (from a derivation of the element) or, failing that, its primitive
   form run through the rules up to that stage. At the word's own (latest)
   stage: its stem, then its dictionary form, in phonetic notation.
2. The forms are joined with a morpheme boundary (+). Junction variants: the
   full first element and the first element without its final vowel.
3. The joined form runs through the rules of the later stages; rules with +
   now see the boundary.

Every variant keeps its trace (rules applied) and the forms it was built from.
The benchmark (backtest) uses Eldamo's compounds that have both elements and
an attested derivation from a primitive form.
"""
from __future__ import annotations

import itertools
import re

from . import junctions as junction_table
from . import morphophonology

from .interpreter import comparable, is_vowel, join, phonemes
from .orthography import to_phonetic

MAX_ORIGINS = 4
MAX_JOINS = 12


def _clean(form: str) -> str:
    """Written primitive form as a phonetic string: Aika-nār- -> aikanār, kiryā́ -> kiryā."""
    f = form.replace('-', '').replace('(', '').replace(')', '').replace('’', '').replace('/', '')
    f = ''.join(ch for ch in f if ch != '́')
    return f.lower() if f[:1].isupper() and not f.isupper() else f


def origins(entry: dict, era: str) -> list:
    """Primitive forms of a word: phonetic starts of its derivations and its
    forms at the end of the primitive stage; written origins only when there is
    no derivation. Roots written in capitals (MBAR) are not forms."""
    proto = 'mp' if era == 'middle' else 'p'
    out = list(entry.get('starts', ())) + list(entry.get('stages', {}).get(proto, ()))
    if not out:
        out = [w for w in entry.get('written_origins', ()) if w.upper() != w]
    seen, clean = set(), []
    for f in out:
        c = _clean(f)
        if c and comparable(c) not in seen:
            seen.add(comparable(c))
            clean.append(c)
    return clean[:MAX_ORIGINS]


def forms_at(entry: dict, seq, era: str, stage: int, final: bool = False) -> list:
    """(form, how) for a word at the end of `stage` (0 = primitive)."""
    langs = [l for l in seq.langs.values() if l['era'] == era]
    code = next((l['code'] for l in langs if l['stage'] == stage), None)
    attested = list(entry.get('stages', {}).get(code, ())) if code and stage > 0 else []
    out = [(f, 'attested') for f in attested]
    if out:
        return out
    if code and entry.get('lang') == code:
        # the word's own language: its stem (the combining form) or its dictionary form
        family = seq.branch
        # (the last element of a compound keeps its own ending)
        out = [] if final else [(to_phonetic(x, family).rstrip('-'), 'stem') for x in entry.get('stems', ())]
        out.append((to_phonetic(entry['form'], family).rstrip('-'), 'dictionary'))
        seen = set()
        return [(f, h) for f, h in out if f and not (comparable(f) in seen or seen.add(comparable(f)))]
    base = [(f, 'primitive') for f in origins(entry, era)]
    final = max(langs, key=lambda l: l['stage'])['code']
    if not base and entry.get('lang') == final:
        # no primitive form in Eldamo: reconstruct one (shared/backform.py)
        from .backform import backform
        word = to_phonetic(entry['form'], seq.branch).rstrip('-')
        found = backform(seq, seq.backform_table(final), word, era, max(l['stage'] for l in langs), limit=3)
        base = [(f['primitive'], 'reconstructed') for f in found]
    if stage == 0:
        return base
    rules = seq.sequence(era, 0, stage)
    for f, how in base:
        for v in seq.run(f, rules)[:2]:
            out.append((v['form'], 'computed' if how == 'primitive' else 'reconstructed'))
    return out


def junctions(a: str, b: str) -> list:
    """(joined, label): the full first element, and without its final vowel."""
    out = [(a + '+' + b, 'full')]
    pa = phonemes(a)
    if len(pa) > 1 and is_vowel(pa[-1]):
        out.append((join(pa[:-1]) + '+' + b, 'elided'))
    return out


POLYSYLLABLE_RULES = re.compile(r'polysyllab', re.I)
LENITION_WEIGHT = 0.2   # the junction table already holds attested lenitions
MORPH_WEIGHT = 0.3      # prior of an optional synchronic adjustment (§6.1)


def predict_latest(lexicon: dict, seq, table: dict, element_ids: list, era: str = 'late') -> list:
    """Two elements joined at the latest stage of the branch.

    The junction table (shared/junctions.py) gives the junction and ending
    variants with their frequency among attested compounds. Quenya adds the
    adjustments of the course, §6.1 (shared/morphophonology.py); Sindarin runs
    the rules of its last stage that apply to polysyllables, since a compound
    is a new polysyllable (S. [au] > [o]: aeg + naur > Aegnor)."""
    last = max(l['stage'] for l in seq.langs.values() if l['era'] == era)
    if len(element_ids) != 2 or table is None:
        return []
    firsts = forms_at(lexicon[element_ids[0]], seq, era, last) if element_ids[0] in lexicon else []
    seconds = forms_at(lexicon[element_ids[1]], seq, era, last, final=True) if element_ids[1] in lexicon else []
    if seq.branch == 'sindarin':
        # the second element of a Sindarin compound is usually lenited
        for b, hb in list(seconds):
            m = morphophonology.lenite(phonemes(comparable(b)))
            if m is not None:
                seconds.append((join(m), 'soft-mutation'))
    poly = [c for c in seq.sequence(era, last, last) if POLYSYLLABLE_RULES.search(c.name)]
    scored = {}

    def add(form, score, info):
        key = comparable(form)
        if key not in scored or scored[key][0] < score:
            scored[key] = (score, form, info)

    for (a, ha), (b, hb) in itertools.product(firsts, seconds):
        pa, pb = phonemes(comparable(a)), phonemes(comparable(b))
        # a first element that has a stem joins by it more often (Q.: 2 of 3)
        weight = 0.5 if ha == 'dictionary' and any(h == 'stem' for _, h in firsts) else 1.0
        if hb == 'soft-mutation':
            weight *= LENITION_WEIGHT
        for form, p, jop, eop, short in junction_table.predict(table, pa, pb, limit=10):
            p *= weight
            info = {'joined': a + '+' + b, 'elements': [a, b], 'element_sources': [ha, hb],
                    'junction': list(jop), 'ending': list(eop), 'shortened': short, 'adjustments': [], 'trace': []}
            add(form, p, info)
            if poly:
                for v in seq.run(form, poly)[:3]:
                    if v['trace']:
                        add(v['form'], p * MORPH_WEIGHT, {**info, 'trace': v['trace']})
        if seq.branch == 'quenya':
            for w, stem, rules in morphophonology.compound_variants(pa, pb)[1:]:
                add(join(w), MORPH_WEIGHT * 0.5 ** (len(rules) - 1) * 0.5,
                    {'joined': a + '+' + b, 'elements': [a, b], 'element_sources': [ha, hb],
                     'junction': [0, 0, ''], 'ending': [0, ''], 'shortened': False,
                     'adjustments': [{'rule': r, **morphophonology.SOURCES[r]} for r in rules],
                     'stem': join(stem) if stem else None, 'trace': []})
    ranked = sorted(scored.values(), key=lambda x: -x[0])
    return [{'form': f, 'score': round(sc, 3), **info} for sc, f, info in ranked]


def predict(lexicon: dict, seq, element_ids: list, era: str = 'late', stage: int = 0,
            last_stage: int | None = None, table: dict | None = None) -> list:
    """Ranked variants [{'form', 'joined', 'junction', 'elements', 'trace'}]."""
    if last_stage is None:
        last_stage = max(l['stage'] for l in seq.langs.values() if l['era'] == era)
    if stage >= last_stage and table is not None:
        return predict_latest(lexicon, seq, table, element_ids, era)
    parts = []
    for k, i in enumerate(element_ids):
        e = lexicon.get(i)
        fs = forms_at(e, seq, era, stage, final=k == len(element_ids) - 1) if e else []
        if not fs:
            return []
        parts.append(fs)
    rules = seq.sequence(era, stage + 1, last_stage)
    variants, seen = [], set()
    joins = []
    for combo in itertools.product(*parts):
        acc = [(combo[0][0], 'full')]
        for form, _ in combo[1:]:
            acc = [(j, max(lab, l2, key=['full', 'elided'].index)) for x, lab in acc for j, l2 in junctions(x, form)]
        for j, label in acc:
            joins.append((j, label, [f for f, _ in combo], [h for _, h in combo]))
    joins.sort(key=lambda x: x[1] != 'full')
    for j, label, forms, how in joins[:MAX_JOINS]:
        for v in seq.run(j, rules):
            key = comparable(v['form'])
            if key in seen:
                continue
            seen.add(key)
            variants.append({'form': v['form'].replace('+', ''), 'joined': j, 'junction': label,
                             'elements': forms, 'element_sources': how, 'trace': v['trace']})
    return variants


def benchmark_cases(data: dict, lexicon_list: list) -> list:
    """Eldamo compounds of two elements with primitive forms and an attested derivation."""
    lexicon = {e['id']: e for e in lexicon_list}
    langs = {l['code']: l for l in data['meta']['languages']}
    ders = {d['id']: d for d in data['derivations']}
    cases = []
    for e in lexicon_list:
        if e.get('neo') or not e.get('derivations') or len(e.get('elements', ())) != 2:
            continue
        ids = [x.get('id') for x in e['elements']]
        if not all(i in lexicon for i in ids):
            continue
        for did in e['derivations']:
            d = ders[did]
            codes = [s['lang'] for s in d['steps'] if s['lang'] in langs]
            if not codes:
                continue
            era = langs[codes[0]]['era']
            if not all(origins(lexicon[i], era) for i in ids):
                continue
            cases.append({'word': e['id'], 'form': e['form'], 'derivation': did, 'era': era,
                          'elements': ids, 'start': d['start'], 'target': d['steps'][-1]['after'],
                          'last_stage': langs[codes[-1]]['stage']})
    return cases


def backtest(data: dict, lexicon_list: list, seq) -> dict:
    lexicon = {e['id']: e for e in lexicon_list}
    results = []
    for c in benchmark_cases(data, lexicon_list):
        vs = predict(lexicon, seq, c['elements'], c['era'], 0, c['last_stage'])
        forms = [comparable(v['form']) for v in vs]
        target = comparable(c['target'])
        joined = {comparable(v['joined']) for v in vs}
        results.append({**c, 'join_ok': comparable(c['start']) in joined,
                        'ok_main': bool(forms) and forms[0] == target, 'ok_any': target in forms,
                        'main': vs[0]['form'] if vs else None, 'variants': len(vs)})
    n = len(results)
    return {'cases': n, 'join_ok': sum(r['join_ok'] for r in results), 'main': sum(r['ok_main'] for r in results),
            'any': sum(r['ok_any'] for r in results), 'results': results}


def latest_backtest(data: dict, lexicon_list: list, seq, limit: int = 8) -> dict:
    """Leave-one-out check of predict_latest on Eldamo's compounds of the
    branch's latest language: the junction table is rebuilt without the
    compound, then the compound is predicted from its elements."""
    lexicon = {e['id']: e for e in lexicon_list}
    rows = junction_table.cases(seq.branch, lexicon_list)
    results = []
    for k, r in enumerate(rows):
        table = junction_table.learn(rows[:k] + rows[k + 1:])
        ids = [x['id'] for x in lexicon[r['word']]['elements']]
        vs = predict_latest(lexicon, seq, table, ids)
        forms = [comparable(v['form']) for v in vs[:limit]]
        results.append({'word': r['word'], 'form': r['form'], 'target': r['c'],
                         'main': vs[0]['form'] if vs else None,
                         'ok_main': bool(forms) and forms[0] == r['c'], 'ok_any': r['c'] in forms})
    return {'cases': len(results), 'main': sum(x['ok_main'] for x in results),
            'any': sum(x['ok_any'] for x in results), 'results': results}
