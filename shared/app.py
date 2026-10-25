"""Build the offline atlas (app/index.html) and the corpus browser (app/corpus.html)."""
from __future__ import annotations

from .formula import NULL
from .graph import GRADES
from .io import embed_json, write_text
from .ipa import layout
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


def build_index(branches: dict) -> str:
    template = (APP / 'template.html').read_text(encoding='utf-8')
    styles = (APP / 'styles.css').read_text(encoding='utf-8')
    runtime = (APP / 'runtime.js').read_text(encoding='utf-8')
    for marker in ('@@STYLES@@', '@@DATA@@', '@@RUNTIME@@'):
        if template.count(marker) != 1:
            raise SystemExit(f'app/template.html must contain {marker} exactly once')
    html = template.replace('@@STYLES@@', styles.rstrip('\n'))
    html = html.replace('@@RUNTIME@@', runtime.rstrip('\n'))
    html = html.replace('@@DATA@@', embed_json(payload(branches)))
    return html


def write_app(branches: dict) -> None:
    write_text(APP / 'index.html', build_index(branches))
