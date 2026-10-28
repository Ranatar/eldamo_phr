"""Run a word form through the sound changes of a branch in chronological order.

Rule order is (language stage, position in the language). The position follows
Eldamo's @order; rules without it (all primitive, ✶ and ᴹ✶) are placed by the
precedences attested in derivations and <before> links (infer_orders).

A rule is applied with all its sub-formulas at once (a sound law); the rule's
unchanged sub-formulas (mb > mb) protect their sites. Rules named as optional
or irregular ("often", "sometimes", "usually", ...) branch: the form with and
the form without the change are both kept. The number of variants is capped.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

from . import interpreter
from .interpreter import Unsupported, comparable
from .languages import STRESS

MONO = re.compile(r'\bmonosyllab', re.I)
POLY = re.compile(r'\bpolysyllab', re.I)
OPTIONAL = re.compile(r'\b(often|sometimes|usually|occasionally|generally|sporadically|frequently|may|might)\b'
                      r'|in long compounds', re.I)
RARE = re.compile(r'(?<!and )\b(sometimes|occasionally|sporadically|may|might)\b', re.I)   # main reading: not applied
MAX_VARIANTS = 24
RUN_CACHE = 50000       # runs kept (Sequencer.run)
CALIBRATION_MIN = 3     # derivations needed to override the reading of a rule's name
POOLED = 'both:'        # calibration key prefix: a primitive rule counted over both branches


@dataclass
class CompiledRule:
    id: str
    name: str
    lang: str
    stage: int
    era: str
    order: float
    optional: bool
    rare: bool
    stress: str | None              # stress model of the rule's stage (shared.stress)
    scope: str | None               # 'mono' / 'poly': rule named for mono- or polysyllables
    rule: object | None             # interpreter.Rule of the changing sub-formulas
    rule_plus: object | None        # the same with sub-formulas that need a morpheme boundary (+)
    protect: object | None          # interpreter.Rule of the unchanged ones
    unsupported: list = field(default_factory=list)
    sources: list = field(default_factory=list)    # input formulas of the changing sub-formulas
    blocked_by: list = field(default_factory=list)  # later rules that take precedence (elsewhere condition)
    formulas: dict = field(default_factory=dict)    # source formulas, for the browser engine (app/wordform.js)


def _compile(rule: dict, pairs: dict, langs: dict, order: float) -> CompiledRule:
    changing, unchanged, bad, sources = [], [], [], []
    formulas = {'changing': [], 'protect': []}
    for pid in rule['pairs']:
        p = pairs[pid]
        if not p.get('in_branch', True):
            continue
        try:
            compiled = interpreter.compile_rule(p['from'] or '', p['to'])
        except Unsupported as exc:
            bad.append(f"{p['from']} > {p['to']}: {exc}")
            continue
        if p['kind'] == 'identity':
            unchanged.append(compiled)
            formulas['protect'].append([p['from'] or '', p['to']])
        else:
            changing.append((compiled, '+' in (p['from'] or '')))
            sources.append(p['from'] or '')
            formulas['changing'].append([p['from'] or '', p['to'], '+' in (p['from'] or '')])
    L = langs[rule['lang']]
    return CompiledRule(
        id=rule['id'], name=rule['name'], lang=rule['lang'], stage=L['stage'], era=L['era'], order=order,
        stress=STRESS.get(rule['lang']),
        scope='mono' if MONO.search(rule['name']) else 'poly' if POLY.search(rule['name']) else None,
        optional=bool(OPTIONAL.search(rule['name'])),
        rare=bool(RARE.search(rule['name'])),
        rule=interpreter.combine([r for r, plus in changing if not plus]) if any(not p for _, p in changing) else None,
        rule_plus=interpreter.combine([r for r, _ in changing]) if any(p for _, p in changing) else None,
        protect=interpreter.combine(unchanged) if unchanged else None,
        unsupported=bad, sources=sources, formulas=formulas)


def infer_orders(rules: list, pairs: dict, derivations: list) -> dict:
    """Order key for every rule within its language.

    Rules with @order keep it. The others (all primitive in 0.8.13) are placed
    by a topological sort of the precedences Eldamo attests: the order of steps
    inside derivations, <before> links and the chain of known orders. Where the
    evidence conflicts, the precedence attested more often wins.
    """
    by_lang = defaultdict(list)
    for r in rules:
        by_lang[r['lang']].append(r)
    rule_lang = {r['id']: r['lang'] for r in rules}
    votes = defaultdict(int)          # (a, b) -> how often a is attested before b
    for d in derivations:
        if d['deleted']:
            continue
        seq = [pairs[s['pair']]['rule'] for s in d['steps'] if s['pair'] in pairs]
        for i, a in enumerate(seq):
            for b in seq[i + 1:]:
                if a != b and rule_lang[a] == rule_lang[b]:
                    votes[(a, b)] += 1
    for r in rules:
        for x in r['before']:
            if x['rule'] in rule_lang and rule_lang[x['rule']] == r['lang']:
                votes[(r['id'], x['rule'])] += 100
    out = {}
    for lang, rs in by_lang.items():
        ids = [r['id'] for r in rs]
        known = sorted((r['order'], r['id']) for r in rs if r['order'] is not None)
        for (o1, a), (o2, b) in zip(known, known[1:]):
            if o1 < o2:
                votes[(a, b)] += 1000
        edges = defaultdict(set)
        for a in ids:
            for b in ids:
                if a != b and votes.get((a, b), 0) > votes.get((b, a), 0):
                    edges[a].add(b)
        indeg = {i: 0 for i in ids}
        for a in ids:
            for b in edges[a]:
                indeg[b] += 1
        order_of = {r['id']: r['order'] for r in rs}
        name_of = {r['id']: r['name'] for r in rs}
        prio = lambda i: (order_of[i] is None, order_of[i] or 0, name_of[i], i)
        remaining, position = set(ids), 0
        while remaining:
            ready = sorted((i for i in remaining if indeg[i] == 0), key=prio)
            if not ready:   # a cycle: release the rule with the fewest incoming precedences
                ready = [min(remaining, key=lambda i: (indeg[i], prio(i)))]
            i = ready[0]
            remaining.discard(i)
            out[i] = position
            position += 1
            for b in edges[i]:
                if b in remaining:
                    indeg[b] -= 1
    return out


class Sequencer:
    def __init__(self, data: dict):
        self.branch = data['summary']['branch'] if 'summary' in data else None
        self.derivations = data['derivations']
        self._backform_tables = {}
        self.langs = {l['code']: l for l in data['meta']['languages']}
        pairs = {p['id']: p for p in data['pairs']}
        position = infer_orders(data['rules'], pairs, data['derivations'])
        self.rules = [_compile(r, pairs, self.langs, position[r['id']]) for r in data['rules']]
        self.unplaced = []
        self.rules.sort(key=lambda c: (c.era, c.stage, c.order, c.id))
        self.by_id = {c.id: c for c in self.rules}
        self._elsewhere()
        # optional rules: whether the main reading applies them, from how often
        # the replayed derivations of Eldamo needed them (calibrate)
        cal = data.get('calibration') or {}
        for rid, (applied, skipped) in cal.items():
            c = self.by_id.get(rid)
            if c is None or rid.startswith(POOLED):
                continue
            if c.optional:
                if applied + skipped >= CALIBRATION_MIN:
                    c.rare = skipped > applied
            elif c.stage == 0:
                # a primitive rule many written primitive forms already went through
                # (_primitive_calibration): optional when the derivations of both branches
                # skip it more often than they name it, and the main reading follows this
                # branch's own derivations (S. ✶kʰjarja: main *harj, variant hair)
                pa, ps = cal.get(POOLED + rid, (applied, skipped))
                if pa + ps >= CALIBRATION_MIN and ps > pa:
                    c.optional = True
                    c.rare = skipped > applied if applied + skipped >= CALIBRATION_MIN else True

    def _elsewhere(self):
        """Elsewhere condition: a general sub-formula (sr > ss anywhere) does not
        take the sites of a later rule of the same language that states the same
        input for a specific position (sr- > r̥-, "initial [s] unvoiced"). Such
        sites are added to the general rule's protected patterns."""
        by_lang = {}
        for c in self.rules:
            by_lang.setdefault((c.era, c.lang), []).append(c)
        for rs in by_lang.values():
            for k, a in enumerate(rs):
                general = {interpreter.position_of(x)[0] for x in a.sources
                           if interpreter.position_of(x)[1] == 'any'}
                if not general:
                    continue
                extra = []
                for b in rs[k + 1:]:
                    hits = [x for x in b.sources
                            if interpreter.position_of(x)[1] != 'any' and interpreter.position_of(x)[0] in general]
                    for x in hits:
                        try:
                            extra.append(interpreter.compile_rule(x, x))
                            a.formulas['protect'].append([x, x])
                        except Unsupported:
                            continue
                    if hits:
                        a.blocked_by.append(b.id)
                if extra:
                    a.protect = interpreter.combine(([a.protect] if a.protect else []) + extra)

    def export(self) -> list:
        """Rules in sequence order with their formulas, for app/wordform.js."""
        out = []
        for c in self.rules:
            ch = c.formulas['changing']
            out.append({'id': c.id, 'name': c.name, 'lang': c.lang, 'stage': c.stage, 'era': c.era,
                        'optional': c.optional, 'rare': c.rare, 'stress': c.stress, 'scope': c.scope,
                        'alts': [[f, t] for f, t, plus in ch if not plus],
                        'all': [[f, t] for f, t, _ in ch] if any(plus for _, _, plus in ch) else [],
                        'protect': c.formulas['protect']})
        return out

    def backform_table(self, final_code: str) -> dict:
        if final_code not in self._backform_tables:
            from .backform import learn
            self._backform_tables[final_code] = learn(self.derivations, self.langs, final_code)
        return self._backform_tables[final_code]

    def sequence(self, era: str, first_stage: int, last_stage: int, after_order: float | None = None):
        """Rules of one era from first_stage to last_stage, optionally only those
        after a given order within the first stage."""
        out = []
        for c in self.rules:
            if c.era != era or not (first_stage <= c.stage <= last_stage):
                continue
            if after_order is not None and c.stage == first_stage and c.order <= after_order:
                continue
            out.append(c)
        return out

    @staticmethod
    def _apply(c: CompiledRule, rule, form: str, sounds: set | None = None) -> list:
        if rule is None:
            return []
        if sounds is not None and not interpreter.may_apply(rule, sounds):
            return []
        try:
            return interpreter.apply_rule(rule, form, protect=c.protect, stress_mode=c.stress, scope=c.scope)['ordered']
        except Unsupported:
            return []

    def run(self, form: str, rules: list, branch_optional: bool = True) -> list:
        """Apply rules in order. Returns variants: [{'form', 'trace'}], the first
        being the main reading: optional rules applied, except those named as
        occasional ("sometimes", "occasionally", "may"), which are not. The same form
        through the same rules is run once (the backward search and the stages of a
        panorama try the same candidates again and again)."""
        key = (form, tuple(c.id for c in rules), branch_optional)
        cache = self.__dict__.setdefault('_runs', {})
        hit = cache.get(key)
        if hit is None:
            if len(cache) >= RUN_CACHE:
                cache.clear()
            hit = cache[key] = self._run(form, rules, branch_optional)
        return [{'form': v['form'], 'trace': list(v['trace'])} for v in hit]

    def _run(self, form: str, rules: list, branch_optional: bool) -> list:
        variants = [{'form': form, 'trace': []}]
        sound_cache = {}
        for c in rules:
            if c.rule is None and c.rule_plus is None:
                continue
            nxt = []
            for v in variants:
                marked = '+' in v['form']
                # Sub-formulas with + need a morpheme boundary. In a form that
                # marks its boundaries they apply only there; in an unmarked
                # form the boundary is unknown, so their result is kept as an
                # extra variant, not as the main reading.
                main_rule = c.rule_plus if marked and c.rule_plus is not None else c.rule
                sounds = sound_cache.get(v['form'])
                if sounds is None:
                    sounds = sound_cache[v['form']] = interpreter.word_sounds(v['form'])
                outs = self._apply(c, main_rule, v['form'], sounds)
                extra = []
                if not marked and c.rule_plus is not None:
                    extra = [o for o in self._apply(c, c.rule_plus, v['form'], sounds) if o not in outs]
                if not outs:
                    nxt.append(v)
                keep = outs and c.optional and branch_optional
                if keep and c.rare:
                    nxt.append({'form': v['form'], 'trace': v['trace'] + [(c.id, v['form'], None)]})
                for o in outs:
                    nxt.append({'form': o, 'trace': v['trace'] + [(c.id, v['form'], o)]})
                if keep and not c.rare:
                    nxt.append({'form': v['form'], 'trace': v['trace'] + [(c.id, v['form'], None)]})
                for o in extra:
                    nxt.append({'form': o, 'trace': v['trace'] + [(c.id, v['form'], o)]})
            seen, variants = set(), []
            for v in nxt:
                key = comparable(v['form'])
                if key not in seen:
                    seen.add(key)
                    variants.append(v)
            variants = variants[:MAX_VARIANTS]
        return variants


