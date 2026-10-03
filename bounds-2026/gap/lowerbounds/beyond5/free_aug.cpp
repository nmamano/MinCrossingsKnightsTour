// BEYOND5 R-a, Q3 form (KT Lower Bounds, 2026-10-03). C++ port of joint_free.py's augmentation and certificate.
// Certifies, per half side:  (X3 - rows) + Q3/2 >= #g + c * N_free(d0) - C.
// Input base_<orient>.bin from dump_base.py (width-three strip graph, one record per base arc).
// Augmented state = (base state, buffer). Buffer:
//   tallies tl[0..Dn] of changed ports booked on collar rows R..R-Dn (Dn = max(2, d0));
//   g bits gb[0..Dn+d0-1] of rows R-1..R-Dn-d0;
//   column-3 hole buffer: u1, u2 = quarters of squares (3, R-1), (3, R-2) that no model edge covers and whose
//   known covering column-3 rows are saturated; s0..s3 = saturation of column-3 vertices of rows R, R-1, R-2, R-3.
// HOLES=4: all quarters (square row R-2 decided at the end of row R); HOLES=2: quarters b, l only, as joint_free.py
// (square row R-1 decided at the end of row R); HOLES=0: no column-3 holes; HOLES=-1: pure crossings (Q3 dropped).
// Arc weight (units 1/(10b)) for c = a/b:  2b(5w - 1) - 10b g - 10a qf + 5b (q3 + holes).
// usage: free_aug base_up.bin d0 HOLES a b [crit]          (g coefficient 1, c = a/b)
//        free_aug base_up.bin d0 HOLES cn cd maxa an ad   (c = cn/cd fixed; Dinkelbach for the largest g coefficient,
//                                                          starting at an/ad)
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <cstring>
#include <algorithm>
#include <numeric>
#include <string>
using namespace std;
typedef long long ll;

static int d0, Dn, HOLES;
static const int COV_B[] = {-1, 0, 1}, COV_R[] = {-1, 0, 1, 2}, COV_T[] = {0, 1, 2}, COV_L[] = {0, 1};
struct Cov { const int *r; int n; };
static const Cov COV[4] = {{COV_B, 3}, {COV_R, 4}, {COV_T, 3}, {COV_L, 2}};   // bit order b, r, t, l

struct Buf { int tl[4]; int gb[6]; int u1, u2, s0, s1, s2, s3; };
static uint64_t enc(const Buf &b) {
    uint64_t c = 0;
    for (int j = 0; j <= Dn; j++) { if (b.tl[j] < 0 || b.tl[j] > 15) { fprintf(stderr, "tally overflow %d\n", b.tl[j]); exit(2); } c = c * 16 + b.tl[j]; }
    for (int i = 0; i < Dn + d0; i++) c = c * 2 + b.gb[i];
    c = c * 16 + b.u1; c = c * 16 + b.u2;
    c = c * 2 + b.s0; c = c * 2 + b.s1; c = c * 2 + b.s2; c = c * 2 + b.s3;
    return c;
}
static Buf dec(uint64_t c) {
    Buf b; b.s3 = c & 1; c >>= 1; b.s2 = c & 1; c >>= 1; b.s1 = c & 1; c >>= 1; b.s0 = c & 1; c >>= 1;
    b.u2 = c & 15; c >>= 4; b.u1 = c & 15; c >>= 4;
    for (int i = Dn + d0 - 1; i >= 0; i--) { b.gb[i] = c & 1; c >>= 1; }
    for (int j = Dn; j >= 0; j--) { b.tl[j] = c & 15; c >>= 4; }
    return b;
}
// sat lookup: rows relative to a square row
static int prune(int u, int mask_known, const int *satrow /* indexed dy+1, -1 = unknown */) {
    int out = 0;
    for (int q = 0; q < 4; q++) if (u >> q & 1) {
        bool ok = true;
        for (int k = 0; k < COV[q].n; k++) { int s = satrow[COV[q].r[k] + 1]; if (s == 0) ok = false; }
        if (ok) out |= 1 << q;
    }
    (void)mask_known; return out;
}

