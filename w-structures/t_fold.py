from fold2 import build, stats
import itertools
n = 48
for combo in itertools.product((1, -1), repeat=2):
    def ut(r, y, par, c=combo):
        return c[par]
    E, deg, U = build(n, uturn=ut)
    print(combo, stats(n, E, deg)[:3])
# per-edge choices: left/bottom different
for combo in itertools.product((1, -1), repeat=4):
    def ut(r, y, par, c=combo):
        return c[r]
    E, deg, U = build(n, uturn=ut)
    s = stats(n, E, deg); print('per-edge', combo, s[:3], s[3][-6:])
