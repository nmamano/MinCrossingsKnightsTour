import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

INK, MUTED, ACC, ACC2, BAD = '#22303a', '#9aa7b0', '#0b7a75', '#c0392b', '#b0b8bf'
ROWS = 7
def board(ax, title, sub, ncols=6, shade=None):
    ax.set_xlim(-0.6, ncols - 0.4); ax.set_ylim(-2.9, ROWS - 0.4); ax.set_aspect('equal'); ax.axis('off')
    for x in range(ncols):
        for y in range(ROWS):
            fc = '#eef1f3' if (x + y) % 2 else '#ffffff'
            if shade and x in shade: fc = shade[x]
            ax.add_patch(Rectangle((x - .5, y - .5), 1, 1, fc=fc, ec='#d5dbe0', lw=.8))
    for x in range(ncols):
        ax.text(x, -0.75, f'col {x}', ha='center', va='center', fontsize=9, color=MUTED)
    ax.plot([-.5, -.5], [-.5, ROWS - .5], color=INK, lw=3)
    ax.set_title(title, fontsize=14, color=INK, loc='left', fontweight='bold', pad=8)
    ax.text(-0.5, -1.15, sub, fontsize=11.5, color=INK, va='top', ha='left')
def arrow(ax, a, b, col, lw=2.2, ls='-'):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=13, color=col, lw=lw, ls=ls, shrinkA=6, shrinkB=6))
def cell(ax, p, col):
    ax.plot(*p, 'o', ms=10, color=col, zorder=5)

fig, axs2 = plt.subplots(2, 2, figsize=(12.5, 14))
axs = axs2.flatten()
# A: column 0
ax = axs[0]; board(ax, '1. Column 0: every cell turns', 'An edge cell can only move right.\nTwo right-going moves are never opposite,\nso the path bends at every one of the n cells.', shade={0: '#d7ecea'})
c = (0, 3); cell(ax, c, ACC)
for d in [(1, 2), (2, 1), (2, -1), (1, -2)]:
    arrow(ax, c, (c[0] + d[0], c[1] + d[1]), ACC)
# B: column 1 and 2
ax = axs[1]; board(ax, '2. Columns 1-2: two outward moves = turn', 'Outward = a move to column 0 or column 3.\nFrom col 1 that is 1 left or 2 right; from col 2,\n2 left or 1 right. Opposite moves would need\nthe same length both ways, so: always a turn.', shade={1: '#f3e6d3', 2: '#f3e6d3'})
c = (1, 4); cell(ax, c, '#b5651d')
for d in [(-1, 2), (-1, -2), (2, 1), (2, -1)]:
    arrow(ax, c, (c[0] + d[0], c[1] + d[1]), '#b5651d')
c2 = (2, 1); cell(ax, c2, '#b5651d')
for d in [(-2, 1), (-2, -1), (1, 2)]:
    arrow(ax, c2, (c2[0] + d[0], c2[1] + d[1]), '#b5651d')
# C: column 3
ax = axs[2]; board(ax, '3. Column 3: no move back means a turn', 'If a column-3 cell has no move back into\ncolumns 1-2, both moves go right (to columns\n4-5), so they are never opposite.', shade={3: '#e3e0f0'})
c = (3, 3); cell(ax, c, '#5b4b9a')
for d in [(1, 2), (2, -1)]:
    arrow(ax, c, (c[0] + d[0], c[1] + d[1]), '#5b4b9a')
for d in [(-1, 2), (-2, -1)]:
    arrow(ax, c, (c[0] + d[0], c[1] + d[1]), BAD, lw=1.4, ls=(0, (3, 3)))
ax.text(3, 6.2, 'dashed = the "back" moves it does not use', ha='center', fontsize=8.5, color=MUTED)
# D: the count
ax = axs[3]; ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_title('4. Add up (B cancels)', fontsize=14, color=INK, loc='left', fontweight='bold', pad=8)
lines = [
    ('Column 0', 'n turns', ACC),
    ('Columns 1-2', 'at least B turns', '#b5651d'),
    ('Column 3', 'at least n - B turns', '#5b4b9a'),
]
y = 8.6
ax.text(0, 9.6, 'B = number of tour moves between\ncolumn 3 and columns 1-2.', fontsize=10, color=INK, va='top')
y = 7.4
for name, val, col in lines:
    ax.text(0.2, y, name, fontsize=13, color=col, fontweight='bold', va='center')
    ax.text(5.3, y, val, fontsize=13, color=INK, va='center')
    y -= 0.95
ax.plot([0.2, 9.6], [y + 0.45, y + 0.45], color=INK, lw=1)
ax.text(0.2, y - 0.1, 'Four columns', fontsize=12, color=INK, fontweight='bold', va='center')
ax.text(5.3, y - 0.1, 'at least 2n turns', fontsize=12, color=INK, fontweight='bold', va='center')
ax.text(0, y - 1.25, 'Why "at least B" in columns 1-2:\ncolumn 0 sends 2n moves in, column 3\nsends B more: 2n + B outward ends on\n2n cells, each cell holds at most 2,\nso at least B cells hold two -> B turns.', fontsize=11.5, color=INK, va='top')
ax.text(0, y - 3.75, 'All four sides: 8n, minus at most 64\nfor the 4x4 corners counted twice.\nOur tours have 8n - 14 turns.', fontsize=12.5, color=ACC, fontweight='bold', va='top')
fig.suptitle('Why every closed knight\'s tour on an n x n board has at least 8n - 64 turns', fontsize=16, color=INK, x=0.02, ha='left', fontweight='bold')
fig.text(0.02, 0.935, 'A cell is a turn when its two moves are not opposite.\nLook only at the 4 columns next to one side.', fontsize=11, color=MUTED)
plt.tight_layout(rect=(0, 0, 1, 0.93))
plt.savefig('/home/nil/nil/knight-formation-research/explain/turns_lemma.png', dpi=170, facecolor='white')
