// B5f (KT Lower Bounds, 2026-10-03): is the U collar the J-cheapest filling of its width-6 pairing class?
// Width-6 strip, cells x = 0..5, scan order (y, x). Fixed boundary = the U collar of FOLD (period 1): ports (4,y)-(6,y+1),
// (5,y)-(7,y+1), so cells 4, 5 have internal degree 1 and cells 0..3 degree 2. U pairing: the path through port (5,r)
// ends at port (4,r+2). State = (x, pending internal edges, piece label per pending end, piece type), types
// G (no port, 2 ends), V (holds its partner pair, 2 ends), W0 / W1 (holds port (5,r), 1 end, partner row due in 0 / 1 rows).
// Arc weight (units of 2J, Structures 13.5): 2 * (new X3 crossings) + at row end (Q3 of the square row - 6).
// A walk from the U state back to the U state = a pairing-preserving filling of a box in the U field (no internal
// cycle), and its weight = 2J(box) - 2J(U collar) up to booking at the box ends. Bellman-Ford from U on the SCC of U:
// convergence => every such walk has weight >= 0 (exact, C = 0 in this booking); else a negative cycle = a periodic
// filling cheaper than U per row.
// usage: b5f build [maxstates] [maxpasses]      |  b5f walk FILE   (FILE: lines "x y dx dy", up-edges of rows Y0..Y1-1)
#include <bits/stdc++.h>
#include "b5f_tables.h"
using namespace std;
typedef unsigned long long u64;
static const int NEED[6] = {2, 2, 2, 2, 1, 1};
static const int DX[4] = {2, -2, 1, -1}, DY[4] = {1, 1, 2, 2};
static inline int sid(int lx, int ly, int m) { return ((ly + 2) * 6 + lx) * 4 + m; }
static inline int slx(int s) { return (s / 4) % 6; }
static inline int sly(int s) { return s / 24 - 2; }
static inline int sux(int s) { return slx(s) + DX[s % 4]; }
static inline int suy(int s) { return sly(s) + DY[s % 4]; }
struct __attribute__((packed)) Key { u64 a, b; uint32_t c; bool operator==(const Key &o) const { return a == o.a && b == o.b && c == o.c; } };
struct St { int x, n, slot[24], lab[24], ty[24]; };   // ty indexed by label (labels < 24 before canonical relabel)
static int MAXE = 0, MAXP = 0;
static int LAM = getenv("B5F_LAM") ? atoi(getenv("B5F_LAM")) : 6;   // per-row test value (U collar: 6)
static bool TRUNC = getenv("B5F_TRUNC") != nullptr;
static bool JP = getenv("B5F_JP") != nullptr;   // J' = J + Y_sh (BEYOND5 13.8): shallow pairs outside S3 at weight 2 (units 2J)            // test only: drop arcs to states beyond the cap
// 160-bit key: bits 0..45 pending-slot mask (46 pendable slots), 46..48 x, 49..74 piece types (13 x 2), 75..158 labels (21 x 4)
static int CI[72], CS[46];
static void init_ci() { int k = 0; for (int sl = 0; sl < 72; sl++) { CI[sl] = -1; if (VALID[sl] && (sly(sl) >= -1 || DY[sl % 4] == 2)) { CI[sl] = k; CS[k++] = sl; } } if (k != 46) { fprintf(stderr, "CI %d\n", k); exit(2); } }
static inline void putb(u64 *w, int pos, int nb, u64 v) { for (int i = 0; i < nb; i++) if (v >> i & 1) w[(pos + i) >> 6] |= 1ULL << ((pos + i) & 63); }
static inline u64 getb(const u64 *w, int pos, int nb) { u64 v = 0; for (int i = 0; i < nb; i++) v |= ((w[(pos + i) >> 6] >> ((pos + i) & 63)) & 1ULL) << i; return v; }
static Key enc(const St &s) {
    int ord[24];
    for (int i = 0; i < s.n; i++) ord[i] = i;
    sort(ord, ord + s.n, [&](int i, int j) { return s.slot[i] < s.slot[j]; });
    int mp[24]; memset(mp, -1, sizeof mp); int np = 0;
    u64 w[3] = {0, 0, 0};
    if (s.n > 21) { fprintf(stderr, "state too large: %d ends\n", s.n); exit(2); }
    for (int t = 0; t < s.n; t++) {
        int i = ord[t], sl = s.slot[i];
        if (t && s.slot[ord[t - 1]] == sl) { fprintf(stderr, "duplicate slot\n"); exit(2); }
        if (CI[sl] < 0) { fprintf(stderr, "unpendable slot %d\n", sl); exit(2); }
        putb(w, CI[sl], 1, 1);
        if (mp[s.lab[i]] < 0) { mp[s.lab[i]] = np++; }
        putb(w, 75 + 4 * t, 4, mp[s.lab[i]]);
    }
    if (np > 13) { fprintf(stderr, "state too large: %d pieces\n", np); exit(2); }
    MAXE = max(MAXE, s.n); MAXP = max(MAXP, np);
    putb(w, 46, 3, s.x);
    for (int l = 0; l < 24; l++) if (mp[l] >= 0) {
        int t = s.ty[l]; if (t < 0 || t > 3) { fprintf(stderr, "bad type %d\n", t); exit(2); }
        putb(w, 49 + 2 * mp[l], 2, t);
    }
    return Key{w[0], w[1], (uint32_t)w[2]};
}
static St dec(const Key &k) {
    u64 w[3] = {k.a, k.b, k.c};
    St s; s.x = getb(w, 46, 3); s.n = 0;
    for (int ci = 0; ci < 46; ci++) if (getb(w, ci, 1)) { s.slot[s.n] = CS[ci]; s.lab[s.n] = getb(w, 75 + 4 * s.n, 4); s.n++; }
    for (int l = 0; l < 24; l++) s.ty[l] = l < 13 ? getb(w, 49 + 2 * l, 2) : -1;
    return s;
}
// expand: callback(Key next, int weight, int chosenMask over cands, const int* cands)
template <class F> static void expand(const St &s, F &&cb) {
    int x = s.x, inc[24], ni = 0, rest[24], nr = 0;
    for (int i = 0; i < s.n; i++) {
        if (sux(s.slot[i]) == x && suy(s.slot[i]) == 0) inc[ni++] = i; else rest[nr++] = i;
    }
    int r = NEED[x] - ni;
    if (r < 0) return;
    int cands[4], nc = 0;
    for (int m = 0; m < 4; m++) if (x + DX[m] >= 0 && x + DX[m] < 6) cands[nc++] = sid(x, 0, m);
    int td0[6][3] = {{0}};
    for (int j = 0; j < nr; j++) { int sl = s.slot[rest[j]]; td0[sux(sl)][suy(sl)]++; }
    bool closed = false;
    if (ni == 2 && s.lab[inc[0]] == s.lab[inc[1]]) {
        if (s.ty[s.lab[inc[0]]] != 1 || x >= 4) return;   // closing a G piece = internal cycle
        closed = true;
    }
    // incoming pieces
    int ip[2], nip = 0;
    for (int i = 0; i < ni; i++) { int l = s.lab[inc[i]]; bool seen = false; for (int j = 0; j < nip; j++) seen |= ip[j] == l; if (!seen) ip[nip++] = l; }
    int nW = 0, nV = 0, wkind = -1;
    for (int j = 0; j < nip; j++) { int t = s.ty[ip[j]]; if (t == 1) nV++; else if (t >= 2) { nW++; wkind = t; } }
    int wd = -1, nwd = 0;
    for (int i = 0; i < s.n; i++) if (s.ty[s.lab[i]] == 2) { if (wd != s.lab[i]) { wd = s.lab[i]; nwd++; } }
    for (int mask = 0; mask < (1 << nc); mask++) {
        if (__builtin_popcount(mask) != r) continue;
        int td[6][3]; memcpy(td, td0, sizeof td); bool ok = true;
        int ch[4], nch = 0;
        for (int j = 0; j < nc; j++) if (mask >> j & 1) {
            int sl = cands[j]; ch[nch++] = sl;
            if (++td[sux(sl)][suy(sl)] > NEED[sux(sl)]) ok = false;
        }
        if (!ok) continue;
        // weight: X3 crossings of new edges
        int w = 0;
        for (int i = 0; i < nch; i++) {
            for (int j = 0; j < nr; j++) w += 2 * X3[s.slot[rest[j]]][ch[i]] + (JP ? 2 * YS[s.slot[rest[j]]][ch[i]] : 0);
            for (int j = 0; j < i; j++) w += 2 * X3[ch[j]][ch[i]] + (JP ? 2 * YS[ch[j]][ch[i]] : 0);
        }
        St t; t.x = x; t.n = 0;
        for (int l = 0; l < 24; l++) t.ty[l] = s.ty[l];
        if (closed) {
            for (int j = 0; j < nr; j++) { t.slot[t.n] = s.slot[rest[j]]; t.lab[t.n] = s.lab[rest[j]]; t.n++; }
        } else {
            auto inip = [&](int l) { for (int j = 0; j < nip; j++) if (ip[j] == l) return true; return false; };
            int pe[24], npe = 0;           // ends of the merged piece
            for (int j = 0; j < nr; j++) if (inip(s.lab[rest[j]])) pe[npe++] = s.slot[rest[j]];
            for (int i = 0; i < nch; i++) pe[npe++] = ch[i];
            int typ; bool fuse = false;
            if (x <= 3) {
                if (nW + nV > 1) continue;
                typ = nW ? wkind : (nV ? 1 : 0);
            } else if (x == 5) {
                if (nW || nV) continue;
                typ = 4;
            } else {   // x == 4: port (4,0) pairs with the W due 0
                if (nwd != 1 || nV) continue;
                if (nW && wkind != 2) continue;
                if (nW) { typ = -1; if (npe) continue; }
                else {
                    for (int j = 0; j < nr; j++) if (s.lab[rest[j]] == wd) pe[npe++] = s.slot[rest[j]];
                    fuse = true; typ = 1;
                }
            }
            int needE = typ < 0 ? 0 : (typ <= 1 ? 2 : 1);
            if (npe != needE) continue;
            for (int j = 0; j < nr; j++) {
                int l = s.lab[rest[j]];
                if (inip(l) || (fuse && l == wd)) continue;
                t.slot[t.n] = s.slot[rest[j]]; t.lab[t.n] = l; t.n++;
            }
            if (typ >= 0) {
                int nl = 23;   // fresh label (canonical labels are < 13)
                t.ty[nl] = typ;
                for (int i = 0; i < npe; i++) { t.slot[t.n] = pe[i]; t.lab[t.n] = nl; t.n++; }
            }
        }
        if (x == 5) {
            // Q3 of square row 0, squares x = 0..4 (20 quarters), from pending edges + the two fixed ports
            int sl[26], ns = 0;
            for (int i = 0; i < t.n; i++) sl[ns++] = t.slot[i];
            sl[ns++] = 72; sl[ns++] = 73;
            int m[20] = {0};
            for (int i = 0; i < ns; i++) for (int q = 0; q < 20; q++) if (QM[sl[i]] >> q & 1) m[q]++;
            int q3 = 0;
            for (int q = 0; q < 20; q++) {
                if (m[q] == 0) q3 += 1;
                q3 += max(max(0, m[q] - 2), max(2 * m[q] - 5, 3 * m[q] - 9));
            }
            for (int i = 0; i < ns; i++) for (int j = i + 1; j < ns; j++) {
                int q = X1Q[sl[i]][sl[j]];
                if (q >= 0 && m[q] == 2) q3 += 1;
            }
            if (JP) for (int i = 0; i < t.n; i++) w += 2 * YS[72][t.slot[i]] + 2 * YS[73][t.slot[i]];   // row-0 ports vs pending edges
            w += q3 - LAM;
            for (int i = 0; i < t.n; i++) {
                if (t.slot[i] < 24) { fprintf(stderr, "row-2 edge left at row end\n"); exit(2); }
                t.slot[i] -= 24;
            }
            for (int l = 0; l < 24; l++) {
                if (t.ty[l] == 2) {
                    bool used = false; for (int i = 0; i < t.n; i++) used |= t.lab[i] == l;
                    if (used) { fprintf(stderr, "W due 0 left at row end\n"); exit(2); }
                }
                if (t.ty[l] == 3) t.ty[l] = 2; else if (t.ty[l] == 4) t.ty[l] = 3;
            }
            t.x = 0;
        } else t.x = x + 1;
        if (w > 120 || w < -120) { fprintf(stderr, "weight out of range\n"); exit(2); }
        cb(enc(t), w, nch, ch);
    }
}
static void rowdfs(const St &s, int acc, int depth, vector<pair<Key, int>> &out) {
    expand(s, [&](Key n2, int w, int, const int *) { if (depth == 5) out.push_back({n2, acc + w}); else rowdfs(dec(n2), acc + w, depth + 1, out); });
}
static St ustate() {   // U collar frontier before cell (0,0); from b5f_size.py u_state()
    St s; s.x = 0; s.n = 0; for (int l = 0; l < 24; l++) s.ty[l] = -1;
    int E[6][5] = {{0, -1, 2, 0, 0}, {1, -2, 0, 0, 1}, {1, -1, 0, 1, 2}, {1, -1, 3, 0, 2}, {2, -1, 4, 0, 3}, {3, -1, 5, 0, 1}};
    for (auto &e : E) {
        int m = -1; for (int k = 0; k < 4; k++) if (DX[k] == e[2] - e[0] && DY[k] == e[3] - e[1]) m = k;
        s.slot[s.n] = sid(e[0], e[1], m); s.lab[s.n] = e[4]; s.n++;
    }
    s.ty[0] = 3; s.ty[1] = 0; s.ty[2] = 0; s.ty[3] = 2;
    return s;
}
static long rss_mb() { long a, b; FILE *f = fopen("/proc/self/statm", "r"); if (fscanf(f, "%ld %ld", &a, &b) != 2) b = 0; fclose(f); return b * 4096 / 1048576; }
struct KH { size_t operator()(const Key &k) const { u64 h = k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL ^ k.c * 0x165667B19E3779F9ULL; return h ^ (h >> 29); } };
template <class T> struct CV {   // chunked vector, no doubling copies
    vector<T *> bl; size_t n = 0; static const size_t B = 1 << 22;
    void push(const T &v) { if (n % B == 0) bl.push_back(new T[B]); bl[n / B][n % B] = v; n++; }
    T &operator[](size_t i) { return bl[i / B][i % B]; }
    void clear() { for (auto p : bl) delete[] p; bl.clear(); n = 0; }
};

