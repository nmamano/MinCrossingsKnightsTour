#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <chrono> //random seed
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
using namespace std;



/////////////////////////////////////
// basic utils
/////////////////////////////////////
bool contains(const vector<int>& v, int val) {
  for (int vi : v) if (vi == val) return true;
  return false;
}
bool atLeast(int k, const vector<bool>& vb) {
  int count = 0;
  for (bool b : vb) if (b) count++;
  return count >= k;
}

////////////////////////////////////////
// for caching preccomputed values directly in binary
/////////////////////////////////////

// template<class T>
// void writeMatrixToBinaryFile(const vector<vector<T> >& matrix, const string& fileName) {
//     uint n1 = matrix.size();
//     uint n2 = matrix[0].size();
//     ofstream fout(fileName.c_str(), ios::out | ios::binary);
//     for (uint i = 0; i < n1; i++) {
//         fout.write((char*)&matrix[i][0], n2*sizeof(T));
//     }
//     fout.close();
// }

// template<class T>
// void readMatrixFromBinaryFile(vector<vector<T> >& matrix, const string& fileName) {
//     uint n1 = matrix.size();
//     uint n2 = matrix[0].size();
//     ifstream fin(fileName.c_str(), ios::in | ios::binary);
//     for (uint i = 0; i < n1; i++) {
//         fin.read((char*)&matrix[i][0], n2*sizeof(T));
//     }
//     fin.close();
// }

/////////////////////////////////////
// Draw API helpers
/////////////////////////////////////

string drawApiSquare(double x0, double y0, double width, bool bg) {
  string sx0 = to_string(x0), sy0 = to_string(y0);
  if (!bg) return "rectangle("+sx0+","+sy0+","+to_string(x0+width)+
                  ","+to_string(y0-width)+",1,black)\n";
  return "filled_rectangle("+sx0+","+sy0+","+to_string(x0+width)+
                  ","+to_string(y0-width)+",1,whitesmoke,whitesmoke)\n";
}
string drawApiSegment(double x0, double y0, double x1, double y1,int w=3) {
  string sx0 = to_string(x0), sy0 = to_string(y0);
  string sx1 = to_string(x1), sy1 = to_string(y1);
  string sw = to_string(w);
  return "segment("+sx0+","+sy0+","+sx1+","+sy1+","+sw+",black)\n";
}
string drawApiRect(double x0, double y0, double x1, double y1) {
  string sx0 = to_string(x0), sy0 = to_string(y0), sx1 = to_string(x1), sy1 = to_string(y1);
  return "rectangle("+sx0+","+sy0+","+sx1+","+sy1+",2,black)\n";
}
string drawGrid() {
  string res = "";
  int w = 5;
  // for (int i = w; i < 100; i+=w) {
  //   res += drawApiSegment(i,0,i,100,1);
  //   res += drawApiSegment(0,i,100,i,1);
  // }
  int alt = 0;
  for (int i = 0; i <= 100; i+=w) {
    for (int j = 0; j <= 100; j+=w) {
      if (alt == 0) {
        if (i>=0 and j >= 0 and i<=100-w and j<=100) res += drawApiSquare(i,j,w,true);
      }
      alt = (alt+1)%2;
    }
  }
  return res;
}




enum Move { UUR, URR, DRR, DDR, DDL, UUL }; //double left moves never happen--too close to edge
vector<Move> allMoves() { return { UUR, URR, DRR, DDR, DDL, UUL }; }
vector<Move> allNonLeftMoves() { return { UUR, URR, DRR, DDR }; }
bool goesLeft(Move move) { return move == DDL or move == UUL; }
string moveToStr(Move move) {
  if(move==UUR)return"UUR"; if(move==URR)return"URR"; if(move==DRR)return"DRR";
  if(move==DDR)return"DDR"; if(move==DDL)return"DDL"; return "UUL";
}

struct Pos {
  int i, j;
  Pos(int i, int j):i(i),j(j){}
};
Pos addMove(Pos pos, Move move){
  int i = pos.i, j = pos.j;
  if(move==UUR)return{i-2,j+1}; if(move==URR)return{i-1,j+2}; if(move==DRR)return{i+1,j+2};
  if(move==DDR)return{i+2,j+1}; if(move==DDL)return{i+2,j-1}; return{i-2,j-1};
}

