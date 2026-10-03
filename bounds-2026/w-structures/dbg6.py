from fold3 import build
from collections import Counter
n=48
E, deg = build(n, ts=(1,1,1,1))
print([(y, deg[(0,y)], deg[(1,y)]) for y in range(6, 18)])
print(sorted(e for e in E if e[0][0] == 0 and 6 <= e[0][1] < 18))
E2, deg2 = build(n, ts=(1,1,1,1), flip=lambda r, y: r == 0 and 8 <= y < 16)
print(sorted(e for e in E2 if e[0][0] == 0 and 6 <= e[0][1] < 18))
