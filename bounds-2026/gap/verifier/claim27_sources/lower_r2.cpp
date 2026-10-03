// r2.cpp - independent C++ check of request R2 (gap/turnstheory/REQUESTS.md): combined boundary and
// interval credit on the width-two strip (KT Edge Searcher, 2026-10-03).
//
// Written from the definitions only (no code of KT Lower Bounds):
//   base strip model   : w-lowerbounds/FINDINGS.md F1 (columns 0,1 degree exactly 2; ghost columns 2,3
//                        degree <= 2 and only joined to strip cells; no cycle; scan order (row, column);
//                        a crossing pair is charged to the transition that adds the later edge).
//                        Base builder = w-searcher/cert/strip2.cpp (82,516 states, 144,674 arcs).
//   endpoint test      : w-turnstheory/FINDINGS.md 10.2 (coefficients), 10.4 (F mod 3, exceptional pair),
//                        11.1-11.2 (h, penalty a), QUESTIONS.md (t = 2a at row end, parity toggles).
//   w0                 : new crossing pairs whose two edges both have an endpoint in column 0 (R1).
//   blocked rows, k    : gap/turnstheory/REQUESTS.md R2 (g, z registers, delayed flag, counter s <= 4).
//   arc weight         : q(4w-1) + p(4w0-1) + 4qk - 2pt   (k, t only at row end).
//
// Implementation choices that differ from an accumulator: the endpoint test of row R is evaluated at
// the row end from the SET of listed edges, taken as (listed edges pending at the start of row R) union
// (listed edges pending at the start of row R+1). Every listed edge straddles row R, so it is in one of
// the two sets. Only the first set is carried through the row (bit mask).
//
// usage: r2 ORIENT(up|down) MODE(cert P Q | crit P Q) [allhist]
//   cert P Q : Bellman-Ford for beta = P/Q; report converged potential range or a negative cycle.
//   crit P Q : Dinkelbach from beta = P/Q down to the exact critical ratio beta*.
//   allhist  : start states with every history (g 4 bits, z 2 bits) and every counter s (default: zero).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned long long ull;

// ------------------------------------------------------------------ base strip graph
struct PE { int lx, ly, ux, uy, comp; };
static bool operator<(const PE& a, const PE& b) { return tie(a.lx, a.ly, a.ux, a.uy) < tie(b.lx, b.ly, b.ux, b.uy); }
static int orient(int ax, int ay, int bx, int by, int cx, int cy) { ll v = (ll)(bx - ax) * (cy - ay) - (ll)(by - ay) * (cx - ax); return (v > 0) - (v < 0); }
static bool crossE(int a, int b, int c, int d, int e, int f, int g, int h) {
    return orient(a, b, c, d, e, f) * orient(a, b, c, d, g, h) < 0 && orient(e, f, g, h, a, b) * orient(e, f, g, h, c, d) < 0;
}
const int K = 2, W = 4;
const int UPX[4] = {2, -2, 1, -1}, UPY[4] = {1, 1, 2, 2};
struct St { int x; vector<PE> e; };
static string enc(const St& s) {
    string k; k.push_back((char)s.x);
    for (auto& p : s.e) { k.push_back((char)p.lx); k.push_back((char)p.ly); k.push_back((char)p.ux); k.push_back((char)p.uy); k.push_back((char)p.comp); }
    return k;
}
static St dec(const string& k) {
    St s; s.x = k[0];
    for (size_t i = 1; i < k.size(); i += 5) s.e.push_back({(signed char)k[i], (signed char)k[i + 1], (signed char)k[i + 2], (signed char)k[i + 3], (signed char)k[i + 4]});
    return s;
}
struct BArc { int to, w, w0, deg; };
vector<string> bkeys; vector<vector<BArc>> badj; vector<int> bx;