struct Cell {
  Move m1, m2;
  Cell(): m1(DDL), m2(DDL) {} //invalid init for default constructor
  Cell(Move m1, Move m2): m1(m1), m2(m2) {}
  vector<Move> getMoves() const {return {m1, m2}; }
  bool isValid() const { return m1 < m2; } //impose canonical order
  bool has(Move move) const { return m1 == move or m2 == move; }
  bool isTurn() const { return not ((has(UUR) and has(DDL)) or (has(UUL) and has(DDR))); }
  bool goesLeft() const { return ::goesLeft(m1) or ::goesLeft(m2); }
  string toStr() const { return "["+moveToStr(m1)+","+moveToStr(m2)+"]"; }
};
vector<Cell> allPossibleCellsAtCol(int j) {
  vector<Move> moves = (j == 0) ? allNonLeftMoves() : allMoves();
  vector<Cell> res(0);
  for (size_t i = 0; i < moves.size()-1; i++)
    for (size_t j = i+1; j < moves.size(); j++)
      res.push_back(Cell(moves[i], moves[j]));
  return res;
}

/*
Node is a group of 3x2 cells adjacent to the left edge of the board
board edge:
 | [0,0] [0,1] 
 | [1,0] [1,1]    
 | [2,0] [2,1] 
 */
struct Node {
  static constexpr int NR = 3, NC = 2; //num rows, num columns 
  Cell cells[NR][NC];
  Node() {}
  Node(const vector<Cell>& cells) { //list of NR*NC cells, sorted by rows
    int k = 0;
    for (int i = 0; i < NR; i++)
      for (int j = 0; j < NC; j++)
        this->cells[i][j] = cells[k++];
  }
  Cell at(int i, int j) const {
    if (i < 0 or j < 0 or i >= NR or j >= NC) cerr<<"wrong access"<<endl;
    return cells[i][j];
  }
  vector<Cell> cellsAtCol0() const { return {at(0,0),at(1,0),at(2,0)}; }
  vector<Cell> cellsAtCol1() const { return {at(0,1),at(1,1),at(2,1)}; }

  bool goesOutsideBoard() const {
    for (auto cell : cellsAtCol0()) if (cell.goesLeft()) return true;
    return false;
  }
  /* check for the following edges (a and b)
  | [ a ] [ b ]
  | [   ] [   ]
  | [ b ] [ a ]
  */
  bool hasMatchingSharedEdges() const {
    return at(0,0).has(DDR) == at(2,1).has(UUL) and //a
           at(0,1).has(DDL) == at(2,0).has(UUR);    //b
  }
  string toStr() const {
    string res;
    for (int i = 0; i < NR; i++)
      res+="| "+at(i,0).toStr()+at(i,1).toStr()+"\n";
    return res;
  }

  string toDrawAPI(double x,double y) const {
    string res = "";
    int w = 5;
    res += drawApiRect(x,y,x+2*w,y-3*w);
    res += drawApiSquare(x,y,w,false);
    res += drawApiSquare(x+w,y,w,false);
    res += drawApiSquare(x,y-w,w,false);
    res += drawApiSquare(x+w,y-w,w,false);
    res += drawApiSquare(x,y-2*w,w,false);
    res += drawApiSquare(x+w,y-2*w,w,false);

    double hw = (double)w/2.0;
    for (int i = 0; i < NR; i++) {
      for (int j = 0; j < NC; j++) {
        for (Move move : cells[i][j].getMoves()) {
          Pos des = addMove({i,j}, move);
          res += drawApiSegment(x+hw+j*w, y-hw-i*w, x+hw+des.j*w, y-hw-des.i*w);
        }
      }
    }
    return res;
  }
};



