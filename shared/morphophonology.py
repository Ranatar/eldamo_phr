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

* ima-class   -ima "-able" after a verb, by its class (Tolkien, Late Verb
                        Structure 1969, PE22/155-156; intro-quenya §9.1.4.1):
                        basic verbs lengthen the base vowel (car- > cárima),
                        a-verbs and half-strong verbs replace the final -a (an
                        a-verb may lengthen: ᴹQ. alfárima; ferya- > férima),
                        u-verbs and weak verbs just add it (liruima, tultaima).
                        The class is Eldamo's <class>, else guessed from the stem.

All functions work on phoneme lists in Eldamo's phonetic notation.
"""
from __future__ import annotations

from .interpreter import is_long, is_vowel, join, lengthen, phonemes, shorten
from .stress import heavy, nuclei

SOURCES = {
    'reduction': {'section': '§6.1.2.1', 'by': 'Толкин (PE17/106, PE21/32)'},
    'shortening': {'section': '§6.1.2.2', 'by': 'Страк, выведено из примеров'},
    'lengthening': {'section': '§6.1.3', 'by': 'практика Толкина, правила сформулированы Страком'},
    'ima-class': {'section': '§9.1.4.1', 'by': 'Толкин (PE22/155–156)'},
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


# Sindarin soft mutation (lenition) of an initial consonant, after Strack's
# Eldamo entry "soft mutation": the second element of a compound is usually
# lenited (Eldamo marks 402 such elements). Phonetic notation: c = k,
# ch = x, dh = ð, lh = l̥, rh = r̥, wh = w̥.
#   p t c > b d g;  b d > v dh;  g (and g of gw) vanishes;  m > v (optional:
#   "generally abandoned", but frequent "at the beginning of second elements of
#   compounds", PE23/136);  s > h;  h > ch;  wh > chw (Strack's analogy with
#   the nasal mutation);  n, f, th, l, r do not mutate;  lh, rh do not mutate
#   in modern Sindarin (archaic thl, thr: PE23/136);
#   an ancient nasalized stop (✶mb-, ✶nd-, ✶ŋg-, now b- d- g-) mutates to
#   m, n, ng: i·mbas / *i·mâr (PE17/104).
SOFT_MUTATION = [('gw', 'w'), ('p', 'b'), ('t', 'd'), ('k', 'g'), ('b', 'v'), ('d', 'ð'), ('g', ''),
                 ('m', 'v'), ('s', 'h'), ('h', 'x'), ('w̥', 'xw')]
NASALIZED = {'mb': 'm', 'nd': 'n', 'ŋg': 'ŋ'}


def lenite(word: list, primitive: str | None = None) -> list | None:
    """Soft mutation of the first sound of a Sindarin word, or None.
    `primitive`: the word's primitive form, to recognise ancient mb-, nd-, ŋg-."""
    s = join(word)
    if primitive:
        p = primitive.lstrip('-')
        for a, b in NASALIZED.items():
            if p.startswith(a) and s[:1] == a[1]:
                return phonemes(b + s[1:])
    for a, b in SOFT_MUTATION:
        if s.startswith(a):
            return phonemes(b + s[len(a):])
    return None


# -ima after a verb by its class (ima-class)
IMA_LENGTHEN = ('basic-verb',)
IMA_REPLACE_A = ('a-verb', 'ta-formative', 'na-formative', 'talat-stem')
IMA_ADD = ('u-verb', 'weak-verb', 'ta-causative', 'ya-causative', 'inceptive-verb')


def verb_classes(entry: dict) -> list:
    """[(class, weight)] of a Quenya verb: Eldamo's <class>, else guessed from its stem
    (a consonant: basic; -u: u-verb; -ta, -ya: formative or causative; -a: a-verb or weak)."""
    if entry.get('verb_class'):
        return [(entry['verb_class'], 1.0)]
    if 'vb' not in (entry.get('speech') or '').split():
        return []
    f = (entry.get('form') or '').rstrip('-¹²³⁴⁵⁶⁷⁸⁹⁰')
    if not f:
        return []
    if f[-1] not in 'aeiouáéíóú':
        return [('basic-verb', 1.0)]
    if f.endswith('u'):
        return [('u-verb', 1.0)]
    if f.endswith('ta'):
        return [('ta-formative', 0.5), ('ta-causative', 0.5)]
    if f.endswith('ya'):
        return [('ya-formative', 0.5), ('ya-causative', 0.5)]
    if f.endswith('a'):
        return [('a-verb', 0.5), ('weak-verb', 0.5)]
    return []


def ima_forms(stem: list, classes: list) -> list:
    """[(phonemes, weight, lengthened)] of stem + -ima for the verb's classes (ima-class)."""
    from .affixes import lengthened
    out = []

    def add(ph, w, length):
        for i, (q, w0, l0) in enumerate(out):
            if q == ph:
                out[i] = (q, w0 + w, l0)
                return
        out.append((ph, w, length))

    ima = phonemes('ima')
    for cls, w in classes:
        if cls in IMA_LENGTHEN:
            longer = lengthened(stem)
            add((longer or stem) + ima, w, longer is not None)
        elif cls in IMA_REPLACE_A and stem and stem[-1] == 'a':
            base = stem[:-1]
            longer = lengthened(base) if cls == 'a-verb' else None
            if longer is not None:
                add(longer + ima, w * 0.5, True)
                add(base + ima, w * 0.5, False)
            else:
                add(base + ima, w, False)
        elif cls == 'ya-formative' and stem[-2:] == ['j', 'a']:
            base = stem[:-2]
            longer = lengthened(base)
            add((longer or base) + ima, w, longer is not None)
        elif cls in IMA_ADD:
            add(stem + ima, w, False)
    return out
