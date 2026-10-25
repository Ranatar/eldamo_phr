"""Graph edges and chains: literal, chronological, honestly graded."""
import unittest

from tests.support import branches
from shared.formula import NULL
from shared.graph import Chronology, GRADES, witness_steps
from shared.languages import BRANCHES, languages
import unicodedata


class Graph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = branches()

    def test_edges_come_from_literal_pairs(self):
        for b in BRANCHES:
            pairs = {p['id']: p for p in self.data[b]['pairs']}
            for e in self.data[b]['edges']:
                self.assertNotEqual(e['a'], e['b'])
                self.assertNotEqual(e['a'], NULL)
                for pid in e['pairs']:
                    p = pairs[pid]
                    self.assertIn(p['kind'], ('literal', 'loss'))
                    self.assertEqual((p['a'], p['b'], p['position'], p['era']), (e['a'], e['b'], e['position'], e['era']))

    def test_every_literal_pair_is_an_edge(self):
        for b in BRANCHES:
            in_edges = {pid for e in self.data[b]['edges'] for pid in e['pairs']}
            for p in self.data[b]['pairs']:
                expected = p['kind'] in ('literal', 'loss') and p['in_branch']
                self.assertEqual(expected, p['id'] in in_edges, p['id'])

    def test_pairs_carry_their_own_language(self):
        # an aq sub-formula on a primitive page is AQ., and stays out of the Sindarin graph
        for b in BRANCHES:
            langs = languages(b)
            for p in self.data[b]['pairs']:
                if p['in_branch']:
                    self.assertEqual((p['stage'], p['marker']), (langs[p['lang']]['stage'], langs[p['lang']]['marker']))
            for e in self.data[b]['edges']:
                self.assertIn(e['lang'], langs)
                self.assertEqual(e['stage'], langs[e['lang']]['stage'])

    def test_graph_nodes_have_no_stress_or_breve(self):
        for b in BRANCHES:
            for e in self.data[b]['edges']:
                for node in (e['a'], e['b']):
                    nfd = unicodedata.normalize('NFD', node)
                    self.assertFalse(set('ˈˌ\u0301\u0306') & set(nfd), node)

    def test_stress_rule_joins_the_graph(self):
        # S. ˌau > o used to be a separate node "ˌau": ǭ > au > o was missing
        ids = {c['id']: c for c in self.data['sindarin']['chains']}
        self.assertIn('late:ǭ>au>o', ids)
        e = [e for e in self.data['sindarin']['edges'] if e['a'] == 'au' and e['b'] == 'o' and e['era'] == 'late']
        self.assertTrue(e and all(x['conditional'] for x in e))

    def test_conditions_are_kept(self):
        # AQ. voiced stops became spirants *except after nasals*: b > β keeps its exceptions
        edges = [e for e in self.data['quenya']['edges'] if e['marker'] == 'AQ.' and e['a'] == 'b' and e['b'] == 'β']
        self.assertTrue(edges)
        self.assertTrue(all(e['conditional'] and 'mb > mb' in e['exceptions'] for e in edges))

    def test_chains_follow_chronology(self):
        for b in BRANCHES:
            model = {'rules': self.data[b]['rules']}
            chrono = Chronology(model)
            edges = {e['id']: e for e in self.data[b]['edges']}
            for c in self.data[b]['chains']:
                path = [edges[i] for i in c['steps']]
                self.assertEqual(len(c['states']), len(path) + 1)
                self.assertEqual(c['states'], [path[0]['a']] + [e['b'] for e in path])
                for e1, e2, t in zip(path, path[1:], c['transitions']):
                    self.assertEqual(chrono.transition(e1, e2), t)
                    self.assertNotEqual(t, 'contradicted')
                    self.assertEqual(e1['era'], e2['era'])

    def test_grades(self):
        for b in BRANCHES:
            edges = {e['id']: e for e in self.data[b]['edges']}
            derivations = self.data[b]['derivations']
            index = {d['id']: i for i, d in enumerate(derivations)}
            witness = {(di, si) for occ in witness_steps(derivations).values() for di, si in occ}
            for c in self.data[b]['chains']:
                self.assertIn(c['grade'], GRADES)
                path = [edges[i] for i in c['steps']]
                if c['grade'] == 'A':
                    self.assertTrue(c['attested_in'])
                    for did in c['attested_in']:  # every listed witness, not only the first
                        di = index[did]
                        d = derivations[di]
                        self.assertFalse(d['deleted'])
                        pos = -1
                        for e in path:  # reproduced, form-changing steps in this order
                            later = [i for i, s in enumerate(d['steps'])
                                     if s['pair'] in e['pairs'] and i > pos and (di, i) in witness]
                            self.assertTrue(later, (c['id'], did))
                            pos = later[0]
                else:
                    self.assertEqual(c['attested_count'], 0)
                if c['grade'] in ('B', 'C'):
                    self.assertTrue(all(e['reproduced'] > 0 for e in path))
                if c['grade'] == 'B':
                    self.assertTrue(all(t in ('stage', 'ordered') for t in c['transitions']))
                if c['grade'] == 'D':
                    self.assertTrue(any(e['reproduced'] == 0 for e in path))

    def test_failed_steps_are_not_witnesses(self):
        # quenya sd > zd > st was graded A on a step nizdo → nizdo the formula does not reproduce
        ids = {c['id']: c for c in self.data['quenya']['chains']}
        self.assertNotEqual(ids['late:sd>zd>st']['grade'], 'A')

    def test_chain_ids_unique(self):
        for b in BRANCHES:
            ids = [c['id'] for c in self.data[b]['chains']]
            self.assertEqual(len(ids), len(set(ids)))


if __name__ == '__main__':
    unittest.main()
