"""Independent corner reuse assembly. No kt or worker code imports."""
import json,hashlib
from pathlib import Path
from check import MOVES,check


def grid(d,n):
    z=d['Z'];B=[r.split() for r in d['bottom']];L=[r.split() for r in d['left']]
    h=len(B);p=len(B[0]);q=len(L);w=len(L[0])
    assert d['off_L']==0 and z==6 and p==8 and q==4
    # Coordinates (x,y), y upward. Convert to row-down only at the end.
    def vec(s):return [(MOVES[int(k)][1],-MOVES[int(k)][0]) for k in s]
    xphase=(13-2*n)%8;yphase=(-n//2)%4
    g=[];origins={'BL':(0,0),'BR':(n-z,0),'TL':(0,n-z),'TR':(n-z,n-z)}
    patches={}
    for key,ds in d['zones'].items():
        tag,coords=key.split(':');u,v=map(int,coords.split(','));ox,oy=origins[tag]
        assert 0<=u<z and 0<=v<z
        patches[ox+u,oy+v]=[tuple(a) for a in ds]
    assert len(patches)==4*z*z
    codes={(dj,-di):str(k) for k,(di,dj) in enumerate(MOVES)}
    for r in range(n):
        y=n-1-r;row=[]
        for x in range(n):
            ds=[(2,-1),(-2,1)]
            if y<h:ds=vec(B[h-1-y][x%p])
            if y>=n-h:ds=[(-a,-b) for a,b in vec(B[y-(n-h)][(xphase-x)%p])]
            if x<w:ds=vec(L[q-1-((y-2)%q)][x])
            if x>=n-w:ds=[(-a,-b) for a,b in vec(L[q-1-((yphase-y)%q)][n-1-x])]
            if (x,y) in patches:ds=patches[x,y]
            row.append(''.join(sorted(codes[t] for t in ds)))
        g.append(row)
    return g


def outside(g,z=6):
    n=len(g)
    def free(p):return (p[0]<z or p[0]>=n-z) and (p[1]<z or p[1]>=n-z)
    def norm(p):return (p[0]>=n-z,p[1]>=n-z,min(p[0],n-1-p[0]),min(p[1],n-1-p[1]))
    adj={}
    for r in range(n):
        for c in range(n):
            if not free((r,c)):adj[r,c]=[(r+MOVES[int(k)][0],c+MOVES[int(k)][1]) for k in g[r][c]]
    seen=set();pairs=[]
    for p,ns in adj.items():
        if p in seen:continue
        ends=[a for a in ns if free(a)]
        if not ends:continue
        u=ends[0];prev=u;cur=p;first=p
        while not free(cur):
            assert cur not in seen,'outside cycle'
            seen.add(cur);nxt=next(a for a in adj[cur] if a!=prev);prev,cur=cur,nxt
        # Keep the incidence direction as well as the corner cell.
        a=(norm(u),(first[0]-u[0],first[1]-u[1]))
        b=(norm(cur),(prev[0]-cur[0],prev[1]-cur[1]))
        pairs.append(tuple(sorted((a,b))))
    assert len(seen)==len(adj),'closed outside component'
    return tuple(sorted(pairs))


def main():
    results=[]
    for f in sorted(Path('w-integrator/corners').glob('*.json')):
        raw=f.read_bytes();d=json.loads(raw);n0=d['n0'];fam='T18' if f.name.startswith('T18') else 'H16a';row=[];signature=None
        for k in (0,1,8):
            n=n0+24*k;g=grid(d,n);x,t=check(g);m=outside(g)
            if signature is None:signature=m;bx=x;bt=t
            else:
                assert m==signature,('matching changed',f,n)
                assert x-bx==(306 if fam=='T18' else 216)*k
                assert t-bt==(204 if fam=='T18' else 246)*k
            expected=(-17,-19,-19,-20)[n%8//2] if fam=='T18' else {0:5,2:0,4:7,6:3,8:5,10:0,12:7,14:1,16:5,18:0,20:7,22:2}[n%24]
            assert (t-8.5*n if fam=='T18' else x-9*n)==expected
            row.append(dict(n=n,k=k,X=x,T=t,outside_paths=len(m)))
        results.append(dict(file=str(f),sha256=hashlib.sha256(raw).hexdigest(),checks=row))
        print(f.name,row,flush=True)
    Path('w-verifier/reuse_results.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
