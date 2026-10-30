"""reports/audit.md and reports/audit.json: what the build extracted and how well formulas replay."""
from __future__ import annotations

from collections import Counter, defaultdict

from .io import dumps, write_text
from .languages import ERA_NAMES, ERAS
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
BACKFORM_SAMPLE = 100


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


def partial_cognates(branches: dict) -> tuple[int, list]:
    """Cognate links of Eldamo between the branches whose words, both with known roots, are
    the same word in part only (shared/reconstruct.py: partial_cognate): (pairs with roots on
    both sides, [the partial ones])."""
    from .reconstruct import partial_cognate, use_canonical
    use_canonical({b: d['lexicon'] for b, d in branches.items()})
    names = list(branches)
    if len(names) != 2:
        return 0, []
    lex = {b: {e['id']: e for e in branches[b]['lexicon']} for b in names}
    a, b = names
    pairs = set()
    for x, y in ((a, b), (b, a)):
        for e in lex[x].values():
            if e.get('speech') == 'root':
                continue
            for l in e.get('links', {}).get('cognate', ()):
                if l['id'] in lex[y] and lex[y][l['id']].get('speech') != 'root':
                    pairs.add((e['id'], l['id']) if x == a else (l['id'], e['id']))
    rooted, out = 0, []
    roots = lambda e: ' + '.join('/'.join(r['form'] for r in e['roots'] if r.get('part', 0) == k)
                                 for k in sorted({r.get('part', 0) for r in e['roots']}))
    for i, j in sorted(pairs, key=lambda t: (lex[a][t[0]]['form'].lower(), lex[b][t[1]]['form'].lower(), t)):
        e1, e2 = lex[a][i], lex[b][j]
        if not e1.get('roots') or not e2.get('roots'):
            continue
        if any(r.get('via') in ('cognate', 'deprecated', 'combine') for r in e1['roots'] + e2['roots']):
            continue                    # roots taken from the other word: not evidence of their own
        rooted += 1
        if partial_cognate(e1, e2):
            out.append({a: [e1['lang'], e1['form'], e1['id'], roots(e1)], b: [e2['lang'], e2['form'], e2['id'], roots(e2)]})
    return rooted, out


def write_report(branches: dict) -> None:
    text, js = render(branches)
    rooted, partial = partial_cognates(branches)
    if rooted:
        a, b = list(branches)
        word = lambda x: f"{x[0]}. [{x[1]}](https://eldamo.org/content/words/word-{x[2]}.html)"
        text += '\n'.join([
            '', '## Частичные когнаты', '',
            f'Связей `<cognate>` Eldamo между ветвями, где у обоих слов известны собственные корни, — {rooted}; из них '
            f'{len(partial)} связывают слова, совпадающие лишь частью состава (другое число частей или часть с другим '
            'корнем; варианты и расширения корня — один корень). При реконструкции такая связь идёт после законов '
            '(«⇋ частичный когнат») и не служит когнатом составляющей. Список — и в `reports/audit.json`.', '',
            f'| {branches[a]["meta"]["title"]} | корни | {branches[b]["meta"]["title"]} | корни |', '|---|---|---|---|',
        ] + [f'| {word(p[a])} | {p[a][3]} | {word(p[b])} | {p[b][3]} |' for p in partial]) + '\n'
        js['partial_cognates'] = {'rooted_pairs': rooted, 'pairs': partial}
    write_text(REPORTS / 'audit.md', text)
    write_text(REPORTS / 'audit.json', dumps(js))


