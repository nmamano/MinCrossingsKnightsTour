// strip2.cpp - independent C++ rebuild of the width-2 strip transfer graph (KT Edge Searcher, 2026-10-02)
// and checks of the strip facts used in w-turnstheory/FINDINGS.md section 7 and
// w-lowerbounds/TILE_INPUTS.md section 2.
//
// Model (from the definition in w-lowerbounds/FINDINGS.md F1 / strip_dp.py docstring):
//   columns 0,1 = strip cells, degree exactly 2; columns 2,3 = ghost cells, degree <= 2;
//   edges = knight moves inside columns 0..3 with at least one end in the strip;
//   no cycle; weight = number of proper crossings between chosen edges.
//   Cells are scanned in order (row y, column x = 0..3). At a cell, the UPWARD edges of the cell are
//   chosen (moves (2,1),(-2,1),(1,2),(-1,2)); a ghost cell may only go up to a strip cell.
//   State = (x, sorted pending edges (lx,ly,ux,uy,comp) with y relative to the current row,
//   comp = canonical component label of the path through that edge).
//   Arc weight = crossings of the chosen edges with pending edges and with each other
//   (minimum over choices that lead to the same next state).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct PE { int lx, ly, ux, uy, comp; };
static bool operator<(const PE& a, const PE& b) { return tie(a.lx, a.ly, a.ux, a.uy) < tie(b.lx, b.ly, b.ux, b.uy); }
static int orient(int ax, int ay, int bx, int by, int cx, int cy) { ll v = (ll)(bx - ax) * (cy - ay) - (ll)(by - ay) * (cx - ax); return (v > 0) - (v < 0); }
static bool crossE(int a, int b, int c, int d, int e, int f, int g, int h) {
    return orient(a, b, c, d, e, f) * orient(a, b, c, d, g, h) < 0 && orient(e, f, g, h, a, b) * orient(e, f, g, h, c, d) < 0;
}
const int K = 2, W = 4;
const int UPX[4] = {2, -2, 1, -1}, UPY[4] = {1, 1, 2, 2};

