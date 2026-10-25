"""Conservative Eldamo sound-rule executor; never treats unsupported grammar as mismatch.
Guided by Eldamo 0.8.13/general/phonetic-descriptions.html.
"""
import re,unicodedata
from dataclasses import dataclass
VOWELS=set('aeiouæœəɛɔɨɯyøǫę')
SUB={'₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6'}
LONG={'a':'ā','e':'ē','i':'ī','o':'ō','u':'ū','æ':'ǣ','ǫ':'ǭ'}
SHORT={v:k for k,v in LONG.items()}
MODS=set('ʰʷʲ̣̥̩̄̆́̀̂')
class Unsupported(Exception):pass
@dataclass
class Token:
 value:str
 index:str=''

def split_top(s,sep='|'):
 depth=0;parts=[];start=0
 for i,ch in enumerate(s):
  if ch=='{':depth+=1
  elif ch=='}':depth-=1
  elif ch==sep and depth==0:parts.append(s[start:i]);start=i+1
 if depth:raise Unsupported('unclosed group')
 parts.append(s[start:]);return parts

def phonemes(s):
 s=unicodedata.normalize('NFC',s)
 out=[]
 for c in s:
  if out and (unicodedata.combining(c) or c in MODS):out[-1]+=c
  else:out.append(c)
 return out

def parse(s):
 s=s.strip().strip('[]'); medial=s.startswith('-') and s.endswith('-'); initial=s.endswith('-') and not medial;final=s.startswith('-') and not medial
 s=s.removeprefix('-').removesuffix('-')
 if '*' in s or '?' in s or '(' in s or ')' in s:raise Unsupported('unresolved operators')
 tokens=[];i=0
 while i<len(s):
  if s[i]=='{':
   j=s.find('}',i+1)
   if j<0:raise Unsupported('unclosed group')
   raw=s[i+1:j];opts=split_top(raw)
   if len(opts)==1:opts=phonemes(raw)
   else:opts=[x for x in opts if x]
   if not opts:raise Unsupported('empty group')
   i=j+1;mods=''
   while i<len(s) and (s[i] in MODS or unicodedata.combining(s[i])):mods+=s[i];i+=1
   idx=''
   while i<len(s) and s[i] in SUB:idx+=SUB[s[i]];i+=1
   tokens.append((tuple(o+mods for o in opts),idx));continue
  ch=s[i];i+=1
  if ch in SUB:raise Unsupported('index without token')
  while i<len(s) and (s[i] in MODS or unicodedata.combining(s[i])):ch+=s[i];i+=1
  idx=''
  while i<len(s) and s[i] in SUB:idx+=SUB[s[i]];i+=1
  tokens.append(((ch,),idx))
 return tokens,initial,final,medial

def base_vowel(x):
 if x in SHORT:return SHORT[x]
 n=unicodedata.normalize('NFD',x);return ''.join(c for c in n if not unicodedata.combining(c))
def is_vowel(x):return base_vowel(x) in VOWELS

def token_match(p,t):
 if (p,t) in {('θ','þ'),('ɣ','ʒ'),('ŋ','ñ')}:return True
 if p=='V':return is_vowel(t)
 if p=='V̄':return is_vowel(t) and (t in SHORT or '̄' in unicodedata.normalize('NFD',t))
 if p=='V̆':return is_vowel(t) and not token_match('V̄',t)
 if p=='C':return not is_vowel(t)
 if p=='X':return True
 if p=='S':raise Unsupported('syllable variable requires syllabification')
 return p==t