/* an adjacency list representation of a set of knight moves
has two options: single node graph, two adjacent nodes graph (top/bottom)
coordinates are mapped to indices first by rows and then by columns,
there's two rows before/after the node(s), and 2 columns to the right of the node(s)
since those squares may also be endpoints of a move starting at a node
Thus, the topleft cell of the node is mapped to index 8, as follows

For single node (brakets mean node cells):

 | ( 0 ) ( 1 ) ( 2 ) ( 3 ) 
 | ( 4 ) ( 5 ) ( 6 ) ( 7 ) 
 | [ 8 ] [ 9 ] (10 ) (11 ) top
 | [12 ] [13 ] (14 ) (15 ) top
 | [16 ] [17 ] (18 ) (19 ) top
 | (20 ) (21 ) (22 ) (23 ) 
 | (24 ) (25 ) (26 ) (27 ) 

or for double node:

 | ( 0 ) ( 1 ) ( 2 ) ( 3 ) 
 | ( 4 ) ( 5 ) ( 6 ) ( 7 ) 
 | [ 8 ] [ 9 ] (10 ) (11 )  top
 | [12 ] [13 ] (14 ) (15 )  top
 | [16 ] [17 ] (18 ) (19 )  top
 | [20 ] [21 ] (22 ) (23 )  bot
 | [24 ] [25 ] (26 ) (27 )  bot
 | [28 ] [29 ] (30 ) (31 )  bot
 | (32 ) (33 ) (34 ) (35 ) 
 | (36 ) (37 ) (38 ) (39 ) 
*/
struct MoveGraph {
  bool singleNode;
  vector<vector<int>> adjList;

  static int numCols() { return 4; }
  int numRows() const { return singleNode ? 7 : 10; }
  int numNodes() const { return numCols() * numRows(); }
  int coordsToIndex(Pos pos, bool isTop) const { return pos.i*4 + pos.j + (isTop ? 8 : 20); }
  vector<int> nodeIndices() const {
    if (singleNode) return {8, 9, 12, 13, 16, 17};
    return {8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29};
  }
  vector<int> nonNodeIndices() const {
    if (singleNode) return {0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27};
    return {0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39};
  }

  void addEdgesFromNode(const Node& node, bool isTop) {
    for (int i = 0; i < Node::NR; i++) {
      for (int j = 0; j < Node::NC; j++) {
        Pos pos = {i,j};
        int idx = coordsToIndex(pos, isTop);
        for (Move move : node.at(i,j).getMoves()) {
          int idx2 = coordsToIndex(addMove(pos, move), isTop);
          if (!contains(adjList[idx], idx2)) { //check case where other endpoint already added this edge
            adjList[idx].push_back(idx2);
            adjList[idx2].push_back(idx);
          }
        }
      }
    }    
  }
  MoveGraph(const Node& node): singleNode(true) {
    adjList = vector<vector<int>> (numNodes());
    addEdgesFromNode(node, true);
  }
  MoveGraph(const Node& top, const Node& bot): singleNode(false) {
    adjList = vector<vector<int>> (numNodes());
    addEdgesFromNode(top, true);
    addEdgesFromNode(bot, false);
  }
  bool isValid() { return allNodeCellsHaveDeg2() and hasValidDegrees() and not hasClosedCycles(); }
  int degree(int idx) const { return adjList[idx].size(); }
  bool allNodeCellsHaveDeg2() {
    for (auto idx : nodeIndices()) if (degree(idx) != 2) return false;
    return true;    
  }
  //no degree >= 3, at least 2 nodes with degree 1, even number with deg 1
  bool hasValidDegrees() {
    int deg1Count = 0;
    // int degSum = 0; //unnecessary check given the constructor works correctly
    for (int idx = 0; idx < numNodes(); idx++) {
      int d = degree(idx);
      if (d > 2) return false;
      if (d == 1) deg1Count++;
      // degSum += d;
    }
    return /*degSum%2 == 0 and*/ deg1Count%2 == 0 and deg1Count>0;
  }
  // int numNodesWithDeg(int deg) {
  //   int count = 0;
  //   for (int i = 0; i < numNodes(); i++) if (degree(i) == deg) count++;
  //   return count;
  // }
  int numNonNodeCellsWithDeg2() {
    int count = 0;
    for (int i : nonNodeIndices()) if (degree(i) == 2) count++;
    return count;
  }

