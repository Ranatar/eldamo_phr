from pathlib import Path
import json,csv,collections,re,hashlib,zipfile,shutil
R=Path(__file__).resolve().parents[1]; A=R/'app'
chains=json.loads((A/'chains.json').read_text()); prior=[x for x in chains if x['kind']=='assessed']; new=[x for x in chains if x['kind'] in ('structural','assessed_extension')];assert len(prior)==101 and len(new)==38
rules=list(csv.DictReader(open(R/'data'/'eldamo_extended_rule_inventory.csv',encoding='utf-8-sig')))
oldkeys={(tuple(x['states']),x['era']) for x in prior}
def terms(s):return [x for x in s.split(' → ') if x]
def signature(x):return set(zip(x['states'],x['states'][1:]))
rows=[]
for c in new:
 states=c['states']; steps=len(states)-1; n=int(c.get('supported',0)); exact=int(c.get('exact',0)); urls=c.get('urls',[]); markers=terms(c['markers']); missing=[i+1 for i,u in enumerate(urls) if not u]
 repeat=len(states)!=len(set(states)); same=(tuple(states),c['era']) in oldkeys
 related=sorted([(len(signature(c)&signature(p)),p['id'],p['grade']) for p in prior],reverse=True)
 best=[z for z in related if z[0]>0][:3]
 candidate=[]
 for i,(fr,to) in enumerate(zip(states,states[1:])):
  mark=markers[i] if i<len(markers) else ''
  rr=[r for r in rules if (fr+' → '+to) in r.get('parsed_variants','') and (not mark or r['marker']==mark)]
  if not rr:rr=[r for r in rules if r['from']==fr and r['to']==to and (not mark or r['marker']==mark)]
  candidate.append(rr[:3])
 # statuses conservative, distinguish absence of example from contradiction
 if repeat:
  grade='U'; why='Последовательность возвращается к ранее встречавшемуся состоянию; необходимо подтвердить разные контексты/исторические ступени, иначе возможно ложное соединение.'
 elif len(missing)>0:
  grade='U'; why=f'Для шагов {missing} нет ссылки на индивидуальную страницу правила; невозможно проверить языковую и контекстную атрибуцию каждого перехода.'
 elif n==steps and exact==steps and steps>0:
  grade='C'; why='Для каждого шага имеется индивидуальное примерное подтверждение и совпадение формулы; общей непрерывной этимологии и полной проверки порядка нет.'
 elif n>0:
  grade='D'; why=f'Прямые примеры найдены лишь для {n} из {steps} шагов (точных совпадений формул: {exact}); вся цепочка остаётся формальной гипотезой.'
 else:
  grade='U'; why='Не найдено применимого примера ни для одного шага; недостаточно данных для содержательной оценки всей цепочки.'
 if same:why+=' Полностью совпадает с ранее оценённой цепочкой.'
 c['grade']=grade;c['kind']='assessed_extension';c['reason']=why
 c['action']='Проверить непрерывные формы одного слова, окружение, последовательность и диалект по заметкам каждого правила.'
 c['rules']=[' / '.join(dict.fromkeys(r['rule'] for r in rs)) if rs else 'Точное правило не сопоставлено с инвентарём' for rs in candidate]
 c['language']=' → '.join('/'.join(dict.fromkeys(r['language_cards'] for r in rs)) if rs else '?' for rs in candidate)
 c['evidence']=f'Переходов: {steps}; с примерами: {n}; с точной формулой: {exact}; шагов без страницы правила: {len(missing)}.'
 c['previous']='ADDITIONAL_STRUCTURAL_CANDIDATE'
 c['related_prior']=[{'id':id,'shared_edges':count,'grade':gr} for count,id,gr in best]
 rows.append({'id':c['id'],'states':' → '.join(states),'era':c['era'],'markers':c['markers'],'grade':grade,'steps':steps,'example_supported_steps':n,'exact_formula_supported_steps':exact,'missing_url_steps':';'.join(map(str,missing)),'repeated_states':repeat,'rule_labels':' || '.join(c['rules']),'rule_urls':' || '.join(urls),'closest_originals':'; '.join(f'{id} ({num} совп. переходов; {gr})' for num,id,gr in best),'assessment':why,'next_check':c['action']})
assert len(rows)==38
for x in chains:
 if x['kind'] in ('structural','assessed_extension'): assert x['grade']!='—'
(A/'chains.json').write_text(json.dumps(chains,ensure_ascii=False,indent=2)+'\n')
(A/'chains.js').write_text('window.ELDAMO_CHAINS = '+json.dumps(chains,ensure_ascii=False,separators=(',',':'))+';\n')
path=R/'reports'/'eldamo_38_chain_assessment.md';path.parent.mkdir(exist_ok=True)
with open(R/'data'/'eldamo_38_chain_assessment.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
counts=collections.Counter(r['grade'] for r in rows)
with open(path,'w') as f:
 f.write('# Критическая оценка дополнительных 38 цепочек Eldamo 0.8.13\n\n')
 f.write('## Границы оценки\n\nЭто оценка **доказательной обеспеченности**, а не вероятность истинности. Категория C присваивается, когда отдельные шаги имеют примеры, но непрерывная этимология не показана; D — частичная опора на примеры; U — неопределённость (отсутствие ссылок, примеров или повторное появление состояния). Никакая новая линия автоматически не получает A/B. Источники цитируются через ссылки Eldamo; письменные тексты Толкина повторно не вычитываются.\n\n')
 f.write('Категории: '+', '.join(f'**{k}: {v}**' for k,v in sorted(counts.items()))+'. Всего **38**.\n\n')
 f.write('**Важно:** поле `example_supported_steps` не доказывает, что все примеры относятся к одному слову, а совпадение звуковых состояний не доказывает сохранение окружения.\n\n')
 for r in rows:
  f.write(f"### {r['id']} — `{r['states']}` · {r['grade']}\n\n")
  f.write(f"Маркеры: `{r['markers']}`. Подтверждены примерами {r['example_supported_steps']} из {r['steps']} шагов; точная формула у {r['exact_formula_supported_steps']}.\n\n")
  f.write('**Оценка:** '+r['assessment']+'\n\n')
  for i,(ru,lab) in enumerate(zip(r['rule_urls'].split(' || '),r['rule_labels'].split(' || ')),1):
   f.write(f'- Шаг {i}: '+(f'[{lab}]({ru})' if ru else lab+' (ссылка на индивидуальное правило отсутствует)')+'\n')
  f.write('\nБлижайшие исходные цепочки: '+(r['closest_originals'] or 'совпадающих рёбер не обнаружено')+'.\n\n')
 f.write('## Методологическое ограничение\n\nЗдесь не подтверждена историческая хронология всех 38 цепочек посредством разметки свободных пояснений. При поиске в HTML категории показываются как **оценка свидетельств**, а не как доказательство допустимости пути.\n')
print('COUNTS',counts,'output',path)
