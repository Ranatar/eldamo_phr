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


SYLLABIC = {'ṛ': 'r', 'ḷ': 'l', 'ṇ': 'n', 'ṃ': 'm'}
NASALS = {'m', 'n', 'ŋ'}


def root_variants(form: str) -> list:
    """The forms a root stands for: WĀ/AWA -> wā, awa; IN(ID) -> in, inid; √KHYAR -> kʰjar."""
    out = []
    for part in (form or '').split('/'):
        part = re.sub(r'[√¹²³⁴⁵⁶⁷⁸⁹⁰\-]', '', part).strip()
        if not part:
            continue
        short = re.sub(r'\([^)]*\)', '', part)
        full = part.replace('(', '').replace(')', '')
        for f in dict.fromkeys([full, short]):
            ph = comparable(primitive_phonetic(f.lower()))
            if ph:
                out.append(ph)
                # most early roots repeat their vowel at the end (NERE, TORO, MBARA): the words
                # often lose it (nert, torn), so the root without it is a variant too
                q = phonemes(ph)
                vs = [x for x in q if is_vowel(x)]
                if len(q) > 2 and is_vowel(q[-1]) and len(vs) >= 2 and _base(vs[0]) == _base(q[-1]):
                    out.append(''.join(q[:-1]))
    return list(dict.fromkeys(out))


def root_phonetic(form: str) -> str:
    """√KHYAR, (A)LAK, LAS² -> kʰjar, alak, las (the first variant)."""
    v = root_variants(form)
    return v[0] if v else ''


def table(lexicon: list) -> list:
    """[[id, lang, form, [phonetic variants]]] of the roots in a lexicon, in a fixed order."""
    out = []
    for e in lexicon:
        if e.get('speech') == 'root' and e['lang'] in PRIMITIVE_ERA and not e.get('neo'):
            # a root needs a vowel: S- (the s-prefix of s-fortification) is not a root of words
            vs = [v for v in root_variants(e['form']) if any(is_vowel(p) for p in phonemes(v))]
            if vs:
                out.append([e['id'], e['lang'], e['form'], vs])
    return sorted(out, key=lambda r: (r[1], r[2], r[0]))


@lru_cache(maxsize=None)
def _phonemes(ph: str) -> tuple:
    return tuple(phonemes(ph))


def _base(p: str) -> str:
    return unicodedata.normalize('NFD', p)[0]


def _cons(ph) -> list:
    """Consonants of a form: a syllabic consonant as the plain one, a long (double)
    consonant once (grottā < ROT? lassē < LAS: dynamic lengthening)."""
    out = []
    for p in ph:
        if p in SYLLABIC:
            out.append(SYLLABIC[p])
        elif not is_vowel(p):
            q = _base(p) if p.endswith('ː') else p
            if not out or out[-1] != q:
                out.append(q)
    return out


def _match(fc: list, rc: list) -> int | None:
    """Penalty of reading the root consonants rc at the beginning of the form consonants fc:
    0 for a plain match; 1 for each nasal the form adds before a root consonant (nasal
    infixion: TAK > tankā, LAB > lambā) and for an initial s- the root lacks (s-fortification:
    smalu < MAL); None if they do not match."""
    best = None

    def go(i, j, pen, start):
        nonlocal best
        if best is not None and pen >= best:
            return
        if j == len(rc):
            best = pen
            return
        if i >= len(fc):
            return
        if fc[i] == rc[j]:
            go(i + 1, j + 1, pen, False)
        if start and fc[i] == 's' and rc[j] != 's':
            go(i + 1, j, pen + 1, False)
        if j > 0 and fc[i] in NASALS and rc[j] not in NASALS:
            go(i + 1, j, pen + 1, False)
    go(0, 0, 0, True)
    return best


def score(form_ph: list, root_ph: list) -> int | None:
    rc = _cons(root_ph)
    if not rc:
        return None
    pen = _match(_cons(form_ph), rc)
    if pen is None:
        return None
    s = 10 + len(rc) - pen
    rv = [p for p in root_ph if is_vowel(p)]
    fv = [p for p in form_ph if is_vowel(p)]
    augment = bool(form_ph) and is_vowel(form_ph[0]) and bool(root_ph) and not is_vowel(root_ph[0])
    if augment:
        # augmentation puts the base vowel before the root (✶ambar < MBAR, Anār < NAR); another
        # vowel is a prefix (al-, u-, o-) more often than not
        s -= 0 if rv and _base(form_ph[0]) == _base(rv[0]) else 2
    body = form_ph[1:] if augment else form_ph
    if [_base(x) for x in body[:len(root_ph)]] == [_base(x) for x in root_ph]:
        s += 4
    # the base vowel: the form's first vowel after an augment; a-fortification (ai, au) keeps it
    bv = [p for p in body if is_vowel(p)]
    if rv and bv and _base(rv[0]) == _base(bv[0]):
        s += 2
    elif rv and fv and _base(rv[0]) == _base(fv[0]):
        s += 1
    return s


def candidates(roots: list, form: str, era: str, limit: int = 3) -> list:
    """[(score, id, lang, form)] of the roots of the era that the primitive form could come
    from, best first."""
    ph = phonemes(comparable(form).strip('-'))
    out = []
    langs = ROOT_LANGS.get(era, {})
    for rid, lang, rform, variants in roots:
        if lang not in langs:
            continue
        scores = [x for x in (score(ph, list(_phonemes(v))) for v in variants) if x is not None]
        if scores:
            out.append((max(scores) + langs[lang], rid, lang, rform))
    out.sort(key=lambda t: (-t[0], t[3], t[1]))
    return out[:limit]
