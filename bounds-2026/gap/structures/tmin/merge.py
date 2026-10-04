# KT Structures, 2026-10-04. Greedy cycle merge: repeatedly apply the cheapest 2-opt swap of two edges in different
# cycles ((a,b),(c,d) -> (a,c),(b,d) or (a,d),(b,c), both knight moves), until one cycle. Turn cost is exact.
# usage: merge.py in.json out.json   (in: any record with "grid"; also accepts PER-extension via extend.dup_rows)
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from kt.core import validate, num_turns

MI = [-2, -1, 1, 2, 2, 1, -1, -2]
MJ = [1, 2, 2, 1, -1, -2, -2, -1]
CODE = {(MI[k], MJ[k]): k for k in range(8)}

def adj_from_grid(g):
    n = len(g)
    return {(i, j): [(i + MI[int(c)], j + MJ[int(c)]) for c in g[i][j]] for i in range(n) for j in range(n)}

def turn(v, nb):
    d = [(q[0] - v[0], q[1] - v[1]) for q in nb]
    return int(d[0][0] + d[1][0] != 0 or d[0][1] + d[1][1] != 0)

def cycles(adj):
    lab = {}; c = 0
    for s in adj:
        if s in lab: continue
        st = [s]; lab[s] = c
        while st:
            v = st.pop()
            for q in adj[v]:
                if q not in lab: lab[q] = c; st.append(q)
        c += 1
    return lab, c

def knight(u, v):
    return (v[0] - u[0], v[1] - u[1]) in CODE

def best_swap(adj, lab):
    best = None
    E = [(u, v) for u in adj for v in adj[u] if u < v]
    byv = {}
    for (u, v) in E:
        byv.setdefault(u, []).append((u, v)); byv.setdefault(v, []).append((u, v))
    for (a, b) in E:
        for x in (a, b):
            # partner edges near x: edges (c,d) with c a knight neighbour of a or b
            for (dx, dy) in CODE:
                c = (x[0] + dx, x[1] + dy)
                for (p, q) in byv.get(c, []):
                    if lab[p] == lab[a]: continue
                    for (c1, d1) in ((p, q), (q, p)):
                        for (u1, v1), (u2, v2) in (((a, c1), (b, d1)), ((a, d1), (b, c1))):
                            if not (knight(u1, v1) and knight(u2, v2)): continue
                            if v1 in adj[u1] or v2 in adj[u2]: continue
                            new = {a: [y for y in adj[a] if y != b], b: [y for y in adj[b] if y != a],
                                   c1: [y for y in adj[c1] if y != d1], d1: [y for y in adj[d1] if y != c1]}
                            for (s, t) in ((u1, v1), (u2, v2)):
                                new[s].append(t); new[t].append(s)
                            if any(len(new[w]) != 2 or new[w][0] == new[w][1] for w in new): continue
                            delta = sum(turn(w, new[w]) - turn(w, adj[w]) for w in new)
                            if best is None or delta < best[0]:
                                best = (delta, new)
    return best

def main():
    rec = json.loads(Path(sys.argv[1]).read_text()); g = rec['grid']; n = len(g)
    adj = adj_from_grid(g); lab, c = cycles(adj); T0 = num_turns(g); tot = 0
    while c > 1:
        b = best_swap(adj, lab)
        if b is None: print('stuck', c); return
        tot += b[0]; adj.update(b[1]); lab, c = cycles(adj)
    out = [['' for _ in range(n)] for _ in range(n)]
    for (i, j), nb in adj.items():
        ks = sorted(CODE[(q[0] - i, q[1] - j)] for q in nb); out[i][j] = '%d%d' % tuple(ks)
    assert validate(out)
    T = num_turns(out); assert T == T0 + tot
    Path(sys.argv[2]).write_text(json.dumps(dict(n=n, T=T, T_minus_8n=T - 8 * n, src=sys.argv[1], merge_cost=tot,
                                                 date='2026-10-04', grid=out)))
    print(f'{sys.argv[1]} n={n} T-8n: {T0 - 8 * n} -> tour {T - 8 * n} (merge cost {tot})')

if __name__ == '__main__':
    main()
