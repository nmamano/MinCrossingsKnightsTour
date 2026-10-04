# KT Structures 2026-10-04: pick the best closed tour per n among my files, write it as a cell order, record sha256.
import json, glob, hashlib
from pathlib import Path
from kt.core import validate, num_turns, MI, MJ
NS = [24, 28, 34, 38, 44, 48, 54, 58, 64, 68, 74, 78, 88, 98]
best = {}
for f in sorted(glob.glob('*.json') + glob.glob('fam/*.json') + glob.glob('mrg/*.json') + glob.glob('desk/*.json')):
    try: g = json.load(open(f))['grid']
    except Exception: continue
    n = len(g)
    if n not in NS or not validate(g): continue
    T = num_turns(g)
    if n not in best or T < best[n][0]: best[n] = (T, f, g)
entries = []
for n in NS:
    T, src, g = best[n]
    order = [(0, 0)]; prev = None
    while len(order) < n * n or prev is None:
        i, j = order[-1]
        nb = [(i + MI[int(c)], j + MJ[int(c)]) for c in g[i][j]]
        nxt = nb[0] if nb[0] != prev else nb[1]
        prev = (i, j)
        if nxt == (0, 0): break
        order.append(nxt)
    assert len(order) == n * n and len(set(order)) == n * n
    out = Path(f'tours/tour_n{n}.json')
    out.write_text(json.dumps(dict(n=n, T=T, T_minus_8n=T - 8 * n, source=src, date='2026-10-04',
        format='order: list of [row, col], 0-based, row 0 = top; consecutive cells and last->first are knight moves',
        order=[list(c) for c in order])))
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    entries.append(dict(n=n, file=f'gap/structures/tmin/{out}', T=T, T_minus_8n=T - 8 * n, sha256=h, source=src))
    print(n, T - 8 * n, src)
Path('single_tours.json').write_text(json.dumps(dict(date='2026-10-04', author='KT Structures',
    turn_definition='a cell is a turn unless its two tour moves are opposite vectors (straight); T = number of turn cells',
    format='each file: JSON with n, T, T_minus_8n, source, order = list of n*n [row, col] pairs (0-based), the closed tour in cyclic order',
    entries=entries), indent=1))
