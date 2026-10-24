"""Build Sindarin interface from Quenya's actual UI source; no separately rewritten UI.
Input Sindarin inventory remains full, not only literal edges. Semantic audit is retained.
"""
from pathlib import Path
import json,re,shutil,hashlib
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
Q=ROOT/'branches/quenya/app';S=ROOT/'branches/sindarin/app';S.mkdir(exist_ok=True)
S0=ROOT/'branches/sindarin'
phonemes=json.loads((S0/'data/phonemes.json').read_text());syms=sorted(phonemes)
raw_edges=json.loads((S0/'data/atomic_edges_unified.json').read_text())
raw_records=json.loads((S0/'data/complete_rules.json').read_text())
raw_chains=json.loads((S0/'data/unified_assessed_chains.json').read_text())
raw_rules={}
for r in raw_records:
 for sym in r['sounds']:
  raw_rules.setdefault(sym,[]).append({'marker':r['marker'],'rule':r['rule'],'formula':r['formula'],'url':r['url'],'catalogs':', '.join(r['catalogs']),'source':', '.join(r['refs'])})
audit={}
import csv
with (S0/'data/unified_semantic_audit.csv').open() as f:
 for r in csv.DictReader(f):
  key=(r['marker'],r['rule'],r['formula'],r['url']);audit.setdefault(key,r)
# Normalize Sindarin data onto the exact Quenya UI data contract (no special Sindarin presentation code).
normalized_rules={}
for sym,items in raw_rules.items():
 normalized_rules[sym]=[]
 for r in items:
  key=(r['marker'],r['rule'],r['formula'],r['url']);a=audit.get(key,{})
  normalized_rules[sym].append({'marker':r['marker'],'title':r['rule'],'formula':r['formula'],'url':r['url'],'langs':r['catalogs'],'sources':[[v.strip(),'https://eldamo.org/'] for v in r.get('source','').split(',') if v.strip()], 'audit':a.get('validation_status','not_audited')})
# Preserve original evidence fields and support filtering only for verified examples.
normalized_edges=[]
for edge in raw_edges:
 e=edge.copy();e['cards']=e.get('cards','');e['tested']=int(bool(e.get('tested')));e['exact']=int(bool(e.get('exact')))
 # Evidence is calculated per exact rule formula in the shared semantic audit.
 for r in audit.values():
  if r['url']==e.get('url') and r['marker']==e.get('marker') and r['a']==e.get('a') and r['b']==e.get('b'):
   if int(r.get('rule_examples_reproduced',0))>0:e['tested']=1;e['exact']=1
   break
 normalized_edges.append(e)
for c in raw_chains:
 c.setdefault('urls',c.get('rule_urls',[]));c.setdefault('rules',[])
 c.setdefault('reason','Не установлено');c.setdefault('action','Проверить контекст и хронологию')
# Use exact same styles and application program; only language configuration and data differ.
shutil.copy2(Q/'styles.css',S/'styles.css')
js=(Q/'app.js').read_text()
js=re.sub(r'const PHONEMES = \[.*?\];', 'const PHONEMES = '+json.dumps(syms,ensure_ascii=False)+';',js,count=1,flags=re.S)
js=js.replace("const vals = { from: 'b', to: 'f' }", "const vals = { from: 'p', to: 'f' }")
js=js.replace(" : 'b');", " : 'p');")
js=js.replace("src === 'b' && dst === 'f'", "false")
js=js.replace('Для b каталог содержит b → β → v, а не b → f; f образуется, например, из ɸ. Для b → f нет соединяющего правила в индексированной выборке.', 'Проверьте альтернативные фонетические окружения и период.')
js=js.replace("const ranking = { 'Q.': 0, 'ᴹQ.': 1, 'AQ.': 2, 'ᴹAQ.': 3, '✶': 4, 'ᴹ✶': 5 };", "const ranking = { 'S.': 0, 'OS.': 1, 'AT.': 2, '✶': 3, 'N.': 4, 'ON.': 5, 'ᴹ✶': 6 };")
js=js.replace("'—': 'Не оценена'", "'—': 'Не оценена', unassessed: 'Не оценена'")
js=js.replace('A–X/U — оценки 139 исследованных цепочек; вновь найденные поиском пути не оценены.', 'Оценки цепочек предварительны; вновь найденные пути не оценены.')
(S/'app.js').write_text(js)
sp=BeautifulSoup((Q/'index.html').read_text(),'html.parser')
sp.title.string='Eldamo — Sindarin / Noldorin · фонетический атлас'
sp.find('h1').string='Атлас звуковых путей Sindarin / Noldorin'
hdr=sp.find('header');hdr.find('div').string='Поздняя ветвь: Primitive → Ancient Telerin → Old Sindarin → Sindarin · Средняя: Middle Primitive → Old Noldorin → Noldorin'
for o in sp.select('#era option'):
 if o.get('value')=='late':o.string='Поздняя концепция (Sindarin)'
 if o.get('value')=='middle':o.string='Средняя концепция (Noldorin)'
