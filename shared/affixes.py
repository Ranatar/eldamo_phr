"""Suffixes and prefixes: deriving a word from a base at the latest stage.

Eldamo marks affixes by part of speech (speech="suf" / "pref"): Q. -itë,
-mo, -ië, ú-, o-; S. -(r)on, -ui, -eg, ar(a)- ... Most affix pages have no
description of how the affix attaches, but the derived words that list the
affix among their <element>s show it (1800 such uses in Quenya, 590 in
Sindarin). This module learns from them:

* allomorphs  -- an affix written with optional parts, -(n)dil, al(a)-,
                 -(r)on, has several forms; which one is used after a base
                 ending (for a suffix) or before a base starting (for a prefix)
                 in a vowel or a consonant is counted per affix;
* junction    -- the changes where base and affix meet and at the end of the
                 word, as in shared/junctions.py, first from the words with
                 this affix, else from all words with an affix of that kind.

What the affix pages and grammar entries state is applied on top:

* Quenya: prosodic lengthening and shortening before suffixes (course §6.1,
  Eldamo "prosodic lengthening", "shortened final syllables");
* Sindarin: a prefix usually lenites the base (Eldamo "soft mutation":
  liquid mutation after r, l is archaic, later compounds show soft
  mutation instead: calardan, ithildin); internal i-affection is "not an
  active feature of modern Sindarin compounds" (Eldamo "vowel mutations"), so
  it is not applied.
"""
from __future__ import annotations

import itertools
import re
from collections import Counter, defaultdict

from . import junctions as J
from . import morphophonology as M
from .interpreter import comparable, is_vowel, join, lengthen, phonemes
from .orthography import to_phonetic

SUPERSCRIPT = re.compile(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]')
KINDS = {'suf': 'suffix', 'pref': 'prefix'}
LENITION_WEIGHT = 0.5
MAX_OP = 2          # sounds of base or affix a junction change may replace
MORPH_WEIGHT = 0.3


def kind(entry: dict) -> str | None:
    return KINDS.get(entry.get('speech'))


def allomorphs(entry: dict, family: str) -> list:
    """Phonetic forms of an affix: -(n)dil -> ndil, dil; al(a)- -> ala, al;
    alternatives with / are split."""
    out = []
    for part in SUPERSCRIPT.sub('', entry['form']).split('/'):
        part = part.strip().strip('-').strip()
        groups = re.findall(r'\(([^)]*)\)', part)
        for keep in itertools.product((True, False), repeat=len(groups)):
            it = iter(keep)
            f = re.sub(r'\(([^)]*)\)', lambda m: m.group(1) if next(it) else '', part)
            f = to_phonetic(f, family).strip('-')
            if f and f not in out:
                out.append(f)
    return out


def _ctx(sound: str) -> str:
    return 'V' if is_vowel(sound) else 'C'


def lengthened(base: list) -> list | None:
    """The base with its last vowel lengthened (cen- + -ima -> cénima), or None
    when that vowel is long already or a diphthong ends the base syllable."""
    v = next((i for i in range(len(base) - 1, -1, -1) if is_vowel(base[i])), None)
    if v is None or _is_long(base[v]) or (v > 0 and is_vowel(base[v - 1])):
        return None
    out = list(base)
    out[v] = lengthen(out[v])
    return out


def length_key(base: list) -> str:
    from .stress import syllable_count
    return 'mono' if syllable_count(base) == 1 else 'poly'


