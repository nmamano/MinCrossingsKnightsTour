"""Port of Algorithm 1 (genTour in board.js) with pluggable heel and block substitution.
heel: 8-wide x 4-tall template used for Sequence1 everywhere (default: paper's 28-crossing heel).
block: optional (template, width) placed greedily in the bottom band and (rotated) top band,
       replacing width/8 consecutive heels, like Shisheng's genTourPatched (bottom band only there)."""
from .core import empty, add_piece, rot180
from . import templates as T

def gen_tour(width, height, heel=T.Sequence1Opt, block=None, block_top=True):
    assert width >= 16 and width % 2 == 0 and height >= 12
    BR = (width // 2 + 2) % 4
    TL = (3 - height) % 4
    TRH = 5 + ((width // 2 + height - 1) % 4)
    t = empty(width, height)
    i = height - 7
    while i >= 0:
        add_piece(t, i, 0, T.VerticalEdge); i -= 4
    i = {0: height - 8, 1: height - 7, 2: height - 10, 3: height - 9}[BR]
    while i >= 0:
        add_piece(t, i, width - 2, rot180(T.VerticalEdge)); i -= 4
    add_piece(t, height - 5, 0, T.CornerHMatchHeight5)
    j = 6
    finalj = {0: width - 6, 1: width - 8, 2: width - 10, 3: width - 4}[BR]
    if block is not None:
        btpl, bw = block
        while j + bw <= finalj:
            add_piece(t, height - 4, j, btpl); j += bw
    while j < finalj:
        add_piece(t, height - 4, j, heel); j += 8
    if BR == 0: add_piece(t, height - 4, j, T.Sequence0)
    elif BR == 1: add_piece(t, height - 4, j, heel)
    elif BR == 2:
        add_piece(t, height - 4, j, T.Sequence0); add_piece(t, height - 6, j + 6, T.Sequence2part2)
    else: add_piece(t, height - 5, j, T.Sequence3)
    if TL == 0: add_piece(t, 0, 0, rot180(T.Sequence0)); j = 6
    elif TL == 1: add_piece(t, 0, 0, rot180(heel)); j = 8
    elif TL == 2:
        add_piece(t, 0, 0, rot180(T.Sequence2part2)); add_piece(t, 0, 4, rot180(T.Sequence0)); j = 10
    else: add_piece(t, 0, 0, rot180(T.Sequence3)); j = 4
    if block is not None and block_top:
        btpl, bw = block
        while j + bw <= width - 8:
            add_piece(t, 0, j, rot180(btpl)); j += bw
    while j < width - 8:
        add_piece(t, 0, j, rot180(heel)); j += 8
    tr = {5: (6, T.CornerVMatchHeight5), 6: (8, T.CornerVMatchHeight6), 7: (10, T.CornerVMatchHeight7), 8: (12, T.CornerVMatchHeight8)}[TRH]
    add_piece(t, 0, width - tr[0], rot180(tr[1]))
    return t
