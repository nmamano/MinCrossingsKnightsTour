/* Algorithm for knight's tour that generalizes the Hausdorff heuristic in the following ways:
- A normal knight jumps 1 squre in one dimension and 2 in the other. We allow to change 1 and 2 to other values
- A chess board usually has a square shape. We allow it to be any rectangle and to have "blocked cells" that cannot be visited
- A knight's tour usually has a single knight. We allow it to have any number of "knights". We only need to specify the starting and ending positions of all the "knights".

This code was used in the paper
"Taming the Knight's Tour: Minimizing Turns and Crossings,"
(available online at https://arxiv.org/pdf/1904.02824.pdf)
to find a valid "giraffe corner" (see Figure 18)

Made by Nil Mamano
*/

#include <bits/stdc++.h>
#include<vector>
#include<string>
#include<array>
using namespace std;

/* Notation and conventions
'.' indicates an unvisited cell
'S' indicates a starting cell
'E' indicates an ending cell
'X' indicates a blocked or already-visited cell

Close move: move between S and E
Normal move: move to '.' from S or E
Legal move: close move or normal move
A continuation to a normal move is a move to '.' or to the opposite letter

An S-path is a sequence of moves starting from an S cell.
An E-path is a sequence of moves starting from an E cell.
A C-path (closed) is a sequence of moves going from an S cell to an E cell.
*/

struct Pos {
    int x, y; //column, row
    Pos(int x, int y): x(x), y(y) {} //column first!
    Pos(): x(-1), y(-1) {}
    Pos operator+(const Pos other) const {
        return Pos(x+other.x, y+other.y);
    }
    Pos& operator=(const Pos &other) {
        x = other.x, y = other.y;
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
    char type; //S, E, or C
    vector<Pos> moves;
    Path(): type('!'), moves(0) {} //not to be used, only for compiler warning
    Path(const Pos& start, char type): type(type), moves(1, start) {}
    int size() const { return (int)moves.size(); }
    Pos first() const { return moves[0]; }
    Pos last() const { return moves[size()-1]; }
    void printMoves() const {
        for (auto pos : moves)
            cout<<"("<<pos.x<<","<<pos.y<<")"<<" ";
    }
    void print() const {
        cout<<size()<<"-"<<type;
        cout<<"("<<first().x<<","<<first().y<<" -> "<<last().x<<","<<last().y<<")";
    }

    //unites an S-path and an E-path into a C-path
    static Path merge(const Path& path1, const Path& path2) {
        const Path& sPath = path1.type == 'S'? path1 : path2;
        const Path& ePath = path1.type == 'E'? path1 : path2;
        Path res(sPath.first(), 'C');
        for (int i = 1; i < sPath.size(); i++)
            res.moves.push_back(sPath.moves[i]);
        for (int i = ePath.size()-1; i >= 0; i--)
            res.moves.push_back(ePath.moves[i]);
        return res;
    }

    void overlayOnGrid(vector<string>& grid, char endpointLabel, char midpointLabel) const {
        for (auto pos : moves)
            grid[pos.y][pos.x] = midpointLabel;
        grid[first().y][first().x] = endpointLabel;
        grid[last().y][last().x] = endpointLabel;
    }
};

struct Board {
    //the 8 cells that can be reached in one move from (0,0)
    array<Pos, 8> moves;

    int numRows, numCols;
    vector<string> grid; //matrix representation of the board state
    //'.': unvisited cell
    //'X': already visited/initially blocked cell
    //'S': the last cell of a type-S open path
    //'E': the last cell of a type-E open path
    vector<Path> openPaths; //S- and E-paths
    vector<Path> closedPaths; //C-paths

private:
    //use the factory method below
    Board(): grid(vector<string>(0)), openPaths(vector<Path>(0)), closedPaths(vector<Path>(0)) {}
public:
    Board(const Board& copy): moves(copy.moves), numRows(copy.numRows), numCols(copy.numCols),
                       grid(copy.grid), openPaths(copy.openPaths), closedPaths(copy.closedPaths) {}
    
