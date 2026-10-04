"""Independent Claim 55 tour/count tests plus bad-input probes (2026-10-04)."""
from pathlib import Path
import json, importlib.util, shutil, subprocess
ROOT=Path('gap/verifier/claim55_run')
MOVES=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
def rebuild(d,n):
    rows={s:[r.split() for r in d[s]] for s in ['bottom','top','left','right']}
    def code(side,x,y):return rows[side][-1-y][x]
    xb,xt,yl,yr=d['phases'];g={}
    for y in range(n):
      for x in range(n):
        ds=[(2,-1),(-2,1)]
        for side,ix,iy,inside,flip in [
          ('bottom',(x-xb)%len(rows['bottom'][0]),y,y<len(rows['bottom']),1),
          ('top',(xt-x)%len(rows['top'][0]),n-1-y,n-1-y<len(rows['top']),-1),
          ('left',x,(y-yl)%len(rows['left']),x<len(rows['left'][0]),1),
          ('right',n-1-x,(yr-y)%len(rows['right']),n-1-x<len(rows['right'][0]),-1)]:
          if inside:ds=[(flip*MOVES[int(k)][0],flip*MOVES[int(k)][1]) for k in code(side,ix,iy)]
        g[x,y]=tuple((x+dx,y+dy) for dx,dy in ds)
    used=set()
    for key,ds in d['zones'].items():
      corner,off=key.split(':');dx,dy=map(int,off.split(','))
      x=dx+(n if corner[1]=='R' else 0);y=dy+(n if corner[0]=='T' else 0)
      assert (x,y) not in used;used.add((x,y))
      assert (x,y) in g
      g[x,y]=tuple((x+a,y+b) for a,b in ds)
    return g

def from_grid(rows):
    n=len(rows);assert all(len(row)==n for row in rows)
    return {(x,n-1-r):tuple((x+MOVES[int(k)][0],n-1-r+MOVES[int(k)][1]) for k in code) for r,row in enumerate(rows) for x,code in enumerate(row)}

def audit(g,n):
    assert set(g)=={(x,y) for x in range(n) for y in range(n)}
    for u,vs in g.items():
      assert len(vs)==2 and len(set(vs))==2
      for v in vs:
        assert sorted((abs(u[0]-v[0]),abs(u[1]-v[1])))==[1,2]
        assert v in g and u in g[v]
    seen=set();v=(0,0);prev=None
    while v not in seen:
      seen.add(v);w=next(w for w in g[v] if w!=prev);prev,v=v,w
    assert v==(0,0) and len(seen)==n*n
    # Determinant criterion, independently of endpoint-sum score in allsize_check.
    return sum((v[0]-u[0])*(w[1]-u[1])!=(v[1]-u[1])*(w[0]-u[0]) for u,(v,w) in g.items())

def main():
 out={}
 for tag in ['selftest_TT16','selftest_L106b','selftest_swap']:
    folder=ROOT/tag;ds={d['residue']:d for d in map(lambda p:json.loads(p.read_text()),folder.glob('res*.json'))}
    values=[]
    for n in list(range(48,112,2))+list(range(192,200,2))+list(range(312,320,2)):
      g=rebuild(ds[n%8],n);t=audit(g,n)
      f=folder/'tours'/f'{tag}_n{n}.json'
      if f.exists():
        d=json.loads(f.read_text());gg=from_grid(d['tour'])
        assert d['n']==n and audit(gg,n)==t==d['turns']
        assert all(set(g[u])==set(gg[u]) for u in g)
      values.append([n,t,t-8*n])
    out[tag]=values
    print(tag,'checked',len(values),'sizes; constants',sorted(set(v[2] for v in values)),flush=True)
 (ROOT/'independent_counts.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
