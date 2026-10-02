#!/usr/bin/env python3
"""Exact finite checks for PROOFS.md. Python standard library; no solver."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRS = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))

def template(rows):
    rows = [r.split() for r in rows]
    return {(x,len(rows)-1-r):tuple(DIRS[int(k)] for k in s)
            for r,row in enumerate(rows) for x,s in enumerate(row)},len(rows[0]),len(rows)

def graph(d,n):
    B,P,D = template(d['bottom']); T,PT,DT = template(d.get('top',d['bottom']))
    L,W,Q = template(d['left']); R,WR,QR = template(d.get('right',d['left']))
    xb,xt,yl,yr = d.get('phases',(0,(13-2*n)%8,2,(-n//2)%4))
    g = {}
    for x in range(n):
        for y in range(n):
            ds = ((2,-1),(-2,1))
            if y<D: ds=B[((x-xb)%P,y)]
            if y>=n-DT: ds=tuple((-a,-b) for a,b in T[((xt-x)%PT,n-1-y)])
            if x<W: ds=L[(x,(y-yl)%Q)]
            if x>=n-WR: ds=tuple((-a,-b) for a,b in R[(n-1-x,(yr-y)%QR)])
            g[x,y]=tuple((x+a,y+b) for a,b in ds)
    z=d['Z']; anchors={'BL':(0,0),'BR':(n-z,0),'TL':(0,n-z),'TR':(n-z,n-z)}
    for name,ds in d['zones'].items():
        corner,uv=name.split(':'); u,v=map(int,uv.split(',')); a,b=anchors[corner]; x,y=a+u,b+v
        g[x,y]=tuple((x+dx,y+dy) for dx,dy in ds)
    return g

def validate(g):
    for u,vs in g.items():
        assert len(set(vs))==2
        for v in vs:
            assert v in g and u in g[v], (u,v)
            assert sorted(map(abs,(v[0]-u[0],v[1]-u[1])))==[1,2]
    start=next(iter(g)); prev=None; u=start; seen=set()
    while u not in seen:
        seen.add(u); v=next(v for v in g[u] if v!=prev); prev,u=u,v
    assert u==start and len(seen)==len(g), (len(seen),len(g))

def line(v): return v[0]+2*v[1]

def port(u,v,a,n):
    if line(u)>line(v): u,v=v,u
    # A cut edge is inside exactly one of the four bands.
    sides=[]
    if max(u[1],v[1])<4: sides.append(('B',u[1],v[1]))
    if min(u[1],v[1])>=n-4: sides.append(('T',n-1-u[1],n-1-v[1]))
    if max(u[0],v[0])<2: sides.append(('L',u[0],v[0]))
    if min(u[0],v[0])>=n-2: sides.append(('R',n-1-u[0],n-1-v[0]))
    assert len(sides)==1,(u,v,sides)
    return sides[0]+(line(u)-a,line(v)-a)

def slab(g,n,a,width=8):
    """Return port names and path matching of one slab; reject closed components."""
    vertices={u for u in g if a<=line(u)<a+width}
    ports={}; names=[set(),set()]
    for u in vertices:
        for v in g[u]:
            if v not in vertices:
                side=int(line(v)>=a+width)
                key=port(u,v,a+side*width,n)
                assert (side,key) not in ports
                ports[side,key]=(u,v); names[side].add(key)
    assert names[0]==names[1]
    keys=sorted(names[0]); seen=set(); matching={}
    for (side,key),(u,prev) in ports.items():
        begin=(side,keys.index(key))
        if begin in matching: continue
        while u in vertices:
            assert u not in seen, ('closed component',n,a,u)
            seen.add(u); nxt=next(v for v in g[u] if v!=prev); prev,u=u,nxt
        endside=int(line(u)>=a+width)
        end=(endside,keys.index(port(prev,u,a+endside*width,n)))
        assert end!=begin
        matching[begin]=end; matching[end]=begin
    assert seen==vertices, ('uncovered cycle',n,a,len(vertices-seen))
    return keys,matching

def compose(A,B):
    """Glue the right ports of A to the left ports of B. Reject closed cycles."""
    adj={}
    for matching,offset in ((A,0),(B,1)):
        for (s,i),(t,j) in matching.items():
            adj.setdefault((s+offset,i),[]).append((t+offset,j))
    seen=set(); out={}
    for u in adj:
        if u[0]==1 or u in seen: continue
        prev=None; v=u
        while True:
            seen.add(v)
            nxt=[w for w in adj[v] if w!=prev]
            assert len(nxt)==1
            prev,v=v,nxt[0]
            if v[0]!=1: break
            assert v not in seen
        seen.add(v)
        a=(u[0]//2,u[1]); b=(v[0]//2,v[1]); out[a]=b; out[b]=a
    assert seen==set(adj), 'closed cycle on gluing'
    return out

def configs():
    for kind,p,glob in [('TT16',8,'TT16_res*.json'),('H16a',24,'H16a_VE_res*.json')]:
        for f in sorted((ROOT/'w-integrator/corners').glob(glob)):
            yield kind,p,f,json.loads(f.read_text())

def turns(g):
    return sum(v[0]+w[0]!=2*u[0] or v[1]+w[1]!=2*u[1]
               for u,(v,w) in g.items())

def crossing_pairs(edges):
    # Exact integer orientation. Grid buckets only remove pairs with disjoint boxes.
    def orient(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    buckets={}
    for e in sorted(edges):
        a,b=e; candidates=set(); cells=[]
        for x in range(min(a[0],b[0]),max(a[0],b[0])+1):
            for y in range(min(a[1],b[1]),max(a[1],b[1])+1):
                cells.append((x,y)); candidates.update(buckets.get((x,y),()))
        for f in candidates:
            c,d=f
            if a in f or b in f: continue
            if orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0:
                yield e,f
        for cell in cells: buckets.setdefault(cell,[]).append(e)

def crossings(g):
    return sum(1 for _ in crossing_pairs({tuple(sorted((u,v))) for u in g for v in g[u]}))

def band_cost(rows,kind):
    """One infinite-band period, plus straight interior edges within crossing range."""
    mv,W,H=template(rows); P,D=(W,H) if kind=='B' else (H,W)
    xy=lambda s,d:(s,d) if kind=='B' else (d,s)
    sd=lambda u:u if kind=='B' else (u[1],u[0])
    g={}
    for s in range(-8,P+9):
        for dep in range(D+6):
            u=xy(s,dep)
            ds=mv[xy(s%P,dep)] if dep<D else ((2,-1),(-2,1))
            g[u]=tuple((u[0]+dx,u[1]+dy) for dx,dy in ds)
    # Check all local incidences, including edges to the straight interior.
    for u in g:
        s,dep=sd(u)
        if 0<=s<P and dep<D+3:
            for v in g[u]:
                assert v in g and u in g[v]
    E={tuple(sorted((u,v))) for u in g for v in g[u] if v in g}
    X=sum(0<=min(sd(v)[0] for e in pair for v in e)<P for pair in crossing_pairs(E))
    T=sum(1 for u,(v,w) in g.items() if 0<=sd(u)[0]<P and sd(u)[1]<D
          and (v[0]+w[0],v[1]+w[1])!=(2*u[0],2*u[1]))
    return P,T,X

def tour_grid(rows):
    n=len(rows); g={}
    for r,row in enumerate(rows):
        for x,code in enumerate(row):
            u=(x,n-1-r)
            g[u]=tuple((u[0]+DIRS[int(k)][0],u[1]+DIRS[int(k)][1]) for k in code)
    return g

def power(M,k):
    out=M
    for _ in range(k-1): out=compose(out,M)
    return out

def main():
    report={'date':'2026-10-02','base_checks':[],'transfers':[],'band_costs':{}}
    cases=list(configs())
    for kind,p in (('TT16',8),('H16a',24)):
        selected=[d for k,_,_,d in cases if k==kind]
        assert len(selected)==p//2
        assert sorted(d['n0']%p for d in selected)==list(range(0,p,2))
    for kind,p,f,d in cases:
        assert d['Z']==6 and len(d['zones'])==144
        assert template(d['bottom'])[1:]==(8,4)
        assert template(d['left'])[1:]==(2,4)
        if kind=='TT16':
            assert d['phases']==[0,1,0,0]
            assert template(d['top'])[1:]==(8,4)
            assert template(d['right'])[1:]==(2,4)
        # Check all even sizes below 96, and one induction base >=96 per residue.
        start=d['n0']
        n=start
        while n<96+p:
            g=graph(d,n); validate(g)
            cost=turns(g) if kind=='TT16' else crossings(g)
            assert cost==8*n-14 if kind=='TT16' else cost<=9*n+7
            report['base_checks'].append([kind,n,cost])
            n+=p
        n-=p  # The checked induction base lies in [96,96+p).
        assert 96<=n<96+p
        g=graph(d,n)
        g2=graph(d,n+p); validate(g2)
        delta=(turns(g2)-turns(g)) if kind=='TT16' else (crossings(g2)-crossings(g))
        assert delta==(64 if kind=='TT16' else 216)
        cuts=[35 if kind=='TT16' else 36, ((n+39)//8)*8,
              2*n+32 if kind=='TT16' else ((2*n+39)//8)*8]
        for region,a in enumerate(cuts):
            assert 24<a-region*n and a+8<(region+1)*n-24
            names,M=slab(g,n,a)
            assert power(M,1+p//8)==M
            # Local equivalence when n grows; positions beyond earlier insertions shift.
            names2,M2=slab(g2,n+p,a+region*p)
            assert (names2,M2)==(names,M)
            # Check actual longer slab against composition, including all its vertices.
            names3,M3=slab(g2,n+p,a+region*p,8+p)
            assert (names3,M3)==(names,M)
            through=sorted((i,j) for (s,i),(t,j) in M.items() if s==0 and t==1)
            assert len(through)==([2,4,2][region] if kind=='TT16' else 4)
            if kind=='H16a':
                assert len(names)==4
                assert [j for i,j in through]==[[1,3,2,0],[0,1,2,3],[0,2,3,1]][region]
            else:
                expected=[
                    [((0,0),(1,3)),((0,1),(0,3)),((0,2),(1,2)),((1,0),(1,1))],
                    [((0,i),(1,i)) for i in range(4)],
                    [((0,0),(0,2)),((0,1),(1,3)),((0,3),(0,5)),
                     ((0,4),(1,0)),((1,1),(1,5)),((1,2),(1,4))]][region]
                assert M=={a:b for u,v in expected for a,b in ((u,v),(v,u))}
            report['transfers'].append({'kind':kind,'n':n,'region':region,'cut':a,
                'ports':names,'matching':sorted([list(u),list(v)] for u,v in M.items() if u<v),
                'through':through,'identity':'M^2=M' if kind=='TT16' else 'M^4=M'})
        if kind not in report['band_costs']:
            bc={name:band_cost(d.get(name,d['bottom'] if name=='top' else d['left']),
                              'B' if name in ('bottom','top') else 'L')
                for name in ('bottom','top','left','right')}
            assert sum(p//v[0]*v[1] for v in bc.values())==64 if kind=='TT16' else sum(p//v[0]*v[2] for v in bc.values())==216
            report['band_costs'][kind]=bc
    for n in (48,50,52,54):
        d=json.loads((ROOT/f'w-integrator/tours/TT16_n{n}.json').read_text())
        g=tour_grid(d['tour']); validate(g); assert turns(g)==8*n-14
        report['base_checks'].append(['TT16',n,turns(g)])
    out=Path(__file__).with_name('upper_proof_checks.json')
    out.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(report['base_checks']),'base tours;',len(report['transfers']),
          'regional transfers; exact local costs',report['band_costs'])
    print('Certificate details:',out)

if __name__=='__main__': main()
