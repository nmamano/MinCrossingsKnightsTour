// corr.cpp - exact transfer matrix for a straight colour-current corridor (KT Edge Searcher, gap mission).
// Re-implementation (own code) of the KT Lower Bounds F12 corridor model, in C++, for wider bands.
//
// Geometry: route direction (A,1): a cell (x,y) has transverse coordinate u = x - A*y - OFF.
// Band = cells with 0 <= u < W. Every band cell has degree exactly 2 (any knight move).
// Outside cells keep their base-field edges. An edge between a band cell and an outside cell is
// allowed only if it is a base edge, and then it is forced. Outside-outside edges are base edges
// (never cross each other, and never cross band edges because their u-ranges are disjoint).
// No finite cycle. Weight = proper crossings among represented edges (all edges with a band end).
// Sweep: rows y increasing; inside a row, positions (band cells and the outside cells that have a
// base edge into the band) by increasing u. The first 3 rows are warm-up (band degree <= 2), so
// every periodic configuration of every period appears as a cycle of the state graph.
// Colour current through the cut below row y: sum over represented edges crossing it of chi(lower end).
// Result: for each current value c, the minimum mean crossings per row over all cycles with current c
// (Howard policy iteration + exact integer Bellman-Ford certificate) and a witness cycle.
//
// usage: corr KIND W [maxstates]      KIND in: diag diag21 diag12 mid vert12 vert21 anti21 anti12 d21_<A> d12_<A>
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int,int> pii;

int A, W, OFF;
function<pii(int,int)> FIELD;   // base out-direction at planar (x,y)
const int KM[8][2] = {{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};
const int UPM[4][2] = {{1,2},{2,1},{-1,2},{-2,1}};   // moves with dy > 0

static inline int uOf(int x, int y) { return x - A * y - OFF; }
static inline bool inBand(int x, int y) { int u = uOf(x, y); return 0 <= u && u < W; }
static inline int chiOf(int x, int y) { return ((x + y) % 2 + 2) % 2 == 0 ? 1 : -1; }
int WALL = 0;   // 1: cells with x < 0 are off the board; base U-turns (0,y)-(1,y+2) (KT Lower Bounds F12 "edge")
static set<pii> baseNbrs(int x, int y) {
    set<pii> s; if (WALL && x < 0) return s;
    pii d = FIELD(x, y); s.insert({x + d.first, y + d.second});
    for (auto& m : KM) { int qx = x - m[0], qy = y - m[1]; pii e = FIELD(qx, qy); if (e.first == m[0] && e.second == m[1]) s.insert({qx, qy}); }
    if (WALL) {
        for (auto it = s.begin(); it != s.end();) if (it->first < 0) it = s.erase(it); else ++it;
        if (WALL == 1 && x == 0) s.insert({1, y + 2});
        if (WALL == 1 && x == 1) s.insert({0, y - 2});
    }
    return s;
}
static int orient(ll ax, ll ay, ll bx, ll by, ll cx, ll cy) { ll v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax); return (v > 0) - (v < 0); }
static bool segX(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4) {
    return orient(x1,y1,x2,y2,x3,y3) * orient(x1,y1,x2,y2,x4,y4) < 0 && orient(x3,y3,x4,y4,x1,y1) * orient(x3,y3,x4,y4,x2,y2) < 0;
}

// positions in a row (row y = 0): u values, kind (band / ghost) and forced up-edges (move index into UPM)
struct Pos { int u; bool band; vector<int> forcedUp; int nForcedDown; };
vector<Pos> P; int NP;
int posOfU(int u) { for (int i = 0; i < NP; i++) if (P[i].u == u) return i; return -1; }

// pending edge: source at (row sdy in {-2,-1,0} relative to current row, position index sp), move m, label
// label: 0..63 partner index in the sorted list; RAY = 63 (strand goes to outside or to infinity); INERT = 62
// (edge into an outside cell: crossing-only, its band end is already joined)
const int RAY = 63, INERT = 62;
struct PE { int sdy, sp, m, lab, org; };   // org: line origin r = c + 2*row (RAY ends), 255 = unknown
int RMAX = 40;   // origins older than this become unknown (relaxation: unknown ends count as re-paired)
struct St { int pos, rp, warm; vector<PE> e; };
// planar coordinates of a pending edge relative to current row 0 (rowpar handled by colour only)
static inline void srcXY(const PE& p, int& x, int& y) { y = p.sdy; x = P[p.sp].u + A * y + OFF; }

