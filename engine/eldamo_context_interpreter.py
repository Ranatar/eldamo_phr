"""Conservative, reproducible interpreter for a SUBSET of Eldamo phonetic rules.
No claim of historical proof. Python 3.9+, pandas optional for audit driver.
"""
import re, unicodedata
VOWELS=set('aeiouāēīōūăĕĭŏŭæǣœøǭęəɛɔ')
BAD=set('{}|₁₂₃₄*?()[]')
BOUNDARY='-'

def tokenise(s):
    # IPA vowel with marks; consonant and aspiration/labialization etc remain in same token
    s=unicodedata.normalize('NFC',s)
    parts=[]
    for ch in s:
        if unicodedata.combining(ch) and parts:parts[-1]+=ch
        elif ch in 'ʰʷʲ' and parts: parts[-1]+=ch
        else:parts.append(ch)
    return parts

def vowel(ch):
    if not ch:return False
    b=unicodedata.normalize('NFD',ch)[0]
    return b in VOWELS or ch in VOWELS

def supports(src,dst):
    a,b=src.strip(),dst.strip()
    if not a or not b:return False,'empty'
    if any(c in a+b for c in BAD):return False,'alternation/metathesis/complex syntax'
    if any(c in a+b for c in 'S'):return False,'syllable metacharacter'
    if 'V̄' in a+b or 'V̆' in a+b:return False,'vowel length variable'
    if 'C' in b and 'C' not in a:return False,'unbound consonant'
    if 'V' in b and 'V' not in a:return False,'unbound vowel'
    return True,'basic literal/boundary/V/C/ø'

def changes(src,dst,word):
    ok,reason=supports(src,dst)
    if not ok:return [],reason
    a,b=src.strip(),dst.strip()
    left=a.startswith('-');right=a.endswith('-');
    if left != b.startswith('-') or right != b.endswith('-'):return [],'incompatible word boundary'
    a=a.strip('-');b=b.strip('-')
    at=tokenise(a);bt=tokenise(b);wt=tokenise(word)
    # Avoid treating a literal ø in source as real phoneme; insertions need explicit mapping
    if 'ø' in at and len(at)!=len(bt):return [],'unsupported insertion alignment'
    output=[]
    for start in range(len(wt)+1):
        if right and start!=0:continue # trailing hyphen = initial
        for end in range(start,len(wt)+1):
            if left and end!=len(wt):continue # leading hyphen = final
            seg=wt[start:end]
            if len(seg)!=len([x for x in at if x!='ø']):continue
            mapping=[]; j=0; matches=True
            for x in at:
                if x=='ø':mapping.append('');continue
                y=seg[j];j+=1
                if x=='V' and not vowel(y):matches=False;break
                elif x=='C' and vowel(y):matches=False;break
                elif x not in ('V','C','X') and x!=y:matches=False;break
                mapping.append(y)
            if not matches:continue
            if len(bt)!=len(mapping):
                # safe constant literal substitution only
                if any(x in ('V','C','X','ø') for x in at+bt):continue
                repl=bt
            else:
                repl=[]
                for x,y in zip(bt,mapping):
                    if x=='ø':continue
                    if x in ('V','C','X'): repl.append(y)
                    else: repl.append(x)
            changed=''.join(wt[:start]+repl+wt[end:]);
            if changed!=word and changed not in output:output.append(changed)
    return output,reason

if __name__=='__main__':
    tests=[('pʰ','ɸ','rapʰe','raɸe'),('ɸ','f','raɸe','rafe'),('tʰ','θ','itʰil','iθil'),('θ','s','iθil','isil'),('VɣV','VøV','aɣa','aa'),('m-','n-','mara','nara'),('-m','-n','tam','tan'),('pm','pw','napma','napwa')]
    for a,b,w,expected in tests:
        got,_=changes(a,b,w)
        assert expected in got,(a,b,w,got)
    assert changes('m-','n-','ama')[0]==[]
    print('tests passed',len(tests)+1)
