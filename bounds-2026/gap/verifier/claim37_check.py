"""Independent square Gap Lemma finite audit, 2026-10-03. No author imports.
Geometric quarter sampling, conditional endpoint H-bit inequality, degree <=2
only at vertices of U. Both outside split choices are SAT variables.
"""
import itertools as it, json, time, sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType
D=((1,0),(-1,0),(0,1),(0,-1))
HS=('BR','TL','RT','LB')

def canon(P):
    out=[]
    for swap in (False,True):
        for sx,sy in it.product((-1,1),repeat=2):
            Q=[(sx*(y if swap else x),sy*(x if swap else y)) for x,y in P]
            a=min(x for x,y in Q); b=min(y for x,y in Q)
            out.append(tuple(sorted((x-a,y-b) for x,y in Q)))
    return min(out)

def shapes(n):
    levels=[None,{((0,0),)}]
    for s in range(2,n+1):
        out=set()
        for pp in levels[-1]:
            p=set(pp); frontier={(x+dx,y+dy) for x,y in p for dx,dy in D}-p
            for x,y in frontier:
                if sum((x+dx,y+dy) in p for dx,dy in D)==1:
                    out.add(canon(p|{(x,y)}))
        levels.append(out)
    return levels

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull(p):
    p=sorted(set(p));lo=[];hi=[]
    for v in p:
        while len(lo)>1 and cross(lo[-2],lo[-1],v)<=0:lo.pop()
        lo.append(v)
    for v in p[::-1]:
        while len(hi)>1 and cross(hi[-2],hi[-1],v)<=0:hi.pop()
        hi.append(v)
    return lo[:-1]+hi[:-1]

@lru_cache(None)
def tile(e):
    (x,y),(u,v)=e
    if abs(u-x)==2: short=((x+1,min(y,v)),(x+1,max(y,v)))
    else: short=((x,(y+v)//2),(u,(y+v)//2))
    poly=[(6*a,6*b) for a,b in hull([e[0],e[1],*short])]
    halves=[]
    for i in range(min(x,u),max(x,u)):
        for j in range(min(y,v),max(y,v)):
            qs=[]
            for q,(a,b) in zip('BRTL',((3,1),(5,3),(3,5),(1,3))):
                z=(6*i+a,6*j+b)
                if all(cross(poly[k],poly[(k+1)%4],z)>0 for k in range(4)):qs.append(q)
            if qs:
                h=next(h for h in HS if set(h)==set(qs));halves.append(((i,j),h))
    assert len(halves)==2
    return tuple(halves)

K=((1,2),(2,1),(2,-1),(1,-2))
def model(U,slack=0,degree=True,absorbing=True):
    U=set(U);N={(x+dx,y+dy) for x,y in U for dx,dy in D}-U;S=U|N
    xs=[x for x,y in S];ys=[y for x,y in S]
    edges=[];own=defaultdict(list)
    for x in range(min(xs)-2,max(xs)+3):
        for y in range(min(ys)-2,max(ys)+3):
            for dx,dy in K:
                e=((x,y),(x+dx,y+dy));hh=tile(e)
                if not any(s in S for s,h in hh):continue
                edges.append(e)
                for z in hh:own[z].append(len(edges))
    top=len(edges);cl=[]
    def var():
        nonlocal top
        top+=1;return top
    sigma={s:var() for s in sorted(N)} # true means slash
    # Exact good halves, with split variables.
    for s in N:
        for h in HS:
            a,b=own[s,h];act=sigma[s] if h in ('BR','TL') else -sigma[s]
            cl.extend([[-act,a,b],[-act,-a,-b],[act,-a],[act,-b]])
    corners={(x+a,y+b) for x,y in U for a,b in it.product((0,1),repeat=2)}
    if degree:
        inc=defaultdict(list)
        for i,e in enumerate(edges,1):
            for v in e:
                if v in corners:inc[v].append(i)
        for ls in inc.values():cl.extend([-a,-b,-c] for a,b,c in it.combinations(ls,3))
    bad=[]
    for s in U:
        bs=[]
        for q in 'BRTL':
            ls=[i for h in HS if q in h for i in own[s,h]]
            assert len(ls)==len(set(ls))==4
            b=var();bad.append(b);bs.append(b)
            # truth table: b iff number of selected tiles != 1
            for bits in it.product((0,1),repeat=4):
                cl.append([(-i if v else i) for i,v in zip(ls,bits)]+([b] if sum(bits)!=1 else [-b]))
        cl.append(bs)
    # Derive chain segments from pairs of halves belonging to each geometric tile.
    seen=set(); cover=defaultdict(list)
    for s in sorted(U):
        for h in HS:
            z=(s,h)
            if z in seen:continue
            stack=[z];comp={z};ends=[]
            while stack:
                v=stack.pop();seen.add(v)
                for eid in own[v]:
                    other=next(t for t in tile(edges[eid-1]) if t!=v)
                    if other[0] not in U:ends.append(other)
                    elif other not in comp:comp.add(other);stack.append(other)
            assert len(ends)==2
            a,b=ends;assert a[0] in N and b[0] in N
            sa,sb=sigma[a[0]],sigma[b[0]]
            cl.extend([[-sa,sb],[sa,-sb]])
            act=sa if h in ('BR','TL') else -sa
            for ss,hh in comp:cover[ss].append(act)
            if absorbing:
                # Good endpoint bit H is its unique tile with horizontal displacement 2.
                aa=next(i for i in own[a] if edges[i-1][1][0]-edges[i-1][0][0]==2)
                bb=next(i for i in own[b] if edges[i-1][1][0]-edges[i-1][0][0]==2)
                cl.extend([[-act,aa,bb],[-act,-aa,-bb]])
    for s in U:cl.append(list(set(cover[s])))
    card=CardEnc.atmost(bad,2*len(U)+1+slack,top_id=top,encoding=EncType.totalizer)
    cl.extend(card.clauses)
    with Minisat22(bootstrap_with=cl) as solver:r=solver.solve()
    return r,len(corners),len(edges),len(cl)

if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 10
    start=time.time();levels=shapes(n);report=[]
    for s in range(1,n+1):
        sats=[];vertices=set()
        for U in sorted(levels[s]):
            r,v,e,c=model(U);vertices.add(v)
            if r:sats.append(U)
        row=dict(size=s,shapes=len(levels[s]),sat=sats,corner_counts=sorted(vertices),elapsed=round(time.time()-start,3))
        report.append(row);print(json.dumps(row),flush=True)
    sanity={}
    for name,kw in [('slack2',{'slack':2}),('no_degree',{'degree':False}),('no_absorbing',{'absorbing':False})]:
        sanity[name]=[s for s in range(1,min(n,6)+1) if any(model(U,**kw)[0] for U in levels[s])]
    print('sanity',sanity,flush=True)
    Path('gap/verifier/claim37_check.json').write_text(json.dumps(dict(levels=report,sanity=sanity),indent=2))
