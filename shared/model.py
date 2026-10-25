"""Build the canonical model of one branch directly from eldamo-data.xml.

Everything comes from the Eldamo data model:

* rules     -- <word speech="phonetic-rule"> pages of the branch languages:
               name, general formula (@from > @rule), @order, <before>, notes;
               rules Tolkien deleted (mark="-") are excluded;
* pairs     -- the <rule l from rule> sub-formulas of each rule page;
* derivations -- every <deriv> with <rule-example> steps that touches a
               branch language: Paul Strack's attested sequence of rule
               applications with every intermediate form;
* phonemes  -- <word speech="phoneme"> cards of the branch languages and the
               rule pairs each card lists.

Each attested step is replayed by shared.interpreter, so every pair carries
counts of how many of its examples the formula reproduces.
"""
from __future__ import annotations

import html
import re
from collections import Counter, defaultdict

from . import interpreter
from .formula import classify_pair, segments
from .languages import BRANCHES, languages
from .source import root, source_label, source_url, word_url

RULE_SPEECH = 'phonetic-rule'


def deleted_mark(mark: str | None) -> bool:
    return bool(mark) and mark.startswith('-')


def notes_text(el) -> str:
    """Eldamo notes are HTML with <a l v/> cross references; reduce them to text."""
    if el is None or not (el.text or '').strip():
        return ''
    s = el.text
    s = re.sub(r'<a\b[^>]*\bv="([^"]*)"[^>]*/>', r'\1', s)
    s = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', s, flags=re.S)
    s = re.sub(r'</(p|li|ul|ol|blockquote)>|<br\s*/?>', '\n', s)
    s = re.sub(r'<li>', '• ', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    return s.strip()


class Index:
    """Lookups over the whole XML shared by both branches."""

    def __init__(self):
        r = root()
        self.parent = {c: p for p in r.iter() for c in p}
        self.rule_words = [w for w in r.iter('word') if w.get('speech') == RULE_SPEECH]
        self.by_name = {(w.get('l'), w.get('v')): w.get('page-id') for w in self.rule_words}
        self.by_id = {w.get('page-id'): w for w in self.rule_words}
        self.pair_key = {}
        for w in self.rule_words:
            for k, c in enumerate(w.findall('rule')):
                # two triples repeat on one page in 0.8.13; steps link to the first
                self.pair_key.setdefault((c.get('l'), c.get('from'), c.get('rule')), (w.get('page-id'), k))
        self.deleted_rules = {w.get('page-id') for w in self.rule_words if deleted_mark(w.get('mark'))}
        self.derivs = [d for d in r.iter('deriv') if d.find('rule-example') is not None]
        self.phoneme_words = [w for w in r.iter('word') if w.get('speech') == 'phoneme']
        self.language_names = {l.get('id'): l.get('name') for l in r.iter('language')}

    def owner_word(self, el):
        while el is not None and el.tag != 'word':
            el = self.parent.get(el)
        return el

    def rule_parent(self, w):
        p = self.parent.get(w)
        return p.get('page-id') if p is not None and p.tag == 'word' and p.get('speech') == RULE_SPEECH else None


_INDEX = None


def index() -> Index:
    global _INDEX
    if _INDEX is None:
        _INDEX = Index()
    return _INDEX


def pair_id(page_id: str, k: int) -> str:
    return f'{page_id}.{k + 1}'


def build(branch: str) -> dict:
    ix = index()
    langs = languages(branch)

    # ---- phoneme inventory ------------------------------------------------
    inventory: dict[str, dict] = {}
    card_pairs = defaultdict(set)   # pair id -> phoneme symbols listing it
    for w in ix.phoneme_words:
        if w.get('l') not in langs or deleted_mark(w.get('mark')):
            continue
        sym = w.get('v', '').strip('[]')
        rec = inventory.setdefault(sym, {'symbol': sym, 'languages': [], 'cards': []})
        if w.get('l') not in rec['languages']:
            rec['languages'].append(w.get('l'))
        rec['cards'].append(word_url(w.get('page-id')))
        for ref in w.iter('ref'):
            key = (ref.get('rl'), ref.get('from'), ref.get('rule'))
            if key in ix.pair_key:
                card_pairs[pair_id(*ix.pair_key[key])].add(sym)
    symbols = sorted(inventory)

    # ---- rules and pairs --------------------------------------------------
    rules, pairs, excluded = [], [], []
    rule_ids = set()
    for w in ix.rule_words:
        lang = w.get('l')
        if lang not in langs:
            continue
        pid = w.get('page-id')
        if deleted_mark(w.get('mark')):
            excluded.append({'rule': pid, 'lang': lang, 'name': w.get('v'), 'reason': 'deleted by Tolkien (mark "-")'})
            continue
        L = langs[lang]
        order = w.get('order')
        rule = {
            'id': pid,
            'lang': lang,
            'marker': L['marker'],
            'era': L['era'],
            'stage': L['stage'],
            'name': w.get('v'),
            'url': word_url(pid),
            'order': int(order) if order else None,
            'formula': {'from': w.get('from'), 'to': w.get('rule')} if w.get('from') is not None else None,
            'mark': w.get('mark') or '',
            'variant_of': ix.rule_parent(w),
            'before': [],
            'after': [],
            'pairs': [],
            'notes': notes_text(w.find('notes')),
        }
        for b in w.findall('before'):
            target = ix.by_name.get((b.get('l'), b.get('v')))
            rule['before'].append({'rule': target, 'lang': b.get('l'), 'name': b.get('v'),
                                   'evidence': [e.get('v') for e in b.findall('order-example')]})
        identity = []
        for k, c in enumerate(w.findall('rule')):
            p_id = pair_id(pid, k)
            info = classify_pair(c.get('from'), c.get('rule'))
            # a sub-formula carries its own language (an aq pair may sit on a p page)
            PL = langs.get(c.get('l'))
            pair = {
                'id': p_id, 'rule': pid, 'lang': c.get('l'),
                'era': (PL or L)['era'], 'stage': (PL or L)['stage'], 'marker': (PL or L)['marker'],
                'in_branch': PL is not None,
                'from': c.get('from'), 'to': c.get('rule'), **info,
                'cards': sorted(card_pairs.get(p_id, ())),
                'segments': sorted(set(segments(info['a'], symbols)) | set(segments(info['b'], symbols))),
            }
            if info['kind'] == 'identity':
                identity.append(f"{c.get('from')} > {c.get('rule')}")
            rule['pairs'].append(p_id)
            pairs.append(pair)
        rule['exceptions'] = identity
        rules.append(rule)
        rule_ids.add(pid)

    by_rule = {r['id']: r for r in rules}
    for r in rules:
        for b in r['before']:
            if b['rule'] in by_rule:
                by_rule[b['rule']]['after'].append(r['id'])
    pair_by_id = {p['id']: p for p in pairs}

    # ---- derivations ------------------------------------------------------
    derivations = []
    stats = Counter()
    for d in ix.derivs:
        examples = d.findall('rule-example')
        if not any(e.get('l') in langs for e in examples):
            continue
        ref = ix.parent.get(d)
        owner = ix.owner_word(d)
        marks = [x.get('mark') for x in (d, ref, owner) if x is not None]
        start = d.find('rule-start')
        prev = start.get('stage') if start is not None else d.get('v')
        steps = []
        for e in examples:
            key = (e.get('l'), e.get('from'), e.get('rule'))
            loc = ix.pair_key.get(key)
            p_id = pair_id(*loc) if loc else None
            step = {'lang': e.get('l'), 'from': e.get('from'), 'to': e.get('rule'),
                    'before': prev, 'after': e.get('stage'), 'pair': p_id}
            if e.get('rule') == '?':
                step['status'] = 'unknown_rule'
            elif loc is None:
                step['status'] = 'unmatched_formula'
            elif loc[0] in ix.deleted_rules:
                step['status'] = 'deleted_rule'
            elif e.get('from') == e.get('rule'):
                step['status'] = 'identity'   # exception of a rule: the form keeps the sound
            else:
                step['status'] = interpreter.check(e.get('from') or '', e.get('rule'), prev or '', e.get('stage') or '')
            if p_id is not None and p_id not in pair_by_id:
                step['outside_branch'] = True
            stats[step['status'].split(':')[0]] += 1
            steps.append(step)
            prev = e.get('stage')
        derivations.append({
            'id': f'D{len(derivations) + 1}',
            'word': owner.get('page-id') if owner is not None else None,
            'word_lang': owner.get('l') if owner is not None else None,
            'word_form': owner.get('v') if owner is not None else None,
            'gloss': (owner.get('gloss') if owner is not None else None) or (ref.get('gloss') if ref is not None else None) or '',
            'form': ref.get('v') if ref is not None else None,
            'source': ref.get('source') if ref is not None else None,
            'derived_from': d.get('v'),
            'derivation_source': d.get('source'),
            'start': start.get('stage') if start is not None else d.get('v'),
            'deleted': any(deleted_mark(m) for m in marks),
            # a word of this branch: its language belongs to the branch, or one of its
            # steps is in a post-primitive branch language (primitive steps are shared)
            'branch_word': (owner is not None and owner.get('l') in langs)
            or any(langs.get(s['lang'], {}).get('stage', 0) > 0 for s in steps),
            'steps': steps,
        })

    # ---- per-pair evidence ------------------------------------------------
    for p in pairs:
        p.update({'examples': 0, 'deleted_examples': 0, 'reproduced': 0, 'partial': 0,
                  'mismatch': 0, 'no_match': 0, 'unsupported': 0})
    for der in derivations:
        for s in der['steps']:
            p = pair_by_id.get(s['pair'])
            if p is None:
                continue
            if der['deleted']:
                p['deleted_examples'] += 1
                continue
            p['examples'] += 1
            st = s['status']
            key = {'reproduced': 'reproduced', 'reproduced_partial': 'partial', 'mismatch': 'mismatch',
                   'no_match': 'no_match'}.get(st, 'unsupported' if st.startswith('unsupported') else None)
            if key:
                p[key] += 1

    return {
        'branch': branch,
        'title': BRANCHES[branch]['title'],
        'path': BRANCHES[branch]['path'],
        'languages': list(langs.values()),
        'phonemes': [inventory[s] for s in symbols],
        'rules': rules,
        'pairs': pairs,
        'derivations': derivations,
        'excluded_rules': excluded,
        'language_names': {code: ix.language_names[code] for code in sorted(
            {s['lang'] for d in derivations for s in d['steps']} | {d['word_lang'] for d in derivations if d['word_lang']})
            if code in ix.language_names},
        'step_status': dict(sorted(stats.items())),
    }


def source_ref(source: str | None) -> dict | None:
    if not source:
        return None
    return {'label': source_label(source), 'anchor': source, 'url': source_url(source)}
