#!/usr/bin/env python3
"""PNG figures for the blog post (writeup/turns/images/). Uses the builder in tt16.py.
usage (from the project root): .venv/bin/python writeup/turns/figures/blog_figs.py"""
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tt16 import build, is_turn, draw_window, ROOT

IMG = Path(__file__).resolve().parent / 'blog_images'
IMG.mkdir(exist_ok=True)
DPI = 160


def save(fig, name):
    fig.savefig(IMG / f'{name}.png', bbox_inches='tight', dpi=DPI, facecolor='white')
    plt.close(fig)


def strips():
    """The four 4-wide strips; the 4x4 corners are counted twice."""
    n = 16
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-0.6, n - 0.4); ax.set_aspect('equal'); ax.axis('off')
    for x in range(n):
        for y in range(n):
            k = (x < 4) + (x >= n - 4) + (y < 4) + (y >= n - 4)
            fc = ['white', '#cfe6e3', '#e8a598'][k]
            ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, fc=fc, ec='#d5dbe0', lw=.6))
    ax.text(n / 2 - .5, 1.5, 'at least 2n turns', ha='center', va='center', fontsize=10)
    ax.text(n / 2 - .5, n - 2.5, 'at least 2n turns', ha='center', va='center', fontsize=10)
    ax.text(1.5, n / 2 - .5, 'at least 2n turns', ha='center', va='center', fontsize=10, rotation=90)
    ax.text(n - 2.5, n / 2 - .5, 'at least 2n turns', ha='center', va='center', fontsize=10, rotation=90)
    save(fig, 'strips')


def band(n, x0, x1, y0, y1, name, size, period_lines=None):
    g = build(n)
    fig, ax = plt.subplots(figsize=size)
    draw_window(ax, g, n, x0, x1, y0, y1, period_lines=period_lines)
    save(fig, name)


def count_figure():
    """Turns per column in the bottom band and in the top band; they add up to 4."""
    n = 48; g = build(n); x0, x1 = 8, 23
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 3.9), gridspec_kw={'hspace': 0.55})
    for ax, (ya, yb), label in ((axes[0], (n - 4, n - 1), 'top 4 rows'), (axes[1], (0, 3), 'bottom 4 rows')):
        draw_window(ax, g, n, x0, x1, ya, yb, shade_zone=False)
        ax.set_ylim(ya - 1.6, yb + 0.6)
        for x in range(x0, x1 + 1):
            k = sum(is_turn(g, (x, y)) for y in range(ya, yb + 1))
            ax.text(x, ya - 1.15, str(k), ha='center', va='center', fontsize=10, color='#c0392b', bbox=dict(fc='white', ec='none', pad=1.5), zorder=5)
        ax.text(x0 - 1.2, (ya + yb) / 2, label, ha='right', va='center', fontsize=9, color='#555')
    save(fig, 'count')


def grow():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.4), gridspec_kw={'width_ratios': [48, 56]})
    for ax, n in zip(axes, (48, 56)):
        g = build(n)
        draw_window(ax, g, n, 0, n - 1, 0, n - 1, dot=1.6)
        ax.set_title(f'n = {n}: {sum(is_turn(g, u) for u in g)} turns', fontsize=10)
    save(fig, 'grow')


def tour(n, name, size):
    g = build(n)
    fig, ax = plt.subplots(figsize=size)
    draw_window(ax, g, n, 0, n - 1, 0, n - 1, dot=2.2, shade_zone=False)
    save(fig, name)


if __name__ == '__main__':
    strips()
    band(48, 0, 25, 0, 8, 't16_band', (7.5, 3.2), period_lines=[8, 16, 24])
    band(48, 0, 9, 14, 29, 'left_band', (2.8, 4.6))
    count_figure()
    grow()
    tour(48, 'tour48', (6.5, 6.5))
    shutil.copy(IMG / 'tour48.png', IMG / 'cover.png')
    shutil.copy(ROOT / 'explain/turns_lemma.png', IMG / 'turns_lemma.png')
    print('wrote', sorted(p.name for p in IMG.iterdir()))
