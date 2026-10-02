"""Independent test of the exterior reduced-graph isomorphism in PROOFS.md."""
import json
from pathlib import Path
from collections import Counter
from check import MOVES
from reuse_audit import grid as hgrid
from tt16_audit import build as tgrid

def reduced(g):
    n=len(g)
    def keep(p):
        x,y=p
        return x<2 or x>=n-2 or y<4 or y>=n-4 or ((x<6 or x>=n-6) and (y<6 or y>=n-6))
    adj={}
    for r,row in enumerate(g):
        for x,code in enumerate(row):
            u=(x,n-1-r);adj[u]=[(x+MOVES[int(k)][1],n-1-r-MOVES[int(k)][0]) for k in code]
    vertices={u for u in adj if keep(u)};E=Counter();covered=set(vertices)
    for u in vertices:
        for v in adj[u]:
            prev=u;cur=v
            while cur not in vertices:
                covered.add(cur);assert cur[0]+2*cur[1]==u[0]+2*u[1]
                nex=next(w for w in adj[cur] if w!=prev);prev,cur=cur,nex
            E[tuple(sorted((u,cur)))]+=1
    assert len(covered)==n*n
    assert all(v==2 for v in E.values())
    return vertices,Counter({e:1 for e in E})

def label(u):return u[0]+2*u[1]

def portname(u,v,a,n):
    if label(u)>label(v):u,v=v,u
    choices=[]
    if max(u[1],v[1])<4:choices.append(('B',u[1],v[1]))
    if min(u[1],v[1])>=n-4:choices.append(('T',n-1-u[1],n-1-v[1]))
    if max(u[0],v[0])<2:choices.append(('L',u[0],v[0]))
    if min(u[0],v[0])>=n-2:choices.append(('R',n-1-u[0],n-1-v[0]))
    assert len(choices)==1
    return choices[0]+(label(u)-a,label(v)-a)

def exterior(V,E,n,cuts,width,transport):
    def block(u):
        return next((i for i,a in enumerate(cuts) if a<=label(u)<a+width),None)
    def node(u):return ('v',)+transport(u)
    vertices={node(u) for u in V if block(u) is None};edges=Counter()
    for (u,v),mult in E.items():
        i,j=block(u),block(v)
        if i is not None and j is not None:assert i==j;continue
        if i is None and j is None:a,b=node(u),node(v)
        else:
            inner,outer,idx=(u,v,i) if i is not None else (v,u,j)
            side=int(label(outer)>=cuts[idx]+width)
            a=node(outer);b=('p',idx,side)+portname(inner,outer,cuts[idx]+side*width,n);vertices.add(b)
        edges[tuple(sorted((a,b),key=repr))]+=mult
    return vertices,edges

def main():
    rows=[]
    for family,period,pattern,builder in [('H16a',24,'H16a_VE_res*.json',hgrid),('TT16',8,'TT16_res*.json',tgrid)]:
        for f in sorted(Path('w-integrator/corners').glob(pattern)):
            d=json.loads(f.read_text());n=96+d['n0']%period
            cuts=[36 if family=='H16a' else 35,((n+39)//8)*8,((2*n+39)//8)*8 if family=='H16a' else 2*n+32]
            def transport(u):
                x,y=u;r=sum(label(u)>=a+8 for a in cuts)
                if (x<6 or x>=n-6) and (y<6 or y>=n-6):return x+period*(x>=n-6),y+period*(y>=n-6)
                if y<4:return x+r*period,y
                if x<2:return x,y+r*period//2
                if x>=n-2:return x+period,y+(r-1)*period//2
                if y>=n-4:return x+(r-2)*period,y+period
                raise AssertionError(u)
            V,E=reduced(builder(d,n));V2,E2=reduced(builder(d,n+period))
            A=exterior(V,E,n,cuts,8,transport)
            B=exterior(V2,E2,n+period,[a+i*period for i,a in enumerate(cuts)],8+period,lambda u:u)
            assert A==B,(family,n,len(A[0]),len(B[0]),len(A[0]^B[0]))
            rows.append(dict(family=family,n=n,larger=n+period,exterior_vertices=len(A[0]),exterior_edges=sum(A[1].values())))
    Path('w-verifier/claim7_transport.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('PASS: exact exterior graph isomorphism for all',len(rows),'phase cases.')
if __name__=='__main__':main()
