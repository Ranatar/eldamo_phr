"""Build the offline atlas (app/index.html) and the corpus browser (app/corpus.html)."""
from __future__ import annotations

import json
from collections import defaultdict

from . import affixes, reconstruct
from . import junctions as junction_table
from .formula import NULL
from .graph import GRADES
from .io import embed_json, write_text
from .ipa import layout
from .sequencer import Sequencer
from .source import ROOT, meta

APP = ROOT / 'app'


def _defaults(data: dict) -> dict:
    symbols = {p['symbol'] for p in data['phonemes']}
    best = None
    for c in data['chains']:
        if c['era'] != 'late' or c['grade'] != 'A':
            continue
        a, b = c['states'][0], c['states'][-1]
        if a in symbols and b in symbols and NULL not in (a, b) and (best is None or c['attested_count'] > best['attested_count']):
            best = c
    if best:
        return {'from': best['states'][0], 'to': best['states'][-1]}
    first = data['edges'][0]
    return {'from': first['a'], 'to': first['b']}


def payload(branches: dict) -> dict:
    out = {'eldamo_version': meta()['eldamo_version'], 'grades': GRADES, 'branches': {}}
    for name, data in branches.items():
        m = data['meta']
        rules = {r['id']: {
            'l': r['lang'], 'n': r['name'], 'o': r['order'],
            'f': [r['formula']['from'], r['formula']['to']] if r['formula'] else None,
            'b': [b['rule'] for b in r['before'] if b['rule']],
        } for r in data['rules']}
        pairs = {p['id']: {
            'r': p['rule'], 'l': p['lang'], 'f': p['from'], 't': p['to'], 'k': p['kind'],
            'a': p['a'], 'b': p['b'], 'p': p['position'], 'c': p['cards'], 's': p['segments'],
            'e': p['examples'], 'ok': p['reproduced'] + p['partial'],
        } for p in data['pairs']}
        edges = [{
            'id': e['id'], 'era': e['era'], 'st': e['stage'], 'm': e['marker'], 'a': e['a'], 'b': e['b'],
            'p': e['position'], 'pr': e['pairs'], 'r': e['rules'], 'c': e['conditional'],
            'cx': e['context'], 'ex': e['exceptions'], 'e': e['examples'], 'ok': e['reproduced'],
        } for e in data['edges']]
        chains = [{
            'id': c['id'], 'era': c['era'], 's': c['states'], 'g': c['grade'], 'steps': c['steps'],
            't': c['transitions'], 'n': c['attested_count'], 'd': c['attested_in'], 'v': c['variants'],
        } for c in data['chains']]
        ordered = sorted(data['derivations'], key=lambda d: (-len(d['steps']), d['word_form'] or '', d['id']))
        derivs = [{
            'id': d['id'], 'w': d['word'], 'wl': d['word_lang'], 'wf': d['word_form'], 'g': d['gloss'],
            'f': d['form'], 'src': d['source'], 'dsrc': d['derivation_source'], 'st': d['start'],
            'del': d['deleted'], 'bw': d['branch_word'],
            'steps': [[s['pair'], s['lang'], s['from'], s['to'], s['after'], s['status'].split(':')[0]] for s in d['steps']],
        } for d in ordered]
        symbols = [p['symbol'] for p in data['phonemes']]
        s = data['summary']
        out['branches'][name] = {
            'title': m['title'], 'path': m['path'], 'languages': m['languages'], 'language_names': m['language_names'],
            'phonemes': symbols, 'grid': layout(symbols), 'defaults': _defaults(data),
            'stats': {'rules': s['rules'], 'derivations': sum(1 for d in data['derivations'] if d['branch_word'] and not d['deleted']),
                      'edges': s['edges'], 'chains': s['chains']['chains'], 'grades': s['chains']['grades'],
                      'reproduction_rate': s['reproduction_rate']},
            'rules': rules, 'pairs': pairs, 'edges': edges, 'chains': chains, 'derivs': derivs,
        }
    return out


