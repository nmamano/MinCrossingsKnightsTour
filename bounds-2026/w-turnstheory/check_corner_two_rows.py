#!/usr/bin/env python3
"""Exact corner charge from two good rows near each endpoint; no solver.
The interior part of either boundary arc is removed by degree-two identities.
"""
from itertools import product,combinations
from check_knight_tiles import cross
MOV=[(x,y) for x in (-2,-1,1,2) for y in (-2,-1,1,2) if abs(x)+abs(y)==3]
chi=lambda u:1 if sum(u)%2==0 else -1
edge=lambda a,b:tuple(sorted((a,b)))
K={(0,y) for y in range(4)}|{(x,0) for x in range(1,4)}

def corner_options():
    opts=[]
    for u in sorted(K):
        neighbours=[(u[0]+dx,u[1]+dy) for dx,dy in MOV if u[0]+dx>=0 and u[1]+dy>=0]
        opts.append([set(edge(u,v) for v in pair) for pair in combinations(neighbours,2)])
    out=[]
    for choices in product(*opts):
        E=set().union(*choices)
        if all(sum(v in e for e in E)==2 for v in K):out.append(E)
    return out

def path(R):
    points=[(3,2*R+1),(1,2*R+1)]
    points.extend((1,y) for y in range(2*R-1,0,-2))
    points.extend((x,1) for x in range(3,2*R+2,2))
    points.append((2*R+1,3))
    return list(zip(points,points[1:]))

def coeff(e,segments):
    E=tuple((2*x,2*y) for x,y in e); out=0
    for a,b in segments:
        if cross(E,(a,b)):
            det=(b[0]-a[0])*(E[0][1]-a[1])-(b[1]-a[1])*(E[0][0]-a[0])
            out+=chi(e[0] if det>0 else e[1])
    return out

def fixed_pattern(R,left,bottom):
    F=set(); E=set()
    for transpose,sign in ((False,left),(True,bottom)):
        f=lambda u:(u[1],u[0]) if transpose else u
        for y in range(R,R+2):
            for x,nb in ((0,((2,y+sign),(1,y+2*sign))),
                         (1,((3,y+sign),(0,y-2*sign)))):
                u=f((x,y)); F.add(u)
                E.update(edge(u,f(v)) for v in nb)
    return F,E

def main():
    options=corner_options(); assert len(options)==2916
    for R in (12,13,14,15):
        segs=path(R); baseline=0
        for a,b in segs:
            dx,dy=b[0]-a[0],b[1]-a[1]
            xx,yy=a[0]+b[0]+dy,a[1]+b[1]-dx
            assert xx%4==yy%4==0
            baseline-=chi((xx//4,yy//4))
        middle={(0,y) for y in range(4,R)}|{(x,0) for x in range(4,R)}
        candidates=set()
        for u in product(range(R+6),repeat=2):
            if min(u)>1:continue
            for dx,dy in MOV:
                v=(u[0]+dx,u[1]+dy)
                if min(v)>=0:candidates.add(edge(u,v))
        residual={e:coeff(e,segs)+sum(chi(v) for v in e if v in middle) for e in candidates}
        const=baseline-2*sum(chi(v) for v in middle)
        corner_values=[sum(residual[e] for e in E) for E in options]
        for L,B in product((1,-1),repeat=2):
            F,known=fixed_pattern(R,L,B)
            assert all(c==0 or any(v in K or v in F for v in e) for e,c in residual.items())
            assert not K & F
            assert all(not any(v in K for v in e) for e in known)
            fixed=sum(residual[e] for e in known)
            values={(const+fixed+c)%3 for c in corner_values}
            assert values=={1},(R,L,B,values)
        print('PASS: R',R,'two endpoint rows; all 4 patterns and 2916 corner choices; Q=1 mod 3.')
    print('The R -> R+2 step adds two opposite-colour middle cells per side and translates the endpoint data.')

if __name__=='__main__':main()