struct St { int x; vector<PE> e; };
string enc(const St& s) {
    string k; k.push_back((char)s.x);
    for (auto& p : s.e) { k.push_back((char)p.lx); k.push_back((char)p.ly); k.push_back((char)p.ux); k.push_back((char)p.uy); k.push_back((char)p.comp); }
    return k;
}
St dec(const string& k) {
    St s; s.x = k[0];
    for (size_t i = 1; i < k.size(); i += 5) s.e.push_back({(signed char)k[i], (signed char)k[i + 1], (signed char)k[i + 2], (signed char)k[i + 3], (signed char)k[i + 4]});
    return s;
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    unordered_map<string, int> id; vector<string> keys;
    vector<vector<pair<int, int>>> adj;   // (target, min weight)
    auto get = [&](const St& s) { string k = enc(s); auto it = id.find(k); if (it != id.end()) return it->second; int n = keys.size(); id[k] = n; keys.push_back(k); adj.emplace_back(); return n; };
    St start; start.x = 0; get(start);
    for (size_t q = 0; q < keys.size(); q++) {
        St s = dec(keys[q]); int x = s.x;
        vector<PE> in, rest;
        for (auto& p : s.e) (p.ux == x && p.uy == 0 ? in : rest).push_back(p);
        bool strip = x < K;
        vector<array<int, 4>> cand;
        for (int m = 0; m < 4; m++) { int tx = x + UPX[m]; if (tx >= 0 && tx < W && (strip || tx < K)) cand.push_back({x, 0, tx, UPY[m]}); }
        vector<int> need;
        int din = in.size();
        if (strip) { if (2 - din < 0) continue; need = {2 - din}; }
        else { if (din > 2) continue; for (int r = 0; r <= 2 - din; r++) need.push_back(r); }
        if (din == 2 && in[0].comp == in[1].comp) continue;   // would close a cycle
        map<int, int> out;
        int nc = cand.size();
        for (int r : need) for (int msk = 0; msk < (1 << nc); msk++) {
            if (__builtin_popcount(msk) != r) continue;
            vector<array<int, 4>> ch; for (int i = 0; i < nc; i++) if (msk >> i & 1) ch.push_back(cand[i]);
            // target degree
            map<pair<int, int>, int> td; bool ok = true;
            for (auto& p : rest) td[{p.ux, p.uy}]++;
            for (auto& f : ch) if (++td[{f[2], f[3]}] > 2) ok = false;
            if (!ok) continue;
            int w = 0;
            for (size_t i = 0; i < ch.size(); i++) {
                auto& f = ch[i];
                for (auto& p : rest) w += crossE(p.lx, p.ly, p.ux, p.uy, f[0], f[1], f[2], f[3]);
                for (size_t j = 0; j < i; j++) w += crossE(ch[j][0], ch[j][1], ch[j][2], ch[j][3], f[0], f[1], f[2], f[3]);
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
            auto it = out.find(tid); if (it == out.end() || it->second > w) out[tid] = w;
        }
        for (auto& kv : out) adj[q].push_back(kv);
    }
    int N = keys.size(); long A = 0; for (auto& a : adj) A += a.size();
    printf("states %d arcs %ld\n", N, A);
    // ---- exact checks with integer weights ----
    // Bellman-Ford from a virtual source (all distances start at 0); returns false on a negative cycle
    auto bf = [&](function<ll(int, int, int)> wt, vector<ll>& d) {
        // Bellman-Ford; every 20 passes the parent graph is checked for a cycle (a cycle there is
        // always negative), so a negative cycle is found fast. Returns true iff no negative cycle.
        d.assign(N, 0); vector<int> par(N, -1);
        for (int it = 0; it <= N; it++) {
            bool ch = false;
            for (int u = 0; u < N; u++) for (auto& a : adj[u]) { ll nd = d[u] + wt(u, a.first, a.second); if (nd < d[a.first]) { d[a.first] = nd; par[a.first] = u; ch = true; } }
            if (!ch) return true;
            if (it % 20 == 19) {
                vector<int> col(N, 0);
                for (int s0 = 0; s0 < N; s0++) if (!col[s0]) {
                    int u = s0; vector<int> path;
                    while (u >= 0 && !col[u]) { col[u] = 1; path.push_back(u); u = par[u]; }
                    if (u >= 0 && col[u] == 1) {
                        ll tot = 0; int v = u, len = 0;
                        do { int p = par[v]; int w = -1; for (auto& a : adj[p]) if (a.first == v) w = a.second; tot += wt(p, v, w); v = p; len++; } while (v != u);
                        printf("   negative cycle found: length %d, total weight %lld\n", len, tot);
                        return false;
                    }
                    for (int x : path) col[x] = 2;
                }
            }
        }
        return false;
    };
    // (A) mean weight per transition >= 1/4: weights 4w - 1 have no negative cycle
    vector<ll> d4;
    bool okA = bf([](int, int, int w) { return 4LL * w - 1; }, d4);
    printf("(A) 4w-1: %s, potential range [%lld, %lld]\n", okA ? "no negative cycle" : "NEGATIVE CYCLE", *min_element(d4.begin(), d4.end()), *max_element(d4.begin(), d4.end()));
    // tight arcs: reduced cost 4w-1 + d(u) - d(v) == 0
    vector<vector<int>> tight(N);
    long nt = 0;
    for (int u = 0; u < N; u++) for (auto& a : adj[u]) if (4LL * a.second - 1 + d4[u] - d4[a.first] == 0) { tight[u].push_back(a.first); nt++; }
    // cycles in the tight graph: SCCs (Tarjan, iterative)
    vector<int> idx(N, -1), low(N), comp(N, -1); vector<char> onst(N, 0); vector<int> stk; int ix = 0, nscc = 0;
    for (int s0 = 0; s0 < N; s0++) if (idx[s0] < 0) {
        vector<pair<int, int>> cs; cs.push_back({s0, 0}); idx[s0] = low[s0] = ix++; stk.push_back(s0); onst[s0] = 1;
        while (!cs.empty()) {
            int u = cs.back().first; int& i = cs.back().second;
            if (i < (int)tight[u].size()) {
                int v = tight[u][i++];
                if (idx[v] < 0) { idx[v] = low[v] = ix++; stk.push_back(v); onst[v] = 1; cs.push_back({v, 0}); }
                else if (onst[v]) low[u] = min(low[u], idx[v]);
            } else {
                if (low[u] == idx[u]) { while (true) { int v = stk.back(); stk.pop_back(); onst[v] = 0; comp[v] = nscc; if (v == u) break; } nscc++; }
                cs.pop_back(); if (!cs.empty()) low[cs.back().first] = min(low[cs.back().first], low[u]);
            }
        }
    }
    map<int, vector<int>> sccs; for (int u = 0; u < N; u++) sccs[comp[u]].push_back(u);
    vector<int> cyc; set<pair<int, int>> cycArcs;
    int ncyc = 0;
    for (auto& kv : sccs) {
        bool nontriv = kv.second.size() > 1;
        if (!nontriv) for (int v : tight[kv.second[0]]) if (v == kv.second[0]) nontriv = true;
        if (!nontriv) continue;
        ncyc++;
        printf("tight SCC %d: %zu states:", ncyc, kv.second.size());
        for (int u : kv.second) { printf(" %d", u); for (int v : tight[u]) if (comp[v] == kv.first) cycArcs.insert({u, v}); }
        printf("\n");
        for (int u : kv.second) { St s = dec(keys[u]); printf("   state %d x=%d pending:", u, s.x); for (auto& p : s.e) printf(" (%d,%d)-(%d,%d)c%d", p.lx, p.ly, p.ux, p.uy, p.comp); printf("\n"); }
    }
    printf("tight arcs %ld, cyclic tight components %d, cycle arcs %zu\n", nt, ncyc, cycArcs.size());
    // (R) row certificate: for each tight cycle, recover the neighbours of strip cells (0,0),(1,0)
    // over one row, and check the pending crossing pair at the start of the row.
    for (auto& kv : sccs) {
        if (kv.second.size() < 2) continue;
        int s0 = -1; for (int u : kv.second) if (dec(keys[u]).x == 0) s0 = u;
        // edges seen in the 4 states of the row (x=0..3) and the next row start, in row-0 coordinates
        set<array<int, 4>> E; int u = s0;
        for (int step = 0; step <= 4; step++) {
            St s = dec(keys[u]); int sh = step == 4 ? 1 : 0;   // after 4 steps y is shifted by one
            for (auto& p : s.e) E.insert({p.lx, p.ly + sh, p.ux, p.uy + sh});
            if (step < 4) { int nxt = -1; for (int v : tight[u]) if (comp[v] == kv.first) nxt = v; u = nxt; }
        }
        for (int cxl = 0; cxl < 2; cxl++) {
            printf("   SCC %d: neighbours of (%d,0):", kv.first, cxl);
            for (auto& e : E) { if (e[0] == cxl && e[1] == 0) printf(" (%d,%d)", e[2], e[3]); if (e[2] == cxl && e[3] == 0) printf(" (%d,%d)", e[0], e[1]); }
            printf("\n");
        }
        St st = dec(keys[s0]); int nx = 0;
        for (size_t i = 0; i < st.e.size(); i++) for (size_t j = i + 1; j < st.e.size(); j++) {
            auto& a = st.e[i]; auto& b = st.e[j];
            if (crossE(a.lx, a.ly, a.ux, a.uy, b.lx, b.ly, b.ux, b.uy)) { printf("   SCC %d row-start pending crossing: (%d,%d)-(%d,%d) x (%d,%d)-(%d,%d)\n", kv.first, a.lx, a.ly, a.ux, a.uy, b.lx, b.ly, b.ux, b.uy); nx++; }
        }
        printf("   SCC %d: %d crossing pair(s) among the pending edges at the row start\n", kv.first, nx);
    }
    // T*: longest path in the tight graph without cycle arcs (must be acyclic)
    {
        vector<int> indeg(N, 0); for (int u = 0; u < N; u++) for (int v : tight[u]) if (!cycArcs.count({u, v})) indeg[v]++;
        deque<int> qq; for (int u = 0; u < N; u++) if (!indeg[u]) qq.push_back(u);
        vector<int> L(N, 0); int seen = 0;
        while (!qq.empty()) { int u = qq.front(); qq.pop_front(); seen++; for (int v : tight[u]) if (!cycArcs.count({u, v})) { L[v] = max(L[v], L[u] + 1); if (!--indeg[v]) qq.push_back(v); } }
        printf("tight graph minus cycle arcs: %s, longest path %d\n", seen == N ? "acyclic" : "HAS CYCLES", *max_element(L.begin(), L.end()));
    }
    // (S) stability: 20w - 5 - 4[non-cycle arc] no negative cycle; potential range
    vector<ll> dS;
    bool okS = bf([&](int u, int v, int w) { return 20LL * w - 5 - (cycArcs.count({u, v}) ? 0 : 4); }, dS);
    printf("(S) 20w-5-4[nc]: %s, potential range [%lld, %lld]\n", okS ? "no negative cycle" : "NEGATIVE CYCLE", *min_element(dS.begin(), dS.end()), *max_element(dS.begin(), dS.end()));
    vector<ll> dT;
    bool okT = bf([&](int u, int v, int w) { return 1000LL * w - 250 - (cycArcs.count({u, v}) ? 0 : 201); }, dT);
    printf("(S') 1000w-250-201[nc]: %s\n", okT ? "no negative cycle" : "NEGATIVE CYCLE (expected)");
    return 0;
}
