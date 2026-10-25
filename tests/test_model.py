"""The extracted model against the Eldamo XML it comes from."""
import unittest
from collections import Counter

from tests.support import branches
from shared.languages import BRANCHES, languages
from shared.model import index
from shared.source import root


class Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()
        cls.ix = index()

    def test_source_checksum_and_version(self):
        self.assertEqual(root().tag, 'word-data')

    def test_every_rule_page_of_branch_languages_is_used_or_excluded(self):
        for b in BRANCHES:
            langs = languages(b)
            expected = {w.get('page-id') for w in self.ix.rule_words if w.get('l') in langs}
            got = {r['id'] for r in self.data[b]['rules']} | {r['rule'] for r in self.data[b]['summary']['excluded_rules']}
            self.assertEqual(expected, got, b)

    def test_rule_language_matches_branch_and_marker(self):
        for b in BRANCHES:
            langs = languages(b)
            for r in self.data[b]['rules']:
                xml = self.ix.by_id[r['id']]
                self.assertEqual(xml.get('l'), r['lang'])
                self.assertIn(r['lang'], langs)
                self.assertEqual(langs[r['lang']]['marker'], r['marker'])

    def test_deleted_rules_are_excluded(self):
        for b in BRANCHES:
            for r in self.data[b]['rules']:
                self.assertFalse((r['mark'] or '').startswith('-'), r['id'])
            for r in self.data[b]['summary']['excluded_rules']:
                self.assertTrue(self.ix.by_id[r['rule']].get('mark', '').startswith('-'))

    def test_each_xml_pair_appears_exactly_once(self):
        for b in BRANCHES:
            ids = Counter(p['id'] for p in self.data[b]['pairs'])
            self.assertEqual(max(ids.values()), 1)
            for r in self.data[b]['rules']:
                xml_pairs = [(c.get('from'), c.get('rule')) for c in self.ix.by_id[r['id']].findall('rule')]
                ours = [(p['from'], p['to']) for p in self.data[b]['pairs'] if p['rule'] == r['id']]
                self.assertEqual(xml_pairs, ours, r['id'])

    def test_order_and_before_come_from_xml(self):
        for b in BRANCHES:
            for r in self.data[b]['rules']:
                xml = self.ix.by_id[r['id']]
                self.assertEqual(r['order'], int(xml.get('order')) if xml.get('order') else None)
                self.assertEqual([x['name'] for x in r['before']], [x.get('v') for x in xml.findall('before')])

    def test_lower_order_means_earlier(self):
        # The chronology check assumes a smaller @order is an earlier rule;
        # Eldamo's explicit <before> links must agree with that.
        for b in BRANCHES:
            rules = {r['id']: r for r in self.data[b]['rules']}
            checked = 0
            for r in rules.values():
                for x in r['before']:
                    t = rules.get(x['rule'])
                    if t and r['lang'] == t['lang'] and r['order'] is not None and t['order'] is not None:
                        self.assertLess(r['order'], t['order'], (r['name'], t['name']))
                        checked += 1
            self.assertGreater(checked, 50, b)

    def test_derivation_steps_reference_real_pairs(self):
        for b in BRANCHES:
            for d in self.data[b]['derivations']:
                for s in d['steps']:
                    if s['pair']:
                        page, k = s['pair'].rsplit('.', 1)
                        c = self.ix.by_id[page].findall('rule')[int(k) - 1]
                        self.assertEqual((c.get('l'), c.get('from'), c.get('rule')), (s['lang'], s['from'], s['to']))

    def test_formulas_replay_attested_steps(self):
        # Guards against silent breakage of the interpreter (e.g. an exception
        # swallowed on an older Python): most attested steps must replay.
        for b in BRANCHES:
            s = self.data[b]['summary']
            self.assertGreater(s['reproduction_rate'], 0.9, b)
            self.assertGreater(s['step_status'].get('reproduced', 0), 1000, b)

    def test_example_counts_match_derivations(self):
        for b in BRANCHES:
            counted = Counter()
            for d in self.data[b]['derivations']:
                if not d['deleted']:
                    counted.update(s['pair'] for s in d['steps'] if s['pair'])
            for p in self.data[b]['pairs']:
                self.assertEqual(p['examples'], counted.get(p['id'], 0), p['id'])


if __name__ == '__main__':
    unittest.main()
