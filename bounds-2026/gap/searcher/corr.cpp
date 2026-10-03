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
static set<pii> baseNbrs(int x, int y) {
    set<pii> s; pii d = FIELD(x, y); s.insert({x + d.first, y + d.second});
    for (auto& m : KM) { int qx = x - m[0], qy = y - m[1]; pii e = FIELD(qx, qy); if (e.first == m[0] && e.second == m[1]) s.insert({qx, qy}); }
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
struct PE { int sdy, sp, m, lab; };
struct St { int pos, rp, warm; vector<PE> e; };
// planar coordinates of a pending edge relative to current row 0 (rowpar handled by colour only)
static inline void srcXY(const PE& p, int& x, int& y) { y = p.sdy; x = P[p.sp].u + A * y + OFF; }

string enc(const St& s) {
    string k; k.reserve(3 + 2 * s.e.size());
    k.push_back((char)s.pos); k.push_back((char)(s.rp | (s.warm << 1)));
    for (auto& p : s.e) { k.push_back((char)((p.sdy + 2) * NP + p.sp)); k.push_back((char)(p.m | (p.lab << 2))); }
    return k;
}
St dec(const string& k) {
    St s; s.pos = (unsigned char)k[0]; s.rp = k[1] & 1; s.warm = (unsigned char)k[1] >> 1;
    for (size_t i = 2; i < k.size(); i += 2) { int a = (unsigned char)k[i], b = (unsigned char)k[i + 1]; s.e.push_back({a / NP - 2, a % NP, b & 3, b >> 2}); }
    return s;
}
int TARGET_SET = 0, TARGET = 0;
int ROWCOLOUR;   // 1 if the colour of (u, row) alternates with the row (A even)

// current through the cut below the current row (only meaningful at pos == 0)
int currentOf(const St& s) {
    int c = 0;
    for (auto& p : s.e) { int x, y; srcXY(p, x, y); int ch = chiOf(x, y); if (ROWCOLOUR && s.rp) ch = -ch; c += ch; }
    return c;
}

// canonicalise: sort entries and rewrite partner indices
St canon(vector<PE> e, vector<int> partner /* index into e or -1 ray, -2 inert */, int pos, int rp, int warm) {
    int n = e.size(); vector<int> ord(n); iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int a, int b) { return make_tuple(e[a].sdy, e[a].sp, e[a].m) < make_tuple(e[b].sdy, e[b].sp, e[b].m); });
    vector<int> where(n); for (int i = 0; i < n; i++) where[ord[i]] = i;
    St s; s.pos = pos; s.rp = rp; s.warm = warm;
    for (int i = 0; i < n; i++) { PE p = e[ord[i]]; int q = partner[ord[i]]; p.lab = q == -1 ? RAY : (q == -2 ? INERT : where[q]); s.e.push_back(p); }
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
    if (npos == NP) { npos = 0; shift = 1; nrp ^= 1; nwarm = min(3, s.warm + 1); }
    auto finish = [&](vector<PE> e, vector<int> partner, int X, const vector<int>& chosen) {
        // drop nothing (incoming already removed); shift rows
        if (shift) for (auto& p : e) p.sdy -= 1;
        for (auto& p : e) if (p.sdy < -2) { fprintf(stderr, "sdy underflow\n"); exit(1); }
        St t = canon(e, partner, npos, nrp, nwarm);
        if (shift && nwarm >= 3 && TARGET_SET && (!ROWCOLOUR || nrp == 0) && currentOf(t) != TARGET) return;
        cb(t, X, chosen);
    };
    // base: copy of rest with partner indices remapped
    vector<int> idxNew(n, -1); vector<PE> e0; vector<int> part0;
    for (int i : rest) { idxNew[i] = e0.size(); e0.push_back(s.e[i]); }
    auto partnerOld = [&](int i) { int l = s.e[i].lab; return l == RAY ? -1 : (l == INERT ? -2 : l); };
    for (int i : rest) { int q = partnerOld(i); part0.push_back(q >= 0 ? idxNew[q] : q); }
    if (!cp.band) {
        // outside cell: incoming edges are forced band->outside edges (INERT); add forced up-edges (RAY)
        for (int i : inc) if (s.e[i].lab != INERT) { fprintf(stderr, "ghost got non-inert edge\n"); exit(1); }
        vector<PE> e = e0; vector<int> part = part0; int X = 0; vector<PE> added;
        for (int m : cp.forcedUp) {
            int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
            if (++fut[{tx, ty}] > 2) return;
            X += edgeCross(cx, cy, tx, ty, added, 0);
            PE p{0, s.pos, m, RAY}; e.push_back(p); part.push_back(-1); added.push_back(p);
        }
        finish(e, part, X, {});
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
    int lo = s.warm >= 3 ? need : 0;
    for (int k = lo; k <= need; k++) {
        // choose k of cand
        vector<int> sel(k);
        function<void(int, int)> rec = [&](int start, int d) {
            if (d == k) {
                vector<PE> e = e0; vector<int> part = part0; int X = 0; vector<PE> added;
                map<pii, int> f2 = fut;
                // forced up edges (to outside): INERT entries; free edges
                vector<int> newIdx;   // indices in e of new free edges
                for (int m : cp.forcedUp) {
                    int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
                    X += edgeCross(cx, cy, tx, ty, added, 0);
                    PE p{0, s.pos, m, INERT}; e.push_back(p); part.push_back(-2); added.push_back(p);
                }
                for (int m : sel) {
                    int tx = cx + UPM[m][0], ty = cy + UPM[m][1];
                    if (++f2[{tx, ty}] > 2) return;
                    X += edgeCross(cx, cy, tx, ty, added, 0);
                    PE p{0, s.pos, m, RAY}; newIdx.push_back(e.size()); e.push_back(p); part.push_back(-1); added.push_back(p);
                }
                // connectors at this cell: incoming (partner known), forced-up (ray), new free (to assign)
                // represent each connector as: type 0 = existing end with partner p (index in e, -1 ray), type 1 = new edge index
                vector<pii> con;
                for (int i : inc) { int q = partnerOld(i); con.push_back({0, q >= 0 ? idxNew[q] : -1}); }
                for (int j = 0; j < nfu; j++) con.push_back({0, -1});
                for (int j : newIdx) con.push_back({1, j});
                while ((int)con.size() < 2) con.push_back({0, -1});   // warm-up: dangling = ray
                // incoming partner could itself be incoming (both ends arriving here) -> closes a cycle
                if (ninc == 2) {
                    int q0 = partnerOld(inc[0]);
                    if (q0 == inc[1]) return;   // finite cycle
                }
                auto c0 = con[0], c1 = con[1];
                // "far end" of each connector: for existing ends, partner index p (or -1 ray); new edge j is its own end
                if (c0.first == 1 && c1.first == 1) { part[c0.second] = c1.second; part[c1.second] = c0.second; }
                else if (c0.first == 1 || c1.first == 1) {
                    int j = c0.first == 1 ? c0.second : c1.second; int p = c0.first == 1 ? c1.second : c0.second;
                    part[j] = p; if (p >= 0) part[p] = j;
                } else {
                    int p = c0.second, q = c1.second;
                    if (p >= 0 && q >= 0) { part[p] = q; part[q] = p; }
                    else if (p >= 0) part[p] = -1;
                    else if (q >= 0) part[q] = -1;
                }
                finish(e, part, X, sel);
                return;
            }
            for (int i = start; i < (int)cand.size(); i++) { sel[d] = cand[i]; rec(i + 1, d + 1); }
        };
        rec(0, 0);
    }
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 3) { fprintf(stderr, "usage: corr KIND W [maxstates] [target]\n"); return 1; }
    string kind = argv[1]; W = atoi(argv[2]);
    long maxStates = argc > 3 ? atol(argv[3]) : 50000000;
    if (argc > 4) { TARGET_SET = 1; TARGET = atoi(argv[4]); }
    OFF = -(W / 2);
    auto uni = [](int fx, int fy) { return function<pii(int,int)>([fx, fy](int, int) { return pii(fx, fy); }); };
    if (kind == "diag") { A = 1; FIELD = [](int x, int y) { return x - y <= -1 ? pii(2, 1) : pii(-1, -2); }; }
    else if (kind == "diag21") { A = 1; FIELD = uni(2, 1); }
    else if (kind == "diag12") { A = 1; FIELD = uni(1, 2); }
    else if (kind == "anti21") { A = -1; FIELD = uni(2, 1); }
    else if (kind == "anti12") { A = -1; FIELD = uni(1, 2); }
    else if (kind == "mid") { A = 0; FIELD = [](int x, int y) { (void)y; return x <= -1 ? pii(1, 2) : pii(1, -2); }; }
    else if (kind == "vert12") { A = 0; FIELD = uni(1, 2); }
    else if (kind == "vert21") { A = 0; FIELD = uni(2, 1); }
    else if (kind.rfind("d21_", 0) == 0) { A = atoi(kind.c_str() + 4); FIELD = uni(2, 1); }
    else if (kind.rfind("d12_", 0) == 0) { A = atoi(kind.c_str() + 4); FIELD = uni(1, 2); }
    else { fprintf(stderr, "unknown kind\n"); return 1; }
    ROWCOLOUR = (A % 2 == 0);
    // positions of row 0
    int G = 3 + abs(A);
    for (int u = -G; u < W + G; u++) {
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
    // BFS
    unordered_map<string, int> id; vector<string> keys; vector<vector<pii>> G2;
    auto getId = [&](const St& s) { string k = enc(s); auto it = id.find(k); if (it != id.end()) return it->second; int nn = keys.size(); id.emplace(k, nn); keys.push_back(k); G2.emplace_back(); return nn; };
    St s0; s0.pos = 0; s0.rp = 0; s0.warm = 0; getId(s0);
    for (size_t q = 0; q < keys.size(); q++) {
        St s = dec(keys[q]);
        map<int, int> best;
        trans(s, [&](const St& t, int X, const vector<int>&) { int to = getId(t); auto it = best.find(to); if (it == best.end() || it->second > X) best[to] = X; });
        G2[q].assign(best.begin(), best.end());
        if ((long)keys.size() > maxStates) { printf("{\"status\":\"STATE_LIMIT\",\"kind\":\"%s\",\"W\":%d}\n", kind.c_str(), W); return 2; }
        if (q % 1000000 == 0 && q) fprintf(stderr, "  q=%zu states=%zu\n", q, keys.size());
    }
    int N = keys.size();
    fprintf(stderr, "states %d\n", N);
    // boundary states with warm 3: currents; check conservation along transitions between boundary states later via cycles
    vector<int> cur(N, INT_MIN); vector<char> steady(N, 0);
    for (int u = 0; u < N; u++) { St s = dec(keys[u]); steady[u] = s.warm >= 3; if (s.pos == 0 && s.warm >= 3 && (!ROWCOLOUR || s.rp == 0)) cur[u] = currentOf(s); }
    set<int> curVals; for (int u = 0; u < N; u++) if (cur[u] != INT_MIN) curVals.insert(cur[u]);
    // also check conservation: for every steady boundary state, the next boundary states reachable have equal current
    // (done implicitly: report per current value)
    for (int c : curVals) {
        vector<char> alive(N, 0);
        for (int u = 0; u < N; u++) alive[u] = steady[u] && (cur[u] == INT_MIN || cur[u] == c);
        // trim to states on cycles
        vector<int> outd(N, 0), ind(N, 0); vector<vector<int>> pred(N);
        for (int u = 0; u < N; u++) if (alive[u]) for (auto& a : G2[u]) if (alive[a.first]) { outd[u]++; ind[a.first]++; pred[a.first].push_back(u); }
        deque<int> dq; for (int u = 0; u < N; u++) if (alive[u] && (!outd[u] || !ind[u])) { alive[u] = 0; dq.push_back(u); }
        while (!dq.empty()) { int u = dq.front(); dq.pop_front();
            for (int p : pred[u]) if (alive[p] && --outd[p] == 0) { alive[p] = 0; dq.push_back(p); }
            for (auto& a : G2[u]) if (alive[a.first] && --ind[a.first] == 0) { alive[a.first] = 0; dq.push_back(a.first); } }
        int NA = 0; for (int u = 0; u < N; u++) NA += alive[u];
        if (!NA) { printf("{\"kind\":\"%s\",\"W\":%d,\"current\":%d,\"status\":\"NO_CYCLE\"}\n", kind.c_str(), W, c); continue; }
        typedef long double LD; const LD eps = 1e-9;
        vector<int> pol(N, -1); vector<LD> eta(N), xv(N);
        for (int u = 0; u < N; u++) if (alive[u]) { int bj = -1; for (int j = 0; j < (int)G2[u].size(); j++) if (alive[G2[u][j].first] && (bj < 0 || G2[u][j].second < G2[u][bj].second)) bj = j; pol[u] = bj; }
        for (int it = 0; it < 100000; it++) {
            vector<int> color(N, 0), path;
            for (int s0i = 0; s0i < N; s0i++) if (alive[s0i] && !color[s0i]) {
                path.clear(); int u = s0i;
                while (!color[u]) { color[u] = 1; path.push_back(u); u = G2[u][pol[u]].first; }
                if (color[u] == 1) {
                    LD sum = 0; int len = 0, v = u; do { sum += G2[v][pol[v]].second; len++; v = G2[v][pol[v]].first; } while (v != u);
                    LD e = sum / len; vector<int> cyc; v = u; do { cyc.push_back(v); v = G2[v][pol[v]].first; } while (v != u);
                    eta[u] = e; xv[u] = 0; color[u] = 2;
                    for (int i = cyc.size() - 1; i >= 1; i--) { int w = cyc[i]; eta[w] = e; xv[w] = G2[w][pol[w]].second - e + xv[G2[w][pol[w]].first]; color[w] = 2; }
                }
                for (int i = path.size() - 1; i >= 0; i--) { int w = path[i]; if (color[w] == 2) continue; int nx = G2[w][pol[w]].first; eta[w] = eta[nx]; xv[w] = G2[w][pol[w]].second - eta[nx] + xv[nx]; color[w] = 2; }
            }
            bool ch = false;
            for (int u = 0; u < N; u++) if (alive[u]) { int bj = pol[u]; LD be = eta[G2[u][bj].first]; for (int j = 0; j < (int)G2[u].size(); j++) { int v = G2[u][j].first; if (alive[v] && eta[v] < be - eps) { be = eta[v]; bj = j; } } if (bj != pol[u]) { pol[u] = bj; ch = true; } }
            if (!ch) for (int u = 0; u < N; u++) if (alive[u]) { int bj = pol[u]; LD bv = G2[u][bj].second - eta[u] + xv[G2[u][bj].first];
                for (int j = 0; j < (int)G2[u].size(); j++) { int v = G2[u][j].first; if (!alive[v] || fabsl(eta[v] - eta[u]) > eps) continue; LD val = G2[u][j].second - eta[u] + xv[v]; if (val < bv - eps) { bv = val; bj = j; } }
                if (bj != pol[u]) { pol[u] = bj; ch = true; } }
            if (!ch) break;
        }
        int bu = -1; for (int u = 0; u < N; u++) if (alive[u] && (bu < 0 || eta[u] < eta[bu])) bu = u;
        { vector<char> seen(N, 0); int u = bu; while (!seen[u]) { seen[u] = 1; u = G2[u][pol[u]].first; } bu = u; }
        // rotate cycle to start at a row boundary
        vector<int> cyc; { int u = bu; do { cyc.push_back(u); u = G2[u][pol[u]].first; } while (u != bu); }
        { int k = 0; while (k < (int)cyc.size() && dec(keys[cyc[k]]).pos != 0) k++; rotate(cyc.begin(), cyc.begin() + (k % cyc.size()), cyc.end()); }
        ll sumC = 0; for (int u : cyc) sumC += G2[u][pol[u]].second; int L = cyc.size();
        bool cert = true;
        { vector<ll> d(N, 0); vector<char> inq(N, 0); vector<int> cnt(N, 0); deque<int> q;
          for (int u = 0; u < N; u++) if (alive[u]) { q.push_back(u); inq[u] = 1; }
          while (!q.empty() && cert) { int u = q.front(); q.pop_front(); inq[u] = 0;
            for (auto& a : G2[u]) if (alive[a.first]) { ll w = (ll)a.second * L - sumC; if (d[u] + w < d[a.first]) { d[a.first] = d[u] + w;
                if (!inq[a.first]) { if (++cnt[a.first] > NA + 1) { cert = false; break; } q.push_back(a.first); inq[a.first] = 1; } } } } }
        // witness: edges (x1,y1,x2,y2) in planar coordinates, rows counted from 0 at the cycle start
        int rows = L / NP;
        printf("{\"kind\":\"%s\",\"W\":%d,\"A\":%d,\"OFF\":%d,\"current\":%d,\"status\":\"%s\",\"states\":%d,\"core\":%d,\"rows\":%d,\"crossings\":%lld,\"rate_per_row\":\"%lld/%d\",\"rate\":%.6f,\"edges\":[",
               kind.c_str(), W, A, OFF, c, cert ? "CERTIFIED" : "UNCERTIFIED", N, NA, rows, sumC, sumC, rows, (double)sumC / rows);
        bool first = true; int row = 0;
        for (int i = 0; i < L; i++) {
            St s = dec(keys[cyc[i]]); int to = G2[cyc[i]][pol[cyc[i]]].first, want = G2[cyc[i]][pol[cyc[i]]].second; bool found = false;
            trans(s, [&](const St& t, int X, const vector<int>& chs) {
                if (found || X != want || id[enc(t)] != to) return; found = true;
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
