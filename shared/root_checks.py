"""Checks for roots reached through links that are not derivations of the word.

A word Eldamo says this one replaced (<deprecated>) is sometimes an earlier form of the
same word (ᴱQ. milt > NQ. miltë, N. rhand > NS. rand) and sometimes another word (NQ. sin
> latúcen "tin", Q. engë > né "was"): its roots are taken only when the two begin alike
and the consonants of the roots are found in this word. Ported from neo-roots
(neo_roots.py: same_onset, same_first_consonant, consonants_match), which resolves the
roots of the Neo-Quenya, Neo-Sindarin and Neo-Primitive word lists on the same data.
"""
from __future__ import annotations

import re
import unicodedata

# classes of consonants as Quenya keeps them: þ/th > s, w > v, kh > h, ñ > n, mb > m,
# nd > n, initial g- lost; a root's classes must appear in order in the word's
_CLS = [set('kgcqxhɣ'), set('tdθþðs'), set('pbfvwɸβ'), set('m'), set('nñŋ'), set('l'), set('r'), set('yj')]
_ONSET = [set('bvwβ'), set('kcgxh'), set('pfɸ'), set('tdθþð'), set('s'), set('nñŋ')]
SINDARIN_LIKE = {'ns', 's', 'n', 'en', 'g', 'on', 'os', 'norths', 'ilk', 'eilk', 'dan', 'nan'}


def _norm(s: str | None) -> str:
    s = unicodedata.normalize('NFD', (s or '').lower())
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰√✶*!^#†()\-\s]', '', s)


def _classes(s: str | None, sindarin: bool = False) -> list:
    """Consonant classes of a form, a repeated class once. In Sindarin ch, dh, lh, rh, mh
    are single sounds, and m joins the labials (lenition m > v)."""
    s = _norm(s)
    if sindarin:
        s = s.replace('ch', 'x').replace('dh', 'ð').replace('lh', 'l').replace('rh', 'r').replace('mh', 'v')
    # Q. ngw is ŋgw (ungwë < √UÑG): its g is kept as a velar, other gw > w (Q. vendë < GWEN)
    s = s.replace('ngw', 'ŋg').replace('kh', 'x').replace('th', 'θ').replace('ph', 'f').replace('qu', 'q') \
        .replace('kw', 'q').replace('gw', 'w').replace('ng', 'ŋ').replace('hy', 'h').replace('hl', 'l').replace('hr', 'r')
    out = []
    for ch in s:
        k = next((i for i, c in enumerate(_CLS) if ch in c), None)
        if k == 3 and sindarin:
            k = 2
        if k is not None and (not out or out[-1] != k):
            out.append(k)
    return out


def _first(x: str | None) -> str:
    """First consonant of a form ('' if it begins with a vowel), digraphs as one sound."""
    x = _norm(x)
    for a, b in (('gw', 'w'), ('th', 'θ'), ('ph', 'f'), ('kh', 'x'), ('ch', 'x'), ('dh', 'ð'),
                 ('hl', 'l'), ('lh', 'l'), ('hr', 'r'), ('rh', 'r'), ('hw', 'w'), ('hy', 'h'),
                 ('ng', 'ñ'), ('qu', 'q'), ('kw', 'q')):
        if x.startswith(a):
            x = b + x[len(a):]
            break
    m = re.match(r'[^aeiouyáéíóúâêîôûäëïöü]', x)
    return m.group(0) if m else ''


def same_first_consonant(a: str | None, b: str | None) -> bool:
    """The first consonant of two forms is the same sound up to b~v~w, k~c~g~h (not kw),
    p~f, t~d~th, n~ñ (ᴱ√SINI ~ ✶sinki; not ᴱ√GWAṘA ~ Q. psar-)."""
    fa, fb = _first(a), _first(b)
    if not fa or not fb:
        return not fa and not fb
    return fa == fb or any(fa in g and fb in g for g in _ONSET)


def same_onset(a: str | None, b: str | None) -> bool:
    """Two forms begin alike: both with a vowel, or the same first consonant
    (same_first_consonant), or a lost initial g-/w- before a vowel."""
    va, vb = not _first(a), not _first(b)
    if va and vb:
        return True
    if not va and not vb:
        return same_first_consonant(a, b)
    return (_first(a) or _first(b)) in ('g', 'w')


def _found(r: list, wc: list, skippable: set):
    best = None

    def go(i, j, n):
        nonlocal best
        if i == len(r):
            best = n if best is None else max(best, n)
            return
        for k in range(j, len(wc)):
            if wc[k] == r[i]:
                go(i + 1, k + 1, n + 1)
                break
        if r[i] in skippable:
            go(i + 1, j, n)
    go(0, 0, 0)
    return best


def consonants_match(word: str | None, root_form: str | None, lang: str | None) -> bool:
    """The consonants of the root, in order, among the word's: at least two of them (or the
    only one of both); a lost initial g-/w- when the word begins with a vowel. In Sindarin a
    velar or y of the root may be missing (medial g lost, y > i)."""
    sindarin = lang in SINDARIN_LIKE
    wc = _classes(word, sindarin)
    initial_vowel = bool(re.match(r'[aeiouáéíóúâêîôûäëïöüy]', _norm(word)))
    skippable = {0, 7} if sindarin else set()
    for variant in (root_form or '').split('/'):
        rc = _classes(variant, sindarin)
        if not rc:
            continue
        tries = [rc]
        if initial_vowel and rc[0] in (0, 2) and len(rc) > 1:
            tries.append(rc[1:])
        for r in tries:
            n = _found(r, wc, skippable)
            if n is not None and (n >= 2 or (len(rc) == 1 and len(wc) == 1 and n == 1)):
                return True
    return False
