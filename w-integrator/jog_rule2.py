import sys; sys.path.insert(0, '.')
from jog_rule import closed_with, seqgen
def find_bands(n, seqs=((5, 9), (5, 13), (7, 15))):
    h = n // 2
    for a, b in seqs:
        s = [D for D in seqgen(a, b) if D < h - 2]
        for K in range(1, len(s) + 1):
            c, dft = closed_with(n, [h - D for D in s[:K]])
            if c == 0: return (a, b), s[:K], dft
    return None
if __name__ == '__main__':
    for n in range(48, 201, 2):
        print(n, find_bands(n), flush=True)
