"""Behaviour of the sound-change executor against Eldamo's documented notation."""
import unittest

from tests.support import ROOT  # noqa: F401  (sets sys.path)
from shared.interpreter import Unsupported, apply, check, comparable, parse_pattern

# (from, to, word, expected) — examples follow general/phonetic-descriptions.html
REPRODUCED = [
    ('m-', 'n-', 'mara', 'nara'),                    # initial
    ('-m', '-n', 'aram', 'aran'),                    # final
    ('-m-', '-n-', 'ama', 'ana'),                    # medial
    ('m{ttʰ}', 'n{ttʰ}', 'amtʰa', 'antʰa'),           # set kept in place
    ('m{ttʰ}', 'm{ppʰ}', 'amta', 'ampa'),             # set mapped by position
    ('{ptk}ʰ', '{ɸθx}', 'apʰa', 'aɸa'),               # modifier applies to every set element
    ('VɣV', 'VøV', 'aɣa', 'aa'),                     # loss between vowels
    ('VɣC', 'V̄øC', 'aɣta', 'āta'),                   # compensatory lengthening
    ('øṇd-', 'and-', 'ṇdo', 'ando'),                 # explicit insertion
    ('ṇd-', 'and-', 'ṇdo', 'ando'),                  # ø omitted when unambiguous
    ('{ptk}ʰ{ptk}', '{ptk}{ptk}ʰ', 'apʰta', 'aptʰa'),  # aspiration moves
    ('{lr}₁{tk}₂', 'C₂C₁', 'alta', 'atla'),          # metathesis by index
    ('V₁Cøl', 'V₁CV₁l', 'akla', 'akala'),            # copied vowel
    ('ṃb-|ṇd-|ŋ̣g-', 'umb-|and-|iñg-', 'ṇdo', 'ando'),  # top-level alternatives
    ('-{mb|nd}-', '-{mm|nn}-', 'amba', 'amma'),      # multi-phoneme set elements
    ('Vk', 'Vg', 'akak', 'agag'),                    # every site at once
    ('Vk', 'Vg', 'a-ka', 'aga'),                     # morpheme boundary in the form
    ('θ', 's', 'aþa', 'asa'),                        # þ and θ are one sound
    ('-Să', '-Sø', 'amba', 'amb'),                   # syllable + explicitly short vowel
    ('-Sā', '-Să', 'eŋgwā', 'eŋgwa'),                # shortening, breve vs unmarked
    ('-Sĕ', '-Sø', '-ne', '-n'),                     # fragment: syllable starts before it
    ('-ĕCi', '-eiC', 'fœrmeni', 'fœrmein'),          # metathesis without indices
    ('CCC', 'CC', 'ampta', 'amta'),                  # which consonant vanished is chosen by the data
    ('V̄jV', 'VijV', 'ājo', 'aijo'),
    ('iŋn', 'īn', 'tiŋna', 'tīna'),                  # literal rewrite of unequal length
    ('C*ăC', 'C*āC', 'bad', 'bād'),                  # star: zero or more
    ('ˌau', 'o', 'feanaur', 'feanor'),               # stress mark ignored
    ('-ɣ-', '-ø-', 'laɣa', 'lā'),                    # aa written as ā
    ('d+d', 'zd', 'ad+da', 'azda'),                  # boundary inside the pattern
]


class Interpreter(unittest.TestCase):
    def test_documented_notation(self):
        for src, dst, word, expected in REPRODUCED:
            with self.subTest(rule=f'{src} > {dst}', word=word):
                self.assertEqual(check(src, dst, word, expected), 'reproduced')

    def test_no_silent_failure_on_unknown_notation(self):
        for src in ('a?', '(a)b', 'a/b'):
            with self.subTest(src=src):
                self.assertTrue(check(src, 'b', 'ab', 'bb').startswith('unsupported'))
                with self.assertRaises(Unsupported):
                    parse_pattern(src)

    def test_no_match_and_mismatch_are_distinct(self):
        self.assertEqual(check('m-', 'n-', 'ama', 'ana'), 'no_match')       # not initial
        self.assertEqual(check('m', 'n', 'ama', 'apa'), 'mismatch')          # applies, other result

    def test_breve_requires_short_vowel(self):
        self.assertEqual(check('-Să', '-Sø', 'ambā', 'amb'), 'no_match')

    def test_positions(self):
        self.assertEqual(apply('-m-', '-n-', 'mamam')['all_sites'], {'manam'})
        self.assertEqual(apply('m-', 'n-', 'mamam')['all_sites'], {'namam'})
        self.assertEqual(apply('-m', '-n', 'mamam')['all_sites'], {'maman'})

    def test_sound_law_keeps_shared_context(self):
        # neighbouring sites share the vowel between them
        self.assertEqual(check('VsV', 'VhV', 'asasa', 'ahaha'), 'reproduced')

    def test_dropped_member_is_determined(self):
        self.assertEqual(check('CCC', 'CC', 'ampta', 'amta'), 'reproduced')   # middle consonant
        self.assertEqual(check('CCC', 'CC', 'ampta', 'apta'), 'mismatch')
        self.assertEqual(check('-CC', '-C', 'kasp', 'kas'), 'reproduced')     # last consonant

    def test_stem_with_trailing_hyphen_ends_the_word(self):
        self.assertEqual(check('-ŭCCa', '-oCCa', 'dulθa-', 'dolθa-'), 'reproduced')
        self.assertEqual(check('m-', 'n-', '-ma', '-na'), 'no_match')         # suffix: not word-initial

    def test_boundary_patterns_need_marked_boundaries(self):
        self.assertTrue(check('Cŏ+C', 'Cø+C', 'uioloss', 'uiolss').startswith('unsupported'))

    def test_partial_application_is_reported_separately(self):
        self.assertEqual(check('Vk', 'Vg', 'akak', 'agak'), 'reproduced_partial')

    def test_comparison_form(self):
        self.assertEqual(comparable('a-ka'), comparable('aka'))
        self.assertEqual(comparable('laa'), comparable('lā'))
        self.assertEqual(comparable('ñal'), comparable('ŋal'))


if __name__ == '__main__':
    unittest.main()