static void buildBase() {
    unordered_map<string, int> id;
    auto get = [&](const St& s) { string k = enc(s); auto it = id.find(k); if (it != id.end()) return it->second; int n = bkeys.size(); id[k] = n; bkeys.push_back(k); badj.emplace_back(); return n; };
    St start; start.x = 0; get(start);
    for (size_t q = 0; q < bkeys.size(); q++) {
        St s = dec(bkeys[q]); int x = s.x;
        vector<PE> in, rest;
        for (auto& p : s.e) (p.ux == x && p.uy == 0 ? in : rest).push_back(p);
        bool strip = x < K;
        vector<array<int, 4>> cand;
        for (int m = 0; m < 4; m++) { int tx = x + UPX[m]; if (tx >= 0 && tx < W && (strip || tx < K)) cand.push_back({x, 0, tx, UPY[m]}); }
        vector<int> need; int din = in.size();
        if (strip) { if (2 - din < 0) continue; need = {2 - din}; }
        else { if (din > 2) continue; for (int r = 0; r <= 2 - din; r++) need.push_back(r); }
        if (din == 2 && in[0].comp == in[1].comp) continue;   // would close a cycle
        map<int, BArc> out;
        int nc = cand.size();
        for (int r : need) for (int msk = 0; msk < (1 << nc); msk++) {
            if (__builtin_popcount(msk) != r) continue;
            vector<array<int, 4>> ch; for (int i = 0; i < nc; i++) if (msk >> i & 1) ch.push_back(cand[i]);
            map<pair<int, int>, int> td; bool ok = true;
            for (auto& p : rest) td[{p.ux, p.uy}]++;
            for (auto& f : ch) if (++td[{f[2], f[3]}] > 2) ok = false;
            if (!ok) continue;
            int w = 0, w0 = 0;
            auto c0 = [](int a, int c) { return a == 0 || c == 0; };
            for (size_t i = 0; i < ch.size(); i++) {
                auto& f = ch[i]; bool f0 = c0(f[0], f[2]);
                for (auto& p : rest) if (crossE(p.lx, p.ly, p.ux, p.uy, f[0], f[1], f[2], f[3])) { w++; if (f0 && c0(p.lx, p.ux)) w0++; }
                for (size_t j = 0; j < i; j++) if (crossE(ch[j][0], ch[j][1], ch[j][2], ch[j][3], f[0], f[1], f[2], f[3])) { w++; if (f0 && c0(ch[j][0], ch[j][2])) w0++; }
            }
            const int NEW = 100;
            int label = din ? in[0].comp : NEW, merge = din == 2 ? in[1].comp : -1;
            vector<PE> ne;
            for (auto p : rest) { if (merge >= 0 && p.comp == merge) p.comp = label; ne.push_back(p); }
            for (auto& f : ch) ne.push_back({f[0], f[1], f[2], f[3], label});
            int nx = x + 1, sh = 0; if (nx == W) { nx = 0; sh = 1; }
            for (auto& p : ne) { p.ly -= sh; p.uy -= sh; }
            sort(ne.begin(), ne.end());
            map<int, int> rl; for (auto& p : ne) { if (!rl.count(p.comp)) { int v = rl.size(); rl[p.comp] = v; } p.comp = rl[p.comp]; }
            St t; t.x = nx; t.e = ne;
            int tid = get(t);
            BArc a{tid, w, w0, din + r};
            auto it = out.find(tid);
            if (it != out.end()) {   // the target fixes the chosen edge set, so the arc data must agree
                if (it->second.w != w || it->second.w0 != w0 || it->second.deg != a.deg) { fprintf(stderr, "non-unique arc data\n"); exit(1); }
            } else out[tid] = a;
        }
        for (auto& kv : out) badj[q].push_back(kv.second);
    }
    bx.resize(bkeys.size()); for (size_t i = 0; i < bkeys.size(); i++) bx[i] = bkeys[i][0];
}

// ------------------------------------------------------------------ endpoint test
// edge normal form: lower end first (knight moves never have dy = 0)
typedef array<int, 4> E4;
static E4 nrm(int ax, int ay, int bx_, int by) { return ay < by ? E4{ax, ay, bx_, by} : E4{bx_, by, ax, ay}; }
vector<E4> LE; vector<int> LCOEF; int EXC0, EXC1;   // listed edges, coefficients, exceptional pair indices
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
static int maskOf(const vector<PE>& e, int shift) {   // listed edges present among pending edges, y + shift
    int m = 0;
    for (auto& p : e) { E4 q = nrm(p.lx, p.ly + shift, p.ux, p.uy + shift); for (size_t i = 0; i < LE.size(); i++) if (LE[i] == q) m |= 1 << i; }
    return m;
}
static int Fmod(int m) { int F = 0; for (size_t i = 0; i < LE.size(); i++) if (m >> i & 1) F += LCOEF[i]; return ((F % 3) + 3) % 3; }
static int tOf(int m, int par) {   // t = 2a; par 0 = even local row (c = +1)
    bool e = (m >> EXC0 & 1) && (m >> EXC1 & 1);
    if (e) return 2;
    int c = par == 0 ? 1 : -1;
    int h = ((((1 + c) / 2 + c * (Fmod(m) + 2)) % 3) + 3) % 3;
    static const int T[3] = {1, 2, 0};
    return T[h];
}