    static Board makeBoardFromInput() {
        Board b;
        int leap1, leap2;
        cin >> leap1 >> leap2;
        b.moves = {Pos( leap1, leap2), Pos( leap1, -leap2),
                   Pos(-leap1, leap2), Pos(-leap1, -leap2),
                   Pos( leap2, leap1), Pos( leap2, -leap1),
                   Pos(-leap2, leap1), Pos(-leap2, -leap1)};
        cin >> b.numRows >> b.numCols;
        for (int i = 0; i < b.numRows; i++) {
            string s;
            cin >> s;
            b.grid.push_back(s);
            for (int j = 0; j < b.numCols; j++) {
                if (s[j] == 'S' || s[j] == 'E') {
                    b.openPaths.push_back(Path(Pos(j, i), s[j]));
                }
            }
        }
        return b;
    }

    //returns the board with each cell labeled according to the paths:
    //starting paths get lowercase letters, ending paths get uppercase letters,
    //and closed paths get numbers
    vector<string> pathOverlayGrid() const {
        vector<string> res(grid);
        char sLabel = 'a', eLabel = 'A', cLabel = '0';
        for (auto &path: openPaths) {
            if (path.type == 'S') {
                path.overlayOnGrid(res, sLabel, sLabel);
                sLabel++;
            } else {
                path.overlayOnGrid(res, eLabel, eLabel);
                eLabel++;
            }
        }
        for (auto &path : closedPaths) {
            path.overlayOnGrid(res, cLabel, cLabel);
            cLabel++;
        }
        return res;
    }

    //returns the board showing the closed paths: each path gets a letter,
    //uppercase denotes the endpoints and lowercase denotes intermediate steps of the path 
    vector<string> closedPathOverlayGrid() const {
        vector<string> res(grid);
        char endpointLabel = 'A', midpointLabel = 'a';
        for (auto &path : closedPaths) {
            path.overlayOnGrid(res, endpointLabel, midpointLabel);
            endpointLabel++;
            midpointLabel++;
        }
        return res;
    }

    void print() {
        cout<<"move-vector for ("<<moves[0].x<<","<<moves[0].y<<")-leaper: ";
        for (int i = 0; i < 8; i++) {
            cout<<"("<<moves[i].x<<","<<moves[i].y<<") ";
        }
        cout<<endl;
        cout<<"open paths";
        for (size_t i = 0; i < openPaths.size(); i++) {
            if (i%4 == 0) cout<<endl;
            openPaths[i].print();
            cout<<" ";
        }
        cout<<endl;
        cout<<"closed paths";
        for (size_t i = 0; i < closedPaths.size(); i++) {
            if (i%4 == 0) cout<<endl;
            closedPaths[i].print();
            cout<<" ";
        }
        cout<<endl;
        cout<<"grid:"<<endl;
        for (int i = 0; i < numRows; i++) {
            cout<<grid[i]<<endl;
        }
        cout<<endl;
        vector<string> overlay = pathOverlayGrid();
        cout<<"path visualization:"<<endl;
        for (int i = 0; i < numRows; i++) {
            cout<<overlay[i]<<endl;
        }
        cout<<endl;
    }

    void printSolution() {
        vector<string> overlay = closedPathOverlayGrid();
        char label = 'A';
        for (auto &path : closedPaths) {
            cout<<label<<": ";
            label++;
            for (int i = 0; i < path.size(); i++) {
                int reversedY = numRows-1-path.moves[i].y;
                cout<<"("<<path.moves[i].x<<","<<reversedY<<")"<<" ";
            }
            cout<<endl;
        }
        for (int i = 0; i < numRows; i++)
            cout<<overlay[i]<<endl;
        cout<<endl;
    }

    inline bool isInBounds(const Pos& pos) const {
        return pos.x >= 0 and pos.x < numCols and pos.y >= 0 and pos.y < numRows;
    }

    inline char cell(const Pos& pos) const {
        //assumes that pos is in bounds
        return grid[pos.y][pos.x]; //note that row (y coord) is indexed first
    }

    inline void setCell(const Pos& pos, char type) {
        //assumes that pos is in bounds
        grid[pos.y][pos.x] = type;
    }

