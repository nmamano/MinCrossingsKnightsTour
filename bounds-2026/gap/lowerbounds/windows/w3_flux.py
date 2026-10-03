"""Exact colour flux on dual paths (same definition as w-turnstheory/check_corner_box.py).
Cells (x,y) integers; dual vertices at half-integers; doubled coordinates internally.
omega(step) = sum over knight edges e crossing the step of chi(e0)*sign(side of e0) + chi(left cell)."""

def chi(p): return 1 if (p[0] + p[1]) % 2 == 0 else -1
def orient(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def sign(x): return (x > 0) - (x < 0)


def edge_flux(e, step):
    a, b = step
    p, q = [(2 * v[0], 2 * v[1]) for v in e]
    if orient(a, b, p) * orient(a, b, q) >= 0 or orient(p, q, a) * orient(p, q, b) >= 0:
        return 0
    return chi(e[0]) * sign(orient(a, b, p))


def grid_term(step):
    a, b = step
    d = ((b[0] - a[0]) // 2, (b[1] - a[1]) // 2)
    m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
    left = ((m[0] - d[1]) // 2, (m[1] + d[0]) // 2)
    return chi(left)


def path_steps(pts):
    """pts: list of dual vertices in doubled coordinates (odd, odd), consecutive corners; returns unit steps."""
    st = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx = (x1 > x0) - (x1 < x0); dy = (y1 > y0) - (y1 < y0)
        x, y = x0, y0
        while (x, y) != (x1, y1):
            st.append(((x, y), (x + 2 * dx, y + 2 * dy))); x += 2 * dx; y += 2 * dy
    return st


def gamma(R):
    """gamma_R: (R+1/2, 3/2) -> (R+1/2, R+1/2) -> (3/2, R+1/2), doubled."""
    return path_steps([(2 * R + 1, 3), (2 * R + 1, 2 * R + 1), (3, 2 * R + 1)])


def coeffs(steps, edges):
    """Linear form: omega(path) = const + sum_e c_e x_e."""
    const = sum(grid_term(s) for s in steps)
    c = {}
    for e in edges:
        v = sum(edge_flux(e, s) for s in steps)
        if v: c[e] = v
    return const, c
