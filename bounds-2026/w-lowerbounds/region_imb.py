import sys
sys.argv=['x']+sys.argv[1:]
exec(open('chevron_untrap.py').read().split("cand = set()")[0])
from collections import Counter
dem=Counter({p:2 for p in free})
for a,b in E:
    if (a in free)!=(b in free):
        dem[a if a in free else b]-=1
print('free',len(free),'imbalance', sum(d if (p[0]+p[1])%2==0 else -d for p,d in dem.items()), 'total demand', sum(dem.values()))
print('defect cells', sorted(bad))
