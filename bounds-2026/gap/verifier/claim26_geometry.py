"""Independent local geometry, half-scan, and constant checks for Claim 26.

Uses only prior verifier tile/tour helpers plus the new verifier scan.
No worker implementation is imported. Run from the research root.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'w-verifier'))
from claim9_tiles import quarters
from check import check as check_tour, MOVES
from claim26_certificate import edge, cross, boundary, transitions, TERMS, EXC

M=[(x,y) for x,y in product((-2,-1,1,2),repeat=2) if abs(x)+abs(y)==3]

def main():
    report={'date':'2026-10-03'}
    # Enumerate every boundary crossing type up to a row translation.
    pairs=set()
    for a in ((1,2),(1,-2),(2,1),(2,-1)):
        e=edge((0,0),a)
        for y in range(5):
            for dx,dy in ((1,2),(1,-2),(2,1),(2,-1)):
                f=edge((0,y),(dx,y+dy))
                if cross(e,f):
                    pairs.add(tuple(sorted((e,f))))
    # The author counts both anchored orders (20). Here the lower
    # boundary endpoint is first, leaving 10 unordered types.
    assert len(pairs)==10
    for e,f in pairs:
        overlap=quarters(e)&quarters(f)
        assert 1<=len(overlap)<=2
        assert all(x<=1 for x,y,z in overlap)
        for x,y,z in overlap:
            if x==1:
                assert set((e,f))==set((edge((0,y),(2,y+1)),edge((0,y+1),(2,y))))
    report['all_boundary_overlap_types']=len(pairs)

    # Adjacent boundary sets share only these four edges.
    corner_edges=[edge((0,0),(1,2)),edge((0,0),(2,1)),
                  edge((0,1),(2,0)),edge((0,2),(1,0))]
    duplicated_pairs=sum(cross(a,b) for a,b in combinations(corner_edges,2))
    assert duplicated_pairs==5
    square_edges={edge((x,y),(x+dx,y+dy)) for x,y in product(range(4),repeat=2)
                  for dx,dy in M if 0<=x+dx<4 and 0<=y+dy<4}
    assert len(square_edges)==24
    report['boundary_union_error']=4*duplicated_pairs
    report['width_two_union_error']=4*(24*23//2)

    # Check the endpoint identity directly for every possible local edge.
    coeff={edge(a,b):c for a,b,c in TERMS}
    identity_cases=0
    for r in (12,13):
        edges={edge((x,y),(x+dx,y+dy)) for x in range(5) for y in range(r-3,r+4)
               for dx,dy in M if 0<=x+dx<5 and r-3<=y+dy<r+4}
        dual=((3,2*r+1),(-1,2*r+1))
        for e in edges:
            a,b=e
            ee=tuple((2*x,2*y) for x,y in e)
            value=0
            if cross(ee,dual):
                value=(-1)**(r+sum(a))*(1 if b[1]>a[1] else -1)
            local=edge((a[0],a[1]-r),(b[0],b[1]-r))
            assert value==coeff.get(local,0)+int((0,r) in e),(r,e,value)
            identity_cases+=1
    report['endpoint_identity_cases']=identity_cases
    for h,k,e,f in product(range(3),range(3),(0,1),(0,1)):
        t=2 if e else (1,2,0)[h]
        u=2 if f else (1,2,0)[k]
        assert 2*int(e or f or (h+k)%3==0)<=t+u
    report['loss_cases']=36

    # Check retained path squares and half-walk parity on representative sizes.
    for n in range(32,102,2):
        h=n//2; used=set(); total=0
        for fx,fy in product((0,1),repeat=2):
            for r in range(12,h-3):
                squares={(r,j) for j in range(1,r+1)}|{(j,r) for j in range(1,r)}
                squares={((n-2-x) if fx else x,(n-2-y) if fy else y) for x,y in squares}
                assert not (used&squares)
                assert all(0<=x<n-1 and 0<=y<n-1 for x,y in squares)
                used|=squares; total+=1
        assert total==2*n-60
        near=set(range(12,h-3)); far={n-1-r for r in near}
        assert near<=set(range(h)) and far<=set(range(h,n)) and not near&far
        for y in far:
            assert ((h-1)+(y-h))%2==(n-1-y)%2
    report['candidate_geometry_sizes']=[32,100,2]

    # Full-tour examples test assigned crossing totals across the half split.
    tour_results=[]
    for n in (96,98):
        source=ROOT/f'w-integrator/tours/FOLD24_n{n}.json'
        data=json.loads(source.read_text())
        x,turns=check_tour(data['tour'])
        assert x==data['crossings'] and turns==data['turns']
        es=set()
        for r,row in enumerate(data['tour']):
            for c,code in enumerate(row):
                for v in code:
                    dr,dc=MOVES[int(v)]
                    es.add(edge((c,n-1-r),(c+dc,n-1-r-dr)))
        frames=[lambda p:p, lambda p:(n-1-p[0],p[1]),
                lambda p:(p[1],p[0]),lambda p:(n-1-p[1],p[0])]
        per_side=[]
        for transform in frames:
            local={edge(transform(a),transform(b)) for a,b in es}
            strip={e for e in local if min(p[0] for p in e)<2}
            all_pairs=[(e,f) for e,f in combinations(strip,2) if cross(e,f)]
            direct_x=len(all_pairs)
            direct_b=sum(boundary(e) and boundary(f) for e,f in all_pairs)
            assigned=[[0,0],[0,0]]
            state=(0,())
            for y,col in product(range(n),range(4)):
                target_edges={((a[0],a[1]-y),(b[0],b[1]-y))
                              for e in strip for a,b in [tuple(sorted(e,key=lambda p:(p[1],p[0])))]
                              if a==(col,y)}
                matches=[]
                for target,w,w0 in transitions(state):
                    shift=int(col==3)
                    added={((a[0],a[1]+shift),(b[0],b[1]+shift))
                           for a,b,c in target[1] if a==(col,-shift)}
                    if added==target_edges:
                        matches.append((target,w,w0))
                assert len(matches)==1
                state,w,w0=matches[0]
                assigned[int(y>=n//2)][0]+=w
                assigned[int(y>=n//2)][1]+=w0
            assert state==(0,())
            assert sum(z[0] for z in assigned)==direct_x
            assert sum(z[1] for z in assigned)==direct_b
            half_a=[]
            for half in (0,1):
                sign=1 if half==0 else -1
                twice_a=0
                for y in range(half*(n//2),(half+1)*(n//2)):
                    tr=lambda p:(p[0],y+sign*p[1])
                    f=sum(c for a,b,c in TERMS if edge(tr(a),tr(b)) in strip)
                    exc=all(edge(tr(a),tr(b)) in strip for a,b in EXC)
                    r=y if half==0 else n-1-y
                    c=(-1)**r
                    hh=((1+c)//2+c*(f+2))%3
                    twice_a+=2 if exc else (1,2,0)[hh]
                left=12*(assigned[half][0]-n//2)+16*(assigned[half][1]-n//2)-8*twice_a
                assert left>=(-155 if half==0 else -159)
                half_a.append(str(Q(twice_a,2)))
            per_side.append({'X':direct_x,'B':direct_b,'half_assignments':assigned,'half_penalties':half_a})
        assert sum(z['X'] for z in per_side)<=x+1104
        tour_results.append({'n':n,'X':x,'sides':per_side})
    report['tour_half_scan_checks']=tour_results

    # Exact algebra, with four half walks in each orientation.
    beta=Q(4,3)
    half_error=4*Q(155,12)+4*Q(159,12)
    assert half_error==Q(314,3)
    d_error=Q(1104-2)
    ar_error=(d_error+half_error)/beta
    assert ar_error==905
    u1_error=2*60+2*(20-2)
    assert u1_error==156
    e_coefficient=4+2/beta
    e_error=2*ar_error+u1_error
    assert e_coefficient==Q(11,2) and e_error==1966
    coefficient=4+4/e_coefficient
    additive=2+e_error/e_coefficient
    assert coefficient==Q(52,11) and additive==Q(3954,11)
    assert additive<360
    report['exact_bound']={'coefficient':str(coefficient),'subtracted_constant':str(additive),
                           'uniform_half_error_constant':'3958/11','rounded_constant':360,
                           'even_n_at_least':32}
    report['status']='PASS'
    Path('gap/verifier/claim26_geometry.json').write_text(json.dumps(report,indent=2))
    print('GEOMETRY, HALF SCANS, AND CONSTANT PASS',report['exact_bound'])

if __name__=='__main__':
    main()
