"""TT16 independent assembly, count, and periodic-state proof certificates."""
import json,hashlib
from pathlib import Path
from check import MOVES,check,orient
from reuse_audit import outside
from strand_audit import pairing,SPANS
from lf1_audit import region,mapping,local_edges
from periodic import count

def build(d,n):
    z=d['Z'];xb,xt,yl,yr=d['phases'];arrays={k:[r.split() for r in d[k]] for k in ['bottom','top','left','right']}
    def vec(k,x,y):
        a=arrays[k];h=len(a);w=len(a[0]);s=a[h-1-y%h][x%w]
        return [(MOVES[int(i)][1],-MOVES[int(i)][0]) for i in s]
    origin={'BL':(0,0),'BR':(n-z,0),'TL':(0,n-z),'TR':(n-z,n-z)};patch={}
    for key,ds in d['zones'].items():
        side,xy=key.split(':');x,y=map(int,xy.split(','));ox,oy=origin[side]
        assert 0<=x<z and 0<=y<z
        patch[ox+x,oy+y]=[tuple(v) for v in ds]
    assert len(patch)==4*z*z
    codes={(dj,-di):str(k) for k,(di,dj) in enumerate(MOVES)}
    grid=[]
    for r in range(n):
        y=n-1-r;row=[]
        for x in range(n):
            ds=[(2,-1),(-2,1)]
            if y<len(arrays['bottom']):ds=vec('bottom',x-xb,y)
            if n-1-y<len(arrays['top']):ds=[(-a,-b) for a,b in vec('top',xt-x,n-1-y)]
            if x<len(arrays['left'][0]):ds=vec('left',x,y-yl)
            if n-1-x<len(arrays['right'][0]):ds=[(-a,-b) for a,b in vec('right',n-1-x,yr-y)]
            if (x,y) in patch:ds=patch[x,y]
            row.append(''.join(sorted(codes[v] for v in ds)))
        grid.append(row)
    return grid

def main():
    out={'date':'2026-10-02','stored':[],'rebuilt':[],'regions':{},'strips':{},'corners':[]}
    for f in sorted(list(Path('w-integrator/tours').glob('TT16_n*.json'))+list(Path('w-integrator/tours/certificates').glob('TT16_n*.json'))):
        raw=f.read_bytes();d=json.loads(raw);x,t=check(d['tour']);assert (x,t)==(d['crossings'],d['turns']);assert t==8*d['n']-14
        out['stored'].append(dict(file=str(f),sha256=hashlib.sha256(raw).hexdigest(),n=d['n'],X=x,T=t))
    corners={}
    for f in sorted(Path('w-integrator/corners').glob('TT16_res*.json')):
        raw=f.read_bytes();d=json.loads(raw);corners[d['residue']]=d;out['corners'].append(dict(file=str(f),sha256=hashlib.sha256(raw).hexdigest()))
    d=corners[0];p={}
    for name in ['bottom','top','left','right']:
        side='B' if name in ['bottom','top'] else 'L';tpl=d[name];local_edges(tpl,side);p[name]=pairing(tpl,side)
        turns=sum(orient(MOVES[int(s[0])],(0,0),MOVES[int(s[1])])!=0 for row in tpl for s in row.split())
        out['strips'][name]=dict(turns=turns,crossings=count(tpl,'bottom' if side=='B' else 'left'),matching=p[name],max_path_span=SPANS[side])
    for n in (56,58,60,62):
        rr={}
        for nm,a,b,s,t,sa,sb in [('BL','bottom','left',0,0,1,1),('MID','left','right',0,n-1,1,-1),('TR','right','top',n-1,2*n-1,-1,-1)]:
            pr=region(p[a],p[b],s,t,sa,sb);assert not pr['finite_cycles'];spans=[]
            for cyc in pr['directed_quotient_cycles']:
                assert abs(cyc['displacement'])==8
                lift=cyc['states'][0][0];coords=[lift]
                for residue,color in cyc['states']:
                    assert lift%8==residue
                    lift=mapping(p[a] if color==0 else p[b],lift,s if color==0 else t,sa if color==0 else sb);coords.append(lift)
                spans.append(max(coords)-min(coords));cyc['lifted_coordinates']=coords
            pr['max_cycle_span']=max(spans);rr[nm]=pr
        out['regions'][n%8]=rr
    sig={}
    for n in list(range(48,136,2))+[312,314,316,318]:
        d=corners[n%8];g=build(d,n);x,t=check(g);m=outside(g)
        if n%8 not in sig:sig[n%8]=m
        else:assert m==sig[n%8],('matching changed',n)
        assert t==8*n-14,(n,t)
        assert x==9.5*n+{0:-2,2:-3,4:0,6:3}[n%8],(n,x)
        out['rebuilt'].append(dict(n=n,X=x,T=t,paths=len(m)))
        print(n,x,t,'same matching',flush=True)
    Path('w-verifier/tt16_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Stored',len(out['stored']),'rebuilt',len(out['rebuilt']),'all pass')
    print('Strips',out['strips'])
    print('Region spans',{r:{k:v['max_cycle_span'] for k,v in rs.items()} for r,rs in out['regions'].items()})
if __name__=='__main__':main()
