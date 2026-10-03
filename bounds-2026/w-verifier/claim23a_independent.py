"""Parse the appendix itself; check its tables and tours without worker imports."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import re,json
from check import check
text=Path('writeup/turns/post.mdx').read_text();appendix=text.split('## Appendix: full proofs')[1]
M=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
alpha={}
for m in re.finditer(r'\| y = ([0-3]) \| ([^\n]+)',appendix):
 vals=[int(x.strip()) for x in m[2].strip().strip('|').split('|')];assert len(vals)==4
 for x,v in enumerate(vals):alpha[x,int(m[1])]=v
beta={}
for a,b,c,d,v in re.findall(r'\(([0-3]),([0-3])\)-\(([0-3]),([0-3])\) \| ([+-]1)',appendix):beta[((int(a),int(b)),(int(c),int(d)))]=int(v)
assert len(alpha)==16 and sum(alpha.values())==-7 and len(beta)==9
L=lambda i,ns: 1 if i==0 else sum(v in (0,3) for v in ns)-1 if i in (1,2) else 1-sum(v in (1,2) for v in ns) if i==3 else 0
hist=Counter();tight=set();local=0
for x in range(4):
 for a,b in combinations([v for v in M if x+v[0]>=0],2):
  t=int(tuple(map(sum,zip(a,b)))!=(0,0));assert t>=L(x,[x+a[0],x+b[0]]);local+=1
for p in product(range(4),repeat=2):
 x,y=p
 for a,b in combinations([(x+dx,y+dy) for dx,dy in M if min(x+dx,y+dy)>=0],2):
  t=int((a[0]-x)*(b[1]-y)!=(a[1]-y)*(b[0]-x));r=t-L(x,[a[0],b[0]])-L(y,[a[1],b[1]])
  div=sum(beta.get(tuple(sorted((p,q))),0)*(1 if p<q else -1) for q in (a,b));slack=r-alpha[p]-div;assert slack>=0;hist[slack]+=1
  if slack==0:tight.add(p)
assert sum(hist.values())==209 and len(tight)==16 and local==77
corners={};counts={};matches=0
for m in re.finditer(r'\*\*Corners for `n mod 8 = ([0246])`\.\*\*\s*```(.*?)```',appendix,re.S):
 r=int(m[1]);lines=[line.split() for line in m[2].splitlines() if re.match(r'^\d\d ',line)];assert len(lines)==12 and all(len(l)==12 for l in lines)
 corners[r]={};d=json.loads(Path(f'w-integrator/corners/TT16_res{r:02d}.json').read_text());counts[r]={}
 for name,start,off in [('TL',0,0),('TR',0,6),('BL',6,0),('BR',6,6)]:
  counts[r][name]=0
  for j in range(6):
   for x in range(6):
    code=lines[start+j][off+x];key=f'{name}:{x},{5-j}';ds={M[int(k)] for k in code};assert ds==set(map(tuple,d['zones'][key])),(r,key)
    corners[r][key]=code;counts[r][name]+=abs(int(code[0])-int(code[1]))!=4;matches+=1
 assert counts[r]=={'TL':20,'TR':20,'BL':21,'BR':21}
assert len(corners)==4 and matches==576
bottom={}
for y,codes in re.findall(r'^ ([0-3])   ((?:\d\d ?){8})$',appendix,re.M):bottom[int(y)]=codes.split()
assert len(bottom)==4
c=[sum(abs(int(bottom[y][k][0])-int(bottom[y][k][1]))!=4 for y in range(4)) for k in range(8)];assert c==[3,1,2,2,1,3,2,2] and all(c[k]+c[(1-k)%8]==4 for k in range(8))
rows=[]
for n in range(48,104,2):
 g={};grid=[['']*n for _ in range(n)]
 for x,y in product(range(n),repeat=2):
  code='26'
  if y<4:code=bottom[y][x%8]
  if y>=n-4:code=''.join(str((int(k)+4)%8) for k in bottom[n-1-y][(1-x)%8])
  if x==0:code='23'
  if x==1:code='27'
  if x==n-2:code='06'
  if x==n-1:code='46'
  if (x<6 or x>=n-6) and (y<6 or y>=n-6):
   name=('B' if y<6 else 'T')+('L' if x<6 else 'R');code=corners[n%8][f'{name}:{x if x<6 else x-n+6},{y if y<6 else y-n+6}']
  g[x,y]=tuple(sorted((x+M[int(k)][0],y+M[int(k)][1]) for k in code));grid[n-1-y][x]=code
 X,T=check(grid);assert T==8*n-14
 prior={tuple(p):tuple(sorted(map(tuple,ns))) for p,ns in json.loads(Path(f'w-verifier/claim16_runner/tour{n}.json').read_text())};assert g==prior
 rows.append({'n':n,'X':X,'T':T})
res={'date':'2026-10-02','four_column_cases':local,'corner_cases':sum(hist.values()),'slack_histogram':dict(hist),'tight_cells':len(tight),'corner_cells_matched':matches,'corner_counts':counts,'bottom_counts':c,'tours_match_prior_audit':rows}
Path('w-verifier/claim23a_independent.json').write_text(json.dumps(res,indent=2));print('PASS:',local,'strip cases;',sum(hist.values()),'corner cases;',matches,'corner grid cells;',len(rows),'printed-rule tours identical to prior audit')
