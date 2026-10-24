import runpy,csv,collections,pathlib,re
P=pathlib.Path('/mnt/data')
# output inventory previously built; only pure literal strings as whole input/output (no context, no placeholders)
rows=list(csv.DictReader((P/'eldamo_extended_rule_inventory.csv').open(encoding='utf-8')))
mapmark={'✶':('late',0),'AQ.':('late',1),'Q.':('late',2),'ᴹ✶':('middle',0),'ᴹAQ.':('middle',1),'ᴹQ.':('middle',2)}
original=set(tuple(r[x] for x in ['era','marker','from','to','rule_url']) for r in csv.DictReader((P/'eldamo_sound_edges.csv').open(encoding='utf8')))
# conservative excludes boundary, metacharacters, complexes, and strings without letters
bad=re.compile(r'[|{}\[\](),+*/?VCXSø-]')
links=[]
for r in rows:
 if r['marker'] not in mapmark:continue
 if not r['parser_status'].startswith('supported'):continue
 variants=r['parsed_variants'].split('; ')
 for v in variants:
  a,sep,b=v.partition(' → ')
  if not sep or not a or not b or a==b or bad.search(a+b):continue
  era,stage=mapmark[r['marker']]
  links.append(dict(era=era,stage=stage,marker=r['marker'],src=a,dst=b,url=r['rule_url'],rule=r['rule']))
by=collections.defaultdict(list)
for e in links:by[(e['era'],e['src'])].append(e)
paths={}
for a in links:
 for b in by[(a['era'],a['dst'])]:
  if b['stage']<=a['stage']:continue
  for path in ([a,b],):
   k=tuple((x['marker'],x['src'],x['dst'],x['url']) for x in path)
   paths[k]=path
  for c in by[(a['era'],b['dst'])]:
   if c['stage']<=b['stage']:continue
   path=[a,b,c];k=tuple((x['marker'],x['src'],x['dst'],x['url']) for x in path);paths[k]=path
new=[]
for p in paths.values():
 if any((e['era'],e['marker'],e['src'],e['dst'],e['url']) not in original for e in p):new.append(p)
with (P/'eldamo_new_atomic_candidates.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['states','markers','rules','urls','status'])
 for p in new:w.writerow([' → '.join([p[0]['src']]+[e['dst'] for e in p]),' → '.join(e['marker'] for e in p),' || '.join(e['rule'] for e in p),' || '.join(e['url'] for e in p),'structural candidate only; not historically validated'])
print('conservative atomic edges',len(links),'total paths',len(paths),'new paths',len(new))
