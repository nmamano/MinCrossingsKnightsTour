from collections import Counter
def imbalance(n, E, free):
    """black-minus-white residual degree demand of window `free` given fixed edges outside."""
    dem = Counter({p: 2 for p in free})
    for a, b in E:
        if (a in free) != (b in free):
            p = a if a in free else b
            dem[p] -= 1
    return sum(d if (p[0] + p[1]) % 2 == 0 else -d for p, d in dem.items())
