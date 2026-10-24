import csv,zipfile,pathlib,posixpath,re,collections,json
from bs4 import BeautifulSoup
B=pathlib.Path('/mnt/data'); Z=zipfile.ZipFile(B/'eldamo-0.8.13.zip')
P=list(csv.DictReader((B/'eldamo_sound_candidate_paths.csv').open(encoding='utf8')))
C={r['rule_url']:r for r in csv.DictReader((B/'eldamo_rule_commentary_audit.csv').open(encoding='utf8'))}
urls={u for p in P for u in p['rule_urls'].split(' || ') if u}; records={}
for url in urls:
 path='eldamo-0.8.13/'+url.replace('https://eldamo.org/',''); soup=BeautifulSoup(Z.read(path),'html.parser'); main=soup.find('p',id='lang-word'); block=main.find_parent('div') if main else None
 rows=[];section=''
 if block:
  for el in block.find_all(recursive=False):
   if el.name=='p' and el.find('u'):section=el.find('u').get_text(' ',strip=True)
   elif section=='Phonetic Rule Examples' and el.name=='table':
    for tr in el.find_all('tr'):
     td=tr.find_all('td',recursive=False)
     if len(td)<3:continue
     form=re.split(r'\s*[>→]\s*',td[0].get_text(' ',strip=True))
     if len(form)!=2:continue
     refs={posixpath.normpath(posixpath.join(posixpath.dirname(path),a['href'].split('#')[0])) for a in td[2].select('a[href]') if 'word-' in a['href']}
     rows.append(dict(a=form[0],b=form[1],refs=refs,source=td[-1].get_text(' ',strip=True),deleted=bool(tr.select('.deleted-section')) or bool(td[0].select('.deleted-section')),formula=td[1].get_text(' ',strip=True)))
 records[url]=rows
norm=lambda s:re.sub(r'\s+','',s.casefold())
for_rule=lambda s:tuple(norm(t.strip(' []')) for t in re.split(r'\s*[>→]\s*',s))
output=[]; proof=[]; total_complete=0
for i,p in enumerate(P,1):
 urls=p['rule_urls'].split(' || '); states=p['states'].split(' → ')
 steps=[]
 for j,url in enumerate(urls):
  candidates=[r for r in records.get(url,[]) if for_rule(r['formula'])==(norm(states[j]),norm(states[j+1]))] if j+1<len(states) else []
  steps.append(candidates)
 # chain enumeration, cap combinatorial duplicates by state + sources + refs + deletion
 chains=[([r],r['refs'], {r['source']},r['deleted']) for r in steps[0]] if steps else []
 for ss in steps[1:]:
  new=[]
  for chain,refs,sources,deleted in chains:
   for row in ss:
    if norm(chain[-1]['b'])!=norm(row['a']):continue
    common=refs&row['refs']; source_common=sources&{row['source']}
    new.append((chain+[row],common,source_common,deleted or row['deleted']))
  chains=new
  if not chains:break
 complete=len(chains)
 # exact source and exact same article for every step; not just either
 coherent=[(ch,ref,src,del_) for ch,ref,src,del_ in chains if ref and src and src!={''}]
 clean=[z for z in coherent if not z[3]]
 strong=[z for z in clean if not any(C.get(u,{}).get('rule_language','') not in ('Primitive Elvish','Middle Primitive Elvish','Ancient Quenya','Middle Ancient Quenya','Quenya','Middle Quenya') for u in urls)]
 langs=[C.get(u,{}).get('rule_language','UNKNOWN') for u in urls]
 foreign=any(l not in ('Primitive Elvish','Middle Primitive Elvish','Ancient Quenya','Middle Ancient Quenya','Quenya','Middle Quenya') for l in langs)
 # conservative labels: none is proven, as source match is not chronology verification
 if foreign: status='LANGUAGE_CONFLICT_REVIEW'
 elif strong: status='COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW'
 elif clean: status='MATCHED_SOURCE_BUT_LANGUAGE_REVIEW'
 elif coherent: status='ONLY_OBSOLETE_OR_DELETED_EXAMPLES'
 elif complete: status='FORM_CHAIN_WITHOUT_COMMON_SOURCE_AND_ARTICLE'
 else:status='NO_CONTINUOUS_WORD_FORMS'
 chosen=(strong or clean or coherent or chains)
 if chosen:
  ch,refs,sources,del_=chosen[0]; example=' → '.join([ch[0]['a']]+[r['b'] for r in ch]);src='; '.join(sorted(sources));art='; '.join(sorted(refs))
 else:example=src=art=''
 cautions=[]
 for u in urls:
  c=C.get(u,{})
  if c.get('caution_terms'):cautions.append(c['caution_terms'])
 output.append(dict(id=i,states=p['states'],era=p['era'],rules=p['rules'],status=status,continuous_examples=complete,shared_source_and_article=len(coherent),clean_same_source_article=len(clean),non_foreign_clean=len(strong),languages=' → '.join(langs),example=example,matched_primary_source=src,matched_lexical_article=art,rule_urls=p['rule_urls'],commentary_warning_terms='; '.join(dict.fromkeys(cautions))))
 for ch,refs,sources,deleted in (strong or clean or coherent)[:10]:
  proof.append(dict(id=i,word_forms=' → '.join([ch[0]['a']]+[r['b'] for r in ch]),source='; '.join(sorted(sources)),article='; '.join(sorted(refs)),deleted=deleted,rule_urls=p['rule_urls']))
