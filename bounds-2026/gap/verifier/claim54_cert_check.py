from pathlib import Path
import re, ast, itertools, hashlib, json
root=Path('gap/verifier/claim54_clean')
lean=(root/'Ktlean/CornerTurns.lean').read_text()
paper=Path('writeup/turns/main.tex').read_text()
cert=lean.split('def cert28 : CornerCert where')[1].split('lemma cert28_valid')[0]
a=ast.literal_eval(re.search(r'alpha := (\[.*?\])',cert,re.S)[1])
la={(x,y):a[4*y+x] for x in range(4) for y in range(4)}
pa={}
for y,tail in re.findall(r'\$y=(\d)\$([^\n]*)',paper.split(r'\begin{tabular}{c|rrrr}')[1].split(r'\end{tabular}')[0]):
 vals=list(map(int,re.findall(r'\$([+-]?\d+)\$',tail)))
 assert len(vals)==4
 for x,v in enumerate(vals):pa[x,int(y)]=v
lb={((int(x),int(y)),(int(z),int(w))):int(v) for x,y,z,w,v in re.findall(r'\(\((\d), (\d)\), \((\d), (\d)\), (-?\d)\)',cert)}
pb={((int(x),int(y)),(int(z),int(w))):int(v) for x,y,z,w,v in re.findall(r'\$\((\d),(\d)\)\$--\$\((\d),(\d)\)\$ & \$([+-]?\d+)\$',paper)}
assert len(la)==len(pa)==16 and la==pa
assert len(lb)==len(pb)==9 and lb==pb
assert sum(la.values())==-7
moves=[(x,y) for x in (-2,-1,1,2) for y in (-2,-1,1,2) if abs(x*y)==2]
def L(i,js):
 if i==0:return 1
 if i in (1,2):return sum(j in (0,3) for j in js)-1
 if i==3:return 1-sum(j in (1,2) for j in js)
 return 0
cases=0; tight=set()
for (x,y),alpha in la.items():
 legal=[(x+dx,y+dy) for dx,dy in moves if x+dx>=0 and y+dy>=0]
 for u,w in itertools.combinations(legal,2):
  t=int((u[0]+w[0],u[1]+w[1])!=(2*x,2*y))
  r=t-L(x,[u[0],w[0]])-L(y,[u[1],w[1]])
  D=sum(lb.get(((x,y),q),0)-lb.get((q,(x,y)),0) for q in (u,w))
  assert r>=alpha+D
  cases+=1
  if r==alpha+D:tight.add((x,y))
assert cases==209 and len(tight)==16
print(json.dumps(dict(alpha_entries=len(la),beta_entries=len(lb),sum_alpha=sum(la.values()),legal_unordered_cases=cases,tight_cells=len(tight),paper_sha256=hashlib.sha256(paper.encode()).hexdigest(),lean_sha256=hashlib.sha256(lean.encode()).hexdigest()),indent=2))
