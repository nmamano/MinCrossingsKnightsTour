// tm.cpp - transfer-matrix search for periodic edge gadgets (KT Edge Searcher, 2026-10-02).
//
// Same model as kt/strip.py: a band of depth D along one board edge, plain knight lines
// x + 2y = c outside it. Sweep coordinate a, depth coordinate b (0 <= b < D):
//   bottom: (x, y) = (a, b);  left: (x, y) = (b, a).
// Every band cell has degree 2. Terminal cells keep one fixed line edge to the outside.
// Strands (terminal to terminal) must join lane 2j to lane 2j+1, lane = floor((c - off)/s).
// No cycles; strand extent bounded by drift limits W (lanes) and W2 (columns) -> finite strands.
//
// The sweep processes one column at a time. State = pending edges that cross the cut,
// plus a label per pending end (terminal lane, or partner end + anchor column), plus phase.
// Each periodic gadget = a cycle in the state graph; cost per column = wX*crossings + wT*turns.
// Seeds: every capacity-valid cut with all ends labelled F ("unknown past", no checks). The F
// label only propagates and never gets created, so every state of every valid periodic gadget is
// reached (its strands are finite), and the analysis graph uses only F-free states, whose
// transitions are exact. Min mean cycle (Howard) = best rate over ALL periods, given the
// drift limits. Witness cycle is printed as a template.
//
// usage: tm kind D s off wX wT W W2 [maxstates]
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

static int floordiv(int a, int b) { return (a >= 0) ? a / b : -((-a + b - 1) / b); }

string KIND; int D, S, OFF, WX, WT, W, W2, PH;
int La, Lb;                       // fixed (line) edge direction from a terminal, in (a,b)
const int FMa[4] = {1, 1, 2, 2}, FMb[4] = {2, -2, 1, -1};
int NS;                           // number of slots
struct Slot { int off, b, m, ta, tb; };   // source (c+off, b), move m, target (c+ta, tb)
vector<Slot> slots;
int slotId[3][16][4];             // [off+2][b][m]
bool term[16];

int lineOf(int a, int b) { return KIND == "bottom" ? a + 2 * b : b + 2 * a; }
int laneOf(int a, int b) { return floordiv(lineOf(a, b) - OFF, S); }
int refLane(int a) { return laneOf(a, 0); }   // lane of cell (a, 0)
// pairing rule mode (env RULE="M:r/d,r/d,..."): labels are LINES, strand {c<c'} allowed iff (c mod M, c'-c) listed
int UNIONQ = -1;   // env UNION=q: forbid finite cycles of (this matching) U (left pairs {c,c+3}, c = q mod 2); bottom only
int RULEM = 0; bool ALLOWED[64][128]; int MINTERM = 0;   // T labels below MINTERM - W become wildcards
int labOf(int a, int b) { return RULEM ? lineOf(a, b) : laneOf(a, b); }
int refLab(int a) { return labOf(a, 0); }
bool pairOK(int L1, int L2) {
    if (RULEM) { int lo = min(L1, L2), d = abs(L1 - L2); return d > 0 && d < 128 && ALLOWED[((lo % RULEM) + RULEM) % RULEM][d]; }
    return floordiv(L1, 2) == floordiv(L2, 2) && L1 != L2;
}

// geometry: proper crossing of open segments (same as kt/core.py seg_cross)
int orient(ll px, ll py, ll qx, ll qy, ll rx, ll ry) {
    ll v = (qy - py) * (rx - qx) - (qx - px) * (ry - qy);
    return v == 0 ? 0 : (v > 0 ? 1 : 2);
}
bool segCross(int a1, int b1, int a2, int b2, int c1, int d1, int c2, int d2) {
    if ((a1 == c1 && b1 == d1) || (a1 == c2 && b1 == d2) || (a2 == c1 && b2 == d1) || (a2 == c2 && b2 == d2)) return false;
    int o1 = orient(a1, b1, a2, b2, c1, d1), o2 = orient(a1, b1, a2, b2, c2, d2);
    int o3 = orient(c1, d1, c2, d2, a1, b1), o4 = orient(c1, d1, c2, d2, a2, b2);
    return o1 && o2 && o3 && o4 && o1 != o2 && o3 != o4;
}
int crossF[16][4];               // new edge (0,b,m) vs all fixed edges
int crossN[16][4][16][4];        // new edge vs new edge (same column)
int crossP[16][4][16][4];        // new edge (0,b,m) vs old pending (-1,b2,m2) with dx=2

// ---------------- state ----------------
// key: phase(1) mask(8) then per set slot: lab(1) anc(1)
// lab: 0..63 partner slot id; 64+ (r+64) terminal rel lane r (r in [-63,63]) -> stored as 128 + r
struct St { int ph; int age; uint64_t mask; int lab[64]; int anc[64]; int uL[3]; };   // lab: <64 partner, 64 = F (unknown past), 160+r = terminal rel lane r
const int LF = 64, LT = 160;
int AGEMAX;
string enc(const St& s) {
    string k; k.push_back((char)s.ph); k.push_back((char)s.age);
    for (int i = 0; i < 8; i++) k.push_back((char)((s.mask >> (8 * i)) & 255));
    for (int i = 0; i < NS; i++) if (s.mask >> i & 1) { k.push_back((char)s.lab[i]); k.push_back((char)s.anc[i]); }
    for (int j = 0; j < 3; j++) k.push_back((char)s.uL[j]);
    return k;
}
St dec(const string& k) {
    St s; s.ph = (unsigned char)k[0]; s.age = (unsigned char)k[1]; s.mask = 0;
    for (int i = 0; i < 8; i++) s.mask |= (uint64_t)(unsigned char)k[2 + i] << (8 * i);
    int p = 10;
    for (int i = 0; i < NS; i++) if (s.mask >> i & 1) { s.lab[i] = (unsigned char)k[p]; s.anc[i] = (signed char)k[p + 1]; p += 2; }
    for (int j = 0; j < 3; j++) s.uL[j] = (unsigned char)k[p + j];
    return s;
}