  /* looks for invalid cycles like
    | [   ] [ 5 ] ( 2 )
    | [ 1 ] [   ]       ( 4 )
    | [   ] [ 3 ] ( 6 )
  */
  bool hasClosedCycles() {
    vector<bool> seen(numNodes(), false);
    for (int i = 0; i < numNodes(); i++) {
      if (degree(i) > 0 and !seen[i]) {
        vector<pair<int,int>> stk;
        stk.push_back({i, -1});
        seen[i] = true;
        while (!stk.empty()) {
          int node = stk.back().first, pred = stk.back().second;
          stk.pop_back();
          for (auto nbr : adjList[node]) {
            if (nbr != pred) {
              if (seen[nbr]) return true;
              seen[nbr] = true;
              stk.push_back({nbr,node});
            }
          }
        }
      }
    }
    return false;
  }
};

bool isValid(const Node& node) {
  if (node.goesOutsideBoard() or not node.hasMatchingSharedEdges()) return false;
  MoveGraph G(node);
  return G.isValid();
}

int nodeWeight(const Node& node) { //number of turns
  int res = 3; //cells at col 0 are always turns
  for (auto cell : node.cellsAtCol1()) res += cell.isTurn() ? 1 : 0;
  MoveGraph G(node);
  return res + G.numNonNodeCellsWithDeg2(); // any cell outside the node with deg 2 is a turn
}

int dist2Weight(const Node& top, const Node& bot) {
  return (top.at(2,1).has(DDR) and bot.at(0,1).has(UUR)) ? 1 : 0;
}
/* check for the following edges (a--d)
| [   ] [   ] top
| [ a ] [ b ] 
| [ c ] [ d ] 
| [ b ] [ a ] bottom
| [ d ] [ c ] 
| [   ] [   ] 
*/
bool hasMatchingSharedEdges(const Node& top, const Node& bot) {
  return top.at(1,0).has(DDR) == bot.at(0,1).has(UUL) and //a
         top.at(1,1).has(DDL) == bot.at(0,0).has(UUR) and //b
         top.at(2,0).has(DDR) == bot.at(1,1).has(UUL) and //c
         top.at(2,1).has(DDL) == bot.at(1,0).has(UUR);    //d
}

/*
possible over-saturated cells:
| [ a ] [ b ]         top
| [ b ] [ c ] [ A ]   top
| [ ac] [ d ] [ B ]   top
| [ bd] [ a ] [ C ]   bottom
| [ c ] [ b ] [ D ]   bottom
| [ d ] [ c ]         bottom
*/
bool hasOversaturatedCells(const Node& top, const Node& bot) {
  return 
    atLeast(3, {top.at(0,0).has(DRR), top.at(2,0).has(URR), bot.at(0,1).has(UUR)}) or                       //A
    atLeast(3, {top.at(0,1).has(DDR), top.at(1,0).has(DRR), bot.at(0,0).has(URR), bot.at(1,1).has(UUR)}) or //B
    atLeast(3, {top.at(1,1).has(DDR), top.at(2,0).has(DRR), bot.at(1,0).has(URR), bot.at(2,1).has(UUR)}) or //C
    atLeast(3, {top.at(2,1).has(DDR), bot.at(0,0).has(DRR), bot.at(2,0).has(URR)});                         //D
}

bool isEdge(const Node& top, const Node& bottom) { //obsolete, use edgeWeight
  if (not hasMatchingSharedEdges(top, bottom) or hasOversaturatedCells(top, bottom)) return false;
  MoveGraph G(top, bottom);
  return G.isValid();
}
int edgeWeight(const Node& top, const Node& bot) { //returns -1 if it's not an edge
  //quick checks for efficiency
  if (not hasMatchingSharedEdges(top, bot) or hasOversaturatedCells(top, bot)) return -1;
  MoveGraph Gedge(top, bot);
  if (!Gedge.isValid()) return -1; //complete check
  MoveGraph Gtop(top), Gbot(bot); 
  return Gedge.numNonNodeCellsWithDeg2() - Gtop.numNonNodeCellsWithDeg2() - Gbot.numNonNodeCellsWithDeg2();
}

void genAllValidNodesRec(vector<Cell>& currState, vector<Node>& res) {
  if (currState.size() == 6) {
    Node node(currState);
    if (isValid(node)) res.push_back(node);
    return;
  } else {
    for (Cell cell : allPossibleCellsAtCol(currState.size()%2)) {
      currState.push_back(cell);
      genAllValidNodesRec(currState, res);
      currState.pop_back();
    }    
  }
}

