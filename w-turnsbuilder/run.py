import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kt.strip import Strip
from kt.search import solve, to_template, build_model
from kt.verify_strip import check_bottom
from kt.core import MI, MJ
from ortools.sat.python import cp_model

OUT = Path(__file__).parent

def verify(tpl):
    rows = [r.split() for r in tpl]
    D, P = len(rows), len(rows[0])
    def neighbors(u):
        x, y = u
        return [(x + MJ[int(c)], y - MI[int(c)]) for c in rows[D-1-y][x % P]]
    covered = set()
    pairing = []
    turns = 0
    for y in range(D):
        for x in range(P):
            u = (x,y)
            a,b = neighbors(u)
            assert a[1] >= 0 and b[1] >= 0
            turns += (a[0]+b[0],a[1]+b[1]) != (2*x,2*y)
            for v in (a,b):
                if v[1] < D:
                    assert u in neighbors(v)
    for x in range(P):
        prev, cur = (x-2,D), (x,D-1)
        seen = set()
        for step in range(P*D+1):
            canonical = (cur[0]%P,cur[1])
            assert canonical not in seen, 'cycle or winding path'
            seen.add(canonical)
            covered.add(canonical)
            ns = [v for v in neighbors(cur) if v != prev]
            assert len(ns) == 1
            prev,cur = cur,ns[0]
            if cur[1] >= D:
                pairing.append([x+2*(D-1),prev[0]+2*prev[1]])
                break
        else:
            raise AssertionError('nonterminal path')
    assert len(covered) == P*D
    return {'turns':int(turns),'line_pairing':pairing,'all_cells_on_finite_paths':True}

def main():
    mode = sys.argv[1]
    for P in (8,16,24):
        for D in (4,5,6):
            st = Strip('bottom',P,D)
            result = solve(st,wX=0,wT=1,lanes=mode=='lanes',workers=1,time_limit=30)
            result.update(P=P,D=D,lanes=mode=='lanes',date='2026-10-02')
            if 'chosen' in result:
                tpl = to_template(st,result['chosen'])
                result['template']=tpl
                result['unrolled']=check_bottom(tpl)
                result['independent']=verify(tpl)
                assert not result['unrolled']['bad']
                assert result['unrolled']['crossings_per_period']==result['X']
                assert result['independent']['turns']==result['T']
                if mode=='lanes': assert result['unrolled']['lane_ok']
            (OUT / f'{mode}-{P}-{D}.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps({k:v for k,v in result.items() if k not in ('chosen','template','unrolled','independent')}),flush=True)

if __name__=='__main__': main()
