"""Synchronic Quenya morphophonology after Paul Strack's Quenya course, §6.1.

These are adjustments of Quenya proper (not historical sound laws) applied
when a compound or a suffixed word is formed at the latest stage. Each rule
records its paragraph and who stated it:

* reduction   §6.1.2.1  long compounds lose the final vowel, shorten a long
                        vowel of the last syllable and simplify a final
                        cluster, restored in the stem: Valinórë -> Valinor,
                        Moriquen (Moriquend-), caimasan (caimasamb-),
                        Eldamar < már. Tolkien (PE17/106, PE21/32).
* shortening  §6.1.2.2  a long vowel in the second-to-last syllable of a
                        longer word shortens before a directional suffix:
                        Endórë -> Endorenna (but lúmenna). Strack, deduced
                        from examples.
* lengthening §6.1.3    prosodic lengthening at the boundary of a word of
                        three or more syllables: culuma + -va -> culumáva,
                        Atanatar + -i -> Atanatári, telumë + -va ->
                        teluméva but falassë + -va -> falasseva; with a
                        disyllabic suffix falassélion; in compounds
                        cuivië + nén -> Cuiviénen. Tolkien's usage, rules
                        formulated by Strack.

All functions work on phoneme lists in Eldamo's phonetic notation.
"""
from __future__ import annotations

from .interpreter import is_long, is_vowel, join, lengthen, phonemes, shorten
from .stress import heavy, nuclei

SOURCES = {
    'reduction': {'section': '§6.1.2.1', 'by': 'Толкин (PE17/106, PE21/32)'},
    'shortening': {'section': '§6.1.2.2', 'by': 'Страк, выведено из примеров'},
    'lengthening': {'section': '§6.1.3', 'by': 'практика Толкина, правила сформулированы Страком'},
}
DIRECTIONAL = ('nna', 'llo', 'sse', 'nnar', 'llon', 'ssen')
FINAL_OK = set('tsnrl')          # consonants a Quenya word may end in


def syllables(word: list) -> int:
    return len(nuclei(word))


def _last_vowel(word: list) -> int | None:
    return next((i for i in range(len(word) - 1, -1, -1) if is_vowel(word[i])), None)


def reduce_compound(word: list) -> tuple[list, list] | None:
    """(reduced form, stem) of a long compound, or None when the rule does not apply.

    The final short vowel is lost, a long vowel of the new last syllable is
    shortened, a final cluster keeps its first consonant (final m becomes n);
    the stem keeps the cluster."""
    if syllables(word) < 3 or not is_vowel(word[-1]) or is_long(word[-1]):
        return None
    if len(word) > 1 and is_vowel(word[-2]):
        return None                       # a diphthong or hiatus at the end: Andúnië stays
    stem = word[:-1]
    form = list(stem)
    v = _last_vowel(form)
    if v is not None and is_long(form[v]):
        form[v] = shorten(form[v])
    coda = len(form) - 1 - v if v is not None else 0
    if coda > 1:
        form = form[:v + 2]
    if form and form[-1] == 'm':
        form[-1] = 'n'
    if form and not is_vowel(form[-1]) and form[-1] not in FINAL_OK:
        return None
    return form, stem


def shorten_final_long(word: list, boundary: int) -> list | None:
    """már -> -mar: a long vowel in a monosyllabic last element shortens."""
    tail = word[boundary:]
    if syllables(tail) != 1:
        return None
    v = _last_vowel(word)
    if v is None or v < boundary or not is_long(word[v]):
        return None
    out = list(word)
    out[v] = shorten(out[v])
    return out


def directional_shortening(base: list, suffix: list) -> list | None:
    """Endórë + -nna -> Endorenna: long penult of a longer base shortens."""
    if join(suffix) not in DIRECTIONAL or syllables(base) < 3:
        return None
    ns = nuclei(base)
    start, end, _ = ns[-2]
    if not any(is_long(base[i]) for i in range(start, end)):
        return None
    out = list(base)
    for i in range(start, end):
        out[i] = shorten(out[i])
    return out + suffix


