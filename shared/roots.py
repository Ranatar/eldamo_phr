"""Roots for a primitive form: which roots of Eldamo a primitive form could come from.

A root (√KHYAR, ᴹ√MBAR) is not a form the sound laws act on: primitive words are built
from it by morphology -- suffixes (✶kʰjar-ja), an augment vowel (✶a-mbar-a), vowel
grades. So the laws do not run back from a primitive form to a root; instead the roots
of the same conception are matched against it: the consonants of the root must begin
the consonants of the form (after an augment vowel, if any), and a root whose whole
form, vowels included, begins the form ranks higher, then a root with the same first
vowel, then a longer root. Measured on the primitive forms Eldamo gives for words
whose root it names (reports/reconstruction.md, «Корни по праформе»). app/wordform.js
repeats candidates().
"""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

from .interpreter import comparable, is_vowel, phonemes
from .orthography import primitive_phonetic

PRIMITIVE_ERA = {'p': 'late', 'mp': 'middle', 'ep': 'early'}
# the roots of each conception; adding the middle roots to the late ones (Eldamo gives many
# late words a root of The Etymologies: Q. lár < ᴹ√DAR) finds more but ranks worse
ROOT_LANGS = {'late': {'p': 0}, 'middle': {'mp': 0}, 'early': {'ep': 0}}


def root_phonetic(form: str) -> str:
    """√KHYAR, (A)LAK, LAS² -> kʰjar, alak, las."""
    f = re.sub(r'[√¹²³⁴⁵⁶⁷⁸⁹⁰()\-]', '', form or '').strip().lower()
    return comparable(primitive_phonetic(f))


def table(lexicon: list) -> list:
    """[[id, lang, form, phonetic]] of the roots in a lexicon, in a fixed order."""
    out = []
    for e in lexicon:
        if e.get('speech') == 'root' and e['lang'] in PRIMITIVE_ERA and not e.get('neo'):
            ph = root_phonetic(e['form'])
            if ph:
                out.append([e['id'], e['lang'], e['form'], ph])
    return sorted(out, key=lambda r: (r[1], r[2], r[0]))


@lru_cache(maxsize=None)
def _phonemes(ph: str) -> tuple:
    return tuple(phonemes(ph))


def _base(p: str) -> str:
    return unicodedata.normalize('NFD', p)[0]


def score(form_ph: list, root_ph: list) -> int | None:
    fc = [p for p in form_ph if not is_vowel(p)]
    rc = [p for p in root_ph if not is_vowel(p)]
    if not rc or fc[:len(rc)] != rc:
        return None
    s = 10 + len(rc)
    augment = bool(form_ph) and is_vowel(form_ph[0]) and bool(root_ph) and not is_vowel(root_ph[0])
    body = form_ph[1:] if augment else form_ph
    if [_base(x) for x in body[:len(root_ph)]] == [_base(x) for x in root_ph]:
        s += 4
    rv = [p for p in root_ph if is_vowel(p)]
    fv = [p for p in form_ph if is_vowel(p)]
    if rv and fv and _base(rv[0]) == _base(fv[0]):
        s += 2
    if augment:
        s -= 1
    return s


def candidates(roots: list, form: str, era: str, limit: int = 3) -> list:
    """[(score, id, lang, form)] of the roots of the era that the primitive form could come
    from, best first."""
    ph = phonemes(comparable(form).strip('-'))
    out = []
    langs = ROOT_LANGS.get(era, {})
    for rid, lang, rform, rph in roots:
        if lang not in langs:
            continue
        s = score(ph, list(_phonemes(rph)))
        if s is not None:
            out.append((s + langs[lang], rid, lang, rform))
    out.sort(key=lambda t: (-t[0], t[3], t[1]))
    return out[:limit]