// compact key store: arena + open addressing
struct KeyStore {
    vector<uint8_t> arena; vector<uint64_t> offs{0}; vector<int> table; uint64_t msk;
    KeyStore() { table.assign(1 << 20, -1); msk = (1 << 20) - 1; }
    size_t size() const { return offs.size() - 1; }
    static uint64_t h(const string& k) { uint64_t x = 1469598103934665603ULL; for (unsigned char c : k) { x ^= c; x *= 1099511628211ULL; } return x ^ (x >> 29); }
    string get(int id) const { return string((const char*)&arena[offs[id]], offs[id + 1] - offs[id]); }
    bool eq(int id, const string& k) const { size_t n = offs[id + 1] - offs[id]; return n == k.size() && memcmp(&arena[offs[id]], k.data(), n) == 0; }
    int find(const string& k) const { uint64_t i = h(k) & msk; while (table[i] >= 0) { if (eq(table[i], k)) return table[i]; i = (i + 1) & msk; } return -1; }
    int insert(const string& k, bool& isNew) {
        if (2 * (size() + 1) > table.size()) grow();
        uint64_t i = h(k) & msk; while (table[i] >= 0) { if (eq(table[i], k)) { isNew = false; return table[i]; } i = (i + 1) & msk; }
        int id = size(); table[i] = id; arena.insert(arena.end(), k.begin(), k.end()); offs.push_back(arena.size()); isNew = true; return id;
    }
    void grow() {
        table.assign(table.size() * 2, -1); msk = table.size() - 1;
        for (int id = 0; id < (int)size(); id++) { uint64_t i = h(get(id)) & msk; while (table[i] >= 0) i = (i + 1) & msk; table[i] = id; }
    }
};
KeyStore KS;
vector<int> fidx, fid2id;          // F-free states get a dense index (analysis graph nodes)
struct Tr { int to; int cost; int X, T; };
vector<vector<Tr>> G;              // over F-free indices
int RELAX = 1, NOLANE = 0;
bool hasF0(const St& s) { for (int i = 0; i < NS; i++) if ((s.mask >> i & 1) && s.lab[i] == LF) return true; return false; }
bool hasF(const St& s) { return RELAX ? false : hasF0(s); }

// transition enumeration. callback(newState, X, T, chosen new edges list)
struct Ctx {
    const St* s; int c;           // c = representative column = phase
    int inc[16][2], ninc[16], need[16];
    int cap1[16], cap2[16];
    vector<pair<int,int>> chosen; // (b, m)
    int X, T;
};
int DBG = 0; uint64_t DBGMASK = 0;
#define FAIL(msg) do { if (dbgOn) fprintf(stderr, "   reject: %s\n", msg); return; } while (0)

