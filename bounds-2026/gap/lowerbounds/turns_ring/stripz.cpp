// Like stripw.cpp (free side strip of width W), plus:
//   writes <prefix>_zcls.txt : one line per zero-cost recurrent class: "size period mask mask ..." (hex cut states)
//   writes <prefix>_zarcs.txt: zero arcs inside recurrent classes "u v" (hex)
//   if env WFILE=<file> ("S w_0 ... w_{K-1}", integers, slot order): streams all arcs and reports the min reduced
//   cost S*c + h(u) - h(v), h(s) = sum_k w_k [slot k in s] (exact integers), writes up to 2000 most violated arcs.
// usage: stripz W prefix
#include <bits/stdc++.h>
using namespace std;
int W; struct E { int x0, y0, x1, y1; };
vector<E> slots; map<array<int,4>, int> slotid;
static const int MV[8][2] = {{1,2},{2,1},{2,-1},{1,-2},{-1,-2},{-2,-1},{-2,1},{-1,2}};
int lowerL(int x, int d1, int d2) {
    if (x == 0) return 1;
    if (x == 1 || x == 2) return ((x + d1 == 0 || x + d1 == 3) + (x + d2 == 0 || x + d2 == 3)) - 1;
    if (x == 3) return 1 - ((x + d1 == 1 || x + d1 == 2) + (x + d2 == 1 || x + d2 == 2));
    return 0;
}
// successors of state s: map next-state -> min row cost
void expand(uint64_t s, unordered_map<uint64_t,int>& best) {
    best.clear();
    vector<vector<int>> inc(W); uint64_t keepMask = 0; int load1[64] = {0};
    for (size_t k = 0; k < slots.size(); k++) if (s >> k & 1) {
        auto& e = slots[k];
        if (e.y1 == 0) { int dx = e.x0 - e.x1, dy = e.y0 - e.y1; int mi = -1; for (int q = 0; q < 8; q++) if (MV[q][0] == dx && MV[q][1] == dy) mi = q; inc[e.x1].push_back(mi); }
        else { keepMask |= 1ULL << k; load1[e.x1]++; }
    }
    for (int x = 0; x < W; x++) if (inc[x].size() > 2) return;
    struct Opt { int cost; int nn; int tx[2], ty[2]; uint64_t bits; };
    vector<vector<Opt>> opts(W);
    for (int x = 0; x < W; x++) {
        vector<int> cand;
        for (int q = 0; q < 8; q++) {
            int x1 = x + MV[q][0], y1 = MV[q][1];
            if (x1 < 0) continue;
            if (find(inc[x].begin(), inc[x].end(), q) != inc[x].end()) continue;
            if (x1 >= W) { cand.push_back(q); continue; }
            if (y1 > 0) cand.push_back(q);
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
            o.bits = 0; for (int k = 0; k < o.nn; k++) o.bits |= 1ULL << slotid.at({x, -1, o.tx[k], o.ty[k] - 1});
            opts[x].push_back(o);
        };
        if (need == 0) mk(inc[x]);
        else if (need == 1) for (int q : cand) { vector<int> mv = inc[x]; mv.push_back(q); mk(mv); }
        else for (size_t i = 0; i < cand.size(); i++) for (size_t j = i + 1; j < cand.size(); j++) mk({cand[i], cand[j]});
    }
    function<void(int, int, uint64_t, vector<int>&, vector<int>&)> rec = [&](int x, int cost, uint64_t nm, vector<int>& l1, vector<int>& l2) {
        if (x == W) { auto it = best.find(nm); if (it == best.end() || cost < it->second) best[nm] = cost; return; }
        for (auto& o : opts[x]) {
            bool ok = true;
            for (int k = 0; k < o.nn; k++) { int& L = (o.ty[k] == 1 ? l1 : l2)[o.tx[k]]; if (L + 1 > 2) ok = false; }
            if (!ok) continue;
            uint64_t m2 = nm | o.bits;
            for (int k = 0; k < o.nn; k++) (o.ty[k] == 1 ? l1 : l2)[o.tx[k]]++;
            rec(x + 1, cost + o.cost, m2, l1, l2);
            for (int k = 0; k < o.nn; k++) (o.ty[k] == 1 ? l1 : l2)[o.tx[k]]--;
        }
    };
    uint64_t base = 0;
    for (size_t k = 0; k < slots.size(); k++) if (keepMask >> k & 1) { auto& e = slots[k]; base |= 1ULL << slotid.at({e.x0, -2, e.x1, 0}); }
    vector<int> l1(W, 0), l2(W, 0);
    for (int x = 0; x < W; x++) l1[x] = load1[x];
    rec(0, 0, base, l1, l2);
}
int main(int argc, char** argv) {
    W = atoi(argv[1]); string pre = argv[2];
    for (int y0 = -2; y0 <= -1; y0++) for (int x0 = 0; x0 < W; x0++) for (auto& m : MV) {
        int x1 = x0 + m[0], y1 = y0 + m[1];
        if (m[1] > 0 && x1 >= 0 && x1 < W && y1 >= 0) { slotid[{x0, y0, x1, y1}] = slots.size(); slots.push_back({x0, y0, x1, y1}); }
    }
    { FILE* f = fopen((pre + "_slots.txt").c_str(), "w"); for (auto& e : slots) fprintf(f, "%d %d %d %d\n", e.x0, e.y0, e.x1, e.y1); fclose(f); }
    vector<long long> w; long long SC = 1; const char* wf = getenv("WFILE");
    if (wf) { FILE* f = fopen(wf, "r"); long long d; if (fscanf(f, "%lld", &SC) != 1) return 1; while (fscanf(f, "%lld", &d) == 1) w.push_back(d); fclose(f); if (w.size() != slots.size() && w.size() != 2 * slots.size()) { fprintf(stderr, "bad w size\n"); return 1; } }
    const bool PAR = w.size() == 2 * slots.size();   // parity mode: h0 = w[0..K), h1 = w[K..2K)
    auto hp = [&](uint64_t s, int p) { long long t = 0; size_t K = slots.size(); for (size_t k = 0; k < K; k++) if (s >> k & 1) t += w[p * K + k]; return t; };
    auto h = [&](uint64_t s) { return hp(s, 0); };
    if (getenv("STATES")) {   // fast parallel check mode: states from a previous run, no BFS, no classes
        if (!wf) return 1;
        FILE* f = fopen(getenv("STATES"), "rb"); vector<uint64_t> st; uint64_t x; while (fread(&x, 8, 1, f) == 1) st.push_back(x); fclose(f);
        long long minred = LLONG_MAX, nviol = 0; vector<tuple<long long,uint64_t,uint64_t,int>> viol;
        #pragma omp parallel
        {
            unordered_map<uint64_t,int> b; long long mr = LLONG_MAX, nv = 0; vector<tuple<long long,uint64_t,uint64_t,int>> vl;
            #pragma omp for schedule(dynamic, 4096)
            for (size_t i = 0; i < st.size(); i++) {
                expand(st[i], b);
                for (int p = 0; p < (PAR ? 2 : 1); p++) { long long hs = hp(st[i], p);
                for (auto& kv : b) { long long red = SC * kv.second + hs - hp(kv.first, PAR ? 1 - p : 0); mr = min(mr, red);
                    if (red < 0) { nv++; vl.push_back({red, st[i], kv.first, kv.second + 1000 * p}); if (vl.size() > 200000) { sort(vl.begin(), vl.end()); vl.resize(20000); } } } }
            }
            #pragma omp critical
            { minred = min(minred, mr); nviol += nv; viol.insert(viol.end(), vl.begin(), vl.end()); }
        }
        sort(viol.begin(), viol.end()); if (viol.size() > 20000) viol.resize(20000);
        printf("W %d states %zu\nscale %lld min reduced cost %lld violated arcs %lld\n", W, st.size(), SC, minred, nviol);
        FILE* g = fopen((pre + "_viol.txt").c_str(), "w"); for (auto& t : viol) fprintf(g, "%llx %llx %d %lld\n", (unsigned long long)get<1>(t), (unsigned long long)get<2>(t), get<3>(t), get<0>(t)); fclose(g);
        return 0;
    }
    unordered_map<uint64_t, int> id; vector<uint64_t> st; id[0] = 0; st.push_back(0);
    vector<array<int,2>> zarcs; unordered_map<uint64_t,int> best;
    long long minred = LLONG_MAX; vector<tuple<long long,uint64_t,uint64_t,int>> viol; long long nviol = 0;
    for (size_t si = 0; si < st.size(); si++) {
        uint64_t s = st[si]; expand(s, best); long long hs = wf ? h(s) : 0;
        for (auto& kv : best) {
            auto it = id.find(kv.first); int v;
            if (it == id.end()) { v = st.size(); id[kv.first] = v; st.push_back(kv.first); } else v = it->second;
            if (kv.second == 0) zarcs.push_back({(int)si, v});
            if (wf) { long long red = SC * kv.second + hs - h(kv.first); minred = min(minred, red);
                if (red < 0) { nviol++; viol.push_back({red, s, kv.first, kv.second}); if (viol.size() > 200000) { sort(viol.begin(), viol.end()); viol.resize(20000); } } }
        }
        if (si % 2000000 == 0) fprintf(stderr, "expanded %zu states %zu\n", si, st.size());
    }
    int N = st.size(); printf("W %d states %d zero arcs %zu\n", W, N, zarcs.size());
    { FILE* f = fopen((pre + "_states.bin").c_str(), "wb"); fwrite(st.data(), 8, N, f); fclose(f); }
    if (wf) { sort(viol.begin(), viol.end()); if (viol.size() > 20000) viol.resize(20000);
        printf("scale %lld min reduced cost %lld violated arcs %lld\n", SC, minred, nviol);
        FILE* f = fopen((pre + "_viol.txt").c_str(), "w"); for (auto& t : viol) fprintf(f, "%llx %llx %d %lld\n", (unsigned long long)get<1>(t), (unsigned long long)get<2>(t), get<3>(t), get<0>(t)); fclose(f); }
    vector<vector<int>> zadj(N); for (auto& a : zarcs) zadj[a[0]].push_back(a[1]);
    vector<int> idx(N, -1), low(N), comp(N, -1); vector<char> on(N, 0); vector<int> stk; int cnt = 0, nc = 0;
    for (int s0 = 0; s0 < N; s0++) if (idx[s0] < 0) {
        vector<pair<int,int>> cs; cs.push_back({s0, 0}); idx[s0] = low[s0] = cnt++; stk.push_back(s0); on[s0] = 1;
        while (!cs.empty()) {
            int v = cs.back().first; int& i = cs.back().second;
            if (i < (int)zadj[v].size()) { int w2 = zadj[v][i++]; if (idx[w2] < 0) { idx[w2] = low[w2] = cnt++; stk.push_back(w2); on[w2] = 1; cs.push_back({w2, 0}); } else if (on[w2]) low[v] = min(low[v], idx[w2]); }
            else { if (low[v] == idx[v]) { while (true) { int x = stk.back(); stk.pop_back(); on[x] = 0; comp[x] = nc; if (x == v) break; } nc++; }
                   cs.pop_back(); if (!cs.empty()) low[cs.back().first] = min(low[cs.back().first], low[v]); }
        }
    }
    vector<int> csize(nc, 0); for (int v = 0; v < N; v++) csize[comp[v]]++;
    vector<int> selfloop(nc, 0); for (auto& a : zarcs) if (a[0] == a[1]) selfloop[comp[a[0]]] = 1;
    vector<int> lev(N, -1); vector<long long> per(nc, 0); vector<vector<int>> members(nc);
    for (int v = 0; v < N; v++) { int c = comp[v]; if (csize[c] > 1 || selfloop[c]) members[c].push_back(v); }
    for (int v = 0; v < N; v++) { int c = comp[v]; if ((csize[c] > 1 || selfloop[c]) && lev[v] < 0) {
        deque<int> q; q.push_back(v); lev[v] = 0;
        while (!q.empty()) { int x = q.front(); q.pop_front(); for (int y : zadj[x]) if (comp[y] == c) { if (lev[y] < 0) { lev[y] = lev[x] + 1; q.push_back(y); } else per[c] = __gcd(per[c], (long long)abs(lev[x] + 1 - lev[y])); } }
    } }
    FILE* f = fopen((pre + "_zcls.txt").c_str(), "w"); FILE* g = fopen((pre + "_zarcs.txt").c_str(), "w"); int ncls = 0;
    for (int c = 0; c < nc; c++) if (!members[c].empty()) { ncls++;
        fprintf(f, "%zu %lld", members[c].size(), per[c]); for (int v : members[c]) fprintf(f, " %llx", (unsigned long long)st[v]); fprintf(f, "\n");
        for (int v : members[c]) for (int y : zadj[v]) if (comp[y] == c) fprintf(g, "%llx %llx\n", (unsigned long long)st[v], (unsigned long long)st[y]); }
    fclose(f); fclose(g); printf("zero recurrent classes %d\n", ncls);
    return 0;
}
