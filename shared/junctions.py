"""Junction table: how the elements of attested compounds meet at the latest stage.

For each Eldamo compound of two elements in the same language (Q. or S.)
the phonetic forms of the elements (first element: its stems and dictionary
form; second: dictionary form) are aligned with the compound:

    Casar + lië -> Casallië        junction  r|l -> ll
    Aldamir = alda + mīre          ending    -mīre -> -mir
    amdir = am + tir (S.)          junction  m|t -> md   (soft mutation)

Two kinds of changes are collected:

* junction -- the end of the first element and the start of the second,
  keyed by (last sound of the first element, first sound of the second);
* ending   -- the end of the compound against the end of the second element,
  keyed by the last two sounds of the second element.

Each key keeps how often each outcome occurs, including "no change". The
table predicts variants for new compounds; the leave-one-out check rebuilds
the table without a compound and predicts it.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from .interpreter import comparable, is_long, is_vowel, join, phonemes, shorten
from .orthography import to_phonetic

MAX_SHARE_CHANGED = 0.5
SMOOTHING = 0.5


def _ph(form: str, family: str) -> list:
    return phonemes(comparable(to_phonetic(form, family).strip('-')))


def _align(x: list, y: list):
    """Edit alignment of x to y: list of (x index or None, y index or None)."""
    n, m = len(x), len(y)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (0 if x[i - 1] == y[j - 1] else 1))
    out, i, j = [], n, m
    while i or j:
        # on ties a gap is taken first, which places changes as late as
        # possible: aegloss -> aeglos loses the last s
        if i and d[i][j] == d[i - 1][j] + 1:
            out.append((i - 1, None))
            i -= 1
        elif j and d[i][j] == d[i][j - 1] + 1:
            out.append((None, j - 1))
            j -= 1
        else:
            out.append((i - 1, j - 1))
            i, j = i - 1, j - 1
    return out[::-1], d[n][m]


def _short(p: list) -> list:
    return [shorten(x) if is_vowel(x) else x for x in p]


def analyse(a: list, b: list, c: list):
    """(junction, ending, cost) or None. junction = (k, m, replacement): the
    last k sounds of a and the first m of b become `replacement`; ending =
    (k, replacement) for the last k sounds of b."""
    x = a + b
    if not a or not b or not c:
        return None
    al, cost = _align(x, c)
    if cost > MAX_SHARE_CHANGED * max(len(x), len(c)):
        return None
    edge = len(a)
    same = [xi is not None and yj is not None and x[xi] == c[yj] for xi, yj in al]
    # the junction region: the run of mismatches touching the boundary
    bpos = next((t for t, (xi, _) in enumerate(al) if xi is not None and xi >= edge), len(al))
    lo = bpos
    while lo > 0 and not same[lo - 1]:
        lo -= 1
    hi = bpos
    while hi < len(al) and not same[hi]:
        hi += 1
    xs = [al[t][0] for t in range(lo, hi) if al[t][0] is not None]
    ys = [al[t][1] for t in range(lo, hi) if al[t][1] is not None]
    k = sum(1 for i in xs if i < edge)
    m = sum(1 for i in xs if i >= edge)
    junction = (k, m, join([c[j] for j in ys]))
    # ending: mismatches from the last exact match to the end
    last = max((t for t in range(len(al)) if same[t]), default=-1)
    tail = al[last + 1:]
    if tail and last >= hi:
        kx = sum(1 for xi, _ in tail if xi is not None)
        rep = join([c[yj] for _, yj in tail if yj is not None])
        ending = (kx, rep)
    else:
        ending = (0, '')
    return junction, ending, cost


def junction_key(a: list, b: list) -> tuple:
    return (a[-1], b[0])


def ending_key(b: list) -> tuple:
    return tuple(b[-2:])


def short_key(b: list) -> str | None:
    """Whether the second element has a long vowel, and where: a long vowel of
    the second element is often shortened in the compound (Aldamir < mīre)."""
    if not any(is_long(x) for x in b):
        return None
    vs = [i for i, x in enumerate(b) if is_vowel(x)]
    return 'last' if is_long(b[vs[-1]]) else 'earlier'


def cases(branch: str, lexicon: list) -> list:
    """Compounds of two same-language elements with their aligned changes."""
    code = {'quenya': 'q', 'sindarin': 's'}[branch]
    by_id = {e['id']: e for e in lexicon}
    out = []
    for e in lexicon:
        if e['lang'] != code or e.get('neo') or len(e.get('elements', ())) != 2 or ' ' in e['form']:
            continue
        els = [by_id.get(x.get('id')) for x in e['elements']]
        if not all(els) or any(x['lang'] != code for x in els):
            continue
        c = _ph(e['form'], branch)
        b = _ph(els[1]['form'], branch)
        best = None
        for f in list(els[0].get('stems', ())) + [els[0]['form']]:
            a = _ph(f, branch)
            for short in ((False, True) if any(is_long(x) for x in b) else (False,)):
                r = analyse(a, _short(b) if short else b, c)
                if r and (best is None or r[2] < best[4][2]):
                    best = (f, a, b, short, r)
        if best is None:
            continue
        f, a, b, short, (junction, ending, cost) = best
        out.append({'word': e['id'], 'form': e['form'], 'first': f, 'second': els[1]['form'],
                    'a': join(a), 'b': join(b), 'c': join(c), 'junction': junction, 'ending': ending,
                    'short': short, 'jkey': junction_key(a, b), 'ekey': ending_key(b), 'skey': short_key(b)})
    return out


def learn(rows: list) -> dict:
    j, e, sh = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
    for r in rows:
        j[tuple(r['jkey'])][tuple(r['junction'])] += 1
        e[tuple(r['ekey'])][tuple(r['ending'])] += 1
        if r['skey']:
            sh[r['skey']][r['short']] += 1
    return {'junction': j, 'ending': e, 'short': sh}


def _apply_j(a: list, b: list, op) -> list | None:
    k, m, rep = op
    if k > len(a) or m > len(b):
        return None
    return a[:len(a) - k] + phonemes(rep) + b[m:]


def _apply_e(c: list, op) -> list | None:
    k, rep = op
    if k > len(c):
        return None
    return c[:len(c) - k] + phonemes(rep)


def predict(table: dict, a: list, b: list, limit: int = 6) -> list:
    """[(form, probability, junction op, ending op, shortened)] most probable first."""
    out = {}
    sk = short_key(b)
    shorts = table.get('short', {}).get(sk) if sk else None
    for short, sc in (shorts or Counter({False: 1})).items():
        sn = sum((shorts or Counter({False: 1})).values())
        for form, p, jo, eo in _predict(table, a, _short(b) if short else b, limit):
            p = p * sc / sn
            if form not in out or out[form][0] < p:
                out[form] = (p, jo, eo, short)
    ranked = sorted(out.items(), key=lambda kv: -kv[1][0])[:limit]
    return [(f, round(p, 3), jo, eo, short) for f, (p, jo, eo, short) in ranked]


def _predict(table: dict, a: list, b: list, limit: int) -> list:
    # the plain join stays possible even where no attested compound shows it
    jops = Counter(table['junction'].get(junction_key(a, b)) or {})
    eops = Counter(table['ending'].get(ending_key(b)) or {})
    jops[(0, 0, '')] += SMOOTHING if jops else 1
    eops[(0, '')] += SMOOTHING if eops else 1
    jn, en = sum(jops.values()), sum(eops.values())
    out = {}
    for jo, jc in jops.items():
        joined = _apply_j(a, b, jo)
        if joined is None:
            continue
        for eo, ec in eops.items():
            # an ending change applies only to the part that came from b
            if eo[0] > len(b) - jo[1]:
                continue
            form = _apply_e(joined, eo)
            if form is None:
                continue
            key = join(form)
            p = (jc / jn) * (ec / en)
            if key not in out or out[key][0] < p:
                out[key] = (p, jo, eo)
    ranked = sorted(out.items(), key=lambda kv: -kv[1][0])[:limit * 2]
    return [(f, p, jo, eo) for f, (p, jo, eo) in ranked]


def leave_one_out(rows: list) -> dict:
    full = learn(rows)
    top = anyv = 0
    misses = []
    for r in rows:
        t = {'junction': defaultdict(Counter, {k: Counter(v) for k, v in full['junction'].items()}),
             'ending': defaultdict(Counter, {k: Counter(v) for k, v in full['ending'].items()})}
        t['short'] = defaultdict(Counter, {k: Counter(v) for k, v in full['short'].items()})
        t['junction'][r['jkey']][r['junction']] -= 1
        t['ending'][r['ekey']][r['ending']] -= 1
        if r['skey']:
            t['short'][r['skey']][r['short']] -= 1
        for part in t.values():
            for k in list(part):
                part[k] = +part[k]
                if not part[k]:
                    del part[k]
        preds = [f for f, *_ in predict(t, phonemes(r['a']), phonemes(r['b']))]
        if preds and preds[0] == r['c']:
            top += 1
        if r['c'] in preds:
            anyv += 1
        else:
            misses.append(r)
    return {'cases': len(rows), 'top': top, 'any': anyv, 'misses': misses}


def table_json(rows: list) -> dict:
    t = learn(rows)
    examples = defaultdict(list)
    for r in rows:
        examples[('j', r['jkey'], r['junction'])].append(r['form'])
        examples[('e', r['ekey'], r['ending'])].append(r['form'])

    shortening = {k: dict(v) for k, v in t['short'].items()}

    def dump(kind, part):
        out = []
        for key, c in sorted(part.items(), key=lambda kv: -sum(kv[1].values())):
            total = sum(c.values())
            out.append({'key': list(key), 'total': total, 'outcomes': [
                {'op': list(op), 'count': n, 'examples': examples[(kind, key, op)][:5]}
                for op, n in c.most_common()]})
        return out
    return {'junction': dump('j', t['junction']), 'ending': dump('e', t['ending']),
            'shortening': {k: {str(s): n for s, n in v.items()} for k, v in shortening.items()}}
