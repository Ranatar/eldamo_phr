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
    base = origins(entry, era)
    if stage == 0:
        return [(f, 'primitive') for f in base]
    rules = seq.sequence(era, 0, stage)
    for f in base:
        for v in seq.run(f, rules)[:2]:
            out.append((v['form'], 'computed'))
    return out


def junctions(a: str, b: str) -> list:
    """(joined, label): the full first element, and without its final vowel."""
    out = [(a + '+' + b, 'full')]
    pa = phonemes(a)
    if len(pa) > 1 and is_vowel(pa[-1]):
        out.append((join(pa[:-1]) + '+' + b, 'elided'))
    return out


def predict(lexicon: dict, seq, element_ids: list, era: str = 'late', stage: int = 0,
            last_stage: int | None = None) -> list:
    """Ranked variants [{'form', 'joined', 'junction', 'elements', 'trace'}]."""
    if last_stage is None:
        last_stage = max(l['stage'] for l in seq.langs.values() if l['era'] == era)
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
