"""Source-grounded exclusion register. Does not infer historic validity."""
from pathlib import Path
import json,csv,collections,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1]
archive=ROOT/'source/eldamo-0.8.13.zip'
z=zipfile.ZipFile(archive)
report=[];overview={}
for branch in ('quenya','sindarin'):
 d=ROOT/'branches'/branch/'data'
 rules=json.loads((d/'unified_rules.json').read_text('utf-8'))
 guarded=json.loads((d/'guarded_rules.json').read_text('utf-8'))
 edges=json.loads((d/'atomic_edges_unified.json').read_text('utf-8'))
 with (d/'unified_semantic_audit.csv').open(encoding='utf-8',newline='') as f: audits=list(csv.DictReader(f))
 assert len(rules)==len(audits)
 audit_index={(r['era'],r['marker'],r['formula'],r['url'],r['rule']):r for r in audits}
 assert len(audit_index)==len(rules)
 entries=[]
 for g in guarded:
  ix=int(g['id'].split('-r')[-1])-1
  r=rules[ix]
  assert all(g[k]==r[k] for k in ('era','marker','formula','url','rule'))
  key=(r['era'],r['marker'],r['formula'],r['url'],r['rule'])
  a=audit_index[key]
  entries.append({'rule_id':g['id'],'era':g['era'],'stage':g['stage'],'marker':g['marker'], 'rule':g['rule'],'formula':g['formula'],'url':g['url'], 'reason':g['reason'], 'validation_status':a['validation_status'], 'matching_source_examples':int(a['formula_matched_examples'] or 0), 'reproduced_source_examples':int(a['rule_examples_reproduced'] or 0), 'unsupported_example_reasons':a['unsupported_example_reasons'], 'card_urls':r['card_urls']})
 (d/'non_atomic_rule_register.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
 reasons=collections.Counter(reason for e in entries for reason in e['reason']);statuses=collections.Counter(e['validation_status'] for e in entries)
 overview[branch]={'total_rules':len(rules),'atomic_edges':len(edges),'non_atomic_entries':len(entries),'non_atomic_reason_counts':dict(reasons),'non_atomic_validation_counts':dict(statuses),'non_atomic_reproduced_examples':sum(e['reproduced_source_examples'] for e in entries),'non_atomic_with_matching_examples':sum(bool(e['matching_source_examples']) for e in entries)}
 # All directly used source cards and rule pages must exist and be valid UTF-8.
 paths={ 'eldamo-0.8.13/'+u.split('eldamo.org/')[-1].split('#')[0] for r in rules for u in [r['url'],r['card_url']] if u }
 missing=[];invalid=[]
 for p in sorted(paths):
  if p not in z.namelist():missing.append(p);continue
  try: z.read(p).decode('utf-8','strict')
  except UnicodeDecodeError:invalid.append(p)
 assert not missing and not invalid,(branch,missing[:5],invalid[:5])
 overview[branch]['source_pages_verified_utf8']=len(paths)
assert sum(x['source_pages_verified_utf8'] for x in overview.values())==522
(ROOT/'reports/v7_exclusion_audit.json').write_text(json.dumps(overview,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Eldamo v7 — проверка полноты исходных записей и неатомарных формул','','Данные получены из включённого Eldamo 0.8.13; обе ветви обработаны одним алгоритмом.','', 'Категория `non_atomic` означает **непредставимость в безусловном атомарном графе**, а не недостоверность фонетического правила. Правила сохранены в `non_atomic_rule_register.json`, с URL источника и результатом проверки примеров.','','| Показатель | Quenya | Sindarin |','|---|---:|---:|']
for label,key in [('Всего правил','total_rules'),('Атомарных рёбер','atomic_edges'),('Неатомарных записей','non_atomic_entries'),('С проверяемыми соответствующими примерами','non_atomic_with_matching_examples'),('Воспроизведённых примеров неатомарных правил','non_atomic_reproduced_examples'),('Проверенных страниц с валидным UTF-8','source_pages_verified_utf8')]:lines.append(f'| {label} | {overview["quenya"][key]} | {overview["sindarin"][key]} |')
for b in overview:
 lines+=['',f'## {b.capitalize()}',f'Причины исключения из безусловного графа (могут перекрываться): `{overview[b]["non_atomic_reason_counts"]}`.',f'Статусы проверки примеров: `{overview[b]["non_atomic_validation_counts"]}`.']
lines+=['','## Ограничения','', '- Применение правила к примеру внутри одной карточки не доказывает, что можно исторически соединить два разных правила.','- Не установлена абсолютная или относительная хронология каждой пары правил, кроме используемой порядка языковых ступеней.','- Правила с контекстом не стали безусловными рёбрами и потому не участвуют в поиске путей; их наличие и статусы доступны в данных.','- URL словарных статей и библиографические пометы из Eldamo не заменяют текстологического сопоставления рукописных редакций.','- Число атомарных рёбер не обязано равняться числу правил минус число неатомарных записей: возможно объединение дублей проекций.','']
(ROOT/'reports/v7_exclusion_audit.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(overview,ensure_ascii=False,indent=2))
