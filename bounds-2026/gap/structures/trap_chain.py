# KT Structures, 2026-10-03. SHEET 12.2: trap components across a shift boundary (lower lines d <= 0 shift s, d > 0 shift s + delta).
P=lambda c: c-3 if c%2==0 else c+3
def run(delta,s=100,N=80,b=0):
    up=lambda d: d+s if d<=b else d+s+delta
    inv={up(d):d for d in range(-N,N+1)}
    open_=0; seen=set(); detail=[]
    for d0 in range(-N+20,N-19):
        if d0 in seen: continue
        d=d0; comp=[]; closed=False
        for _ in range(4*N):
            comp+= [d, P(d)]; seen.update((d,P(d)))
            u=P(up(P(d)))
            if u not in inv: break
            d=inv[u]
            if d==d0: closed=True; break
        if not closed: open_+=1; detail.append(sorted(set(comp))[:8])
    return open_, detail
for delta in (0,2,4,6,8,1,3,5):
    o,dt=run(delta); print('delta',delta,'open components (returns approx)',o, dt[:4])
