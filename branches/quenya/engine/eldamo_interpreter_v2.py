"""Conservative executable interpreter for Eldamo phonetic notation.
Tokens/context alternatives, correlated sets, vowel length, deletion, boundaries.
Ambiguity returns explicit status; historical chronology NOT inferred.
"""
import re,unicodedata,itertools
VOWELS='aeiouāēīōūăĕĭŏŭæǣœǭęəɛɔȳȃ'
MACRON={'a':'ā','e':'ē','i':'ī','o':'ō','u':'ū','æ':'ǣ','ę':'ę̄','ǫ':'ǭ'}
CONSONANTS='ptkbdgmnŋlrwszɸβɣðθxfhjʍʎʔɹ'

def tokenize(s):
 s=unicodedata.normalize('NFC',s);out=[]
 for c in s:
  if out and (unicodedata.combining(c) or c in 'ʰʷʲ'):out[-1]+=c
  else:out.append(c)
 return out

def option_group(s):
 # split brace items into IPA tokens (longest cluster on aspiration), not single codepoints
 if '{' not in s:return [(s,())]
 m=re.search(r'\{([^{}]+)\}',s)
 if not m:raise ValueError('nested brace')
 inner=m.group(1)
 opts=inner.split('|') if '|' in inner else tokenize(inner)
 if len(opts)>15:raise ValueError('large set')
 result=[]
 for i,o in enumerate(opts):
  for tail,inds in option_group(s[:m.start()]+o+s[m.end():]): result.append((tail,(i,)+inds))
 return result

def variants(src,dst):
 # aligned left/right sets chosen using same index
 src_alt=src.split('|');dst_alt=dst.split('|')
 if len(src_alt)>1 or len(dst_alt)>1:
  if len(src_alt)!=len(dst_alt):raise ValueError('unaligned pipe alternatives')
  a=[]
  for s,d in zip(src_alt,dst_alt):a.extend(variants(s,d))
  return a
 aa=option_group(src);bb=option_group(dst)
 if len(aa)>1 and len(bb)>1:
  if len(aa)!=len(bb):raise ValueError('unaligned brace sets')
  return [(x[0],y[0]) for x,y in zip(aa,bb)]
 return [(x[0],y[0]) for x in aa for y in bb]

def isv(t):return bool(t) and (unicodedata.normalize('NFD',t)[0] in VOWELS or t in VOWELS)

def match_and_apply(src,dst,word):
 a=tokenize(src);b=tokenize(dst);w=tokenize(word)
 # initial and final hyphens mark environment; pipe splits handled prior
 ini=a[-1:]==['-'];fin=a[:1]==['-']
 if ini!= (b[-1:]==['-']) or fin!=(b[:1]==['-']):return [],'boundary mismatch'
 a=[x for x in a if x!='-'];b=[x for x in b if x!='-']
 # each V / C / S matching symbol is a positional bound capture; repeated V must match same quality
 meaningful=[x for x in a if x!='ø'];outputs=[]
 for i in range(len(w)-len(meaningful)+1):
  if ini and i!=0:continue
  if fin and i+len(meaningful)!=len(w):continue
  seg=w[i:i+len(meaningful)];captures=[];ok=True
  for sym,actual in zip(meaningful,seg):
   if sym in ('V','V̄','V̆') and not isv(actual):ok=False;break
   if sym=='V̄' and actual not in MACRON.values():ok=False;break
   if sym=='V̆' and (not isv(actual) or actual in MACRON.values()):ok=False;break
   if sym in ('C','S') and (isv(actual) or actual=='ø'):ok=False;break
   if sym not in ('V','V̄','V̆','C','S','X') and sym!=actual:ok=False;break
   captures.append((sym,actual))
  if not ok:continue
  # Align variable captures by symbol, no silent borrowing of unrelated tokens
  varmap={}
  for symbol,actual in captures:
   if symbol in ('V','V̄','V̆','C','S','X'):varmap.setdefault(symbol,[]).append(actual)
  replacement=[];counts={};bad=False
  for sym in b:
   if sym=='ø':continue
   if sym in ('V','C','S','X','V̄','V̆'):
    kind=sym
    source_candidates=varmap.get(kind,[])
    if not source_candidates and kind in ('V̄','V̆'):source_candidates=varmap.get('V',[])
    if not source_candidates and kind=='V':source_candidates=varmap.get('V̄',[])+varmap.get('V̆',[])
    idx=counts.get(kind,0);counts[kind]=idx+1
    if idx>=len(source_candidates):bad=True;break
    val=source_candidates[idx]
    if sym=='V̄':val=MACRON.get(val,val if val in MACRON.values() else None)
    if val is None:bad=True;break
    replacement.append(val)
   else:replacement.append(sym)
  if bad:continue
  changed=''.join(w[:i]+replacement+w[i+len(meaningful):]);
  if changed!=word and changed not in outputs:outputs.append(changed)
 return outputs,'executed'

def apply(src,dst,word):
 try:vp=variants(src,dst)
 except Exception as ex:return [],'unresolved:'+str(ex)
 outputs=[]
 for a,b in vp:
  if any(c in a+b for c in '[]()?*'):return [],'unresolved:unsupported syntax'
  got,_=match_and_apply(a,b,word)
  for item in got:
   if item not in outputs:outputs.append(item)
 return outputs,'executed' if outputs else 'no matching application'

if __name__=='__main__':
 cases=[('pʰ','ɸ','rapʰe','raɸe'),('ɸ','f','raɸe','rafe'),('Vnr','V̄ør','anra','āra'),('Vŋn','V̄n','aŋna','āna'),('w-|VwV','β-|VβV','awa','aβa'),('w-|VwV','β-|VβV','wara','βara'),('{rl}θ','{rl}t','arθa','arta'),('z{bdg}','s{ptk}','azba','aspa'),('rl|lr','ll|ll','arla','alla'),('-Sĭ','-Se','rĭ','re'),('pm','pw','napma','napwa')]
 for s,d,w,out in cases:
  got,status=apply(s,d,w);assert out in got,(s,d,w,out,got,status)
 print('passed',len(cases))
