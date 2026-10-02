"""Check the area accounting and exhibit the missing U-domain restriction."""
import json
from pathlib import Path
from collections import Counter
from check import MOVES,check
from claim9_tiles import quarters,D

def main():
    base={d:quarters(((0,0),d)) for d in D};results=[]
    for path in ['w-integrator/tours/certificates/TT16_n56.json','w-integrator/tours/H16a_VerticalEdge_off0_small_n48.json']:
        doc=json.loads(Path(path).read_text());g=doc['tour'];n=len(g);X,T=check(g);E=set()
        for r,row in enumerate(g):
            for x,s in enumerate(row):
                a=(x,n-1-r)
                for k in s:E.add(tuple(sorted((a,(a[0]+MOVES[int(k)][1],a[1]-MOVES[int(k)][0])))))
        m=Counter()
        for a,b in E:
            dx,dy=b[0]-a[0],b[1]-a[1]
            for i,j,k in base[dx,dy]:
                cell=(int(i+a[0]),int(j+a[1]),k);assert 0<=cell[0]<n-1 and 0<=cell[1]<n-1;m[cell]+=1
        G=4*(n-1)**2-len(m);excess=sum(v-1 for v in m.values());pair_area=sum(v*(v-1)//2 for v in m.values())
        assert sum(m.values())==4*n*n and excess==8*n-4+G
        assert excess<=pair_area<=2*X and G<=2*X-8*n+4
        results.append(dict(file=path,n=n,X=X,G=G,excess=excess,pair_overlap_quarters=pair_area,gap_bound=2*X-8*n+4))
    example=results[0]
    counter=dict(tour=example['file'],n=example['n'],X=example['X'],B_size=example['X'],U_outside_size=example['gap_bound']+1,claimed_bad_triangle_bound=example['gap_bound'],construction='U={(56+j,0,0): j=0,...,616}; B is all crossing pairs; all U triangles are uncovered and all B overlaps avoid U.')
    report=dict(date='2026-10-02',board_checks=results,scope_counterexample=counter)
    Path('w-verifier/claim9_board_results.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':main()
