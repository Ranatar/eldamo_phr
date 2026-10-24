import csv,re,zipfile,pathlib,posixpath
from bs4 import BeautifulSoup
B=pathlib.Path('/mnt/data');z=zipfile.ZipFile(B/'eldamo-0.8.13.zip');paths=list(csv.DictReader((B/'eldamo_sound_candidate_paths.csv').open()))
urls=set(u for p in paths for u in p['rule_urls'].split(' || ')); records={}
for u in urls:
 p='eldamo-0.8.13/'+u.replace('https://eldamo.org/','');s=BeautifulSoup(z.read(p),'html.parser');main=s.find('p',id='lang-word');block=main.find_parent('div') if main else None;section=None;rows=[]
 if block is None:
  print('SKIPPED',u);records[u]=[];continue
 for n in block.find_all(recursive=False):
  if n.name=='p' and n.find('u'):section=n.find('u').get_text(' ',strip=True)
  elif section=='Phonetic Rule Examples' and n.name=='table':
   for tr in n.find_all('tr'):
    td=tr.find_all('td',recursive=False)
    if len(td)<3:continue
    forms=re.split(r'\s*[>→]\s*',td[0].get_text(' ',strip=True));
    if len(forms)!=2:continue
    refs={posixpath.normpath(posixpath.join(posixpath.dirname(p),a['href'].split('#')[0])) for a in td[2].select('a[href]') if 'word-' in a['href']}
    rows.append((forms[0],forms[1],refs,td[-1].get_text(' ',strip=True),bool(tr.select('.deleted-section')),td[1].get_text(' ',strip=True)))
 records[u]=rows
norm=lambda x:re.sub(r'\s+','',x.strip().casefold())
result=[];pairs=[]
for idx,p in enumerate(paths,1):
 us=p['rule_urls'].split(' || ');matches=[]; states=[v.strip() for v in p['states'].split(' → ')]
 def compatible(row,index):
  if index+1>=len(states):return False
  expr=re.split(r'\s*[>→]\s*',row[5]);return len(expr)==2 and norm(expr[0].strip('[]'))==norm(states[index]) and norm(expr[1].strip('[]'))==norm(states[index+1])
 for j in range(len(us)-1):
  found=[]
  for a in records[us[j]]:
   for b in records[us[j+1]]:
    if norm(a[1])==norm(b[0]) and compatible(a,j) and compatible(b,j+1):
     shared=a[2]&b[2];found.append((a,b,shared));pairs.append(dict(id=idx,join=j+1,intermediate=a[1],first=f'{a[0]} > {a[1]}',second=f'{b[0]} > {b[1]}',same_lexical_article=bool(shared),shared_articles='; '.join(sorted(shared)),same_source=bool(a[3] and a[3]==b[3]),source_first=a[3],source_second=b[3],deleted_or_obsolete=a[4] or b[4],first_rule=us[j],second_rule=us[j+1]))
  matches.append(found)
 branches=[([a],a[2]) for a in records[us[0]] if compatible(a,0)]
 for step,u in enumerate(us[1:],1):
  branches=[(chain+[b],refs&b[2]) for chain,refs in branches for b in records[u] if norm(chain[-1][1])==norm(b[0]) and compatible(b,step)]
  if not branches:break
 full=[v for v in branches if v[1]]
 result.append(dict(id=idx,states=p['states'],era=p['era'],markers=p['periods'],join_counts=';'.join(str(len(m)) for m in matches),all_joins=all(map(bool,matches)),full_form_sequence_count=len(branches),full_sequence_shared_article_count=len(full),example=' | '.join(f'{a[0]} > {a[1]}' for a in branches[0][0]) if branches else '',shared_article='; '.join(sorted(full[0][1])) if full else '',rule_urls=p['rule_urls']))
for name,rows in [('eldamo_word_chain_validation.csv',result),('eldamo_exact_word_joins.csv',pairs)]:
 with (B/name).open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('examples on',len(records),'pages');print('pair joins',len(pairs),'same article',sum(x['same_lexical_article'] for x in pairs));print('chains',len(result),'all exact',sum(x['all_joins'] for x in result),'full word',sum(bool(x['full_form_sequence_count']) for x in result),'full common article',sum(bool(x['full_sequence_shared_article_count']) for x in result))
for r in result:
 if r['full_form_sequence_count']:print('MATCH',r['id'],r['states'],r['example'][:180],r['shared_article'][:80])