def _sequencer_branch(b: str, data: dict) -> tuple:
    """The section of reports/sequencer.md for one branch, and its JSON."""
    from . import affixes, backform, compound
    from .sequencer import Sequencer, backtest
    lines = []
    seq = Sequencer(data)
    res = backtest(data, seq)
    langs = seq.langs
    era_of = {d['id']: langs[d['steps'][0]['lang']]['era'] for d in data['derivations']
              if d['steps'] and d['steps'][0]['lang'] in langs}
    pairs = {p['id']: p for p in data['pairs']}
    rules = {r['id']: r for r in data['rules']}
    lines += [f"## {data['meta']['title']}", '', '| эпоха | дериваций | основное | любое |', '|---|---|---|---|']
    per_era = {}
    for era in ERAS:
        rs = [r for r in res['results'] if era_of.get(r['derivation']) == era]
        if not rs:
            continue
        n, m, a = len(rs), sum(r['ok_main'] for r in rs), sum(r['ok_any'] for r in rs)
        per_era[era] = {'derivations': n, 'main': m, 'any': a}
        lines.append(f"| {ERA_NAMES[era]} | {n} | {m} ({100 * m / n:.1f}%) | {a} ({100 * a / n:.1f}%) |")
    n = res['derivations']
    lines += [f"| всего | {n} | {res['main']} ({100 * res['main'] / n:.1f}%) | {res['any']} ({100 * res['any'] / n:.1f}%) |", '']
    blame = Counter()
    for r in res['results']:
        if not r['ok_main'] and r['diverge'] and r['diverge']['pair'] in pairs:
            blame[pairs[r['diverge']['pair']]['rule']] += 1
    lines += ['### Где основное чтение впервые расходится с деривацией', '',
              'Правило засвидетельствованного шага, чью форму основное чтение не проходит.', '',
              '| правило | язык | дериваций |', '|---|---|---|']
    for rid, c in blame.most_common(15):
        lines.append(f"| [{rules[rid]['name']}](https://eldamo.org/content/words/word-{rid}.html) | {rules[rid]['lang']} | {c} |")
    lines.append('')
    blocked = [c for c in seq.rules if c.blocked_by]
    if blocked:
        lines += ['### Условие «elsewhere»', '',
                  'Общая подформула не применяется там, где более позднее правило того же языка задаёт тот же '
                  'вход для определённой позиции:', '']
        lines += [f"- {c.lang}: {c.name} ← {', '.join(seq.by_id[x].name for x in c.blocked_by)}" for c in blocked]
        lines.append('')
    bad = [c for c in seq.rules if c.unsupported]
    if bad:
        lines += [f"Подформул вне документированной нотации, пропускаемых секвенсором: "
                  f"{sum(len(c.unsupported) for c in bad)} (в {len(bad)} правилах).", '']
    cres = compound.backtest(data, data['lexicon'], seq)
    if cres['cases']:
        k = cres['cases']
        lines += ['### Сложения с праформами', '',
                  'Сложения Eldamo из двух элементов, у которых есть деривация от праформы и праформы обоих '
                  'элементов. Праформы элементов соединяются через `+` (полный первый элемент или без '
                  'конечного гласного), затем соединение проходит все правила ветви (`shared/compound.py`).', '',
                  '| показатель | случаев |', '|---|---|',
                  f'| случаев (сложение × деривация) | {k} |',
                  f"| соединение праформ совпало с начальной формой деривации | {cres['join_ok']} ({100 * cres['join_ok'] / k:.0f}%) |",
                  f"| основное чтение = засвидетельствованная форма | {cres['main']} ({100 * cres['main'] / k:.0f}%) |",
                  f"| форма среди вариантов | {cres['any']} ({100 * cres['any'] / k:.0f}%) |", '']
    lres = compound.latest_backtest(data, data['lexicon'], seq)
    if lres['cases']:
        k = lres['cases']
        lines += ['### Сложения на последней стадии', '',
                  f"Сложения {'квенья' if b == 'quenya' else 'синдарина'} из двух элементов того же языка. "
                  'Таблица стыков (`shared/junctions.py`, `branches/' + b + '/data/junctions.json`) строится '
                  'без проверяемого сложения, затем сложение предсказывается по элементам: основа или словарная '
                  'форма первого элемента, словарная форма второго; изменения на стыке и в конце — по частоте '
                  'в остальных сложениях; ' + ('плюс правила §6.1 учебника (`shared/morphophonology.py`).'
                                                if b == 'quenya' else
                                                'плюс мягкая мутация второго элемента и правила синдарина для многосложных слов.'), '',
                  '| показатель | случаев |', '|---|---|',
                  f'| сложений | {k} |',
                  f"| первый вариант = засвидетельствованная форма | {lres['main']} ({100 * lres['main'] / k:.0f}%) |",
                  f"| форма среди первых 8 вариантов | {lres['any']} ({100 * lres['any'] / k:.0f}%) |", '']
    ares = affixes.leave_one_out(b, data['lexicon'])
    if ares['cases']:
        pct = lambda x, n: f'{x} ({100 * x / n:.0f}%)' if n else '0'
        lines += ['### Суффиксы и приставки', '',
                  'Производные слова Eldamo из основы и одного аффикса (часть речи `suf` или `pref`). Модель '
                  '(`shared/affixes.py`, `branches/' + b + '/data/affixes.json`) строится без проверяемого слова: '
                  'какая форма аффикса берётся после гласного и после согласного, что происходит на стыке и в '
                  'конце — сначала по словам с этим же аффиксом, иначе по всем словам с аффиксом того же вида.', '',
                  '| | слов | первый вариант = форма Eldamo | среди первых 8 |', '|---|---|---|---|']
        for k, label in (('suffix', 'суффиксы'), ('prefix', 'приставки')):
            x = ares[k]
            lines.append(f"| {label} | {x['cases']} | {pct(x['main'], x['cases'])} | {pct(x['any'], x['cases'])} |")
        lines += [f"| всего | {ares['cases']} | {pct(ares['main'], ares['cases'])} | {pct(ares['any'], ares['cases'])} |", '']
    final_code = max((l for l in langs.values() if l['era'] == 'late'), key=lambda l: l['stage'])['code']
    bres = backform.evaluate(data, seq, final_code, sample=BACKFORM_SAMPLE)
    if bres.get('cases'):
        k = bres['cases']
        lines += ['### Обратное восстановление праформ', '',
                  'Соответствия «праформа → конечная форма» выучены на половине дериваций; для другой половины '
                  '(первые ' + str(k) + ') праформа восстанавливается по конечной форме: кандидаты перебираются по '
                  'вероятности и проверяются прямым прогоном (`shared/backform.py`). Восстановленная праформа — '
                  'гипотеза; так помечаются и сложения, построенные на ней.', '',
                  '| показатель | случаев |', '|---|---|',
                  f'| конечных форм | {k} |',
                  f"| найдена хотя бы одна праформа, дающая форму прямым прогоном | {bres.get('verified', 0)} ({100 * bres.get('verified', 0) / k:.0f}%) |",
                  f"| первая из них = праформа Eldamo | {bres.get('first', 0)} ({100 * bres.get('first', 0) / k:.0f}%) |",
                  f"| праформа Eldamo среди найденных (до 8) | {bres.get('any', 0)} ({100 * bres.get('any', 0) / k:.0f}%) |", '']
    js = {'derivations': n, 'main': res['main'], 'any': res['any'], 'eras': per_era,
             'backform': bres,
             'affixes': {k2: v for k2, v in ares.items()},
             'latest_compounds': {k2: v for k2, v in lres.items()},
             'results': [r for r in res['results'] if not r['ok_main']],
             'compounds': {k2: v for k2, v in cres.items()}}
    lines += [f"Расходящиеся деривации ({n - res['main']}) — `reports/sequencer.json`.", '']
    return lines, js


