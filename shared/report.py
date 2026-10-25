"""reports/audit.md and reports/audit.json: what the build extracted and how well formulas replay."""
from __future__ import annotations

from collections import Counter, defaultdict

from .io import dumps, write_text
from .source import ROOT, meta, source_label

REPORTS = ROOT / 'reports'
STATUS_RU = {
    'reproduced': 'формула воспроизводит шаг',
    'reproduced_partial': 'воспроизводит при применении в одной позиции',
    'mismatch': 'формула применима, но даёт другую форму',
    'no_match': 'формула не находит, к чему примениться',
    'unsupported': 'нотация вне документированной',
    'unknown_rule': 'правило в Eldamo не указано («?»)',
    'unmatched_formula': 'формулы шага нет среди правил',
    'identity': 'исключение правила: звук сохраняется',
    'deleted_rule': 'правило удалено Толкином',
}
FAILING = ('mismatch', 'no_match', 'unsupported')


def failing_steps(data: dict) -> list:
    codes = {l['code'] for l in data['meta']['languages']}
    pairs = {p['id']: p for p in data['pairs']}
    rules = {r['id']: r for r in data['rules']}
    out = []
    for d in data['derivations']:
        if d['deleted']:
            continue
        prev = d['start']
        for s in d['steps']:
            status = s['status'].split(':')[0]
            if s['lang'] in codes and status in FAILING:
                p = pairs.get(s['pair'])
                out.append({'derivation': d['id'], 'word': d['word_form'], 'source': source_label(d['source']),
                            'rule': p['rule'] if p else None, 'rule_name': rules[p['rule']]['name'] if p else None,
                            'formula': f"{s['from']} > {s['to']}", 'before': s['before'], 'after': s['after'],
                            'status': s['status']})
            prev = s['after']
    return out


def render(branches: dict) -> tuple[str, dict]:
    lines = [
        '# Аудит сборки',
        '',
        f"Источник: Eldamo {meta()['eldamo_version']} (`eldamo-data.xml`, sha256 `{meta()['xml_sha256'][:16]}…`). "
        'Файл создаётся `scripts/build.py`; не править вручную.',
        '',
        'Каждый засвидетельствованный шаг деривации Eldamo (`<rule-example>`) проигрывается интерпретатором '
        '`shared/interpreter.py`: формула шага применяется к предыдущей форме и результат сравнивается со следующей. '
        'Расхождение не обязательно ошибка интерпретатора: в данных Eldamo встречаются шаги, где в одной записи '
        'совмещено несколько изменений, повторы формы без изменения и позиционные правила внутри сложных слов.',
        '',
    ]
    js = {}
    for b, data in branches.items():
        s = data['summary']
        fails = failing_steps(data)
        js[b] = {'summary': s, 'failing_steps': fails}
        lines += [f"## {data['meta']['title']}", '']
        lines += [
            '| показатель | значение |', '|---|---|',
            f"| правил (страниц `phonetic-rule`) | {s['rules']} |",
            f"| из них с порядком Eldamo (`order`) | {s['rules_with_order']} |",
            f"| исключено как удалённые Толкином | {len(s['excluded_rules'])} |",
            f"| подформул `<rule>` | {s['pairs']} ({', '.join(f'{k}: {v}' for k, v in s['pair_kinds'].items())}) |",
            f"| подформул с засвидетельствованными примерами | {s['pairs_with_examples']} |",
            f"| дериваций (из них отвергнутых Толкином) | {s['derivations']} ({s['deleted_derivations']}) |",
            f"| шагов дериваций в языках ветви | {s['branch_steps']} |",
            f"| доля воспроизведённых среди шагов с известной формулой | {s['reproduction_rate'] * 100:.1f}% |",
            f"| рёбер графа (условных; с примерами) | {s['edges']} ({s['conditional_edges']}; {s['edges_with_examples']}) |",
            f"| контекстных подформул вне графа | {s['contextual_pairs']} |",
            f"| цепочек | {s['chains']['chains']} ({', '.join(f'{g}: {n}' for g, n in s['chains']['grades'].items())}) |",
            f"| путей, отброшенных как противоречащие хронологии Eldamo | {s['chains']['rejected_by_chronology']} |",
            '',
            '### Проверка шагов', '',
            '| результат | шагов |', '|---|---|',
        ]
        for k, v in s['step_status'].items():
            lines.append(f"| {STATUS_RU.get(k, k)} (`{k}`) | {v} |")
        lines.append('')
        by_rule = defaultdict(Counter)
        names = {}
        for f in fails:
            if f['rule']:
                by_rule[f['rule']][f['status'].split(':')[0]] += 1
                names[f['rule']] = f['rule_name']
        top = sorted(by_rule.items(), key=lambda kv: -sum(kv[1].values()))[:15]
        if top:
            lines += ['### Правила с наибольшим числом невоспроизведённых шагов', '',
                      '| правило | mismatch | no_match | unsupported |', '|---|---|---|---|']
            for rid, c in top:
                lines.append(f"| [{names[rid]}](https://eldamo.org/content/words/word-{rid}.html) | {c['mismatch']} | {c['no_match']} | {c['unsupported']} |")
            lines.append('')
        if s['excluded_rules']:
            lines += ['### Исключённые правила', '']
            lines += [f"- {r['lang']}: {r['name']} — {r['reason']}" for r in s['excluded_rules']] + ['']
        if s['unmatched_formulas']:
            lines += ['### Формулы шагов, которых нет среди правил', '']
            lines += [f'- `{x}`' for x in s['unmatched_formulas']] + ['']
        lines += [f"Полный список невоспроизведённых шагов ({len(fails)}) — `reports/audit.json`.", '']
    return '\n'.join(lines).rstrip() + '\n', js


def write_report(branches: dict) -> None:
    text, js = render(branches)
    write_text(REPORTS / 'audit.md', text)
    write_text(REPORTS / 'audit.json', dumps(js))
