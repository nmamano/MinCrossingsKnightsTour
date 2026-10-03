// BEYOND5 R-d (KT Lower Bounds, 2026-10-03). Compact version of free_aug.cpp: arcs stored as (uint32 dst, int16
// base weight, int8 Y), uint32 offsets, hash table freed after the search (base13_<orient>.bin from dump_base.py).
// Certifies, per half side:
//   (X3 - rows) + Q3/2 >= A #g + Cc N_free(d0) + Y-term - C,
//   mode b : Y-term = b N_near(d0),  N_near = all changed ports - N_free   (Dinkelbach for the largest b)
//   mode aF: Y-term = aF F',  F' = rows with g = 0 and no port (2,R)-(4,R+-1)   (Dinkelbach for the largest aF)
// Augmented buffer and Q3 / column-3 hole rules exactly as free_aug.cpp with HOLES = 4.
// Weight (units 1/(10 den)) for parameter num/den:  den (2(5w-1) - 10 A g + 5 q3h - 10 Cc qf) - 10 num Y.
// usage: free_aug2 base13.bin d0 A Cc b|aF num den [reserve_states reserve_arcs]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
using namespace std;
typedef long long ll;
static int d0, Dn; static bool MODE_AF;
static const int COV_B[] = {-1, 0, 1}, COV_R[] = {-1, 0, 1, 2}, COV_T[] = {0, 1, 2}, COV_L[] = {0, 1};
struct Cov { const int *r; int n; };
static const Cov COV[4] = {{COV_B, 3}, {COV_R, 4}, {COV_T, 3}, {COV_L, 2}};
struct Buf { int tl[4]; int gb[6]; int u1, u2, s0, s1, s2, s3, pb; };
static uint64_t enc(const Buf &b) {
    uint64_t c = 0;
    for (int j = 0; j <= Dn; j++) { if (b.tl[j] < 0 || b.tl[j] > 15) { fprintf(stderr, "tally overflow\n"); exit(2); } c = c * 16 + b.tl[j]; }
    for (int i = 0; i < Dn + d0; i++) c = c * 2 + b.gb[i];
    c = c * 16 + b.u1; c = c * 16 + b.u2;
    c = c * 2 + b.s0; c = c * 2 + b.s1; c = c * 2 + b.s2; c = c * 2 + b.s3; c = c * 2 + b.pb;
    return c;
}
static Buf dec(uint64_t c) {
    Buf b; b.pb = c & 1; c >>= 1; b.s3 = c & 1; c >>= 1; b.s2 = c & 1; c >>= 1; b.s1 = c & 1; c >>= 1; b.s0 = c & 1; c >>= 1;
    b.u2 = c & 15; c >>= 4; b.u1 = c & 15; c >>= 4;
    for (int i = Dn + d0 - 1; i >= 0; i--) { b.gb[i] = c & 1; c >>= 1; }
    for (int j = Dn; j >= 0; j--) { b.tl[j] = c & 15; c >>= 4; }
    return b;
}
static int prune(int u, const int *sr) {
    int out = 0;
    for (int q = 0; q < 4; q++) if (u >> q & 1) {
        bool ok = true; for (int k = 0; k < COV[q].n; k++) if (sr[COV[q].r[k] + 1] == 0) ok = false;
        if (ok) out |= 1 << q;
    }
    return out;
}
struct Rec { int src, dst, w, g, c0, c1, c2, re, q3, sat, u3, x, p24; };
struct Out { uint64_t key; int w, g, qf, q3h, ntot, fp; };
static Out step(const Buf &b, const Rec &r) {
    Buf t = b; t.tl[0] += r.c0; t.tl[1] += r.c1; t.tl[2] += r.c2;
    if (r.sat) t.s0 = 1;
    if (MODE_AF && r.p24) t.pb = 1;
    Out o; o.w = r.w; o.g = r.re ? r.g : 0; o.qf = 0; o.q3h = r.q3; o.ntot = r.c0 + r.c1 + r.c2; o.fp = 0;
    Buf nb = t;
    if (r.re) {
        int g = r.g; bool far = true;
        for (int j = Dn - d0; j <= Dn + d0; j++) if ((j == 0 ? g : t.gb[j - 1]) != 0) far = false;
        o.qf = far ? t.tl[Dn] : 0;
        if (MODE_AF) o.fp = (1 - g) * (1 - t.pb);
        int holes = 0;
        if (t.u2) { int sr[4] = {t.s3, t.s2, t.s1, t.s0}; for (int q = 0; q < 4; q++) if (t.u2 >> q & 1) { bool ok = true; for (int k = 0; k < COV[q].n; k++) if (!sr[COV[q].r[k] + 1]) ok = false; holes += ok; } }
        o.q3h += holes;
        int srR[4] = {t.s1, t.s0, -1, -1}; int uR = prune(r.u3, srR);
        int sr1[4] = {t.s2, t.s1, t.s0, -1}; int u1 = prune(t.u1, sr1);
        nb.u1 = uR; nb.u2 = u1; nb.s1 = (u1 || uR) ? t.s0 : 0; nb.s2 = (u1 || uR) ? t.s1 : 0; nb.s3 = u1 ? t.s2 : 0; nb.s0 = 0; nb.pb = 0;
        for (int j = Dn; j >= 1; j--) nb.tl[j] = t.tl[j - 1]; nb.tl[0] = 0;
        for (int i = Dn + d0 - 1; i >= 1; i--) nb.gb[i] = t.gb[i - 1]; nb.gb[0] = g;
        for (int j = 1; j <= Dn; j++) if (nb.tl[j]) for (int i = 0; i < Dn + d0; i++) if (nb.gb[i] && abs(1 + i - j) <= d0) { nb.tl[j] = 0; break; }
        for (int i = 0; i < Dn + d0; i++) if (nb.gb[i]) {
            bool keep = 1 + i <= d0 + 2;
            for (int j = 1; j <= Dn && !keep; j++) if (nb.tl[j] && abs(1 + i - j) <= d0) keep = true;
            if (!keep) nb.gb[i] = 0;
        }
    }
    o.key = ((uint64_t)r.dst << 40) | enc(nb);
    return o;
}
static vector<uint64_t> keys; static vector<uint32_t> tab; static uint64_t mask;
static inline uint64_t hh(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
static void rehash(size_t cap) {
    tab.assign(cap, 0xffffffffu); mask = cap - 1;
    for (uint32_t id = 0; id < keys.size(); id++) { size_t i = hh(keys[id]) & mask; while (tab[i] != 0xffffffffu) i = (i + 1) & mask; tab[i] = id; }
}
static uint32_t find_or_add(uint64_t k, bool add) {
    size_t i = hh(k) & mask;
    while (tab[i] != 0xffffffffu) { if (keys[tab[i]] == k) return tab[i]; i = (i + 1) & mask; }
    if (!add) { fprintf(stderr, "missing key\n"); exit(3); }
    uint32_t id = keys.size(); keys.push_back(k); tab[i] = id;
    if (keys.size() * 10 > tab.size() * 8) rehash(tab.size() * 2);
    return id;
}
int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: free_aug2 base13.bin d0 A Cc b|aF num den\n"); return 1; }
    d0 = atoi(argv[2]); ll A = atoll(argv[3]), Cc = atoll(argv[4]); MODE_AF = string(argv[5]) == "aF";
    ll num = atoll(argv[6]), den = atoll(argv[7]); Dn = max(2, d0);
    FILE *f = fopen(argv[1], "rb"); int32_t hdr[2]; if (fread(hdr, 4, 2, f) != 2) return 1;
    int N = hdr[0]; ll M = hdr[1];
    vector<Rec> R(M); if (fread(R.data(), sizeof(Rec), M, f) != (size_t)M) return 1; fclose(f);
    sort(R.begin(), R.end(), [](const Rec &a, const Rec &b) { return a.src < b.src; });
    vector<ll> ptr(N + 1, 0); for (auto &r : R) ptr[r.src + 1]++; for (int i = 0; i < N; i++) ptr[i + 1] += ptr[i];
    fprintf(stderr, "base: %d states, %lld arcs, mode %s\n", N, M, MODE_AF ? "aF" : "b");
    Buf z; memset(&z, 0, sizeof z);
    rehash(1 << 24); find_or_add(enc(z), true);
    // BFS in id order; arcs stored compactly: off[u] (uint32), adst (uint32), abase (int16), ay (int8)
    vector<uint32_t> off; vector<uint32_t> adst; vector<int16_t> abase; vector<int8_t> ay;
    if (argc > 9) { size_t rs = atoll(argv[8]), ra = atoll(argv[9]); keys.reserve(rs); off.reserve(rs + 1); adst.reserve(ra); abase.reserve(ra); ay.reserve(ra); }
    off.push_back(0);
    for (size_t u = 0; u < keys.size(); u++) {
        uint64_t kv = keys[u]; int s = kv >> 40; Buf b = dec(kv & ((1ULL << 40) - 1));
        for (ll p = ptr[s]; p < ptr[s + 1]; p++) {
            Out o = step(b, R[p]); uint32_t v = find_or_add(o.key, true);
            ll bs = 2 * (5 * (ll)o.w - 1) - 10 * A * o.g + 5 * o.q3h - 10 * Cc * o.qf;
            ll Y = MODE_AF ? o.fp : (o.ntot - o.qf);
            if (bs < -32000 || bs > 32000 || Y < -120 || Y > 120) { fprintf(stderr, "range\n"); return 5; }
            adst.push_back(v); abase.push_back((int16_t)bs); ay.push_back((int8_t)Y);
        }
        if (adst.size() > 0xfffffff0ULL) { fprintf(stderr, "too many arcs\n"); return 6; }
        off.push_back((uint32_t)adst.size());
        if (u % 20000000 == 0 && u) fprintf(stderr, "  bfs %zu / %zu, arcs %zu\n", u, keys.size(), adst.size());
    }
    size_t S = keys.size(), E = adst.size();
    { vector<uint32_t> t; tab.swap(t); }
    adst.shrink_to_fit(); abase.shrink_to_fit(); ay.shrink_to_fit();
    fprintf(stderr, "augmented (d0=%d): states %zu, arcs %zu\n", d0, S, E);
    vector<int32_t> dist(S); vector<uint32_t> pred(S);
    for (;;) {
        fill(dist.begin(), dist.end(), 0); fill(pred.begin(), pred.end(), 0xffffffffu);
        bool conv = false; vector<pair<uint32_t, uint32_t>> cyc;   // (source state, arc index)
        for (int it = 1; it <= 100000 && !conv && cyc.empty(); it++) {
            bool ch = false;
            for (size_t u = 0; u < S; u++) {
                ll du = dist[u];
                for (uint32_t e = off[u]; e < off[u + 1]; e++) {
                    ll c = du + den * (ll)abase[e] - 10 * num * (ll)ay[e];
                    uint32_t v = adst[e];
                    if (c < dist[v]) { if (c < -2000000000LL) { fprintf(stderr, "dist overflow\n"); exit(4); } dist[v] = (int32_t)c; pred[v] = u; ch = true; if (v == u) du = c; }
                }
            }
            if (!ch) { conv = true; fprintf(stderr, "converged after %d passes\n", it); break; }
            if (it % 3 == 0) {
                vector<int8_t> st(S, 0);
                for (size_t s0 = 0; s0 < S && cyc.empty(); s0++) {
                    if (st[s0] || pred[s0] == 0xffffffffu) continue;
                    vector<uint32_t> path; uint32_t v = s0;
                    while (st[v] == 0) { st[v] = 1; path.push_back(v); if (pred[v] == 0xffffffffu) break; v = pred[v]; }
                    if (st[v] == 1 && pred[v] != 0xffffffffu) {
                        auto itv = find(path.begin(), path.end(), v);
                        if (itv != path.end()) for (auto jt = itv; jt != path.end(); ++jt) {
                            uint32_t to = *jt, fr = pred[to]; uint32_t best = 0xffffffffu; ll bw = 0;
                            for (uint32_t e = off[fr]; e < off[fr + 1]; e++) if (adst[e] == to) {
                                ll w = den * (ll)abase[e] - 10 * num * (ll)ay[e];
                                if (best == 0xffffffffu || w < bw) { best = e; bw = w; }
                            }
                            cyc.push_back({fr, best});
                        }
                    }
                    for (uint32_t x : path) st[x] = 2;
                }
            }
        }
        if (conv) {
            ll mn = 0; for (size_t i = 0; i < S; i++) mn = min(mn, (ll)dist[i]);
            printf("d0=%d A=%lld Cc=%lld mode %s: parameter %lld/%lld CERTIFIED; potential range %lld..0 (units 1/(10*%lld)); states %zu, arcs %zu\n",
                   d0, A, Cc, MODE_AF ? "aF" : "b", num, den, mn, den, S, E);
            return 0;
        }
        ll base = 0, Ys = 0, wsum = 0;
        for (auto &e : cyc) { base += abase[e.second]; Ys += ay[e.second]; wsum += den * (ll)abase[e.second] - 10 * num * (ll)ay[e.second]; }
        printf("negative cycle: %zu arcs (%zu rows): base sum %lld, Y sum %lld, weight %lld\n", cyc.size(), cyc.size() / 5, base, Ys, wsum);
        printf("  states:"); for (auto it = cyc.rbegin(); it != cyc.rend(); ++it) { uint64_t kv = keys[it->first]; printf(" %llu", (unsigned long long)(kv >> 40)); } printf("\n"); fflush(stdout);
        if (Ys <= 0 || base < 0) { printf("  parameter 0 fails on this cycle\n"); return 0; }
        ll g0 = gcd(base, 10 * Ys); num = base / g0; den = 10 * Ys / g0;
        printf("  -> parameter <= %lld/%lld = %.6f\n", num, den, (double)num / den); fflush(stdout);
    }
}
