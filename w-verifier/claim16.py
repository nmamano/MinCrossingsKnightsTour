"""Independent check of printed TT16 rules and the printed corner certificate."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import json
from check import check
ROOT=Path(__file__).resolve().parents[1]
M=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
B=['16 67 06 16 06 16 16 67'.split(),'25 26 25 26 26 25 26 25'.split(),'36 26 26 46 26 46 36 26'.split(),['26']*8]
turn=lambda ds: tuple(ds[0])!=tuple(-z for z in ds[1])
def moves(s):return tuple(M[int(k)] for k in s)
def certificate():
 A=[[-1,0,0,-1],[0,1,0,-1],[0,0,0,-1],[-1,-1,-1,-1]]
 beta={((0,1),(1,3)):-1,((0,2),(2,3)):-1,((0,3),(1,1)):1,((1,0),(3,1)):-1,((1,1),(3,0)):-1,((1,2),(3,3)):-1,((2,0),(3,2)):-1,((2,1),(3,3)):-1,((2,2),(3,0)):-1}
 def ell(i,a,b):
  if i==0:return 1
  if i in (1,2):return (a in (0,3))+(b in (0,3))-1
  assert i==3
  return 1-(a in (1,2))-(b in (1,2))
 count=0;minimum={};hist=Counter()
 for x,y in product(range(4),repeat=2):
  p=(x,y);nb=[(x+a,y+b) for a,b in M if x+a>=0 and y+b>=0];ss=[]
  for a,b in combinations(nb,2):
   t=int((a[0]-x)*(b[1]-y)!=(a[1]-y)*(b[0]-x))
   r=t-ell(x,a[0],b[0])-ell(y,a[1],b[1])
   div=sum(beta.get(tuple(sorted((p,q))),0)*(1 if p<q else -1) for q in (a,b))
   slack=r-A[y][x]-div;assert slack>=0;ss.append(slack);count+=1;hist[slack]+=1
  minimum[str(p)]=min(ss);assert min(ss)==0
 assert count==209 and sum(map(sum,A))==-7
 assert all(all(0<=v<4 for p in e for v in p) for e in beta)
 return {'cases':count,'alpha_sum':-7,'tight_cells':16,'slack_histogram':dict(hist)}
def main():
 cert=certificate();c=[sum(turn(moves(B[y][k])) for y in range(4)) for k in range(8)]
 assert c==[3,1,2,2,1,3,2,2] and all(c[k]+c[(1-k)%8]==4 for k in range(8))
 corners={};docs={}
 for r in (0,2,4,6):
  d=json.loads((ROOT/f'w-integrator/corners/TT16_res{r:02d}.json').read_text());docs[r]=d
  assert d['Z']==6 and d['phases']==[0,1,0,0]
  assert [s.split() for s in d['bottom']]==list(reversed(B)) and d['top']==d['bottom']
  assert d['left']==['23 27']*4 and d['right']==['02 24']*4
  corner={name:0 for name in ('BL','BR','TL','TR')}
  assert set(d['zones'])=={f'{name}:{x},{y}' for name in corner for x,y in product(range(6),repeat=2)}
  for key,ds in d['zones'].items():corner[key.split(':')[0]]+=turn(ds)
  assert sum(corner.values())==82;corners[r]=corner
 rows=[]
 for n in range(48,104,2):
  d=docs[n%8];g={}
  for x,y in product(range(n),repeat=2):
   ds=moves('26')
   if y<4:ds=moves(B[y][x%8])
   if y>=n-4:ds=tuple(tuple(-v for v in z) for z in moves(B[n-1-y][(1-x)%8]))
   if x==0:ds=moves('23')
   if x==1:ds=moves('27')
   if x==n-2:ds=moves('06')
   if x==n-1:ds=moves('46')
   if (x<6 or x>=n-6) and (y<6 or y>=n-6):
    name=('B' if y<6 else 'T')+('L' if x<6 else 'R');u=x if x<6 else x-(n-6);v=y if y<6 else y-(n-6)
    ds=d['zones'][f'{name}:{u},{v}']
   g[x,y]=tuple(sorted((x+a,y+b) for a,b in ds))
  supplied={tuple(p):tuple(sorted(map(tuple,qs))) for p,qs in json.loads((ROOT/f'w-verifier/claim16_runner/tour{n}.json').read_text())}
  assert g==supplied
  grid=[['' for _ in range(n)] for _ in range(n)]
  for (x,y),ns in g.items():grid[n-1-y][x]=''.join(str(M.index((a-x,b-y))) for a,b in ns)
  X,T=check(grid);assert T==8*n-14
  flags={p:turn(tuple((a-p[0],b-p[1]) for a,b in ns)) for p,ns in g.items()}
  middle=set()
  for x in range(6,n-6):
   ps={(x,y) for y in list(range(4))+list(range(n-4,n))};assert sum(flags[p] for p in ps)==4;middle|=ps
  for y in range(6,n-6):
   ps={(x,y) for x in (0,1,n-2,n-1)};assert sum(flags[p] for p in ps)==4;middle|=ps
  corner={p for p in g if (p[0]<6 or p[0]>=n-6) and (p[1]<6 or p[1]>=n-6)}
  assert not middle&corner and sum(flags[p] for p in corner)==82
  assert not any(flags[p] for p in set(g)-middle-corner)
  rows.append({'n':n,'X':X,'T':T,'corner_turns':82})
 tables=(ROOT/'writeup/turns/figures/corner_tables.tex').read_bytes()==(ROOT/'w-verifier/claim16_runner/corner_tables.tex').read_bytes()
 assert tables
 out={'date':'2026-10-02','certificate':cert,'bottom_per_column':c,'corner_turns':corners,'printed_tables_match':tables,'tours':rows,'text_defect':'Right pattern codes 46,06 are correct; the claim that this is the left pattern turned 180 degrees is false.'}
 (ROOT/'w-verifier/claim16.json').write_text(json.dumps(out,indent=1));print(json.dumps(out,indent=1))
if __name__=='__main__':main()
