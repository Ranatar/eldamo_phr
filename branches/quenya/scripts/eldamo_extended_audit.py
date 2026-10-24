import csv,re,collections,unicodedata,sys
from pathlib import Path
import zipfile,bs4
sys.path.insert(0,'/mnt/data')
from eldamo_context_interpreter import changes,supports
P=Path('/mnt/data');z=zipfile.ZipFile(P/'eldamo-0.8.13.zip')
ns={};exec((P/'build_eldamo_corrected.py').read_text().split('sounds={x:ix_sounds(x)')[0],ns)
langs=['q','mq','aq','maq','p','mp']
rows=[]
for lang in langs:
 for ph,path,kind in ns['ix_sounds'](lang):
  for r in ns['parse_page'](lang,ph,path):
   if not r['mark'].startswith('ᴱ'):rows.append(r)
# Test all formulas individually using observed examples if available, conservative extensible parser
# Recognize each explicit alternative only if both sides can be expanded without mixing correlated captures.
def alternatives(v):
 v=v.strip()
 # explicit braces with pipe-delimited alternatives, a single brace-group only
 m=re.fullmatch(r'(.*?)\{([^{}]+)\}(.*?)',v)
 if m:
  parts=m[2].split('|') if '|' in m[2] else list(m[2])
  return [m[1]+p.strip()+m[3] for p in parts if p.strip()], 'brace_class'
 return [v],''
def classify(a,b):
 aa,kind1=alternatives(a);bb,kind2=alternatives(b)
 if len(aa)>1 and len(bb)>1 and len(aa)!=len(bb):return [],'unpaired_alternatives'
 combos=list(zip(aa,bb)) if len(aa)==len(bb) and len(aa)>1 else [(x,y) for x in aa for y in bb]
 if len(combos)>12:return [],'alternative_explosion'
 compatible=[]; errors=[]
 for x,y in combos:
  if any(c in x+y for c in '|{}*?[](),') or 'V̄' in x+y or 'V̆' in x+y:
   errors.append('complex_variable_or_alternation');continue
  ok,why=supports(x,y)
  if ok:compatible.append((x,y))
  else:errors.append(why)
 if compatible:return compatible,'supported'+(' expanded' if kind1 or kind2 else '')
 return [],','.join(sorted(set(errors))) or 'unsupported'
unique={};ctr=collections.Counter();examples=[]
for r in rows:
 a,b=r['result'].strip(),r['origin'].strip()
 if r['op'] in ('<','←'): src,dst=b,a
 else:src,dst=a,b
 if src==dst:ctr['unchanged']+=1;continue
 pairs,reason=classify(src,dst)
 key=(r['mark'],src,dst,r['rulelink'],r['op'])
 if key not in unique:unique[key]={**r,'src':src,'dst':dst,'pairs':pairs,'reason':reason,'langs':set(),'phs':set()}
 unique[key]['langs'].add(r['lang']);unique[key]['phs'].add(r['ph'])
 ctr[reason]+=1
 if not pairs and len(examples)<40:examples.append((r['mark'],src,dst,reason,r['rulelink']))
