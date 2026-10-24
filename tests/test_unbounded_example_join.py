"""Regression for the removed 5000-combination evidence cutoff."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.chains import join_examples_exact

def ex(a,b,ref,source):
    return {'before':a,'after':b,'refs':{ref},'source':source,'deleted':False}
first=[ex('a','b',f'other{i}','X') for i in range(6000)]+[ex('a','b','valid','S')]
second=[ex('b','c','valid','S')]
res=join_examples_exact([first,second])
assert res['contiguous']==6001,res
assert res['coherent']==1,res
assert [r['before'] for r in res['witness']]==['a','b']
assert join_examples_exact([[ex('a','b','x','Y')],[ex('z','c','x','Y')]])['contiguous']==0
assert join_examples_exact([[ex('a','b','x','Y')],[ex('b','c','y','Y')]])['coherent']==0
print('UNBOUNDED EVIDENCE JOIN PASS')
