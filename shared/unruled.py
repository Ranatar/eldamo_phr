"""Steps of Eldamo's derivations that name no rule ('?').

Strack marks a step with '?' when no known sound law explains it: Q. pupso
'fly' < ✶buzbō > buspō > puspō (b > p?) > pupso. For every such step the laws
of that language are tried on the form before it:

* rule   -- one rule of the language gives the form (Eldamo just did not name it);
* laws   -- the language's rules in their order give it (several rules at once);
* none   -- no law gives it: the form departs from the laws (pupso, not *vupso).

reports/sequencer.md gives the counts, reports/sequencer.json every step.
"""
from __future__ import annotations

from collections import Counter

from .interpreter import comparable
from .sequencer import Sequencer


def unruled_steps(branches: dict) -> list:
    out, seen = [], set()
    for b, data in branches.items():
        seq = Sequencer(data)
        by_lang = {}
        for c in seq.rules:
            by_lang.setdefault(c.lang, []).append(c)
        for d in data['derivations']:
            if d['deleted'] or d['id'] in seen:
                continue
            prev = d['start']
            for k, st in enumerate(d['steps']):
                if st['status'].startswith('unknown_rule') and st['lang'] in by_lang:
                    seen.add(d['id'])
                    out.append(_classify(seq, by_lang[st['lang']], d, k, prev, st))
                prev = st['after']
    return out


def _classify(seq: Sequencer, rules: list, d: dict, k: int, before: str, st: dict) -> dict:
    target = comparable(st['after'])
    rec = {'derivation': d['id'], 'word': d['word'], 'word_form': d['word_form'], 'lang': st['lang'],
           'before': before, 'after': st['after'], 'kind': 'none', 'rule': None, 'laws': None}
    for c in rules:
        rule = c.rule or c.rule_plus
        if rule is not None and any(comparable(o) == target for o in seq._apply(c, rule, before)):
            rec.update(kind='rule', rule=c.name)
            return rec
    variants = seq.run(before, rules)
    rec['laws'] = variants[0]['form']
    if any(comparable(v['form']) == target for v in variants):
        rec['kind'] = 'laws'
    return rec


def summary(steps: list) -> dict:
    by = Counter((s['lang'], s['kind']) for s in steps)
    langs = sorted({s['lang'] for s in steps})
    return {lang: {k: by[(lang, k)] for k in ('rule', 'laws', 'none')} for lang in langs}
