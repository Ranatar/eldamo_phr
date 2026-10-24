import json,collections,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
lines=['# Методологическая сверка Quenya / Sindarin — v5','',
'Основным и отображаемым по умолчанию корпусом является `unified_assessed_chains.json`, создаваемый одним `shared/graph.py` и одним `shared/chains.py` для обеих ветвей. Поиск в приложении работает на тех же `atomic_edges_unified.json`. Старые графы и критические атласы остаются отдельными архивными наборами, не являются вторым источником основной статистики.','',
'**Важно:** одинаковый код не гарантирует полной фонологической полноты. Сложные/контекстные правила сохраняются, но не входят в безусловный атомарный поиск. Непроверенные диалект, относительная хронология и контексты — открытые вопросы.','',
'## Результаты повторного вычисления','', '| Показатель | Quenya | Sindarin |','|---|---:|---:|']
metrics={}
for branch in ('quenya','sindarin'):
 d=ROOT/'branches'/branch/'data';a=ROOT/'branches'/branch/'app'
 canonical=json.loads((d/'unified_assessed_chains.json').read_text());edges=json.loads((d/'atomic_edges_unified.json').read_text()); oldedges=json.loads((a/'edges.json').read_text());guarded=json.loads((d/'guarded_rules.json').read_text());rules=json.loads((d/'unified_rules.json').read_text());display=json.loads((a/'chains.json').read_text())
 new_by={(e['era'],e['stage'],e['marker'],e['a'],e['b'],e['url']) for e in edges};old_by={(e.get('era'),e.get('stage'),e.get('marker'),e.get('a'),e.get('b'),e.get('url')) for e in oldedges}
 onlyold=sorted(old_by-new_by,key=str);onlynew=sorted(new_by-old_by,key=str)
 (d/'legacy_edge_comparison.json').write_text(json.dumps({'comparison_key':['era','stage','marker','a','b','url'],'legacy_only':[list(x) for x in onlyold],'canonical_only':[list(x) for x in onlynew]},ensure_ascii=False,indent=2))
 metrics[branch]={'rules':len(rules),'guarded':len(guarded),'canonical_edges':len(edges),'legacy_edges':len(oldedges),'canonical_chains':len(canonical),'legacy_chains':len(display),'grade':collections.Counter(x['grade'] for x in canonical),'onlylegacy':len(onlyold),'onlycanonical':len(onlynew)}
for title,key in [('Непосредственно извлечённых правил (основной корпус)','rules'),('Сохранённых сложных/контекстных правил','guarded'),('Рёбер основного графа','canonical_edges'),('Рёбер архивного графа','legacy_edges'),('Цепочек основного корпуса','canonical_chains'),('Цепочек архивного критического атласа','legacy_chains'),('Только в архивном графе по составному ключу','onlylegacy'),('Только в основном графе по составному ключу','onlycanonical')]:
 lines.append(f"| {title} | {metrics['quenya'][key]} | {metrics['sindarin'][key]} |")
for grade in ['C','D','U']:
 lines.append(f"| Основной корпус: {grade} | {metrics['quenya']['grade'][grade]} | {metrics['sindarin']['grade'][grade]} |")
lines+=['','## Уточнение оценок','',
'В старом общем модуле цепочка, составленная из непрерывных словоформ разных правил, могла получить C без установленного совпадения словарной статьи и библиографического источника. В v5 этот случай получает U, а не C. C остаётся предварительной категорией только для последовательностей, удовлетворяющих машинной проверке обеих связей; это по-прежнему не подтверждает все исторические условия.','',
'## Что НЕ проверено и не должно называться завершённым','',
'- Контекстные условия всех сложных формул для каждой словоформы; они сохранены как `guarded_rules.json`.','- Историческая совместимость авторских редакций внутри каждого периода.','- Полная филологическая интерпретация цепочек, отсутствующих в общем графе, из прежних архивных атласов.','- Отождествление конкретных этимологических статей при всех разночтениях написания, удаления и источников.','- Отсутствие иных фонетических законов вне извлечённых страниц Eldamo 0.8.13.','',
'## Воспроизведение','', 'Запустить `python scripts/validate_and_build_canonical.py`, затем `python tests/test_canonical_pipeline.py`, `python tests/test_research_corpus.py` и `python tests/test_unified.py`. Архивный материал не удаляется.']
out=ROOT/'reports/v5_methodology_and_remaining_limits.md';out.write_text('\n'.join(lines),encoding='utf-8');print(out)