string enc(const St& s) {
    string k; k.reserve(3 + 3 * s.e.size());
    k.push_back((char)s.pos); k.push_back((char)(s.rp | (s.warm << 1)));
    for (auto& p : s.e) { k.push_back((char)((p.sdy + 2) * NP + p.sp)); k.push_back((char)(p.m | (p.lab << 2))); k.push_back((char)(p.lab == RAY ? p.org : 0)); }
    return k;
}
St dec(const string& k) {
    St s; s.pos = (unsigned char)k[0]; s.rp = k[1] & 1; s.warm = (unsigned char)k[1] >> 1;
    for (size_t i = 2; i < k.size(); i += 3) { int a = (unsigned char)k[i], b = (unsigned char)k[i + 1]; s.e.push_back({a / NP - 2, a % NP, b & 3, b >> 2, (unsigned char)k[i + 2]}); }
    return s;
}
int TARGET_SET = 0, TARGET = 0;
const int WARMR = 2;   // rows 0,1 relaxed; from row 2 on every band cell has all its down-neighbours processed
int ROWCOLOUR;   // 1 if the colour of (u, row) alternates with the row (A even)

// current through the cut below the current row (only meaningful at pos == 0)
int currentOf(const St& s) {
    int c = 0;
    for (auto& p : s.e) { int x, y; srcXY(p, x, y); int ch = chiOf(x, y); if (ROWCOLOUR && s.rp) ch = -ch; c += ch; }
    return c;
}

// canonicalise: sort entries and rewrite partner indices
St canon(vector<PE> e, vector<int> partner /* index into e or -1 ray, -2 inert */, int pos, int rp, int warm, const vector<int>& org) {
    int n = e.size(); vector<int> ord(n); iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int a, int b) { return make_tuple(e[a].sdy, e[a].sp, e[a].m) < make_tuple(e[b].sdy, e[b].sp, e[b].m); });
    vector<int> where(n); for (int i = 0; i < n; i++) where[ord[i]] = i;
    St s; s.pos = pos; s.rp = rp; s.warm = warm;
    for (int i = 0; i < n; i++) { PE p = e[ord[i]]; int q = partner[ord[i]]; p.lab = q == -1 ? RAY : (q == -2 ? INERT : where[q]); p.org = q == -1 ? org[ord[i]] : 0; s.e.push_back(p); }
    return s;
}

