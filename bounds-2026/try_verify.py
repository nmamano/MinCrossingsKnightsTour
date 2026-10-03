from kt.verify_strip import check_bottom
from kt import templates as T
tpl16 = ['46 46 56 56 56 26 46 46','14 14 14 45 45 45 45 46','05 15 15 15 15 05 05 05','01 01 01 01 01 01 01 01']
print('opt heel', check_bottom(T.Sequence1Opt))
print('candidate16', check_bottom(tpl16))