template <class F>
void finish(Ctx& C, F& cb) {
    const St& s = *C.s;
    bool dbgOn = false;
    if (DBG) {
        uint64_t wm = 0;
        for (int i = 0; i < NS; i++) if ((s.mask >> i & 1) && slots[i].off == -1 && FMa[slots[i].m] == 2) wm |= 1ULL << slotId[0][slots[i].b][slots[i].m];
        for (auto& pr : C.chosen) wm |= 1ULL << slotId[1][pr.first][pr.second];
        dbgOn = (wm == DBGMASK);
    }
    // build graph of ends
    int nodes = 0;
    // node ids: old slots 0..NS-1, new slots NS..2NS-1, T nodes from 2NS
    static int eu[512], ev[512], eanc[512]; int ne = 0;
    static int inc_e[256][2], ndeg[256], tlane[256], isF[256], torig[256];
    for (int i = 0; i < 2 * NS + 2 * D + 70; i++) ndeg[i] = 0;
    int nT = 2 * NS;
    auto link = [&](int u, int v, int anc) {
        eu[ne] = u; ev[ne] = v; eanc[ne] = anc;
        inc_e[u][ndeg[u]++] = ne; inc_e[v][ndeg[v]++] = ne; ne++;
    };
    const int BIG = 1000;
    for (int i = 0; i < NS; i++) if (s.mask >> i & 1) {
        if (s.lab[i] == LF) { isF[nT] = 1; link(i, nT, BIG); nT++; }
        else if (s.lab[i] > LF) { isF[nT] = 0; torig[nT] = i; tlane[nT] = s.lab[i] - LT; link(i, nT, BIG); nT++; }
        else if (i < s.lab[i]) link(i, s.lab[i], s.anc[i]);
    }
    // new slot ids in new frame: (off=-1, b, m) ; old kept (off=-1, dx=2) -> (off=-2, b, m)
    vector<int> isNewEnd(2 * NS, 0);
    for (int b = 0; b < D; b++) {
        int items[3], k = 0;
        for (int j = 0; j < C.ninc[b]; j++) items[k++] = C.inc[b][j];
        for (auto& pr : C.chosen) if (pr.first == b) { int id = NS + slotId[1][b][pr.second]; items[k++] = id; isNewEnd[id] = 1; }
        if (term[b]) { isF[nT] = 0; torig[nT] = -1; tlane[nT] = labOf(C.c, b) - refLab(C.c); items[k++] = nT++; }
        if (k != 2) { fprintf(stderr, "bad degree\n"); exit(1); }
        link(items[0], items[1], 0);
    }
    // ends of new state
    vector<int> ends;
    for (int i = 0; i < NS; i++) if ((s.mask >> i & 1) && slots[i].off == -1 && FMa[slots[i].m] == 2) ends.push_back(i);
    for (int i = NS; i < 2 * NS; i++) if (isNewEnd[i]) ends.push_back(i);
    // walk
    static int visE[512]; for (int e = 0; e < ne; e++) visE[e] = 0;
    St t; t.ph = (s.ph + 1) % PH; t.mask = 0; bool anyF = false;
    int shift = refLab(C.c + 1) - refLab(C.c);
    auto newSlot = [&](int node) {
        if (node >= NS) return slotId[1][slots[node - NS].b][slots[node - NS].m];
        return slotId[0][slots[node].b][slots[node].m];
    };
    auto isEndNode = [&](int u) { return u >= 2 * NS || (u < 2 * NS && ndeg[u] == 1); };
    vector<int> done(2 * NS + 2 * D + 70, 0);
    int refPar = refLab(C.c);
    auto walk = [&](int start, int& other, int& anc) {
        int u = start, e = inc_e[u][0]; anc = BIG;
        while (true) {
            visE[e] = 1; anc = min(anc, eanc[e]);
            int v = eu[e] == u ? ev[e] : eu[e];
            if (ndeg[v] == 1) { other = v; return; }
            int e2 = inc_e[v][0] == e ? inc_e[v][1] : inc_e[v][0];
            u = v; e = e2;
        }
    };
    // union events (UNIONQ mode): half nodes 0..63 old B-halves (old slot id), 64..66 old L-halves
    // (line t-k), 67 new line B-half, 68 new line L-half, 70+ INF nodes
    int nInf = 70; vector<pair<int,int>> ulinks; int newHalf[64]; for (int i = 0; i < 64; i++) newHalf[i] = -1;
    auto halfOf = [&](int tn) { return torig[tn] >= 0 ? torig[tn] : 67; };
    // T nodes as starts as well
    for (int u = 2 * NS; u < nT; u++) {
        if (done[u]) continue;
        int o, anc; walk(u, o, anc); done[u] = 1; done[o] = 1;
        if (o >= 2 * NS) {   // T - T strand: check pairing (no check if one side has unknown past)
            if (UNIONQ >= 0) {
                if (!isF[u] && !isF[o]) ulinks.push_back({halfOf(u), halfOf(o)});
                else if (!isF[u]) ulinks.push_back({halfOf(u), nInf++});
                else if (!isF[o]) ulinks.push_back({halfOf(o), nInf++});
            }
            if (isF[u] || isF[o] || NOLANE) continue;
            int L1 = tlane[u] + refPar, L2 = tlane[o] + refPar;
            if (!pairOK(L1, L2)) FAIL("pairing");
        } else if (isF[u]) {
            int ns = newSlot(o); t.mask |= 1ULL << ns; t.lab[ns] = LF; t.anc[ns] = 0; anyF = true;
        } else {
            int r = NOLANE ? 0 : tlane[u] - shift;
            int ns = newSlot(o); t.mask |= 1ULL << ns; t.anc[ns] = 0;
            if (r < MINTERM - W) { if (!RELAX) FAIL("lane drift"); t.lab[ns] = LF; } else t.lab[ns] = LT + r;
            newHalf[ns] = halfOf(u);
        }
    }
    for (int u : ends) {
        if (done[u]) continue;
        int o, anc; walk(u, o, anc); done[u] = 1; done[o] = 1;
        if (o >= 2 * NS) { fprintf(stderr, "unexpected\n"); exit(1); }
        int a2 = (anc >= BIG ? 0 : anc) - 1;
        if (RELAX) a2 = 0; else if (a2 < -W2) FAIL("anchor drift");
        int n1 = newSlot(u), n2 = newSlot(o);
        t.mask |= 1ULL << n1; t.mask |= 1ULL << n2;
        t.lab[n1] = n2; t.lab[n2] = n1; t.anc[n1] = t.anc[n2] = a2;
    }
    for (int e = 0; e < ne; e++) if (!visE[e]) FAIL("cycle");
    t.age = 0; (void)anyF;
    for (int j = 0; j < 3; j++) t.uL[j] = 255;
    if (UNIONQ >= 0) {
        int tl = lineOf(C.c - 1 + PH * 100, D - 1), tn = tl + 1;   // newest old line, new line (absolute parity)
        auto lower = [&](int line) { return ((line - UNIONQ) % 2 + 2) % 2 == 0; };
        // old partner links
        for (int i = 0; i < NS; i++) if ((s.mask >> i & 1) && s.lab[i] > LF) {
            int cd = s.anc[i] & 255;
            if (cd == 254) ulinks.push_back({i, nInf++});
            else if (cd < 64) { if (i < cd) ulinks.push_back({i, cd}); }
            else ulinks.push_back({i, cd});
        }
        for (int k = 0; k < 3; k++) if (lower(tl - k)) {
            int cd = s.uL[k];
            if (cd == 254) ulinks.push_back({64 + k, nInf++});
            else if (cd >= 64 && cd < 67 && 64 + k < cd) ulinks.push_back({64 + k, cd});
            else if (cd == 255) FAIL("uL missing");
        }
        ulinks.push_back({67, 68});                       // new line vertex
        if (!lower(tn)) ulinks.push_back({68, 66});       // L edge {tn-3, tn}
        // walk the union graph
        static int udeg[256], uinc[256][2]; static int uvis[600];
        for (int i = 0; i < nInf; i++) udeg[i] = 0;
        for (int e = 0; e < (int)ulinks.size(); e++) {
            int a = ulinks[e].first, b = ulinks[e].second;
            if (udeg[a] >= 2 || udeg[b] >= 2) FAIL("union degree");
            uinc[a][udeg[a]++] = e; uinc[b][udeg[b]++] = e; uvis[e] = 0;
        }
        auto uwalk = [&](int st0) {
            int u = st0, e = uinc[u][0];
            while (true) {
                uvis[e] = 1; int v = ulinks[e].first == u ? ulinks[e].second : ulinks[e].first;
                if (udeg[v] == 1) return v;
                int e2 = uinc[v][0] == e ? uinc[v][1] : uinc[v][0]; u = v; e = e2;
            }
        };
        int code[256]; for (int i = 0; i < nInf; i++) code[i] = 254;
        vector<int> eps;
        for (int ns = 0; ns < NS; ns++) if (newHalf[ns] >= 0) { code[newHalf[ns]] = ns; eps.push_back(newHalf[ns]); }
        int lh[3] = {lower(tn) ? 68 : -1, lower(tl) ? 64 : -1, lower(tl - 1) ? 65 : -1};
        for (int k = 0; k < 3; k++) if (lh[k] >= 0) { code[lh[k]] = 64 + k; eps.push_back(lh[k]); }
        for (int h : eps) {
            if (udeg[h] != 1) FAIL("endpoint degree");
            int o = uwalk(h);
            if (o < 70 && code[o] == 254 && o != h) FAIL("dangling");
            int cd = (o >= 70) ? 254 : code[o];
            bool found = false;
            for (int ns = 0; ns < NS; ns++) if (newHalf[ns] == h) { t.anc[ns] = cd; found = true; }
            for (int k = 0; k < 3; k++) if (lh[k] == h) { t.uL[k] = cd; found = true; }
        }
        for (int i = 70; i < nInf; i++) if (udeg[i] == 1) uwalk(i);
        for (int e = 0; e < (int)ulinks.size(); e++) if (!uvis[e]) FAIL("union cycle");
    }
    cb(t, C.X, C.T, C.chosen);
}

