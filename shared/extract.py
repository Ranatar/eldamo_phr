"""One shared phoneme-card extractor for both research branches.
Does not infer direction from presentation language; preserves direction and original HTML formula.
Never discards contextual rules merely because they cannot become simple edges.
"""
import json,zipfile,re,posixpath,collections,csv,sys
from pathlib import Path
from bs4 import BeautifulSoup,Tag
ROOT=Path(__file__).resolve().parents[1]
CONFIGS={
 'quenya':[('q','Q.','late',2),('mq','ᴹQ.','middle',2),('aq','AQ.','late',1),('maq','ᴹAQ.','middle',1),('p','✶','late',0),('mp','ᴹ✶','middle',0)],
 'sindarin':[('s','S.','late',3),('os','OS.','late',2),('at','AT.','late',1),('p','✶','late',0),('n','N.','middle',2),('on','ON.','middle',1),('mp','ᴹ✶','middle',0)]}
LANGUAGE_NAMES={'q':'Quenya','mq':'Middle Quenya','aq':'Ancient Quenya','maq':'Middle Ancient Quenya','p':'Primitive Elvish','mp':'Middle Primitive Elvish','s':'Sindarin','os':'Old Sindarin','at':'Ancient Telerin','n':'Noldorin','on':'Old Noldorin'}
PREFIX='eldamo-0.8.13/content/'
MARKERS={branch:{marker:(era,stage) for code,marker,era,stage in cfg} for branch,cfg in CONFIGS.items()}

def parse(archive,branch):
 cfg=CONFIGS[branch];z=zipfile.ZipFile(archive);out=[];errors=[];sounds=collections.defaultdict(set)
 def loc(frompath,href):return posixpath.normpath(posixpath.join(posixpath.dirname(frompath),href.split('#')[0]))
 def soup(path):return BeautifulSoup(z.read(PREFIX+path).decode('utf-8',errors='strict'),'html.parser')
 for code,marker,era,stage in cfg:
  index='phonetic-indexes/phonetics-'+code+'.html'
  try:sp=soup(index)
  except Exception as exc:errors.append({'catalog':code,'error':str(exc)});continue
  heading=next((h for h in sp.find_all(re.compile(r'^h[1-6]$')) if h.get_text(' ',strip=True).lower()=='phonemes'),None)
  if heading is None:errors.append({'catalog':code,'error':'missing Phonemes section'});continue
  links=[];seen=set()
  for e in heading.next_elements:
   if isinstance(e,Tag) and e.name in ['h1','h2','h3'] and 'Phonetic Groups' in e.get_text(' ',strip=True):break
   if isinstance(e,Tag) and e.name=='a' and e.get('href'):
    label=e.get_text(' ',strip=True)
    if not re.fullmatch(r'\[[^\]]+\]',label):continue
    sym=label[1:-1];path=loc(index,e['href'])
    if (sym,path) not in seen:links.append((sym,path));seen.add((sym,path))
  for sym,path in links:
   sounds[sym].add(code)
   try:page=soup(path)
   except Exception as exc:errors.append({'catalog':code,'phoneme':sym,'error':str(exc)});continue
   for label in page.find_all(string=lambda t:bool(t) and t.strip()=='Phonetic Development'):
    tab=label.parent.find_next('table')
    if tab is None:continue
    active='';name=''
    for tr in tab.find_all('tr'):
     cells=tr.find_all(['td','th'],recursive=False)
     if len(cells)<4:continue
     descriptor=cells[0].get_text(' ',strip=True)
     m=re.match(r'^((?:ᴱ|ᴹ)?(?:AT|OS|ON|S|N|Q|AQ|T)\.|ᴹ✶|ᴱ✶|✶)\s*(.*)',descriptor)
     if m:active,name=m.groups()
     if active not in MARKERS[branch]:continue
     arrow=cells[2].get_text(' ',strip=True)
     if arrow not in ('<','>','←','→'):continue
     left=cells[1].get_text(' ',strip=True);right=cells[3].get_text(' ',strip=True)
     origin,result=(right,left) if arrow in ('<','←') else (left,right)
     links=[ 'https://eldamo.org/content/'+loc(path,a['href']) for a in cells[0].select('a[href]')]
     ref=[]
     for a in (cells[4].select('a[href]') if len(cells)>4 else []):ref.append(a.get_text(' ',strip=True))
     actual_era,actual_stage=MARKERS[branch][active]
     out.append({'era':actual_era,'stage':actual_stage,'marker':active,'rule':name or '[без названия]','a':origin,'b':result,'formula':left+' '+arrow+' '+right,'url':links[0] if links else '', 'catalogs':code,'sounds':sym,'refs':ref,'card_url':'https://eldamo.org/content/'+path})
 # Dedup across every phoneme card retaining all associations
 merged={}
 for r in out:
  key=(r['era'],r['marker'],r['formula'],r['url'],r['rule'])
  if key not in merged:
   v=r.copy();v['catalogs']=[r['catalogs']];v['sounds']=[r['sounds']];v['refs']=list(r['refs']);v['card_urls']=[r['card_url']];merged[key]=v
  else:
   v=merged[key]
   for name,value in [('catalogs',r['catalogs']),('sounds',r['sounds']),('card_urls',r['card_url'])]:
    if value not in v[name]:v[name].append(value)
   for ref in r['refs']:
    if ref not in v['refs']:v['refs'].append(ref)
  
 return list(merged.values()),out,errors,sounds

def write(branch,archive):
 rows,raw,errors,phonemes=parse(archive,branch)
 target=ROOT/'branches'/branch/'data';target.mkdir(parents=True,exist_ok=True)
 (target/'unified_rules.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 (target/'unified_raw.json').write_text(json.dumps(raw,ensure_ascii=False))
 (target/'unified_phonemes.json').write_text(json.dumps({k:sorted(v) for k,v in phonemes.items()},ensure_ascii=False,indent=2))
 (target/'unified_extraction_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))
 return {'branch':branch,'raw':len(raw),'deduplicated':len(rows),'phonemes':len(phonemes),'errors':errors}
if __name__=='__main__':
 archive=sys.argv[1];results=[write(b,archive) for b in CONFIGS];print(json.dumps(results,ensure_ascii=False,indent=2))
