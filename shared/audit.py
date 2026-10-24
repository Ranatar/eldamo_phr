"""Common, non-silent Eldamo rule validation for both language branches.
A rule is NEVER discarded because its syntax is difficult. Executability is a separate field.
"""
import sys,csv,json,re,zipfile,posixpath,collections,importlib.util
from pathlib import Path
from bs4 import BeautifulSoup
BASE=Path(__file__).resolve().parents[1]
def load_engine():
 p=BASE/'shared/eldamo_interpreter_v3.py'; spec=importlib.util.spec_from_file_location('eldamo_executor',p); m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
engine=load_engine()
def normalize_formula(r):
 a=r.get('a') or r.get('origin') or '';b=r.get('b') or r.get('result') or ''
 return a,b

def examples(z,url):
 loc=url.partition('eldamo.org/')[2].split('#')[0]
 candidates=['eldamo-0.8.13/'+loc,loc]
 p=next((x for x in candidates if x in z.namelist()),None)
 if not p:return [],'page_not_found'
 sp=BeautifulSoup(z.read(p).decode('utf-8',errors='strict'),'html.parser'); result=[]
 # Extract only Phonetic Rule Examples: heading and following table, not other unrelated sample tables
 headings=[e for e in sp.find_all(['p','h2','h3','h4']) if e.get_text(' ',strip=True).strip(':')=='Phonetic Rule Examples']
 for h in headings:
  tab=h.find_next('table')
  if tab is None:continue
  for tr in tab.find_all('tr'):
   tds=tr.find_all('td',recursive=False)
   if len(tds)<2:continue
   forms=tds[0].get_text(' ',strip=True)
   parts=re.split(r'\s*(?:→|>)\s*',forms)
   if len(parts)!=2:continue
   result.append({'before':parts[0].strip(),'after':parts[1].strip(),'formula':tds[1].get_text(' ',strip=True),'source':tds[-1].get_text(' ',strip=True),'deprecated':bool(tr.select('.deleted-section'))})
 return result,'ok'
def audit_rows(records,archive):
 out=[];z=zipfile.ZipFile(archive);cache={}
 for i,r in enumerate(records):
  a,b=normalize_formula(r);url=r.get('url','');key=url.split('#')[0]
  if key not in cache:cache[key]=examples(z,url) if url else ([], 'no_rule_url')
  items,page_status=cache[key]; good=[];unsupported=[];miss=[];tested=0
  for ex in items:
   if ex['deprecated']:continue
   # A rule-page example can illustrate a different phonetic formula.
   if not ex['formula']:continue
   f=re.split(r'\s*(?:→|>|←|<)\s*',ex['formula'])
   if len(f)!=2:continue
   x,y=f; direction=re.search(r'[←<→>]',ex['formula']).group()
   if direction in '<←':x,y=y,x
   produced,status=engine.apply(x.strip().strip('[]'),y.strip().strip('[]'),ex['before'])
   tested+=1
   if ex['after'] in produced:good.append(ex)
   elif status.startswith('unsupported') or status.startswith('error'):unsupported.append(status)
   else:miss.append(ex)
  # Direct executable probe only if an authentic source example matches this rule's formula.
  matching=[]
  for ex in items:
   f=ex.get('formula','')
   if not f:continue
   parts=re.split(r'\s*(?:→|>|←|<)\s*',f)
   if len(parts)!=2:continue
   x,y=parts; direction=re.search(r'[←<→>]',f).group()
   if direction in '<←':x,y=y,x
   if re.sub(r'[\[\]\s]','',x)==re.sub(r'[\[\]\s]','',a) and re.sub(r'[\[\]\s]','',y)==re.sub(r'[\[\]\s]','',b):matching.append(ex)
  direct_good=0;direct_unsupported=[]
  for ex in matching:
   if ex['deprecated']:continue
   outputs,status=engine.apply(a,b,ex['before'])
   if ex['after'] in outputs:direct_good+=1
   elif status.startswith('unsupported') or status.startswith('error'):direct_unsupported.append(status)
  x=dict(r);x.update({'rule_index':i,'page_status':page_status,'rule_page_example_count':len(items),'examples_tested':tested,'page_examples_reproduced':len(good),'formula_matched_examples':len(matching),'rule_examples_reproduced':direct_good,'unsupported_example_reasons':' | '.join(sorted(set(unsupported+direct_unsupported)))[:500],'example_mismatch_count':len(miss),'validation_status':('reproduced' if direct_good else 'unsupported_on_example' if direct_unsupported else 'unverified_no_matching_example' if not matching else 'mismatch_or_context')})
  out.append(x)
 return out

def read_sindarin(p):
 with open(p,newline='') as f:
  return [dict(row) for row in csv.DictReader(f)]

def write_csv(path,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with open(path,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)

def audit_quenya(archive):
 inp=BASE/'branches/quenya/data/eldamo_v2_all_rules.csv'
 with inp.open(newline='') as f:
  records=[]
  for r in csv.DictReader(f):
   records.append({'marker':r.get('marker',''),'rule':r.get('rule',''),'a':r.get('from',''),'b':r.get('to',''),'formula':r.get('from','')+' → '+r.get('to',''), 'url':r.get('rule_url',''),'catalogs':r.get('language_cards',''),'sounds':r.get('phoneme_cards','')})
 result=audit_rows(records,archive)
 write_csv(BASE/'branches/quenya/data/rule_semantic_audit_shared.csv',result)
 stats=collections.Counter(x['validation_status'] for x in result)
 (BASE/'reports/quenya_semantic_summary.json').write_text(json.dumps({'total':len(result),'outcomes':dict(stats)},indent=2,ensure_ascii=False))
 return result

def audit_unified(branch,archive):
 src=BASE/'branches'/branch/'data/unified_rules.json'
 records=json.loads(src.read_text())
 result=audit_rows(records,archive)
 write_csv(BASE/'branches'/branch/'data/unified_semantic_audit.csv',result)
 stats=collections.Counter(x['validation_status'] for x in result)
 (BASE/'reports'/f'{branch}_unified_semantic_summary.json').write_text(json.dumps({'total':len(result),'outcomes':dict(stats)},indent=2,ensure_ascii=False))
 return result

def audit_sindarin(archive):
 inp=BASE/'branches/sindarin/data/rule_inventory.csv'; data=read_sindarin(inp)
 result=audit_rows(data,archive);write_csv(BASE/'branches/sindarin/data/rule_semantic_audit.csv',result)
 summary=collections.Counter(r['validation_status'] for r in result)
 (BASE/'reports/sindarin_semantic_summary.json').write_text(json.dumps({'total':len(result),'outcomes':dict(summary),'unsupported_rule_count':sum(bool(x['unsupported_example_reasons']) for x in result)},indent=2,ensure_ascii=False))
 return result
if __name__=='__main__':
 if len(sys.argv)<2:raise SystemExit('Usage: python shared/audit.py /path/to/eldamo-0.8.13.zip')
 q=audit_unified('quenya',sys.argv[1]);a=audit_unified('sindarin',sys.argv[1]);print('QUENYA',len(q),collections.Counter(x['validation_status'] for x in q));print('SINDARIN',len(a),collections.Counter(x['validation_status'] for x in a))