template <class F>
void rec(Ctx& C, int b, F& cb) {
    if (b == D) { finish(C, cb); return; }
    int need = C.need[b];
    // options: subsets of forward moves of size need
    for (int msk = 0; msk < 16; msk++) {
        if (__builtin_popcount(msk) != need) continue;
        bool ok = true;
        for (int m = 0; m < 4 && ok; m++) if (msk >> m & 1) {
            int tb = b + FMb[m];
            if (tb < 0 || tb >= D) ok = false;
        }
        if (!ok) continue;
        // capacities
        int add1[16] = {0}, add2[16] = {0};
        for (int m = 0; m < 4; m++) if (msk >> m & 1) {
            int tb = b + FMb[m];
            if (FMa[m] == 1) add1[tb]++; else add2[tb]++;
        }
        for (int tb = 0; tb < D && ok; tb++) {
            if (C.cap1[tb] + add1[tb] > 2 - term[tb]) ok = false;
            if (C.cap2[tb] + add2[tb] > 2 - term[tb]) ok = false;
        }
        if (!ok) continue;
        // costs
        int dX = 0;
        for (int m = 0; m < 4; m++) if (msk >> m & 1) {
            dX += crossF[b][m];
            for (int i = 0; i < NS; i++) if ((C.s->mask >> i & 1) && slots[i].off == -1 && FMa[slots[i].m] == 2)
                dX += crossP[b][m][slots[i].b][slots[i].m];
            for (auto& pr : C.chosen) dX += crossN[b][m][pr.first][pr.second];
            for (int m2 = 0; m2 < m; m2++) if (msk >> m2 & 1) dX += crossN[b][m][b][m2];
        }
        // turn at cell b
        int da[2], db[2], k = 0;
        for (int j = 0; j < C.ninc[b]; j++) { const Slot& sl = slots[C.inc[b][j]]; da[k] = -FMa[sl.m]; db[k] = -FMb[sl.m]; k++; }
        if (term[b]) { da[k] = La; db[k] = Lb; k++; }
        for (int m = 0; m < 4; m++) if (msk >> m & 1) { da[k] = FMa[m]; db[k] = FMb[m]; k++; }
        int dT = (da[0] == -da[1] && db[0] == -db[1]) ? 0 : 1;
        for (int tb = 0; tb < D; tb++) { C.cap1[tb] += add1[tb]; C.cap2[tb] += add2[tb]; }
        size_t csz = C.chosen.size();
        for (int m = 0; m < 4; m++) if (msk >> m & 1) C.chosen.push_back({b, m});
        C.X += dX; C.T += dT;
        rec(C, b + 1, cb);
        C.X -= dX; C.T -= dT;
        C.chosen.resize(csz);
        for (int tb = 0; tb < D; tb++) { C.cap1[tb] -= add1[tb]; C.cap2[tb] -= add2[tb]; }
    }
}

