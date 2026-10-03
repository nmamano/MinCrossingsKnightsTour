"""Flux route 'edge + outer V arm' for the fold design (KT Structures, 2026-10-02). Spec in ROUTE_ARM.md.
In each quadrant frame r (BL frame coordinates, mapped to the board with paste.Rot):
  edge segment : cells x < We, 0 <= y < h/2 + We     (left board edge from the corner window to the arm start)
  arm corridor : cells within Chebyshev distance Wa of the traced field line that starts at the left-edge
                 cell (0, h/2) and leaves along its line edge (direction (2,1)), until it is within `stop` of the centre.
Returns the route cells (all 4 frames) and the traced arm paths (BL-frame lists, for period ties)."""
from paste import Rot

def trace_arm(n, E, r, stop=6):
    h = n // 2
    nb = {}
    for a, b in E:
        nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    inv = lambda p: Rot(p, n, (4 - r) % 4)
    start = Rot((0, h // 2), n, r)
    line = [q for q in nb[start] if inv(q) == (2, h // 2 + 1)]
    assert line, ('arm start is not a (2,1) line end', inv(start), [inv(q) for q in nb[start]])
    path, prev, cur = [start], start, line[0]
    while True:
        path.append(cur)
        p = inv(cur)
        if max(abs(p[0] - h), abs(p[1] - h)) <= stop or len(path) > 2 * n:
            break
        nxt = [q for q in nb[cur] if q != prev]
        prev, cur = cur, nxt[0]
    return [inv(p) for p in path]

def arm_route(n, E, We=4, Wa=2, stop=6):
    h = n // 2
    cells, paths = set(), {}
    for r in range(4):
        for x in range(We):
            for y in range(0, h // 2 + We):
                cells.add(Rot((x, y), n, r))
        path = trace_arm(n, E, r, stop)
        paths[r] = path
        for (x, y) in path:
            for dx in range(-Wa, Wa + 1):
                for dy in range(-Wa, Wa + 1):
                    if 0 <= x + dx < n and 0 <= y + dy < n:
                        cells.add(Rot((x + dx, y + dy), n, r))
    return cells, paths

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../w-integrator')
    import fold_jog
    n = int(sys.argv[1])
    E, deg = fold_jog.build_jog(n)
    cells, paths = arm_route(n, E)
    p = paths[0]
    steps = [(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:])]
    from collections import Counter
    print('n', n, 'route cells', len(cells), 'arm length (moves)', len(p) - 1, 'steps', Counter(steps).most_common(5), 'end', p[-1])