int main(int argc, char **argv) {
    string mode = argc > 1 ? argv[1] : "build";
    init_ci();
    Key k0 = enc(ustate());
    if (mode == "walk") {
        // up-edges per cell from file; follow them from the U state
        map<pair<int, int>, vector<pair<int, int>>> up; int y0 = INT_MAX, y1 = INT_MIN;
        FILE *f = fopen(argv[2], "r"); int a, b, c, d;
        while (fscanf(f, "%d %d %d %d", &a, &b, &c, &d) == 4) { up[{a, b}].push_back({c, d}); y0 = min(y0, b); y1 = max(y1, b); }
        fclose(f);
        Key cur = k0; long tot = 0;
        for (int y = y0; y <= y1; y++) {
            long rowW = 0;
            for (int x = 0; x < 6; x++) {
                set<int> want; for (auto &p : up[{x, y}]) { int m = -1; for (int k = 0; k < 4; k++) if (DX[k] == p.first && DY[k] == p.second) m = k; want.insert(sid(x, 0, m)); }
                int found = 0; Key nx{}; int wt = 0;
                expand(dec(cur), [&](Key n2, int w, int nch, const int *ch) { set<int> got(ch, ch + nch); if (got == want) { found++; nx = n2; wt = w; } });
                if (found != 1) { printf("walk FAILED at cell (%d,%d): %d matching transitions\n", x, y, found); return 1; }
                cur = nx; rowW += wt;
            }
            tot += rowW; printf("row %d weight %ld\n", y, rowW);
        }
        printf("walk total weight %ld (units of 2J relative to 6 per row); back to U state: %s\n", tot, cur == k0 ? "yes" : "no");
        return 0;
    }
    size_t cap = argc > 2 ? atoll(argv[2]) : (size_t)170000000; long maxpass = argc > 3 ? atol(argv[3]) : 100000;
    int tbits = argc > 4 ? atoi(argv[4]) : 28;
    // ---- build (BFS from the U state); open addressing table of 2^tbits uint32 (index + 1), keys stored once ----
    CV<Key> keys; size_t A = 0;   // arcs are streamed to disk during the build (b5f_off.bin, b5f_dst.bin, b5f_wt.bin)
    FILE *fo = fopen("b5f_off.bin", "wb"), *fd = fopen("b5f_dst.bin", "wb"), *fw = fopen("b5f_wt.bin", "wb");
    setvbuf(fo, nullptr, _IOFBF, 1 << 24); setvbuf(fd, nullptr, _IOFBF, 1 << 24); setvbuf(fw, nullptr, _IOFBF, 1 << 24);
    bool ROWS = getenv("B5F_ROWS") != nullptr;   // store only row-start states; arcs = whole rows (min weight per successor)
    vector<pair<Key, int>> succ;
    size_t TS = (size_t)1 << tbits, TM = TS - 1;
    if (cap > TS * 3 / 4) cap = TS * 3 / 4;
    uint32_t *tab = (uint32_t *)calloc(TS, 4);
    if (!tab) { printf("table alloc failed\n"); return 2; }
    KH kh;
    auto look = [&](const Key &k, bool ins, bool &isnew) -> uint32_t {
        size_t h = kh(k) & TM;
        while (tab[h]) { if (keys[tab[h] - 1] == k) { isnew = false; return tab[h] - 1; } h = (h + 1) & TM; }
        isnew = true; if (!ins) return UINT32_MAX;
        uint32_t j = keys.n; keys.push(k); tab[h] = j + 1; return j;
    };
    { bool nw; look(k0, true, nw); }
    auto t0 = chrono::steady_clock::now();
    for (size_t i = 0; i < keys.n; i++) {
        if (A >= 0xFFFFFFF0ULL) { printf("too many arcs for uint32 offsets\n"); return 2; }
        { uint32_t o = A; fwrite(&o, 4, 1, fo); }
        auto add = [&](Key n2, int w) {
            bool nw; uint32_t j;
            if (TRUNC && keys.n >= cap) { j = look(n2, false, nw); if (nw) return; }
            else j = look(n2, true, nw);
            if (nw && keys.n > cap) { printf("CAP %zu reached: states %zu arcs %zu rss %ld MB\n", cap, keys.n, A, rss_mb()); fflush(stdout); exit(3); }
            if (w < -32000 || w > 32000) { printf("weight overflow\n"); exit(2); }
            int16_t w16 = w; fwrite(&j, 4, 1, fd); fwrite(&w16, 2, 1, fw); A++;
        };
        if (!ROWS) expand(dec(keys[i]), [&](Key n2, int w, int, const int *) { add(n2, w); });
        else {
            succ.clear(); rowdfs(dec(keys[i]), 0, 0, succ);
            sort(succ.begin(), succ.end(), [](const pair<Key, int> &p, const pair<Key, int> &q) {
                return make_tuple((u64)p.first.a, (u64)p.first.b, (uint32_t)p.first.c, p.second) < make_tuple((u64)q.first.a, (u64)q.first.b, (uint32_t)q.first.c, q.second); });
            for (size_t t = 0; t < succ.size(); t++) if (t == 0 || !(succ[t].first == succ[t - 1].first)) add(succ[t].first, succ[t].second);
        }
        if (i % (ROWS ? 2000000 : 10000000) == 0 && i) printf("  expanded %zu states %zu arcs %zu rss %ld MB %.0fs\n", i, keys.n, A, rss_mb(), chrono::duration<double>(chrono::steady_clock::now() - t0).count()), fflush(stdout);
    }
    { uint32_t o = A; fwrite(&o, 4, 1, fo); }
    fclose(fo); fclose(fd); fclose(fw);
    size_t N = keys.n;
    printf("built: states %zu arcs %zu max ends %d max pieces %d rss %ld MB %.0fs\n", N, A, MAXE, MAXP, rss_mb(), chrono::duration<double>(chrono::steady_clock::now() - t0).count());
    fflush(stdout);
    free(tab);
    { FILE *kf = fopen("b5f_keys.bin", "wb"); for (size_t i = 0; i < N; i++) fwrite(&keys[i], sizeof(Key), 1, kf); fclose(kf); }
    keys.clear();
    printf("table freed, keys written to b5f_keys.bin, rss %ld MB\n", rss_mb());
    vector<uint32_t> off(N + 1), dst(A); vector<int16_t> wt(A);
    { FILE *f = fopen("b5f_off.bin", "rb"); if (fread(off.data(), 4, N + 1, f) != N + 1) exit(2); fclose(f);
      f = fopen("b5f_dst.bin", "rb"); if (fread(dst.data(), 4, A, f) != A) exit(2); fclose(f);
      f = fopen("b5f_wt.bin", "rb"); if (fread(wt.data(), 2, A, f) != A) exit(2); fclose(f); }
    printf("arcs loaded, rss %ld MB\n", rss_mb()); fflush(stdout);
    auto keyat = [&](uint32_t i) { Key k; FILE *kf = fopen("b5f_keys.bin", "rb"); fseek(kf, (long)i * sizeof(Key), SEEK_SET); if (fread(&k, sizeof k, 1, kf) != 1) exit(2); fclose(kf); return k; };
    // ---- co-reachability to U: sweeps in reverse index order until stable (no reverse arcs, to save memory) ----
    vector<char> co(N, 0); co[0] = 1;
    for (int sw = 1;; sw++) {
        bool ch = false;
        for (size_t u = N; u-- > 0;) {
            if (co[u]) continue;
            for (u64 a = off[u]; a < (u64)off[u + 1]; a++) if (co[dst[a]]) { co[u] = 1; ch = true; break; }
        }
        if (!ch) { printf("co-reachability: %d sweeps\n", sw); break; }
    }
    size_t NC = 0; for (size_t v = 0; v < N; v++) NC += co[v];
    printf("SCC of U (reachable from U and back): %zu states; rss %ld MB\n", NC, rss_mb()); fflush(stdout);
    // ---- Bellman-Ford from U (weights in units of 2J, test value 6 per row already subtracted) ----
    const int INF = INT_MAX / 4;
    vector<int> d(N, INF); vector<uint32_t> par(N, UINT32_MAX); d[0] = 0;
    long pass = 0; bool changed = true; uint32_t lastv = 0;
    while (changed && pass < maxpass) {
        changed = false; pass++;
        for (size_t u = 0; u < N; u++) {
            if (!co[u] || d[u] >= INF) continue;
            for (u64 a = off[u]; a < (u64)off[u + 1]; a++) {
                uint32_t v = dst[a]; if (!co[v]) continue;
                int nd = d[u] + wt[a];
                if (nd < d[v]) { d[v] = nd; par[v] = u; changed = true; lastv = v; }
            }
        }
        if (d[0] < 0) { printf("negative closed walk through U found at pass %ld\n", pass); break; }
        if (pass % 50 == 0) printf("  pass %ld\n", pass), fflush(stdout);
    }
    if (!changed && d[0] == 0) {
        int lo = INF, hi = -INF; for (size_t v = 0; v < N; v++) if (co[v]) { lo = min(lo, d[v]); hi = max(hi, d[v]); }
        printf("CERTIFIED after %ld passes: every walk U -> U has weight >= 0, i.e. 2J(box) >= 2J(U collar) for every\n"
               "pairing-preserving width-6 filling. Potential d range %d..%d (units 2J).\n", pass, lo, hi);
        return 0;
    }
    // negative cycle: walk parents N steps from lastv, then trace
    uint32_t v = d[0] < 0 ? 0 : lastv;
    for (size_t i = 0; i < N && par[v] != UINT32_MAX; i++) v = par[v];
    vector<uint32_t> cyc{v}; uint32_t u = par[v];
    while (u != v && cyc.size() <= N) { cyc.push_back(u); u = par[u]; }
    reverse(cyc.begin(), cyc.end());
    long cw = 0;
    for (size_t i = 0; i < cyc.size(); i++) {
        uint32_t a0 = cyc[i], b0 = cyc[(i + 1) % cyc.size()]; int best = INF;
        for (u64 a = off[a0]; a < (u64)off[a0 + 1]; a++) if (dst[a] == b0) best = min(best, (int)wt[a]);
        cw += best;
    }
    double rows = ROWS ? cyc.size() : cyc.size() / 6.0;
    printf("NOT certified: negative cycle of %.2f rows, weight %ld, mean 2J per row %.4f (U: 6)\n", rows, cw, LAM + cw / rows);
    for (size_t i = 0; i < cyc.size(); i++) {
        St s = dec(keyat(cyc[i])); printf("  x%d:", s.x);
        for (int j = 0; j < s.n; j++) printf(" (%d,%d)-(%d,%d)L%dT%d", slx(s.slot[j]), sly(s.slot[j]), sux(s.slot[j]), suy(s.slot[j]), s.lab[j], s.ty[s.lab[j]]);
        printf("\n");
    }
    return 1;
}
