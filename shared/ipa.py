"""Phonetic classification used to lay out the sound picker of the atlas.

The grid is generated from each branch's phoneme inventory, so a symbol
missing from a branch simply does not appear. Symbols not listed here fall
into an "other" group instead of being dropped.
"""
from __future__ import annotations

PLACES = [('labial', 'Губные'), ('dental', 'Зубные / альвеолярные'), ('palatal', 'Палатальные'),
          ('velar', 'Велярные'), ('labiovelar', 'Лабиовелярные'), ('glottal', 'Гортанные')]
MANNERS = [('stop', 'Смычные'), ('fricative', 'Фрикативные'), ('nasal', 'Носовые'),
           ('lateral', 'Боковые'), ('trill', 'Дрожащие'), ('approximant', 'Аппроксиманты')]
HEIGHTS = [('high', 'Верхние'), ('mid', 'Средние'), ('low', 'Нижние')]
BACKNESS = [('front', 'Передние'), ('central', 'Центральные'), ('back', 'Задние')]

CONSONANTS = {
    'p': ('stop', 'labial'), 'b': ('stop', 'labial'), 'pʰ': ('stop', 'labial'),
    't': ('stop', 'dental'), 'd': ('stop', 'dental'), 'tʰ': ('stop', 'dental'),
    'tʲ': ('stop', 'palatal'), 'dʲ': ('stop', 'palatal'),
    'k': ('stop', 'velar'), 'g': ('stop', 'velar'), 'kʰ': ('stop', 'velar'),
    'kʷ': ('stop', 'labiovelar'), 'gʷ': ('stop', 'labiovelar'),
    'ɸ': ('fricative', 'labial'), 'β': ('fricative', 'labial'), 'f': ('fricative', 'labial'), 'v': ('fricative', 'labial'),
    'θ': ('fricative', 'dental'), 'ð': ('fricative', 'dental'), 's': ('fricative', 'dental'), 'z': ('fricative', 'dental'),
    'x': ('fricative', 'velar'), 'ɣ': ('fricative', 'velar'), 'h': ('fricative', 'glottal'),
    'm': ('nasal', 'labial'), 'm̥': ('nasal', 'labial'),
    'n': ('nasal', 'dental'), 'n̥': ('nasal', 'dental'), 'nʲ': ('nasal', 'palatal'),
    'ŋ': ('nasal', 'velar'), 'ŋʷ': ('nasal', 'labiovelar'),
    'l': ('lateral', 'dental'), 'l̥': ('lateral', 'dental'),
    'r': ('trill', 'dental'), 'r̥': ('trill', 'dental'),
    'j': ('approximant', 'palatal'), 'j̊': ('approximant', 'palatal'),
    'w': ('approximant', 'labiovelar'), 'w̥': ('approximant', 'labiovelar'),
}
VOWELS = {
    'i': ('high', 'front'), 'ī': ('high', 'front'), 'y': ('high', 'front'), 'ȳ': ('high', 'front'),
    'u': ('high', 'back'), 'ū': ('high', 'back'),
    'e': ('mid', 'front'), 'ē': ('mid', 'front'), 'ę̄': ('mid', 'front'), 'œ': ('mid', 'front'),
    'o': ('mid', 'back'), 'ō': ('mid', 'back'), 'ǭ': ('mid', 'back'),
    'a': ('low', 'central'), 'ā': ('low', 'central'), 'ǣ': ('low', 'front'),
}
DIPHTHONG_ENDS = [('i', 'На -i'), ('u', 'На -u'), ('e', 'На -e'), ('w', 'На -w')]
NULL_LABEL = 'ø — исчезновение звука'


def classify(symbol: str) -> dict:
    if symbol in CONSONANTS:
        manner, place = CONSONANTS[symbol]
        return {'group': 'consonant', 'row': manner, 'col': place}
    if symbol in VOWELS:
        height, back = VOWELS[symbol]
        return {'group': 'vowel', 'row': height, 'col': back}
    if symbol == 'ø':
        return {'group': 'null'}
    if len(symbol) == 2 and symbol[0] in 'aeiouœ' and symbol[1] in 'iuew':
        return {'group': 'diphthong', 'col': symbol[1]}
    return {'group': 'other'}


def layout(symbols: list[str]) -> dict:
    """Grid description consumed by app/runtime.js."""
    cells: dict = {}
    other, null = [], []
    for s in symbols:
        c = classify(s)
        if c['group'] in ('consonant', 'vowel'):
            cells.setdefault(c['group'], {}).setdefault(c['row'], {}).setdefault(c['col'], []).append(s)
        elif c['group'] == 'diphthong':
            cells.setdefault('diphthong', {}).setdefault(c['col'], []).append(s)
        elif c['group'] == 'null':
            null.append(s)
        else:
            other.append(s)
    return {
        'consonants': {'rows': MANNERS, 'cols': PLACES, 'cells': cells.get('consonant', {})},
        'vowels': {'rows': HEIGHTS, 'cols': BACKNESS, 'cells': cells.get('vowel', {})},
        'diphthongs': {'cols': [c for c in DIPHTHONG_ENDS if c[0] in cells.get('diphthong', {})],
                       'cells': cells.get('diphthong', {})},
        'null': null, 'null_label': NULL_LABEL,
        'other': other,
    }
