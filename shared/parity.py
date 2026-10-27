"""Test vectors: the Python engine's answers that app/wordform.js must repeat.

tests/test_browser.py loads the atlas, passes these vectors to the page and
compares; scripts can also feed them to Node (tests/parity.js).
"""
from __future__ import annotations

import random

from . import affixes, backform, compound, junctions
from .interpreter import Unsupported, apply_rule, comparable, compile_rule, phonemes
from .orthography import to_phonetic
from .sequencer import Sequencer
from .stress import stressed


def vectors(branches: dict, size: int = 1, recon_every: int = 1) -> dict:
    """size scales the number of cases (1: a quick set for the browser test); of the
    reconstruction calls only every recon_every-th is made (each takes a while)."""
    rnd = random.Random(13)
    out = {}
    for b, data in branches.items():
        seq = Sequencer(data)
        lexicon = {e['id']: e for e in data['lexicon']}
        V = {'apply': [], 'comparable': [], 'stress': [], 'run': [], 'phonetic': [], 'junction': [],
             'latest': [], 'early': [], 'backform': [], 'allomorphs': [], 'affixed': []}
        steps = [(s['from'] or '', s['to'], s['before'] or '') for d in data['derivations'] for s in d['steps']
                 if s['to'] and s['to'] != '?' and s['before']]
        for f, t, before in rnd.sample(steps, min(len(steps), 400 * size)):
            try:
                res = apply_rule(compile_rule(f, t), before)['ordered']
            except Unsupported:
                res = None
            V['apply'].append([f, t, before, res])
        forms = [d['start'] for d in data['derivations'] if d['start']]
        for f in rnd.sample(forms, min(len(forms), 200 * size)):
            V['comparable'].append([f, comparable(f)])
            for mode in ('initial', 'latin', 'latin-sindarin'):
                V['stress'].append([f, mode, sorted(stressed(phonemes(f.strip('-')), mode))])
        langs = seq.langs
        ders = [d for d in data['derivations'] if d['steps'] and all(s['lang'] in langs for s in d['steps'])]
        for d in rnd.sample(ders, min(len(ders), 40 * size)):
            era = langs[d['steps'][0]['lang']]['era']
            first, last = langs[d['steps'][0]['lang']]['stage'], langs[d['steps'][-1]['lang']]['stage']
            vs = seq.run(d['start'], seq.sequence(era, first, last))
            V['run'].append([d['start'], era, first, last, [v['form'] for v in vs],
                             [[t[0], t[2]] for t in vs[0]['trace']]])
        words = [e['form'] for e in data['lexicon'] if e['lang'] in ('q', 's', 'mq', 'n')]
        for w in rnd.sample(words, min(len(words), 300 * size)):
            V['phonetic'].append([w, to_phonetic(w, b)])
        rows = data['junctions']['cases']
        table = junctions.learn(rows)
        for r in rnd.sample(rows, min(len(rows), 60 * size)):
            a, bb = phonemes(r['a']), phonemes(r['b'])
            V['junction'].append([r['a'], r['b'], [[f, p, list(j), list(e), s] for f, p, j, e, s in
                                                   junctions.predict(table, a, bb, limit=10)]])
        for r in rnd.sample(rows, min(len(rows), 25 * size)):
            ids = [x['id'] for x in lexicon[r['word']]['elements']]
            vs = compound.predict(lexicon, seq, ids, 'late', 9, table=table)
            V['latest'].append([ids, [[v['form'], v['score']] for v in vs[:10]]])
        cases = compound.benchmark_cases(data, data['lexicon'])
        for c in rnd.sample(cases, min(len(cases), 8 * size)):
            vs = compound.predict(lexicon, seq, c['elements'], c['era'], 0, c['last_stage'])
            V['early'].append([c['elements'], c['era'], 0, c['last_stage'], [v['form'] for v in vs[:10]]])
        final = max((l for l in langs.values() if l['era'] == 'late'), key=lambda l: l['stage'])
        for d in rnd.sample([d for d in ders if d['steps'][-1]['lang'] == final['code']], min(5 * size, 40)):
            res = backform.backform(seq, seq.backform_table(final['code']), d['steps'][-1]['after'], 'late', final['stage'])
            V['backform'].append([d['steps'][-1]['after'], final['stage'], [r['primitive'] for r in res]])
        affix_model = affixes.learn(data['affixes']['cases'])
        affix_entries = [e for e in data['lexicon'] if affixes.kind(e)]
        for e in rnd.sample(affix_entries, min(len(affix_entries), 40 * size)):
            V['allomorphs'].append([e['id'], affixes.allomorphs(e, b)])
        arows = data['affixes']['cases']
        for r in rnd.sample(arows, min(len(arows), 25 * size)):
            ids = [r['base'], r['affix']] if r['kind'] == 'suffix' else [r['affix'], r['base']]
            if rnd.random() < 0.3:
                ids = ids[::-1]                 # either order of picking
            vs = compound.predict(lexicon, seq, ids, 'late', 9, table=table, affix_model=affix_model)
            V['affixed'].append([ids, [[v['form'], v['score']] for v in vs[:10]]])
        out[b] = V
    out['__recon__'] = recon_vectors(branches, size, recon_every)
    return out


def recon_vectors(branches: dict, size: int = 1, every: int = 1) -> list:
    """Reconstruction calls of every route, with the Python answers; every: only the
    calls 0, every, 2 * every... are made and returned (the cases are drawn the same)."""
    from .reconstruct import Context, reconstruct
    rnd = random.Random(17)
    ctx = Context(branches)
    cases = []
    n_case = 0
    for b in branches:
        lex = ctx.lexicon[b]
        langs = ctx.langs(b)
        words = [e for e in lex.values() if e['speech'] != 'root' and not e.get('neo') and e['lang'] in langs]
        for e in rnd.sample(words, min(len(words), 6 * size)):
            l = langs[e['lang']]
            src = (b, l['era'], l['stage'])
            for dst in ((b, l['era'], 0), (b, 'late', 2 if b == 'quenya' else 3),
                        ('sindarin' if b == 'quenya' else 'quenya', l['era'], max(x['stage'] for x in ctx.langs(
                            'sindarin' if b == 'quenya' else 'quenya').values() if x['era'] == l['era']))):
                n_case += 1
                if (n_case - 1) % every:
                    continue
                vs = reconstruct(ctx, src, dst, word=e['id'])
                cases.append([list(src), list(dst), {'word': e['id']}, [[v['form'], v['score'], v['marks']] for v in vs]])
        norm = [n for n in ctx.normal[b] if n['era'] == 'late']
        last = ctx.last_stage(b, 'late')
        for n in rnd.sample([n for n in norm if last in n['forms']], 3 * size):
            for t in range(last):
                n_case += 1
                if (n_case - 1) % every:
                    continue
                vs = reconstruct(ctx, (b, 'late', last), (b, 'late', t), form=n['forms'][last])
                cases.append([[b, 'late', last], [b, 'late', t], {'form': n['forms'][last]},
                              [[v['form'], v['score'], v['marks']] for v in vs]])
    return cases