def prosodic_lengthening(base: list, suffix: list, e_noun: bool = False) -> list | None:
    """Lengthen the vowel at the boundary of a base of three or more syllables.

    (a) base ends in a vowel and the suffix starts with a single consonant;
    (b) base ends in a single consonant and the suffix starts with a vowel
        (possibly followed by a single consonant).
    A monosyllabic suffix lengthens only when both preceding syllables are
    light; a disyllabic one always. A final cluster of the base blocks the
    lengthening; -i, -in, -ion replacing the final -e of an e-noun do not
    trigger it."""
    if syllables(base) < 3 or not suffix:
        return None
    ns = nuclei(base)
    s_syl = syllables(suffix)
    if is_vowel(base[-1]):
        if is_vowel(suffix[0]) or (len(suffix) > 1 and not is_vowel(suffix[1])):
            return None                     # (a) needs a single consonant
        target = ns[-1]
    else:
        if len(base) > 1 and not is_vowel(base[-2]):
            return None                     # final cluster: Moriquend-ion
        if not is_vowel(suffix[0]) or (e_noun and join(suffix) in ('i', 'in', 'ion')):
            return None
        if len(suffix) > 2 and not is_vowel(suffix[1]) and not is_vowel(suffix[2]):
            return None                     # vowel + cluster
        target = ns[-1]
    start, end, long_ = target
    if long_:
        return None                         # already long or a diphthong
    if s_syl < 2:
        k = len(ns) - 1
        light = all(not heavy(base + suffix, nuclei(base + suffix), j) for j in (k - 1, k))
        if not light:
            return None
    out = list(base)
    out[start] = lengthen(out[start])
    return out + suffix


def compound_variants(first: list, second: list) -> list:
    """Variants of a two-element compound at the latest stage:
    [(form, stem or None, [rule names])]. The plain join comes first."""
    word = first + second
    out = [(word, None, [])]
    length = prosodic_lengthening(first, second)
    if length is not None:
        out.append((length, None, ['lengthening']))
    for base, rules in list((w, r) for w, _, r in out):
        red = reduce_compound(base)
        if red is not None:
            out.append((red[0], red[1], rules + ['reduction']))
        sh = shorten_final_long(base, len(first))
        if sh is not None:
            out.append((sh, None, rules + ['reduction']))
    seen, uniq = set(), []
    for w, stem, rules in out:
        key = join(w)
        if key not in seen:
            seen.add(key)
            uniq.append((w, stem, rules))
    return uniq


def suffix_variants(base: list, suffix: list, e_noun: bool = False) -> list:
    out = [(base + suffix, [])]
    for fn, name in ((directional_shortening, 'shortening'),):
        r = fn(base, suffix)
        if r is not None:
            out.append((r, [name]))
    r = prosodic_lengthening(base, suffix, e_noun)
    if r is not None:
        out.append((r, ['lengthening']))
    return out


def text(form: str) -> list:
    return phonemes(form)


# Sindarin soft mutation (lenition) of an initial consonant: the second element
# of a compound is usually lenited (Eldamo marks 402 such elements). Phonetic
# notation: c = k, ch = x, dh = ð, lh = l̥, rh = r̥.
SOFT_MUTATION = [('gw', 'w'), ('p', 'b'), ('t', 'd'), ('k', 'g'), ('b', 'v'), ('d', 'ð'), ('g', ''),
                 ('m', 'v'), ('s', 'h'), ('h', 'x'), ('l̥', 'l'), ('r̥', 'r'), ('w̥', 'xw')]


def lenite(word: list) -> list | None:
    """Soft mutation of the first sound of a Sindarin word, or None."""
    s = join(word)
    for a, b in SOFT_MUTATION:
        if s.startswith(a):
            return phonemes(b + s[len(a):])
    return None