def apply_one(src,dst,word):
 # Plus in a source formula can indicate concatenation of the two surface segments.
 # Only allow it where the literal adjacent input is unambiguous.
 if re.fullmatch(r"[^+]+\+[^+]+",src):src=src.replace("+","")
 aa,ini,fin,med=parse(src);bb,ini2,fin2,med2=parse(dst)
 if (ini,fin,med)!=(ini2,fin2,med2):raise Unsupported('different boundary constraints')
 if any('S' in opts for opts,_ in aa+bb):
  # A syllable in Eldamo is vowel/diphthong possibly flanked by consonants.
  # Enumerate candidate syllable spans; this is NOT a unique syllabification.
  if not (fin and len(aa)==2 and len(bb)==2 and aa[0][0]==('S',) and bb[0][0]==('S',)
          and aa[1][0] in (('ĭ',),('ŭ',)) and len(bb[1][0])==1):
   raise Unsupported('unresolved syllable expression')
  w=phonemes(word);srcv=aa[1][0][0];dstv=bb[1][0][0]
  if not w or w[-1] not in ({'ĭ':('i','ĭ'),'ŭ':('u','ŭ')}[srcv]):return []
  diphthongs={'ai','au','oi','ui','eu','iu','ei','ou','ae','oe'}
  for j in range(len(w)-1):
   segment=w[j:-1];v=[k for k,ch in enumerate(segment) if is_vowel(ch)]
   if len(v)==1 or (len(v)==2 and v[1]==v[0]+1 and ''.join(segment[x] for x in v) in diphthongs):
    return [''.join(w[:-1]+[dstv])]
  return []
 if len(aa)!=len(bb):
  # Syllable epenthesis after two consonants before a liquid:
  # CCr > CCar (the consonant variables are individually bound).
  if ([opts for opts,_ in aa]==[('C',),('C',),('r',)]
      and [opts for opts,_ in bb]==[('C',),('C',),('a',),('r',)]):
   w=phonemes(word);out=[]
   for j in range(len(w)-2):
    if ini and j:continue
    if fin and j+3!=len(w):continue
    if med and (j==0 or j+3==len(w)):continue
    if token_match('C',w[j]) and token_match('C',w[j+1]) and w[j+2]=='r':
     n=''.join(w[:j]+[w[j],w[j+1],'a','r']+w[j+3:])
     if n!=word:out.append(n)
   return sorted(set(out))
  # Compensatory lengthening: V + disappearing literal consonant + C -> long V + C
  if (len(aa)==3 and len(bb)==2 and aa[0][0] in (('V',),('a',),('i',),('u',),('e',),('o',))
      and aa[2][0]==bb[1][0] and bb[0][0] in (('V̄',),('ā',),('ī',),('ū',),('ē',),('ō',))
      and len(aa[1][0])==1 and aa[1][0][0] not in ('V','C','X','S')):
   first=aa[0][0][0];middle=aa[1][0][0];third=aa[2][0][0];changed=[]
   w=phonemes(word)
   for j in range(len(w)-2):
    if ini and j:continue
    if fin and j+3!=len(w):continue
    if med and (j==0 or j+3==len(w)):continue
    if not token_match(first,w[j]) or w[j+1]!=middle or not token_match(third,w[j+2]):continue
    vowel=LONG.get(base_vowel(w[j]));
    if vowel is None:raise Unsupported('unmapped long vowel')
    nv=''.join(w[:j]+[vowel,w[j+2]]+w[j+3:]);
    if nv!=word:changed.append(nv)
   return sorted(set(changed))
  # Safe whole-substring rewrite for fully literal, context-free segment formulas.
  # No inference of alignment, phonological order, or unstated environment.
  if all(len(opts)==1 and not idx and opts[0] not in ('V','V̄','V̆','C','S','X','ø') for opts,idx in aa+bb):
   left=''.join(opts[0] for opts,_ in aa);right=''.join(opts[0] for opts,_ in bb)
   if not left:raise Unsupported('empty input')
   results=[];start=0
   while True:
    pos=word.find(left,start)
    if pos<0:break
    start=pos+1
    if ini and pos!=0:continue
    if fin and pos+len(left)!=len(word):continue
    if med and (pos==0 or pos+len(left)==len(word)):continue
    new=word[:pos]+right+word[pos+len(left):]
    if new!=word and new not in results:results.append(new)
   return sorted(results)
  raise Unsupported('unaligned insertion/deletion')
 wt=phonemes(word);out=set()
 for offset in range(len(wt)+1):
  if ini and offset!=0:continue
  if med and offset==0:continue
  if fin and offset+sum(x[0]!=('ø',) for x in aa)!=len(wt):continue
  cursor=offset;caps={};slots=[];ok=True
  for k,(opts,idx) in enumerate(aa):
   if opts==('ø',):slots.append('');continue
   if cursor>=len(wt):ok=False;break
   target=wt[cursor];cursor+=1
   if not any(token_match(p,target) for p in opts):ok=False;break
   slots.append(target);caps[k]=target
   if idx:caps[idx]=target
  if not ok:continue
  if med and cursor>=len(wt):continue
  if not ini and not fin and offset==0 and src.startswith('-'):continue
  result=[]
  for k,(opts,idx) in enumerate(bb):
   p=opts[0] if len(opts)==1 else None
   prev=slots[k]
   # paired choice by index within sets
   if p is None:
    aopts=aa[k][0]
    if len(aopts)!=len(opts):raise Unsupported('unpaired sets')
    source=caps.get(k)
    if source is None:
     if idx and idx in caps:source=caps[idx]
     else:raise Unsupported('unbound destination set')
    matches=[i for i,x in enumerate(aopts) if token_match(x,source)]
    if len(matches)!=1:raise Unsupported('ambiguous set alignment')
    p=opts[matches[0]]
   if p=='ø':result.append('');continue
   if p in ('V','V̄','V̆','C','X') or (p=='S'):
    val=caps.get(idx,caps.get(k))
    if val is None:raise Unsupported('unbound variable')
    if p=='V̄':val=LONG.get(base_vowel(val));
    elif p=='V̆':val=base_vowel(val)
    elif p=='V' and not is_vowel(val):raise Unsupported('non-vowel capture')
    if not val:raise Unsupported('unknown length operation')
    result.append(val)
   elif idx and p in ('C','X'):
    result.append(caps[idx])
   else:
    # indexed C2 can be permuted via generic branch above
    result.append(p)
  changed=''.join(wt[:offset]+result+wt[cursor:])
  if changed!=word:out.add(changed)
 return sorted(out)

def apply(src,dst,word):
 try:
  a=split_top(src);b=split_top(dst)
  if len(a)!=len(b):raise Unsupported('unpaired pipe alternatives')
  results=set()
  for x,y in zip(a,b):results.update(apply_one(x,y,word))
  return sorted(results),'executed' if results else 'no_match'
 except Unsupported as e:return [],'unsupported:'+str(e)
 except Exception as e:return [],'error:'+repr(e)

if __name__=='__main__':
 cases=[('m-','n-','mara','nara'),('-m','-n','aram','aran'),('-m-','-n-','ama','ana'),('{ptk}ʰ','{ɸθx}','apʰa','aɸa'),('VɣV','VøV','aɣa','aa'),('VɣC','V̄øC','aɣta','āta'),('V₁Cøl','V₁CV₁l','akla','akala'),('{lr}₁{tk}₂','C₂C₁','alta','atla'),('z{bdg}','s{ptk}','azba','aspa'),('pʰ','ɸ','rapʰe','raɸe')]
 for a,b,w,expect in cases:
  ans,st=apply(a,b,w);print(a,b,w,ans,st,'PASS' if expect in ans else 'FAIL')
