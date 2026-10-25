"""Executor for Eldamo sound-change patterns.

Implements the notation documented by Paul Strack in Eldamo
(general/phonetic-descriptions.html, section "Sound Changes"):

* each phoneme (letter + diacritics/modifiers) matches exactly;
* ``{...}`` matches one element; ``|`` inside braces separates multi-phoneme
  elements (``{mb|nd}``); modifiers after the braces apply to every element
  (``{ptk}ʰ``);
* ``V`` any vowel, ``V̄`` long, ``V̆`` short, ``C`` any consonant, ``X`` any
  phoneme, ``S`` a syllable (consonants + vowel/diphthong + consonants);
* ``x-`` word-initial, ``-x`` word-final, ``-x-`` word-medial;
* ``ø`` marks a vanished or inserted phoneme and may be omitted when the
  alignment is unambiguous;
* numeric subscripts bind values for metathesis and copying;
* ``|`` at top level combines several patterns into one rule.

A rule is applied to every non-overlapping site of a word at once (a sound
law), and also, as a separate weaker candidate, to each single site.
Anything the notation does not define (``*``, ``?``, stress marks, unpaired
sets) raises :class:`Unsupported` instead of silently reporting "no match".
"""
from __future__ import annotations

import itertools
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache

SUBSCRIPTS = {'₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}
MODIFIERS = set('ʰʷʲ')
MACRON, BREVE, ACUTE = '\u0304', '\u0306', '\u0301'
VOWEL_BASES = set('aeiouyæœøəɛɔɨɯǫęɑɒʊɪ')
CLASSES = {'V', 'C', 'X', 'S'}
# Notational variants that denote the same sound in Eldamo forms.
EQUIVALENT = {'þ': 'θ', 'ñ': 'ŋ', 'ʒ': 'ɣ'}
BOUNDARY_CHARS = set("+’'ʼ·")
# Falling diphthongs: a rule whose match starts at their second element does
# not change it (u > o leaves the u of ou alone; ou > au applies).
LABIALIZABLE = set('kg')
DIPHTHONGS = {'ai', 'au', 'oi', 'ui', 'eu', 'iu', 'ei', 'ou', 'ae', 'oe', 'œi', 'yi', 'yu'}


class Unsupported(Exception):
    """The pattern uses notation this executor does not define."""


# --------------------------------------------------------------------------
# phonemes

def nfc(s: str) -> str:
    return unicodedata.normalize('NFC', s)


def phonemes(s: str) -> list[str]:
    """Split a string into phonemes: a base letter plus combining marks and modifiers."""
    out: list[str] = []
    for ch in unicodedata.normalize('NFD', s):
        if out and (unicodedata.combining(ch) or ch in MODIFIERS):
            out[-1] += ch
        else:
            out.append(ch)
    return [nfc(p) for p in out]


def canonical(p: str) -> str:
    """Comparison form: notational variants unified, breve (explicit shortness)
    and acute (stress in phonetic stages) removed."""
    p = nfc(p)
    if not p:
        return p
    p = EQUIVALENT.get(p[0], p[0]) + p[1:]   # composed letters: ñ, þ
    d = unicodedata.normalize('NFD', p)
    return nfc(d[0] + ''.join(c for c in d[1:] if c not in (BREVE, ACUTE)))


def base(p: str) -> str:
    d = unicodedata.normalize('NFD', p)
    return d[0] if d else ''


def is_vowel(p: str) -> bool:
    return base(p) in VOWEL_BASES


def is_long(p: str) -> bool:
    return MACRON in unicodedata.normalize('NFD', p)


def shorten(p: str) -> str:
    d = unicodedata.normalize('NFD', p)
    return nfc(''.join(c for c in d if c not in (MACRON, BREVE)))


def lengthen(p: str) -> str:
    d = unicodedata.normalize('NFD', shorten(p))
    return nfc(d[0] + MACRON + d[1:])


def strip_breve(p: str) -> str:
    return nfc(''.join(c for c in unicodedata.normalize('NFD', p) if c != BREVE))


# --------------------------------------------------------------------------
# pattern parsing

@dataclass
class Token:
    kind: str                      # 'lit' | 'set' | 'class' | 'null' | 'boundary' (+)
    options: tuple = ()            # lit: (tuple(phonemes),); set: tuple of phoneme tuples
    cls: str = ''                  # class letter
    length: str = ''               # '', 'long', 'short' (for V)
    index: str = ''
    star: bool = False             # Kleene star: zero or more repetitions
    stress: str = ''               # '', 'stressed' (V́, Ś, ˈ), 'unstressed' (ˌ)

    def family(self) -> str:
        if self.kind == 'class':
            return 'V' if self.cls == 'V' else self.cls
        return self.kind


@dataclass
class Pattern:
    tokens: list
    position: str                  # 'any' | 'initial' | 'final' | 'medial'
    text: str = ''


def split_top(s: str, sep: str = '|') -> list[str]:
    depth, start, parts = 0, 0, []
    for i, ch in enumerate(s):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                raise Unsupported('unbalanced braces')
        elif ch == sep and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    if depth:
        raise Unsupported('unbalanced braces')
    parts.append(s[start:])
    return parts


def position_of(s: str) -> tuple[str, str]:
    s = s.strip()
    if s.startswith('[') and s.endswith(']'):
        s = s[1:-1]
    lead, trail = s.startswith('-'), s.endswith('-') and len(s) > 1
    core = s[1 if lead else 0: len(s) - 1 if trail else len(s)]
    if lead and trail:
        return core, 'medial'
    if trail:
        return core, 'initial'
    if lead:
        return core, 'final'
    return core, 'any'


def _read_tail(s: str, i: int) -> tuple[str, str, int]:
    """Read modifiers/diacritics then subscripts following position i."""
    mods = ''
    while i < len(s) and (unicodedata.combining(s[i]) or s[i] in MODIFIERS):
        mods += s[i]
        i += 1
    idx = ''
    while i < len(s) and s[i] in SUBSCRIPTS:
        idx += SUBSCRIPTS[s[i]]
        i += 1
    return mods, idx, i


def parse_pattern(text: str) -> Pattern:
    core, position = position_of(text)
    # Stress marks: ˌ before a token = unstressed, ˈ = stressed, an acute on a
    # vowel or on S = stressed. They constrain matching only when the caller
    # supplies the stressed positions of the word (apply_rule(stress_mode=...));
    # otherwise they are ignored and such rules may over-apply.
    if any(ch in core for ch in '?()/=<>'):
        raise Unsupported('notation not defined by Eldamo documentation')
    s = unicodedata.normalize('NFD', core)
    tokens: list[Token] = []
    i = 0
    pending, mark = '', 0
    while i < len(s):
        if pending and len(tokens) > mark:
            tokens[mark].stress, pending = pending, ''
        ch = s[i]
        if ch in 'ˌˈ':
            pending, mark = ('unstressed' if ch == 'ˌ' else 'stressed'), len(tokens)
            i += 1
            continue
        if ch in ' \t':
            raise Unsupported('space inside pattern')
        if ch == '{':
            j = s.find('}', i)
            if j < 0:
                raise Unsupported('unclosed group')
            raw = s[i + 1:j]
            mods, idx, i = _read_tail(s, j + 1)
            if '|' in raw:
                opts = tuple(tuple(phonemes(o + mods)) for o in raw.split('|') if o)
            else:
                opts = tuple((p,) for p in phonemes(nfc(raw)))
                if mods:
                    opts = tuple((nfc(o[0] + mods),) for o in opts)
            if not opts:
                raise Unsupported('empty group')
            if any(c in CLASSES for o in opts for p in o for c in p):
                raise Unsupported('class inside group')
            tokens.append(Token('set', opts, index=idx, stress='stressed' if ACUTE in mods else ''))
            continue
        if ch == '+':
            # morpheme boundary: zero-width, matches where the form has + (or
            # anywhere when the form marks no boundaries)
            tokens.append(Token('boundary'))
            i += 1
            continue
        if ch == '*':
            if not tokens or tokens[-1].kind in ('null', 'boundary'):
                raise Unsupported('star without token')
            tokens[-1].star = True
            i += 1
            continue
        if ch in SUBSCRIPTS:
            raise Unsupported('subscript without token')
        if ch == '}':
            raise Unsupported('unbalanced braces')
        mods, idx, nxt = _read_tail(s, i + 1)
        if ch in CLASSES:
            length = 'long' if MACRON in mods else 'short' if BREVE in mods else ''
            if ch != 'V' and mods.replace(ACUTE, ''):
                raise Unsupported('diacritic on non-vowel class')
            tokens.append(Token('class', cls=ch, length=length, index=idx))
        elif ch == 'ø':
            tokens.append(Token('null', index=idx))
        else:
            tokens.append(Token('lit', ((nfc(ch + mods),),), index=idx))
        if ACUTE in mods:
            tokens[-1].stress = 'stressed'
        i = nxt
    if pending and len(tokens) > mark:
        tokens[mark].stress = pending
    return Pattern(tokens, position, text)


# --------------------------------------------------------------------------
# matching

def _lit_eq(pattern: str, sound: str) -> bool:
    """A pattern phoneme matches a word phoneme; an explicit breve in the
    pattern requires a short vowel, which word forms leave unmarked."""
    if BREVE in unicodedata.normalize('NFD', pattern) and is_long(sound):
        return False
    return canonical(pattern) == canonical(sound)


def _stress_ok(tok: Token, word: list[str], i: int, end: int, stress) -> bool:
    """A stress-marked token matches only a stressed (or unstressed) vowel;
    unknown stress (None) or a span without vowels satisfies any mark."""
    if not tok.stress or stress is None:
        return True
    vowels = [k for k in range(i, end) if is_vowel(word[k])]
    if not vowels:
        return True
    hit = any(k in stress for k in vowels)
    return hit if tok.stress == 'stressed' else not hit


def _match_token(tok: Token, word: list[str], i: int, open_start: bool = False, stress=None, bounds=None):
    """Yield (end, captured phonemes, chosen option index) for tok at word[i:]."""
    if tok.kind == 'boundary':
        if bounds is None or i in bounds:
            yield i, (), None
        return
    for end, cap, opt in _match_plain(tok, word, i, open_start):
        if _stress_ok(tok, word, i, end, stress):
            yield end, cap, opt


def _match_plain(tok: Token, word: list[str], i: int, open_start: bool = False):
    if tok.kind == 'null':
        yield i, (), None
        return
    if tok.kind in ('lit', 'set'):
        for k, opt in enumerate(tok.options):
            n = len(opt)
            if i + n <= len(word) and all(_lit_eq(x, y) for x, y in zip(opt, word[i:i + n])):
                yield i + n, tuple(word[i:i + n]), k
        return
    # classes
    if tok.cls == 'S':
        yield from _match_syllable(word, i, open_start)
        return
    if i >= len(word):
        return
    p = word[i]
    if tok.cls == 'C' and i + 1 < len(word) and base(p) in LABIALIZABLE and word[i + 1] == 'w':
        # kw, gw (Quenya qu, ngw) also count as one consonant: alakwā > alkwā
        yield i + 2, (p, 'w'), None
    if tok.cls == 'X':
        ok = True
    elif tok.cls == 'C':
        ok = not is_vowel(p)
    else:  # V
        ok = is_vowel(p) and (
            tok.length == '' or (tok.length == 'long') == is_long(p))
    if ok:
        yield i + 1, (p,), None


def _match_syllable(word: list[str], i: int, open_start: bool = False):
    n = len(word)
    if open_start:
        # a fragment such as "-ne": the syllable may begin before the fragment
        k = i
        while k < n and not is_vowel(word[k]):
            k += 1
            yield k, tuple(word[i:k]), None
    j = i
    while j < n and not is_vowel(word[j]):
        j += 1
    if j >= n:
        return
    nuclei = [j + 1]
    if j + 1 < n and is_vowel(word[j + 1]) and base(word[j + 1]) in 'iue' and not is_long(word[j + 1]):
        nuclei.append(j + 2)
    for k in nuclei:
        end = k
        ends = [end]
        while end < n and not is_vowel(word[end]):
            end += 1
            ends.append(end)
        for e in ends:
            yield e, tuple(word[i:e]), None


def match_at(pattern: Pattern, word: list[str], start: int, fragment: tuple[bool, bool], stress=None, bounds=None):
    """Yield (end, captures) for every way pattern matches word starting at start.
    stress: indices of stressed phonemes, or None when unknown; bounds: indices
    of phonemes preceded by a morpheme boundary, or None when unmarked."""
    lead_fragment, trail_fragment = fragment
    pos = pattern.position

    def rec(t, i, caps):
        if t == len(pattern.tokens):
            if pos == 'initial' and (start != 0 or lead_fragment):
                return
            if pos == 'final' and i != len(word):  # a stem such as dulθa- ends the word
                return
            if pos == 'medial' and (start == 0 and not lead_fragment or i == len(word) and not trail_fragment):
                return
            yield i, tuple(caps)
            return
        tok = pattern.tokens[t]
        if tok.star:
            # zero or more repetitions, longest first
            spans = [(i, ())]
            frontier = [(i, ())]
            while frontier:
                nxt = []
                for at, cap in frontier:
                    for end, c, _ in _match_token(tok, word, at, lead_fragment and at == 0, stress, bounds):
                        if end > at:
                            nxt.append((end, cap + c))
                spans += nxt
                frontier = nxt
            for end, cap in sorted(spans, key=lambda x: -x[0]):
                yield from rec(t + 1, end, caps + [(cap, None)])
            return
        for end, cap, opt in _match_token(tok, word, i, lead_fragment and i == 0, stress, bounds):
            yield from rec(t + 1, end, caps + [(cap, opt)])

    yield from rec(0, start, [])


def _offglide(word: list[str], i: int) -> bool:
    a, b = word[i - 1], word[i]
    return (is_vowel(a) and is_vowel(b) and not is_long(a) and not is_long(b)
            and canonical(a)[0] + canonical(b)[0] in DIPHTHONGS
            and not (i >= 2 and _offglide(word, i - 1)))


# --------------------------------------------------------------------------
# alignment and output

def _compatible(a: Token, b: Token) -> int:
    """Alignment cost between an input and output token (0 = same slot)."""
    if a.kind == 'boundary' or b.kind == 'boundary':
        return 0 if a.kind == b.kind else 2
    if a.kind == 'null' or b.kind == 'null':
        return 0
    if a.index and b.index and a.index == b.index:
        return 0
    if a.kind == 'class' and b.kind == 'class' and a.family() == b.family():
        return 0
    if a.kind == 'set' and b.kind == 'set' and len(a.options) == len(b.options):
        return 0
    if a.kind == 'lit' and b.kind == 'lit':
        x, y = a.options[0], b.options[0]
        if len(x) == 1 and len(y) == 1:
            if _lit_eq(x[0], y[0]):
                return 0
            return 1 if is_vowel(x[0]) == is_vowel(y[0]) else 2
        return 2
    return 2


def align(src: list[Token], dst: list[Token]) -> list[tuple]:
    """Pair input and output tokens; None marks deletion/insertion."""
    if len(src) == len(dst):
        return list(zip(src, dst))
    n, m = len(src), len(dst)
    INF = 10 ** 9
    cost = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if cost[i][j] == INF:
                continue
            if i < n and j < m:
                c = cost[i][j] + _compatible(src[i], dst[j])
                if c < cost[i + 1][j + 1]:
                    cost[i + 1][j + 1], back[i + 1][j + 1] = c, (i, j, 'pair')
            if i < n:
                c = cost[i][j] + 2
                if c < cost[i + 1][j]:
                    cost[i + 1][j], back[i + 1][j] = c, (i, j, 'del')
            if j < m:
                c = cost[i][j] + 2
                if c < cost[i][j + 1]:
                    cost[i][j + 1], back[i][j + 1] = c, (i, j, 'ins')
    out = []
    i, j = n, m
    while (i, j) != (0, 0):
        pi, pj, op = back[i][j]
        out.append((src[pi] if op != 'ins' else None, dst[pj] if op != 'del' else None))
        i, j = pi, pj
    return out[::-1]


def _render(out_tok: Token, in_tok, cap, opt, bound) -> list[list[str]]:
    """Return candidate phoneme lists produced for one output slot."""
    if out_tok is None:
        return [[]]
    if out_tok.kind in ('null', 'boundary'):
        return [[]]     # boundaries are carried over by position (apply_rule)
    if out_tok.kind == 'lit':
        return [list(out_tok.options[0])]
    if out_tok.kind == 'set':
        k = None
        if in_tok is not None and in_tok.kind == 'set' and len(in_tok.options) == len(out_tok.options):
            k = opt
        if out_tok.index and out_tok.index in bound and bound[out_tok.index][1] is not None \
                and len(bound[out_tok.index][2].options) == len(out_tok.options):
            k = bound[out_tok.index][1]
        if k is None:
            raise Unsupported('output set without a paired input set')
        return [list(out_tok.options[k])]
    # class
    source = None
    if out_tok.index and out_tok.index in bound:
        source = bound[out_tok.index][0]
    elif in_tok is not None and (in_tok.kind == 'class' or in_tok.kind in ('set', 'lit')):
        source = cap
    if source is None:
        raise Unsupported('output class without a source')
    source = list(source)
    if out_tok.star or (in_tok is not None and in_tok.star):
        return [source]
    if out_tok.cls == 'V' and source:
        v = source[-1]
        if out_tok.length == 'long':
            return [source[:-1] + [lengthen(v)]]
        if out_tok.length == 'short':
            return [source[:-1] + [shorten(v)]]
        if in_tok is not None and in_tok.kind == 'class' and in_tok.length and in_tok.length != out_tok.length:
            # V̄ > V or V̆ > V: notation leaves the length of the result open
            return [source, source[:-1] + [shorten(v)]]
    return [source]


def _family_key(tok: Token) -> str:
    if tok.kind == 'class':
        return 'class:' + tok.family()
    if tok.kind == 'set':
        return f'set:{len(tok.options)}'
    return ''


def _correspondences(src: list[Token], dst: list[Token]) -> list[dict]:
    """Candidate maps output-token index -> input-token index.

    Unindexed classes and sets correspond by order of occurrence within their
    family (V-family, C, X, S; sets of equal size), as in -ĕCi > -eiC or
    V̄jV > VijV. When the output has fewer members of a family than the input
    the outer members are kept: CCC > CC drops the middle consonant and
    -CC > -C the last one.
    """
    families: dict[str, tuple[list, list]] = {}
    for i, t in enumerate(src):
        k = _family_key(t)
        if k and not t.index:
            families.setdefault(k, ([], []))[0].append(i)
    for j, t in enumerate(dst):
        k = _family_key(t)
        if k and not t.index:
            families.setdefault(k, ([], []))[1].append(j)
    options = []
    for k, (ins, outs) in families.items():
        if not outs:
            continue
        if len(outs) > len(ins):
            if not ins:
                options.append([{}])  # fall back to positional alignment
                continue
            raise Unsupported('more output than input members of ' + k)
        # fewer output members: the outer ones stay and the inner ones vanish
        # (CCC > CC loses the middle consonant, -CC > -C the last one)
        keep = ins[:len(outs) - 1] + [ins[-1]] if len(outs) > 1 else ins[:1]
        options.append([dict(zip(outs, keep))])
    maps = []
    for combo in itertools.product(*options) if options else [()]:
        merged = {}
        for part in combo:
            merged.update(part)
        maps.append(merged)
    return maps


def transform(src: Pattern, dst: Pattern, captures) -> list[list[str]]:
    caps = list(captures)
    bound = {}
    for i, tok in enumerate(src.tokens):
        if tok.index:
            bound[tok.index] = (caps[i][0], caps[i][1], tok)
    positional = {}
    for a, b in align(src.tokens, dst.tokens):
        if a is not None and b is not None:
            positional[id(b)] = src.tokens.index(a)
    results = []
    for mapping in _correspondences(src.tokens, dst.tokens):
        pieces: list[list[list[str]]] = []
        for j, b in enumerate(dst.tokens):
            i = mapping.get(j, positional.get(id(b)))
            a = src.tokens[i] if i is not None else None
            cap, opt = caps[i] if i is not None else ((), None)
            pieces.append(_render(b, a, cap, opt, bound))
        for combo in itertools.product(*pieces):
            results.append([p for part in combo for p in part])
    return results


# --------------------------------------------------------------------------
# rules

@dataclass
class Rule:
    alternatives: list = field(default_factory=list)   # [(Pattern, Pattern)]

    @classmethod
    def parse(cls, src: str, dst: str) -> 'Rule':
        a, b = split_top(src.strip()), split_top(dst.strip())
        if len(a) != len(b):
            raise Unsupported('unpaired top-level alternatives')
        alts = []
        for x, y in zip(a, b):
            px, py = parse_pattern(x), parse_pattern(y)
            if px.position != py.position:
                raise Unsupported('different position constraints')
            if not px.tokens:
                raise Unsupported('empty input pattern')
            alts.append((px, py))
        return cls(alts)

    def sites(self, word: list[str], fragment=(False, False), stress=None, bounds=None):
        """All (start, end, alternatives' outputs) match sites."""
        out = []
        for start in range(len(word) + 1):
            for src, dst in self.alternatives:
                for end, caps in match_at(src, word, start, fragment, stress, bounds):
                    if end == start and all(t.kind in ('null', 'boundary') for t in src.tokens):
                        continue
                    outs = transform(src, dst, caps)
                    out.append((start, end, outs))
        return out


def boundaries(form: str) -> frozenset | None:
    """Indices (in normalize_word phonemes) of phonemes preceded by +, or None
    when the form marks no morpheme boundary."""
    s = nfc(form.strip())
    if '+' not in s:
        return None
    out, k = set(), 0
    for part in phonemes(''.join(ch for ch in s if ch not in BOUNDARY_CHARS - {'+'} and ch != '-' and not ch.isspace())):
        if part == '+':
            out.add(k)
        else:
            k += 1
    return frozenset(out)


def _rebuild(word: list[str], changes, bounds) -> str:
    """word with non-overlapping, sorted (start, end, replacement) changes
    applied. Morpheme boundaries stay at their positions; one inside a
    replaced span moves to its end."""
    bounds = bounds or frozenset()
    res, cursor = [], 0

    def copy(a, b):
        for k in range(a, b):
            if k in bounds:
                res.append('+')
            res.append(word[k])

    for cs, ce, repl in changes:
        copy(cursor, cs)
        if cs in bounds:
            res.append('+')
        res.extend(repl)
        if any(cs < k < ce for k in bounds):
            res.append('+')
        cursor = ce
    copy(cursor, len(word))
    if len(word) in bounds:
        res.append('+')
    return join(res)


def normalize_word(form: str) -> tuple[list[str], tuple[bool, bool]]:
    """Strip morpheme boundaries; report whether the form is a fragment at either edge."""
    s = nfc(form.strip())
    lead = s.startswith('-')
    trail = s.endswith('-')
    s = ''.join(ch for ch in s if ch not in BOUNDARY_CHARS and ch != '-' and not ch.isspace())
    return phonemes(s), (lead, trail)


def join(ph: list[str]) -> str:
    return nfc(''.join(ph))


@lru_cache(maxsize=None)
def compile_rule(src: str, dst: str) -> 'Rule':
    """Parsed rule, cached; raises Unsupported like Rule.parse."""
    return Rule.parse(src, dst)


def combine(rules) -> 'Rule':
    """One rule whose alternatives are those of all given rules (applied together)."""
    return Rule([alt for r in rules for alt in r.alternatives])


def apply(src: str, dst: str, form: str, limit: int = 64) -> dict:
    """Apply a rule to a word form.

    Returns {'all_sites': set, 'ordered': list, 'single_site': set, 'sites': n};
    'ordered' holds all_sites in the order of the rule's sub-formulas.
    'all_sites' applies the rule at every site at once; 'single_site' at one site.
    """
    return apply_rule(compile_rule(src, dst), form, limit)


def apply_rule(rule: 'Rule', form: str, limit: int = 64, protect: 'Rule | None' = None,
               stress_mode: str | None = None, scope: str | None = None) -> dict:
    """apply() for a compiled rule. `protect` lists patterns whose matches must
    not change (a rule's exceptions such as mb > mb). `stress_mode` ('initial',
    'latin', see shared.stress) makes stress-marked patterns match only
    stressed or unstressed vowels. `scope` restricts a rule named for
    monosyllables ('mono': the word has one syllable and the match covers its
    vowel and the word's end, as in C*V̆C) or polysyllables ('poly')."""
    word, fragment = normalize_word(form)
    stress = None
    if stress_mode:
        from .stress import stressed
        stress = stressed(word, stress_mode)
    bounds = boundaries(form)
    sites = rule.sites(word, fragment, stress, bounds)
    if scope:
        from .stress import syllable_count
        n = syllable_count(word)
        if scope == 'mono':
            sites = [x for x in sites if n == 1 and x[1] == len(word) and not any(is_vowel(p) for p in word[:x[0]])]
        elif scope == 'poly' and n < 2:
            sites = []
    guarded = []
    if protect is not None:
        guarded = [(st, en) for st, en, _ in protect.sites(word, fragment, stress, bounds)]
        if guarded:
            def free(cs, ce):
                return not any((cs < en and ce > st) if ce > cs else (st < cs < en) for st, en in guarded)
            sites = [(st, en, outs) for st, en, outs in sites if free(st, en)]
    # Only the part of a match that actually changes is replaced, so context
    # shared by neighbouring sites stays available in simultaneous
    # application (a sound law): VsV > VhV turns asasa into ahaha.
    changes = []   # per site: [(core start, core end, replacement), ...] one per output variant
    for start, end, outs in sites:
        variants = []
        span = word[start:end]
        for o in outs[:limit]:
            pre = 0
            while pre < len(span) and pre < len(o) and canonical(span[pre]) == canonical(o[pre]):
                pre += 1
            suf = 0
            while suf < len(span) - pre and suf < len(o) - pre and canonical(span[-1 - suf]) == canonical(o[-1 - suf]):
                suf += 1
            if pre == len(span) == len(o):
                continue  # no change at this site
            if pre == 0 and start > 0 and start < len(word) and _offglide(word, start):
                continue  # a lone vowel pattern leaves the second element of a diphthong alone
            cs = start + pre
            if cs == end - suf and 0 < cs < len(word) and word[cs - 1] == word[cs] and not is_vowel(word[cs]):
                continue  # nothing is inserted inside a geminate: ll is one long consonant, not C + l
            variants.append((start + pre, end - suf, tuple(o[pre:len(o) - suf])))
        if variants:
            changes.append(list(dict.fromkeys(variants)))   # keep the order of the sub-formulas
    single = {_rebuild(word, [(cs, ce, list(r))], bounds) for site in changes for cs, ce, r in site}
    if not changes and sites:
        single = {join(word)}     # the rule matches but changes nothing
    all_sites, ordered = set(), []
    for combo in itertools.islice(itertools.product(*changes), limit) if changes else ():
        chosen, last = [], -1
        for cs, ce, repl in sorted(combo):
            if cs >= last and not (cs == ce == last):
                chosen.append((cs, ce, repl))
                last = max(ce, cs + (1 if cs == ce else 0))
        out = _rebuild(word, [(cs, ce, list(repl)) for cs, ce, repl in chosen], bounds)
        if out not in all_sites:
            all_sites.add(out)
            ordered.append(out)
    return {'all_sites': all_sites, 'ordered': ordered, 'single_site': single, 'sites': len(sites)}


def comparable(form: str) -> str:
    """Form used to compare results: canonical phonemes, and two identical
    short vowels written as one long vowel (Eldamo writes both aa and ā)."""
    word, _ = normalize_word(form)
    out: list[str] = []
    for p in (canonical(x) for x in word):
        if out and is_vowel(p) and not is_long(p) and out[-1] == p:
            out[-1] = lengthen(p)
        else:
            out.append(p)
    return join(out)


def check(src: str, dst: str, before: str, after: str) -> str:
    """Classify whether rule src > dst turns `before` into `after`.

    reproduced          -- applying at every site gives `after`
    reproduced_partial  -- applying at a single site gives `after`
    mismatch            -- the rule applies but yields something else
    no_match            -- the rule does not apply to `before`
    unsupported:<why>   -- notation outside the documented grammar
    """
    if '+' in src and '+' not in before:
        return 'unsupported:morpheme boundary not marked in the form'
    try:
        res = apply(src, dst, before)
    except Unsupported as exc:
        return 'unsupported:' + str(exc)
    target = comparable(after)
    if target in {comparable(x) for x in res['all_sites']}:
        return 'reproduced'
    if target in {comparable(x) for x in res['single_site']}:
        return 'reproduced_partial'
    if comparable(before) == target and not res['sites']:
        return 'no_match'
    return 'mismatch' if res['sites'] else 'no_match'
