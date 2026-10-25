"""Classification of Eldamo rule formulas for the sound graph."""
from __future__ import annotations

import unicodedata

from .interpreter import ACUTE, canonical, nfc, phonemes, position_of

STRESS_MARKS = ('ˈ', 'ˌ', ACUTE)

NULL = 'ø'  # Eldamo's sign for a vanished (or inserted) sound
# Characters that make a side a pattern rather than a literal sound sequence.
PATTERN_CHARS = set('{}|()[]/_+*?=<>⁺⁻ ') | set('₁₂₃₄₅₆₇₈₉0123456789')


def stressed(text: str | None) -> bool:
    """Does the formula condition the change on stress (ˈ, ˌ or an acute accent)?"""
    return bool(text) and any(m in unicodedata.normalize('NFD', text) for m in STRESS_MARKS)


def sound_name(core: str) -> str:
    """Graph node for a literal: stress marks and breves (explicit shortness) removed,
    notational variants unified (þ = θ, ñ = ŋ), so ˌau and au are one node."""
    core = core.replace('ˈ', '').replace('ˌ', '')
    return nfc(''.join(canonical(p) for p in phonemes(core)))


def literal_side(text: str | None):
    """Return (value, position) for a literal side, or (None, position) for a pattern.

    A side consisting only of ø is the empty sound and is returned as NULL.
    """
    if text is None:
        return None, 'any'
    core, position = position_of(text)
    core = nfc(core)
    if core == 'ø':
        return NULL, position
    if not core or 'ø' in core:
        return None, position
    if any(ch in PATTERN_CHARS for ch in core):
        return None, position
    if any(ch.isupper() for ch in unicodedata.normalize('NFD', core)):
        return None, position  # V, C, X, S and other classes
    return sound_name(core), position


def classify_pair(src: str, dst: str) -> dict:
    """Describe one <rule from=... rule=...> pair."""
    a, pa = literal_side(src)
    b, pb = literal_side(dst)
    if a is not None and b is not None and pa == pb:
        if a == b:
            kind = 'identity'
        elif a == NULL:
            kind = 'insertion'
        elif b == NULL:
            kind = 'loss'
        else:
            kind = 'literal'
        return {'kind': kind, 'a': a, 'b': b, 'position': pa, 'stress': stressed(src) or stressed(dst)}
    return {'kind': 'contextual', 'a': None, 'b': None, 'position': pa if pa == pb else 'mixed',
            'stress': stressed(src) or stressed(dst)}


def segments(value: str, inventory: list[str]) -> list[str]:
    """Split a literal sequence into inventory phonemes, longest match first."""
    if value in (None, NULL):
        return []
    inv = sorted(set(inventory), key=len, reverse=True)
    out, i, s = [], 0, nfc(value)
    while i < len(s):
        for p in inv:
            if p and s.startswith(p, i):
                out.append(p)
                i += len(p)
                break
        else:
            ph = phonemes(s[i:])[0]
            out.append(ph)
            i += len(ph)
    return out
