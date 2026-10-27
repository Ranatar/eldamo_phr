"""Branch data: model + graph + chains, written to branches/<branch>/data/."""
from __future__ import annotations

import json
from collections import Counter

from .graph import GRADES, build_chains, build_edges
from .io import write_json
from .languages import BRANCHES, languages
from .lexicon import build_lexicon, summary as lexicon_summary
from .reconstruct import normalize
from .sequencer import Sequencer, calibrate, primitive_counts, primitive_evidence
from . import affixes
from . import junctions as junction_table
from .model import build
from .source import ROOT, meta

DATA_FILES = ('phonemes', 'rules', 'pairs', 'derivations', 'edges', 'chains', 'lexicon', 'junctions', 'affixes', 'calibration',
              'stages',
              'summary')


def branch_dir(branch: str):
    return ROOT / 'branches' / branch / 'data'


def build_branch(branch: str) -> dict:
    """One branch on its own (the rules of Primitive Elvish calibrated on its derivations
    only; build_all pools both branches)."""
    return finish_branch(prepare_branch(branch))


def prepare_branch(branch: str) -> dict:
    """Everything but the calibration and the stage forms."""
    model = build(branch)
    edges, contextual = build_edges(model)
    chains, chain_summary = build_chains(model, edges)
    lexicon = build_lexicon(branch, model['derivations'])
    junction_rows = junction_table.cases(branch, lexicon)
    affix_rows = affixes.cases(branch, lexicon)
    codes = {l['code'] for l in model['languages']}
    steps = [s for d in model['derivations'] if not d['deleted'] for s in d['steps'] if s['lang'] in codes]
    status = Counter(s['status'].split(':')[0] for s in steps)
    not_checked = ('unknown_rule', 'unmatched_formula', 'identity', 'deleted_rule')
    with_formula = sum(v for k, v in status.items() if k not in not_checked)
    reproduced = status['reproduced'] + status['reproduced_partial']
    summary = {
        'branch': branch,
        'eldamo_version': meta()['eldamo_version'],
        'phonemes': len(model['phonemes']),
        'rules': len(model['rules']),
        'rules_with_order': sum(1 for r in model['rules'] if r['order'] is not None),
        'excluded_rules': model['excluded_rules'],
        'pairs': len(model['pairs']),
        'pair_kinds': dict(sorted(Counter(p['kind'] for p in model['pairs']).items())),
        'pairs_with_examples': sum(1 for p in model['pairs'] if p['examples']),
        'derivations': len(model['derivations']),
        'deleted_derivations': sum(1 for d in model['derivations'] if d['deleted']),
        'branch_steps': len(steps),
        'step_status': dict(sorted(status.items())),
        'reproduction_rate': round(reproduced / with_formula, 4) if with_formula else None,
        'edges': len(edges),
        'conditional_edges': sum(1 for e in edges if e['conditional']),
        'edges_with_examples': sum(1 for e in edges if e['examples']),
        'contextual_pairs': len(contextual),
        'chains': chain_summary,
        'lexicon': lexicon_summary(lexicon),
        'junction_cases': len(junction_rows),
        'affix_cases': len(affix_rows),
        'grade_legend': GRADES,
        'unmatched_formulas': sorted({f"{s['lang']}: {s['from']} > {s['to']}" for d in model['derivations']
                                      for s in d['steps'] if s['status'] == 'unmatched_formula'}),
        'language_names': model['language_names'],       # load_branch restores meta from it
    }
    out = {
        'phonemes': model['phonemes'],
        'rules': model['rules'],
        'pairs': model['pairs'],
        'derivations': model['derivations'],
        'edges': edges,
        'chains': chains,
        'lexicon': lexicon,
        'junctions': {'cases': junction_rows, **junction_table.table_json(junction_rows)},
        'affixes': {'cases': affix_rows},
        'summary': summary,
        'meta': {'title': model['title'], 'path': model['path'], 'languages': model['languages'],
                 'language_names': model['language_names']},
    }
    return out


def finish_branch(out: dict, primitive: dict | None = None) -> dict:
    # which optional rules the sequencer's main reading applies (shared/sequencer.py)
    out['calibration'] = calibrate(out, primitive)
    # forms at the end of every stage, from the derivations the sequencer reproduces
    out['stages'] = normalize(out, Sequencer(out))
    return out


def _prepare(branch: str) -> tuple:
    out = prepare_branch(branch)
    return out, primitive_evidence(out)


def _finish(args: tuple) -> dict:
    return finish_branch(*args)


def write_branch(branch: str, data: dict) -> None:
    target = branch_dir(branch)
    for name in DATA_FILES:
        write_json(target / f'{name}.json', data[name])


def build_all() -> dict:
    """Both branches, side by side in forked processes where there are CPUs for it
    (QUETTAMIN_JOBS limits them); the result is the same either way."""
    import multiprocessing as mp
    import os
    processes = int(os.environ.get('QUETTAMIN_JOBS') or os.cpu_count() or 1)
    names = list(BRANCHES)
    if processes > 1 and 'fork' in mp.get_all_start_methods():
        with mp.get_context('fork').Pool(min(processes, len(names))) as pool:
            prepared = pool.map(_prepare, names)
            # the rules of Primitive Elvish are one language for both branches
            primitive = primitive_counts([ev for _, ev in prepared])
            return dict(zip(names, pool.map(_finish, [(out, primitive) for out, _ in prepared])))
    prepared = [_prepare(b) for b in names]
    primitive = primitive_counts([ev for _, ev in prepared])
    return {b: finish_branch(out, primitive) for b, (out, _) in zip(names, prepared)}


def load_branch(branch: str) -> dict:
    """A branch as build_branch returns it, read from branches/<branch>/data/
    (written by scripts/build.py): seconds instead of a minute."""
    target = branch_dir(branch)
    out = {name: json.loads((target / f'{name}.json').read_text(encoding='utf-8')) for name in DATA_FILES}
    for n in out['stages']:                     # JSON object keys are strings; stages are numbers
        n['forms'] = {int(k): v for k, v in n['forms'].items()}
    out['meta'] = {'title': BRANCHES[branch]['title'], 'path': BRANCHES[branch]['path'],
                   'languages': list(languages(branch).values()),
                   'language_names': out['summary'].get('language_names', {})}
    return out


def load_all() -> dict:
    return {b: load_branch(b) for b in BRANCHES}
