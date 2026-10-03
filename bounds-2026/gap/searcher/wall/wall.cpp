// wall.cpp - wall tension of a straight periodic defect band (KT Edge Searcher, 2026-10-03).
// Step A of gap/searcher/PLAN.md.
//
// Geometry: a cell (u, y) of the scan is the board cell (x, y) = (u + A*y, y). Modeled cells: 0 <= u < WM,
// degree exactly 2. Ghost cells: every other cell that is a knight neighbour of a modeled cell; degree <= 2,
// edges only to modeled cells. So every edge with a modeled end is represented. No cycle (path labels).
// The scan goes row by row, cells in increasing u; an edge is chosen at its lower end.
//
// Squares: [X, X+1] x [Y, Y+1]. A square is COMPLETE if every knight edge whose tile covers one of its quarters has
// a modeled end. The complete squares of a square row form an interval; the KM leftmost and KM rightmost are
// MARGIN squares: all 4 quarters must have multiplicity exactly 1. The others are COST squares.
// Cost per row = G + W3 + X1 (G: uncovered quarters in cost squares, W3: sum binom(m-1,2) in cost squares,
// X1: crossing pairs of represented edges whose tiles share exactly one quarter). By the identity
// E = (G + X1 + W3)/2 (PLAN.md section 1) the band's share of E is cost/2.
// psi jump: sum over the vertical grid edges between consecutive complete squares of chi(a)(m_+ + m_- + 1) mod 3
// (audited flux formula (2)); MODE nz requires != 0 at every row end, MODE zero requires == 0, MODE any none.
// Warm-up: the first WU rows have modeled degree <= 2 and no checks, so every periodic configuration is a
// cycle of the strict part of the graph.
// Result: min mean cost per row over all cycles (exact: Dinkelbach + integer Bellman-Ford).
//
// usage: wall A WM KM MODE [P Q]      (start ratio P/Q, default 8/1)
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; typedef unsigned long long ull;
int A, WM, KM; string MODE; const int WU = 3;
int ULO, UHI, NC;                         // scan columns u in [ULO, UHI]
const int MDX[4] = {2, -2, 1, -1}, MDY[4] = {1, 1, 2, 2};
static bool modeled(int u) { return u >= 0 && u < WM; }
static ll orient(ll ax, ll ay, ll bx, ll by, ll cx, ll cy) { ll v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax); return (v > 0) - (v < 0); }
static bool crossR(ll a, ll b, ll c, ll d, ll e, ll f, ll g, ll h) { return orient(a, b, c, d, e, f) * orient(a, b, c, d, g, h) < 0 && orient(e, f, g, h, a, b) * orient(e, f, g, h, c, d) < 0; }
// ---- tiles: quarters (dX, dY, q) relative to the lower end, per upward move; q: 0 bottom 1 right 2 top 3 left
vector<array<int, 3>> TQ[4];
static void makeTiles() {
    for (int m = 0; m < 4; m++) {
        int dx = MDX[m], dy = MDY[m];   // scaled by 6
        ll ax = 0, ay = 0, cx = 6 * dx, cy = 6 * dy, mx = 3 * dx, my = 3 * dy;
        ll sx = abs(dx) == 2 ? 0 : 3, sy = abs(dx) == 2 ? 3 : 0;
        ll P[4][2] = {{ax, ay}, {mx - sx, my - sy}, {cx, cy}, {mx + sx, my + sy}};
        auto inside = [&](ll px, ll py) {
            int sg = 0;
            for (int k = 0; k < 4; k++) { ll ux = P[k][0], uy = P[k][1], vx = P[(k + 1) % 4][0], vy = P[(k + 1) % 4][1];
                ll cr = (vx - ux) * (py - uy) - (vy - uy) * (px - ux); if (cr == 0) return false; int s2 = cr > 0 ? 1 : -1;
                if (!sg) sg = s2; else if (s2 != sg) return false; }
            return true;
        };
        for (int i = min(0, dx); i < max(0, dx); i++) for (int j = 0; j < dy; j++) {
            ll C[4][2] = {{6 * i + 3, 6 * j + 1}, {6 * i + 5, 6 * j + 3}, {6 * i + 3, 6 * j + 5}, {6 * i + 1, 6 * j + 3}};
            for (int q = 0; q < 4; q++) if (inside(C[q][0], C[q][1])) TQ[m].push_back({i, j, q});
        }
        if (TQ[m].size() != 4) { fprintf(stderr, "tile error\n"); exit(1); }
    }
}
// ---- slots
struct Slot { int c, ly, m, tc, ty; };
vector<Slot> SL; int SID[64][3][4];
int sqClass[256]; const int SOFF = 128;   // class of square by s = X - A*Y: 0 incomplete, 1 margin, 2 cost
int sLo, sHi;                              // complete squares s in [sLo, sHi]
struct Key { ull m[3]; ull l[2]; uint8_t x, warm; bool operator==(const Key& o) const { return !memcmp(this, &o, sizeof(Key)); } };
struct PE { int c, ly, m, comp; };        // lower end column index c (u = c + ULO), row ly; move m
static Key encode(int x, int warm, const vector<PE>& e) {
    Key k; memset(&k, 0, sizeof k); k.x = x; k.warm = warm; int li = 0;
    for (auto& p : e) { int s = SID[p.c][p.ly + 2][p.m]; k.m[s >> 6] |= 1ULL << (s & 63); k.l[li >> 4] |= (ull)p.comp << (4 * (li & 15)); li++; }
    return k;
}
static void decode(const Key& k, vector<PE>& e) {
    e.clear(); int li = 0;
    for (int s = 0; s < (int)SL.size(); s++) if (k.m[s >> 6] >> (s & 63) & 1) { e.push_back({SL[s].c, SL[s].ly, SL[s].m, (int)(k.l[li >> 4] >> (4 * (li & 15)) & 15)}); li++; }
}
vector<Key> keys; vector<uint32_t> tab; ull tmask;
static ull hk(const Key& k) { ull h = 1469598103934665603ULL; const unsigned char* p = (const unsigned char*)&k; for (size_t i = 0; i < sizeof(Key); i++) { h ^= p[i]; h *= 1099511628211ULL; } h ^= h >> 29; return h; }
static void rehash(int lg) { tab.assign(1ULL << lg, ~0u); tmask = (1ULL << lg) - 1; for (uint32_t i = 0; i < keys.size(); i++) { ull h = hk(keys[i]) & tmask; while (tab[h] != ~0u) h = (h + 1) & tmask; tab[h] = i; } }
static uint32_t getId(const Key& k) {
    ull h = hk(k) & tmask;
    while (tab[h] != ~0u) { if (keys[tab[h]] == k) return tab[h]; h = (h + 1) & tmask; }
    uint32_t id = keys.size(); keys.push_back(k); tab[h] = id;
    if (keys.size() * 2 > tab.size()) rehash(__builtin_ctzll(tab.size()) + 1);
    return id;
}
// real coordinates of a slot end (row ly relative to the current row 0)
static inline ll RX(int c, int y) { return (ll)(c + ULO) + (ll)A * y; }

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 5) { fprintf(stderr, "usage: wall A WM KM nz|zero|any [P Q] [cap]\n"); return 1; }
    A = atoi(argv[1]); WM = atoi(argv[2]); KM = atoi(argv[3]); MODE = argv[4];
    ll P = argc > 6 ? atoll(argv[5]) : 8, Q = argc > 6 ? atoll(argv[6]) : 1; size_t CAP = argc > 7 ? atoll(argv[7]) : 400000000;
    auto T0 = chrono::steady_clock::now(); auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
    makeTiles();
    int dmin = 0, dmax = 0;
    for (int m = 0; m < 4; m++) { int du = MDX[m] - A * MDY[m]; dmin = min({dmin, du, -du}); dmax = max({dmax, du, -du}); }
    ULO = dmin; UHI = WM - 1 + dmax; NC = UHI - ULO + 1;
    if (NC > 64) { printf("too many columns\n"); return 1; }
    memset(SID, -1, sizeof SID);
    for (int c = 0; c < NC; c++) for (int ly = -2; ly <= 0; ly++) for (int m = 0; m < 4; m++) {
        int tc = c + MDX[m] - A * MDY[m], ty = ly + MDY[m];
        if (ty < 0 || tc < 0 || tc >= NC) continue;
        if (!modeled(c + ULO) && !modeled(tc + ULO)) continue;
        SID[c][ly + 2][m] = SL.size(); SL.push_back({c, ly, m, tc, ty});
    }
    if (SL.size() > 192) { printf("too many slots %zu\n", SL.size()); return 1; }
    // ---- square classes (square row Y = 0, X = s)
    memset(sqClass, 0, sizeof sqClass); sLo = 1 << 30; sHi = -(1 << 30);
    for (int X = -40; X <= 60; X++) {
        bool comp = true, any = false;
        for (int x1 = X - 2; x1 <= X + 3; x1++) for (int y1 = -2; y1 <= 1; y1++) for (int m = 0; m < 4; m++) {
            bool cov = false;
            for (auto& t : TQ[m]) if (x1 + t[0] == X && y1 + t[1] == 0) cov = true;
            if (!cov) continue;
            any = true;
            int x2 = x1 + MDX[m], y2 = y1 + MDY[m];
            if (!modeled(x1 - A * y1) && !modeled(x2 - A * y2)) comp = false;
        }
        if (comp && any) { sqClass[X + SOFF] = 2; sLo = min(sLo, X); sHi = max(sHi, X); }
    }
    for (int X = sLo; X <= sHi; X++) if (sqClass[X + SOFF] != 2) { printf("complete squares not an interval\n"); return 1; }
    for (int k = 0; k < KM; k++) { sqClass[sLo + k + SOFF] = 1; sqClass[sHi - k + SOFF] = 1; }
    int ncost = 0; for (int X = sLo; X <= sHi; X++) ncost += sqClass[X + SOFF] == 2;
    printf("A=%d WM=%d KM=%d MODE=%s: columns u in [%d,%d], %zu slots, complete squares s in [%d,%d], %d cost squares per row\n",
           A, WM, KM, MODE.c_str(), ULO, UHI, SL.size(), sLo, sHi, ncost);
    // ---- graph
    rehash(20);
    { vector<PE> e0; getId(encode(0, WU, e0)); }
    vector<ull> off{0}; vector<uint32_t> tgt; vector<uint8_t> wgt; vector<uint8_t> isRowEnd;
    vector<PE> s, in, rest, ne;
    long rejM = 0, rejPsi = 0;
    for (size_t q = 0; q < keys.size(); q++) {
        if (keys.size() > CAP) { size_t cw[4] = {0, 0, 0, 0}, cx[4] = {0,0,0,0}; for (size_t i = 0; i < q; i++) cw[keys[i].warm]++; for (size_t i = q; i < keys.size(); i++) cx[keys[i].warm]++; printf("CAP reached: %zu states (processed %zu) %.0fs; processed by warm 0..3: %zu %zu %zu %zu; queued: %zu %zu %zu %zu\n", keys.size(), q, el(), cw[0], cw[1], cw[2], cw[3], cx[0], cx[1], cx[2], cx[3]); return 0; }
        Key kq = keys[q]; int x = kq.x, warm = kq.warm; decode(kq, s);
        in.clear(); rest.clear();
        for (auto& p : s) { auto& S = SL[SID[p.c][p.ly + 2][p.m]]; (S.tc == x && S.ty == 0 ? in : rest).push_back(p); }
        int din = in.size(); bool isMod = modeled(x + ULO);
        bool ok0 = din <= 2 && !(din == 2 && in[0].comp == in[1].comp);
        vector<pair<uint32_t, uint8_t>> outs;
        if (ok0) {
            vector<int> cand; for (int m = 0; m < 4; m++) if (SID[x][2][m] >= 0) cand.push_back(m);
            int nc = cand.size();
            for (int msk = 0; msk < (1 << nc); msk++) {
                int r = __builtin_popcount(msk);
                if (din + r > 2) continue;
                if (isMod && !warm && din + r != 2) continue;
                vector<int> ch; for (int i = 0; i < nc; i++) if (msk >> i & 1) ch.push_back(cand[i]);
                bool ok = true;
                for (int m : ch) { auto& S = SL[SID[x][2][m]]; int dg = 0; for (auto& p : rest) { auto& T = SL[SID[p.c][p.ly + 2][p.m]]; if (T.tc == S.tc && T.ty == S.ty) dg++; } for (int m2 : ch) { auto& S2 = SL[SID[x][2][m2]]; if (S2.tc == S.tc && S2.ty == S.ty) dg++; } if (dg > 2) ok = false; }
                if (!ok) continue;
                // crossings of new edges, X1 and margin overlap pruning
                int x1c = 0;
                auto edgeR = [&](int c, int ly, int m, ll* E) { E[0] = RX(c, ly); E[1] = ly; E[2] = E[0] + MDX[m]; E[3] = ly + MDY[m]; };
                auto pairCheck = [&](const ll* e, int me, const ll* f, int mf) {
                    if (!crossR(e[0], e[1], e[2], e[3], f[0], f[1], f[2], f[3])) return;
                    int ov = 0;
                    for (auto& a : TQ[me]) for (auto& b : TQ[mf]) {
                        ll X1 = e[0] + a[0], Y1 = e[1] + a[1], X2 = f[0] + b[0], Y2 = f[1] + b[1];
                        if (X1 == X2 && Y1 == Y2 && a[2] == b[2]) { ov++; if (!warm && sqClass[(int)(X1 - (ll)A * Y1) + SOFF] == 1) ok = false; }
                    }
                    if (ov < 1 || ov > 2) { fprintf(stderr, "overlap error %d\n", ov); exit(1); }
                    if (ov == 1) x1c++;
                };
                for (size_t i = 0; i < ch.size() && ok; i++) {
                    ll e[4]; edgeR(x, 0, ch[i], e);
                    for (auto& p : rest) { ll f[4]; edgeR(p.c, p.ly, p.m, f); pairCheck(e, ch[i], f, p.m); }
                    for (size_t j = 0; j < i; j++) { ll f[4]; edgeR(x, 0, ch[j], f); pairCheck(e, ch[i], f, ch[j]); }
                }
                if (!ok) { rejM++; continue; }
                const int NEW = 100; int label = din ? in[0].comp : NEW, merge = din == 2 ? in[1].comp : -1;
                ne.clear();
                for (auto p : rest) { if (merge >= 0 && p.comp == merge) p.comp = label; ne.push_back(p); }
                for (int m : ch) ne.push_back({x, 0, m, label});
                int nx = x + 1, sh = 0, nwarm = warm; if (nx == NC) { nx = 0; sh = 1; if (nwarm) nwarm--; }
                for (auto& p : ne) p.ly -= sh;
                int w = x1c;
                if (sh && !warm) {
                    // square row Y = -1 (between rows -1 and 0 of the new frame): multiplicities from pending edges
                    int span = sHi - sLo + 1; vector<array<int, 4>> mm(span, {0, 0, 0, 0});
                    for (auto& p : ne) {
                        ll ex = RX(p.c, p.ly);
                        for (auto& t : TQ[p.m]) { ll X = ex + t[0], Y = p.ly + t[1]; if (Y != -1) continue; ll sidx = X + A; if (sidx >= sLo && sidx <= sHi) mm[sidx - sLo][t[2]]++; }
                    }
                    int G = 0, W3 = 0; bool good = true;
                    for (int i = 0; i < span; i++) {
                        int cl = sqClass[sLo + i + SOFF];
                        for (int qq = 0; qq < 4; qq++) { int mv = mm[i][qq];
                            if (cl == 1 && mv != 1) good = false;
                            if (cl == 2) { if (mv == 0) G++; if (mv >= 3) W3 += (mv - 1) * (mv - 2) / 2; } }
                    }
                    if (!good) { rejM++; continue; }
                    // psi jump: grid edges between squares i-1 and i (real X = sLo + i - A), chi relative (-1)^X
                    int psi = 0;
                    for (int i = 1; i < span; i++) { int X = sLo + i - A; int chi = (X & 1) ? -1 : 1; psi += chi * (mm[i - 1][1] + mm[i][3] + 1); }
                    psi = ((psi % 3) + 3) % 3;
                    if ((MODE == "nz" && psi == 0) || (MODE == "zero" && psi != 0)) { rejPsi++; continue; }
                    w += G + W3;
                } else if (warm) w = 0;
                sort(ne.begin(), ne.end(), [&](const PE& a, const PE& b) { return SID[a.c][a.ly + 2][a.m] < SID[b.c][b.ly + 2][b.m]; });
                int rl[128]; memset(rl, -1, sizeof rl); int nl = 0;
                for (auto& p : ne) { if (rl[p.comp] < 0) rl[p.comp] = nl++; p.comp = rl[p.comp]; }
                if (nl > 15 || ne.size() > 32) { printf("label overflow\n"); return 1; }
                if (w > 255) { printf("weight overflow\n"); return 1; }
                outs.push_back({getId(encode(nx, nwarm, ne)), (uint8_t)w});
            }
        }
        sort(outs.begin(), outs.end());
        for (size_t i = 0; i < outs.size(); i++) {
            if (i && outs[i].first == outs[i - 1].first) { if (outs[i].second < wgt.back()) wgt.back() = outs[i].second; continue; }   // min weight per target
            tgt.push_back(outs[i].first); wgt.push_back(outs[i].second); isRowEnd.push_back(x == NC - 1);
        }
        off.push_back(tgt.size());
        if (q && (q & ((1 << 22) - 1)) == 0) printf("  ... %zu/%zu states, %zu arcs, %.0fs\n", q, keys.size(), tgt.size(), el());
    }
    size_t N = keys.size(), M = tgt.size();
    { size_t cw[4] = {0, 0, 0, 0}; for (auto& k : keys) cw[k.warm]++; printf("states by warm level: strict %zu, warm1 %zu, warm2 %zu, warm3 %zu\n", cw[0], cw[1], cw[2], cw[3]); }
    printf("graph: states %zu arcs %zu (rejected: margin %ld, psi %ld) %.0fs\n", N, M, rejM, rejPsi, el());
    // ---- min mean cost per row: Dinkelbach with exact Bellman-Ford (weights Q*w - P per row end)
    vector<ll> d(N); vector<uint32_t> par(N), src(M);
    for (size_t u = 0; u < N; u++) for (ull i = off[u]; i < off[u + 1]; i++) src[i] = u;
    vector<uint32_t> cyc;
    auto bf = [&](ll p, ll q) {
        fill(d.begin(), d.end(), 0); fill(par.begin(), par.end(), ~0u); vector<uint8_t> col(N);
        for (int pass = 1;; pass++) {
            bool chg = false;
            for (size_t u = 0; u < N; u++) { ll du = d[u]; for (ull i = off[u]; i < off[u + 1]; i++) { ll nd = du + q * wgt[i] - (isRowEnd[i] ? p : 0); if (nd < d[tgt[i]]) { d[tgt[i]] = nd; par[tgt[i]] = i; chg = true; } } }
            if (!chg) return true;
            if (pass % 4 == 0) {
                fill(col.begin(), col.end(), 0); vector<size_t> path;
                for (size_t s0 = 0; s0 < N; s0++) if (!col[s0]) {
                    size_t u = s0; path.clear();
                    while (!col[u]) { col[u] = 1; path.push_back(u); if (par[u] == ~0u) break; u = src[par[u]]; }
                    if (par[path.back()] != ~0u && col[src[par[path.back()]]] == 1) {
                        size_t v0 = src[par[path.back()]], y = v0; cyc.clear();
                        do { cyc.push_back(par[y]); y = src[par[y]]; } while (y != v0);
                        reverse(cyc.begin(), cyc.end()); return false;
                    }
                    for (size_t y : path) col[y] = 2;
                }
            }
        }
    };
    auto printCycle = [&]() {
        size_t st = 0; for (size_t j = 0; j < cyc.size(); j++) if (keys[src[cyc[j]]].x == 0) { st = j; break; }
        int row = 0;
        for (size_t jj = 0; jj < cyc.size(); jj++) {
            uint32_t i = cyc[(st + jj) % cyc.size()]; int x = keys[src[i]].x;
            vector<PE> tv; decode(keys[tgt[i]], tv); int sh = keys[tgt[i]].x == 0 ? 1 : 0;
            bool any = false; for (auto& p : tv) if (p.c == x && p.ly == -sh) any = true;
            if (any || wgt[i]) {
                printf("    row %d u %d (%s) w=%d:", row, x + ULO, modeled(x + ULO) ? "mod" : "ghost", wgt[i]);
                for (auto& p : tv) if (p.c == x && p.ly == -sh) { ll ax = x + ULO + (ll)A * row, ay = row; printf(" (%lld,%lld)-(%lld,%lld)", ax, ay, ax + MDX[p.m], ay + MDY[p.m]); }
                printf("\n");
            }
            if (isRowEnd[i]) row++;
        }
    };
    int lev = max(abs(A), 1);
    while (true) {
        printf(" try mean %lld/%lld per row\n", P, Q);
        if (bf(P, Q)) {
            printf("RESULT A=%d WM=%d KM=%d %s: min mean cost per row = %lld/%lld (CERTIFIED: no cycle below); E share per row = %lld/%lld; per level = %lld/%lld = %.4f  (%.0fs)\n",
                   A, WM, KM, MODE.c_str(), P, Q, P, 2 * Q, P, 2 * Q * lev, (double)P / (2 * Q * lev), el());
            break;
        }
        ll sw = 0; int rows = 0; for (auto i : cyc) { sw += wgt[i]; rows += isRowEnd[i]; }
        printf("  cycle: %zu arcs, %d rows, cost %lld -> mean %lld/%d\n", cyc.size(), rows, sw, sw, rows);
        if (rows == 0) { printf("  ERROR: cycle without row end\n"); return 1; }
        ll g = __gcd(sw, (ll)rows); ll P2 = sw / g, Q2 = rows / g;
        if (g == 0) { P2 = 0; Q2 = 1; }
        if (P2 * Q >= P * Q2) { printf("  ERROR: ratio did not decrease\n"); return 1; }
        P = P2; Q = Q2;
        printCycle();
        if (P == 0) { printf("  zero-cost cycle\n"); }
    }
    printf("total %.0fs\n", el());
}
