#!/usr/bin/env python3
"""Check the compressed blocked-run automaton of combo_stab.py against the raw definition.

Random sequences of ghost degrees d2(y), d3(y) in {0,1,2}. Raw: blocked(y) iff d3(y)=0, d2(y-2)=d2(y+2)=2;
K = sum over maximal blocked runs of max(0, l - CAP). Automaton (as in combo_stab.augment): state
(cand(r-1), cand(r), b2(r-1), b2(r), c), started after two rows with true history, emits k while scanning.
The totals agree on every rows window that the automaton sees (rows 2..L-3 can be emitted).
"""
import random


def raw_K(d2, d3, CAP, lo, hi):
    bl = [lo <= y <= hi and d3[y] == 0 and d2[y - 2] == 2 and d2[y + 2] == 2 for y in range(len(d2))]
    K = 0; y = 0
    while y < len(bl):
        if bl[y]:
            z = y
            while z + 1 < len(bl) and bl[z + 1]: z += 1
            K += max(0, z - y + 1 - CAP); y = z + 1
        else:
            y += 1
    return K


def auto_K(d2, d3, CAP):
    L = len(d2)
    b2 = [int(d == 2) for d in d2]; z3 = [int(d == 0) for d in d3]
    # history after row r=1 (rows 0,1 processed): cand(0), cand(1) need d2(-2), d2(-1): unknown -> 0
    cand1, cand2, b2a, b2b, c = 0, 0, b2[0], b2[1], 0
    K = 0
    for r1 in range(2, L):
        blocked = cand1 & b2[r1]
        newcand = z3[r1] & b2a
        if blocked:
            K += int(c == CAP); c = min(c + 1, CAP)
        else:
            c = 0
        cand1, cand2, b2a, b2b = cand2, newcand, b2b, b2[r1]
    return K


def main():
    rnd = random.Random(1)
    for CAP in range(0, 6):
        for trial in range(3000):
            L = rnd.randint(5, 40)
            pr = rnd.random()
            d2 = [2 if rnd.random() < pr else rnd.randint(0, 1) for _ in range(L)]
            d3 = [0 if rnd.random() < pr else rnd.randint(1, 2) for _ in range(L)]
            # automaton emits blocked(y) for y = 2 .. L-3 (needs d2(y+2)); rows 0,1 lack history
            assert auto_K(d2, d3, CAP) == raw_K(d2, d3, CAP, 2, L - 3), (CAP, d2, d3)
    print('PASS: automaton K equals raw K on 18000 random degree sequences, run constants 0..5')


if __name__ == '__main__':
    main()
