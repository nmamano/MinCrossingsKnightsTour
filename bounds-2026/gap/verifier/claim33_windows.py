"""Independent reconstruction of W3 clauses and rerun of saved DRUP proofs.

No author geometry/model imports. All geometry uses integers.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'gap/lowerbounds/windows'
OUT = ROOT/'gap/verifier'
MOVES = [(x,y) for x,y in product(range(-2,3),repeat=2)
         if sorted((abs(x),abs(y))) == [1,2]]
def edge(a,b): return tuple(sorted((a,b)))
def sub(a,b): return a[0]-b[0],a[1]-b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def cross(e,f):
    a,b=e; c,d=f
    den=det(sub(b,a),sub(d,c))
    if not den: return False
    t=det(sub(c,a),sub(d,c)); s=det(sub(c,a),sub(b,a))
    if den<0: den,t,s=-den,-t,-s
    return 0<t<den and 0<s<den
def covers(e,point):
    a,b=e
    mid=(3*(a[0]+b[0]),3*(a[1]+b[1]))
    dv=(0,3) if abs(a[0]-b[0])==2 else (3,0)
    vertices=[(6*a[0],6*a[1]),(mid[0]-dv[0],mid[1]-dv[1]),
              (6*b[0],6*b[1]),(mid[0]+dv[0],mid[1]+dv[1])]
    ds=[det(sub(vertices[(i+1)%4],v),sub(point,v)) for i,v in enumerate(vertices)]
    return all(d>0 for d in ds) or all(d<0 for d in ds)
def clauses_for(w,h,side):
    core=set(product(range(w),range(h)))
    edges=sorted({edge(v,(v[0]+dx,v[1]+dy)) for v in core for dx,dy in MOVES
                  if not side or v[0]+dx>=0})
    ids={e:i+1 for i,e in enumerate(edges)}
    inc=defaultdict(list)
    for e,i in ids.items():
        for v in e: inc[v].append(i)
    clauses=[]
    for v,vs in inc.items():
        clauses.extend(tuple(-j for j in triple) for triple in combinations(vs,3))
        if v in core:
            clauses.extend(tuple(j for j in vs if i!=j) for i in vs)
    degree_count=len(clauses)
    for e,f in combinations(edges,2):
        if side and all(min(v[0] for v in g)<=1 for g in (e,f)): continue
        if cross(e,f): clauses.append((-ids[e],-ids[f]))
    return ids,clauses,degree_count
def saved_clauses(path):
    cs=[]; header=None
    for line in path.read_text().splitlines():
        if not line or line.startswith('c'): continue
        if line.startswith('p'):
            p,kind,n,m=line.split(); assert kind=='cnf'; header=int(n),int(m)
            continue
        c=list(map(int,line.split())); assert c[-1]==0
        assert all(c[:-1]); cs.append(tuple(c[:-1]))
    assert header and header[1]==len(cs)
    assert max(abs(l) for c in cs for l in c)==header[0]
    return header,cs
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def proof(cnf,drup):
    r=subprocess.run([sys.executable,str(ROOT/'w-lowerbounds/check_drup.py'),str(cnf),str(drup)],
                     capture_output=True,text=True,check=True)
    assert 'PASS ' in r.stdout
    return dict(proof=drup.name,sha256=digest(drup),result=r.stdout.strip())

results=[]
for w,h,side,depths in [(7,7,False,[3]),(12,9,True,[4,5,6])]:
    ids,base,degree_count=clauses_for(w,h,side)
    for d in depths:
        cy=h//2
        # Any edge covering this square has both coordinates within this range.
        near={edge(v,(v[0]+dx,v[1]+dy))
              for v in product(range(d-2,d+4),range(cy-2,cy+4)) for dx,dy in MOVES
              if not side or min(v[0],v[0]+dx)>=0}
        for q,(qx,qy) in dict(b=(3,1),r=(5,3),t=(3,5),l=(1,3)).items():
            point=(6*d+qx,6*cy+qy)
            cov=sorted(e for e in near if covers(e,point))
            assert cov and all(e in ids for e in cov)
            expected=base+[(-ids[e],) for e in cov]
            name=f'sidehole_W{w}_H{h}_d{d}_S_{q}' if side else f'hole_k{w}_{q}'
            cnf=SRC/(name+'.cnf'); drup=SRC/(name+'.drup')
            header,actual=saved_clauses(cnf)
            canon=lambda cs: Counter(tuple(sorted(c)) for c in cs)
            assert header==(len(ids),len(expected))
            assert canon(actual)==canon(expected),name
            rec=dict(name=name,variables=len(ids),clauses=len(expected),degree_clauses=degree_count,
                     crossing_clauses=len(base)-degree_count,hole_edges=cov,
                     hole_units=[ids[e] for e in cov],cnf_sha256=digest(cnf),
                     clause_multiset_match=True,drup=proof(cnf,drup))
            results.append(rec)
            print(name,len(ids),len(expected),rec['drup']['result'],flush=True)

# Re-run the independent W1 reconstruction and both proof checks for this audit.
r=subprocess.run([sys.executable,str(OUT/'claim30_w1.py')],capture_output=True,text=True,check=True)
w1=json.loads(r.stdout)
w1['proofs']=[proof(SRC/'w1cert_k9_b3.cnf',SRC/('w1cert_k9_b3.'+solver+'.drup'))
              for solver in ('glucose4','lingeling')]
print('W1:',json.dumps(w1),flush=True)
(OUT/'claim33_windows.json').write_text(json.dumps(dict(date='2026-10-03',w1=w1,w3=results),indent=2))
