#!/usr/bin/env python3
"""The full 48 x 48 tour (gen_TT16, 8n - 14 = 370 turns) in the style of the post's figures, turns in red
(Personal Site Agent, 2026-10-04). Output: writeup/turns/images/tour48_full.png.
usage (from the project root): .venv/bin/python writeup/turns/figures/tour48_fig.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.collections import LineCollection

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'demo'))
from build_data import gen_TT16
from kt.core import MI, MJ
from tt16 import is_turn

INK, TURN = '#22303a', '#c0392b'
n = 48
grid = gen_TT16(n)[0]
g = {}
for i, row in enumerate(grid):
    for j, code in enumerate(row):
        x, y = j, n - 1 - i
        g[x, y] = [(x + MJ[int(k)], y - MI[int(k)]) for k in code]
turns = [p for p in g if is_turn(g, p)]
assert len(turns) == 8 * n - 14, len(turns)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-.7, n - .3); ax.set_ylim(-.7, n - .3); ax.set_aspect('equal'); ax.axis('off')
for x in range(n):
    for y in range(n):
        if (x + y) % 2 == 0: ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color='#eef1f4', lw=0, zorder=0))
segs, seen = [], set()
for u, vs in g.items():
    for v in vs:
        e = tuple(sorted((u, v)))
        if e not in seen:
            seen.add(e); segs.append(e)
ax.add_collection(LineCollection(segs, colors='#7d8a96', linewidths=0.9, zorder=2, capstyle='round'))
ax.plot([p[0] for p in turns], [p[1] for p in turns], 'o', color=TURN, ms=3.2, zorder=3)
ax.add_patch(mp.Rectangle((-.5, -.5), n, n, fill=False, ec=INK, lw=2.2, zorder=4))
out = ROOT / 'writeup' / 'turns' / 'images' / 'tour48_full.png'
fig.savefig(out, bbox_inches='tight', dpi=220, facecolor='white')
print('wrote', out, len(turns), 'turns')
