/* Algorithm for knight's tour that generalizes the Hausdorff heuristic in the following ways:
- A normal knight jumps 1 squre in one dimension and 2 in the other. We allow to change 1 and 2 to other values
- A chess board is usually a square. We allow it to be any rectangle and to have "blocked squares" that cannot be visited
- A knight's tour usually has a single knight. We allow it to have any number of "knights". We only need to specify the starting and ending positions of all the "knights".

This code was used in the paper
"Taming the Knight's Tour: Minimizing Turns and Crossings,"
(available online at https://arxiv.org/pdf/1904.02824.pdf)
to find a valid "giraffe heel" (see Figure 18)


Made by Nil Mamano
*/

#include <bits/stdc++.h>
#include<vector>
#include<string>

using namespace std;


/*
'.' indicates an unvisited square
'*' indicates an end square
'S' indicates a starting square
'E' indicates an ending square
'X' indicates a blocked/visited square
Close move: move between S and E
Normal move: move to '.' from S or E
Legal move: close more or normal move
A continuation to a normal move is a move
to '.' or to the opposite letter
*/

struct Pos {
    int x; //column
    int y; //row
    Pos(int x, int y): x(x), y(y) {} //column first!
    Pos(): x(-1), y(-1) {}
    Pos operator+(const Pos other) const {
        return Pos(x+other.x, y+other.y);
    }
    Pos& operator=(const Pos &other) {
        x = other.x;
        y = other.y;
        return *this;
    }
    bool operator==(const Pos& other) {
        return x == other.x and y == other.y;
    }
    bool operator!=(const Pos& other) {
        return not (x == other.x and y == other.y);
    }

};

struct Path{

    char type; //'S' or 'E' or 'C' (complete)
    vector<Pos> moves;
    Path(): type('!'), moves(0) {} //not to be used, only for compiler warning
    Path(const Pos& start, char type): type(type), moves(1, start) {}

    int size() const {
        return (int)moves.size();
    }
    Pos first() const {
        return moves[0];
    }
    Pos last() const {
        return moves[size()-1];
    }

    static Path merge(const Path& path1, const Path& path2) {
        const Path& startPath = path1.type == 'S'? path1 : path2;
        const Path& endPath = path1.type == 'E'? path1 : path2;
        Path res(startPath.first(), 'C');
        for (int i = 1; i < startPath.size(); i++) {
            res.moves.push_back(startPath.moves[i]);
        }
        for (int i = endPath.size()-1; i >= 0; i--) {
            res.moves.push_back(endPath.moves[i]);
        }
        return res;
    }

    void print() const {
        cout<<size()<<"-"<<type;
        cout<<"("<<first().x<<","<<first().y<<" -> "<<last().x<<","<<last().y<<")";
    }

    void printMoves() const {
        for (int i = 0; i < size(); i++) {
            cout<<"("<<moves[i].x<<","<<moves[i].y<<")"<<" ";
        }
    }

    void overlayOnGrid(vector<string>& grid, char endLabel, char midLabel) const {
        for (const Pos& pos : moves) {
            grid[pos.y][pos.x] = midLabel;
        }
        grid[first().y][first().x] = endLabel;
        grid[last().y][last().x] = endLabel;
    }
};

struct Board {
    vector<Pos> moves;
    int numRows;
    int numCols;

    vector<string> grid; //matrix representation of the board state
    //'.' indicates unvisited cell
    //'X' indicates already visited/initially blocked cell
    //'S' indicates the last cell of a type-S open path
    //'E' indicates the last cell of a type-E open path
    vector<Path> openPaths; //incomplete
    vector<Path> closedPaths; //complete
    Board(): moves(vector<Pos>(8)), grid(vector<string>(0)),
             openPaths(vector<Path>(0)), closedPaths(vector<Path>(0)) {}
    Board(const Board& copy): moves(vector<Pos>(copy.moves)), numRows(copy.numRows), numCols(copy.numCols), grid(copy.grid),
                       openPaths(copy.openPaths), closedPaths(copy.closedPaths) {}
    void init() {
        int leap1, leap2;
        cin >> leap1 >> leap2;
        moves[0] = Pos( leap1,  leap2);
        moves[1] = Pos( leap1, -leap2);
        moves[2] = Pos(-leap1,  leap2);
        moves[3] = Pos(-leap1, -leap2);
        moves[4] = Pos( leap2,  leap1);
        moves[5] = Pos( leap2, -leap1);
        moves[6] = Pos(-leap2,  leap1);
        moves[7] = Pos(-leap2, -leap1);

        cin >> numRows >> numCols;
        for (int i = 0; i < numRows; i++) {
            string s;
            cin >> s;
            grid.push_back(s);
            for (int j = 0; j < numCols; j++) {
                if (s[j] == 'S' || s[j] == 'E') {
                    openPaths.push_back(Path(Pos(j, i), s[j]));
                }
            }
        }
    }