_SEQ_BRANCHES = None


def _sequencer_worker(b: str):
    return _sequencer_branch(b, _SEQ_BRANCHES[b])


def render_sequencer(branches: dict) -> tuple[str, dict]:
    """reports/sequencer.md: every attested derivation replayed from its start
    form through the whole chronology of the branch (shared/sequencer.py)."""
    lines = [
        '# Проверка секвенсора',
        '',
        f"Источник: Eldamo {meta()['eldamo_version']}. Файл создаётся `scripts/build.py`; не править вручную.",
        '',
        'Секвенсор (`shared/sequencer.py`) прогоняет начальную форму деривации через все правила ветви в '
        'хронологическом порядке — так, как будет порождаться форма нового слова, — и сравнивает результат с '
        'конечной формой деривации Eldamo. В отличие от `audit.md`, где каждый шаг проверяется отдельно, здесь '
        'правила не подсказываются: секвенсор сам решает, какие из них применимы. Прогон останавливается на '
        'правиле последнего засвидетельствованного шага (деривация может кончаться промежуточной формой).',
        '',
        '«Основное» — первое чтение (необязательные правила применены, из альтернатив выбрана первая '
        'подформула); «любое» — конечная форма среди всех вариантов (необязательные правила, альтернативные '
        'исходы, правила на границе морфем `+` в формах без отмеченной границы).',
        '',
    ]
    global _SEQ_BRANCHES
    import multiprocessing as mp
    import os
    js = {}
    processes = int(os.environ.get('QUETTAMIN_JOBS') or os.cpu_count() or 1)
    _SEQ_BRANCHES = branches
    try:
        if processes > 1 and len(branches) > 1 and 'fork' in mp.get_all_start_methods():
            with mp.get_context('fork').Pool(min(processes, len(branches))) as pool:
                parts = pool.map(_sequencer_worker, list(branches))
        else:
            parts = [_sequencer_worker(b) for b in branches]
    finally:
        _SEQ_BRANCHES = None
    for b, (part, part_js) in zip(branches, parts):
        lines += part
        js[b] = part_js
    from .unruled import summary, unruled_steps
    steps = unruled_steps(branches)
    table = summary(steps)
    names = {l['code']: f"{l['marker']} {l['name']}" for data in branches.values() for l in data['meta']['languages']}
    lines += ['## Шаги без правила в деривациях Eldamo', '',
              'Шаг, у которого Страк ставит «?» вместо правила: ни один известный закон его не объясняет '
              '(Q. pupso «муха» < ✶buzbō > buspō > **puspō** > pupso; законы дают βuspō, отсюда *vupso). Для каждого '
              'такого шага к форме перед ним применяются законы того же языка (`shared/unruled.py`): «правило» — '
              'шаг даёт одно правило языка, которое Eldamo не назвало; «законы» — их последовательность; «нет» — '
              'форма расходится с законами.', '',
              '| язык | шагов | правило | законы | нет |', '|---|---|---|---|---|']
    for lang, c in table.items():
        lines.append(f"| {names.get(lang, lang)} | {sum(c.values())} | {c['rule']} | {c['laws']} | {c['none']} |")
    total = Counter(s['kind'] for s in steps)
    lines += [f"| всего | {len(steps)} | {total['rule']} | {total['laws']} | {total['none']} |", '',
              '| слово | язык | шаг Eldamo | по законам |', '|---|---|---|---|']
    for st in steps:
        if st['kind'] == 'none':
            lines.append(f"| [{st['word_form']}](https://eldamo.org/content/words/word-{st['word']}.html) | "
                         f"{names.get(st['lang'], st['lang'])} | {st['before']} > {st['after']} | {st['laws'] or ''} |")
    lines.append('')
    js['unruled'] = steps
    return '\n'.join(lines).rstrip() + '\n', js


