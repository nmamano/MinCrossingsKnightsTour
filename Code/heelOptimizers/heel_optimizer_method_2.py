'''
This pyfile is adapted from a notebook, it may not run perfectly without a little bit of finnicking
The main purpose of this file is have some record of this style of search

This notebook is much more exploratory than method 1, and I am going to avoid documenting much of it unless there is a demand.

TLDR: expanding the heel search space does not seem to yield better solutions!

This notebook does three things:
-The search space can be arbitrarily expanded
-Two larger search spaces are explored and the resulting number of turns and crossings are plotted. Due to the way the code is written, it just prints the number of turns and crossings when it finds a solution, and I copy pasted these results into a cell and plot them, there is a lot of scrolling to do (sorry). For this reason I am not able to easily display the actual paths, if this exploration ever yielded better solutions I would have added this capability.
-The underlying data structures used for search are made in a way that can be ported into C (so it can be paralellized across different search paths) and use very inexpensive operations (mainly modulus). Again, based on the results from expanding the search twice, this probably would not yield better solutions, so it has not been tried.
'''

import copy



#incrementing start and fin will increase the search space
start = 2
fin = 0
size_array = (4 + max((start-1),fin),8 + max((start-3)*2,fin*2))
starting_array = [[6 for n in range(size_array[1])] for c in range(size_array[0])]


a1,a2 = 1,0
b1,b2 = 1,1
c1, c2 = 2,0
d1, d2 = 2,1

e1, e2 = 2,6
f1, f2 = 2,7
g1, g2 = 3,6
h1, h2 = 3,7

for i in range(8):
    starting_array[0][i] = 5
for i in range(2,8):
    starting_array[1][i] = 5
for i in range(4,6):
    starting_array[2][i] = 5

while start > 0:
    starting_array[a1][a2] = 5
    starting_array[b1][b2] = 5
    starting_array[c1][c2] = 5
    starting_array[d1][d2] = 5
    a1 += 1
    a2 += 2
    b1 += 1
    b2 += 2
    c1 += 1
    c2 += 2
    d1 += 1
    d2 += 2
    start -= 1
starting_array[a1][a2] = 0
starting_array[b1][b2] = 1
starting_array[c1][c2] = 2
starting_array[d1][d2] = 3

fin += 1 #hacky
while fin > 0:
    starting_array[e1][e2] = 5
    starting_array[f1][f2] = 5
    starting_array[g1][g2] = 5
    starting_array[h1][h2] = 5
    e1 += 1
    e2 += 2
    f1 += 1
    f2 += 2
    g1 += 1
    g2 += 2
    h1 += 1
    h2 += 2
    fin -= 1

fin2_ubound = 7 + fin*2
fin2_lbound = 6 + fin*2
fin1_ubound = 3 + fin
fin1_lbound = 2 + fin

def is_fin(v1,v2):
    return (v1 == fin1_lbound or v1 == fin1_ubound) and (v2 == fin2_lbound or v2 == fin2_ubound) 

rec = []
for r in range(4):
    toadd = []
    for c in range(8):
        toadd.append(is_fin(r,c))
    rec.append(toadd)

# [[ 5, 5, 5, 5, 5, 5, 5, 5],
#  [ 0, 1, 5, 5, 5, 5, 5, 5],
#  [ 2, 3, 6, 6, 5, 5, 5, 5],
#  [ 6, 6, 6, 6, 6, 6, 5, 5]]
#use mod 7


def print_arr(arr):
    for r in arr:
        print(r)
    print()
print_arr(starting_array)
print_arr(rec)


#notes: this is probably very inefficient but whatever
def turns_and_crosses(oarr):
#takes in search result and gives [[(r,c),...],[],[],[]]
#also tacks on to account for extra turns and crossings from the entrance and exit +1r +2c
    arr = copy.deepcopy(oarr)
    p = [[],[],[],[]]
    for m in range(4):
        t = m
        while 1:
            found = False
            for r in range(len(arr)):
                for c in range(len(arr[0])):
                    if arr[r][c] == t:
                        p[t%7].append((r,c))
                        found = True
            if not found:
                break
            t += 7
    for path in p:
        first = path[0]
        path.insert(0,(first[0] + 1,first[1] + 2))
        last = path[-1]                
        path.append((last[0] + 1,last[1] + 2))
    return p

def ccw(A,B,C):
return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D) and (A != C and A != D and B != C and B != D)

def count_crossings(p):
    segs = set()
    intersects = 0
    for knight in p:
        for i in range(len(knight)-1):
            new_seg = (knight[i],knight[i+1])
            for other_seg in segs:
                if intersect(new_seg[0],new_seg[1],other_seg[0],other_seg[1]):
                    intersects +=1
                    #print(new_seg[0],new_seg[1],other_seg[0],other_seg[1])
                    #plt.plot([new_seg[0][0],new_seg[1][0]],[new_seg[0][1],new_seg[1][1]])
                    #plt.plot([other_seg[0][0],other_seg[1][0]],[other_seg[0][1],other_seg[1][1]])
                    #plt.show()
            segs.add(new_seg)
    return intersects

def count_turns(p):
    turns = 0
    for knight in p:
        curr_x = None
        curr_y = None
        for i in range(1,len(knight)):
            new_x = knight[i][0] - knight[i-1][0]
            new_y = knight[i][1] - knight[i-1][1]

            if (curr_x != new_x or curr_y != new_y) and curr_x != None:
                turns += 1
            curr_x = new_x
            curr_y = new_y
    return turns

depth_hist = [0 for n in range(100)]


def search(locs, #[a1,a2,b1,b2,...]
           arr,
           extend_idx = 0, depth = 0):
    found = False
    for d_extend in range(4):
        i1,i2 = extend_idx*2,extend_idx*2 + 1
        v1,v2 = locs[i1], locs[i2]

        if not is_fin(v1,v2):
            found = True
            break
        extend_idx = (extend_idx + 1) % 4 
    if not found:
        for r in arr:
            for c in r:
                if c % 7 == 5:
                    return
        #print_arr(arr)
        o = turns_and_crosses(arr)
        print("(" + str(count_crossings(o)) + "," +  str(count_turns(o)) +"),")

        return
        #verify that all squares got hit (no v % 7 == 5) and return

    for diff1,diff2 in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:

        poss1,poss2 = v1 + diff1, v2 + diff2
        if (poss1 >= 0 and poss1 < size_array[0]) and (poss2 >= 0 and poss2 < size_array[1]):

            #print(v1,v2,poss1,poss2)
            #print(arr[v1][v2],arr[poss1][poss2])
            if arr[poss1][poss2] % 7 == 5: 
                new_arr = copy.deepcopy(arr)
                new_arr[poss1][poss2] = arr[v1][v2] + 7
                new_locs = locs.copy()
                new_locs[i1] = poss1
                new_locs[i2] = poss2
                search(new_locs,new_arr,(extend_idx + 1) % 4,depth +1)
    return