// one transition; callback(next state, crossings, chosen free moves)
template <class CB> void trans(const St& s, CB cb) {
    const Pos& cp = P[s.pos];
    int cx = cp.u + OFF, cy = 0;   // planar position of current cell (row 0)
    int n = s.e.size();
    vector<int> inc, rest;
    for (int i = 0; i < n; i++) {
        int x, y; srcXY(s.e[i], x, y); int tx = x + UPM[s.e[i].m][0], ty = y + UPM[s.e[i].m][1];
        if (tx == cx && ty == cy) inc.push_back(i); else rest.push_back(i);
    }
    // incoming capacity per future target
    map<pii, int> fut;
    for (int i : rest) { int x, y; srcXY(s.e[i], x, y); fut[{x + UPM[s.e[i].m][0], y + UPM[s.e[i].m][1]}]++; }
    auto edgeCross = [&](int x1, int y1, int x2, int y2, const vector<PE>& extra, int skipSelf) {
        int c = 0;
        for (int i : rest) { int x, y; srcXY(s.e[i], x, y); c += segX(x1, y1, x2, y2, x, y, x + UPM[s.e[i].m][0], y + UPM[s.e[i].m][1]); }
        for (auto& p : extra) { int x, y; srcXY(p, x, y); c += segX(x1, y1, x2, y2, x, y, x + UPM[p.m][0], y + UPM[p.m][1]); }
        (void)skipSelf; return c;
    };
    // next position
    int npos = s.pos + 1, nrp = s.rp, nwarm = s.warm, shift = 0;
    if (npos == NP) { npos = 0; shift = 1; nrp ^= 1; nwarm = min(WARMR, s.warm + 1); }
    auto finish = [&](vector<PE> e, vector<int> partner, int X, const vector<int>& chosen, vector<int> org) {
        // drop nothing (incoming already removed); shift rows; origins age by one row
        if (shift) for (size_t i = 0; i < e.size(); i++) { e[i].sdy -= 1; if (partner[i] == -1 && org[i] != 255) { org[i] += 2; if (org[i] > RMAX) org[i] = 255; } }
        for (auto& p : e) if (p.sdy < -2) { fprintf(stderr, "sdy underflow\n"); exit(1); }
        St t = canon(e, partner, npos, nrp, nwarm, org);
        if (shift && nwarm >= WARMR && TARGET_SET && (!ROWCOLOUR || nrp == 0) && currentOf(t) != TARGET) return;
        cb(t, X, chosen);
    };
    // base: copy of rest with partner indices remapped
    vector<int> idxNew(n, -1); vector<PE> e0; vector<int> part0;
    for (int i : rest) { idxNew[i] = e0.size(); e0.push_back(s.e[i]); }
    auto partnerOld = [&](int i) { int l = s.e[i].lab; return l == RAY ? -1 : (l == INERT ? -2 : l); };
    for (int i : rest) { int q = partnerOld(i); part0.push_back(q >= 0 ? idxNew[q] : q); }
    vector<int> org0; for (int i : rest) org0.push_back(s.e[i].lab == RAY ? s.e[i].org : 0);
    if (!cp.band) {
        // outside cell: incoming edges are forced band->outside edges (INERT); add forced up-edges (RAY)
        for (int i : inc) if (s.e[i].lab != INERT) { fprintf(stderr, "ghost got non-inert edge\n"); exit(1); }
        vector<PE> e = e0; vector<int> part = part0; vector<int> org = org0; int X = 0; vector<PE> added;
        for (int m : cp.forcedUp) {
            int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
            if (++fut[{tx, ty}] > 2) return;
            X += edgeCross(cx, cy, tx, ty, added, 0);
            PE p{0, s.pos, m, RAY, 255}; e.push_back(p); part.push_back(-1); org.push_back(255); added.push_back(p);
        }
        finish(e, part, 2 * X, {}, org);
        return;
    }
    // band cell
    int ninc = inc.size(), nfu = cp.forcedUp.size();
    int need = 2 - ninc - nfu;
    if (need < 0) return;
    vector<int> cand;
    for (int m = 0; m < 4; m++) {
        int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
        if (!inBand(tx, ty)) continue;
        cand.push_back(m);
    }
    int lo = s.warm >= WARMR ? need : 0;
    for (int k = lo; k <= need; k++) {
        // choose k of cand
        vector<int> sel(k);
        function<void(int, int)> rec = [&](int start, int d) {
            if (d == k) {
                vector<PE> e = e0; vector<int> part = part0; vector<int> org = org0; int X = 0; vector<PE> added;
                map<pii, int> f2 = fut;
                // forced up edges (to outside): INERT entries; free edges
                vector<int> newIdx;   // indices in e of new free edges
                for (int m : cp.forcedUp) {
                    int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
                    X += edgeCross(cx, cy, tx, ty, added, 0);
                    PE p{0, s.pos, m, INERT, 0}; e.push_back(p); part.push_back(-2); org.push_back(0); added.push_back(p);
                }
                for (int m : sel) {
                    int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
                    if (++f2[{tx, ty}] > 2) return;
                    X += edgeCross(cx, cy, tx, ty, added, 0);
                    PE p{0, s.pos, m, RAY, 255}; newIdx.push_back(e.size()); e.push_back(p); part.push_back(-1); org.push_back(255); added.push_back(p);
                }
                // connectors at this cell: incoming (partner known), forced-up (ray), new free (to assign)
                // represent each connector as: type 0 = existing end with partner p (index in e, -1 ray), type 1 = new edge index
                // connectors: {type, idx, origin}: type 0 existing end (idx = partner index in e or -1 ray with origin), 1 new edge idx
                struct Con { int t, i, o; };
                vector<Con> con;
                for (int i : inc) { int q = partnerOld(i); con.push_back({0, q >= 0 ? idxNew[q] : -1, q >= 0 ? 0 : s.e[i].org}); }
                for (int j = 0; j < nfu; j++) con.push_back({0, -1, cx});   // line of this cell: c = x - 2*0, r = c + 2*0
                for (int j : newIdx) con.push_back({1, j, 0});
                while ((int)con.size() < 2) con.push_back({0, -1, 255});   // warm-up: dangling end, unknown line
                if (ninc == 2) {
                    int q0 = partnerOld(inc[0]);
                    if (q0 == inc[1]) return;   // finite cycle
                }
                Con c0 = con[0], c1 = con[1]; int bonus = 0;
                if (c0.t == 1 && c1.t == 1) { part[c0.i] = c1.i; part[c1.i] = c0.i; }
                else if (c0.t == 1 || c1.t == 1) {
                    Con nw = c0.t == 1 ? c0 : c1, ex = c0.t == 1 ? c1 : c0;
                    part[nw.i] = ex.i; if (ex.i >= 0) part[ex.i] = nw.i; else org[nw.i] = ex.o;
                } else {
                    int p = c0.i, q = c1.i;
                    if (p >= 0 && q >= 0) { part[p] = q; part[q] = p; }
                    else if (p >= 0) { part[p] = -1; org[p] = c1.o; }
                    else if (q >= 0) { part[q] = -1; org[q] = c0.o; }
                    else {   // a strand joins two line ends: P-pair = {c, c+3} with c odd
                        int o1 = c0.o, o2 = c1.o;
                        bool pp = o1 != 255 && o2 != 255 && abs(o1 - o2) == 3 && (min(o1, o2) & 1);
                        bonus = pp ? 0 : 2;
                    }
                }
                finish(e, part, 2 * X - bonus, sel, org);
                return;
            }
            for (int i = start; i < (int)cand.size(); i++) { sel[d] = cand[i]; rec(i + 1, d + 1); }
        };
        rec(0, 0);
    }
}