def write_sequencer_report(branches: dict) -> None:
    text, js = render_sequencer(branches)
    write_text(REPORTS / 'sequencer.md', text)
    write_text(REPORTS / 'sequencer.json', dumps(js))


RECON_SAMPLE = 30


def render_reconstruction(branches: dict) -> tuple[str, dict]:
    """reports/reconstruction.md: reconstruction between periods checked on Eldamo."""
    from .reconstruct import Context, evaluate
    ctx = Context(branches)
    res = evaluate(ctx, sample=RECON_SAMPLE)
    pct = lambda x, n: f'{x} ({100 * x / n:.0f}%)' if n else '—'
    lines = [
        '# Проверка реконструкции между периодами',
        '',
        f"Источник: Eldamo {meta()['eldamo_version']}. Файл создаётся `scripts/build.py`; не править вручную. "
        f'Выборки — до {RECON_SAMPLE} случаев на строку. Устройство — `shared/reconstruct.py`, план — '
        '`docs/period-reconstruction-plan.md`.',
        '',
        '## Назад по стадиям одного языка',
        '',
        'Эталон — формы на конце каждой стадии из дериваций, которые секвенсор воспроизводит '
        '(`branches/<ветвь>/data/stages.json`). Соответствия выучены на половине дериваций, проверка — на другой: по '
        'форме последней стадии восстанавливается форма более ранней (0 — праформа).',
        '',
        '| ветвь | концепция: со стадии → на стадию | случаев | кандидат найден | первый = Eldamo | среди 8 |',
        '|---|---|---|---|---|---|',
    ]
    for b in branches:
        for key, st in res[b].items():
            n = st.get('cases', 0)
            era, path = key.split(': ')
            lines.append(f"| {b} | {ERA_NAMES[era]}: {path.replace('->', '→')} | {n} | {pct(st.get('found', 0), n)} | "
                         f"{pct(st.get('first', 0), n)} | {pct(st.get('any', 0), n)} |")
    lines += ['', '## Когнаты: квенья ↔ синдарин (поздняя концепция)', '',
              'Через праформу: назад в своей ветви, вперёд по законам другой. Пары с одной и той же праформой в '
              'нормализованных деривациях обеих ветвей и пары по связям `<cognate>` Eldamo; для последних — по '
              'слову (своя праформа Eldamo, если есть) и по одной форме.', '',
              '| пары | случаев | по слову: первый / среди 8 | по форме: первый / среди 8 |', '|---|---|---|---|']
    for key in ('cognates quenya -> sindarin', 'cognates sindarin -> quenya'):
        st = res[key]
        n = st['cases']
        lines.append(f"| общая праформа, {key.split(' ', 1)[1].replace('->', '→')} | {n} | — | "
                     f"{pct(st['first'], n)} / {pct(st['any'], n)} |")
    for key in ('cognate links q -> s', 'cognate links s -> q'):
        st = res[key]
        n = st['cases']
        lines.append(f"| `<cognate>`, {key.split(' ', 2)[2].replace('->', '→')} | {n} | {pct(st['word_first'], n)} / "
                     f"{pct(st['word_any'], n)} | {pct(st['form_first'], n)} / {pct(st['form_any'], n)} |")
    lines += ['', '## Концепции Толкина: ранняя и средняя → поздняя', '',
              'Пары `combine`/`deprecated` Eldamo. Проверяемая связь при реконструкции не используется: ответ '
              'строится как для слова без связи — без изменений, если поздний язык допускает форму, иначе '
              'переэтимологизация через праформу. «Без изменений» — доля пар, где форма у Толкина действительно не '
              'изменилась (нулевая модель).', '',
              '| пары | всего | случаев | без изменений | первый вариант | среди 8 |', '|---|---|---|---|---|---|']
    for key in ('conceptions mq -> q', 'conceptions n -> s', 'conceptions eq -> q', 'conceptions g -> s'):
        st = res[key]
        n = st['cases']
        lines.append(f"| {key.split(' ', 1)[1].replace('->', '→')} | {st['pairs']} | {n} | {pct(st['identity'], n)} | "
                     f"{pct(st['first'], n)} | {pct(st['any'], n)} |")
    lines += ['', '## Основы слов', '',
              'Слова с основой (Q. lindë, lindi-; nér, ner-) и праформой Eldamo: восстановление праформы по форме слова '
              'без основы и с ней. Основа — форма слова перед окончанием: в ней сохраняется то, что утрачено или '
              'изменилось на конце (учебник Eldamo, intro-quenya §2.4.2, §11.3). Кандидат согласуется с основой, если его '
              'прогон вперёд как основы (без законов конца слова) даёт основу — с последним гласным или без него '
              '(Ambar, ambar- < ✶ambara). Проба: такой кандидат получает вес ×10. Выигрыша над корнями проба не даёт, поэтому '
              'в реконструкции согласие с основой только помечается (⊢), вес не меняется. «Праформа Eldamo согласуется» — у скольких '
              'слов сама праформа Eldamo проходит эту проверку: остальные основы законами не объясняются (долгота '
              'односложных nér, ner- — морфологическая; farnë, farni- при ✶pʰarne).', '',
              '| язык | слов с основой | случаев | праформа Eldamo согласуется | без основы: первый / среди 8 | '
              'с основой: первый / среди 8 |', '|---|---|---|---|---|---|']
    for code in ('q', 'mq', 's', 'n'):
        st = res[f'stems {code}']
        n = st.get('cases', 0)
        lines.append(f"| {code} | {st['words']} | {n} | {pct(st.get('gold_stem', 0), n)} | "
                     f"{pct(st.get('plain_first', 0), n)} / {pct(st.get('plain_any', 0), n)} | "
                     f"{pct(st.get('stem_first', 0), n)} / {pct(st.get('stem_any', 0), n)} |")
    lines += ['', '## Сложения по когнатам составляющих', '',
              'Сложное или производное слово одной ветви с когнатом Eldamo в другой (поздняя концепция): если у каждой '
              'составляющей есть когнат в языке назначения, слово собирается заново из них словообразованием этого языка '
              '(S. Adanel = Adan + -iel → Q. Atan + -iel → Atanel, Ataniel). Связь самого слова не используется. '
              '«Собрано» — у скольких слов у всех составляющих нашлись когнаты.', '',
              '| пары | всего | случаев | собрано | без сборки: первый / среди 8 | со сборкой: первый / среди 8 |',
              '|---|---|---|---|---|---|']
    for key in ('compounds q -> s', 'compounds s -> q'):
        st = res[key]
        n = st.get('cases', 0)
        lines.append(f"| {key.split(' ', 1)[1].replace('->', '→')} | {st['pairs']} | {n} | {pct(st.get('built', 0), n)} | "
                     f"{pct(st.get('plain_first', 0), n)} / {pct(st.get('plain_any', 0), n)} | "
                     f"{pct(st.get('elements_first', 0), n)} / {pct(st.get('elements_any', 0), n)} |")
    lines += ['', '## Праформа, начатая корнем', '',
              'Обратный поиск хуже всего угадывает начало слова (Q. hy- < ✶kʰj- или ✶sj-). Если корень слова известен '
              '(свой или первой составляющей), к найденным кандидатам добавляются праформы, начатые корнем: корень без '
              'конечного гласного ставится на место начала кандидата до согласного того же места образования, что и '
              'последний согласный корня (✶j̊arma → √KHYAR + -ma = ✶kʰjarma); такая праформа остаётся, только если '
              'законы ведут от неё к форме слова. Слова с корнем и праформой Eldamo; праформа восстанавливается по форме '
              'слова без своей деривации.', '',
              '| язык | слов | случаев | без корня в начале: первый / среди 8 | с корнем: первый / среди 8 |',
              '|---|---|---|---|---|']
    for code in ('q', 'mq', 's', 'n'):
        st = res[f'root seeds {code}']
        n = st.get('cases', 0)
        lines.append(f"| {code} | {st['words']} | {n} | {pct(st.get('plain_first', 0), n)} / {pct(st.get('plain_any', 0), n)} | "
                     f"{pct(st.get('seed_first', 0), n)} / {pct(st.get('seed_any', 0), n)} |")
    res['root_candidates'] = _root_candidate_check(branches)
    lines += ['', '## Корни по праформе', '',
              'Корень не форма, к которой применимы звуковые законы: праформа строится из него морфологией '
              '(✶kʰjar-ja, ✶a-mbar-a), поэтому назад к корню законы не ведут. Вместо этого корни той же концепции '
              'сопоставляются с праформой (`shared/roots.py`): согласные корня должны начинать согласные праформы. '
              'Учтены способы образования из грамматических статей Eldamo (PE18/84–101, VT39, PE14/63): '
              'приставка основного гласного корня (augmentation: ✶ambar < MBAR; другой гласный — скорее приставка вроде '
              'al-, u-, штрафуется), носовой перед согласным корня (nasal infixion: KAB > kambā), начальное s- '
              '(s-fortification), удвоенный согласный (dynamic lengthening), слоговые ṛ ḷ ṇ ранних корней, варианты '
              'через «/» и в скобках (WĀ/AWA, IN(ID)), у ранних корней — без конечного гласного, повторяющего первый '
              '(NERE → nert). Выше — корень, который начинает праформу целиком, потом — с тем же основным гласным '
              '(a-усиление ai, au его сохраняет), потом — более длинный. Проверка — на праформах Eldamo слов, чей корень Eldamo называет '
              '(своей деривацией, не через составляющие); корни-омонимы (LAK¹, LAK²) различаются, так что первый '
              'вариант часто ошибается только номером. «Без корня» — слова с праформой, но без корня у Eldamo: у '
              'скольких находится хоть один корень-кандидат.', '',
              '| язык | слов | первый = корень Eldamo | среди 3 | среди 8 | без корня: слов / с кандидатом |',
              '|---|---|---|---|---|---|']
    for code, st in res['root_candidates'].items():
        n = st['words']
        lines.append(f"| {code} | {n} | {pct(st['first'], n)} | {pct(st['top3'], n)} | {pct(st['any'], n)} | "
                     f"{st['rootless']} / {pct(st['guessed'], st['rootless'])} |")
    lines.append('')
    return '\n'.join(lines) + '\n', res


