import csv,collections,zipfile,posixpath,re
from pathlib import Path
from bs4 import BeautifulSoup
from eldamo_interpreter_v3 import apply
P=Path(__file__).resolve().parent;Z=zipfile.ZipFile(P/'eldamo-0.8.13.zip')
def load(name):return list(csv.DictReader((P/name).open(encoding='utf-8')))
inv=load('eldamo_v2_all_rules.csv')
urls=sorted(set(x['rule_url'] for x in inv if x['rule_url'].startswith('https://eldamo.org/')))
ex={};badpages=[]
for url in urls:
 path='eldamo-0.8.13/'+url.replace('https://eldamo.org/','')
 try:s=BeautifulSoup(Z.read(path),'html.parser')
 except Exception as e:badpages.append((url,str(e)));continue
 main=s.find('p',id='lang-word');block=main.find_parent('div') if main else None
 if block is None:ex[url]=[];continue
 sec='';rows=[]
 for node in block.find_all(recursive=False):
  if node.name=='p' and node.find('u'):sec=node.find('u').get_text(' ',strip=True)
  if sec=='Phonetic Rule Examples' and node.name=='table':
   for tr in node.find_all('tr'):
    td=tr.find_all('td',recursive=False)
    if len(td)<3:continue
    forms=re.split(r'\s*[>→]\s*',td[0].get_text(' ',strip=True))
    if len(forms)!=2:continue
    ph=td[1].get_text(' ',strip=True)
    refs=[a.get('href','') for a in td[2].select('a[href]')]
    rows.append({'src_word':forms[0],'dst_word':forms[1],'example_formula':ph,'source':td[-1].get_text(' ',strip=True),'obsolete':bool(tr.select('.deleted-section')),'lexrefs':'; '.join(refs)})
 ex[url]=rows
out=[];stats=collections.Counter();tests=[]
for i,r in enumerate(inv,1):
 url=r['rule_url']; samples=ex.get(url,[])
 ok=0;no=0;unsupported=0;matching=[];errors=[]; exact_ok=0; exact_rows=0
 for e in samples:
  # do not assume all rule-page examples apply to every associated subformula
  formula=re.sub(r'\s+','',e['example_formula']).strip('[]')
  expected=re.sub(r'\s+','',r['from']+'>'+r['to']).strip('[]')
  is_exact=formula==expected
  if is_exact:exact_rows+=1
  predicted,state=apply(r['from'],r['to'],e['src_word'])
  if state.startswith(('unsupported:','error:')):unsupported+=1;errors.append(state)
  elif e['dst_word'] in predicted:
   ok+=1;exact_ok+=int(is_exact);matching.append((e['src_word'],e['dst_word']))
  else:no+=1
 if not samples:status='no_page_examples'
 elif ok:status='at_least_one_word_example_reproduced'
 elif unsupported and not no:status='unsupported_on_examples'
 else:status='no_matching_example_for_formula'
 stats[status]+=1
 out.append({'id':i,'marker':r['marker'],'from':r['from'],'to':r['to'],'rule_url':url,'page_example_rows':len(samples),'matching_example_rows':ok,'exact_formula_example_rows':exact_rows,'exact_formula_matches':exact_ok,'nonmatching_rows':no,'unsupported_rows':unsupported,'status':status,'matching_examples':' ; '.join(a+' → '+b for a,b in matching[:3]),'warnings':' ; '.join(sorted(set(errors))[:3])})
for name,rows in [('eldamo_v3_rule_example_validation.csv',out)]:
 with (P/name).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
# audit existing paths by their abstract states on all accumulated example-chain witnesses
atlas=load('eldamo_critical_101_atlas.csv'); ev=load('eldamo_strict_chain_evidence.csv');by=collections.defaultdict(list)
for e in ev:by[e['id']].append(e)
aud=[]
for r in atlas:
 states=[s.strip() for s in r['states'].split('→')]; row_tests=0;row_success=0;statusc=collections.Counter()
 for e in by[r['id']]:
  forms=[s.strip() for s in e['word_forms'].split('→')]
  if len(forms)!=len(states):continue
  states2=[]
  for a,b,w,target in zip(states,states[1:],forms,forms[1:]):
   got,st=apply(a,b,w);states2.append((target in got,st))
  row_tests+=1
  if all(k for k,_ in states2):row_success+=1
  for k,st in states2:statusc['matches' if k else st]+=1
 aud.append({'id':r['id'],'states':r['states'],'grade_prior':r['grade'],'example_sequences_tested':row_tests,'example_sequences_reproduced':row_success,'step_matches':statusc['matches'],'step_no_match':statusc['no_match'],'step_unsupported':sum(v for k,v in statusc.items() if k.startswith('unsupported:')),'note':'word-level executable check; not historical authentication'})
with (P/'eldamo_v3_101_reassessment.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=aud[0].keys());w.writeheader();w.writerows(aud)
# original 27 structural candidate lookup by normalized key of period/source/result; absence not failure
cands=load('eldamo_new_atomic_candidates.csv'); candidate_out=[]
for i,c in enumerate(cands,1):
 states=[x.strip() for x in c['states'].split('→')];marks=[x.strip() for x in c['markers'].split('→')]
 confirmations=[]
 for a,b,m in zip(states,states[1:],marks):
  subset=[r for r in inv if r['marker']==m and r['from']==a and r['to']==b]
  confirmations.append(len(subset))
 candidate_out.append({'id':i,'states':c['states'],'markers':c['markers'],'literal_inventory_edge_counts':';'.join(map(str,confirmations)),'every_edge_found':all(confirmations),'word_level_verified':False,'status':'structural; inspect rule examples and context'})
with (P/'eldamo_v3_27_reassessment.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=candidate_out[0].keys());w.writeheader();w.writerows(candidate_out)
print('unique pages',len(urls),'unread',len(badpages),'with example',sum(bool(x) for x in ex.values()),'sample rows',sum(map(len,ex.values())))
print('rule status',stats,'original 101 reproduced',sum(x['example_sequences_reproduced']>0 for x in aud),'candidate 27 all literal edges',sum(x['every_edge_found'] for x in candidate_out))
(P/'eldamo_v3_summary.json').write_text(__import__('json').dumps({'rules':len(inv),'pages':len(urls),'read_errors':badpages,'pages_with_examples':sum(bool(x) for x in ex.values()),'rule_status_counts':dict(stats),'original_101_reproduced':sum(x['example_sequences_reproduced']>0 for x in aud),'previous_27_literal_edges':sum(x['every_edge_found'] for x in candidate_out)},ensure_ascii=False,indent=2),encoding='utf-8')
