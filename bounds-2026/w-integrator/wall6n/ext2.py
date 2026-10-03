#!/usr/bin/env python3
"""Can a periodic wall witness be extended by PERFECT exterior regions? (KT Edge Searcher, 2026-10-03)
Cylinder: cells (x, y), y mod H = 4L, identified with (x + 2L, y + H) (the witness period (2,4) repeated L times).
Window: -D <= x - floor((1+y)/2) < 4 + D. Edges at modeled cells (0 <= x - floor((1+y)/2) < 4) are fixed to the
witness. Every other window cell has degree exactly 2, except cells within 2 of the window edge (degree <= 2).
Every quarter of every inner square that is not complete (complete = determined by the witness) must be covered
exactly once. CP-SAT feasibility (2 workers). Cycles are not forbidden."""
import sys
from collections import defaultdict
sys.path.insert(0, '/home/nil/nil/knight-formation-research/gap/searcher')
from check_identity import tile_quarters
from ortools.sat.python import cp_model

L = int(sys.argv[1]) if len(sys.argv) > 1 else 2
D = int(sys.argv[2]) if len(sys.argv) > 2 else 8
LD = sys.argv[3] if len(sys.argv) > 3 else 'any'
RD = sys.argv[4] if len(sys.argv) > 4 else 'any'
DIRS={'any':None,'21':{(2,1),(-2,-1)},'12':{(1,2),(-1,-2)},'2m1':{(2,-1),(-2,1)},'1m2':{(1,-2),(-1,2)}}
H = 4 * L
W = [((-1,0),(1,1)), ((1,0),(3,1)), ((1,0),(2,2)), ((2,0),(3,2)), ((3,0),(5,1)), ((3,0),(4,2)),
     ((0,1),(2,2)), ((2,1),(4,2)), ((2,1),(3,3)), ((4,1),(6,2)), ((4,1),(5,3)),
     ((1,2),(3,3)), ((1,2),(2,4)), ((3,2),(5,3)),
     ((0,3),(2,4)), ((2,3),(4,4)), ((2,3),(3,5)), ((4,3),(6,4)), ((4,3),(5,5))]
sv = lambda x, y: x - (1 + y) // 2           # band coordinate of a cell
def canon(c):
    x, y = c; k = y // H
    return (x - 2 * L * k, y - H * k)
def csq(X, Y):                                # canonical square
    k = Y // H; return (X - 2 * L * k, Y - H * k)
