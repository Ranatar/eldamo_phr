"""Conservative word-form evidence audit for Sindarin/Noldorin candidate paths.
Uses Eldamo's Phonetic Rule Examples; no grade A is automatically granted."""
from pathlib import Path
import re,json,zipfile,posixpath,csv,collections
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent.parent
archive=P.parent/'eldamo-0.8.13.zip'
if not archive.exists():raise FileNotFoundError(archive)
z=zipfile.ZipFile(archive)
chains=json.loads((P/'app'/'chains.json').read_text())
E=json.loads((P/'app'/'edges.json').read_text())
rule_cache={}
def norm(v):return re.sub(r'\s+','',str(v).casefold()).strip('[]')
def get_rule_examples(url):
 if url in rule_cache:return rule_cache[url]
 path='eldamo-0.8.13/'+url.replace('https://eldamo.org/','').split('#')[0]
 examples=[]
 if path not in z.namelist():rule_cache[url]=examples;return examples
 soup=BeautifulSoup(z.read(path),'html.parser')
 main=soup.find('p',id='lang-word')
 block=main.find_parent('div') if main else None
 if block:
  section=''
  for el in block.find_all(recursive=False):
   if el.name=='p' and el.find('u'):section=el.find('u').get_text(' ',strip=True)
   elif section=='Phonetic Rule Examples' and el.name=='table':
    for tr in el.find_all('tr'):
     td=tr.find_all('td',recursive=False)
     if len(td)<3:continue
     forms=re.split(r'\s*(?:>|→)\s*',td[0].get_text(' ',strip=True))
     if len(forms)!=2:continue
     refs=set(posixpath.normpath(posixpath.join(posixpath.dirname(path),a['href'].split('#')[0])) for a in td[2].select('a[href]') if 'word-' in a['href'])
     examples.append({'a':forms[0],'b':forms[1], 'formula':td[1].get_text(' ',strip=True),'source':td[-1].get_text(' ',strip=True),'article_refs':refs,'deleted':bool(tr.select('.deleted-section')) or bool(td[0].select('.deleted-section'))})
 rule_cache[url]=examples
 return examples
adj=collections.defaultdict(list)
for e in E:adj[e['era'],e['a'],e['b']].append(e)
rows=[]; distributions=collections.Counter()
for chain in chains:
 states=chain['states'];urls=chain['urls'];steps=[];can_join=[]
 for a,b,url in zip(states,states[1:],urls):
  # Match exact rule page and phonetic formula to tested step
  candidates=[r for r in get_rule_examples(url) if norm(r['formula'])==norm(a+' > '+b) or re.sub(r'[\[\] ]','',r['formula'])==re.sub(r'[\[\] ]','',a+' > '+b)]
  # Formula of the record may differ from lexical realization; inspect lexical forms
  if not candidates:
   candidates=[r for r in get_rule_examples(url) if norm(r['formula'].split('>')[0])==norm(a) and norm(r['formula'].split('>')[-1])==norm(b)]
  steps.append(candidates)
 can_join=[([r],set(r['article_refs']),{r['source']},r['deleted']) for r in steps[0]] if steps else []
 for nxt in steps[1:]:
  newer=[]
  for forms,refs,sources,deleted in can_join:
   for r in nxt:
    if norm(forms[-1]['b'])!=norm(r['a']):continue
    newer.append((forms+[r],refs & set(r['article_refs']),sources & {r['source']},deleted or r['deleted']))
  can_join=newer[:1500]
 coherent=[x for x in can_join if x[1] and x[2] and x[2]!={''} and not x[3]]
 contiguous=[x for x in can_join if not x[3]]
 step_attested=sum(bool(s) for s in steps)
 # Do not confer B without textual chronological audit, even when examples join.
 if coherent:grade='C';reason='Непрерывные примеры с общей словарной статьёй и библиографической ссылкой; хронология и контекст ещё требуют текстологической проверки.'
 elif contiguous:grade='C';reason='Промежуточные словоформы стыкуются, но единая статья и источник не доказаны; требуется проверка концептуальной принадлежности.'
 elif step_attested==len(steps) and steps:grade='D';reason='Каждый переход представлен примерами соответствующей формулы, но непрерывного ряда одной словоформы не обнаружено.'
 else:grade='U';reason=f'Строго сопоставимые примеры найдены для {step_attested} из {len(steps)} переходов; этого недостаточно для оценки исторической последовательности.'
 chain['grade']=grade;chain['kind']='machine-audited';chain['reason']=reason;chain['evidence']=('Примеры с общим источником и статьёй' if coherent else 'Сопоставленные примеры отдельных правил: '+str(step_attested)+'/'+str(len(steps)))
 chain['action']='Проверить полные заметки к правилам, относительный порядок, окружение и период, прежде чем утверждать историческую последовательность.'
 if coherent:
  forms=coherent[0][0];chain['evidence']+='; формы: '+' → '.join([forms[0]['a']]+[r['b'] for r in forms])
 distributions[grade]+=1
 rows.append({'id':chain['id'],'era':chain['era'],'path':' → '.join(states),'grade':grade,'step_count':len(steps),'steps_with_formula_examples':step_attested,'word_form_joins':len(contiguous),'coherent_same_source_article':len(coherent),'reason':reason,'urls':' | '.join(urls)})
with (P/'data'/'chain_word_evidence_audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'app'/'chains.json').write_text(json.dumps(chains,ensure_ascii=False,indent=2))
(P/'app'/'chains.js').write_text('window.ELDAMO_CHAINS = '+json.dumps(chains,ensure_ascii=False)+';\n')
report=['# Проверка 118 структурных цепочек по примерам Eldamo','','Оценки предварительные, без автоматического присвоения A или B. Категория U означает отсутствие достаточных данных, не ошибочность.','','| Оценка | Количество |','|---|---:|']
for g in 'CDU':report.append(f'| {g} | {distributions[g]} |')
report +=['','## Реестр цепочек','','| ID | Цепочка | Период | Оценка | Примеров шагов | Непрерывных рядов |','|---|---|---|---|---:|---:|']
for r in rows:report.append(f"| {r['id']} | `{r['path']}` | {r['era']} | {r['grade']} | {r['steps_with_formula_examples']}/{r['step_count']} | {r['word_form_joins']} |")
report+=['','Не обнаруженные примеры и строгие несовпадения не рассматриваются как отрицательное доказательство. Требуются проверки заметок о хронологии и контекстных условиях.']
(P/'reports').mkdir(exist_ok=True)
(P/'reports'/'chain_assessment.md').write_text('\n'.join(report))
print('CHAIN ASSESSMENT',distributions)