with (B/'eldamo_strict_chain_audit.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=output[0]);w.writeheader();w.writerows(output)
with (B/'eldamo_strict_chain_evidence.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=proof[0] if proof else ['id']);w.writeheader();w.writerows(proof)
# Second-pass anomaly screen: spelling-level example must change at EACH step
for r in output:
 if r['status']=='COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW' and r['example']:
  forms=r['example'].split(' → ')
  if any(norm(a)==norm(b) for a,b in zip(forms,forms[1:])):
   r['status']='ANNOTATION_OR_UNCHANGED_FORM_REVIEW'
# Rewrite machine audit after anomaly labels
with (B/'eldamo_strict_chain_audit.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=output[0]);w.writeheader();w.writerows(output)
counts=collections.Counter(r['status'] for r in output)
lines=['# Проверка сквозных фонетических цепочек Eldamo 0.8.13: строгий этап','', '## Метод и границы доказательства','','Исследованы 101 формальный кандидат и примеры в HTML-карточках фонетических правил из локального архива. Для полной последовательности требуется: (1) соответствие формулы в каждой строке примера ребру графа; (2) буквальное равенство промежуточных **словоформ**; (3) общий идентификатор словарной статьи **на всех шагах**; (4) одинаковая библиографическая ссылка **на всех шагах**; (5) отсутствие метки `deleted-section` для приоритетного класса; (6) принадлежность страниц правила к одному из шести рассматриваемых языковых каталогов.','','**Статус «подтверждена история слова» не присваивается автоматически**: одинаковая библиографическая ссылка не удостоверяет порядок реализации законов, условия и редакционную совместимость. Встречающиеся в заметках оговорки требуют отдельной филологической интерпретации.','','## Статистика','','| Машинный статус | Цепочек |','|---|---:|']
for k,v in counts.most_common():lines.append(f'| `{k}` | {v} |')
lines+=['',f'Полных склеек с одинаковой статьёй и источником, без явной пометы удалённого примера, на страницах шести целевых языков: **{sum(r['status']=='COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW' for r in output)} цепочек**. Это **кандидаты на углублённую филологическую проверку**, а не окончательные реконструкции.','','## Приоритетные линии со сквозными примерами','','| ID | Звуковая линия | Полные формы | Первичный источник | Статус |','|---:|---|---|---|---|']
for r in output:
 if r['status']=='COHERENT_EXAMPLES_NEEDS_TEXTUAL_REVIEW':
  lines.append('| '+ ' | '.join([str(r['id']), '`'+r['states']+'`','`'+r['example'].replace('|','/')[:90]+'`',r['matched_primary_source'][:60],r['status']])+' |')
lines+=['','## Случаи, требующие отдельной проверки','','| ID | Звуки | Причина |','|---:|---|---|']
for r in output:
 if r['status'] in ('LANGUAGE_CONFLICT_REVIEW','ONLY_OBSOLETE_OR_DELETED_EXAMPLES','FORM_CHAIN_WITHOUT_COMMON_SOURCE_AND_ARTICLE','ANNOTATION_OR_UNCHANGED_FORM_REVIEW'):
  lines.append(f'| {r["id"]} | `{r["states"]}` | `{r["status"]}` |')
lines+=['','## Как читать данные','','- `eldamo_strict_chain_audit.csv` — отдельный статус для всех 101 цепочек.','- `eldamo_strict_chain_evidence.csv` — примеры с одинаковой ссылкой на статью и первоисточник, до 10 для каждой цепочки.','- Поля `languages` и `rule_urls` помогают перепроверить, не происходит ли смешение Telerin/Sindarin с Quenya.','- `commentary_warning_terms` — сигнальные слова из пояснений, а не автоматическая интерпретация исключений.','- Этот этап ограничен исходными 101 кандидатами, полученными упрощённым графом; он не доказывает полноту всех возможных звуковых цепочек.']
(B/'eldamo_strict_chain_report.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('COUNTS',counts,'evidence',len(proof),'output',len(output))