vector<Node> genAllValidNodes() {
  vector<Cell> currState(0);
  vector<Node> res(0);
  res.reserve(182250); //num nodes
  genAllValidNodesRec(currState, res);
  return res;
}




////////////////////////////////////////////////////////
// signatures
////////////////////////////////////////////////////////

//a bit vector based on the non-node cells reached
unsigned long long nodeSignature(const Node& node) {
  MoveGraph G(node);
  unsigned long long res = 0;
  for (int i : G.nonNodeIndices()) {
    res = res<<2;
    res += G.degree(i);
  }
  return res;
}

void printNodeSignatureStats(const vector<Node>& nodes) {
  unordered_map<unsigned long long,int> counts;
  unordered_map<unsigned long long,vector<Node>> pools;
  counts.reserve(164000);
  for (const Node& node : nodes) {
    auto sig = nodeSignature(node);
    counts[sig]++;
    pools[sig].push_back(node);
  } 
  cout <<"Number different signatures"<<endl;
  cout <<counts.size()<<endl;
  vector<int> dis;
  for (const Node& node : nodes) {
    auto sig = nodeSignature(node);
    int poolSize = counts[sig];
    while ((int)dis.size() <= poolSize) dis.push_back(0);
    dis[poolSize]++;
  }
  cout<<endl<<"Number of nodes with signature shared among i nodes:"<<endl;
  for (size_t i = 0; i < dis.size(); i++) {
    if(dis[i]!=0)cout<<i<<": "<<dis[i]<<endl;
  }

  for (auto kv : pools) {
    vector<Node> pool = kv.second;
    if (pool.size()==5) {
      cout<<"GROUP of 5:)"<<endl<<endl;
      cout<<drawGrid()<<endl;
      int x=0;
      for (auto node : pool) {
        // cout<<node.toStr()<<endl;
        cout<<node.toDrawAPI(x,50)<<endl;
        x+= 20;
      }
      return;
    }
  }
}

vector<Node> pruneSameSignature(const vector<Node>& nodes) {
  unordered_map<unsigned long long,int> counts;
  unordered_map<unsigned long long,vector<Node>> pools;
  counts.reserve(164000);
  for (const Node& node : nodes) {
    auto sig = nodeSignature(node);
    counts[sig]++;
    pools[sig].push_back(node);
  } 
  vector<Node> res;
  res.reserve(164000);
  for (auto kv : pools) {
    vector<Node> pool = kv.second;
    Node minNode = pool[0];
    int minTurns = nodeWeight(minNode);
    for (auto node : pool) {
      int numTurns = nodeWeight(minNode);
      if (numTurns < minTurns) {
        minTurns = numTurns;
        minNode = node;
      }
    }
    res.push_back(minNode);
  }
  return res;
}



struct ConfGraph {
  vector<Node> nodes; //may be before or after prunning

  //cached stuff to avoid recomputing
  vector<MoveGraph> moveGraphs; 
  vector<int> nodeWeights;
  vector<int> cachedNumNonNodeCellsWithDeg2; //used in computations of node and edge weights
  
  double maxEdges() const { return nodes.size() * nodes.size(); }
  int size() const { return nodes.size(); }

  ConfGraph() {
    nodes = genAllValidNodes();
    //prune ?
    nodes = pruneSameSignature(nodes);

    int n = nodes.size();

    //compute cached stuff
    moveGraphs.reserve(n);
    nodeWeights.reserve(n);
    cachedNumNonNodeCellsWithDeg2.reserve(n);
    for (int i = 0; i < n; i++) {
      moveGraphs.push_back(MoveGraph(nodes[i]));
      cachedNumNonNodeCellsWithDeg2.push_back(moveGraphs[i].numNonNodeCellsWithDeg2());
      //compute node weights (see nodeWeight function above to see where this comes from)
      nodeWeights.push_back(3 + cachedNumNonNodeCellsWithDeg2[i]);
      for (const Cell& cell : nodes[i].cellsAtCol1()) if (cell.isTurn()) nodeWeights[i]++;
    }
  }