def _root_candidate_check(branches: dict) -> dict:
    from . import roots as RT
    from .compound import origins
    out = {}
    for b, data in branches.items():
        table = RT.table(data['lexicon'])
        langs = {l['code']: l for l in data['meta']['languages']}
        last = {}
        for l in data['meta']['languages']:
            last[l['era']] = max(last.get(l['era'], 0), l['stage'])
        codes = [l['code'] for l in data['meta']['languages'] if l['stage'] == last[l['era']] and l['stage'] > 0]
        for code in codes:
            era = langs[code]['era']
            st = {'words': 0, 'first': 0, 'top3': 0, 'any': 0, 'rootless': 0, 'guessed': 0}
            for e in data['lexicon']:
                if e['lang'] != code or e.get('neo') or e.get('speech') == 'root':
                    continue
                prims = origins(e, era)
                if not prims:
                    continue
                cands = [c[1] for c in RT.candidates(table, prims[0], era, 8)]
                own = [r for r in e.get('roots', ()) if not r.get('via')]
                if not e.get('roots'):
                    st['rootless'] += 1
                    st['guessed'] += bool(cands)
                if not own:
                    continue
                gold = {r['id'] for r in own}
                st['words'] += 1
                st['first'] += bool(cands) and cands[0] in gold
                st['top3'] += any(c in gold for c in cands[:3])
                st['any'] += any(c in gold for c in cands)
            out[code] = st
    return out


def write_reconstruction_report(branches: dict) -> None:
    text, js = render_reconstruction(branches)
    write_text(REPORTS / 'reconstruction.md', text)
    write_text(REPORTS / 'reconstruction.json', dumps(js))
