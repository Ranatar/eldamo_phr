"""Branch data: model + graph + chains, written to branches/<branch>/data/."""
from __future__ import annotations

from collections import Counter

from .graph import GRADES, build_chains, build_edges
from .io import write_json
from .languages import BRANCHES
from .lexicon import build_lexicon, summary as lexicon_summary
from .model import build
from .source import ROOT, meta

DATA_FILES = ('phonemes', 'rules', 'pairs', 'derivations', 'edges', 'chains', 'lexicon', 'summary')


def branch_dir(branch: str):
    return ROOT / 'branches' / branch / 'data'


def build_branch(branch: str) -> dict:
    model = build(branch)
    edges, contextual = build_edges(model)
    chains, chain_summary = build_chains(model, edges)
    lexicon = build_lexicon(branch, model['derivations'])
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
        'grade_legend': GRADES,
        'unmatched_formulas': sorted({f"{s['lang']}: {s['from']} > {s['to']}" for d in model['derivations']
                                      for s in d['steps'] if s['status'] == 'unmatched_formula'}),
    }
    return {
        'phonemes': model['phonemes'],
        'rules': model['rules'],
        'pairs': model['pairs'],
        'derivations': model['derivations'],
        'edges': edges,
        'chains': chains,
        'lexicon': lexicon,
        'summary': summary,
        'meta': {'title': model['title'], 'path': model['path'], 'languages': model['languages'],
                 'language_names': model['language_names']},
    }


def write_branch(branch: str, data: dict) -> None:
    target = branch_dir(branch)
    for name in DATA_FILES:
        write_json(target / f'{name}.json', data[name])


def build_all() -> dict:
    return {b: build_branch(b) for b in BRANCHES}
