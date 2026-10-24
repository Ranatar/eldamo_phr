"""Common chain evidence evaluation. C is only a provisional category when
all attested intermediate wordforms join AND source/article IDs match.
No automatic A or B. Empty examples = unknown, not disproved.
"""
import json,zipfile,re,posixpath,collections,csv
from pathlib import Path
from bs4 import BeautifulSoup
from .audit import BASE

def norm(x):return re.sub(r'\s+','',str(x).casefold()).strip('[]')
def extract(z,url):
 path='eldamo-0.8.13/'+url.replace('https://eldamo.org/','').split('#')[0]
 if path not in z.namelist():return []
 sp=BeautifulSoup(z.read(path).decode('utf-8',errors='strict'),'html.parser');main=sp.find('p',id='lang-word')
 block=main.find_parent('div') if main else None
 out=[]
 if block:
  section=''
  for element in block.find_all(recursive=False):
   if element.name=='p' and element.find('u'):section=element.find('u').get_text(' ',strip=True)
   elif section=='Phonetic Rule Examples' and element.name=='table':
    for tr in element.find_all('tr'):
     cells=tr.find_all('td',recursive=False)
     if len(cells)<3:continue
     forms=re.split(r'\s*(?:→|>)\s*',cells[0].get_text(' ',strip=True))
     if len(forms)!=2:continue
     refs=set(posixpath.normpath(posixpath.join(posixpath.dirname(path),a['href'].split('#')[0])) for a in cells[2].select('a[href]') if 'word-' in a['href'])
     out.append({'before':forms[0],'after':forms[1], 'formula':cells[1].get_text(' ',strip=True),'source':cells[-1].get_text(' ',strip=True),'refs':refs,'deleted':bool(tr.select('.deleted-section'))})
 return out

def join_examples_exact(steps):
 """Exact dynamic programming for contiguous examples. No arbitrary enumeration cap.
 State tracks the last form and the intersections of article IDs and sources.
 Multiplicities count all alternative row sequences; witness preserves one path.
 """
 if not steps or any(not step for step in steps):return {'contiguous':0,'coherent':0,'witness':None,'states':0}
 current={}
 for row in steps[0]:
  if row['deleted']:continue
  key=(norm(row['after']),frozenset(row['refs']),frozenset([row['source']]) if row['source'] else frozenset())
  count,witness=current.get(key,(0,None))
  current[key]=(count+1,witness or (row,))
 maxstates=len(current)
 for following in steps[1:]:
  nxt={}
  for (last,refs,sources),(count,witness) in current.items():
   for row in following:
    if row['deleted'] or last!=norm(row['before']):continue
    key=(norm(row['after']), refs.intersection(row['refs']), sources.intersection([row['source']]) if row['source'] else frozenset())
    n,old=nxt.get(key,(0,None))
    nxt[key]=(n+count,old or witness+(row,))
  current=nxt
  maxstates=max(maxstates,len(current))
 coherent=[(count,witness) for (_,refs,sources),(count,witness) in current.items() if refs and sources]
 return {'contiguous':sum(c for c,_ in current.values()),'coherent':sum(c for c,_ in coherent),
         'witness':coherent[0][1] if coherent else None,'states':maxstates}

def evaluate(branch,archive):
 root=BASE/'branches'/branch;d=root/'data';z=zipfile.ZipFile(archive)
 chains=json.loads((d/'unified_structural_chains.json').read_text());edges=json.loads((d/'atomic_edges_unified.json').read_text())
 lookup=collections.defaultdict(list)
 for e in edges:lookup[e['era'],e['a'],e['b'],e['url']].append(e)
 cache={};stats=collections.Counter();report=[]
 for c in chains:
  states=c['states'];urls=c['urls'];era=c['era'];sequences=[];steps=[];statuses=[]
  for a,b,url in zip(states,states[1:],urls):
   if url not in cache:cache[url]=extract(z,url)
   exact=[]
   for r in cache[url]:
    if r['deleted']:continue
    formula=r['formula'].replace('←','<').replace('→','>')
    m=re.split(r'\s*[<>]\s*',formula)
    if len(m)!=2:continue
    source,target=m
    if '<' in formula:source,target=target,source
    if norm(source)==norm(a) and norm(target)==norm(b):exact.append(r)
   steps.append(exact)
  joined=join_examples_exact(steps)
  coherent_count=joined['coherent']
  contiguous_count=joined['contiguous']
  available=sum(bool(step) for step in steps)
  if coherent_count:
   grade='C';reason='Непрерывные формы в примерах правил с общей словарной статьёй и библиографическим источником; хронология требует проверки.'
   c['evidence']=' → '.join([joined['witness'][0]['before']]+[s['after'] for s in joined['witness']])
  elif contiguous_count:
   grade='U';reason='Непрерывные формы наблюдаются в примерах разных правил, однако не установлены общая словарная статья и библиографический источник: это не доказательство единой этимологии.'
  elif available==len(steps) and steps:
   grade='D';reason='Есть примеры отдельных точных формул, однако нет непрерывной истории одного слова.'
  else:
   grade='U';reason=f'Примеры точных формул найдены для {available} из {len(steps)} шагов; историческая применимость остаётся открытой.'
  c['grade']=grade;c['kind']='machine-audited';c['reason']=reason
  c['action']='Проверить фонетическое окружение, диалект, редакцию Толкина и относительную хронологию.'
  c['step_evidence_count']=available;c['whole_word_attested']=bool(coherent_count)
  report.append({'id':c['id'],'era':era,'path':' → '.join(states),'grade':grade,'attested_steps':available,'steps':len(steps),'coherent_examples':coherent_count,'contiguous_examples':contiguous_count,'coherent_source_and_article':bool(coherent_count),'dp_max_states':joined['states'],'urls':' | '.join(urls)})
  stats[grade]+=1
 (d/'unified_assessed_chains.json').write_text(json.dumps(chains,ensure_ascii=False,indent=2))
 with (d/'unified_chain_assessment.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(report[0]) if report else []);w.writeheader();w.writerows(report)
 return {'branch':branch,'number':len(chains),'distribution':dict(stats)}
if __name__=='__main__':
 import sys
 for b in ['quenya','sindarin']:print(evaluate(b,sys.argv[1]))
