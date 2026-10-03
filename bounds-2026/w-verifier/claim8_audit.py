"""Independent LF4 assembly, count, and exterior graph transport audit."""
import json,hashlib,re
from pathlib import Path
from fractions import Fraction
from collections import Counter
from check import check
from tt16_audit import build
from claim7_transport import reduced,label,portname
from lf1_audit import local_edges
from periodic import count

def exterior(V,E,n,cuts,widths,transport):
    def block(u):return next((i for i,(a,w) in enumerate(zip(cuts,widths)) if a<=label(u)<a+w),None)
    def node(u):return ('v',)+transport(u)
    vertices={node(u) for u in V if block(u) is None};edges=Counter()
    for (u,v),mult in E.items():
        i,j=block(u),block(v)
        if i is not None and j is not None:assert i==j;continue
        if i is None and j is None:a,b=node(u),node(v)
        else:
            inner,outer,idx=(u,v,i) if i is not None else (v,u,j)
            side=int(label(outer)>=cuts[idx]+widths[idx])
            a=node(outer);b=('p',idx,side)+portname(inner,outer,cuts[idx]+side*widths[idx],n);vertices.add(b)
        edges[tuple(sorted((a,b),key=repr))]+=mult
    return vertices,edges

def main():
    text=Path('w-turnstheory/PROOFS.md').read_text().split('## 5.')[1]
    table={int(r):(int(n),int(x),Fraction(b.strip())) for r,n,x,b in re.findall(r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([\d/]+)\s*\|',text)}
    assert set(table)==set(range(0,48,2))
    results={'date':'2026-10-02','period':48,'slope':'343/48','cases':[],'costs':{}}
    first=None
    for f in sorted(Path('w-turnstheory/lf-corners').glob('LF4_res*.json')):
        raw=f.read_bytes();d=json.loads(raw);n=d['n0'];p=48;cuts=[36,n+36,2*n+36];widths=[12,8,16]
        if first is None:
            first=d
            for key in ['bottom','top','left','right']:
                tpl=d[key];side='B' if key in ('bottom','top') else 'L';local_edges(tpl,side)
                xx=count(tpl,'bottom' if side=='B' else 'left');period=len(tpl[0].split()) if side=='B' else len(tpl)
                results['costs'][key]=dict(period=period,crossings=xx,rate=str(Fraction(xx,period)))
            assert sum(Fraction(v['rate']) for v in results['costs'].values())==Fraction(343,48)
            assert len(set(d['left']))==len(set(d['right']))==1
        assert all(d[k]==first[k] for k in ['bottom','top','left','right','phases'])
        assert d['phases']==[1,1,0,0] and d['Z']==6 and len(d['zones'])==144
        g=build(d,n);h=build(d,n+p);x,t=check(g);x2,t2=check(h)
        assert x2-x==343
        n0,x0,b=table[n%48];assert n0==n and x0==x and Fraction(x)-Fraction(343,48)*n==b
        V,E=reduced(g);V2,E2=reduced(h)
        def transport(u):
            x,y=u;r=sum(label(u)>=a+w for a,w in zip(cuts,widths))
            if (x<6 or x>=n-6) and (y<6 or y>=n-6):return x+p*(x>=n-6),y+p*(y>=n-6)
            if y<4:return x+r*p,y
            if x<2:return x,y+r*p//2
            if x>=n-2:return x+p,y+(r-1)*p//2
            if y>=n-4:return x+(r-2)*p,y+p
            raise AssertionError(u)
        A=exterior(V,E,n,cuts,widths,transport)
        B=exterior(V2,E2,n+p,[a+i*p for i,a in enumerate(cuts)],[w+p for w in widths],lambda u:u)
        assert A==B,('exterior mismatch',n)
        results['cases'].append(dict(file=str(f),sha256=hashlib.sha256(raw).hexdigest(),n=n,X=x,T=t,b=str(b),larger=n+p,X_larger=x2,T_larger=t2,exterior_vertices=len(A[0]),exterior_edges=sum(A[1].values())))
        print(n,x,'->',n+p,x2,'b',str(b),'exterior exact',flush=True)
    assert len(results['cases'])==24
    Path('w-verifier/claim8_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print('PASS: all 48 independently assembled tours and all 24 exterior-graph transports.')
if __name__=='__main__':main()
