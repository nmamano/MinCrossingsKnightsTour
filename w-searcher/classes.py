"""Pairing classes for the menu. A class = (name, M, allowed set of (lower line mod M, span d))."""
def lane_class(s, o):
    M = 2 * s; al = set()
    for r in range(s):
        for u in range(s, 2 * s):
            al.add(((o + r) % M, u - r))
    return ('lane s=%d o=%d' % (s, o), M, al)
def classes():
    out = [('free', None, None)]
    for d in (1, 3, 5, 7):
        for p in (0, 1):
            out.append(('d=%d low%%2=%d' % (d, p), 2, {(p, d)}))
    for p in (0, 1):
        out.append(('d in {1,3,5} low%%2=%d' % p, 2, {(p, 1), (p, 3), (p, 5)}))
    for o in range(4):
        out.append(('d=2 low%%4 in {%d,%d}' % (o, (o + 1) % 4), 4, {(o, 2), ((o + 1) % 4, 2)}))
    for s in (2, 3, 4):
        for o in range(2 * s):
            out.append(lane_class(s, o))
    return out

def compat_classes(dmax=9):
    """Lane-free except the pairs of one left class: no 2-cycle with that left gadget."""
    out = []
    for bad in ((1, 3), (0, 1), (0, 5)):
        al = {(p, d) for p in (0, 1) for d in range(1, dmax + 1)} - {bad}
        out.append(('not {c,c+%d} c%%2=%d' % (bad[1], bad[0]), 2, al))
    return out
