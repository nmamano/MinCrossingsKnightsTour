// jr.cpp - joint strip certificate engine (KT Edge Searcher, 2026-10-03).
//
// Generic strip: columns 0..NC-1, scanned in (row, column) order. DEG gives per column 'E' (degree
// exactly 2) or 'L' (degree <= 2). PAIRS lists the allowed column pairs of knight edges.
// No cycle among labelled edges: with SLAB, only S edges (an end in column 0 or 1) carry path labels
// (the width-two acyclicity); other edges are unlabelled (a relaxation). Without SLAB all edges are labelled.
//
// Weights (beta = P/Q): per arc Q*4w + P*4w0 + 4Q*wx; at the row end -4Q - 4P - 2P*t (baseline 1 per row).
//   w  = new crossing pairs with both edges in S,
//   w0 = new crossing pairs whose two edges both have an end in column 0,
//   wx = new crossing pairs with at least one edge outside S (all modelled edges),
//   t  = 2a, endpoint penalty of the row (w-turnstheory FINDINGS 10.2, 10.4, 11.1-11.2), at row end.
// A crossing pair is charged to the transition that adds the later edge.
// With DEG=EELL, PAIRS=01,02,12,13 this is exactly the R1 model (wx = 0).
//
// Endpoint test at the end of row R: the set of listed edges = (listed edges pending at the start of
// row R whose upper end is in row R: "lost" bits, carried in the state) U (listed edges pending at the
// start of row R+1, shifted). Augmented state = (base state, lost bits, row parity).
//
// usage: jr DEG PAIRS slab|full ORIENT crit|cert P Q [nolimit]
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; typedef unsigned long long ull;
const int UPX[4] = {2, -2, 1, -1}, UPY[4] = {1, 1, 2, 2};
int NC; string DEG; bool AL[8][8]; bool SLAB;
static bool isS(int a, int b) { return a < 2 || b < 2; }
static int orientf(int ax, int ay, int bx, int by, int cx, int cy) { ll v = (ll)(bx - ax) * (cy - ay) - (ll)(by - ay) * (cx - ax); return (v > 0) - (v < 0); }
static bool crossE(int a, int b, int c, int d, int e, int f, int g, int h) {
    return orientf(a, b, c, d, e, f) * orientf(a, b, c, d, g, h) < 0 && orientf(e, f, g, h, a, b) * orientf(e, f, g, h, c, d) < 0;
}
// ---------------- slots: possible pending edges (lower end (lx,ly), ly in -2..0, upward move m)
struct Slot { int lx, ly, ux, uy; bool lab; };
vector<Slot> SL; int slotId[8][3][4];
struct PE { int lx, ly, ux, uy, comp; };
struct Key { ull a, b; bool operator==(const Key& o) const { return a == o.a && b == o.b; } };
static Key encode(int x, const vector<PE>& e) {   // e sorted by slot id
    Key k{(ull)x << 61, 0}; int li = 0;
    for (auto& p : e) {
        int m = -1; for (int j = 0; j < 4; j++) if (p.lx + UPX[j] == p.ux && p.ly + UPY[j] == p.uy) m = j;
        int s = slotId[p.lx][p.ly + 2][m]; k.a |= 1ULL << s;
        if (SL[s].lab) { k.b |= (ull)p.comp << (4 * li); li++; }
    }
    return k;
}
static int keyX(const Key& k) { return k.a >> 61; }
static void decode(const Key& k, vector<PE>& e) {
    e.clear(); int li = 0;
    for (int s = 0; s < (int)SL.size(); s++) if (k.a >> s & 1) {
        int c = 15; if (SL[s].lab) { c = k.b >> (4 * li) & 15; li++; }
        e.push_back({SL[s].lx, SL[s].ly, SL[s].ux, SL[s].uy, c});
    }
}
// ---------------- hash of base states
vector<Key> keys; vector<uint32_t> tab; ull tmask;
static ull hk(const Key& k) { ull x = k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL; x ^= x >> 31; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 29; return x; }
static void rehash(size_t lg) { tab.assign(1ULL << lg, ~0u); tmask = (1ULL << lg) - 1; for (uint32_t i = 0; i < keys.size(); i++) { ull h = hk(keys[i]) & tmask; while (tab[h] != ~0u) h = (h + 1) & tmask; tab[h] = i; } }
static uint32_t getId(const Key& k) {
    ull h = hk(k) & tmask;
    while (tab[h] != ~0u) { if (keys[tab[h]] == k) return tab[h]; h = (h + 1) & tmask; }
    uint32_t id = keys.size(); keys.push_back(k); tab[h] = id;
    if (keys.size() * 2 > tab.size()) rehash(__builtin_ctzll(tab.size()) + 1);
    return id;
}
// ---------------- endpoint test lists
typedef array<int, 4> E4;
static E4 nrm(int ax, int ay, int bx_, int by) { return ay < by ? E4{ax, ay, bx_, by} : E4{bx_, by, ax, ay}; }
vector<E4> LE; vector<int> LCOEF; int EXC0, EXC1;
static void makeList(bool down) {
    struct R { int ax, ay, bx, by, c; };
    vector<R> L = {{0, -1, 1, 1, -1}, {0, 0, 1, -2, -1}, {0, 0, 2, -1, -1}, {0, 1, 1, -1, +1},
                   {0, 1, 2, 0, +1},  {0, 2, 1, 0, -1},  {1, 0, 2, 2, -1},  {1, 1, 2, -1, -1}};
    vector<R> X = {{0, 0, 2, 1, 0}, {0, 1, 2, 0, 0}};
    int sg = down ? -1 : 1;
    auto add = [&](const R& r) {
        E4 e = nrm(r.ax, sg * r.ay, r.bx, sg * r.by);
        for (size_t i = 0; i < LE.size(); i++) if (LE[i] == e) { LCOEF[i] += r.c; return (int)i; }
        LE.push_back(e); LCOEF.push_back(r.c); return (int)LE.size() - 1;
    };
    for (auto& r : L) add(r);
    EXC0 = add(X[0]); EXC1 = add(X[1]);
}
vector<int> lostIdx;   // listed edges whose upper end is in row 0 (relative to the row they straddle)
static int listedMask(const vector<PE>& e, int shift) {
    int m = 0;
    for (auto& p : e) { E4 q = nrm(p.lx, p.ly + shift, p.ux, p.uy + shift); for (size_t i = 0; i < LE.size(); i++) if (LE[i] == q) m |= 1 << i; }
    return m;
}
static int tOf(int m, int par) {
    bool e = (m >> EXC0 & 1) && (m >> EXC1 & 1);
    if (e) return 2;
    int F = 0; for (size_t i = 0; i < LE.size(); i++) if (m >> i & 1) F += LCOEF[i];
    F = ((F % 3) + 3) % 3;
    int c = par == 0 ? 1 : -1;
    int h = ((((1 + c) / 2 + c * (F + 2)) % 3) + 3) % 3;
    static const int T[3] = {1, 2, 0};
    return T[h];
}
// ---------------- main
vector<ull> boff; vector<uint32_t> btgt; vector<uint16_t> binfo;   // info: w | w0<<4 | wx<<8 (4 bits each)
vector<uint16_t> lostB, prevB;   // per x=0 base state: lost-bit mask (compressed), listed mask shifted by +1

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 8) { fprintf(stderr, "usage: jr DEG PAIRS slab|full ORIENT crit|cert P Q\n"); return 1; }
    DEG = argv[1]; NC = DEG.size(); string pairs = argv[2]; SLAB = string(argv[3]) == "slab";
    string ORI = argv[4], MODE = argv[5]; ll P = atoll(argv[6]), Q = atoll(argv[7]);
    for (size_t i = 0; i + 1 < pairs.size(); i += 3) { int a = pairs[i] - '0', b = pairs[i + 1] - '0'; AL[a][b] = AL[b][a] = true; }
    auto T0 = chrono::steady_clock::now();
    auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
    memset(slotId, -1, sizeof slotId);
    for (int lx = 0; lx < NC; lx++) for (int ly = -2; ly <= 0; ly++) for (int m = 0; m < 4; m++) {
        int ux = lx + UPX[m], uy = ly + UPY[m];
        if (ux < 0 || ux >= NC || uy < 0 || !AL[lx][ux]) continue;
        slotId[lx][ly + 2][m] = SL.size(); SL.push_back({lx, ly, ux, uy, !SLAB || isS(lx, ux)});
    }
    printf("DEG %s PAIRS %s labels %s: %zu slots\n", DEG.c_str(), pairs.c_str(), SLAB ? "S-only" : "all", SL.size());
    if (SL.size() > 61) { printf("too many slots\n"); return 1; }
    // ---- base graph
    rehash(20);
    getId(encode(0, {}));
    boff.push_back(0);
    vector<PE> s, in, rest, inL, ne;
    for (size_t q = 0; q < keys.size(); q++) {
        Key kq = keys[q]; int x = keyX(kq); decode(kq, s);
        in.clear(); rest.clear();
        for (auto& p : s) (p.ux == x && p.uy == 0 ? in : rest).push_back(p);
        int din = in.size();
        bool okc = din <= 2;
        inL.clear(); for (auto& p : in) if (!SLAB || isS(p.lx, p.ux)) inL.push_back(p);
        if (inL.size() == 2 && inL[0].comp == inL[1].comp) okc = false;
        if (okc) {
            vector<array<int, 4>> cand;
            for (int m = 0; m < 4; m++) { int tx = x + UPX[m]; if (tx >= 0 && tx < NC && AL[x][tx]) cand.push_back({x, 0, tx, UPY[m]}); }
            vector<int> need; if (DEG[x] == 'E') need = {2 - din}; else for (int r = 0; r <= 2 - din; r++) need.push_back(r);
            int nc = cand.size();
            vector<pair<uint32_t, uint16_t>> outs;
            for (int r : need) for (int msk = 0; msk < (1 << nc); msk++) {
                if (__builtin_popcount(msk) != r) continue;
                vector<array<int, 4>> ch; for (int i = 0; i < nc; i++) if (msk >> i & 1) ch.push_back(cand[i]);
                bool ok = true;
                for (auto& f : ch) { int dg = 0; for (auto& p : rest) if (p.ux == f[2] && p.uy == f[3]) dg++; for (auto& g : ch) if (g[2] == f[2] && g[3] == f[3]) dg++; if (dg > 2) ok = false; }
                if (!ok) continue;
                int w = 0, w0 = 0, wx = 0;
                auto tally = [&](int a1, int b1, int a2, int b2, int c1, int d1, int c2, int d2) {
                    if (!crossE(a1, b1, a2, b2, c1, d1, c2, d2)) return;
                    bool s1 = isS(a1, a2), s2 = isS(c1, c2);
                    if (s1 && s2) w++; else wx++;
                    if ((a1 == 0 || a2 == 0) && (c1 == 0 || c2 == 0)) w0++;
                };
                for (size_t i = 0; i < ch.size(); i++) {
                    auto& f = ch[i];
                    for (auto& p : rest) tally(p.lx, p.ly, p.ux, p.uy, f[0], f[1], f[2], f[3]);
                    for (size_t j = 0; j < i; j++) tally(ch[j][0], ch[j][1], ch[j][2], ch[j][3], f[0], f[1], f[2], f[3]);
                }
                if (w > 15 || w0 > 15 || wx > 15) { printf("weight overflow\n"); return 1; }
                const int NEW = 100;
                int label = inL.size() ? inL[0].comp : NEW, merge = inL.size() == 2 ? inL[1].comp : -1;
                ne.clear();
                for (auto p : rest) { if (merge >= 0 && p.comp == merge) p.comp = label; ne.push_back(p); }
                for (auto& f : ch) ne.push_back({f[0], f[1], f[2], f[3], (!SLAB || isS(f[0], f[2])) ? label : 15});
                int nx = x + 1, sh = 0; if (nx == NC) { nx = 0; sh = 1; }
                for (auto& p : ne) { p.ly -= sh; p.uy -= sh; }
                auto sid = [&](const PE& p) { int m = -1; for (int j = 0; j < 4; j++) if (p.lx + UPX[j] == p.ux && p.ly + UPY[j] == p.uy) m = j; return slotId[p.lx][p.ly + 2][m]; };
                sort(ne.begin(), ne.end(), [&](const PE& a, const PE& b) { return sid(a) < sid(b); });
                int rl[128]; memset(rl, -1, sizeof rl); int nl = 0;
                for (auto& p : ne) { bool lab = !SLAB || isS(p.lx, p.ux); if (!lab) { p.comp = 15; continue; } if (rl[p.comp] < 0) rl[p.comp] = nl++; p.comp = rl[p.comp]; }
                if (nl > 15) { printf("too many labels\n"); return 1; }
                int nlab = 0; for (auto& p : ne) if (!SLAB || isS(p.lx, p.ux)) nlab++;
                if (nlab > 16) { printf("too many labelled edges\n"); return 1; }
                uint32_t tid = getId(encode(nx, ne));
                outs.push_back({tid, (uint16_t)(w | w0 << 4 | wx << 8)});
            }
            sort(outs.begin(), outs.end());
            for (size_t i = 0; i < outs.size(); i++) {
                if (i && outs[i].first == outs[i - 1].first) { if (outs[i].second != outs[i - 1].second) { printf("non-unique arc data\n"); return 1; } continue; }
                btgt.push_back(outs[i].first); binfo.push_back(outs[i].second);
            }
        }
        boff.push_back(btgt.size());
        if (q && (q & ((1 << 22) - 1)) == 0) printf("  base ... %zu/%zu states, %zu arcs, %.0fs\n", q, keys.size(), btgt.size(), el());
    }
    size_t NB = keys.size(), AB = btgt.size();
    printf("base: states %zu arcs %zu (%.0fs)\n", NB, AB, el());
    { vector<uint32_t>().swap(tab); }
    // ---- endpoint data per row-start state
    makeList(ORI == "down");
    for (size_t i = 0; i < LE.size(); i++) if (LE[i][3] == 0) lostIdx.push_back(i);   // upper end in row 0
    printf("orient %s: %zu listed edges, lost-bit edges %zu\n", ORI.c_str(), LE.size(), lostIdx.size());
    lostB.assign(NB, 0); prevB.assign(NB, 0);
    for (size_t b = 0; b < NB; b++) if (keyX(keys[b]) == 0) {
        decode(keys[b], s);
        int m0 = listedMask(s, 0), lb = 0;
        for (size_t j = 0; j < lostIdx.size(); j++) if (m0 >> lostIdx[j] & 1) lb |= 1 << j;
        lostB[b] = lb; prevB[b] = listedMask(s, 1);
    }
    auto lostFull = [&](int lb) { int m = 0; for (size_t j = 0; j < lostIdx.size(); j++) if (lb >> j & 1) m |= 1 << lostIdx[j]; return m; };
    // variant v = lb << 1 | par; at x = 0 states lb = 0
    vector<uint8_t> bxv(NB); for (size_t b = 0; b < NB; b++) bxv[b] = keyX(keys[b]);
    auto nextV = [&](uint32_t b, int v, uint32_t b2, int& t) {
        int x = bxv[b], par = v & 1, lb = v >> 1; t = 0;
        if (x == 0) return lostB[b] << 1 | par;
        if (bxv[b2] != 0) return v;
        t = tOf(lostFull(lb) | prevB[b2], par);
        return par ^ 1;
    };
    // ---- reachable variants (sweeps)
    vector<uint32_t> reach(NB, 0); reach[0] = 3;
    for (int sw = 1;; sw++) {
        bool ch = false;
        for (size_t b = 0; b < NB; b++) if (reach[b]) for (ull i = boff[b]; i < boff[b + 1]; i++) {
            uint32_t b2 = btgt[i];
            for (uint32_t vs = reach[b]; vs; vs &= vs - 1) { int v = __builtin_ctz(vs), t; int v2 = nextV(b, v, b2, t); if (!(reach[b2] >> v2 & 1)) { reach[b2] |= 1u << v2; ch = true; } }
        }
        if (!ch) { printf("reachability: %d sweeps\n", sw); break; }
    }
    vector<ull> aoff(NB + 1, 0); for (size_t b = 0; b < NB; b++) aoff[b + 1] = aoff[b] + __builtin_popcount(reach[b]);
    size_t N = aoff[NB]; ll NA = 0; for (size_t b = 0; b < NB; b++) NA += (ll)__builtin_popcount(reach[b]) * (boff[b + 1] - boff[b]);
    size_t unreach = 0; for (size_t b = 0; b < NB; b++) if (!reach[b]) unreach++;
    printf("augmented: nodes %zu arcs %lld (unreached base states %zu) %.0fs\n", N, NA, unreach, el());
    auto aid = [&](uint32_t b, int v) { return aoff[b] + __builtin_popcount(reach[b] & ((1u << v) - 1)); };
    // ---- Bellman-Ford
    vector<ll> d(N); vector<uint32_t> pnode(N), parc(N);   // parent aug node, base arc index
    vector<uint32_t> nodeB(N); vector<uint8_t> nodeV(N);
    for (size_t b = 0; b < NB; b++) { size_t i = aoff[b]; for (uint32_t vs = reach[b]; vs; vs &= vs - 1) { nodeB[i] = b; nodeV[i] = __builtin_ctz(vs); i++; } }
    // baseline: -1 per row for X and for B (-4q - 4p in units 1/4), charged at the row end (any number of columns)
    auto wbase = [&](uint16_t inf, ll p, ll q) { int w = inf & 15, w0 = inf >> 4 & 15, wx = inf >> 8 & 15; return q * (4 * w) + p * (4 * w0) + 4 * q * wx; };
    auto rowend = [&](uint32_t b, ll p, ll q) -> ll { return bxv[b] == NC - 1 ? -4 * q - 4 * p : 0; };
    vector<uint32_t> cyc;   // pairs (aug node, base arc) flattened: store aug source node; arc in carc
    vector<uint32_t> carc;
    auto bf = [&](ll p, ll q) {
        ll WB[1 << 12]; for (int i = 0; i < (1 << 12); i++) WB[i] = wbase(i, p, q);
        fill(d.begin(), d.end(), 0); fill(pnode.begin(), pnode.end(), ~0u);
        vector<uint8_t> col(N);
        for (int pass = 1;; pass++) {
            bool chg = false;
            for (size_t u = 0; u < N; u++) {
                uint32_t b = nodeB[u]; int v = nodeV[u]; ll du = d[u]; ll RE = rowend(b, p, q);
                for (ull i = boff[b]; i < boff[b + 1]; i++) {
                    uint32_t b2 = btgt[i]; int t; int v2 = nextV(b, v, b2, t);
                    ll nd = du + WB[binfo[i]] - 2 * p * t + RE;
                    size_t w2 = aid(b2, v2);
                    if (nd < d[w2]) { d[w2] = nd; pnode[w2] = u; parc[w2] = i; chg = true; }
                }
            }
            if (!chg) { printf("  converged after %d passes (%.0fs)\n", pass, el()); return true; }
            if (pass % 4 == 0) {
                fill(col.begin(), col.end(), 0);
                vector<size_t> path;
                for (size_t s0 = 0; s0 < N; s0++) if (!col[s0]) {
                    size_t u = s0; path.clear();
                    while (!col[u]) { col[u] = 1; path.push_back(u); if (pnode[u] == ~0u) break; u = pnode[u]; }
                    if (pnode[path.back()] != ~0u && col[pnode[path.back()]] == 1) {
                        size_t v0 = pnode[path.back()], y = v0; cyc.clear(); carc.clear();
                        do { cyc.push_back(pnode[y]); carc.push_back(parc[y]); y = pnode[y]; } while (y != v0);
                        reverse(cyc.begin(), cyc.end()); reverse(carc.begin(), carc.end());
                        printf("  negative cycle after %d passes (%.0fs)\n", pass, el());
                        return false;
                    }
                    for (size_t y : path) col[y] = 2;
                }
            }
        }
    };
    struct CS { ll sw, sw0, swx, st; int rows; };
    auto cycStats = [&]() {
        CS c{0, 0, 0, 0, 0};
        for (size_t j = 0; j < cyc.size(); j++) {
            uint32_t u = cyc[j], i = carc[j]; uint16_t inf = binfo[i];
            int t; nextV(nodeB[u], nodeV[u], btgt[i], t);
            c.sw += 4 * (inf & 15); c.sw0 += 4 * (inf >> 4 & 15); c.swx += inf >> 8 & 15; c.st += t;
            if (bxv[nodeB[u]] == NC - 1) { c.rows++; c.sw -= 4; c.sw0 -= 4; }
        }
        return c;
    };
    auto printCycle = [&]() {
        // re-derive introduced edges: rebuild keys is not kept; print weights per arc and row-end data
        size_t st = 0; for (size_t j = 0; j < cyc.size(); j++) if (bxv[nodeB[cyc[j]]] == 0) { st = j; break; }
        int row = 0;
        for (size_t jj = 0; jj < cyc.size(); jj++) {
            size_t j = (st + jj) % cyc.size(); uint32_t u = cyc[j], i = carc[j]; uint16_t inf = binfo[i];
            int t; nextV(nodeB[u], nodeV[u], btgt[i], t);
            int x = bxv[nodeB[u]];
            printf("    row %d x %d: w=%d w0=%d wx=%d", row, x, inf & 15, inf >> 4 & 15, inf >> 8 & 15);
            { vector<PE> tv; decode(keys[btgt[i]], tv); int sh = bxv[btgt[i]] == 0 ? 1 : 0;
              for (auto& p : tv) if (p.lx == x && p.ly == -sh) printf(" (%d,%d)-(%d,%d)", p.lx, row, p.ux, p.uy + sh + row); }
            if (x == NC - 1) { printf("  | row end par=%d t=%d", nodeV[u] & 1, t); row++; }
            printf("\n");
        }
    };
    auto verify = [&](ll p, ll q) {
        ll bad = 0;
        for (size_t u = 0; u < N; u++) { uint32_t b = nodeB[u]; int v = nodeV[u];
            for (ull i = boff[b]; i < boff[b + 1]; i++) { int t; int v2 = nextV(b, v, btgt[i], t); ll wt = wbase(binfo[i], p, q) - 2 * p * t + rowend(b, p, q); if (d[u] + wt < d[aid(btgt[i], v2)]) bad++; } }
        return bad;
    };
    if (MODE == "cert") {
        if (bf(P, Q)) printf("%s beta=%lld/%lld: CERTIFIED, potential range [%lld, %lld] (units 1/(4q)), violated arcs %lld\n", ORI.c_str(), P, Q, *min_element(d.begin(), d.end()), *max_element(d.begin(), d.end()), verify(P, Q));
        else { CS c = cycStats(); printf("%s beta=%lld/%lld: NEGATIVE CYCLE %zu arcs %d rows sum(4w-1)=%lld sum(4w0-1)=%lld sum wx=%lld sum t=%lld\n", ORI.c_str(), P, Q, cyc.size(), c.rows, c.sw, c.sw0, c.swx, c.st); printCycle(); }
    } else {
        while (true) {
            printf(" try beta = %lld/%lld = %.6f\n", P, Q, (double)P / Q);
            if (bf(P, Q)) { printf("%s: beta* = %lld/%lld = %.6f, potential range [%lld, 0] (units 1/(4q)), violated arcs %lld\n", ORI.c_str(), P, Q, (double)P / Q, *min_element(d.begin(), d.end()), verify(P, Q)); break; }
            CS c = cycStats();
            ll Nn = c.sw + 4 * c.swx, Dd = 2 * c.st - c.sw0;
            printf("  cycle: %zu arcs, %d rows, sum(4w-1)=%lld sum(4w0-1)=%lld sum wx=%lld sum t=%lld -> ratio %lld/%lld\n", cyc.size(), c.rows, c.sw, c.sw0, c.swx, c.st, Nn, Dd);
            printCycle();
            if (Dd <= 0) { printf("  cycle with D <= 0: negative for every beta\n"); return 0; }
            ll g = __gcd(llabs(Nn), Dd); ll P2 = Nn / g, Q2 = Dd / g;
            if (P2 * Q >= P * Q2) { printf("  ERROR: ratio did not decrease\n"); return 1; }
            P = P2; Q = Q2;
        }
    }
    printf("total %.0fs\n", el());
}