def _replays(data: dict, seq: Sequencer):
    """(derivation, variants) for every replayable derivation (see backtest)."""
    langs = seq.langs
    pair_rule = {p['id']: p['rule'] for p in data['pairs']}
    for d in data['derivations']:
        if d['deleted'] or not d['steps']:
            continue
        codes = [s['lang'] for s in d['steps']]
        if any(c not in langs for c in codes):
            continue
        era = langs[codes[0]]['era']
        if any(langs[c]['era'] != era for c in codes):
            continue
        first, last = langs[codes[0]]['stage'], langs[codes[-1]]['stage']
        rules = seq.sequence(era, first, last)
        # stop after the rule of the last attested step: the derivation may end
        # at an intermediate form, later rules of that language belong to later forms
        last_pair = next((s['pair'] for s in reversed(d['steps']) if s['pair'] in pair_rule), None)
        if last_pair:
            bound = seq.by_id[pair_rule[last_pair]]
            rules = [c for c in rules if (c.stage, c.order) <= (bound.stage, bound.order)]
        yield d, seq.run(d['start'], rules)


def calibrate(data: dict, primitive: dict | None = None) -> dict:
    """{rule id: [applied, skipped]} for optional rules: in the first variant
    that reproduces an attested derivation, was the rule applied or not. The
    rules of Primitive Elvish are counted by _primitive_calibration over this
    branch and, given `primitive` (primitive_counts), over both branches as well
    (keys 'both:<rule id>')."""
    seq = Sequencer({**data, 'calibration': None})
    out = {}
    for d, variants in _replays(data, seq):
        target = comparable(d['steps'][-1]['after'])
        hit = next((v for v in variants if comparable(v['form']) == target), None)
        if hit is None:
            continue
        for rid, _, after in hit['trace']:
            if seq.by_id[rid].optional:
                out.setdefault(rid, [0, 0])[0 if after is not None else 1] += 1
    out.update(_primitive_calibration(data, seq))
    for rid, counts in (primitive or {}).items():
        out[POOLED + rid] = counts
    return dict(sorted(out.items()))


