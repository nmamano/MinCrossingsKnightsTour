#!/usr/bin/env python3
"""Paper heel (12n) vs the new heel H16a (9n): bottom band of real tours, crossings in red.
usage (from the project root): .venv/bin/python writeup/crossings/figures/heel_fig.py"""
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from kt.core import edges, crossing_list, validate
from kt.gentour import gen_tour
OUT = Path(__file__).resolve().parent
RED, INK, GREY, GRID = '#c0392b', '#22303a', '#9aa5b1', '#eef1f4'


def xy(n, e):
    return tuple((j, n - 1 - i) for i, j in e)


def panel(ax, t, title, x0=6, x1=29, y1=7):
    n = len(t); validate(t)
    E = edges(t); C = crossing_list(E)
    ax.set_xlim(x0 - .6, x1 + .6); ax.set_ylim(-.6, y1 + .6); ax.set_aspect('equal'); ax.axis('off')
    for x in range(x0, x1 + 1):
        for y in range(0, y1 + 1):
            if (x + y) % 2 == 0:
                ax.add_patch(plt.Rectangle((x - .5, y - .5), 1, 1, color=GRID, lw=0, zorder=0))
    for e in E:
        a, b = xy(n, e)
        if any(x0 - 2 <= p[0] <= x1 + 2 and p[1] <= y1 + 2 for p in (a, b)):
            ax.plot([a[0], b[0]], [a[1], b[1]], color='#5a6872', lw=.8, zorder=2)
    cnt = 0
    for e, f in C:
        (a, b), (c, d) = xy(n, e), xy(n, f)
        dd = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
        s = ((a[0] - c[0]) * (c[1] - d[1]) - (a[1] - c[1]) * (c[0] - d[0])) / dd
        p = (a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1]))
        if x0 - .5 <= p[0] <= x1 + .5 and p[1] <= y1 + .5:
            ax.plot(*p, 'o', color=RED, ms=3.5, zorder=3)
    ax.plot([x0 - .6, x1 + .6], [-.5, -.5], color=INK, lw=2)
    ax.set_title(title, fontsize=9, loc='left')


fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.4))
panel(axes[0], gen_tour(48, 48), "the paper's heel: 28 crossings per 8 columns")
d = json.loads((ROOT / 'w-integrator/tours/H16a_VerticalEdge_off0_n64.json').read_text())
panel(axes[1], d['tour'], 'the new heel: 16 crossings per 8 columns')
fig.savefig(OUT / 'heels.png', bbox_inches='tight', dpi=160, facecolor='white')
print('wrote heels.png')
