"""Independent T18 local and full-tour checks."""
import json,hashlib
from pathlib import Path
from check import MOVES,orient,check
from periodic import count
from turn_audit import counts

def strip():
    tpl=json.loads(Path('w-turnsbuilder/T18-P8-D4.json').read_text())
    cells=[r.split() for r in tpl];h=len(cells);w=len(cells[0])
    def adj(p):
        r,c=p;s=cells[r][c%w] if 0<=r<h else '26'
        return [(r+MOVES[int(k)][0],c+MOVES[int(k)][1]) for k in s]
    for r in range(h):
        for c in range(w):
            p=(r,c)
            for q in adj(p):
                assert q[0]<h and p in adj(q),('strip edge',p,q)
    turns=sum(orient(MOVES[int(s[0])],(0,0),MOVES[int(s[1])])!=0 for row in cells for s in row)
    ends=[];visited=set()
    for r in range(h):
        for c in range(-24,25):
            p=(r,c)
            for q in adj(p):
                label=q[1]+2*(h-1-q[0])
                if q[0]<0 and 0<=label<8:
                    prev=q;cur=p;seen=set()
                    while cur[0]>=0:
                        assert cur not in seen and len(seen)<1000,'cycle or long path'
                        seen.add(cur);visited.add((cur[0],cur[1]%w))
                        nxt=next(a for a in adj(cur) if a!=prev);prev,cur=cur,nxt
                    other=cur[1]+2*(h-1-cur[0]);ends.append((label,other))
    assert len(ends)==8 and len(visited)==h*w,(ends,len(visited))
    return dict(turns=turns,crossings=count(tpl,'bottom'),terminal_pairs=sorted(ends),covered_period_cells=len(visited))

def main():
    local=strip();rows=[]
    for f in sorted(Path('runs/t18').glob('T18_n*.json')):
        raw=f.read_bytes();d=json.loads(raw);x,t=check(d['tour']);_,s=counts(d['tour']);n=len(d['tour'])
        assert x==d['crossings'] and t==d['turns']
        rows.append(dict(file=str(f),n=n,X=x,T=t,T_minus_8_5n=t-8.5*n,strips=s,info=d.get('info'),sha256=hashlib.sha256(raw).hexdigest()))
    result=dict(date='2026-10-02',strip=local,tours=rows)
    Path('w-verifier/t18_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