    //returns the board, but with each cell labeled according to the paths
    vector<string> pathOverlayGrid() const {
        vector<string> res(grid);
        char startLabel = 'a';
        char endLabel = 'A';
        for (auto &path: openPaths) {
            if (path.type == 'S') {
                path.overlayOnGrid(res, startLabel, startLabel);
                startLabel++;
            } else {
                path.overlayOnGrid(res, endLabel, endLabel);
                endLabel++;
            }
        }
        char completeLabel = '0';
        for (auto &path : closedPaths) {
            path.overlayOnGrid(res, completeLabel, completeLabel);
            completeLabel++;
        }
        return res;
    }

    vector<string> closedPathOverlayGrid() const {
        vector<string> res(grid);
        char endLabel = 'A';
        char midLabel = 'a';
        for (auto &path : closedPaths) {
            path.overlayOnGrid(res, endLabel, midLabel);
            endLabel++;
            midLabel++;
        }
        return res;
    }

    void print() {
        cerr<<"move vector for ("<<moves[0].x<<","<<moves[0].y<<")-leaper: ";
        for (int i = 0; i < 8; i++) {
            cerr<<"("<<moves[i].x<<","<<moves[i].y<<") ";
        }
        cerr<<endl;
        cerr<<"open paths";
        for (int i = 0; i < (int)openPaths.size(); i++) {
            if (i%4 == 0) cerr<<endl;
            openPaths[i].print();
            cerr<<" ";
        }
        cerr<<endl;
        cerr<<"closed paths";
        for (int i = 0; i < (int)closedPaths.size(); i++) {
            if (i%4 == 0) cerr<<endl;
            closedPaths[i].print();
            cerr<<" ";
        }
        cerr<<endl;
        cerr<<"grid:"<<endl;
        for (int i = 0; i < numRows; i++) {
            cerr<<grid[i]<<endl;
        }
        cerr<<endl;
        vector<string> overlay = pathOverlayGrid();
        cerr<<"path visualization:"<<endl;
        for (int i = 0; i < numRows; i++) {
            cerr<<overlay[i]<<endl;
        }
        cerr<<endl;
    }

    void printSolution() {
        vector<string> overlay = closedPathOverlayGrid();
        char label = 'A';
        for (auto &path : closedPaths) {
            cout<<label<<": ";
            label++;
            for (int i = 0; i < path.size(); i++) {
                cout<<"("<<path.moves[i].x<<","<<numRows-1-path.moves[i].y<<")"<<" ";
            }
            cout<<endl;
        }
        for (int i = 0; i < numRows; i++) {
            cerr<<overlay[i]<<endl;
        }
        cerr<<endl;
    }

    bool isInBounds(const Pos& pos) const {
        return pos.x >= 0 and pos.x < numCols and pos.y >= 0 and pos.y < numRows;
    }

    char cell(const Pos& pos) const {
        //assumes that pos is in bounds
        return grid[pos.y][pos.x]; //note that row (y coord) is indexed first
    }

    void setCell(const Pos& pos, char type) {
        grid[pos.y][pos.x] = type;
    }

    bool isLegal(const Path& p, const Pos& pos) const {
        if ((not isInBounds(pos)) or cell(pos) == 'X') return false;
        return cell(pos) == '.' || cell(pos) != p.type;
        //in fact, the '.' case is redundant, but there for legibility
    }


