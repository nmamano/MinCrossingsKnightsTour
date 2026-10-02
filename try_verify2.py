from kt.verify_strip import unroll_bottom
tpl16 = ['46 46 56 56 56 26 46 46','14 14 14 45 45 45 45 46','05 15 15 15 15 05 05 05','01 01 01 01 01 01 01 01']
adj, P, D, W = unroll_bottom(tpl16, 12)
for x in range(48, 56):
    t = (x, D-1); prev, cur = (x-2, D), t; path=[t]
    while True:
        nx = [v for v in adj[cur] if v != prev]
        if len(nx) != 1: path.append(('stuck', nx)); break
        prev, cur = cur, nx[0]; path.append(cur)
        if cur[1] >= D: break
    print(x, 'c=', x+2*(D-1), 'len', len(path), 'end', path[-2], 'c_end', path[-2][0]+2*path[-2][1] if isinstance(path[-2], tuple) else None, 'minx', min(p[0] for p in path if isinstance(p, tuple)))