  int edgeW(int topi, int boti) const {
    //quick checks before constructing move graph:
    if (not hasMatchingSharedEdges(nodes[topi], nodes[boti]) or hasOversaturatedCells(nodes[topi], nodes[boti])) return -1;

    MoveGraph Gedge(nodes[topi], nodes[boti]);
    if (!Gedge.isValid()) return -1; //complete check
    return Gedge.numNonNodeCellsWithDeg2()-cachedNumNonNodeCellsWithDeg2[topi]-cachedNumNonNodeCellsWithDeg2[boti];
  }
  bool isEdg(int topi, int boti) const {
    //quick checks before constructing move graph:
    if (not hasMatchingSharedEdges(nodes[topi], nodes[boti]) or hasOversaturatedCells(nodes[topi], nodes[boti])) return false;

    MoveGraph Gedge(nodes[topi], nodes[boti]);
    return Gedge.isValid(); //complete check
  }


};


void printNodeWeightDistr(const ConfGraph& CF) {
  vector<int> dis(0);
  for (int w : CF.nodeWeights) {
    while ((int) dis.size() <= w) dis.push_back(0);
    dis[w]++;
    // if (w == 3 or w == 10) {
    //   cout <<"node with w "<<w<<":"<<endl<<node.toStr()<<endl<<endl;
    // }
  }
  cout<<"Node weight distribution:"<<endl;
  for (int i = 0;i < (int)dis.size(); i++){
    if (dis[i]!=0)cout<<i<<": "<<dis[i]<<endl;
  }
}



void printApproxNumEdges(const ConfGraph& CF) {
  std::mt19937_64 RNG{static_cast<uint64_t> (std::chrono::steady_clock::now().time_since_epoch().count())};

  double numSamples = 10000000;
  int foundEdges = 0;
  int n = CF.nodes.size();
  for (int i = 0; i < numSamples; i++) {
    if (CF.isEdg(RNG()%n, RNG()%n)) foundEdges++;
  }
  double estDensity = foundEdges / numSamples;
  double estNumEdges = CF.maxEdges() * estDensity;
  cout <<"Estimated num edges: "<<endl<<(long long)estNumEdges<<endl;
  cout <<"Estimated density: "<<endl<<estDensity<<endl;

}

void printEstimatedEgdeWeightDistr(const ConfGraph& CF) {
  std::mt19937_64 RNG{static_cast<uint64_t> (std::chrono::steady_clock::now().time_since_epoch().count())};

  double numSamples = 1000000;
  vector<int> frqs;
  int n = CF.nodes.size();
  int samples = 0;
  // bool printedHigh = false, printedLow = false;
  while (samples < numSamples) {
    int idx1 = RNG()%n, idx2 = RNG()%n;
    if (CF.isEdg(idx1, idx2)) {
      samples++;
      int w = CF.edgeW(idx1, idx2);
      while ((int) frqs.size() <= w) frqs.push_back(0);
      frqs[w]++;
      // if (w >= 6 and not printedHigh) {
      //   cout <<"edge with w "<<w<<":"<<endl<<CF.nodes[idx1].toStr()<<endl<<CF.nodes[idx2].toStr()<<endl;
      //   printedHigh = true;
      // } else if (w == 0 and not printedLow) {
      //   cout <<"edge with w "<<w<<":"<<endl<<CF.nodes[idx1].toStr()<<endl<<CF.nodes[idx2].toStr()<<endl;
      //   printedLow = true;        
      // }
    }
  }
  cout <<"Edge weight distribution:"<<endl;
  for (size_t i = 0; i < frqs.size(); i++) {
    cout<<i<<": "<<frqs[i]<<" ("<<frqs[i]/(double) numSamples<<")"<<endl;
  }
}

void printOneNodeCycleDistr(const ConfGraph& CF) {
  int numLoops = 0;
  vector<int> wToCount;
  for (int i = 0; i < CF.size(); i++) {
    if (CF.isEdg(i, i)) {
      numLoops++;
      int w = CF.nodeWeights[i] + CF.edgeW(i, i) + dist2Weight(CF.nodes[i], CF.nodes[i]);
      while ((int)wToCount.size() <= w) wToCount.push_back(0); 
      wToCount[w]++;
      // if (w == 5) {
      //   cout<<node.toStr()<<endl;
      //   cout<<node.toDrawAPI(75)<<node.toDrawAPI(60)<<node.toDrawAPI(45)<<node.toDrawAPI(30)<<endl;
      //   cout<<endl;
      // }
    }
  }
  cout<<"Total number cycles of len 1: "<<numLoops<<endl;
  cout<<"Weight distribution:"<<endl;
  for (size_t i = 0; i < wToCount.size(); i++) {
    if (wToCount[i] != 0) cout<<i<<": "<<wToCount[i]<<endl;
  }
  cout<<endl;
}

