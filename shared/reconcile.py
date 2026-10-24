"""Lossless reconciliation of raw Eldamo formulas and previously expanded variants.
One algorithm for both branches. Distinct rule links and labels are never collapsed.
Legacy-derived variants are explicitly labeled, not misrepresented as new citations.
"""
import json,csv,collections,re
from pathlib import Path
from .audit import BASE
MARKER={'Q.':('late',2),'ᴹQ.':('middle',2),'AQ.':('late',1),'ᴹAQ.':('middle',1),'✶':('late',0),'ᴹ✶':('middle',0),'S.':('late',3),'OS.':('late',2),'AT.':('late',1),'N.':('middle',2),'ON.':('middle',1)}

def reconcile(branch):
 folder=BASE/'branches'/branch/'data';new=json.loads((folder/'unified_rules.json').read_text())
 oldfile=folder/('eldamo_v2_all_rules.csv' if branch=='quenya' else 'rule_inventory.csv')
 with oldfile.open(newline='') as f:legacy=list(csv.DictReader(f))
 out=[{**r,'provenance':'direct_eldamo_phoneme_card'} for r in new]
 bypath=collections.defaultdict(list)
 for i,r in enumerate(out):bypath[(r['marker'],r['a'],r['b'])].append(i)
 added=[];existing=0
 for r in legacy:
  marker=r['marker'];a=r.get('from',r.get('a',''));b=r.get('to',r.get('b',''))
  key=(marker,a,b)
  if key in bypath:
   existing+=1;continue
  era,stage=MARKER[marker]
  n={'era':era,'stage':stage,'marker':marker,'rule':r.get('rule','[без названия]'),
   'a':a,'b':b,'formula':r.get('formula') or a+' → '+b,
   'url':r.get('rule_url',r.get('url','')), 'catalogs':(r.get('language_cards','') or r.get('catalogs','')).replace(';',',').split(','),
   'sounds':(re.findall(r'\[([^\]]+)\]',r.get('phoneme_cards','') or r.get('sounds','')) or [r.get('phoneme_cards','') or r.get('sounds','')]), 'refs':[],
   'provenance':'legacy_expanded_variant_not_found_in_direct_extraction',
   'legacy_parser_status':r.get('parser_status','')}
  out.append(n);bypath[key].append(len(out)-1);added.append(n)
 (folder/'complete_rules.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 (folder/'legacy_variant_recovery.json').write_text(json.dumps(added,ensure_ascii=False,indent=2))
 return {'branch':branch,'direct_records':len(new),'prior_records':len(legacy),'prior_matched':existing,'restored_legacy_variants':len(added),'total_records':len(out)}
if __name__=='__main__':
 for branch in ['quenya','sindarin']:print(reconcile(branch))