LEXICON_FIELDS = ('id', 'lang', 'form', 'gloss', 'speech', 'mark', 'neo', 'stems', 'starts', 'stages', 'written_origins',
                  'proto_forms')


def _key(parts) -> str:
    """Python tuple key -> the JSON string app/wordform.js builds (keyOf)."""
    return json.dumps(list(parts), ensure_ascii=False, separators=(',', ':'))


def wordform_payload(name: str, data: dict) -> dict:
    """What app/wordform.js needs: rules in sequence order, a trimmed lexicon,
    the junction table and the backform correspondences of the branch."""
    seq = Sequencer(data)
    final = max((l for l in data['meta']['languages'] if l['era'] == 'late'), key=lambda l: l['stage'])['code']
    rows = data['junctions']['cases']
    table = junction_table.learn(rows)
    analogues = defaultdict(list)
    for r in rows:
        if len(analogues[_key(r['jkey'])]) < 12:
            analogues[_key(r['jkey'])].append([r['form'], list(r['junction'])])
    bf = seq.backform_table(final)
    lexicon = []
    for e in data['lexicon']:
        if e['speech'] == 'root':
            continue
        x = {k: e[k] for k in LEXICON_FIELDS if e.get(k)}
        if x.get('starts'):
            x.pop('written_origins', None)
        if len(x.get('gloss', '')) > 80:
            x['gloss'] = x['gloss'][:77] + '…'
        if e.get('elements'):
            x['elements'] = [el.get('id') for el in e['elements']]
        if e.get('links'):
            x['links'] = {tag: [l['id'] for l in ls] for tag, ls in e['links'].items()}
        if e.get('roots'):
            x['roots'] = [r['form'] for r in e['roots']]
        lexicon.append(x)
    return {
        'languages': data['meta']['languages'],
        'rules': seq.export(),
        'lexicon': lexicon,
        'junctions': {
            'junction': {_key(k): [[list(op), n] for op, n in c.items()] for k, c in table['junction'].items()},
            'ending': {_key(k): [[list(op), n] for op, n in c.items()] for k, c in table['ending'].items()},
            'short': {k: [[s, n] for s, n in c.items()] for k, c in table['short'].items()},
            'smoothing': junction_table.SMOOTHING,
        },
        'analogues': dict(analogues),
        'backform': {_key(k): c.most_common() for k, c in bf.items()},
        'affixes': affixes.model_json(data['affixes']['cases']),
        'recon': reconstruct.export(data),
        'final': final,
    }


SCRIPTS = {                     # template marker -> file in app/
    '@@ROUTER@@': 'router.js',
    '@@WORDFORM@@': 'wordform.js',
    '@@WORD_UI@@': 'word_ui.js',
    '@@WORDFORM_UI@@': 'wordform_ui.js',
    '@@RECON_UI@@': 'reconstruct_ui.js',
    '@@RUNTIME@@': 'runtime.js',
}


def build_index(branches: dict) -> str:
    template = (APP / 'template.html').read_text(encoding='utf-8')
    markers = ('@@STYLES@@', '@@DATA@@', '@@WORDFORM_DATA@@', '@@ELDAMO_VERSION@@', *SCRIPTS)
    for marker in markers:
        if template.count(marker) != 1:
            raise SystemExit(f'app/template.html must contain {marker} exactly once')
    html = template.replace('@@STYLES@@', (APP / 'styles.css').read_text(encoding='utf-8').rstrip('\n'))
    for marker, name in SCRIPTS.items():
        html = html.replace(marker, (APP / name).read_text(encoding='utf-8').rstrip('\n'))
    html = html.replace('@@ELDAMO_VERSION@@', meta()['eldamo_version'])
    html = html.replace('@@WORDFORM_DATA@@', embed_json({b: wordform_payload(b, d) for b, d in branches.items()}))
    html = html.replace('@@DATA@@', embed_json(payload(branches)))
    return html


def write_app(branches: dict) -> None:
    write_text(APP / 'index.html', build_index(branches))