vector<int> nodesWithWeightAtMost(const ConfGraph& CF, int w) {
  vector<int> res;
  for (int i = 0; i < CF.size(); i++) if (CF.nodeWeights[i] <= w) res.push_back(i);
  return res;
}

// void printTwoNodeCycleDistr(const vector<Node>& nodes) {
//   vector<Node> nodes3 = nodesWithWeightAtMost(3, nodes);
//   vector<Node> nodes34 = nodesWithWeightAtMost(4, nodes);
//   int numCycles = 0;
//   vector<int> wToCount;
//   for (const Node& top : nodes3) {
//     for (const Node& bot : nodes34) {
//       if (isEdge(top,bot) and isEdge(bot,top)) {
//         numCycles++;
//         int w = nodeWeight(top)+nodeWeight(bot)+edgeWeight(top,bot)+edgeWeight(bot,top)
//                     +dist2Weight(top,top)+dist2Weight(bot,bot);
//         while ((int)wToCount.size() <= w) wToCount.push_back(0); 
//         wToCount[w]++;
//         // if (w == 9) {
//         //   cout<<nodeWeight(top)<<" "<<nodeWeight(bot)<<" "<<edgeWeight(top,bot)<<" "<<edgeWeight(bot, top)
//         //             <<" "<<dist2Weight(top,top)<<" "<<dist2Weight(bot,bot)<<endl;
//         //   cout<<top.toStr()<<endl<<bot.toStr()<<endl;
//         //   cout<<top.toDrawAPI(75)<<bot.toDrawAPI(60)<<top.toDrawAPI(45)<<bot.toDrawAPI(30)<<endl;
//         // }
//       }
//     }
//   }
//   cout<<"Total number cycles of len 2 of max node weight 7: "<<numCycles<<endl;
//   cout<<"Weight distribution:"<<endl;
//   for (size_t i = 0; i < wToCount.size(); i++) {
//     if(wToCount[i]!=0)cout<<i<<": "<<wToCount[i]<<endl;
//   }
//   cout<<endl;
// }


vector<int> dijkstra(const ConfGraph& CF, int src) {
  int INF = 9999;

  vector<int> res(CF.size(), INF);
  res[src] = CF.nodeWeights[src];
  set<pair<int,int>> PQ;
  PQ.insert({res[src],src});
  
  // int iter = 0;
  while (!PQ.empty()) {
    int node = PQ.begin()->second;
    PQ.erase(PQ.begin());
    // int num_updates = 0;
    for (int nbr = 0; nbr < CF.size(); nbr++) {
      int totalW = res[node] + CF.nodeWeights[nbr]; //still missing the weight of the edge node->nbr 
      if (res[nbr] <= totalW) continue; //this also prunes the case node==nbr
      int edgeW = CF.edgeW(node,nbr);
      if (edgeW == -1) continue; //not an edge
      totalW += edgeW;
      if (res[nbr] > totalW) {
        if (res[nbr] < INF) {
          PQ.erase(PQ.find({res[nbr], nbr}));
        }
        res[nbr] = totalW;
        PQ.insert({res[nbr], nbr});
        // num_updates++;
      }
    }
    // cerr<<iter<<": node "<<node<<" weight "<<res[node]<<" updates "<<num_updates<<" PQ size "<<PQ.size()<<endl;
    // iter++;
  }
  // for (int i = 0; i < CF.size(); i++){
  //   cout<<res[i]<<endl;
  // }
  return res;
}

