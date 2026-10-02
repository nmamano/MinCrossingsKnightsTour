#!/usr/bin/env python
"""Render a tour JSON (from assemble.py) to PNG: board cells, tour segments, crossings marked.
Usage: .venv/bin/python w-integrator/render.py tours/H16a_VerticalEdge_off0_n48.json out.png"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from kt.core import edges, crossing_list, num_turns

def seg_point(e, f):
    (a, b), (c, d) = e, f
    # rows i, cols j -> plot x = j, y = -i
    p = [(a[1], -a[0]), (b[1], -b[0])]; q = [(c[1], -c[0]), (d[1], -d[0])]
    x1, y1 = p[0]; x2, y2 = p[1]; x3, y3 = q[0]; x4, y4 = q[1]
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return x1 + t * (x2 - x1), y1 + t * (y2 - y1)

def render(g, out, title=''):
    n = len(g)
    E = list(edges(g))
    X = crossing_list(set(E))
    fig, ax = plt.subplots(figsize=(12, 12), dpi=110)
    for i in range(n):
        for j in range(n):
            if (i + j) % 2:
                ax.add_patch(plt.Rectangle((j - .5, -i - .5), 1, 1, color='#ececec', lw=0))
    turn = [(j, -i) for i in range(n) for j in range(n)
            if g[i][j] not in ('04', '40', '15', '51', '26', '62', '37', '73')]
    ax.add_collection(LineCollection([[(a[1], -a[0]), (b[1], -b[0])] for a, b in E],
                                     colors='#2a5d9f', linewidths=0.8))
    ax.scatter([p[0] for p in turn], [p[1] for p in turn], s=4, c='#2a5d9f', zorder=3)
    pts = [seg_point(e, f) for e, f in X]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=14, c='#d1352b', zorder=4, label=f'{len(X)} crossings')
    ax.set_xlim(-1, n); ax.set_ylim(-n, 1); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title or f'{n}x{n} closed knight\'s tour: {len(X)} crossings (red), {num_turns(g)} turns (dots)')
    fig.tight_layout(); fig.savefig(out); plt.close(fig)

if __name__ == '__main__':
    d = json.load(open(sys.argv[1]))
    render(d['tour'], sys.argv[2])
