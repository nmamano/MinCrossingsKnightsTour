// Free side strip of width W (columns 0..W-1, side at x=0; moves into x>=W are free), row-level transfer graph on
// cut states (bitmask of in-strip edges crossing the row cut). Row cost = sum of r = t - L_x over the W cells.
// Prints sizes, zero-cost recurrent classes (size, period), Bellman-Ford potential range (min cycle mean 0).
// usage: stripw W [out_prefix]     (writes <prefix>_arcs.bin: int32 triples u v cost, if a prefix is given)
#include <bits/stdc++.h>
using namespace std;
int W; bool ZEROONLY = false; long long nposarcs = 0;
struct E { int x0, y0, x1, y1; };
vector<E> slots; map<array<int,4>, int> slotid;
static const int MV[8][2] = {{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};
int lowerL(int x, int d1, int d2) {
    if (x == 0) return 1;
    if (x == 1 || x == 2) return ((x + d1 == 0 || x + d1 == 3) + (x + d2 == 0 || x + d2 == 3)) - 1;
    if (x == 3) return 1 - ((x + d1 == 1 || x + d1 == 2) + (x + d2 == 1 || x + d2 == 2));
    return 0;
}
int main(int argc, char** argv) {
    W = atoi(argv[1]); ZEROONLY = getenv("ZEROONLY") != nullptr;
    for (int y0 = -2; y0 <= -1; y0++) for (int x0 = 0; x0 < W; x0++) for (auto& m : MV) {
        int x1 = x0 + m[0], y1 = y0 + m[1];
        if (m[1] > 0 && x1 >= 0 && x1 < W && y1 >= 0) { slotid[{x0, y0, x1, y1}] = slots.size(); slots.push_back({x0, y0, x1, y1}); }
    }
    if (slots.size() > 64) { fprintf(stderr, "too many slots %zu\n", slots.size()); return 1; }
    fprintf(stderr, "slots %zu\n", slots.size());
    unordered_map<uint64_t, int> id; vector<uint64_t> st; id[0] = 0; st.push_back(0);
    vector<array<int,3>> arcs;
    for (size_t si = 0; si < st.size(); si++) {
        uint64_t s = st[si];
        // incoming moves per cell in row 0 (as move from the cell), kept edges (target row 1)
        vector<vector<int>> inc(W); vector<int> keepTo; uint64_t keepMask = 0; bool bad = false;
        int load1[64] = {0};
        for (size_t k = 0; k < slots.size(); k++) if (s >> k & 1) {
            auto& e = slots[k];
            if (e.y1 == 0) { int dx = e.x0 - e.x1, dy = e.y0 - e.y1; int mi = -1; for (int q = 0; q < 8; q++) if (MV[q][0] == dx && MV[q][1] == dy) mi = q; inc[e.x1].push_back(mi); }
            else { keepMask |= 1ULL << k; load1[e.x1]++; }
        }
        for (int x = 0; x < W; x++) if (inc[x].size() > 2) bad = true;
        if (bad) continue;
        // per cell option lists: (move a, move b, cost, list of new in-strip edges as (x1, y1))
        struct Opt { int cost; int nn; int tx[2], ty[2]; };
        vector<vector<Opt>> opts(W);
        for (int x = 0; x < W; x++) {
            vector<int> cand;
            for (int q = 0; q < 8; q++) {
                int x1 = x + MV[q][0], y1 = MV[q][1];
                if (x1 < 0) continue;
                bool isInc = find(inc[x].begin(), inc[x].end(), q) != inc[x].end();
                if (isInc) continue;
                if (x1 >= W) { cand.push_back(q); continue; }        // free zone, any dy
                if (y1 > 0) cand.push_back(q);                       // later strip rows
            }
            int need = 2 - (int)inc[x].size();
            auto mk = [&](vector<int> mv) {
                Opt o; int a = mv[0], b = mv[1];
                int t = (MV[a][0] + MV[b][0] != 0 || MV[a][1] + MV[b][1] != 0);
                o.cost = t - lowerL(x, MV[a][0], MV[b][0]); o.nn = 0;
                for (int q : mv) {
                    bool isInc = find(inc[x].begin(), inc[x].end(), q) != inc[x].end();
                    int x1 = x + MV[q][0];
                    if (!isInc && x1 < W) { o.tx[o.nn] = x1; o.ty[o.nn] = MV[q][1]; o.nn++; }
                }
                opts[x].push_back(o);
            };
            if (need == 0) mk(inc[x]);
            else if (need == 1) for (int q : cand) { vector<int> mv = inc[x]; mv.push_back(q); mk(mv); }
            else for (size_t i = 0; i < cand.size(); i++) for (size_t j = i + 1; j < cand.size(); j++) mk({cand[i], cand[j]});
        }
        // enumerate combinations with load checks
        unordered_map<uint64_t, int> best;
        vector<int> choice(W);
        function<void(int, int, uint64_t, vector<int>&, vector<int>&)> rec = [&](int x, int cost, uint64_t nm, vector<int>& l1, vector<int>& l2) {
            if (x == W) {
                // next state: kept edges (row -1 -> 1) shift to (-2 -> 0); new edges (0 -> 1|2) shift to (-1 -> 0|1)
                auto it = best.find(nm); if (it == best.end() || cost < it->second) best[nm] = cost; return;
            }
            for (auto& o : opts[x]) {
                bool ok = true;
                for (int k = 0; k < o.nn; k++) { int& L = (o.ty[k] == 1 ? l1 : l2)[o.tx[k]]; if (L + 1 > 2) ok = false; }
                if (!ok) continue;
                uint64_t m2 = nm;
                for (int k = 0; k < o.nn; k++) { (o.ty[k] == 1 ? l1 : l2)[o.tx[k]]++; m2 |= 1ULL << slotid[{x, -1, o.tx[k], o.ty[k] - 1}]; }
                rec(x + 1, cost + o.cost, m2, l1, l2);
                for (int k = 0; k < o.nn; k++) (o.ty[k] == 1 ? l1 : l2)[o.tx[k]]--;
            }
        };
        uint64_t base = 0;
        for (size_t k = 0; k < slots.size(); k++) if (keepMask >> k & 1) { auto& e = slots[k]; base |= 1ULL << slotid[{e.x0, -2, e.x1, 0}]; }
        vector<int> l1(W, 0), l2(W, 0);
        for (int x = 0; x < W; x++) l1[x] = load1[x];
        rec(0, 0, base, l1, l2);
        for (auto& kv : best) {
            auto it = id.find(kv.first); int v;
            if (it == id.end()) { v = st.size(); id[kv.first] = v; st.push_back(kv.first); } else v = it->second;
            if (!ZEROONLY || kv.second == 0) arcs.push_back({(int)si, v, kv.second}); else nposarcs++;
        }
        if (si % 200000 == 0) fprintf(stderr, "expanded %zu states %zu arcs %zu\n", si, st.size(), arcs.size());
    }
    int N = st.size(); printf("W %d states %d stored arcs %zu (positive arcs not stored %lld)\n", W, N, arcs.size(), nposarcs);
    int mn = INT_MAX; for (auto& a : arcs) mn = min(mn, a[2]); printf("min arc cost %d\n", mn);
    // zero classes: Tarjan on zero arcs (iterative)
    vector<vector<int>> zadj(N); for (auto& a : arcs) if (a[2] == 0) zadj[a[0]].push_back(a[1]);
    vector<int> idx(N, -1), low(N), comp(N, -1); vector<char> on(N, 0); vector<int> stk; int cnt = 0, nc = 0;
    for (int s0 = 0; s0 < N; s0++) if (idx[s0] < 0) {
        vector<pair<int,int>> cs; cs.push_back({s0, 0}); idx[s0] = low[s0] = cnt++; stk.push_back(s0); on[s0] = 1;
        while (!cs.empty()) {
            int v = cs.back().first; int& i = cs.back().second;
            if (i < (int)zadj[v].size()) { int w = zadj[v][i++]; if (idx[w] < 0) { idx[w] = low[w] = cnt++; stk.push_back(w); on[w] = 1; cs.push_back({w, 0}); } else if (on[w]) low[v] = min(low[v], idx[w]); }
            else { if (low[v] == idx[v]) { while (true) { int w = stk.back(); stk.pop_back(); on[w] = 0; comp[w] = nc; if (w == v) break; } nc++; }
                   cs.pop_back(); if (!cs.empty()) low[cs.back().first] = min(low[cs.back().first], low[v]); }
        }
    }
    vector<int> csize(nc, 0); for (int v = 0; v < N; v++) csize[comp[v]]++;
    vector<int> selfloop(nc, 0); for (auto& a : arcs) if (a[2] == 0 && a[0] == a[1]) selfloop[comp[a[0]]] = 1;
    // periods via BFS levels inside each recurrent class
    vector<int> lev(N, -1); vector<long long> per(nc, 0);
    for (int v = 0; v < N; v++) { int c = comp[v]; if ((csize[c] > 1 || selfloop[c]) && lev[v] < 0) {
        deque<int> q; q.push_back(v); lev[v] = 0;
        while (!q.empty()) { int x = q.front(); q.pop_front(); for (int w : zadj[x]) if (comp[w] == c) { if (lev[w] < 0) { lev[w] = lev[x] + 1; q.push_back(w); } else per[c] = __gcd(per[c], (long long)abs(lev[x] + 1 - lev[w])); } }
    } }
    vector<pair<int,int>> cls; for (int c = 0; c < nc; c++) if (csize[c] > 1 || selfloop[c]) cls.push_back({csize[c], (int)per[c]});
    sort(cls.rbegin(), cls.rend());
    printf("zero recurrent classes %zu:", cls.size()); for (size_t i = 0; i < min<size_t>(cls.size(), 20); i++) printf(" (%d,p%d)", cls[i].first, cls[i].second); printf("\n");
    // Bellman-Ford potential from all-zero (cost >= 0 so it converges; range shows transition costs)
    if (argc > 2) { FILE* f = fopen((string(argv[2]) + "_arcs.bin").c_str(), "wb"); for (auto& a : arcs) fwrite(a.data(), 4, 3, f); fclose(f);
        f = fopen((string(argv[2]) + "_states.bin").c_str(), "wb"); fwrite(st.data(), 8, N, f); fclose(f); }
    return 0;
}
