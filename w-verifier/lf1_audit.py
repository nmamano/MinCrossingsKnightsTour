"""Independent LF1 counts and exact infinite-region cycle certificate."""
import json,hashlib,math
from pathlib import Path
from fractions import Fraction
from check import check,MOVES
from periodic import count
from strand_audit import pairing

def mapping(p,c,shift=0,sign=1):
    local=sign*(c-shift);block,r=divmod(local,len(p))
    return shift+sign*(block*len(p)+p[r])

def region(p,q,s,t,signp,signq):
    P=math.lcm(len(p),len(q))
    fs=[lambda c:mapping(p,c,s,signp),lambda c:mapping(q,c,t,signq)]
    # States carry line residue AND next edge color. Keep parallel edges distinct.
    unseen={(c,b) for c in range(P) for b in range(2)};cycles=[]
    for f in fs:
        for c in range(-P,2*P):assert f(f(c))==c and f(c)!=c
    while unseen:
        start=min(unseen);state=start;lift=start[0];visited=[]
        while state in unseen:
            unseen.remove(state);visited.append(state)
            lift=fs[state[1]](lift);state=(lift%P,1-state[1])
        assert state==start,'quotient map is not a permutation'
        disp=lift-start[0];assert disp%P==0
        cycles.append(dict(states=visited,displacement=disp,winding=disp//P))
    finite=any(c['displacement']==0 for c in cycles)
    strand_count=None if finite else sum(abs(c['winding']) for c in cycles)//2
    if not finite:assert sum(abs(c['winding']) for c in cycles)%2==0
    cuts=[]
    radius=max(abs(f(c)-c) for f in fs for c in range(P))
    for cut in range(P):
        cuts.append(sum(1 for f in fs for c in range(cut-radius,cut+1) if c<=cut<f(c)))
    return dict(period=P,finite_cycles=finite,strands=strand_count,cut_counts=sorted(set(cuts)),directed_quotient_cycles=cycles)

def local_edges(tpl,side):
    a=[r.split() for r in tpl];h=len(a);w=len(a[0])
    def adj(x,y):
        s=a[h-1-y][x%w] if side=='B' else a[h-1-y%h][x]
        return [(x+MOVES[int(k)][1],y-MOVES[int(k)][0]) for k in s]
    for x in range(w):
        for y in range(h):
            ns=adj(x,y);assert len(set(ns))==2
            for u,v in ns:
                assert (v>=0 if side=='B' else u>=0),'off board'
                if v<h if side=='B' else u<w:assert (x,y) in adj(u,v)
                else:assert (u-x,v-y) in ((2,-1),(-2,1)),'bad straight interface'

def main():
    files=sorted(Path('w-integrator/tours').glob('LF1_*.json'));data=json.loads(files[0].read_text());gadgets={}
    pairs={}
    for key,kind,side in [('bottom','bottom','B'),('top','bottom','B'),('left','left','L'),('right','left','L')]:
        tpl=data[key];period=len(tpl[0].split()) if side=='B' else len(tpl)
        local_edges(tpl,side);x=count(tpl,kind);pairs[key]=pairing(tpl,side)
        gadgets[key]=dict(template=tpl,period=period,crossings=x,rate=str(Fraction(x,period)),matching=pairs[key])
    rows=[]
    for f in files:
        raw=f.read_bytes();d=json.loads(raw);n=d['n'];x,t=check(d['tour']);assert (x,t)==(d['crossings'],d['turns'])
        assert all(d[k]==data[k] for k in gadgets)
        assert Fraction(x)-Fraction(47,6)*n==11
        xb,xt,yl,yr=d['info']['phases']
        regs={
            'BL':region(pairs['bottom'],pairs['left'],xb,2*yl,1,1),
            'MID':region(pairs['left'],pairs['right'],2*yl,n-1+2*yr,1,-1),
            'TR':region(pairs['right'],pairs['top'],n-1+2*yr,xt+2*(n-1),-1,-1)}
        for r,want in [('BL',2),('MID',4),('TR',2)]:
            assert not regs[r]['finite_cycles'] and regs[r]['strands']==want
        rows.append(dict(file=str(f),sha256=hashlib.sha256(raw).hexdigest(),n=n,X=x,T=t,regions=regs))
        print(n,x,t,{r:(v['period'],v['strands'],v['cut_counts'],[c['displacement'] for c in v['directed_quotient_cycles']]) for r,v in regs.items()},flush=True)
    result=dict(date='2026-10-02',gadgets=gadgets,tours=rows)
    Path('w-verifier/lf1_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Gadgets:',gadgets)
if __name__=='__main__':main()