    void extendPath(int pathId, const Pos& pos) {
        //assumes that pos is a legal neighbor of the last cell in the open path
        Path& p = openPaths[pathId];
        setCell(p.last(), 'X');
        if (cell(pos) == '.') {
            setCell(pos, p.type);
            p.moves.push_back(pos);
        } else { //merging two open paths into a closed path
            setCell(pos, 'X');
            int id2 = 0;
            while (not (openPaths[id2].last() == pos)) id2++;
            closedPaths.push_back(Path::merge(p, openPaths[id2]));
            //delete the open paths, starting with the later one
            //so indices don't get messed up
            int minId = pathId < id2 ? pathId : id2;
            int maxId = pathId > id2 ? pathId : id2;
            openPaths.erase(openPaths.begin()+maxId);
            openPaths.erase(openPaths.begin()+minId);
        }
    }

/* Returns false if it is not possible to extend any path.
   Otherwise, chooses a move according to the following rules, and
   updates the data structures accordingly

For an (open) path p, let c_p be a "p-move" if c_p is a a legal continuation to p,
and let p.degree be the number of p-moves
(includes free cells and path ends of a different type)

for a non-ending p-move c_p, let c_p.degree be the number of continuations to p if p goes to c_p
for a path p, let p.2degree be the sum of c_p.degree over all c_p.
(if c_p is an ending path, consider c_p.degree = 1)

Forced propagation: (consider paths and p-moves in random order)
1. If a p-move c_p has degree 0, fail (only open paths with the type of p can reach c_p,
and they have no continuation)
2. If a p-move c_p has degree 1, and c_p has no other open-path ends as neighbors,
extend p to c_p and to its only continuation
(if p went anywhere else, c_p could never be visited)
3. If a path p has degre 0, fail (cannot continue that path)
4. If a path p has degree 1, extend it to its only p-move

Heuristic rule:
- Choose a path p with smallest 2degree (randomly).
- Choose a p-move with the smallest degree (randomly)
among those that are not closing moves.
- If there is no such move, choose a closing move
*/
    bool extendAPath() {
        const int INF = 1000000;

        //call minp a path with smallest 2degree
        //and minc_minp a minp-move with smallest degree
        int minp_id = -1; //we use ids to refer to indices to openPaths
        Pos minc_minp;
        int minp_2degree = INF;
        //we will update these values as we search for forced propagations
        //in case we don't find any forced propagation

        //iterate through paths and count path degrees and 2degrees, and p-move degrees
        //todo: 'i' should start at random index and loop around,
        //so that any forced continuation is equally likely to be found first
        bool DBG = false;
        if(DBG)cerr<<"there are "<<openPaths.size()<<" open paths left"<<endl;
        int rand_offset = rand()%openPaths.size();
        for (int i = 0; i < (int)openPaths.size(); i++) {
            int id = (i+rand_offset)%openPaths.size();
            if(DBG)cerr<<"path "<<id<<" ";
            Path& p = openPaths[id];
            int p_degree = 0;
            int p_2degree = 0;
            Pos minc_p; //the choice of move for p, according to the heuristic rule
                        //(the non-closing move with smallest degree, or any closing move otherwise)
            int minc_p_degree = INF;
            for (int j = 0; j < 8; j++) { //should j be random?
                Pos c_p = p.last()+moves[j];
                if (isLegal(p, c_p)) {
                    p_degree++;
                    if (cell(c_p) != '.') { //ending move
                        p_2degree++; //an ending move contributes +1 to the 2degree
                        //choose it as next move if no non-ending move has been found yet
                        if (minc_p_degree == INF) {
                            minc_p = c_p;
                        }
                    } else  { //non-ending move
                        int c_p_degree = 0;
                        Pos c_p_cont; //any c_p cont
                        for (int k = 0; k < 8; k++) { //should k be random?
                            if (isLegal(p, c_p+moves[k])) {
                                c_p_cont = c_p+moves[k];
                                c_p_degree++;
                                p_2degree++;
                            }
                        }
                        //forced propagation
                        if (c_p_degree == 0) {
                            if(DBG)cerr<<"next to dead end. fail"<<endl;
                            return false;
                        }
                        if (c_p_degree == 1) {
                            if(DBG)cerr<<"triggers double forced prop."<<endl;
                            extendPath(id, c_p);
                            extendPath(id, c_p_cont);
                            return true;
                        }
                        if (c_p_degree < minc_p_degree) {
                            minc_p = c_p;
                            minc_p_degree = c_p_degree;
                        }
                    }
                }
            }
            //forced propagation
            if (p_degree == 0) {
                if(DBG)cerr<<"cannot continue. fail"<<endl;
                return false;
            }
            if (p_degree == 1) {
                if(DBG)cerr<<"triggers forced prop"<<endl;
                extendPath(id, minc_p);
                return true;
            }
            if (p_2degree < minp_2degree) { //found better candidate to minp
                minp_id = id;
                minc_minp = minc_p;
                minp_2degree = p_2degree;
            }
            if(DBG)cerr<<"has degree "<<p_degree<<" and 2degree "<<p_2degree<<endl;
        }

        //heuristically chosen non-forced move
        if(DBG)cerr<<"heuristic: extend path "<<minp_id<<endl;
        extendPath(minp_id, minc_minp);
        return true;
    }

    bool everyCellVisited() const {
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                if (grid[i][j] == '.') return false;
            }
        }
        return true;
    }

    /* Returns false if no solution found */
    bool completePaths() {
        int iter_count = 0;
        cerr << "iteration: ";
        while(not openPaths.empty()) {
            if (extendAPath()) {
                cerr<<".";
                iter_count++;
                if (iter_count% 50 == 0) cerr<<endl;
            } else {
                return false;
            }
        }
        if (not everyCellVisited()) {
            //this rarely happens
            cerr<<"closed all paths but didn't explore all cells"<<endl;
            return false;
        }
        cerr<<"completed paths in "<<iter_count<<" iterations"<<endl;
        return true;
    }


};




int main()
{
    // To make sure that different random
    // initial positions are picked.
    srand(time(NULL));
    Board b;
    b.init();
    int attempt_count = 1;
    bool success = false;
    while (not success) {
        cout <<"ATTEMPT "<<attempt_count<<endl;
        Board b2(b);
        success = b2.completePaths();
        // b2.print();
        if (success) {
            b2.print();
            b2.printSolution();
        }
    }
}