    //checks whether an open path p can be extended to cell pos
    inline bool isLegal(const Path& p, const Pos& pos) const {
        return isInBounds(pos) and cell(pos) != 'X' and cell(pos) != p.type;
        //last condition checks that an S-path goes to '.' or 'E' and an
        //E-path goes to '.' or 'S'
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

    /* If it is not possible to extend any path, returns false.
    Otherwise, extends one path by 1 move (occasionally 2), updates the data structures
    accordingly, and returns true.

    It chooses the move according to the following rules.
    - If there is a forced progatation, it does that.
    - Otherwise, it follows an heuristic inspired by the Hausdorff heuristic.

    Notation:
    For an (open) path p, let c_p be a "p-move" if c_p is a a legal continuation to p.
    p-moves can be ending or non-ending
    An ending p-move connects p to a path of a different type (S vs E) 
    A non-ending p-move connects p to a free cell ('.')
    Let p.degree be the number of p-moves.
    For a non-ending p-move c_p, let c_p.degree be the number of continuations to p if p goes to c_p
    For an ending p-move c_p, define c_p.degree as 1.
    For a path p, let p.2degree be the sum of c_p.degree over all c_p.

    Forced propagations:
    1. If a p-move c_p has degree 0, fail (only open paths with the type of p can reach c_p,
    and they have no continuation)
    2. If a non-ending p-move c_p has degree 1, and c_p has no other open-path ends as neighbors,
    extend p to c_p and to its only continuation (if p went anywhere else, c_p could never be visited)
    3. If a path p has degre 0, fail (cannot continue that path)
    4. If a path p has degree 1, extend it to its only p-move

    Heuristic rule:
    - Choose a path p with smallest 2degree (randomly)
    - Choose a p-move with the smallest degree among those that are not closing moves (randomly).
    - If there is no such move, choose a closing move */
    bool extendAPath() {
        constexpr int INF = 1000000;
        constexpr bool DBG = false;

        //we call minp a path with smallest 2degree
        //and minc_minp a minp-move with smallest degree
        int minp_id = -1; //we use ids to refer to indices to openPaths
        Pos minc_minp;
        int minp_2degree = INF;
        //we will update these values as we search for forced propagations,
        //in case we don't find any forced propagation

        //iterate through paths and count path degrees and 2degrees, and p-move degrees
        //todo: 'i' should start at random index and loop around,
        //so that any forced continuation is equally likely to be found first
        if(DBG)cerr<<"there are "<<openPaths.size()<<" open paths left"<<endl;
        int rand_offset = rand()%openPaths.size();
        for (size_t i = 0; i < openPaths.size(); i++) {
            int id = (i+rand_offset)%openPaths.size();
            if(DBG)cerr<<"path "<<id<<" ";
            Path& p = openPaths[id];
            int p_degree = 0;
            int p_2degree = 0;
            Pos minc_p; //the choice of move for p, according to the heuristic rule
                        //(the non-closing move with smallest degree, or any closing move otherwise)
            int minc_p_degree = INF;
            for (int j = 0; j < 8; j++) { //todo: should j be random?
                Pos c_p = p.last()+moves[j];
                if (isLegal(p, c_p)) {
                    p_degree++;
                    if (cell(c_p) != '.') { //ending move
                        p_2degree++; //an ending move contributes +1 to the 2degree
                        //choose it as next move if no non-ending move has been found yet
                        if (minc_p_degree == INF)
                            minc_p = c_p;
                    } else { //non-ending move
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
            if (extendAPath()) { //try to extend one path by one move
                cerr<<".";
                iter_count++;
                if (iter_count% 50 == 0) cerr<<endl;
            } else {
                cerr<<endl;
                return false;
            }
        }
        cerr<<endl;
        if (not everyCellVisited()) { //this seems to rarely happen
            cerr<<"closed all paths but didn't explore all cells"<<endl;
            return false;
        }
        cerr<<"completed paths in "<<iter_count<<" iterations"<<endl;
        return true;
    }
};

int main() {
    //to make sure that a different random initial position is picked each run
    srand(time(NULL));
    Board b = Board::makeBoardFromInput();
    int attempt_count = 1;
    bool success = false;
    while (not success) {
        cout<<"ATTEMPT "<<attempt_count++<<endl;
        Board b2(b);
        success = b2.completePaths();
        if (success) {
            cout<<"SUCCESS!"<<endl;
            b2.print();
            cout<<"solution:"<<endl;
            b2.printSolution();
        } else {
            cout<<"FAIL!"<<endl;
            b2.print();
        }
    }
}
