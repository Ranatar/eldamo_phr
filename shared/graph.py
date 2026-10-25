"""Sound graph, structural chains and their grading.

Edges are literal rule pairs (a > b, including losses a > ø). Pairs with
classes, sets or context stay out of the graph and are listed as contextual.
An edge keeps the general formula of its rule page: an edge taken from a
rule whose general formula is contextual, or whose page lists unchanged
(identity) pairs as exceptions, is marked conditional.

Chains are paths of 2..MAX_STEPS edges in one era. Consecutive steps must be
in chronological order: a later language stage, or within one language an
Eldamo @order / <before> relation saying the first rule precedes the second.
Paths that Eldamo's chronology contradicts are not chains; they are counted.

Grades
  A  attested: the steps occur in this order in one attested derivation
  B  every step has attested examples the formula reproduces, and every
     transition is chronologically confirmed (by stage or by Eldamo's order)
  C  every step has reproduced examples; some transition's order is unknown
  D  some step has no reproduced attested example

Only steps that the formula reproduces and that change the form count as
evidence (shared.graph.witness_steps).
"""
from __future__ import annotations

from collections import defaultdict

from .formula import NULL, stressed
from .interpreter import Unsupported, parse_pattern, split_top

MAX_STEPS = 3
GRADES = {
    'A': 'засвидетельствована в одной деривации',
    'B': 'шаги засвидетельствованы, порядок подтверждён',
    'C': 'шаги засвидетельствованы, порядок не установлен',
    'D': 'есть шаг без засвидетельствованных примеров',
}


def general_is_contextual(rule: dict) -> bool:
    """True when the rule's general formula conditions the change on classes
    (V, C, X, S), inserted/null slots or stress; sets such as {bdg} only enumerate sounds."""
    f = rule.get('formula')
    if not f:
        return False
    if stressed(f['from']) or stressed(f['to']):
        return True
    try:
        for side in (f['from'], f['to']):
            for alt in split_top(side):
                if any(t.kind in ('class', 'null') for t in parse_pattern(alt).tokens):
                    return True
    except Unsupported:
        return True
    return False


def build_edges(model: dict) -> tuple[list, list]:
    rules = {r['id']: r for r in model['rules']}
    groups = defaultdict(list)
    contextual = []
    for p in model['pairs']:
        if not p['in_branch']:
            contextual.append({'pair': p['id'], 'rule': p['rule'], 'reason': 'language outside the branch'})
        elif p['kind'] in ('literal', 'loss'):
            groups[(p['era'], p['stage'], p['a'], p['b'], p['position'])].append(p)
        else:
            reason = {'identity': 'unchanged (exception of the rule)', 'insertion': 'insertion without context',
                      'contextual': 'pattern with classes, sets or context'}[p['kind']]
            contextual.append({'pair': p['id'], 'rule': p['rule'], 'reason': reason})
    edges = []
    for key in sorted(groups, key=lambda k: (k[0], k[1], k[2], k[3], k[4])):
        era, stage, a, b, position = key
        ps = groups[key]
        uniq, seen = [], set()
        for p in ps:
            if p['rule'] not in seen:
                seen.add(p['rule'])
                uniq.append(rules[p['rule']])
        context = sorted({f"{r['formula']['from']} > {r['formula']['to']}" for r in uniq if general_is_contextual(r)}
                         | {f"{p['from']} > {p['to']} (ударение)" for p in ps if p['stress']})
        exceptions = sorted({x for r in uniq for x in r['exceptions']})
        edges.append({
            'id': f'E{len(edges) + 1}',
            'era': era, 'stage': stage, 'lang': ps[0]['lang'], 'marker': ps[0]['marker'],
            'a': a, 'b': b, 'position': position,
            'pairs': [p['id'] for p in ps],
            'rules': [r['id'] for r in uniq],
            'names': [r['name'] for r in uniq],
            'orders': sorted({r['order'] for r in uniq if r['order'] is not None}),
            'conditional': bool(context or exceptions),
            'context': context,
            'exceptions': exceptions,
            'examples': sum(p['examples'] for p in ps),
            'reproduced': sum(p['reproduced'] + p['partial'] for p in ps),
        })
    return edges, contextual


def witness_steps(derivations: list) -> dict:
    """pair id -> [(derivation index, step index)] for steps that bear witness:
    not rejected by Tolkien, reproduced by the formula, and actually changing the form."""
    occurrences = defaultdict(list)
    for di, d in enumerate(derivations):
        if d['deleted']:
            continue
        for si, s in enumerate(d['steps']):
            if s['pair'] and s['status'] in ('reproduced', 'reproduced_partial') and s['before'] != s['after']:
                occurrences[s['pair']].append((di, si))
    return occurrences


