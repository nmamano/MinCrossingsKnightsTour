#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <chrono> //random seed
#include <unordered_map>
using namespace std;

bool contains(const vector<int>& v, int val) {
  for (int vi : v) if (vi == val) return true;
  return false;
}
bool atLeast(int k, const vector<bool>& vb) {
  int count = 0;
  for (bool b : vb) if (b) count++;
  return count >= k;
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
  vector<Cell> cellsAtCol(int j) const {
    vector<Cell> res(0);
    for (int i = 0; i < NR; i++) res.push_back(at(i,j));
    return res;
  }
  bool goesOutsideBoard() const {
    for (auto cell : cellsAtCol(0))
      if (cell.goesLeft()) return true;
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
  static string drawApiSquare(double x0, double y0, double width, bool bg) {
    string sx0 = to_string(x0), sy0 = to_string(y0);
    if (!bg) return "rectangle("+sx0+","+sy0+","+to_string(x0+width)+
                    ","+to_string(y0-width)+",1,black)\n";
    return "filled_rectangle("+sx0+","+sy0+","+to_string(x0+width)+
                    ","+to_string(y0-width)+",1,black,gray)\n";
  }
  static string drawApiSegment(double x0, double y0, double x1, double y1) {
    string sx0 = to_string(x0), sy0 = to_string(y0), sx1 = to_string(x1), sy1 = to_string(y1);
    return "segment("+sx0+","+sy0+","+sx1+","+sy1+",3,black)\n";
  }
  static string drawApiRect(double x0, double y0, double x1, double y1) {
    string sx0 = to_string(x0), sy0 = to_string(y0), sx1 = to_string(x1), sy1 = to_string(y1);
    return "rectangle("+sx0+","+sy0+","+sx1+","+sy1+",2,black)\n";
  }
  string toDrawAPI(double yTop) const {
    string res = "";
    int w = 5;
    res += drawApiRect(0,yTop,2*w,yTop-3*w);
    res += drawApiSquare(0,yTop,w,false);
    res += drawApiSquare(w,yTop,w,false);
    res += drawApiSquare(0,yTop-w,w,false);
    res += drawApiSquare(w,yTop-w,w,false);
    res += drawApiSquare(0,yTop-2*w,w,false);
    res += drawApiSquare(w,yTop-2*w,w,false);

    double hw = (double)w/2.0;
    for (int i = 0; i < NR; i++) {
      for (int j = 0; j < NC; j++) {
        for (Move move : cells[i][j].getMoves()) {
          Pos des = addMove({i,j}, move);
          res += drawApiSegment(hw+j*w, yTop-hw-i*w, hw+des.j*w, yTop-hw-des.i*w);
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
          if (!contains(adjList[idx], idx2)) adjList[idx].push_back(idx2);
          if (!contains(adjList[idx2], idx)) adjList[idx2].push_back(idx);
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
  bool isValid() { return allNodeCellsHaveDeg(2) and hasValidDegrees() and not hasClosedCycles(); }
  int degree(int idx) const { return adjList[idx].size(); }
  bool allNodeCellsHaveDeg(int deg) {
    for (auto idx : nodeIndices())
      if (degree(idx) != deg) return false;
    return true;    
  }
  //no degree >= 3, at least 2 nodes with degree 1, even number with deg 1
  bool hasValidDegrees() {
    int deg1Count = 0;
    int degSum = 0;
    for (int idx = 0; idx < numNodes(); idx++) {
      int d = degree(idx);
      if (d > 2) return false;
      if (d == 1) deg1Count++;
      degSum += d;
    }
    return degSum%2 == 0 and deg1Count%2 == 0 and deg1Count>0;
  }
  int numNodesWithDeg(int deg) {
    int count = 0;
    for (int i = 0; i < numNodes(); i++) if (degree(i) == deg) count++;
    return count;
  }
  int numNonNodeCellsWithDeg(int deg) {
    if (deg == 2) return numNodesWithDeg(deg) - (singleNode ? 6 : 12);
    else return -1;
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
  for (auto cell : node.cellsAtCol(1)) res += cell.isTurn() ? 1 : 0;
  MoveGraph G(node);
  return res + G.numNonNodeCellsWithDeg(2); // any cell outside the node with deg 2 is a turn
}
int edgeWeight(const Node& top, const Node& bot) {
  //assuming (top bottom) is valid edge
  MoveGraph Gedge(top, bot), Gtop(top), Gbot(bot);
  return Gedge.numNonNodeCellsWithDeg(2) - Gtop.numNonNodeCellsWithDeg(2) - Gbot.numNonNodeCellsWithDeg(2);
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

bool isEdge(const Node& top, const Node& bottom) {
  if (not hasMatchingSharedEdges(top, bottom) or hasOversaturatedCells(top, bottom)) return false;
  MoveGraph G(top, bottom);
  return G.isValid();
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

void printNodeWeightDistr(const vector<Node>& nodes) {
  vector<int> dis(0);
  for (auto& node : nodes) {
    int w = nodeWeight(node);
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

double maxEdges(int numNodes) { return (double) numNodes * (double) numNodes; }

double approxNumEdges(const vector<Node>& nodes) {
  std::mt19937_64 RNG{static_cast<uint64_t> (std::chrono::steady_clock::now().time_since_epoch().count())};

  double numSamples = 10000000;
  int foundEdges = 0;
  int n = nodes.size();
  for (int i = 0; i < numSamples; i++) {
    if (isEdge(nodes[RNG()%n], nodes[RNG()%n])) foundEdges++;
  }
  double estDensity = foundEdges / numSamples;
  // cout<<foundEdges<<" "<<estDensity<<endl;
  return maxEdges(n) * estDensity;
}

void printEstimatedEgdeWeightDistr(const vector<Node>& nodes) {
  std::mt19937_64 RNG{static_cast<uint64_t> (std::chrono::steady_clock::now().time_since_epoch().count())};

  double numSamples = 1000000;
  vector<int> frqs;
  int n = nodes.size();
  int samples = 0;
  // bool printedHigh = false, printedLow = false;
  while (samples < numSamples) {
    int idx1 = RNG()%n, idx2 = RNG()%n;
    if (isEdge(nodes[idx1], nodes[idx2])) {
      samples++;
      int w = edgeWeight(nodes[idx1], nodes[idx2]);
      while ((int) frqs.size() <= w) frqs.push_back(0);
      frqs[w]++;
      // if (w >= 6 and not printedHigh) {
      //   cout <<"edge with w "<<w<<":"<<endl<<nodes[idx1].toStr()<<endl<<nodes[idx2].toStr()<<endl;
      //   printedHigh = true;
      // } else if (w == 0 and not printedLow) {
      //   cout <<"edge with w "<<w<<":"<<endl<<nodes[idx1].toStr()<<endl<<nodes[idx2].toStr()<<endl;
      //   printedLow = true;        
      // }
    }
  }
  cout <<"Edge weight distribution:"<<endl;
  for (size_t i = 0; i < frqs.size(); i++) {
    cout<<i<<": "<<frqs[i]<<" ("<<frqs[i]/(double) numSamples<<")"<<endl;
  }
}

void printOneNodeCycleDistr(const vector<Node>& nodes) {
  int numCycles = 0;
  vector<int> wToCount;
  for (const Node& node : nodes) {
    if (isEdge(node, node)) {
      numCycles++;
      int w = nodeWeight(node) + edgeWeight(node, node) + dist2Weight(node, node);
      while ((int)wToCount.size() <= w) wToCount.push_back(0); 
      wToCount[w]++;
      if (w == 5) {
        cout<<node.toStr()<<endl;
        cout<<node.toDrawAPI(75)<<node.toDrawAPI(60)<<node.toDrawAPI(45)<<node.toDrawAPI(30)<<endl;
        cout<<endl;
      }
    }
  }
  cout<<"Total number cycles of len 1: "<<numCycles<<endl;
  cout<<"Weight distribution:"<<endl;
  for (size_t i = 0; i < wToCount.size(); i++) {
    if (wToCount[i] != 0) cout<<i<<": "<<wToCount[i]<<endl;
  }
  cout<<endl;
}

vector<Node> nodesWithWeightAtMost(int deg, const vector<Node>& nodes) {
  vector<Node> res;
  for (const Node& node : nodes)
    if (nodeWeight(node) <= deg) res.push_back(node);
  return res;
}
void printTwoNodeCycleDistr(const vector<Node>& nodes) {
  vector<Node> nodes3 = nodesWithWeightAtMost(3, nodes);
  vector<Node> nodes34 = nodesWithWeightAtMost(4, nodes);
  int numCycles = 0;
  vector<int> wToCount;
  for (const Node& top : nodes3) {
    for (const Node& bot : nodes34) {
      if (isEdge(top,bot) and isEdge(bot,top)) {
        numCycles++;
        int w = nodeWeight(top)+nodeWeight(bot)+edgeWeight(top,bot)+edgeWeight(bot,top)
                    +dist2Weight(top,top)+dist2Weight(bot,bot);
        while ((int)wToCount.size() <= w) wToCount.push_back(0); 
        wToCount[w]++;
        if (w == 9) {
          cout<<nodeWeight(top)<<" "<<nodeWeight(bot)<<" "<<edgeWeight(top,bot)<<" "<<edgeWeight(bot, top)
                    <<" "<<dist2Weight(top,top)<<" "<<dist2Weight(bot,bot)<<endl;
          cout<<top.toStr()<<endl<<bot.toStr()<<endl;
          cout<<top.toDrawAPI(75)<<bot.toDrawAPI(60)<<top.toDrawAPI(45)<<bot.toDrawAPI(30)<<endl;
        }
      }
    }
  }
  cout<<"Total number cycles of len 2 of max node weight 7: "<<numCycles<<endl;
  cout<<"Weight distribution:"<<endl;
  for (size_t i = 0; i < wToCount.size(); i++) {
    if(wToCount[i]!=0)cout<<i<<": "<<wToCount[i]<<endl;
  }
  cout<<endl;
}

void printDegreeDistr(const vector<Node>& subset, const vector<Node>& nodes) {
  vector<int> degToCount(0);
  for (const Node& node : subset) {
    int deg = 0;
    for (const Node& nbr : nodes) {
      if (isEdge(node,nbr)) deg++;
    }
    while ((int)degToCount.size() <= deg) degToCount.push_back(0);
    degToCount[deg]++;
    cerr<<".";
  }
  cout<<endl<<"Number of nodes with degree:"<<endl;
  for (size_t i = 0; i < degToCount.size(); i++) {
    if(degToCount[i]!=0)cout<<i<<": "<<degToCount[i]<<endl;
  }
  cout<<endl;  
}

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
  counts.reserve(1640000);
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
      cout<<"group of 5:"<<endl;
      for (auto node : pool) {
        cout<<node.toStr();
        cout<<node.toDrawAPI(60);
        cout<<endl;
      }
    }
  }
  cout<<endl;  
}



int main() {
  vector<Node> nodes = genAllValidNodes();

  // int n = nodes.size();
  // cout<<"Num nodes:"<<endl<<n<<endl;

  // double m = approxNumEdges(nodes);
  // cout <<"Estimated num edges:"<<endl<<(long long) m<<endl;
  // double density = m/maxEdges(n);
  // cout <<"Estimated density:"<<endl<<density<<endl;
  
  // printNodeWeightDistr(nodes);
  // printEstimatedEgdeWeightDistr(nodes);

  cout<<"look at some nodes: "<<endl;
  // cout<<nodes[0].toStr()<<endl;
  cout<<nodes[0].toDrawAPI(30)<<endl;
  // for (int i = 0; i < 10; i++) {
  //   cout<<nodes[i].toStr()<<endl;
  // }

  printOneNodeCycleDistr(nodes);
  // printTwoNodeCycleDistr(nodes);

  // printDegreeDistr(nodesWithWeightAtMost(3, nodes), nodes);

  // printNodeSignatureStats(nodes);
}

