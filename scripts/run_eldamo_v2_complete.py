import csv,collections,pathlib,re
from eldamo_interpreter_v2 import apply,variants
P=pathlib.Path('/mnt/data')
def load(n):return list(csv.DictReader((P/n).open(encoding='utf8')))
inv=load('eldamo_extended_rule_inventory.csv');old=load('eldamo_recovered_exclusions.csv');atlas=load('eldamo_critical_101_atlas.csv');evid=load('eldamo_strict_chain_evidence.csv');new=load('eldamo_new_atomic_candidates.csv')
allrule=[]
for r in inv:
 try:
  opts=variants(r['from'],r['to']);status='parsed'; details=len(opts)
 except Exception as exc:status='unresolved: '+str(exc);details=0
 # try on synthetic source to avoid false claim of executable proof
 allrule.append({**r,'v2_syntax':status,'v2_variants':details})
with (P/'eldamo_v2_all_rules.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(allrule[0]));w.writeheader();w.writerows(allrule)
nov=[];index={(r['marker'],r['from'],r['to'],r['rule_url']):r for r in allrule}
for r in old:
 key=(r['marker'],r['source'],r['result'],r['url']);x=index.get(key,{})
 nov.append({**r,'v2_syntax':x.get('v2_syntax','not matched'),'v2_variants':x.get('v2_variants','')})
with (P/'eldamo_v2_recovered_exclusions.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(nov[0]));w.writeheader();w.writerows(nov)
byid=collections.defaultdict(list)
for r in evid:byid[int(r['id'])].append(r)
results=[]
for r in atlas:
 states=[x.strip() for x in r['states'].split('→')];full=0;tested=0;matched=0;notmatch=[];sourcecount=0
 for e in byid[int(r['id'])]:
  forms=[x.strip() for x in e['word_forms'].split('→')]
  if len(forms)!=len(states):continue
  hits=[]
  for a,b,w,target in zip(states,states[1:],forms,forms[1:]):
   outputs,status=apply(a,b,w);hits.append(target in outputs);tested+=1;matched+=int(target in outputs)
  if hits and all(hits):full+=1;sourcecount+=1
  elif len(notmatch)<2:notmatch.append(' → '.join(forms))
 results.append({'id':r['id'],'states':r['states'],'prior_grade':r['grade'],'example_steps_tested':tested,'example_steps_matched':matched,'full_examples_reproduced':full,'status':'reproduced example' if full else ('partial example' if matched else 'no complete evidence example'),'example_failure_samples':' | '.join(notmatch)})
with (P/'eldamo_v2_101_recheck.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
newrows=[]
for i,r in enumerate(new,1):
 states=[x.strip() for x in r['states'].split('→')]; marks=[x.strip() for x in r['markers'].split('→')]
 # structural recheck by extracting matched inventory edges and missing supporting evidence; whole word cannot be claimed
 matches=[]
 for a,b,m in zip(states,states[1:],marks):
  matching=[x for x in allrule if x['marker']==m and x['v2_syntax']=='parsed' and (a,b) in variants(x['from'],x['to'])]
  matches.append(bool(matching))
 newrows.append({'id':i,'states':r['states'],'markers':r['markers'],'all_edges_found':all(matches),'sound_only_status':'structural candidate; no word-level demonstration','requires':'test lexical examples, chronology, context and dialect'})
with (P/'eldamo_v2_27_recheck.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(newrows[0]));w.writeheader();w.writerows(newrows)
# graph: atomic edges only, no arbitrary context edges; compare genuinely expanded candidates without overwriting older 27
markers={'✶':('late',0),'AQ.':('late',1),'Q.':('late',2),'ᴹ✶':('middle',0),'ᴹAQ.':('middle',1),'ᴹQ.':('middle',2)}
atom=[];pat=re.compile(r'[VCXSø{}|\-\[\]()?,*]')
for r in allrule:
 if r['marker'] not in markers or r['v2_syntax']!='parsed':continue
 for a,b in variants(r['from'],r['to']):
  if not a or not b or a==b or pat.search(a+b):continue
  era,stage=markers[r['marker']];atom.append({'from':a,'to':b,'mark':r['marker'],'era':era,'stage':stage,'url':r['rule_url']})
by=collections.defaultdict(list)
for r in atom:by[(r['era'],r['from'])].append(r)
chains={}
for a in atom:
 for b in by[a['era'],a['to']]:
  if b['stage']<=a['stage']:continue
  path=[a,b];chains[tuple((e['mark'],e['from'],e['to'],e['url']) for e in path)]=path
  for c in by[a['era'],b['to']]:
   if c['stage']<=b['stage']:continue
   p=[a,b,c];chains[tuple((e['mark'],e['from'],e['to'],e['url']) for e in p)]=p
with (P/'eldamo_v2_structural_candidates.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['states','markers','rule_urls','status'])
 for p in chains.values():w.writerow([' → '.join([p[0]['from']]+[e['to'] for e in p]),' → '.join(x['mark'] for x in p),' || '.join(x['url'] for x in p),'structural only'])
print('inventory',len(inv),'syntax parsed',sum(r['v2_syntax']=='parsed' for r in allrule),'excluded',len(old),'excluded parsed',sum(r['v2_syntax']=='parsed' for r in nov),'101',len(results),'fully reproduced',sum(r['full_examples_reproduced']>0 for r in results),'27',len(newrows),'edges matched',sum(r['all_edges_found'] for r in newrows),'atomic',len(atom),'new total structural paths',len(chains))