def cases(branch: str, lexicon: list) -> list:
    """Attested derived words: one base and one affix of the branch's latest language."""
    code = {'quenya': 'q', 'sindarin': 's'}[branch]
    by_id = {e['id']: e for e in lexicon}
    rows = []
    for e in lexicon:
        if e['lang'] != code or e.get('neo') or len(e.get('elements', ())) != 2 or ' ' in e['form']:
            continue
        els = [by_id.get(x.get('id')) for x in e['elements']]
        if not all(els) or any(x['lang'] != code for x in els):
            continue
        kinds = [kind(x) for x in els]
        if kinds == [None, 'suffix']:
            base, affix, k = els[0], els[1], 'suffix'
        elif kinds == ['prefix', None]:
            affix, base, k = els[0], els[1], 'prefix'
        else:
            continue
        c = J._ph(e['form'], branch)
        best = None
        base_forms = (list(base.get('stems', ())) + [base['form']]) if k == 'suffix' else [base['form']]
        for bf in base_forms:
            pb0 = J._ph(bf, branch)
            longer = lengthened(pb0) if k == 'suffix' else None
            for pb, length in ((pb0, False), (longer, True)):
                if pb is None:
                    continue
                for allo in allomorphs(affix, branch):
                    pa = phonemes(comparable(allo))
                    a, b = (pb, pa) if k == 'suffix' else (pa, pb)
                    for short in ((False, True) if any(map(_is_long, b)) else (False,)):
                        r = J.analyse(a, J._short(b) if short else b, c)
                        # a lengthened base only when it fits better
                        if r and (best is None or r[2] + (0.5 if length else 0) < best['cost']):
                            best = {'cost': r[2] + (0.5 if length else 0), 'a': a, 'b': b, 'allo': allo,
                                    'base_form': bf, 'short': short, 'junction': r[0], 'ending': r[1],
                                    'lengthened': length, 'lkey': length_key(pb0) if longer is not None else None}
        if best is None or best['junction'][0] > MAX_OP or best['junction'][1] > MAX_OP:
            continue        # a change reaching deep into base or affix: the word is built otherwise (atheg < adar)
        a, b = best['a'], best['b']
        rows.append({'word': e['id'], 'form': e['form'], 'kind': k, 'affix': affix['id'], 'affix_form': affix['form'],
                     'base': base['id'], 'base_form': best['base_form'], 'allomorph': best['allo'],
                     'ctx': _ctx(b[0] if k == 'prefix' else a[-1]),
                     'a': join(a), 'b': join(b), 'c': join(c), 'junction': best['junction'], 'ending': best['ending'],
                     'short': best['short'], 'lengthened': best['lengthened'], 'lkey': best['lkey'], 'jkey': J.junction_key(a, b), 'ekey': J.ending_key(b), 'skey': J.short_key(b)})
    return rows


def _is_long(p: str) -> bool:
    from .interpreter import is_long
    return is_long(p)


def learn(rows: list) -> dict:
    """Per affix: allomorph counts by context and its own junction table;
    per kind: the pooled table used where an affix has no example."""
    by_affix = defaultdict(list)
    for r in rows:
        by_affix[r['affix']].append(r)
    def lengths(rs):
        c = defaultdict(Counter)
        for r in rs:
            if r.get('lkey'):
                c[r['lkey']][r['lengthened']] += 1
        return c
    model = {'kind': {k: J.learn([r for r in rows if r['kind'] == k]) for k in ('suffix', 'prefix')}, 'affix': {},
             'lengths': lengths([r for r in rows if r['kind'] == 'suffix'])}
    for aid, rs in by_affix.items():
        allo = defaultdict(Counter)
        for r in rs:
            allo[r['ctx']][r['allomorph']] += 1
        model['affix'][aid] = {'allomorphs': allo, 'table': J.learn(rs), 'n': len(rs), 'lengths': lengths(rs)}
    return model


def _table(model: dict, aid: str, k: str, jkey, ekey, skey) -> dict:
    """The affix's own counts for these keys, else those of its kind."""
    own = model['affix'].get(aid, {}).get('table')
    pooled = model['kind'][k]
    pick = lambda part, key: (own and own[part].get(key)) or pooled[part].get(key) or Counter()
    out = {'junction': {jkey: pick('junction', jkey)}, 'ending': {ekey: pick('ending', ekey)}, 'short': {}}
    if skey:
        out['short'][skey] = pick('short', skey)
    return out


