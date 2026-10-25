"""Syllables and stress, after Paul Strack's Eldamo notes on Quenya and Sindarin stress.

Quenya (RGEO/60, quoted in Eldamo's "stress" entry): the main stress "was
originally on the first syllable of all words", then moved: in words of three
or more syllables it falls on the penultimate if that is heavy, otherwise on
the antepenultimate; disyllables keep it on the first syllable. Sindarin follows
the same pattern (LotR/1116). A heavy syllable has a long vowel, a diphthong,
or a short vowel followed by two or more consonants.

Modes: 'initial' (the old stress), 'latin' (the shifted one) and
'latin-sindarin', where an intervocalic ph [f] counts as a long consonant
(Orophin: o.RO.phin; th, dh, ch are single phonemes θ, ð, x anyway). Which
stage uses which mode is set in shared.languages. A form that marks stress
itself with an acute accent (kurúmbā) keeps the marked syllable.
"""
from __future__ import annotations

import unicodedata

from .interpreter import DIPHTHONGS, is_long, is_vowel, base

ACUTE = '́'
SYLLABIC = '̣'      # dot below: syllabic consonant (ṇ, ṃ, ḷ, ŋ̣)


def _nfd(p: str) -> str:
    return unicodedata.normalize('NFD', p)


def is_nucleus(p: str) -> bool:
    return is_vowel(p) or (SYLLABIC in _nfd(p) and not is_vowel(p))


def nuclei(word: list[str]) -> list[tuple[int, int, bool]]:
    """(start, end, heavy-by-itself) for every syllable nucleus; a diphthong is one nucleus."""
    out, i = [], 0
    while i < len(word):
        p = word[i]
        if not is_nucleus(p):
            i += 1
            continue
        if (i + 1 < len(word) and is_vowel(p) and is_vowel(word[i + 1]) and not is_long(p)
                and not is_long(word[i + 1]) and base(p) + base(word[i + 1]) in DIPHTHONGS):
            out.append((i, i + 2, True))
            i += 2
            continue
        out.append((i, i + 1, is_vowel(p) and is_long(p)))
        i += 1
    return out


LONG_CONSONANTS = {'latin-sindarin': {'f', 'ɸ'}}


def heavy(word: list[str], ns: list, k: int, mode: str = 'latin') -> bool:
    start, end, long_ = ns[k]
    if long_:
        return True
    nxt = ns[k + 1][0] if k + 1 < len(ns) else len(word)
    if nxt - end == 1 and k + 1 < len(ns) and base(word[end]) in LONG_CONSONANTS.get(mode, ()):
        return True
    return nxt - end >= 2


def stressed(word: list[str], mode: str | None) -> frozenset | None:
    """Indices of phonemes in the stressed nucleus, or None when stress is not modelled."""
    if not mode:
        return None
    marked = [i for i, p in enumerate(word) if ACUTE in _nfd(p)]
    if marked:
        return frozenset(marked)
    ns = nuclei(word)
    if not ns:
        return frozenset()
    if mode == 'initial' or len(ns) <= 2:
        k = 0
    elif mode in ('latin', 'latin-sindarin'):
        k = len(ns) - 2 if heavy(word, ns, len(ns) - 2, mode) else len(ns) - 3
    else:
        raise ValueError(f'unknown stress mode {mode}')
    start, end, _ = ns[k]
    return frozenset(range(start, end))


def syllable_count(word: list[str]) -> int:
    return len(nuclei(word))
