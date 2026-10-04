#!/usr/bin/env python3
"""Bottom pieces with the 4 knight paths of one pair of lanes coloured, in the style of heel_original_fig.py
(Personal Site Agent, 2026-10-04). Tours from demo/build_data at n = 48:
- heel21: Parker's heel (gen_heel21), 21 turns per 8 columns; the paths stay inside their heel's box.
- t18: the T18 piece (gen_T18, lane rule), 18 turns per 8 columns; no walls, so the paths cross the boxes.
- t16_paths: the TT16 tour (gen_TT16, no lane rule), 16 turns per 8 columns; the 4 lines of one formation
  join lines of other formations (offsets +-7, +-9), so the formation splits.
Dashed boxes mark 8-column heels, placed 4 columns left of the pair's first line (c = x + 2y).
Output: writeup/turns/images/heel21.png, t18_band.png and t16_paths.png.
usage (from the project root): .venv/bin/python writeup/turns/figures/t18_fig.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import networkx as nx

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'demo'))
from build_data import gen_T18, gen_heel21, gen_TT16
from kt.core import MI, MJ

INK = '#22303a'
COLS = ['#e41a1c', '#2e8b57', '#1f4fe0', '#9b30d9']   # same colours as heel_original.png
n = 48

def draw(gen, p0, name, boxes):
    grid = gen(n)[0]
    g = {}
    for i, row in enumerate(grid):
        for j, code in enumerate(row):
            x, y = j, n - 1 - i
            g[x, y] = [(x + MJ[int(k)], y - MI[int(k)]) for k in code]
    X0, X1, Y0, Y1 = p0 - 20, p0 + 14, 0, 7
    LANE = range(p0, p0 + 4)      # the 4 lines c = x + 2y of one formation (one lane)
    BOXES = tuple(p0 + b for b in boxes)
    W = {(x, y) for x in range(X0, X1) for y in range(Y0, Y1)}
    G = nx.Graph(); G.add_nodes_from(W)
    for u in W:
        for v in g[u]:
            if v in W: G.add_edge(u, v)
    paths = []
    for c in nx.connected_components(G):
        top = sorted(p for p in c if p[1] == Y1 - 1)
        if len(top) == 2 and any(p[0] + 2 * p[1] in LANE for p in top):
            paths.append(c)
    # colour each path by the formation line it uses, so the colours follow the formation order
    entry = lambda c: next(p[0] + 2 * p[1] for p in c if p[1] == Y1 - 1 and p[0] + 2 * p[1] in LANE)
    paths.sort(key=entry)
    assert [entry(c) for c in paths] == list(LANE), [entry(c) for c in paths]

    fig, ax = plt.subplots(figsize=(9.6, 2.9))
    ax.set_xlim(X0 - .6, X1 - .4); ax.set_ylim(Y0 - .9, Y1 - .4); ax.set_aspect('equal'); ax.axis('off')
    for x in range(X0, X1):
        for y in range(Y0, Y1):
            if (x + y) % 2 == 0: ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color='#eef1f4', lw=0, zorder=0))
    # one outline around both boxes plus one shared divider, so no dashed edge is drawn twice; on top of the paths
    ax.add_patch(mp.Rectangle((BOXES[0] - .5, -.5), 8 * len(BOXES), 4, fill=False, ec=INK, lw=1.4, ls='--', zorder=6))
    for a in BOXES[1:]:
        ax.plot([a - .5, a - .5], [-.5, 3.5], color=INK, lw=1.4, ls='--', zorder=6)
    ax.plot([X0 - .5, X1 - .5], [-.5, -.5], color=INK, lw=2, zorder=1)          # bottom side of the board
    drawn = set()
    for u in W:
        for v in g[u]:
            e = tuple(sorted((u, v)))
            if e in drawn or not (u in W or v in W): continue
            drawn.add(e)
            col, lw, z = '#c3ccd4', .8, 2
            for k, c in enumerate(paths):
                if u in c and v in c: col, lw, z = COLS[k], 2.4, 3
            ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color=col, lw=lw, zorder=z, solid_capstyle='round')
    for k, c in enumerate(paths):
        ax.plot([p[0] for p in c], [p[1] for p in c], 'o', color=COLS[k], ms=3.5, zorder=4)
    out = ROOT / 'writeup' / 'turns' / 'images' / name
    fig.savefig(out, bbox_inches='tight', dpi=160, facecolor='white')
    print('wrote', out)

draw(gen_heel21, 26, 'heel21.png', (-4, 4))
draw(gen_T18, 24, 't18_band.png', (-4, 4))
draw(gen_TT16, 24, 't16_paths.png', (-12, -4, 4))

