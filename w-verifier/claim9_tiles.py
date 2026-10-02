"""Independent exact polygon-intersection and signed-flux audit. No worker imports."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from collections import Counter
from pathlib import Path
import json
D=((1,-2),(1,2),(2,-1),(2,1))

def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def hull(points):
    points=sorted(set(points));lo=[];hi=[]
    for p in points:
        while len(lo)>=2 and det(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(points):
        while len(hi)>=2 and det(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    return lo[:-1]+hi[:-1]

def clip(poly,window):
    for a,b in zip(window,window[1:]+window[:1]):
        out=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            dp,dq=det(a,b,p),det(a,b,q)
            if dp>=0:out.append(p)
            if (dp<0<dq) or (dq<0<dp):
                t=F(dp,dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
            elif dp<0 and dq==0:out.append(q)
        poly=out
        if not poly:break
    return poly

def area(poly):
    return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/F(2) if poly else F(0)

def proper(e,f):
    a,b=e;c,d=f
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

@lru_cache(None)
def tile(e):
    a,b=e;mid=((a[0]+b[0])/F(2),(a[1]+b[1])/F(2))
    axis=(0,F(1,2)) if abs(a[0]-b[0])==2 else (F(1,2),0)
    q=(mid[0]-axis[0],mid[1]-axis[1]);r=(mid[0]+axis[0],mid[1]+axis[1])
    p=hull([a,b,q,r]);assert area(p)==1
    return p,(q,r)

def quarter(i,j,k):
    corners=[(F(i),F(j)),(F(i+1),F(j)),(F(i+1),F(j+1)),(F(i),F(j+1))]
    return [corners[k],corners[(k+1)%4],(F(2*i+1,2),F(2*j+1,2))]

@lru_cache(None)
def quarters(e):
    p,_=tile(e);out=set()
    for i in range(int(min(v[0] for v in p)),int(max(v[0] for v in p))):
        for j in range(int(min(v[1] for v in p)),int(max(v[1] for v in p))):
            for k in range(4):
                z=area(clip(quarter(i,j,k),p));assert z in (0,F(1,4))
                if z:out.add((i,j,k))
    assert len(out)==4
    return frozenset(out)

def main():
    counts=Counter();pairs=0;shared=0
    for dx,dy in D:
        e=((0,0),(dx,dy));A,_=tile(e)
        for x,y in product(range(-4,5),repeat=2):
            for u,v in D:
                f=((x,y),(x+u,y+v))
                if f==e:continue
                B,_=tile(f);overlap=area(clip(A,B));cross=proper(e,f)
                assert (overlap>0)==cross,(e,f,overlap,cross)
                assert overlap in (0,F(1,4),F(1,2))
                common=len(quarters(e)&quarters(f));assert F(common,4)==overlap
                if set(e)&set(f):assert overlap==0;shared+=1
                counts[str(overlap)]+=1;pairs+=1
    fluxes=0
    for ox,oy in product(range(2),repeat=2):
        for axis in (0,1):
            a=(ox,oy);b=(ox+int(axis==0),oy+int(axis==1))
            mid=((a[0]+b[0])/F(2),(a[1]+b[1])/F(2));tangent=(0,F(1,2)) if axis==0 else (F(1,2),0)
            dual=((mid[0]-tangent[0],mid[1]-tangent[1]),(mid[0]+tangent[0],mid[1]+tangent[1]))
            adjacent=[]
            for i in range(ox-1,ox+2):
                for j in range(oy-1,oy+2):
                    for k in range(4):
                        tri=quarter(i,j,k)
                        if set((a,b))<=set(tri):adjacent.append((i,j,k))
            assert len(adjacent)==2
            for sign in (-1,1):
                aa=a if sign==1 else b;chi=1 if sum(aa)%2==0 else -1
                for x,y in product(range(-4,5),repeat=2):
                    for dx,dy in D:
                        e=((ox+x,oy+y),(ox+x+dx,oy+y+dy));black,white=e if sum(e[0])%2==0 else tuple(reversed(e))
                        flux=0
                        if proper(e,dual):flux=1 if sign*(white[axis]-black[axis])>0 else -1
                        _,short=tile(e);g=int(set(short)==set((a,b)));m=sum(v in quarters(e) for v in adjacent)
                        assert flux==chi*(m-3*g),(e,a,b,sign,flux,m,g)
                        assert (flux+chi-chi*(m+1))%3==0
                        fluxes+=1
    result=dict(date='2026-10-02',tile_pairs=pairs,areas=dict(counts),shared_endpoint_cases=shared,flux_cases=fluxes,method='rational polygon clipping; exact quarter-triangle areas; oriented proper intersection')
    Path('w-verifier/claim9_geometry.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
if __name__=='__main__':main()