void printDistDistrFromNode(const ConfGraph& CF, int src) {
  vector<int> dists = dijkstra(CF, src);
  vector<int> distr(0);
  for (int dist : dists) {
    while ((int)distr.size()<dist)distr.push_back(0);
    distr[dist]++;
  }
  cout<<"Nodes at distance i from src:"<<endl;
  for (size_t i = 0; i < distr.size(); i++) {
    if(distr[i]!=0)cout<<i<<": "<<distr[i]<<endl;
  }
}

void printDegreeDistrSubset(const vector<int>& subset, const ConfGraph& CF) {
  int k = subset.size();
  vector<int> inDegs(k,0), outDegs(k,0);
  int idx = 0;
  for (int i : subset) {
    for (int j = 0; j < CF.size(); j++) {
      if (CF.isEdg(i,j)) outDegs[idx]++;
      if (CF.isEdg(j,i)) inDegs[idx]++;
    }
    idx++;
  }

  cout<<"In degrees in subset:"<<endl;
  for (int i = 0; i < k; i++) cout<<inDegs[i]<<endl;
  cout<<"Out degrees in subset:"<<endl;
  for (int i = 0; i < k; i++) cout<<outDegs[i]<<endl;
  
  vector<int> inDis(0), outDis(0);
  for (int inDeg : inDegs) {
    while ((int)inDis.size() <= inDeg) inDis.push_back(0);
    inDis[inDeg]++;
  }
  for (int outDeg : outDegs) {
    while ((int)outDis.size() <= outDeg) outDis.push_back(0);
    outDis[outDeg]++;
  }

  cout<<"Number of nodes in subset with in degree:"<<endl;
  for (size_t i = 0; i < inDis.size(); i++) {
    if(inDis[i]!=0)cout<<i<<": "<<inDis[i]<<endl;
  }
  cout<<"Number of nodes in subset with out degree:"<<endl;
  for (size_t i = 0; i < outDis.size(); i++) {
    if(outDis[i]!=0)cout<<i<<": "<<outDis[i]<<endl;
  }

}

void printDegreeDistr(const ConfGraph& CF) {
  int n = CF.size();
  vector<int> inDegs(n, 0), outDegs(n, 0);
  for (int i = 0; i < n; i++) {
    if (i%100 == 0) cerr<<'.';
    for (int j = i; j < n; j++) {
      if (CF.isEdg(i, j)) {
        outDegs[i]++;
        inDegs[j]++;
      }
      if (i != j and CF.isEdg(j, i)) {
        outDegs[j]++;
        inDegs[i]++;
      }
    }
  }
  vector<int> inDis(0), outDis(0);
  for (int i = 0; i < n; i++) {
    while ((int)inDis.size() <= inDegs[i]) inDis.push_back(0);
    inDis[inDegs[i]]++;
    while ((int)outDis.size() <= outDegs[i]) outDis.push_back(0);
    outDis[outDegs[i]]++;
  }
  cout<<endl<<"Number of nodes with in-degree:"<<endl;
  for (size_t i = 0; i < inDis.size(); i++) {
    if(inDis[i]!=0)cout<<i<<": "<<inDis[i]<<endl;
  }  
  cout<<endl<<"Number of nodes with out-degree:"<<endl;
  for (size_t i = 0; i < outDis.size(); i++) {
    if(outDis[i]!=0)cout<<i<<": "<<outDis[i]<<endl;
  }  
}

void printSomeNodes(const ConfGraph& CF) {
  cout<<"look at some nodes: "<<endl;
  cout<<CF.nodes[0].toStr()<<endl;
  cout<<CF.nodes[0].toDrawAPI(0, 30)<<endl;
  for (int i = 0; i < 10; i++) {
    cout<<CF.nodes[i].toStr()<<endl;
  }
}

int main() {
  ConfGraph CF;

  cout<<"Num nodes:"<<endl<<CF.size()<<endl;


  //printSomeNodes(CF);


  // printNodeWeightDistr(CF);
  // printApproxNumEdges(CF);  
  // printEstimatedEgdeWeightDistr(CF);

  
  // printOneNodeCycleDistr(CF);


  // printDegreeDistrSubset(nodesWithWeightAtMost(CF, 3), CF);
  // printDegreeDistr(CF); //too slow

  // printDistDistrFromNode(CF, 0);
  
  // printNodeSignatureStats(nodes);

  // dijkstra(nodes, 0);

}

