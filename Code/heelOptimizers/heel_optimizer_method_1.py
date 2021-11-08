'''
This was the initial attempt at discovering optimized heels, I've included it particularly because it visualizes the paths at the end. 

The basics of what is going on here:
-Generate array to represent the heel structure
-Generate a graph from that array to represent how the knight can move on the board
-Find all solutions for getting one of the four knights to the end
-For all of those solutions, find all the solutions for the next knight... and so on until you have all possible sets of 4 paths (where each knight goes from start to finish)
-Get rid of all the sets of paths where some squares dont get visited
-Check against turns and crossings metrics

-Parker
'''
from matplotlib import pyplot as plt
#This throws together the heel structure as a 2-d array, quite hard-coded
def generate_small_heel():
    final_set = set()
    for x in range(8):
        for y in range(2):
            final_set.add((x,y))
    for x in [0,1,4,5,6,7]:
        final_set.add((x,2))
    final_set.add((6,3))
    final_set.add((7,3))
    return final_set


#Use the basic rules of knight moves to generate a graph from the array
def generate_connections(P,allowed_coords):
    final_set = set()
    x = P[0]
    y = P[1]
    for diffx, diffy in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]: #theres a smart way to generate this that im not bothering to think of :)
        candidate_coord = (x+diffx,y+diffy)
        if candidate_coord in allowed_coords:
            final_set.add(candidate_coord)
    return final_set


            
#exhaustive search across the space of paths from S to F
def exhaustive_paths(path,connections,final_paths,dont_use = set()):
    curr = path[-1]
    for neigh in connections[curr]:
        if neigh == "D":
            final_paths.append(path)
            return
            
        if not neigh in path and not neigh in dont_use:
            exhaustive_paths(path + [neigh],connections,final_paths,dont_use)
            

        
#we extend the start and finish paths for easier visualizations and to count the true number of turns and crossings
def tack_on(coord):
    return (coord[0] + 2, coord[1] + 1)




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


def show_paths(p):
    for ind in p:
        x_vals = [-x[0] for x in ind]
        y_vals = [x[1] for x in ind]
        plt.plot(x_vals,y_vals)
        plt.plot(x_vals,y_vals, 'bo')
        plt.axis('scaled')
    plt.show()
    

if __name__ == "__main__":    
    small_heel = generate_small_heel()

    start_points = set([(x,y) for x in range(2) for y in range(1,3)])
    finish_points = set([(x,y) for x in range(6,8) for y in range(2,4)])

    

    connection_map_small_heel = {p:generate_connections(p,small_heel) for p in small_heel}
    
    #Visualize our heel to make sure it's right


    for y in range(5,-1,-1):
        s = ""
        for x in range(10):
            if (x,y) in small_heel:
                if (x,y) in start_points:
                    s += "S"
                elif (x,y) in finish_points:
                    s += "F"
                else:
                    s += "@"
            else:
                s += "."
        print(s)


    #if we reach an "F" that knight is considered done, and we will begin searches on the next night

    for tup in finish_points:
        connection_map_small_heel[tup] = "Done"
    for v in connection_map_small_heel.values():
        for coor in start_points:
            if type(v) == type(set()):
                v.discard(coor)


        #all paths for the first knight
    first_point_exhaust = []
    exhaustive_paths([(0,2)],connection_map_small_heel,first_point_exhaust)
    #for each path, find all the possible paths for the second knight
    i = 1
    total = len(first_point_exhaust)
    first_and_second_point_exhaust = []
    for path in first_point_exhaust:
        print(i,"of",total,"...")
        temp = []
        exhaustive_paths([(1,2)],connection_map_small_heel,temp,dont_use = set(path))
        if temp != []:
            for path_two in temp:
                first_and_second_point_exhaust.append([path,path_two])

        i += 1

    #add in the third knight..
    i = 1
    total = len(first_and_second_point_exhaust)
    first_and_second_and_third_point_exhaust = []
    for paths in first_and_second_point_exhaust:
        path_a = paths[0]
        path_b = paths[1]


        print(i,"of",total,"...")
        temp = []
        exhaustive_paths([(0,1)],connection_map_small_heel,temp,dont_use = set(path_a + path_b))
        if temp != []:
            for path_three in temp:
                first_and_second_and_third_point_exhaust.append([path_a,path_b,path_three])

        i += 1

    #and the fourth..
    i = 1
    total = len(first_and_second_and_third_point_exhaust)
    first_and_second_and_third_and_fourth_point_exhaust = []
    for paths in first_and_second_and_third_point_exhaust:
        path_a = paths[0]
        path_b = paths[1]
        path_c = paths[2]

        print(i,"of",total,"...")
        temp = []
        exhaustive_paths([(1,1)],connection_map_small_heel,temp,dont_use = set(path_a + path_b + path_c))
        if temp != []:
            for path_four in temp:
                first_and_second_and_third_and_fourth_point_exhaust.append([path_a,path_b,path_c,path_four])

        i += 1


    #get rid of all sets of paths for which not all squares are visited
    final_paths = []
    for paths in first_and_second_and_third_and_fourth_point_exhaust:
        nodes = sum([len(p) for p in paths])
        if nodes == 24:
            final_paths.append(paths)
    
    extend_final = [ [[tack_on(k[0])] + k + [tack_on(k[-1])] for k in p] for p in final_paths]
    
    for p in extend_final:
        show_paths(p)
        print("crossings:",count_crossings(p))
        print("turns:", count_turns(p))