template <class F>
void transitions(const St& s, F cb) {
    Ctx C; C.s = &s; C.c = s.ph; C.X = 0; C.T = 0;
    for (int b = 0; b < D; b++) { C.ninc[b] = 0; C.cap1[b] = 0; C.cap2[b] = 0; }
    for (int i = 0; i < NS; i++) if (s.mask >> i & 1) {
        const Slot& sl = slots[i];
        if (sl.ta == 0) { if (C.ninc[sl.tb] >= 2) return; C.inc[sl.tb][C.ninc[sl.tb]++] = i; }
        else C.cap1[sl.tb]++;
    }
    for (int b = 0; b < D; b++) { C.need[b] = 2 - C.ninc[b] - term[b]; if (C.need[b] < 0) return; }
    rec(C, 0, cb);
}

int main(int argc, char** argv) {
    if (argc < 9) { fprintf(stderr, "usage: tm kind D s off wX wT W W2 [maxstates]\n"); return 1; }
    KIND = argv[1]; D = atoi(argv[2]); S = atoi(argv[3]); OFF = atoi(argv[4]);
    WX = atoi(argv[5]); WT = atoi(argv[6]); W = atoi(argv[7]); W2 = atoi(argv[8]);
    long maxStates = argc > 9 ? atol(argv[9]) : 40000000;
    if (getenv("EXACT")) RELAX = 0;
    if (getenv("NOLANE")) NOLANE = 1;
    if (getenv("UNION")) { UNIONQ = atoi(getenv("UNION")); if (KIND != "bottom" || RELAX) { fprintf(stderr, "UNION needs bottom + EXACT\n"); return 1; } }
    if (KIND == "bottom") { La = -2; Lb = 1; PH = 2 * S; } else { La = -1; Lb = 2; PH = S; }
    if (getenv("RULE")) {
        string r = getenv("RULE"); RULEM = atoi(r.c_str()); PH = RULEM; memset(ALLOWED, 0, sizeof ALLOWED);
        size_t p = r.find(':') + 1;
        while (p < r.size()) { int a, d; if (sscanf(r.c_str() + p, "%d/%d", &a, &d) != 2) break; ALLOWED[a][d] = true;
            size_t q = r.find(',', p); if (q == string::npos) break; p = q + 1; }
    }
    // PH must make refLane parity and terminal lanes periodic: check
    for (int c = 0; c < PH; c++) {
        if (!RULEM && ((refLane(c + PH) - refLane(c)) & 1) != 0) { fprintf(stderr, "phase\n"); return 1; }
        if (RULEM && (refLab(c + PH) - refLab(c)) % RULEM != 0) { fprintf(stderr, "phase\n"); return 1; }
    }
    for (int b = 0; b < D; b++) term[b] = (b + Lb >= D);
    MINTERM = 1000;
    for (int c = 0; c < PH; c++) for (int b = 0; b < D; b++) if (term[b]) MINTERM = min(MINTERM, labOf(c, b) - refLab(c));
    memset(slotId, -1, sizeof slotId);
    for (int off = -2; off <= -1; off++) for (int b = 0; b < D; b++) for (int m = 0; m < 4; m++) {
        if (off == -2 && FMa[m] != 2) continue;
        int tb = b + FMb[m]; if (tb < 0 || tb >= D) continue;
        slotId[off + 2][b][m] = slots.size(); slots.push_back({off, b, m, off + FMa[m], tb});
    }
    NS = slots.size();
    if (NS > 64) { fprintf(stderr, "too many slots\n"); return 1; }
    // crossing tables (a = column of new edge = 0)
    for (int b = 0; b < D; b++) for (int m = 0; m < 4; m++) {
        int a1 = 0, b1 = b, a2 = FMa[m], b2 = b + FMb[m];
        crossF[b][m] = 0;
        for (int ta = -4; ta <= 6; ta++) for (int tb = 0; tb < D; tb++) if (term[tb])
            crossF[b][m] += segCross(a1, b1, a2, b2, ta, tb, ta + La, tb + Lb);
        for (int bb = 0; bb < D; bb++) for (int mm = 0; mm < 4; mm++) {
            crossN[b][m][bb][mm] = segCross(a1, b1, a2, b2, 0, bb, FMa[mm], bb + FMb[mm]);
            crossP[b][m][bb][mm] = FMa[mm] == 2 ? segCross(a1, b1, a2, b2, -1, bb, 1, bb + FMb[mm]) : 0;
        }
    }
    if (getenv("TRACE")) {
        // trace a periodic template (aligned to absolute phase 0) through the exact transitions
        ifstream f(getenv("TRACE")); vector<vector<string>> rows; string line;
        while (getline(f, line)) { if (line.empty()) continue; istringstream is(line); vector<string> r; string t; while (is >> t) r.push_back(t); rows.push_back(r); }
        int L = KIND == "bottom" ? rows[0].size() : rows.size();
        const int MI[8] = {-2, -1, 1, 2, 2, 1, -1, -2}, MJ[8] = {1, 2, 2, 1, -1, -2, -2, -1};
        auto has = [&](int a, int b, int m) {   // does cell (a,b) have forward move m
            a = ((a % L) + L) % L; string cd = KIND == "bottom" ? rows[D - 1 - b][a] : rows[L - 1 - a][b];
            for (char ch : cd) { int k = ch - '0'; int dx = MJ[k], dy = -MI[k]; int da = KIND == "bottom" ? dx : dy, db = KIND == "bottom" ? dy : dx;
                if (da == FMa[m] && db == FMb[m]) return true; }
            return false;
        };
        auto maskAt = [&](int c) { uint64_t m = 0; for (int i = 0; i < NS; i++) if (has(c + slots[i].off, slots[i].b, slots[i].m)) m |= 1ULL << i; return m; };
        St s; s.ph = 0; s.age = 0; s.mask = maskAt(0); for (int j = 0; j < 3; j++) s.uL[j] = 255;
        for (int i = 0; i < NS; i++) if (s.mask >> i & 1) { s.lab[i] = LF; s.anc[i] = 0; }
        for (int c = 0; c < 4 * L; c++) {
            uint64_t want = maskAt(c + 1); bool found = false; St nx; int fx = 0, ft = 0;
            transitions(s, [&](const St& t, int X, int T, const vector<pair<int,int>>&) { if (t.mask == want) { found = true; nx = t; fx = X; ft = T; } });
            fprintf(stderr, "col %d: %s X=%d T=%d F=%d\n", c, found ? "ok" : "NO TRANSITION", fx, ft, found ? (int)hasF(nx) : -1);
            if (!found) { DBG = 1; DBGMASK = want; transitions(s, [&](const St&, int, int, const vector<pair<int,int>>&) {}); return 4; }
            s = nx;
        }
        return 0;
    }
    fprintf(stderr, "kind=%s D=%d s=%d off=%d wX=%d wT=%d W=%d W2=%d slots=%d PH=%d\n", KIND.c_str(), D, S, OFF, WX, WT, W, W2, NS, PH);
    // BFS from empty states at every phase
    auto getId = [&](const St& st) {
        bool nw; int id = KS.insert(enc(st), nw);
        if (nw) { if (hasF(st)) fidx.push_back(-1); else { fidx.push_back(fid2id.size()); fid2id.push_back(id); G.emplace_back(); } }
        return id;
    };
    // seeds: every capacity-valid mask, all ends labelled F (unknown past), at every phase.
    // Every state of a valid bi-infinite configuration is reached from the seed of its cut
    // far enough to the left (all strands across that cut have ended).
    {
        vector<uint64_t> masks;
        int inC[16], inC1[16], outM1[16], outM2[16];
        memset(inC, 0, sizeof inC); memset(inC1, 0, sizeof inC1); memset(outM1, 0, sizeof outM1); memset(outM2, 0, sizeof outM2);
        function<void(int, uint64_t)> dfs = [&](int i, uint64_t m) {
            if (i == NS) { masks.push_back(m); return; }
            dfs(i + 1, m);
            const Slot& sl = slots[i];
            int* tgt = sl.ta == 0 ? inC : inC1; int* src = sl.off == -2 ? outM2 : outM1;
            if (tgt[sl.tb] + 1 > 2 - term[sl.tb] || src[sl.b] + 1 > 2 - term[sl.b]) return;
            tgt[sl.tb]++; src[sl.b]++;
            dfs(i + 1, m | 1ULL << i);
            tgt[sl.tb]--; src[sl.b]--;
        };
        dfs(0, 0);
        fprintf(stderr, "seed masks=%zu\n", masks.size());
        for (int ph = 0; ph < PH; ph++) for (uint64_t m : masks) {
            St e; e.ph = ph; e.mask = m; e.age = 0; for (int j = 0; j < 3; j++) e.uL[j] = UNIONQ >= 0 ? 254 : 255;
            for (int i = 0; i < NS; i++) if (m >> i & 1) { e.lab[i] = LF; e.anc[i] = 0; }
            getId(e);
        }
    }
    for (size_t q = 0; q < KS.size(); q++) {
        St s = dec(KS.get(q));
        int fq = fidx[q];
        unordered_map<int, Tr> best;
        transitions(s, [&](const St& t, int X, int T, const vector<pair<int,int>>&) {
            int to = getId(t);
            if (fq < 0) return;
            to = fidx[to]; int cost = WX * X + WT * T;
            auto it = best.find(to);
            if (it == best.end() || it->second.cost > cost) best[to] = {to, cost, X, T};
        });
        if (fq >= 0) for (auto& kv : best) G[fq].push_back(kv.second);
        if ((long)KS.size() > maxStates) { fprintf(stderr, "state limit hit\n"); printf("{\"status\":\"STATE_LIMIT\",\"states\":%zu}\n", KS.size()); return 2; }
        if (q % 1000000 == 0) fprintf(stderr, "  q=%zu states=%zu ffree=%zu\n", q, KS.size(), fid2id.size());
    }
    fprintf(stderr, "all states=%zu\n", KS.size());
    int N = fid2id.size();
    long E = 0; for (auto& g : G) E += g.size();
    fprintf(stderr, "states=%d edges=%ld\n", N, E);
    // trim: keep nodes with successors (iterate) and with predecessors
    vector<char> alive(N, 1);
    // optional matching-parity filter (env PI=0/1): pi = (#pending ends whose strand started at a
    // terminal) - (line of the newest processed terminal)  mod 2. Invariant along valid transitions.
    if (getenv("PI")) {
        int want = atoi(getenv("PI")), kept = 0;
        for (int u = 0; u < N; u++) {
            St s = dec(KS.get(fid2id[u])); int cnt = 0;
            for (int i = 0; i < NS; i++) if ((s.mask >> i & 1) && s.lab[i] >= LF) cnt++;
            int tl = -1000; for (int b = 0; b < D; b++) if (term[b]) tl = max(tl, lineOf(s.ph - 1 + PH * 100, b));
            int pi = ((cnt - tl) % 2 + 2) % 2;
            if (pi != want) alive[u] = 0; else kept++;
        }
        fprintf(stderr, "PI=%d keeps %d of %d states\n", want, kept, N);
    }
    {
        vector<int> outd(N, 0), ind(N, 0);
        vector<vector<int>> pred(N);
        for (int u = 0; u < N; u++) if (alive[u]) for (auto& t : G[u]) if (alive[t.to]) { pred[t.to].push_back(u); outd[u]++; ind[t.to]++; }
        deque<int> dq;
        for (int u = 0; u < N; u++) if (alive[u] && (outd[u] == 0 || ind[u] == 0)) { alive[u] = 0; dq.push_back(u); }
        while (!dq.empty()) {
            int u = dq.front(); dq.pop_front();
            for (int p : pred[u]) if (alive[p]) { if (--outd[p] == 0) { alive[p] = 0; dq.push_back(p); } }
            for (auto& t : G[u]) if (alive[t.to]) { if (--ind[t.to] == 0) { alive[t.to] = 0; dq.push_back(t.to); } }
        }
    }
    int NA = 0; for (int u = 0; u < N; u++) NA += alive[u];
    fprintf(stderr, "core states=%d\n", NA);
    if (NA == 0) { printf("{\"status\":\"NO_CYCLE\",\"states\":%d}\n", N); return 0; }
    // Howard policy iteration (min mean cycle)
    typedef long double LD;
    vector<int> pol(N, -1);   // index into G[u]
    for (int u = 0; u < N; u++) if (alive[u]) {
        int bi = -1; for (int j = 0; j < (int)G[u].size(); j++) if (alive[G[u][j].to] && (bi < 0 || G[u][j].cost < G[u][bi].cost)) bi = j;
        pol[u] = bi;
    }
    vector<LD> eta(N), x(N);
    const LD eps = 1e-9;
    for (int iter = 0; iter < 10000; iter++) {
        // evaluate
        vector<int> color(N, 0);   // 0 new, 1 on stack, 2 done
        vector<int> path;
        for (int s0 = 0; s0 < N; s0++) if (alive[s0] && color[s0] == 0) {
            path.clear(); int u = s0;
            while (color[u] == 0) { color[u] = 1; path.push_back(u); u = G[u][pol[u]].to; }
            if (color[u] == 1) {     // new cycle starting at u
                LD sum = 0; int len = 0; int v = u;
                do { sum += G[v][pol[v]].cost; len++; v = G[v][pol[v]].to; } while (v != u);
                LD e = sum / len;
                // potentials along cycle: x(u)=0, go backwards
                vector<int> cyc; v = u; do { cyc.push_back(v); v = G[v][pol[v]].to; } while (v != u);
                eta[u] = e; x[u] = 0; color[u] = 2;
                for (int i = cyc.size() - 1; i >= 1; i--) { int w = cyc[i]; eta[w] = e; x[w] = G[w][pol[w]].cost - e + x[G[w][pol[w]].to]; color[w] = 2; }
            }
            for (int i = path.size() - 1; i >= 0; i--) {
                int w = path[i]; if (color[w] == 2) continue;
                int nx = G[w][pol[w]].to; eta[w] = eta[nx]; x[w] = G[w][pol[w]].cost - eta[nx] + x[nx]; color[w] = 2;
            }
        }
        bool changed = false;
        for (int u = 0; u < N; u++) if (alive[u]) {
            int bj = pol[u]; LD be = eta[G[u][bj].to];
            for (int j = 0; j < (int)G[u].size(); j++) { int v = G[u][j].to; if (alive[v] && eta[v] < be - eps) { be = eta[v]; bj = j; } }
            if (bj != pol[u]) { pol[u] = bj; changed = true; }
        }
        if (!changed) {
            for (int u = 0; u < N; u++) if (alive[u]) {
                int bj = pol[u]; LD bv = G[u][bj].cost - eta[u] + x[G[u][bj].to];
                for (int j = 0; j < (int)G[u].size(); j++) {
                    int v = G[u][j].to; if (!alive[v] || fabsl(eta[v] - eta[u]) > eps) continue;
                    LD val = G[u][j].cost - eta[u] + x[v];
                    if (val < bv - eps) { bv = val; bj = j; }
                }
                if (bj != pol[u]) { pol[u] = bj; changed = true; }
            }
        }
        if (!changed) { fprintf(stderr, "howard converged in %d iterations\n", iter); break; }
    }
    // best cycle
    int bu = -1; for (int u = 0; u < N; u++) if (alive[u] && (bu < 0 || eta[u] < eta[bu])) bu = u;
    // walk to the cycle
    { vector<char> seen(N, 0); int u = bu; while (!seen[u]) { seen[u] = 1; u = G[u][pol[u]].to; } bu = u; }
    vector<int> cyc; { int u = bu; do { cyc.push_back(u); u = G[u][pol[u]].to; } while (u != bu); }
    ll sumC = 0, sumX = 0, sumT = 0;
    for (int u : cyc) { sumC += G[u][pol[u]].cost; sumX += G[u][pol[u]].X; sumT += G[u][pol[u]].T; }
    int L = cyc.size();
    // exact check: no cycle with mean < sumC/L  <=>  weights w*L - sumC have no negative cycle (Bellman-Ford / SPFA)
    bool certified = true;
    {
        vector<ll> d(N, 0); vector<char> inq(N, 0); vector<int> cnt(N, 0);
        vector<vector<pair<int,ll>>> dummy;
        deque<int> q; for (int u = 0; u < N; u++) if (alive[u]) { q.push_back(u); inq[u] = 1; }
        long relax = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop_front(); inq[u] = 0;
            for (auto& t : G[u]) if (alive[t.to]) {
                ll w = (ll)t.cost * L - sumC;
                if (d[u] + w < d[t.to]) {
                    d[t.to] = d[u] + w; relax++;
                    if (!inq[t.to]) { if (++cnt[t.to] > NA + 1) { certified = false; q.clear(); break; } q.push_back(t.to); inq[t.to] = 1; }
                }
            }
        }
        fprintf(stderr, "certificate %s (relaxations %ld)\n", certified ? "OK" : "FAILED", relax);
    }
    // reconstruct template of the witness cycle
    // per column: list of (b, move dir (da,db)) for all edges at the cell
    vector<vector<vector<pair<int,int>>>> cell(L, vector<vector<pair<int,int>>>(D));
    for (int i = 0; i < L; i++) {
        St s = dec(KS.get(fid2id[cyc[i]])); int to = G[cyc[i]][pol[cyc[i]]].to; int want = G[cyc[i]][pol[cyc[i]]].cost;
        bool found = false;
        transitions(s, [&](const St& t, int X, int T, const vector<pair<int,int>>& ch) {
            if (found) return;
            if (WX * X + WT * T != want) return;
            if (fidx[KS.find(enc(t))] != to) return;
            found = true;
            for (auto& pr : ch) {
                int b = pr.first, m = pr.second;
                cell[i][b].push_back({FMa[m], FMb[m]});
                int ta = (i + FMa[m]) % L, tb = b + FMb[m];
                cell[ta][tb].push_back({-FMa[m], -FMb[m]});
            }
        });
        if (!found) { fprintf(stderr, "reconstruct failed\n"); return 3; }
    }
    for (int i = 0; i < L; i++) for (int b = 0; b < D; b++) if (term[b]) cell[i][b].push_back({La, Lb});
    // board.js codes: (di,dj) -> code; (dx,dy) = (MJ, -MI)
    const int MI[8] = {-2, -1, 1, 2, 2, 1, -1, -2}, MJ[8] = {1, 2, 2, 1, -1, -2, -2, -1};
    auto code = [&](int dx, int dy) { for (int m = 0; m < 8; m++) if (MJ[m] == dx && -MI[m] == dy) return m; return -1; };
    // phase of the cycle start: column index i corresponds to absolute column with phase dec(cyc[0]).ph + i
    int ph0 = dec(KS.get(fid2id[cyc[0]])).ph;
    auto cellCode = [&](int i, int b) {
        vector<int> cs;
        for (auto& d : cell[i][b]) {
            int dx, dy; if (KIND == "bottom") { dx = d.first; dy = d.second; } else { dx = d.second; dy = d.first; }
            cs.push_back(code(dx, dy));
        }
        sort(cs.begin(), cs.end());
        string r; for (int c : cs) r += char('0' + c); return r;
    };
    int wild = 0; for (int u : cyc) wild += hasF0(dec(KS.get(fid2id[u])));
    printf("{\"status\":\"%s\",\"mode\":\"%s\",\"wild\":%d,\"kind\":\"%s\",\"D\":%d,\"s\":%d,\"off\":%d,\"wX\":%d,\"wT\":%d,\"W\":%d,\"W2\":%d,",
           certified ? "CERTIFIED" : "UNCERTIFIED", NOLANE ? "nolane_lower_bound" : RULEM ? (RELAX ? "rule_relaxed_lower_bound" : "rule_exact") : RELAX ? "relaxed_lower_bound" : "exact_reachable", wild, KIND.c_str(), D, S, OFF, WX, WT, W, W2);
    printf("\"states\":%d,\"core\":%d,\"period\":%d,\"phase0\":%d,\"cost\":%lld,\"X\":%lld,\"T\":%lld,\"rate\":%.6f,\"Xrate\":%.6f,\"Trate\":%.6f,\"tpl\":[",
           N, NA, L, ph0, sumC, sumX, sumT, (double)sumC / L, (double)sumX / L, (double)sumT / L);
    // template: bottom rows y=D-1..0, columns x=0..L-1 ; left rows y=L-1..0, columns x=0..D-1
    // column 0 of the template is absolute column with phase ph0; shift to absolute phase 0 is the reader's job
    if (KIND == "bottom") {
        for (int y = D - 1; y >= 0; y--) {
            printf("%s\"", y == D - 1 ? "" : ",");
            for (int i = 0; i < L; i++) printf("%s%s", i ? " " : "", cellCode(i, y).c_str());
            printf("\"");
        }
    } else {
        for (int i = L - 1; i >= 0; i--) {
            printf("%s\"", i == L - 1 ? "" : ",");
            for (int b = 0; b < D; b++) printf("%s%s", b ? " " : "", cellCode(i, b).c_str());
            printf("\"");
        }
    }
    printf("]}\n");
    return 0;
}