with (P/'eldamo_extended_rule_inventory.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['marker','from','to','rule','rule_url','language_cards','phoneme_cards','parser_status','parsed_variants'])
 for r in unique.values():w.writerow([r['mark'],r['src'],r['dst'],r['rule'],r['rulelink'],';'.join(sorted(r['langs'])),';'.join(sorted(r['phs'])),r['reason'],'; '.join(f'{x} → {y}' for x,y in r['pairs'])])
print('input',len(rows),'unique',len(unique),'parsed unique',sum(bool(x['pairs']) for x in unique.values()),'unparsed',sum(not x['pairs'] for x in unique.values()),'reason counts',ctr.most_common(12))
print('unparsed examples',examples[:12])
import pandas as pd
inv=pd.read_csv(P/'eldamo_extended_rule_inventory.csv').fillna('')
old=pd.read_csv(P/'eldamo_sound_edges.csv').fillna('')
oldurls=set(old.rule_url)
novel=inv[(inv.parser_status.str.startswith('supported')) & (~inv.rule_url.isin(oldurls))]
print('new candidate unique rules not in original edge URLs',len(novel))
print('new examples',novel[['from','to','marker','parser_status']].head(10).to_dict('records'))
# Reassess all previously excluded rows with explicit reasons; do not equate parseability with valid word application.
oldrows=set((str(r['marker']),str(r['from']),str(r['to']),str(r['rule_url'])) for _,r in old.iterrows())
previously_unrepresented=[]
for r in unique.values():
 k=(r['mark'],r['src'],r['dst'],r['rulelink'])
 if k not in oldrows:
  previously_unrepresented.append(r)
with (P/'eldamo_recovered_exclusions.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['marker','source','result','status','rule','url','language_cards'])
 for r in previously_unrepresented:w.writerow([r['mark'],r['src'],r['dst'],r['reason'],r['rule'],r['rulelink'],';'.join(sorted(r['langs']))])
print('previously unrepresented unique',len(previously_unrepresented),'parseable',sum(bool(r['pairs']) for r in previously_unrepresented))
# Reassess original 101 using evidence examples. For every prior example, attempt its literal steps with extended formula alternatives.
atlas=pd.read_csv(P/'eldamo_critical_101_atlas.csv').fillna('')
evidence=pd.read_csv(P/'eldamo_strict_chain_evidence.csv').fillna('')
byid=collections.defaultdict(list)
for _,r in evidence.iterrows():byid[int(r['id'])].append(r)
checks=[]
for _,r in atlas.iterrows():
 pid=int(r['id']);states=[x.strip() for x in r['states'].split('→')]
 total=0; matched=0; complete=0
 for e in byid[pid]:
  forms=[x.strip() for x in str(e['word_forms']).split('→')]
  if len(forms)!=len(states):continue
  hits=[]
  for j,(a,b) in enumerate(zip(states,states[1:])):
   variants,status=classify(a,b)
   possibles=[]
   for x,y in variants:
    outs,_=changes(x,y,forms[j]);possibles.extend(outs)
   hit=forms[j+1] in possibles
   total+=1;matched+=int(hit);hits.append(hit)
  if hits and all(hits):complete+=1
 checks.append(dict(id=pid,chain=r['states'],old_grade=r['grade'],example_step_tests=total,example_step_matches=matched,full_example_matches=complete,scope='full-form examples from prior evidence; no new etymological claims'))
with (P/'eldamo_extended_101_reassessment.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
print('reassessed 101 full reproduced',sum(x['full_example_matches']>0 for x in checks),'total tests',sum(x['example_step_tests'] for x in checks))
md=['# Eldamo 0.8.13 — расширенный разбор правил и повторная проверка','',
'## Область проверки','',
'Разобраны шесть каталогов фонем (`q`, `mq`, `aq`, `maq`, `p`, `mp`); ранние маркеры `ᴱ` исключены. Направление формул восстановлено по символам `<`/`>` (и стрелкам). Повторное сравнение проведено с рёбрами предыдущего прототипа.','',
'## Итоги','',
f'- Исходных вхождений: **{len(rows)}**. Уникальных формул с маркером и ссылкой на правило: **{len(unique)}**.',
f'- Поддаются текущему *синтаксическому разбору*: **{sum(bool(v["pairs"]) for v in unique.values())}**; требуют реализации сложной семантики: **{sum(not v["pairs"] for v in unique.values())}**.',
f'- Ранее отсутствовали в CSV начального графа: **{len(previously_unrepresented)}** уникальных записей; синтаксически разобраны из них **{sum(bool(r["pairs"]) for r in previously_unrepresented)}**.',f'- Проверено исходных цепочек: **{len(checks)}**; как минимум один полный пример воспроизводится у **{sum(x["full_example_matches"]>0 for x in checks)}**.','',
'## Критическая оговорка','',
'Синтаксический разбор НЕ означает полноценную применимость фонетического правила. В частности, текущий интерпретатор не доказывает относительную хронологию, диалектную совместимость, непротиворечивость редакций, а также **не гарантирует корректную связанную подстановку переменных**. Обозначение `supported` в CSV означает лишь распознавание ограниченного шаблона. Не следует считать все распознанные правила работающими фонетическими законами.','',
'## Проблемные категории','',
'- Формулы с `|` описывают альтернативные контексты и требуют условного разбора, а не независимой замены.',
'- Долгота (`V̄`) означает операцию над гласной и не сводится к замене букв.',
'- Слоговое `S` требует особой формализации.',
'- Множества вроде `{rl}` разворачиваются на отдельные варианты только если смысл в данной записи действительно является выбором одного звука; для исторического вывода это всё ещё нужно проверять.',
'- Удаления, вставки и границы слова нуждаются в строгом сопоставлении сегментов.',
'',
'## Следующая необходимая разработка','',
'Нужен полноценный AST-парсер с операциями над множествами, захватом переменных и выравниванием, языковыми ступенями и документированными ограничениями из заметок. Только после этого следует автоматически пересоздавать **новые** цепочки из расширенного графа. Новые линии на основании одного синтаксического разбора здесь умышленно не объявлены подтверждёнными.',
'',
'## Файлы','',
'- `eldamo_extended_rule_inventory.csv` — все уникальные записи и классы разбора.',
'- `eldamo_recovered_exclusions.csv` — ранее не вошедшие записи.',
'- `eldamo_extended_101_reassessment.csv` — повторная проверка 101 цепочки.',
'- `eldamo_extended_audit.py` — воспроизводимый скрипт.',
]
(P/'eldamo_extended_analysis_report.md').write_text('\n'.join(md)+'\n',encoding='utf8')