def predict(model: dict, branch: str, affix: dict, base_forms: list, limit: int = 10) -> list:
    """Variants for affix + base forms [(form, source)]: [{'form', 'score', ...}]."""
    k = kind(affix)
    allos = allomorphs(affix, branch)
    info = model['affix'].get(affix['id'], {})
    scored = {}

    def add(form, score, rec):
        key = comparable(form)
        if key not in scored or scored[key][0] < score:
            scored[key] = (score, form, rec)

    bases = [(bf, how, False, 1.0) for bf, how in base_forms]
    if k == 'suffix':
        # lengthening of the base vowel before the suffix (Q. cénima "visible" vs. kalima
        # "luminous": PE22/156), as often as with this suffix, else with all suffixes
        for bf, how in base_forms:
            pb = phonemes(comparable(bf))
            longer = lengthened(pb)
            if longer is None:
                continue
            lk = length_key(pb)
            c = info.get('lengths', {}).get(lk) or model['lengths'].get(lk) or Counter()
            share = (c.get(True, 0) + 0.5) / (sum(c.values()) + 1)
            bases.append((join(longer), how, True, share))
            # the plain base keeps the complement
            i = next(i for i, x in enumerate(bases) if x[0] == bf and not x[2])
            bases[i] = (bf, how, False, 1 - share)
    if branch == 'sindarin' and k == 'prefix':
        for bf, h, _, sh in list(bases):
            m = M.lenite(phonemes(comparable(bf)))
            if m is not None:
                bases.append((join(m), 'soft-mutation', False, sh))
    for (bf, how, length, share), allo in itertools.product(bases, allos):
        pb, pa = phonemes(comparable(bf)), phonemes(comparable(allo))
        a, b = (pb, pa) if k == 'suffix' else (pa, pb)
        if not a or not b:
            continue
        ctx = _ctx(b[0] if k == 'prefix' else a[-1])
        counts = info.get('allomorphs', {}).get(ctx) or Counter()
        # allomorph share in this context (add-one smoothing over the affix's forms)
        w = (counts.get(allo, 0) + 1) / (sum(counts.values()) + len(allos))
        if how == 'dictionary' and any(h == 'stem' for _, h in base_forms):
            w *= 0.5
        if how == 'soft-mutation':
            w *= LENITION_WEIGHT
        w *= share
        table = _table(model, affix['id'], k, J.junction_key(a, b), J.ending_key(b), J.short_key(b))
        for form, p, jop, eop, short in J.predict(table, a, b, limit=limit):
            add(form, p * w, {'joined': join(a) + '+' + join(b), 'allomorph': allo, 'base': bf, 'base_source': how,
                              'junction': list(jop), 'ending': list(eop), 'shortened': short,
                              'lengthened': length, 'adjustments': []})
        if branch == 'quenya' and k == 'suffix':
            for v, rules in M.suffix_variants(a, b)[1:]:
                add(join(v), w * MORPH_WEIGHT, {'joined': join(a) + '+' + join(b), 'allomorph': allo, 'base': bf,
                                                'base_source': how, 'junction': [0, 0, ''], 'ending': [0, ''],
                                                'shortened': False, 'lengthened': length, 'adjustments': rules})
    ranked = sorted(scored.values(), key=lambda x: -x[0])
    return [{'form': f, 'score': round(sc, 3), **rec} for sc, f, rec in ranked[:limit]]


def leave_one_out(branch: str, lexicon: list, limit: int = 8) -> dict:
    """Each attested derived word predicted from its base and affix by a model
    learnt without it."""
    from .compound import forms_at_latest  # noqa: circular at import time
    by_id = {e['id']: e for e in lexicon}
    rows = cases(branch, lexicon)
    results = []
    for i, r in enumerate(rows):
        model = learn(rows[:i] + rows[i + 1:])
        base = by_id[r['base']]
        vs = predict(model, branch, by_id[r['affix']], forms_at_latest(base, branch, final=r['kind'] == 'prefix'))
        forms = [comparable(v['form']) for v in vs[:limit]]
        results.append({'word': r['word'], 'form': r['form'], 'kind': r['kind'], 'target': r['c'],
                        'main': vs[0]['form'] if vs else None,
                        'ok_main': bool(forms) and forms[0] == r['c'], 'ok_any': r['c'] in forms})
    out = {'cases': len(results), 'main': sum(x['ok_main'] for x in results),
           'any': sum(x['ok_any'] for x in results), 'results': results}
    for k in ('suffix', 'prefix'):
        rs = [x for x in results if x['kind'] == k]
        out[k] = {'cases': len(rs), 'main': sum(x['ok_main'] for x in rs), 'any': sum(x['ok_any'] for x in rs)}
    return out


def model_json(rows: list) -> dict:
    """The learnt model in JSON form (keys as in app/wordform.js)."""
    m = learn(rows)
    key = lambda parts: J._key(parts)
    dump = lambda t: {'junction': {key(k): [[list(op), n] for op, n in c.items()] for k, c in t['junction'].items()},
                      'ending': {key(k): [[list(op), n] for op, n in c.items()] for k, c in t['ending'].items()},
                      'short': {k: [[s, n] for s, n in c.items()] for k, c in t['short'].items()}}
    lengths = lambda c: {lk: [[v, n] for v, n in cc.items()] for lk, cc in c.items()}
    return {'kind': {k: dump(t) for k, t in m['kind'].items()}, 'lengths': lengths(m['lengths']),
            'affix': {aid: {'allomorphs': {ctx: [[a, n] for a, n in c.items()] for ctx, c in v['allomorphs'].items()},
                            'table': dump(v['table']), 'n': v['n'], 'lengths': lengths(v['lengths']),
                            'examples': [r['form'] for r in rows if r['affix'] == aid][:10]}
                      for aid, v in m['affix'].items()}}
