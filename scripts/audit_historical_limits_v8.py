"""Auditable epistemic limits of canonical and archival chains; does NOT infer history."""
from pathlib import Path
import json,csv,collections
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text(encoding='utf8'))
def run():
 summary={}; all_rows=[]
 for branch in ('quenya','sindarin'):
  base=ROOT/'branches'/branch;d=base/'data'
  edges=load(d/'atomic_edges_unified.json'); guarded=load(d/'guarded_rules.json')
  index=collections.defaultdict(list)
  for e in edges:index[(e['era'],e['a'],e['b'])].append(e)
  chains=load(d/'unified_assessed_chains.json'); old=load(d/'chain_step_provenance.json')
  ledger=[];counter=collections.Counter()
  for c in chains:
   matches=[]; ambiguity=[]
   for i,(a,b,url) in enumerate(zip(c['states'],c['states'][1:],c['urls'])):
    candidates=[e for e in index[c['era'],a,b] if e['url']==url]
    if len(candidates)!=1:ambiguity.append({'step':i,'count':len(candidates)})
    matches.append(candidates[0] if len(candidates)==1 else None)
   stages=[e['stage'] if e else None for e in matches]
   same_stage=any(stages[i] is not None and stages[i]==stages[i+1] for i in range(len(stages)-1))
   positions={e.get('position','any') for e in matches if e and e.get('position','any')!='any'}
   multi_provenance=[{'step':i,'source_rule_ids':e['source_rule_ids']} for i,e in enumerate(matches) if e and len(e['source_rule_ids'])>1]
   missing_examples=not c.get('whole_word_attested',False)
   rec={'id':c['id'],'branch':branch,'era':c['era'],'states':c['states'],'urls':c['urls'],
    'grade':c['grade'],'stage_sequence':stages,'same_stage_order_unverified':same_stage,
    'different_position_requirements':len(positions)>1,'ambiguous_atomic_match':ambiguity,
    'merged_rule_provenance':multi_provenance,'shared_article_and_source_example':bool(c.get('whole_word_attested',False)),
    'contextual_rules_not_considered':True,'relative_chronology_unverified':True,
    'authorial_revision_compatibility_unverified':True,
    'machine_attested_examples_are_not_historical_proof':True}
   ledger.append(rec)
   for k in ('same_stage_order_unverified','different_position_requirements','contextual_rules_not_considered','relative_chronology_unverified','authorial_revision_compatibility_unverified'):
    counter[k]+=bool(rec[k])
   counter['ambiguous_atomic_match']+=bool(ambiguity)
   counter['merged_rule_provenance']+=bool(multi_provenance)
   counter['without_shared_example_witness']+=missing_examples
   counter['total']+=1
   all_rows.append({'branch':branch,'id':c['id'],'era':c['era'],'grade':c['grade'],
    'same_stage_order_unverified':same_stage,'different_position_requirements':len(positions)>1,
    'ambiguous_atomic_match':len(ambiguity),'merged_rule_steps':len(multi_provenance),
    'whole_word_attested_machine':bool(c.get('whole_word_attested',False)),
    'states':' → '.join(c['states']),'urls':' | '.join(c['urls'])})
  (d/'historical_limit_ledger_v8.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf8')
  archived={}
  for corpus,records in old.items():
   causes=collections.Counter(x['overall'] for x in records)
   step_causes=collections.Counter(s['status'] for x in records for s in x['steps'])
   problems=[{'id':x['id'],'overall':x['overall'],'steps':[s for s in x['steps'] if s['status']!='exact_step_match']} for x in records if x['overall']!='graph_steps_verified']
   archived[corpus]={'total':len(records),'chain_statuses':dict(causes),'step_statuses':dict(step_causes),'unresolved':problems}
  (d/'archival_gap_register_v8.json').write_text(json.dumps(archived,ensure_ascii=False,indent=2),encoding='utf8')
  summary[branch]={'canonical':dict(counter),'archival':{k:{'chain_statuses':v['chain_statuses'],'step_statuses':v['step_statuses']} for k,v in archived.items()},'guarded_records':len(guarded)}
 with (ROOT/'reports/v8_canonical_chain_limits.csv').open('w',newline='',encoding='utf8') as f:
  writer=csv.DictWriter(f,fieldnames=list(all_rows[0]));writer.writeheader();writer.writerows(all_rows)
 (ROOT/'reports/v8_historical_limit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
 lines=['# Eldamo v8 — ограничения канонических и архивных цепочек','',
 'Все сведения взяты только из включённых данных Eldamo и файлов проекта v7. Неизвестное не превращено в утверждение о фонологии.','',
 '**Ни один формально корректный переход не считается доказанной историей слова только по наличию графового пути.**','',
 '## Поцепочечные проверки','']
 for branch,s in summary.items():
  lines+=['### '+branch,'', '| Проверяемое обстоятельство | Количество цепочек |','|---|---:|']
  for k,v in s['canonical'].items():lines.append(f'| `{k}` | {v} |')
  lines+=['',f'Контекстных/неатомарных записей: {s["guarded_records"]}; они сохранены и не заявляются как исполняемые рёбра.','', '### Архивные цепочки — '+branch,'']
  for corpus,v in s['archival'].items():lines+=['**'+corpus+'**: '+str(v['chain_statuses'])+'; статусы шагов: '+str(v['step_statuses']),'']
 lines+=['## Принципиальные ограничения','',
 '- Порядок правил внутри одной языковой ступени не восстановлен по рукописям; `same_stage_order_unverified` выделяет особенно явные случаи.',
 '- Воспроизведение отдельных правил на примерах не означает, что все правила можно последовательно применить к одной исторической форме.',
 '- Совпадающие ссылки на словарные статьи и библиографические обозначения являются машинными свидетельствами, не текстологической экспертизой.',
 '- `archival_gap_register_v8.json` не трактует отсутствие в атомарном графе как опровержение правила; он фиксирует наблюдаемую причину технического разрыва.',
 '- Сложные формулы не превращены в безусловные стрелки: это привело бы к ложным результатам.',
 '- Невозможно корректно присвоить окончательные исторические A/B оценки по имеющимся автоматизированным проверкам.',
 '', '## Воспроизводимые файлы', '',
 '`branches/{quenya,sindarin}/data/historical_limit_ledger_v8.json`, `archival_gap_register_v8.json`, `reports/v8_canonical_chain_limits.csv`, `reports/v8_historical_limit_summary.json`.']
 (ROOT/'reports/v8_historical_limits.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
 print(json.dumps(summary,ensure_ascii=False))
 return summary
if __name__=='__main__':run()