// ------------------------------------------------------------------ augmented graph
// key bits: base id 0..19 | mask 20..29 | par 30 | gh 31..34 | zh 35..36 | s 37..39 | gc 40
static inline ull mk(ull b, ull m, ull par, ull gh, ull zh, ull s, ull gc) { return b | m << 20 | par << 30 | gh << 31 | zh << 35 | s << 37 | gc << 40; }
struct HMap {
    vector<ull> k; vector<uint32_t> v; ull mask;
    HMap(int lg) { k.assign(1ULL << lg, ~0ULL); v.resize(1ULL << lg); mask = (1ULL << lg) - 1; }
    static ull h(ull x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
    // returns id; inserts nid if absent (sets ins)
    uint32_t get(ull key, uint32_t nid, bool& ins) {
        ull i = h(key) & mask;
        while (true) {
            if (k[i] == key) { ins = false; return v[i]; }
            if (k[i] == ~0ULL) { k[i] = key; v[i] = nid; ins = true; return nid; }
            i = (i + 1) & mask;
        }
    }
};
vector<ull> nkey; vector<ull> off; vector<uint32_t> atgt; vector<uint16_t> ainfo;   // info: w | w0<<4 | k<<8 | t<<9
vector<int> mStart, mPrev;

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 5) { fprintf(stderr, "usage: r2 up|down cert|crit P Q [allhist]\n"); return 1; }
    string ORI = argv[1], MODE = argv[2]; ll P = atoll(argv[3]), Q = atoll(argv[4]);
    bool allhist = argc > 5 && string(argv[5]) == "allhist";
    auto T0 = chrono::steady_clock::now();
    auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
    buildBase();
    long nb = 0; for (auto& a : badj) nb += a.size();
    printf("base: states %zu arcs %ld\n", bkeys.size(), nb);
    makeList(ORI == "down");
    printf("orient %s: %zu listed edges:", ORI.c_str(), LE.size());
    for (size_t i = 0; i < LE.size(); i++) printf(" (%d,%d)-(%d,%d)%+d", LE[i][0], LE[i][1], LE[i][2], LE[i][3], LCOEF[i]);
    printf("; exceptional %d,%d\n", EXC0, EXC1);
    int NB = bkeys.size(); mStart.assign(NB, 0); mPrev.assign(NB, 0);
    for (int b = 0; b < NB; b++) if (bx[b] == 0) { St s = dec(bkeys[b]); mStart[b] = maskOf(s.e, 0); mPrev[b] = maskOf(s.e, 1); }

    HMap hm(26);
    auto addNode = [&](ull key) { bool ins; uint32_t id = hm.get(key, nkey.size(), ins); if (ins) nkey.push_back(key); return id; };
    for (int par = 0; par < 2; par++) {
        if (!allhist) addNode(mk(0, 0, par, 0, 0, 0, 0));
        else for (int gh = 0; gh < 16; gh++) for (int zh = 0; zh < 4; zh++) for (int s = 0; s <= 4; s++) addNode(mk(0, 0, par, gh, zh, s, 0));
    }
    off.push_back(0);
    for (size_t u = 0; u < nkey.size(); u++) {
        ull key = nkey[u];
        int b = key & 0xFFFFF, m = key >> 20 & 0x3FF, par = key >> 30 & 1, gh = key >> 31 & 15, zh = key >> 35 & 3, s = key >> 37 & 7, gc = key >> 40 & 1;
        int x = bx[b];
        for (auto& a : badj[b]) {
            ull nk; int k = 0, t = 0;
            if (x == 0) nk = mk(a.to, mStart[b], par, gh, zh, s, 0);
            else if (x == 1) nk = mk(a.to, m, par, gh, zh, s, 0);
            else if (x == 2) nk = mk(a.to, m, par, gh, zh, s, a.deg == 2);
            else {   // row end
                int z = a.deg == 0;
                int bl = (gh >> 3 & 1) & gc & (zh >> 1 & 1);
                k = bl && s == 4;
                int s2 = bl ? min(4, s + 1) : 0;
                int gh2 = ((gh << 1) | gc) & 15, zh2 = ((zh << 1) | z) & 3;
                t = tOf(m | mPrev[a.to], par);
                nk = mk(a.to, mStart[a.to], par ^ 1, gh2, zh2, s2, 0);
            }
            uint32_t v = addNode(nk);
            atgt.push_back(v); ainfo.push_back(a.w | a.w0 << 4 | k << 8 | t << 9);
        }
        off.push_back(atgt.size());
        if ((u & ((1 << 22) - 1)) == 0 && u) printf("  ... %zu nodes, %zu arcs, %.0fs\n", u, atgt.size(), el());
    }
    size_t N = nkey.size(), A = atgt.size();
    printf("augmented: nodes %zu arcs %zu (%s starts), built in %.0fs\n", N, A, allhist ? "all-history" : "zero-history", el());
    { HMap tmp(1); swap(hm, tmp); }

    // ---------------------------------------------------------------- Bellman-Ford with cycle extraction
    vector<ll> d(N); vector<uint32_t> par(N);   // par = arc index into atgt, ~0 = none
    vector<uint32_t> src(A);                     // source node of each arc
    for (size_t u = 0; u < N; u++) for (ull i = off[u]; i < off[u + 1]; i++) src[i] = u;
    auto comp = [&](uint16_t inf, int& w, int& w0, int& k, int& t) { w = inf & 15; w0 = inf >> 4 & 15; k = inf >> 8 & 1; t = inf >> 9 & 3; };
    // returns true if converged; otherwise fills cyc (arc indices in walk order)
    auto bf = [&](ll p, ll q, vector<uint32_t>& cyc) {
        ll WT[1 << 11];
        for (int i = 0; i < (1 << 11); i++) { int w, w0, k, t; comp(i, w, w0, k, t); WT[i] = q * (4 * w - 1) + p * (4 * w0 - 1) + 4 * q * k - 2 * p * t; }
        fill(d.begin(), d.end(), 0); fill(par.begin(), par.end(), ~0u);
        vector<char> col(N);
        for (int pass = 1;; pass++) {
            bool ch = false;
            for (size_t u = 0; u < N; u++) { ll du = d[u]; for (ull i = off[u]; i < off[u + 1]; i++) { ll nd = du + WT[ainfo[i]]; uint32_t v = atgt[i]; if (nd < d[v]) { d[v] = nd; par[v] = i; ch = true; } } }
            if (!ch) { printf("  converged after %d passes (%.0fs)\n", pass, el()); return true; }
            if (pass % 4 == 0) {   // look for a cycle in the parent graph; it is always negative
                fill(col.begin(), col.end(), 0);
                for (size_t s0 = 0; s0 < N; s0++) if (!col[s0]) {
                    size_t u = s0; vector<size_t> path;
                    while (!col[u]) { col[u] = 1; path.push_back(u); if (par[u] == ~0u) break; u = src[par[u]]; }
                    // did the walk stop on a node of the current path?
                    if (par[path.back()] != ~0u) {
                        size_t v = src[par[path.back()]];
                        if (col[v] == 1) {   // v is on the current path: cycle v -> ... -> path.back() -> v
                            cyc.clear(); size_t y = v;
                            do { cyc.push_back(par[y]); y = src[par[y]]; } while (y != v);
                            reverse(cyc.begin(), cyc.end());
                            printf("  negative cycle after %d passes (%.0fs)\n", pass, el());
                            return false;
                        }
                    }
                    for (size_t y : path) col[y] = 2;
                }
            }
        }
    };
    auto cycStats = [&](const vector<uint32_t>& cyc, ll& Nn, ll& Dd, int& rows, ll& sw, ll& sk, ll& sw0, ll& st) {
        Nn = Dd = sw = sk = sw0 = st = 0; rows = 0;
        for (auto i : cyc) { int w, w0, k, t; comp(ainfo[i], w, w0, k, t); sw += 4 * w - 1; sw0 += 4 * w0 - 1; sk += k; st += t; if (bx[nkey[src[i]] & 0xFFFFF] == 3) rows++; }
        Nn = sw + 4 * sk; Dd = 2 * st - sw0;
    };
    auto printCycle = [&](const vector<uint32_t>& cyc) {
        // the field: edges introduced on each arc (lower end at the cell being scanned), absolute rows
        size_t st = 0; for (size_t j = 0; j < cyc.size(); j++) if (bx[nkey[src[cyc[j]]] & 0xFFFFF] == 0) { st = j; break; }
        int row = 0;
        printf("  field (edges introduced per cell; row index relative to cycle start):\n");
        for (size_t jj = 0; jj < cyc.size(); jj++) {
            uint32_t i = cyc[(st + jj) % cyc.size()];
            ull ku = nkey[src[i]], kv = nkey[atgt[i]];
            int bu = ku & 0xFFFFF, bv = kv & 0xFFFFF, x = bx[bu];
            St sv = dec(bkeys[bv]); int sh = bx[bv] == 0 ? 1 : 0;
            int w, w0, k, t; comp(ainfo[i], w, w0, k, t);
            printf("    row %d x %d: w=%d w0=%d", row, x, w, w0);
            for (auto& p : sv.e) if (p.lx == x && p.ly == -sh) printf(" (%d,%d)-(%d,%d)", p.lx, row, p.ux, p.uy + sh + row);
            if (x == 3) printf("   | row end: par=%d t=%d k=%d g=%d z=%d s=%d", (int)(ku >> 30 & 1), t, k, (int)(ku >> 40 & 1), (int)(kv >> 35 & 1), (int)(kv >> 37 & 7));
            printf("\n");
            if (x == 3) row++;
        }
    };
    vector<uint32_t> cyc;
    if (MODE == "cert") {
        bool ok = bf(P, Q, cyc);
        if (ok) {
            ll mn = *min_element(d.begin(), d.end()), mx = *max_element(d.begin(), d.end());
            // independent final check of all reduced costs
            ll bad = 0; for (size_t i = 0; i < A; i++) { int w, w0, k, t; comp(ainfo[i], w, w0, k, t); ll wt = Q * (4 * w - 1) + P * (4 * w0 - 1) + 4 * Q * k - 2 * P * t; if (d[src[i]] + wt < d[atgt[i]]) bad++; }
            printf("%s beta=%lld/%lld: CERTIFIED, potential range [%lld, %lld] (units 1/(4q)), violated arcs %lld\n", ORI.c_str(), P, Q, mn, mx, bad);
        } else {
            ll Nn, Dd, sw, sk, sw0, st; int rows; cycStats(cyc, Nn, Dd, rows, sw, sk, sw0, st);
            printf("%s beta=%lld/%lld: NEGATIVE CYCLE, %zu arcs, %d rows, sum(4w-1)=%lld sum k=%lld sum(4w0-1)=%lld sum t=%lld -> ratio %lld/%lld\n", ORI.c_str(), P, Q, cyc.size(), rows, sw, sk, sw0, st, Nn, Dd);
            printCycle(cyc);
        }
    } else {
        while (true) {
            printf(" try beta = %lld/%lld = %.6f\n", P, Q, (double)P / Q);
            bool ok = bf(P, Q, cyc);
            if (ok) {
                ll mn = *min_element(d.begin(), d.end());
                ll bad = 0; for (size_t i = 0; i < A; i++) { int w, w0, k, t; comp(ainfo[i], w, w0, k, t); ll wt = Q * (4 * w - 1) + P * (4 * w0 - 1) + 4 * Q * k - 2 * P * t; if (d[src[i]] + wt < d[atgt[i]]) bad++; }
                printf("%s: beta* = %lld/%lld = %.6f, potential range [%lld, 0] (units 1/(4q)), violated arcs %lld\n", ORI.c_str(), P, Q, (double)P / Q, mn, bad);
                break;
            }
            ll Nn, Dd, sw, sk, sw0, st; int rows; cycStats(cyc, Nn, Dd, rows, sw, sk, sw0, st);
            printf("  cycle: %zu arcs, %d rows, sum(4w-1)=%lld sum k=%lld sum(4w0-1)=%lld sum t=%lld -> ratio %lld/%lld\n", cyc.size(), rows, sw, sk, sw0, st, Nn, Dd);
            if (Dd <= 0) { printf("  cycle with D <= 0: negative for every beta\n"); printCycle(cyc); return 0; }
            ll g = __gcd(llabs(Nn), Dd); ll P2 = Nn / g, Q2 = Dd / g;
            if (P2 * Q >= P * Q2) { printf("  ERROR: ratio did not decrease\n"); return 1; }
            P = P2; Q = Q2;
            printCycle(cyc);
        }
    }
    printf("total %.0fs\n", el());
    return 0;
}
