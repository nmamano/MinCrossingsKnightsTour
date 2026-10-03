"""Diagnostic scan of SHEET labels and actual same-side interior chords.
Collar convention: x=0,1,2, all incident edges in a +/-3 row window.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'w-verifier'))
from check import check,MOVES
from claim9_tiles import quarters
templates={d:quarters(((0,0),d)) for d in [(1,2),(2,1),(1,-2),(2,-1)]}
def edge(a,b):return tuple(sorted((a,b)))
def run(file):
    data=json.loads(Path(file).read_text());grid=data['tour'];n=len(grid);X,turns=check(grid)
    E={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
    adj=defaultdict(set)
    for a,b in E:adj[a].add(b);adj[b].add(a)
    transforms=[lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])]
    cheap=[];labels=[]
    for si,T in enumerate(transforms):
        local={edge(T(a),T(b)) for a,b in E};la=defaultdict(set);own=defaultdict(list)
        for a,b in local:
            la[a].add(b);la[b].add(a)
            for x,y,k in templates[b[0]-a[0],b[1]-a[1]]:own[x+a[0],y+a[1],k].append((a,b))
        if si==0:BQ=sum(len(own[x,y,k])!=1 for x in range(3,n-4) for y in range(3,n-4) for k in range(4))
        pure={}
        for y in range(n):
            for sign in (1,-1):
                def expected(x,y):
                    if x==0:return {(2,y+sign),(1,y+2*sign)}
                    if x==1:return {(3,y+sign),(0,y-2*sign)}
                    return {(x+2,y+sign),(x-2,y-sign)}
                if all(la[x,y]==expected(x,y) for x in range(3)):pure[y]=sign
        slots={y:pure[y] for y in range(3,n-3) if y in pure and all(pure.get(j)==pure[y] for j in range(y-3,y+4))}
        cheap.append(slots)
        def state(t):
            x,y,h=t;qs={'TL':(2,3),'BR':(0,1),'RT':(1,2),'LB':(3,0)}[h]
            if not (3<=x<n-4 and 3<=y<n-4):return 'OUT'
            if not all(len(own[x,y,k])==1 for k in range(4)):return 'BAD'
            if own[x,y,qs[0]]!=own[x,y,qs[1]]:return 'OTHER'
            a,b=own[x,y,qs[0]][0]
            return 'H' if b[0]-a[0]==2 else 'V'
        def nxt(t):
            x,y,h=t
            return {'TL':(x,y+1,'BR'),'BR':(x+1,y,'TL'),'LB':(x,y-1,'RT'),'RT':(x+1,y,'LB')}[h]
        for y,sign in slots.items():
            start=(3,y,'TL' if sign==1 else 'LB');cur=start;prev_good=False;bad=False
            for _ in range(4*n):
                st=state(cur)
                if st=='OUT':typ='EXIT';break
                if st=='OTHER':typ='UNDEFINED' if bad or not prev_good else 'W';break
                if st=='V':typ='D' if bad else 'UNEXPECTED_V';break
                if st=='BAD':bad=True
                else:bad=False;prev_good=True
                cur=nxt(cur)
            labels.append(dict(side=si,row=y,kind=typ,stop=cur))
    inside=lambda v:all(3<=z<=n-4 for z in v)
    ports={}
    for a,b in E:
        if inside(a)==inside(b):continue
        outer,inner=(b,a) if inside(a) else (a,b)
        sides=[i for i,T in enumerate(transforms) if T(outer)[0]<3]
        si=sides[0] if len(sides)==1 else None
        row=transforms[si](outer)[1] if si is not None else None
        ports[edge(a,b)]=dict(side=si,row=row,cheap=si is not None and row in cheap[si],outer=outer,inner=inner)
    chords=[];done=set()
    for e,info in ports.items():
        if e in done:continue
        prev,cur=info['outer'],info['inner'];path=[prev,cur]
        while inside(cur):
            nxt=next(v for v in adj[cur] if v!=prev);prev,cur=cur,nxt;path.append(cur)
        f=edge(prev,cur);assert f in ports;done.update((e,f));end=ports[f]
        if info['cheap'] and end['cheap'] and info['side']==end['side']:
            chords.append(dict(side=info['side'],rows=[info['row'],end['row']],ports=[e,f],path=path))
    kinds=Counter(z['kind'] for z in labels)
    result=dict(file=file,n=n,cheap_slots=sum(map(len,cheap)),all_slots=4*(n-6),label_counts=dict(kinds),
                W=kinds['W'],SSR=len(chords),W_minus_2SSR=kinds['W']-2*len(chords),labels=labels,SSR_chords=chords,
                X=X,E=X-4*n+2,BQ=BQ,EXC=4*(n-6)-sum(map(len,cheap)),
                revised_B_left=BQ+2*len(chords)+2*(4*(n-6)-sum(map(len,cheap))))
    return result
if __name__=='__main__':
    results=[]
    for file in sys.argv[1:]:
        r=run(file);results.append(r);print({k:v for k,v in r.items() if k not in ('labels','SSR_chords')},flush=True)
    (ROOT/'gap/verifier/claim36_scan.json').write_text(json.dumps(results,indent=2))