modeled = lambda c: 0 <= sv(*c) < 4
inwin = lambda c: -D <= sv(*c) < 4 + D
soft = lambda c: sv(*c) < -D + 2 or sv(*c) >= 4 + D - 2
cells = [(x, y) for y in range(H) for x in range(-D - 2 + (1 + y) // 2 - 2, 4 + D + (1 + y) // 2 + 2) if inwin((x, y))]
fixed = set()
for k in range(L):
    for a, b in W:
        p = canon((a[0] + 2 * k, a[1] + 4 * k)); q = canon((b[0] + 2 * k, b[1] + 4 * k))
        fixed.add(tuple(sorted([p, q])))
MV = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
edges = {}   # canonical edge -> unwrapped representative (p, q) with p canonical
for c in cells:
    for dx, dy in MV:
        q = (c[0] + dx, c[1] + dy)
        if not inwin(canon(q)) and not inwin(q): continue
        if not inwin(q): continue
        e = tuple(sorted([c, canon(q)]))
        if modeled(c) or modeled(q): continue
        edges.setdefault(e, (c, q))
m = cp_model.CpModel()
var = {e: m.NewBoolVar(str(e)) for e in edges}
for e,(p,q) in edges.items():
    d=(q[0]-p[0],q[1]-p[1]); K=int(__import__('os').environ.get('K','0')); side = 'L' if sv(*p) < -K and sv(*q) < -K else ('R' if sv(*p) >= 4+K and sv(*q) >= 4+K else 'M')
    allow = DIRS[LD] if side=='L' else (DIRS[RD] if side=='R' else None)
    if allow is not None and d not in allow: m.Add(var[e]==0)
deg = defaultdict(list)
for e, (p, q) in edges.items():
    deg[canon(p)].append(var[e]); deg[canon(q)].append(var[e])
fdeg = defaultdict(int)
for e in fixed: fdeg[e[0]] += 1; fdeg[e[1]] += 1
for c in cells:
    if modeled(c): continue
    tot = sum(deg[c]) + fdeg[c]
    if soft(c): m.Add(tot <= 2)
    else: m.Add(tot == 2)
# quarter cover
cov = defaultdict(list); fcov = defaultdict(int)
for e, (p, q) in edges.items():
    for (X, Y, t) in tile_quarters(p, q): cov[(csq(X, Y), t)].append(var[e])
for e in fixed:
    p, q = e
    if q[1] < p[1]: p, q = q, p
    # unwrap: choose representative with q close to p
    best = None
    for k in (-1, 0, 1):
        qq = (q[0] + 2 * L * k, q[1] + H * k)
        if abs(qq[0] - p[0]) + abs(qq[1] - p[1]) == 3 and abs(qq[0] - p[0]) in (1, 2): best = qq
    for (X, Y, t) in tile_quarters(p, best): fcov[(csq(X, Y), t)] += 1
def complete(X, Y):
    for x1 in range(X - 2, X + 4):
        for y1 in range(Y - 2, Y + 2):
            for dx, dy in [(2,1),(-2,1),(1,2),(-1,2)]:
                if any((X, Y) == (a, b) for (a, b, t) in tile_quarters((x1, y1), (x1 + dx, y1 + dy))):
                    if not modeled((x1, y1)) and not modeled((x1 + dx, y1 + dy)): return False
    return True
nreq = 0
for Y in range(H):
    for X in range(-D - 4 + (1 + Y) // 2, 4 + D + (1 + Y) // 2 + 4):
        s = sv(X, Y)
        if s < -D + 3 or s >= 4 + D - 3: continue
        if complete(X, Y): continue
        for t in range(4):
            m.Add(sum(cov[((X, Y), t)]) + fcov[((X, Y), t)] == 1); nreq += 1
print(f"L={L} D={D}: {len(cells)} cells, {len(edges)} free edges, {len(fixed)} fixed, {nreq} quarter constraints")
sol = cp_model.CpSolver(); sol.parameters.num_workers = 2; sol.parameters.max_time_in_seconds = 600
r = sol.Solve(m)
print("status:", sol.StatusName(r))
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    ch = sorted(e for e in edges if sol.Value(var[e]))
    left = [e for e in ch if sv(*e[0]) < 0 and sv(*e[1]) < 0][:12]; right = [e for e in ch if sv(*e[0]) >= 4][:12]
    from collections import Counter
    def dc(es): return Counter((abs(q[0]-p[0]),(q[0]-p[0])*(q[1]-p[1])>0) for p,q in (edges[e] for e in es))
    print("left dirs", dc([e for e in ch if sv(*e[0]) < 0 and sv(*e[1]) < 0])); print("right dirs", dc([e for e in ch if sv(*e[0]) >= 4 and sv(*e[1]) >= 4]))
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) and __import__('os').environ.get('SHOW'):
    nb = defaultdict(list)
    for e in ch:
        p, q = edges[e]
        nb[canon(p)].append((q[0]-p[0], q[1]-p[1])); nb[canon(q)].append((p[0]-q[0], p[1]-q[1]))
    for e in fixed:
        p, q = e
        for k in (-1,0,1):
            qq=(q[0]+2*L*k,q[1]+H*k)
            if abs(qq[0]-p[0])+abs(qq[1]-p[1])==3 and abs(qq[0]-p[0]) in (1,2):
                nb[p].append((qq[0]-p[0],qq[1]-p[1])); 
                pp=(p[0]-2*L*k,p[1]-H*k); nb[q].append((pp[0]-q[0],pp[1]-q[1]))
    code={(2,1):'a',(-2,-1):'A',(1,2):'b',(-1,-2):'B',(2,-1):'c',(-2,1):'C',(1,-2):'d',(-1,2):'D'}
    for y in range(H-1,-1,-1):
        row=''
        for s_ in range(-D, 4+D):
            x = s_ + (1+y)//2
            c=(x,y); ds=nb.get(canon(c),[])
            t=''.join(sorted(code[d] for d in ds))
            row += (t.ljust(2,'.') if not modeled(c) else ('|'+t)[:2])+' '
        print(f"{y:2d} {row}")
