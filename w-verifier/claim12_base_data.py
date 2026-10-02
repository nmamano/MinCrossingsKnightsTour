"""Check that saved local moves reproduce each base tour on all saved cells."""
from pathlib import Path
from collections import Counter
import json
from check import MOVES

def rot(p,n,r):
 x,y=p
 for _ in range(r):x,y=n-1-y,x
 return x,y

def rv(p,r):
 x,y=p
 for _ in range(r):x,y=-y,x
 return x,y

def main():
 out=[];signatures=[]
 for f in sorted(Path('w-integrator/corners').glob('FOLD24_base_n*.json')):
  d=json.loads(f.read_text());n=d['n0'];g=json.loads(Path(f'w-integrator/tours/FOLD24_n{n}.json').read_text())['tour']
  assert (d['p'],d['lo'],d['band'],d['rad'])==(6,8,1,4)
  assert set(d['template'])=={f'{r}:{s},{delta}' for r in range(4) for s in range(6) for delta in range(3)}
  def actual(c):return { (MOVES[int(k)][1],-MOVES[int(k)][0]) for k in g[n-1-c[1]][c[0]] }
  used=set();mid=set()
  for r in range(4):
   for x in range(11,n//2-11):
    for delta in range(3):
     c=rot((x,x+delta),n,r);assert c not in used
     assert actual(c)=={rv(ds,r) for ds in d['template'][f'{r}:{(x-8)%6},{delta}']}
     mid.add(c);used.add(c)
  shapes=Counter()
  for co in d['components']:
   ox,oy=co['offset'];shape=frozenset(co['cells']);shapes[shape]+=1
   for key,moves in co['cells'].items():
    x,y=map(int,key.split(','));c=(x+ox,y+oy)
    assert c not in used and 0<=c[0]<n and 0<=c[1]<n
    assert actual(c)=={tuple(ds) for ds in moves};used.add(c)
  assert len(used)-len(mid)==1008
  signatures.append(shapes)
  out.append({'n0':n,'middle_cells':len(mid),'copied_cells':1008,'total_saved_cells':len(used),'shape_multiplicities':sorted(shapes.values()),'matches_base_tour':True})
 assert len(out)==12 and all(s==signatures[0] for s in signatures)
 Path('w-verifier/claim12_base_data.json').write_text(json.dumps(out,indent=1))
 print('PASS: all 12 base templates and 13-component move records match their base tours.')
 print('Shape multiplicities',out[0]['shape_multiplicities'],'copied cells 1008; total saved cells 6n+744.')
if __name__=='__main__':main()
