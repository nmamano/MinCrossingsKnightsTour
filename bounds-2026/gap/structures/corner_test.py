"""Do the cheap edge patterns P and P' pass the endpoint tests of the audited 14n/3 proof (Section 3)?
Coefficient table copied from w-turnstheory/PROOF_crossings_lower.md. KT Structures, 2026-10-03."""
coef = {((0,-1),(1,1)): -1, ((0,0),(1,-2)): -1, ((0,0),(2,-1)): -1, ((0,1),(1,-1)): 1,
        ((0,1),(2,0)): 1, ((0,2),(1,0)): -1, ((1,0),(2,2)): -1, ((1,1),(2,-1)): -1}
norm = lambda e: tuple(sorted(e))
coef = {norm(k): v for k, v in coef.items()}
def edges(mirror, Y=range(-12, 12)):
    s = -1 if mirror else 1
    E = set()
    for y in Y:
        E.add(norm(((0, y), (1, y + 2*s))))           # U-turn
        for x in (0, 1, 2):
            E.add(norm(((x, y), (x + 2, y + s))))     # line edges
    return E
def test(E, R, down=False):
    E = {norm(((a[0], a[1] - R), (b[0], b[1] - R))) for a, b in E}
    if down:
        E = {norm(((a[0], -a[1]), (b[0], -b[1]))) for a, b in E}
    F = sum(coef.get(e, 0) for e in E)
    forb = norm(((0,0),(2,1))) in E and norm(((0,1),(2,0))) in E
    return F % 3 == 2 and not forb
for mirror, name in ((False, 'P'), (True, "P'")):
    E = edges(mirror)
    res = [(test(E, R), test(E, R, True)) for R in range(-3, 4)]
    assert all(a and b for a, b in res), res
    print(name, 'passes the up and down tests at every scan row')
