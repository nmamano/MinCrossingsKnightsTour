#!/usr/bin/env python3
"""The three insertion blocks of the TT16 proof on the n = 72 tour (KT Integrator, 2026-10-03).
A block = the cells with line label c = x + 2y in [a, a + 8): 8 consecutive interior lines plus the side pieces
at both ends. Cut positions are those of check_upper_proofs.py (w-turnstheory/PROOFS.md section 2, TT16):
a = 35 (bottom-left), the first multiple of 8 >= n + 32 (left-right), a = 2n + 32 (right-top).
usage (from the project root): .venv/bin/python writeup/turns/figures/blocks_fig.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from tt16 import build, is_turn

INK = '#22303a'
n = 72
g = build(n)
blocks = [('bottom-left block', 35, '#9fd3c7'), ('left-right block', -(-(n + 32) // 8) * 8, '#f6c28b'),
          ('right-top block', 2 * n + 32, '#c3b1e1')]
fig, ax = plt.subplots(figsize=(7.2, 7.2))
ax.set_xlim(-1, n); ax.set_ylim(-1, n); ax.set_aspect('equal'); ax.axis('off')
inblock = {}
for name, a, col in blocks:
    for x in range(n):
        for y in range(n):
            if a <= x + 2 * y < a + 8:
                inblock[x, y] = col
                ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color=col, lw=0, zorder=1))
ax.add_patch(mp.Rectangle((-.5, -.5), n, n, fill=False, ec=INK, lw=1, zorder=1))
drawn = set()
for u, vs in g.items():
    for v in vs:
        e = tuple(sorted((u, v)))
        if e in drawn: continue
        drawn.add(e)
        dark = e[0] in inblock and e[1] in inblock
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color=INK if dark else '#b4bec7', lw=0.9 if dark else 0.5,
                zorder=3 if dark else 2, solid_capstyle='round')
tx = [u for u in g if is_turn(g, u)]
ax.plot([u[0] for u in tx], [u[1] for u in tx], 'o', color='#c0392b', ms=1.8, zorder=4)
# labels next to the middle of each strip, in a white box
for name, a, col in blocks:
    cells = [(x, y) for x in range(n) for y in range(n) if a <= x + 2 * y < a + 8]
    mx = sum(c[0] for c in cells) / len(cells); my = sum(c[1] for c in cells) / len(cells)
    ax.text(mx, my + 3, name, ha='center', va='bottom', fontsize=9, color=INK, zorder=6,
            bbox=dict(fc='white', ec=col, lw=1.5, boxstyle='round,pad=0.3'))
out = HERE.parent / 'images' / 'blocks.png'
fig.savefig(out, bbox_inches='tight', dpi=160, facecolor='white')
print('wrote', out, [(nm, a) for nm, a, _ in blocks])
