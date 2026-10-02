"""Exact local strand matchings; no worker imports."""
import json
from pathlib import Path
from check import MOVES

SPANS={}

def pairing(tpl,side):
    cells=[r.split() for r in tpl];h=len(cells);w=len(cells[0]);P=w if side=='B' else 2*h
    def inside(p):x,y=p;return y<h if side=='B' else x<w
    def adj(p):
        x,y=p
        s=(cells[h-1-y][x%w] if side=='B' else cells[h-1-y%h][x]) if inside(p) else '26'
        return [(x+MOVES[int(k)][1],y-MOVES[int(k)][0]) for k in s]
    domain=((x,y) for x in range(-24,25) for y in range(h)) if side=='B' else ((x,y) for x in range(w) for y in range(-24,25))
    result={};covered=set();max_span=0
    for p in domain:
        for q in adj(p):
            c=q[0]+2*q[1]
            if inside(q) or not 0<=c<P:continue
            prev=q;cur=p;seen=set();labels=[c]
            while inside(cur):
                assert cur not in seen and len(seen)<200,'local cycle'
                seen.add(cur);x,y=cur;labels.append(x+2*y);covered.add((x%w,y) if side=='B' else (x,y%h))
                choices=adj(cur);assert prev in choices
                nxt=next(a for a in choices if a!=prev);prev,cur=cur,nxt
            result[c]=cur[0]+2*cur[1]
            labels.append(result[c]);max_span=max(max_span,max(labels)-min(labels))
    assert len(result)==P and len(covered)==w*h
    SPANS[side]=max_span
    return result

def mapping(p,c,shift=0,sign=1):
    local=sign*(c-shift);block,r=divmod(local,8)
    return shift+sign*(8*block+p[r])

def main():
    out=[]
    for family in ('H16a_VE','T18'):
        d=json.loads(Path(f'w-integrator/corners/{family}_res00.json').read_text())
        b=pairing(d['bottom'],'B');l=pairing(d['left'],'L');out.append(f'{family}: B={b}; L={l}; max path spans={dict(SPANS)}')
        for nr in (0,2,4,6):
            n=48+nr;X=(13-2*n)%8;Y=(-n//2)%4
            fs=[lambda c:mapping(b,c),lambda c:mapping(l,c,4),lambda c:mapping(l,c,n-1+2*Y,-1),lambda c:mapping(b,c,X+2*(n-1),-1)]
            for name,f,g in [('BL',fs[0],fs[1]),('MID',fs[1],fs[2]),('TR',fs[2],fs[3])]:
                found=[]
                for a in range(8):
                    for first,second in [(f,g),(g,f)]:
                        mid=[first(a+i) for i in range(4)]
                        end=[second(v) for v in mid]
                        if sorted(mid)==list(range(a+4,a+8)) and sorted(end)==list(range(a+8,a+12)):
                            perm=[v-a-8 for v in end];third=[perm[perm[perm[i]]] for i in range(4)]
                            assert third==list(range(4));found.append((a,perm))
                assert found,(family,nr,name)
                out.append(f'n mod 8={nr} {name}: {found}; cube is identity')
    Path('w-verifier/strand_results.txt').write_text('\n'.join(out)+'\n');print('\n'.join(out))
if __name__=='__main__':main()
