#!/usr/bin/env python3
"""Figure of the paper's optimised heel (21 turns per 8 columns) for the turns post (KT Integrator, 2026-10-03).
The heel is the reconstruction w-integrator/gadgets/heel21.json (audited in Claim 22), placed by Algorithm 1
(demo/build_data.gen_heel21). Drawn with tt16.draw_window, the style of the post's other figures.
usage (from the project root): .venv/bin/python writeup/turns/figures/heel21_fig.py"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / 'demo'))
from tt16 import draw_window, is_turn
from build_data import gen_heel21
from kt.core import MI, MJ

n = 48
grid = gen_heel21(n)[0]
g = {}
for i, row in enumerate(grid):
    for j, code in enumerate(row):
        x, y = j, n - 1 - i
        g[x, y] = tuple((x + MJ[int(k)], y - MI[int(k)]) for k in code)
# Heels sit at columns 14 + 8k (the same place as heel_original_fig.py's HX = 14): a heel box at
# offset 6 mod 8 is crossed by only 2 moves inside rows 0-3, every other offset by 6-8.
HEELS = (6, 14, 22, 30)
x0, x1, y0, y1 = 6, 37, 0, 6
per = [sum(is_turn(g, (x, y)) for x in range(a, a + 8) for y in range(0, 4)) for a in HEELS]
assert per == [21, 21, 21, 21], per
fig, ax = plt.subplots(figsize=(9.5, 2.6))
draw_window(ax, g, n, x0, x1, y0, y1, period_lines=None, shade_zone=False)
import matplotlib.patches as mp
for a in HEELS:
    ax.add_patch(mp.Rectangle((a - .5, -.5), 8, 4, fill=False, ec='#2c7fb8', lw=1.2, ls='--', zorder=4))
out = ROOT / 'writeup' / 'turns' / 'images' / 'heel21.png'
fig.savefig(out, bbox_inches='tight', dpi=160, facecolor='white')
print('wrote', out, 'turns per 8 columns in the bottom 4 rows:', per)
