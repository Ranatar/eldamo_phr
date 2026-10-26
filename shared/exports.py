"""Exports: one canonical JSON, a GraphML sound graph and the corpus browser."""
from __future__ import annotations

from xml.sax.saxutils import escape, quoteattr

from .graph import GRADES
from .io import dumps, embed_json, write_text
from .languages import ERAS
from .pipeline import DATA_FILES
from .source import ROOT, meta

EXPORTS = ROOT / 'exports'


def canonical(branches: dict) -> dict:
    m = meta()
    return {
        'format': 'eldamo-phonetic-atlas/2',
        'source': {k: m[k] for k in ('eldamo_version', 'xml_sha256', 'upstream')},
        'grades': GRADES,
        'branches': {b: {'title': d['meta']['title'], 'path': d['meta']['path'], 'languages': d['meta']['languages'],
                         **{k: d[k] for k in DATA_FILES}} for b, d in branches.items()},
    }


def graphml(branches: dict) -> str:
    keys = [('n', 'node', 'sound', 'string'), ('n', 'node', 'branch', 'string'), ('n', 'node', 'era', 'string'),
            ('e', 'edge', 'marker', 'string'), ('e', 'edge', 'stage', 'int'), ('e', 'edge', 'position', 'string'),
            ('e', 'edge', 'rules', 'string'), ('e', 'edge', 'rule_names', 'string'), ('e', 'edge', 'conditional', 'boolean'),
            ('e', 'edge', 'context', 'string'), ('e', 'edge', 'exceptions', 'string'), ('e', 'edge', 'examples', 'int'),
            ('e', 'edge', 'reproduced', 'int')]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
           f'  <!-- Eldamo {meta()["eldamo_version"]} © Paul Strack, CC BY 4.0; sound graph built by eldamo_phr -->']
    for prefix, domain, name, typ in keys:
        out.append(f'  <key id="{prefix}_{name}" for="{domain}" attr.name="{name}" attr.type="{typ}"/>')
    for b, d in branches.items():
        for era in ERAS:
            out.append(f'  <graph id="{b}-{era}" edgedefault="directed">')
            edges = [e for e in d['edges'] if e['era'] == era]
            nodes = sorted({e['a'] for e in edges} | {e['b'] for e in edges})
            nid = {s: f'{b}-{era}-n{i}' for i, s in enumerate(nodes)}
            for s in nodes:
                out.append(f'    <node id="{nid[s]}"><data key="n_sound">{escape(s)}</data>'
                           f'<data key="n_branch">{b}</data><data key="n_era">{era}</data></node>')
            for e in edges:
                vals = {'marker': e['marker'], 'stage': e['stage'], 'position': e['position'],
                        'rules': ' '.join(e['rules']), 'rule_names': ' | '.join(e['names']),
                        'conditional': str(e['conditional']).lower(), 'context': ' | '.join(e['context']),
                        'exceptions': ' | '.join(e['exceptions']), 'examples': e['examples'], 'reproduced': e['reproduced']}
                data = ''.join(f'<data key="e_{k}">{escape(str(v))}</data>' for k, v in vals.items())
                out.append(f'    <edge id={quoteattr(b + "-" + e["id"])} source="{nid[e["a"]]}" target="{nid[e["b"]]}">{data}</edge>')
            out.append('  </graph>')
    out.append('</graphml>')
    return '\n'.join(out) + '\n'


def corpus_html(branches: dict) -> str:
    template = (ROOT / 'app' / 'corpus_template.html').read_text(encoding='utf-8')
    styles = (ROOT / 'app' / 'styles.css').read_text(encoding='utf-8')
    data = canonical(branches)
    slim = {'branches': {b: {k: v for k, v in d.items() if k not in ('summary', 'path', 'languages')}
                         for b, d in data['branches'].items()}}
    for d in slim['branches'].values():
        d['rules'] = [{k: v for k, v in r.items() if k != 'notes'} for r in d['rules']]
    html = template.replace('@@STYLES@@', styles.rstrip('\n')).replace('@@VERSION@@', meta()['eldamo_version'])
    return html.replace('@@DATA@@', embed_json(slim))


def write_exports(branches: dict) -> None:
    write_text(EXPORTS / 'canonical.json', dumps(canonical(branches), compact=True) + '\n')
    write_text(EXPORTS / 'atlas.graphml', graphml(branches))
    write_text(ROOT / 'app' / 'corpus.html', corpus_html(branches))
