"""Tolkien's spelling of Quenya and Sindarin words -> Eldamo's phonetic notation.

Derivations in Eldamo end in phonetic forms (Quendi -> kwendi, nehta- ->
nexta-, Thû -> θū, rhaed -> r̥aed). Word formation at the latest stage starts
from dictionary forms, so they are converted the same way. The conversion is
checked against the attested pairs (tests/test_lexicon.py).
"""
from __future__ import annotations

import re
import unicodedata

ACUTE, CIRCUMFLEX, DIAERESIS, MACRON, BREVE = '\u0301', '\u0302', '\u0308', '\u0304', '\u0306'
SUPERSCRIPT = re.compile(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]')

QUENYA = [
    ('x', 'ks'), ('χ', 'x'), ('ph', 'f'), ('nqu', 'ŋkw'), ('ngw', 'ŋgw'), ('qu', 'kw'), ('q', 'kw'),
    ('nc', 'ŋk'), ('nk', 'ŋk'), ('ng', 'ŋg'), ('ñ', 'ŋ'),
    ('hy', 'j̊'), ('hw', 'w̥'), ('hl', 'l̥'), ('hr', 'r̥'), ('ht', 'xt'),
    ('c', 'k'), ('þ', 'θ'), ('th', 'θ'), ('y', 'j'),
]
SINDARIN = [
    ('ch', 'x'), ('th', 'θ'), ('dh', 'ð'), ('lh', 'l̥'), ('rh', 'r̥'), ('mh', 'ṽ'),
    ('hm', 'm̥'), ('hn', 'n̥'), ('wh', 'w̥'),
    ('nc', 'ŋk'), ('ng', 'ŋg'), ('ñ', 'ŋ'), ('c', 'k'), ('þ', 'θ'), ('k', 'k'),
]


# Eldamo writes primitive words (✶) in a spelling of its own, its derivations
# in phonetic notation (✶delya, start delja; ✶phayanāro, pʰajanāro). Most
# frequent correspondences between the two, from words that have both:
PRIMITIVE = [
    ('ı̯', 'j'), ('i̯', 'j'), ('u̯', 'w'), ('\u032f', ''),
    ('ph', 'pʰ'), ('th', 'tʰ'), ('kh', 'kʰ'), ('qu', 'kʷ'), ('q', 'kʷ'),
    ('ñ', 'ŋ'), ('ʒ', 'ɣ'), ('χ', 'x'), ('þ', 'θ'), ('đ', 'ð'), ('c', 'k'), ('y', 'j'),
]
VELAR_NASAL = re.compile(r'n(?=[kgxɣ])')


def primitive_phonetic(form: str) -> str:
    """A primitive form as Eldamo writes it -> its phonetic notation. Roots in
    capitals (DEL) are left as they are."""
    if not form or form.upper() == form:
        return form
    f = unicodedata.normalize('NFC', form)
    for a, b in PRIMITIVE:
        f = f.replace(a, b)
    return VELAR_NASAL.sub('ŋ', f)


def _long(text: str) -> str:
    """Acute and circumflex mark long vowels; the diaeresis only shows a
    vowel is pronounced (ë); a breve (explicit shortness) is dropped."""
    out = []
    for ch in unicodedata.normalize('NFD', text):
        if ch in (ACUTE, CIRCUMFLEX):
            if not out or out[-1] != MACRON:
                out.append(MACRON)
        elif ch in (DIAERESIS, BREVE):
            continue
        else:
            out.append(ch)
    return unicodedata.normalize('NFC', ''.join(out))


def clean(form: str) -> str:
    """Drop homonym numbers and optional parts: riel(lë) -> riel, ur(u) -> ur."""
    f = SUPERSCRIPT.sub('', form.strip())
    return re.sub(r'\([^)]*\)', '', f).strip()


def to_phonetic(form: str, family: str) -> str:
    """family: 'quenya' or 'sindarin'."""
    f = _long(clean(form)).lower()
    if family == 'quenya':
        if f.startswith('ñ'):
            f = 'n' + f[1:]      # initial [ŋ] became [n] (Q.)
        for a, b in QUENYA:
            f = f.replace(a, b)
        return f
    for a, b in SINDARIN:
        f = f.replace(a, b)
    f = re.sub(r'(?<=.)f', 'v', f)                   # f is [v] except initially: ylf -> ylv, drafn -> dravn
    f = re.sub(r'^ph', 'f', f)
    f = re.sub(r'ph$', 'f', f)
    f = f.replace('ph', 'ff')                        # medial ph is long: aphad- -> affad-
    f = re.sub(r'ŋg$', 'ŋ', f)                       # final ng is [ŋ]
    f = re.sub(r'(?<=[aā])w$', 'u', f)               # final aw is a diphthong: maw -> mau (raew, tîw keep w)
    f = re.sub(r'(?<=[^aeiouyāēīōūȳ])w$', 'u', f)    # final w after a consonant is a vowel: delw -> delu
    f = re.sub(r'^i(?=[aeouāēōū])', 'j', f)          # initial i before a vowel: iolf -> jolv
    return f