// open addressing hash map uint64 -> uint32
struct HMap {
    vector<uint64_t> k; vector<uint32_t> v; size_t cap, n = 0;
    HMap(size_t c) : k(c, ~0ULL), v(c), cap(c) {}
    static uint64_t h(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
    void grow() {
        HMap m(cap * 2);
        for (size_t i = 0; i < cap; i++) if (k[i] != ~0ULL) m.put(k[i], v[i]);
        k.swap(m.k); v.swap(m.v); cap = m.cap;
    }
    void put(uint64_t key, uint32_t val) {
        size_t i = h(key) & (cap - 1);
        while (k[i] != ~0ULL) { if (k[i] == key) { v[i] = val; return; } i = (i + 1) & (cap - 1); }
        k[i] = key; v[i] = val; n++;
    }
    // returns value or inserts val
    uint32_t get_or(uint64_t key, uint32_t val, bool &ins) {
        if (n * 10 > cap * 7) grow();
        size_t i = h(key) & (cap - 1);
        while (k[i] != ~0ULL) { if (k[i] == key) { ins = false; return v[i]; } i = (i + 1) & (cap - 1); }
        k[i] = key; v[i] = val; n++; ins = true; return val;
    }
};

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: free_aug base.bin d0 HOLES a b [crit]\n"); return 1; }
    d0 = atoi(argv[2]); HOLES = atoi(argv[3]); ll a = atoll(argv[4]), bb = atoll(argv[5]); bool crit = argc > 6;
    bool maxa = argc > 8 && string(argv[6]) == "maxa"; ll gan = 1, gad = 1;
    if (maxa) { gan = atoll(argv[7]); gad = atoll(argv[8]); }
    Dn = max(2, d0);
    FILE *f = fopen(argv[1], "rb"); int32_t hdr[2]; if (fread(hdr, 4, 2, f) != 2) return 1;
    int N = hdr[0]; ll M = hdr[1];
    vector<int32_t> R((size_t)M * 11); if (fread(R.data(), 4, R.size(), f) != R.size()) return 1; fclose(f);
    // CSR by source
    vector<ll> ptr(N + 1, 0); for (ll e = 0; e < M; e++) ptr[R[e * 11] + 1]++;
    for (int i = 0; i < N; i++) ptr[i + 1] += ptr[i];
    vector<ll> ord(M); { vector<ll> pos(ptr.begin(), ptr.end() - 1); for (ll e = 0; e < M; e++) ord[pos[R[e * 11]]++] = e; }
    fprintf(stderr, "base: %d states, %lld arcs\n", N, M);
    // augmented BFS
    HMap idx(1 << 24);
    vector<uint64_t> key; vector<uint32_t> AS, AD; vector<int8_t> AW, AG, AQ, A3; vector<int32_t> AK;
    Buf z; memset(&z, 0, sizeof z);
    const uint64_t SH = 40;
    bool ins; idx.get_or(((uint64_t)0 << SH) | enc(z), 0, ins); key.push_back(enc(z));
    for (size_t u = 0; u < key.size(); u++) {
        uint64_t kv = key[u]; int s = (int)(kv >> SH); Buf b = dec(kv & ((1ULL << SH) - 1));
        for (ll p = ptr[s]; p < ptr[s + 1]; p++) {
            ll e = ord[p]; const int32_t *r = &R[e * 11];
            int dst = r[1], w = r[2], g = r[3], c0 = r[4], c1 = r[5], c2 = r[6], re = r[7], q3 = r[8], sat = r[9], u3 = r[10];
            Buf t = b; t.tl[0] += c0; t.tl[1] += c1; t.tl[2] += c2;
            if (sat && HOLES > 0) t.s0 = 1;
            int qf = 0, holes = 0;
            Buf nb = t;
            if (re) {
                bool far = true;
                for (int j = Dn - d0; j <= Dn + d0; j++) if ((j == 0 ? g : t.gb[j - 1]) != 0) far = false;
                qf = far ? t.tl[Dn] : 0;
                int uR = u3, u1 = t.u1, u2 = t.u2;
                if (HOLES == 4) {
                    if (u2) { int sr[4] = {t.s3, t.s2, t.s1, t.s0}; for (int q = 0; q < 4; q++) if (u2 >> q & 1) { bool ok = true; for (int k = 0; k < COV[q].n; k++) if (!sr[COV[q].r[k] + 1]) ok = false; holes += ok; } }
                    int srR[4] = {t.s1, t.s0, -1, -1}; uR = prune(uR, 0, srR);
                    int sr1[4] = {t.s2, t.s1, t.s0, -1}; u1 = prune(u1, 0, sr1);
                    nb.u1 = uR; nb.u2 = u1;
                    nb.s1 = (u1 || uR) ? t.s0 : 0; nb.s2 = (u1 || uR) ? t.s1 : 0; nb.s3 = u1 ? t.s2 : 0; nb.s0 = 0;
                } else if (HOLES == 2) {   // b, l of square row R-1 decided now (joint_free.py rule)
                    if (u1) holes = ((u1 & 1) && t.s2 && t.s1 && t.s0) + ((u1 & 8) && t.s1 && t.s0);
                    int nu = ((uR & 1) && t.s1 && t.s0 ? 1 : 0) | ((uR & 8) && t.s0 ? 8 : 0);
                    nb.u1 = nu; nb.u2 = 0; nb.s1 = nu ? t.s0 : 0; nb.s2 = (nu & 1) ? t.s1 : 0; nb.s3 = 0; nb.s0 = 0;
                } else { nb.u1 = nb.u2 = nb.s0 = nb.s1 = nb.s2 = nb.s3 = 0; }
                // shift tallies and g bits, then canonicalize
                for (int j = Dn; j >= 1; j--) nb.tl[j] = t.tl[j - 1]; nb.tl[0] = 0;
                for (int i = Dn + d0 - 1; i >= 1; i--) nb.gb[i] = t.gb[i - 1]; nb.gb[0] = g;
                for (int j = 1; j <= Dn; j++) if (nb.tl[j]) for (int i = 0; i < Dn + d0; i++) if (nb.gb[i] && abs(1 + i - j) <= d0) { nb.tl[j] = 0; break; }
                for (int i = 0; i < Dn + d0; i++) if (nb.gb[i]) {
                    bool keep = 1 + i <= d0 + 2;
                    for (int j = 1; j <= Dn && !keep; j++) if (nb.tl[j] && abs(1 + i - j) <= d0) keep = true;
                    if (!keep) nb.gb[i] = 0;
                }
            }
            uint64_t kk = ((uint64_t)dst << SH) | enc(nb);
            uint32_t v = idx.get_or(kk, (uint32_t)key.size(), ins);
            if (ins) { key.push_back(kk); if (key.size() % 5000000 == 0) fprintf(stderr, "  aug states %zu\n", key.size()); }
            AS.push_back(u); AD.push_back(v); AW.push_back(w); AG.push_back(re ? g : 0); AQ.push_back(qf); A3.push_back(HOLES < 0 ? 0 : q3 + holes); AK.push_back((int32_t)e);
        }
    }
    size_t S = key.size(), E = AS.size();
    { HMap tmp(2); swap(idx.k, tmp.k); swap(idx.v, tmp.v); }
    fprintf(stderr, "augmented (d0=%d, HOLES=%d): states %zu, arcs %zu\n", d0, HOLES, S, E);
    vector<ll> dist(S), nd; vector<int64_t> par(S);
    for (;;) {
        // Bellman-Ford from 0 on all nodes, weight 2b(5w-1) - 10b g - 10a qf + 5b q3h
        fill(dist.begin(), dist.end(), 0); fill(par.begin(), par.end(), -1);
        bool conv = false; vector<int64_t> cyc;
        for (int it = 1; it <= 200000; it++) {
            bool ch = false;
            for (size_t e = 0; e < E; e++) {
                ll ww = gad * (2 * bb * (5 * (ll)AW[e] - 1) - 10 * a * AQ[e] + 5 * bb * A3[e]) - 10 * bb * gan * AG[e];
                ll c = dist[AS[e]] + ww;
                if (c < dist[AD[e]]) { dist[AD[e]] = c; par[AD[e]] = e; ch = true; }
            }
            if (!ch) { conv = true; fprintf(stderr, "converged after %d passes\n", it); break; }
            if (it % 5 == 0) {
                vector<int8_t> st(S, 0);
                for (size_t s0 = 0; s0 < S && cyc.empty(); s0++) {
                    if (st[s0] || par[s0] < 0) continue;
                    vector<size_t> path; size_t v = s0;
                    while (st[v] == 0) { st[v] = 1; path.push_back(v); if (par[v] < 0) break; v = AS[par[v]]; }
                    if (st[v] == 1 && par[v] >= 0) {
                        // v is on the current path: cycle
                        size_t k = find(path.begin(), path.end(), v) - path.begin();
                        bool onpath = k < path.size();
                        if (onpath) { for (size_t i = k; i < path.size(); i++) cyc.push_back(par[path[i]]); }
                    }
                    for (size_t x : path) st[x] = 2;
                }
                if (!cyc.empty()) break;
            }
        }
        if (conv) {
            ll mn = 0; for (size_t i = 0; i < S; i++) mn = min(mn, dist[i]);
            printf("d0=%d HOLES=%d: g coefficient %lld/%lld, c = %lld/%lld CERTIFIED; potential range %lld..0 (units 1/(10*%lld*%lld)), states %zu, arcs %zu\n", d0, HOLES, gan, gad, a, bb, mn, bb, gad, S, E);
            return 0;
        }
        if (cyc.empty()) { printf("no convergence\n"); return 1; }
        ll num = 0, den = 0, rows = 0, q3s = 0;
        for (int64_t e : cyc) { num += 2 * (5 * (ll)AW[e] - 1) - 10 * AG[e] + 5 * A3[e]; den += AQ[e]; q3s += A3[e]; }
        rows = cyc.size() / 5;
        printf("negative cycle: %zu arcs (%lld rows), sum(10w-2-10g+5q3) = %lld, sum q3+holes = %lld, sum Qfar = %lld\n", cyc.size(), rows, num, q3s, den);
        printf("  base arcs:"); for (auto it = cyc.rbegin(); it != cyc.rend(); ++it) printf(" %d", AK[*it]); printf("\n");
        fflush(stdout);
        if (maxa) {
            ll gs = 0, nm = 0; for (int64_t e : cyc) { gs += AG[e]; nm += 2 * bb * (5 * (ll)AW[e] - 1) - 10 * a * AQ[e] + 5 * bb * A3[e]; }
            if (gs <= 0) { printf("  cycle without g rows: c = %lld/%lld fails for every g coefficient\n", a, bb); return 0; }
            ll g0 = gcd(nm, 10 * bb * gs); gan = nm / g0; gad = 10 * bb * gs / g0;
            printf("  -> g coefficient <= %lld/%lld = %.6f\n", gan, gad, (double)gan / gad); fflush(stdout); continue;
        }
        if (!crit || den <= 0) return 0;
        ll g0 = gcd(num, 10 * den); a = num / g0; bb = 10 * den / g0;
        printf("  -> c <= %lld/%lld = %.6f\n", a, bb, (double)a / bb); fflush(stdout);
    }
}
