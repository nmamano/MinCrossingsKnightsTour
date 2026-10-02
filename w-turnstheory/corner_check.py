from itertools import combinations
M=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
def lower(x,ds):
    if x==0:return 1
    if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
    if x==3:return 1-sum(x+d in (1,2) for d in ds)
    return 0
loss=[]
for y in range(4):
    row=[]
    for x in range(4):
        vals=[]
        for a,b in combinations([d for d in M if x+d[0]>=0 and y+d[1]>=0],2):
            t=int(a[0]+b[0]!=0 or a[1]+b[1]!=0)
            vals.append(lower(x,[a[0],b[0]])+lower(y,[a[1],b[1]])-t)
        row.append(max(vals))
    loss.append(row)
print(loss,'sum=',sum(map(sum,loss)))