class Chronology:
    def __init__(self, model):
        self.rules = {r['id']: r for r in model['rules']}
        self.before = {(r['id'], b['rule']) for r in model['rules'] for b in r['before'] if b['rule']}

    def relation(self, r1: str, r2: str) -> str:
        """'<' r1 precedes r2, '>' follows, '=' same rule, '?' unknown."""
        if r1 == r2:
            return '='
        if (r1, r2) in self.before:
            return '<'
        if (r2, r1) in self.before:
            return '>'
        o1, o2 = self.rules[r1]['order'], self.rules[r2]['order']
        if o1 is not None and o2 is not None and o1 != o2:
            return '<' if o1 < o2 else '>'
        return '?'

    def transition(self, e1: dict, e2: dict) -> str:
        """'stage' | 'ordered' | 'unknown' | 'contradicted'."""
        if e2['stage'] > e1['stage']:
            return 'stage'
        if e2['stage'] < e1['stage']:
            return 'contradicted'
        rel = {self.relation(r1, r2) for r1 in e1['rules'] for r2 in e2['rules']}
        if '<' in rel:
            return 'ordered'
        if '?' in rel:
            return 'unknown'
        return 'contradicted'  # only '>' or the same rule (simultaneous pairs do not feed)


def _position_ok(current: str, e: dict) -> tuple[bool, str]:
    if current == 'any' or e['position'] == 'any':
        return True, e['position'] if current == 'any' else current
    return current == e['position'], current


def build_chains(model: dict, edges: list) -> tuple[list, dict]:
    chrono = Chronology(model)
    out = defaultdict(list)
    by_a = defaultdict(list)
    for e in edges:
        by_a[(e['era'], e['a'])].append(e)
    rejected = 0

    def extend(path, transitions, position):
        nonlocal rejected
        last = path[-1]
        if len(path) >= 2:
            states = (path[0]['a'],) + tuple(e['b'] for e in path)
            out[(last['era'], states)].append((list(path), list(transitions)))
        if len(path) == MAX_STEPS or last['b'] == NULL:
            return
        visited = {path[0]['a']} | {e['b'] for e in path}
        for e in by_a[(last['era'], last['b'])]:
            if e['b'] in visited:
                continue
            ok, pos = _position_ok(position, e)
            if not ok:
                continue
            t = chrono.transition(last, e)
            if t == 'contradicted':
                rejected += 1
                continue
            extend(path + [e], transitions + [t], pos)

    for e in edges:
        extend([e], [], e['position'])

    occurrences = witness_steps(model['derivations'])

    def attesting(path):
        found = None
        for e in path:
            pos = defaultdict(list)
            for p in e['pairs']:
                for di, si in occurrences.get(p, ()):
                    pos[di].append(si)
            if found is None:
                found = {di: min(v) for di, v in pos.items()}
            else:
                nxt = {}
                for di, prev in found.items():
                    later = [si for si in pos.get(di, ()) if si > prev]
                    if later:
                        nxt[di] = min(later)
                found = nxt
            if not found:
                return []
        return sorted(found)

    chains = []
    derivs = model['derivations']
    for (era, states), variants in sorted(out.items(), key=lambda kv: (kv[0][0], len(kv[0][1]), kv[0][1])):
        best = None
        for path, transitions in variants:
            att = attesting(path)
            if att:
                grade = 'A'
            elif any(e['reproduced'] == 0 for e in path):
                grade = 'D'
            elif all(t in ('stage', 'ordered') for t in transitions):
                grade = 'B'
            else:
                grade = 'C'
            if best is None or grade < best[0]:
                best = (grade, path, transitions, att)
        grade, path, transitions, att = best
        chains.append({
            'id': f"{era}:{'>'.join(states)}",
            'era': era,
            'states': list(states),
            'grade': grade,
            'steps': [e['id'] for e in path],
            'transitions': transitions,
            'variants': len(variants),
            'markers': [e['marker'] for e in path],
            'attested_in': [derivs[di]['id'] for di in att[:12]],
            'attested_count': len(att),
        })
    chains.sort(key=lambda c: (c['era'], c['grade'], -c['attested_count'], len(c['states']), c['states']))
    summary = {'chains': len(chains), 'rejected_by_chronology': rejected,
               'grades': {g: sum(1 for c in chains if c['grade'] == g) for g in GRADES}}
    return chains, summary