// Minimum mean cycle over alive states. Howard (approximate, capped) gives a start cycle; then exact
// refinement: Bellman-Ford/SPFA on integer weights L*w - S finds a cycle of smaller mean if one exists.
// On return, cert = true means no cycle has mean < S/L (exact integer certificate).
static double tnow() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }
struct CSR { vector<uint64_t> st; vector<uint32_t> to; vector<int16_t> w; size_t deg(int u) const { return st[u + 1] - st[u]; } };
ll LAM_S = -1; int LAM_L = 0;   // env LAMBDA=p/q: skip Howard, start the exact refinement at p/q per row
void mmc(int N, const CSR& G, const vector<char>& alive, int NA, vector<int>& cyc, ll& S, int& L, bool& cert) {
    double t0 = tnow();
    if (LAM_S >= 0) { S = LAM_S; L = LAM_L * NP; cyc.clear(); goto refine; }
    {
    typedef long double LD; const LD eps = 1e-7;
    vector<int> pol(N, -1); vector<LD> eta(N), xv(N);
    for (int u = 0; u < N; u++) if (alive[u]) { int bj = -1; for (int j = 0; j < (int)G.deg(u); j++) if (alive[G.to[G.st[u] + j]] && (bj < 0 || G.w[G.st[u] + j] < G.w[G.st[u] + bj])) bj = j; pol[u] = bj; }
    int it;
    for (it = 0; it < 200; it++) {
        vector<char> color(N, 0); vector<int> path;
        for (int s0i = 0; s0i < N; s0i++) if (alive[s0i] && !color[s0i]) {
            path.clear(); int u = s0i;
            while (!color[u]) { color[u] = 1; path.push_back(u); u = G.to[G.st[u] + pol[u]]; }
            if (color[u] == 1) {
                LD sum = 0; int len = 0, v = u; do { sum += G.w[G.st[v] + pol[v]]; len++; v = G.to[G.st[v] + pol[v]]; } while (v != u);
                LD e = sum / len; vector<int> cy; v = u; do { cy.push_back(v); v = G.to[G.st[v] + pol[v]]; } while (v != u);
                eta[u] = e; xv[u] = 0; color[u] = 2;
                for (int i = cy.size() - 1; i >= 1; i--) { int w = cy[i]; eta[w] = e; xv[w] = G.w[G.st[w] + pol[w]] - e + xv[G.to[G.st[w] + pol[w]]]; color[w] = 2; }
            }
            for (int i = path.size() - 1; i >= 0; i--) { int w = path[i]; if (color[w] == 2) continue; int nx = G.to[G.st[w] + pol[w]]; eta[w] = eta[nx]; xv[w] = G.w[G.st[w] + pol[w]] - eta[nx] + xv[nx]; color[w] = 2; }
        }
        bool ch = false;
        for (int u = 0; u < N; u++) if (alive[u]) { int bj = pol[u]; LD be = eta[G.to[G.st[u] + bj]]; for (int j = 0; j < (int)G.deg(u); j++) { int v = G.to[G.st[u] + j]; if (alive[v] && eta[v] < be - eps) { be = eta[v]; bj = j; } } if (bj != pol[u]) { pol[u] = bj; ch = true; } }
        if (!ch) for (int u = 0; u < N; u++) if (alive[u]) { int bj = pol[u]; LD bv = G.w[G.st[u] + bj] - eta[u] + xv[G.to[G.st[u] + bj]];
            for (int j = 0; j < (int)G.deg(u); j++) { int v = G.to[G.st[u] + j]; if (!alive[v] || fabsl(eta[v] - eta[u]) > eps) continue; LD val = G.w[G.st[u] + j] - eta[u] + xv[v]; if (val < bv - eps) { bv = val; bj = j; } }
            if (bj != pol[u]) { pol[u] = bj; ch = true; } }
        if (!ch) break;
    }
    int bu = -1; for (int u = 0; u < N; u++) if (alive[u] && (bu < 0 || eta[u] < eta[bu])) bu = u;
    { vector<char> seen(N, 0); int u = bu; while (!seen[u]) { seen[u] = 1; u = G.to[G.st[u] + pol[u]]; } bu = u; }
    cyc.clear(); { int u = bu; do { cyc.push_back(u); u = G.to[G.st[u] + pol[u]]; } while (u != bu); }
    S = 0; for (int u : cyc) S += G.w[G.st[u] + pol[u]]; L = cyc.size();
    fprintf(stderr, "    howard: %d iterations, cycle %lld/%d, %.1fs\n", it, S, L, tnow() - t0);
    // exact refinement
    }
  refine:
    for (int round = 0; round < 1000; round++) {
        vector<ll> d(N, 0); vector<int> par(N, -1), parw(N, 0), cnt(N, 0); vector<char> inq(N, 0); deque<int> q;
        for (int u = 0; u < N; u++) if (alive[u]) { q.push_back(u); inq[u] = 1; }
        int bad = -1; long relax = 0;
        while (!q.empty() && bad < 0) {
            int u = q.front(); q.pop_front(); inq[u] = 0;
            for (uint64_t ei = G.st[u]; ei < G.st[u + 1]; ei++) if (alive[G.to[ei]]) { pii a(G.to[ei], G.w[ei]);
                ll w = (ll)a.second * L - S;
                if (d[u] + w < d[a.first]) {
                    d[a.first] = d[u] + w; par[a.first] = u; parw[a.first] = a.second;
                    if (++relax % (4L * NA + 16) == 0) {
                        // look for a cycle in the parent graph
                        vector<int> mark(N, 0); int stamp = 0;
                        for (int s0 = 0; s0 < N && bad < 0; s0++) if (alive[s0] && !mark[s0]) {
                            ++stamp; int v = s0; while (v >= 0 && !mark[v]) { mark[v] = stamp + 1000000; v = par[v]; }
                            if (v >= 0 && mark[v] == stamp + 1000000) bad = v;
                            v = s0; while (v >= 0 && mark[v] == stamp + 1000000) { mark[v] = 1; v = par[v]; }
                        }
                        if (bad >= 0) break;
                    }
                    if (!inq[a.first]) { q.push_back(a.first); inq[a.first] = 1; }
                }
            }
        }
        if (bad < 0) { cert = true; fprintf(stderr, "    certified %lld/%d after %d refinements, %.1fs\n", S, L, round, tnow() - t0); return; }
        // parent cycle through bad (edges par[v] -> v)
        vector<int> cy; int v = bad; do { cy.push_back(v); v = par[v]; } while (v != bad);
        reverse(cy.begin(), cy.end());
        ll s2 = 0; for (int x : cy) s2 += parw[x];   // weight of edge par[x] -> x
        // reorder so that cyc[i] -> cyc[i+1]: cy is in forward order after reverse; edge into cy[i] from cy[i-1]
        int L2 = cy.size();
        if (s2 * L >= S * (ll)L2) { fprintf(stderr, "    parent cycle not better (%lld/%d); stop\n", s2, L2); cert = false; return; }
        S = s2; L = L2; cyc = cy;
        fprintf(stderr, "    refined to %lld/%d\n", S, L);
    }
    cert = false;
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 3) { fprintf(stderr, "usage: corr KIND W [maxstates] [target]\n"); return 1; }
    string kind = argv[1]; W = atoi(argv[2]);
    long maxStates = argc > 3 ? atol(argv[3]) : 50000000;
    if (argc > 4) { TARGET_SET = 1; TARGET = atoi(argv[4]); }
    if (getenv("LAMBDA")) { int p, q; if (sscanf(getenv("LAMBDA"), "%d/%d", &p, &q) == 2) { LAM_S = p; LAM_L = q; } }
    OFF = -(W / 2); if (kind == "edge" || kind == "edgeB") OFF = 0;
    auto uni = [](int fx, int fy) { return function<pii(int,int)>([fx, fy](int, int) { return pii(fx, fy); }); };
    if (kind == "diag") { A = 1; FIELD = [](int x, int y) { return x - y <= -1 ? pii(2, 1) : pii(-1, -2); }; }
    else if (kind == "diag21") { A = 1; FIELD = uni(2, 1); }
    else if (kind == "diag12") { A = 1; FIELD = uni(1, 2); }
    else if (kind == "anti21") { A = -1; FIELD = uni(2, 1); }
    else if (kind == "anti12") { A = -1; FIELD = uni(1, 2); }
    else if (kind == "mid") { A = 0; FIELD = [](int x, int y) { (void)y; return x <= -1 ? pii(1, 2) : pii(1, -2); }; }
    else if (kind == "vert12") { A = 0; FIELD = uni(1, 2); }
    else if (kind == "vert21") { A = 0; FIELD = uni(2, 1); }
    else if (kind == "edge") { A = 0; FIELD = uni(2, 1); WALL = 1; }
    else if (kind == "edgeB") { A = 0; FIELD = uni(1, 2); WALL = 2; }   // shallow-field left edge, no base U-turns
    else if (kind.rfind("d21_", 0) == 0) { A = atoi(kind.c_str() + 4); FIELD = uni(2, 1); }
    else if (kind.rfind("d12_", 0) == 0) { A = atoi(kind.c_str() + 4); FIELD = uni(1, 2); }
    else { fprintf(stderr, "unknown kind\n"); return 1; }
    ROWCOLOUR = (A % 2 == 0);
    // positions of row 0
    int GH = 4 + 2 * abs(A);
    for (int u = -GH; u < W + GH; u++) {
        int x = u + OFF, y = 0; Pos p; p.u = u; p.band = (0 <= u && u < W); p.nForcedDown = 0;
        auto bn = baseNbrs(x, y);
        bool touches = false;
        for (auto& q : bn) {
            bool qb = inBand(q.first, q.second);
            if (p.band != qb) {
                touches = true;
                if (q.second > y) { int dx = q.first - x, dy = q.second - y; for (int m = 0; m < 4; m++) if (UPM[m][0] == dx && UPM[m][1] == dy) p.forcedUp.push_back(m); }
                else p.nForcedDown++;
            }
        }
        if (p.band || touches) P.push_back(p);
    }
    NP = P.size();
    fprintf(stderr, "kind %s A=%d W=%d OFF=%d positions/row %d:", kind.c_str(), A, W, OFF, NP);
    for (auto& p : P) fprintf(stderr, " %d%s(up%zu,dn%d)", p.u, p.band ? "b" : "g", p.forcedUp.size(), p.nForcedDown);
    fprintf(stderr, "\n");
    // ---- BFS with compact storage: key arena + open-addressing hash + CSR edges ----
    vector<uint8_t> arena; vector<uint64_t> koff; koff.push_back(0);
    vector<uint32_t> table(1 << 20, 0); uint64_t mask = table.size() - 1;
    auto hsh = [](const uint8_t* p, size_t n) { uint64_t h = 1469598103934665603ULL; for (size_t i = 0; i < n; i++) { h ^= p[i]; h *= 1099511628211ULL; } return h ^ (h >> 29); };
    auto keyOf = [&](int i) { return pair<const uint8_t*, size_t>(arena.data() + koff[i], koff[i + 1] - koff[i]); };
    auto rehash = [&]() {
        vector<uint32_t> nt(table.size() * 2, 0); uint64_t nm = nt.size() - 1;
        for (size_t i = 0; i + 1 < koff.size(); i++) { auto k = keyOf(i); uint64_t h = hsh(k.first, k.second) & nm; while (nt[h]) h = (h + 1) & nm; nt[h] = i + 1; }
        table.swap(nt); mask = nm;
    };
    auto findId = [&](const string& k) -> long {
        uint64_t h = hsh((const uint8_t*)k.data(), k.size()) & mask;
        while (table[h]) { int i = table[h] - 1; auto kk = keyOf(i); if (kk.second == k.size() && !memcmp(kk.first, k.data(), k.size())) return i; h = (h + 1) & mask; }
        return -1;
    };
    auto getId = [&](const St& s) -> int {
        string k = enc(s);
        uint64_t h = hsh((const uint8_t*)k.data(), k.size()) & mask;
        while (table[h]) { int i = table[h] - 1; auto kk = keyOf(i); if (kk.second == k.size() && !memcmp(kk.first, k.data(), k.size())) return i; h = (h + 1) & mask; }
        int n = koff.size() - 1; arena.insert(arena.end(), k.begin(), k.end()); koff.push_back(arena.size()); table[h] = n + 1;
        if ((uint64_t)(n + 1) * 2 > table.size()) rehash();
        return n;
    };
    auto keyStr = [&](int i) { auto k = keyOf(i); return string((const char*)k.first, k.second); };
    CSR G; G.st.push_back(0);
    // warm-up layers (warm < 3) are a DAG: expand them layer by layer without storing them; the steady
    // states they reach seed the main BFS
    {
        St s0; s0.pos = 0; s0.rp = 0; s0.warm = 0;
        vector<string> layer{enc(s0)}; long nwarm = 0;
        while (!layer.empty()) {
            unordered_set<string> nxt;
            for (auto& k : layer) {
                St s = dec(k);
                trans(s, [&](const St& t, int, const vector<int>&) { if (t.warm >= WARMR) getId(t); else nxt.insert(enc(t)); });
            }
            nwarm += layer.size();
            layer.assign(nxt.begin(), nxt.end());
        }
        fprintf(stderr, "warm-up states %ld, steady seeds %zu\n", nwarm, koff.size() - 1);
    }
    double tb = tnow();
    vector<pair<int,int>> loc;
    for (size_t q = 0; q + 1 < koff.size(); q++) {
        St s = dec(keyStr(q));
        loc.clear();
        trans(s, [&](const St& t, int X, const vector<int>&) { int to = getId(t); bool f = false; for (auto& a : loc) if (a.first == to) { a.second = min(a.second, X); f = true; } if (!f) loc.push_back({to, X}); });
        for (auto& a : loc) { G.to.push_back(a.first); G.w.push_back((int16_t)a.second); }
        G.st.push_back(G.to.size());
        if ((long)koff.size() > maxStates) { printf("{\"status\":\"STATE_LIMIT\",\"kind\":\"%s\",\"W\":%d}\n", kind.c_str(), W); return 2; }
        if (q % 2000000 == 0 && q) fprintf(stderr, "  q=%zu states=%zu edges=%zu arena=%zuMB %.0fs\n", q, koff.size() - 1, G.to.size(), arena.size() >> 20, tnow() - tb);
    }
    int N = koff.size() - 1;
    fprintf(stderr, "states %d edges %zu arena %zuMB, BFS %.0fs\n", N, G.to.size(), arena.size() >> 20, tnow() - tb);
    vector<int> cur(N, INT_MIN); vector<char> steady(N, 0);
    for (int u = 0; u < N; u++) { St s = dec(keyStr(u)); steady[u] = s.warm >= WARMR; if (s.pos == 0 && s.warm >= WARMR && (!ROWCOLOUR || s.rp == 0)) cur[u] = currentOf(s); }
    { long nst = 0; for (int u = 0; u < N; u++) nst += steady[u]; fprintf(stderr, "steady states %ld of %d\n", nst, N); }
    set<int> curVals; for (int u = 0; u < N; u++) if (cur[u] != INT_MIN) curVals.insert(cur[u]);
    // reverse CSR
    CSR R; { R.st.assign(N + 1, 0); for (int u = 0; u < N; u++) for (uint64_t e = G.st[u]; e < G.st[u + 1]; e++) R.st[G.to[e] + 1]++;
        for (int u = 0; u < N; u++) R.st[u + 1] += R.st[u]; R.to.resize(G.to.size()); vector<uint64_t> fill(R.st.begin(), R.st.end() - 1);
        for (int u = 0; u < N; u++) for (uint64_t e = G.st[u]; e < G.st[u + 1]; e++) R.to[fill[G.to[e]]++] = u; }
    for (int c : curVals) {
        vector<char> alive(N, 0);
        for (int u = 0; u < N; u++) alive[u] = steady[u] && (cur[u] == INT_MIN || cur[u] == c);
        vector<int> outd(N, 0), ind(N, 0);
        for (int u = 0; u < N; u++) if (alive[u]) for (uint64_t e = G.st[u]; e < G.st[u + 1]; e++) if (alive[G.to[e]]) { outd[u]++; ind[G.to[e]]++; }
        deque<int> dq; for (int u = 0; u < N; u++) if (alive[u] && (!outd[u] || !ind[u])) { alive[u] = 0; dq.push_back(u); }
        while (!dq.empty()) { int u = dq.front(); dq.pop_front();
            for (uint64_t e = R.st[u]; e < R.st[u + 1]; e++) { int p = R.to[e]; if (alive[p] && --outd[p] == 0) { alive[p] = 0; dq.push_back(p); } }
            for (uint64_t e = G.st[u]; e < G.st[u + 1]; e++) { int v = G.to[e]; if (alive[v] && --ind[v] == 0) { alive[v] = 0; dq.push_back(v); } } }
        int NA = 0; for (int u = 0; u < N; u++) NA += alive[u];
        if (!NA) { printf("{\"kind\":\"%s\",\"W\":%d,\"current\":%d,\"status\":\"NO_CYCLE\"}\n", kind.c_str(), W, c); continue; }
        fprintf(stderr, "  current %d: core %d\n", c, NA);
        vector<int> cyc; ll sumC; int L; bool cert;
        mmc(N, G, alive, NA, cyc, sumC, L, cert);
        if (cyc.empty()) { printf("{\"kind\":\"%s\",\"W\":%d,\"current\":%d,\"status\":\"%s\",\"lower_bound_per_row\":\"%s\",\"states\":%d,\"core\":%d}\n", kind.c_str(), W, c, cert ? "CERTIFIED_LOWER_BOUND" : "UNCERTIFIED", getenv("LAMBDA"), N, NA); continue; }
        { int k = 0; while (k < (int)cyc.size() && dec(keyStr(cyc[k])).pos != 0) k++; rotate(cyc.begin(), cyc.begin() + (k % cyc.size()), cyc.end()); }
        int rows = L / NP;
        printf("{\"kind\":\"%s\",\"W\":%d,\"A\":%d,\"OFF\":%d,\"current\":%d,\"status\":\"%s\",\"states\":%d,\"core\":%d,\"rows\":%d,\"crossings\":%lld,\"rate_per_row\":\"%lld/%d\",\"rate\":%.6f,\"edges\":[",
               kind.c_str(), W, A, OFF, c, cert ? "CERTIFIED" : "UNCERTIFIED", N, NA, rows, sumC, sumC, rows, (double)sumC / rows);
        bool first = true; int row = 0;
        for (int i = 0; i < L; i++) {
            St s = dec(keyStr(cyc[i])); int to = cyc[(i + 1) % L]; int want = 1 << 30;
            for (uint64_t e = G.st[cyc[i]]; e < G.st[cyc[i] + 1]; e++) if ((int)G.to[e] == to) want = min(want, (int)G.w[e]);
            bool found = false;
            trans(s, [&](const St& t, int X, const vector<int>& chs) {
                if (found || X != want || findId(enc(t)) != to) return; found = true;
                const Pos& p = P[s.pos]; int x = p.u + OFF + A * row, y = row;
                for (int m : chs) { printf("%s[%d,%d,%d,%d]", first ? "" : ",", x, y, x + UPM[m][0], y + UPM[m][1]); first = false; }
            });
            if (!found) { fprintf(stderr, "reconstruct failed\n"); return 3; }
            if (s.pos == NP - 1) row++;
        }
        printf("]}\n");
    }
    return 0;
}