def primitive_evidence(data: dict) -> dict:
    """{rule id: [ids of derivations that name it, ids of those that skip it]} for the
    rules of Primitive Elvish (_primitive_calibration). The primitive language is the
    same for both branches, so build_all pools the evidence of both (primitive_counts):
    S. ✶kʰjarja > hair, not *harj by 'short final [e], [a], [o] vanished', which the
    Sindarin derivations alone, mostly starting in Old Sindarin, leave obligatory."""
    seq = Sequencer({**data, 'calibration': None})
    return _primitive_calibration(data, seq, ids=True)


def primitive_counts(evidences: list) -> dict:
    """{rule id: [applied, skipped]} from the evidence of several branches; a derivation
    both branches hold (of a Primitive Elvish word) counts once."""
    pooled = {}
    for ev in evidences:
        for rid, (applied, skipped) in ev.items():
            a, k = pooled.setdefault(rid, [set(), set()])
            a.update(applied)
            k.update(skipped)
    return {rid: [len(a), len(k)] for rid, (a, k) in pooled.items()}


def _primitive_calibration(data: dict, seq: 'Sequencer', ids: bool = False) -> dict:
    """{rule id: [applied, skipped]} for the rules of Primitive Elvish (stage 0)
    that are not named as optional. Eldamo writes most primitive forms after
    these rules (✶delya -> AQ. lelja, not ✶delya -> delj by 'short final [e],
    [a], [o] vanished'), and only some derivations start before them (✶ambara ->
    ambar). A rule is counted as applied when a derivation names it, as skipped
    when a derivation of the same era does not name it although it would change
    the form the derivation starts from."""
    pair_rule = {p['id']: p['rule'] for p in data['pairs']}
    rules = [c for c in seq.rules if c.stage == 0 and not c.optional and c.rule is not None]
    out = {}
    for d in data['derivations']:
        if d['deleted'] or not d['steps']:
            continue
        first = seq.langs.get(d['steps'][0]['lang'])
        if first is None:
            continue
        # a start form written at a later stage counts too: had the primitive rule acted, the
        # later form would show it (S. dail < ✶delja: the -a is still there in Sindarin)
        named = {pair_rule.get(s['pair']) for s in d['steps']}
        start = comparable(d['start'])
        sounds = interpreter.word_sounds(d['start'])
        for c in rules:
            if c.era != first['era']:
                continue
            # the same derivation of the XML has another id in each branch's data
            key = (d.get('word'), d.get('source'), d['start'], tuple(x['after'] for x in d['steps']))
            if c.id in named:
                out.setdefault(c.id, [set(), set()])[0].add(key)
                continue
            changed = Sequencer._apply(c, c.rule, d['start'], sounds)
            if changed and comparable(changed[0]) != start:
                out.setdefault(c.id, [set(), set()])[1].add(key)
    if ids:
        return out
    return {rid: [len(a), len(k)] for rid, (a, k) in out.items()}


def backtest(data: dict, seq: Sequencer | None = None) -> dict:
    """Replay every attested derivation of the branch from its start form."""
    seq = seq or Sequencer(data)
    results = []
    for d, variants in _replays(data, seq):
        target = comparable(d['steps'][-1]['after'])
        forms = [comparable(v['form']) for v in variants]
        main = forms[0] == target
        anyv = target in forms
        diverge = None
        if not main:
            # first attested intermediate form the main reading never passes through
            passed = {comparable(d['start'])} | {comparable(t[2]) for t in variants[0]['trace'] if t[2]}
            for s in d['steps']:
                if comparable(s['after']) not in passed:
                    diverge = {'pair': s['pair'], 'expected': s['after']}
                    break
        results.append({'derivation': d['id'], 'word': d['word_form'], 'start': d['start'],
                        'target': d['steps'][-1]['after'], 'main': variants[0]['form'],
                        'variants': len(variants), 'ok_main': main, 'ok_any': anyv, 'diverge': diverge,
                        'steps': len(d['steps'])})
    n = len(results)
    return {
        'derivations': n,
        'main': sum(r['ok_main'] for r in results),
        'any': sum(r['ok_any'] for r in results),
        'results': results,
        'unplaced_rules': seq.unplaced,
    }
