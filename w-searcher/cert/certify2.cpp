// certify2.cpp - independent exhaustive check for finite crossing-free window lemmas, version 2
// (KT Edge Searcher, 2026-10-02). No solver: a column sweep over ALL edge subsets.
//
// Same input as certify.cpp:
//   NC / (x y req)*NC / NE / (u v flags w)*NE
//   req 2 = degree exactly 2, req 1 = degree at most 2
//   flags: 1 forced, 2 forbidden, 4 exempt (may cross anything); w = flux weight
// Rules: degree rules; two chosen edges must not cross properly unless both forced or one exempt.
// Output: the set of reachable flux values (sum of w over chosen edges).
//
// Difference to certify.cpp: an edge is DECIDED at the column of its "owner" endpoint: the
// endpoint with req 2 if exactly one endpoint has req 2 (frame cells never decide), else the left
// endpoint. Columns are swept left to right; at column c all edges owned by column c are decided
// edge by edge (DFS with pruning). The frontier state at cut c keeps exactly the decided edges that
// (a) may still cross an undecided edge, or (b) touch a cell that still has undecided edges.
// This keeps the frontier small next to frame columns (frame cells have degree <= 2 only).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned long long u64;

static int orient(ll px, ll py, ll qx, ll qy, ll rx, ll ry) {
    ll v = (qx - px) * (ry - py) - (qy - py) * (rx - px);
    return v > 0 ? 1 : (v < 0 ? -1 : 0);
}
static bool properCross(ll ax, ll ay, ll bx, ll by, ll cx, ll cy, ll dx, ll dy) {
    int d1 = orient(ax, ay, bx, by, cx, cy), d2 = orient(ax, ay, bx, by, dx, dy);
    int d3 = orient(cx, cy, dx, dy, ax, ay), d4 = orient(cx, cy, dx, dy, bx, by);
    return d1 * d2 < 0 && d3 * d4 < 0;
}
const int KW = 4;   // key words: up to 256 frontier edges
struct Key { u64 w[KW]; bool operator==(const Key& o) const { for (int i = 0; i < KW; i++) if (w[i] != o.w[i]) return false; return true; } };
struct KH { size_t operator()(const Key& k) const { u64 h = 1469598103934665603ULL; for (int i = 0; i < KW; i++) { h ^= k.w[i]; h *= 1099511628211ULL; h ^= h >> 31; } return h; } };
const int FR = 64, FOFF = 32;

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: certify2 input.txt\n"); return 1; }
    FILE* f = fopen(argv[1], "r");
    int NC, NE;
    if (fscanf(f, "%d", &NC) != 1) return 1;
    vector<int> cx(NC), cy(NC), req(NC);
    for (int i = 0; i < NC; i++) if (fscanf(f, "%d %d %d", &cx[i], &cy[i], &req[i]) != 3) return 1;
    if (fscanf(f, "%d", &NE) != 1) return 1;
    vector<int> eu, ev, ef, ew;
    for (int i = 0; i < NE; i++) {
        int u, v, fl, w; if (fscanf(f, "%d %d %d %d", &u, &v, &fl, &w) != 4) return 1;
        if (fl & 2) continue;                       // forbidden: drop
        eu.push_back(u); ev.push_back(v); ef.push_back(fl); ew.push_back(w);
    }
    fclose(f);
    NE = eu.size();
    int xmin = *min_element(cx.begin(), cx.end()), xmax = *max_element(cx.begin(), cx.end());
    int NX = xmax - xmin + 1;
    // owner column of each edge
    vector<int> dc(NE);
    for (int e = 0; e < NE; e++) {
        int u = eu[e], v = ev[e], o;
        if (req[u] == 2 && req[v] != 2) o = u; else if (req[v] == 2 && req[u] != 2) o = v; else o = cx[u] <= cx[v] ? u : v;
        dc[e] = cx[o] - xmin;
    }
    // crossing lists
    vector<vector<int>> X(NE);
    long ncr = 0;
    for (int a = 0; a < NE; a++) for (int b = a + 1; b < NE; b++) {
        if ((ef[a] & 1) && (ef[b] & 1)) continue;
        if ((ef[a] & 4) || (ef[b] & 4)) continue;
        if (max(min(cx[eu[a]], cx[ev[a]]), min(cx[eu[b]], cx[ev[b]])) >= min(max(cx[eu[a]], cx[ev[a]]), max(cx[eu[b]], cx[ev[b]]))) continue;
        if (properCross(cx[eu[a]], cy[eu[a]], cx[ev[a]], cy[ev[a]], cx[eu[b]], cy[eu[b]], cx[ev[b]], cy[ev[b]])) { X[a].push_back(b); X[b].push_back(a); ncr++; }
    }
    // per cell: incident edges, last decision column
    vector<vector<int>> inc(NC);
    for (int e = 0; e < NE; e++) { inc[eu[e]].push_back(e); inc[ev[e]].push_back(e); }
    vector<int> lastDc(NC, -1);
    for (int c = 0; c < NC; c++) for (int e : inc[c]) lastDc[c] = max(lastDc[c], dc[e]);
    // cells with req 2 but no edges -> infeasible immediately
    for (int c = 0; c < NC; c++) if (req[c] == 2 && inc[c].size() < 2) { printf("{\"maxStates\":0,\"feasible\":{}}\n"); return 0; }
    // keep[c] = edges kept in the state at cut c (decided at < c, still relevant at >= c)
    vector<vector<int>> keep(NX + 1);
    vector<unordered_map<int, int>> pos(NX + 1);
    for (int c = 0; c <= NX; c++) {
        for (int e = 0; e < NE; e++) {
            if (dc[e] >= c) continue;
            bool k = lastDc[eu[e]] >= c || lastDc[ev[e]] >= c;
            if (!k) for (int g : X[e]) if (dc[g] >= c) { k = true; break; }
            if (k) keep[c].push_back(e);
        }
        if (keep[c].size() > 64 * KW) { fprintf(stderr, "frontier too wide (%zu)\n", keep[c].size()); return 1; }
        for (int i = 0; i < (int)keep[c].size(); i++) pos[c][keep[c][i]] = i;
    }
    vector<vector<int>> owned(NX);
    for (int e = 0; e < NE; e++) owned[dc[e]].push_back(e);
    // order owned edges by owner cell then y, so that cells complete early
    for (int c = 0; c < NX; c++) sort(owned[c].begin(), owned[c].end(), [&](int a, int b) {
        auto key = [&](int e) { int u = cx[eu[e]] - xmin == c ? eu[e] : ev[e]; return make_pair(cy[u], e); };
        return key(a) < key(b); });
    // within column c, the last owned edge index touching each cell (for exact-degree checks)
    unordered_map<Key, u64, KH> cur, nxt;
    Key z; memset(&z, 0, sizeof z); cur[z] = 1ULL << FOFF;
    size_t maxStates = 1;
    vector<char> on(NE, 0);
    vector<int> deg(NC, 0);
    fprintf(stderr, "cells=%d edges=%d crossing pairs=%ld columns=%d\n", NC, NE, ncr, NX);
    for (int c = 0; c < NX; c++) {
        nxt.clear();
        const vector<int>& O = owned[c];
        int no = O.size();
        // lastIdx[cell] = last position in O touching the cell, if the cell completes in this column
        unordered_map<int, int> lastIdx;
        for (int i = 0; i < no; i++) for (int u : {eu[O[i]], ev[O[i]]}) if (lastDc[u] == c) lastIdx[u] = i;
        // cells that complete in this column without any owned edge here are checked at the start
        vector<int> doneHere;
        for (int u = 0; u < NC; u++) if (lastDc[u] == c && !lastIdx.count(u)) doneHere.push_back(u);
        for (auto& kv : cur) {
            const Key& k = kv.first;
            vector<int> st;
            for (int i = 0; i < (int)keep[c].size(); i++) if (k.w[i >> 6] >> (i & 63) & 1) { int e = keep[c][i]; st.push_back(e); on[e] = 1; deg[eu[e]]++; deg[ev[e]]++; }
            bool okStart = true;
            for (int u : doneHere) if (req[u] == 2 && deg[u] != 2) okStart = false;
            if (okStart) {
                function<void(int, int)> dfs = [&](int i, int flux) {
                    if (i == no) {
                        Key nk; memset(&nk, 0, sizeof nk);
                        for (int e : st) { auto it = pos[c + 1].find(e); if (it != pos[c + 1].end()) nk.w[it->second >> 6] |= 1ULL << (it->second & 63); }
                        for (int j = 0; j < no; j++) if (on[O[j]]) { auto it = pos[c + 1].find(O[j]); if (it != pos[c + 1].end()) nk.w[it->second >> 6] |= 1ULL << (it->second & 63); }
                        u64 src = kv.second, add;
                        if (flux > 0) { if (src >> (FR - flux)) { fprintf(stderr, "flux range\n"); exit(1); } add = src << flux; }
                        else if (flux < 0) { if (src & ((1ULL << -flux) - 1)) { fprintf(stderr, "flux range\n"); exit(1); } add = src >> -flux; }
                        else add = src;
                        nxt[nk] |= add;
                        return;
                    }
                    int e = O[i], u = eu[e], v = ev[e];
                    auto completeOK = [&]() {
                        for (int w : {u, v}) { auto it = lastIdx.find(w); if (it != lastIdx.end() && it->second == i && req[w] == 2 && deg[w] != 2) return false; }
                        return true;
                    };
                    // skip e
                    if (!(ef[e] & 1) && completeOK()) dfs(i + 1, flux);
                    // take e
                    if (deg[u] < 2 && deg[v] < 2) {
                        bool ok = true;
                        for (int g : X[e]) if (on[g]) { ok = false; break; }
                        if (ok) {
                            on[e] = 1; deg[u]++; deg[v]++;
                            if (completeOK()) dfs(i + 1, flux + ew[e]);
                            on[e] = 0; deg[u]--; deg[v]--;
                        }
                    }
                };
                dfs(0, 0);
            }
            for (int e : st) { on[e] = 0; deg[eu[e]]--; deg[ev[e]]--; }
        }
        swap(cur, nxt);
        maxStates = max(maxStates, cur.size());
        fprintf(stderr, "  column %d: states %zu (frontier edges %zu)\n", c + xmin, cur.size(), keep[c + 1].size());
        if (cur.empty()) break;
    }
    u64 tot = 0; for (auto& kv : cur) tot |= kv.second;
    printf("{\"maxStates\":%zu,\"feasible\":{", maxStates);
    bool first = true;
    for (int t = 0; t < FR; t++) if (tot >> t & 1) { printf("%s\"%d\":1", first ? "" : ",", t - FOFF); first = false; }
    printf("}}\n");
    return 0;
}