# IPA semantic navigation based on original Quenya articulation table; add missing sounds in dedicated block.
qset={b.get('data-phoneme') for b in sp.select('button.ipa-sound')}
new_sounds=[s for s in syms if s not in qset]
for slot in ('from','to'):
 area=sp.find(id=slot+'-ipa')
 for b in area.select('button.ipa-sound'):
  if b['data-phoneme'] not in syms:b['disabled']='';b['title']='Не включено в выбранную синдаринскую ветвь'
 if new_sounds:
  h=sp.new_tag('h3');h.string='Дополнительные исторические обозначения Eldamo';area.append(h)
  tb=sp.new_tag('table');body=sp.new_tag('tbody');tb.append(body)
  for j in range(0,len(new_sounds),9):
   tr=sp.new_tag('tr')
   for s in new_sounds[j:j+9]:
    td=sp.new_tag('td');b=sp.new_tag('button',attrs={'type':'button','class':'ipa-sound','data-phoneme':s});b.string=s;td.append(b);tr.append(td)
   body.append(tr)
  area.append(tb)
sp.select_one('#chain-atlas p').string=f'{len(raw_chains)} синдаринских цепочек, оценки предварительные и не переносятся из квенийского атласа.'
# preserve previous status options; no retroactive evidence upgrade
sel=sp.select_one('#atlas-grade')
if sel and not sel.select_one('option[value="unassessed"]'):
 opt=sp.new_tag('option',value='unassessed');opt.string='Не оценена';sel.append(opt)
(S/'index.html').write_text(str(sp))
(S/'rules.json').write_text(json.dumps(normalized_rules,ensure_ascii=False,indent=2))
(S/'edges.json').write_text(json.dumps(normalized_edges,ensure_ascii=False,indent=2))
(S/'data.js').write_text('window.ELDAMO_EDGES = '+json.dumps(normalized_edges,ensure_ascii=False)+';\nwindow.ELDAMO_RULES = '+json.dumps(normalized_rules,ensure_ascii=False)+';\n')
(S/'chains.js').write_text('window.ELDAMO_CHAINS = '+json.dumps(raw_chains,ensure_ascii=False)+';\n')
# Build a true single-file standalone from these exact modules
html=(S/'index.html').read_text()
html=re.sub(r'<link\s+href="styles.css"\s+rel="stylesheet"\s*/?>',lambda m:'<style>\n'+(S/'styles.css').read_text()+'\n</style>',html)
for n in ('data.js','chains.js','app.js'):
 html=re.sub(r'<script\b[^>]*\bsrc="'+n+r'"[^>]*>\s*</script>',lambda m:'<script>\n'+(S/n).read_text()+'\n</script>',html)
for n in ('data.js','chains.js','app.js'):
 assert ('src="'+n+'"') not in html,n
(S/'standalone.html').write_text(html)
# Cross-interface contract: DOM control ids and JS baseline exports match.
q_ids={x.get('id') for x in BeautifulSoup((Q/'index.html').read_text(),'html.parser').select('[id]')}
s_ids={x.get('id') for x in sp.select('[id]')}
assert q_ids==s_ids, {'missing':sorted(q_ids-s_ids),'extra':sorted(s_ids-q_ids)}
assert (Q/'styles.css').read_bytes()==(S/'styles.css').read_bytes()
print('same control IDs:',len(q_ids),'new phonemes:',len(new_sounds),'edges:',len(normalized_edges),'verified edge examples:',sum(e['exact'] for e in normalized_edges))
