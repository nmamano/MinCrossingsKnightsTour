// certify.cpp - independent exhaustive check for finite crossing-free window lemmas
// (KT Edge Searcher, 2026-10-02). No solver: a column sweep (transfer matrix) over ALL edge subsets.
//
// Input (text):
//   NC                      number of cells
//   x y req                 req 2 = degree exactly 2, req 1 = degree at most 2   (NC lines)
//   NE                      number of candidate edges
//   u v flags w             cell indices, flags: 1 forced, 2 forbidden, 4 exempt (may cross anything),
//                           w = integer flux weight (sum over chosen edges is the flux)   (NE lines)
// Rules: every chosen edge set must meet the degree rules; two chosen edges must not cross
// properly, unless both are forced or at least one is exempt.
// Output: every reachable flux value
// (as a set) and the max number of frontier states.
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

struct Key { u64 a, b; bool operator==(const Key& o) const { return a == o.a && b == o.b; } };
struct KH { size_t operator()(const Key& k) const { return k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL + (k.a << 6)); } };
const int FR = 64, FOFF = 32;   // flux range -32..31
typedef u64 Vals;   // bit t = flux value t - FOFF reachable

int NC, NE;
vector<int> cx, cy, req;
vector<int> eu, ev, ef, ew;     // eu = left endpoint (smaller x)
vector<vector<int>> crossList;  // non-exempt crossing partners

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: certify input.txt\n"); return 1; }
    FILE* f = fopen(argv[1], "r");
    if (fscanf(f, "%d", &NC) != 1) return 1;
    cx.resize(NC); cy.resize(NC); req.resize(NC);
    for (int i = 0; i < NC; i++) if (fscanf(f, "%d %d %d", &cx[i], &cy[i], &req[i]) != 3) return 1;
    if (fscanf(f, "%d", &NE) != 1) return 1;
    eu.resize(NE); ev.resize(NE); ef.resize(NE); ew.resize(NE);
    for (int i = 0; i < NE; i++) {
        int u, v; if (fscanf(f, "%d %d %d %d", &u, &v, &ef[i], &ew[i]) != 4) return 1;
        if (cx[u] > cx[v]) swap(u, v);
        if (cx[u] == cx[v]) { fprintf(stderr, "vertical edge not supported\n"); return 1; }
        eu[i] = u; ev[i] = v;
    }
    fclose(f);
    // forbidden edges are dropped
    vector<int> live; for (int i = 0; i < NE; i++) if (!(ef[i] & 2)) live.push_back(i);
    // crossing lists (only x-overlapping pairs can cross)
    crossList.assign(NE, {});
    long ncross = 0;
    for (int a = 0; a < (int)live.size(); a++) for (int b = a + 1; b < (int)live.size(); b++) {
        int e = live[a], g = live[b];
        if (max(cx[eu[e]], cx[eu[g]]) >= min(cx[ev[e]], cx[ev[g]])) continue;
        if ((ef[e] & 1) && (ef[g] & 1)) continue;
        if ((ef[e] & 4) || (ef[g] & 4)) continue;
        if (properCross(cx[eu[e]], cy[eu[e]], cx[ev[e]], cy[ev[e]], cx[eu[g]], cy[eu[g]], cx[ev[g]], cy[ev[g]])) {
            crossList[e].push_back(g); crossList[g].push_back(e); ncross++;
        }
    }
    // columns
    int xmin = *min_element(cx.begin(), cx.end()), xmax = *max_element(cx.begin(), cx.end());
    int NX = xmax - xmin + 1;
    vector<vector<int>> colCells(NX);
    for (int i = 0; i < NC; i++) colCells[cx[i] - xmin].push_back(i);
    for (auto& v : colCells) sort(v.begin(), v.end(), [&](int a, int b) { return cy[a] < cy[b]; });
    vector<vector<int>> fwd(NC);
    for (int e : live) fwd[eu[e]].push_back(e);
    // pending edges at cut c (before processing column index c): left < c <= right
    vector<vector<int>> pend(NX + 1);
    vector<unordered_map<int, int>> pos(NX + 1);
    for (int c = 0; c <= NX; c++) {
        for (int e : live) { int l = cx[eu[e]] - xmin, r = cx[ev[e]] - xmin; if (l < c && c <= r) pend[c].push_back(e); }
        if (pend[c].size() > 128) { fprintf(stderr, "frontier too wide\n"); return 1; }
        for (int i = 0; i < (int)pend[c].size(); i++) pos[c][pend[c][i]] = i;
    }
    auto getBit = [](const Key& k, int i) { return i < 64 ? (k.a >> i & 1) : (k.b >> (i - 64) & 1); };
    auto setBit = [](Key& k, int i) { if (i < 64) k.a |= 1ULL << i; else k.b |= 1ULL << (i - 64); };
    unordered_map<Key, Vals, KH> cur, nxt;
    cur[{0, 0}] = 1ULL << FOFF;
    size_t maxStates = 1;
    vector<char> chosen(NE, 0);
    vector<int> deg(NC, 0);
    fprintf(stderr, "cells=%d edges=%zu crossing pairs=%ld columns=%d\n", NC, live.size(), ncross, NX);
    for (int c = 0; c < NX; c++) {
        nxt.clear();
        const vector<int>& cells = colCells[c];
        for (auto& kv : cur) {
            const Key& k = kv.first;
            // mark pending edges as chosen, compute incoming degrees
            vector<int> on;
            for (int i = 0; i < (int)pend[c].size(); i++) if (getBit(k, i)) { int e = pend[c][i]; on.push_back(e); chosen[e] = 1; deg[ev[e]]++; }
            // DFS over cells of column c
            vector<int> newE;
            function<void(int, int)> dfs = [&](int ci, int flux) {
                if (ci == (int)cells.size()) {
                    Key nk{0, 0};
                    for (int e : on) if (cx[ev[e]] - xmin > c) setBit(nk, pos[c + 1].at(e));
                    for (int e : newE) setBit(nk, pos[c + 1].at(e));
                    Vals& dst = nxt.try_emplace(nk, 0).first->second;
                    Vals src = kv.second;
                    if (flux > 0) { if (src >> (FR - flux)) { fprintf(stderr, "flux range\n"); exit(1); } dst |= src << flux; }
                    else if (flux < 0) { if (src & ((1ULL << -flux) - 1)) { fprintf(stderr, "flux range\n"); exit(1); } dst |= src >> -flux; }
                    else dst |= src;
                    return;
                }
                int u = cells[ci];
                const vector<int>& F = fwd[u];
                int nf = F.size();
                for (int m = 0; m < (1 << nf); m++) {
                    int cntm = __builtin_popcount(m);
                    bool ok = true;
                    for (int j = 0; j < nf && ok; j++) if ((ef[F[j]] & 1) && !(m >> j & 1)) ok = false;
                    if (!ok) continue;
                    int d = deg[u] + cntm;
                    if (req[u] == 2 ? d != 2 : d > 2) continue;
                    // capacity of targets + crossings
                    for (int j = 0; j < nf && ok; j++) if (m >> j & 1) {
                        int e = F[j]; if (deg[ev[e]] + 1 > 2) { ok = false; break; }
                        for (int g : crossList[e]) if (chosen[g]) { ok = false; break; }
                        if (!ok) break;
                        chosen[e] = 1; deg[ev[e]]++; deg[u]++;   // tentatively add (undo below)
                    }
                    // undo partial adds if failed
                    if (!ok) {
                        for (int j = 0; j < nf; j++) if ((m >> j & 1) && chosen[F[j]]) { chosen[F[j]] = 0; deg[ev[F[j]]]--; deg[u]--; }
                        continue;
                    }
                    int fl = 0; size_t sz = newE.size();
                    for (int j = 0; j < nf; j++) if (m >> j & 1) { newE.push_back(F[j]); fl += ew[F[j]]; }
                    dfs(ci + 1, flux + fl);
                    newE.resize(sz);
                    for (int j = 0; j < nf; j++) if (m >> j & 1) { chosen[F[j]] = 0; deg[ev[F[j]]]--; deg[u]--; }
                }
            };
            dfs(0, 0);
            for (int e : on) { chosen[e] = 0; deg[ev[e]]--; }
        }
        swap(cur, nxt);
        maxStates = max(maxStates, cur.size());
        fprintf(stderr, "  column %d: states %zu\n", c + xmin, cur.size());
        if (cur.empty()) break;
    }
    Vals tot = 0;
    for (auto& kv : cur) tot |= kv.second;
    printf("{\"maxStates\":%zu,\"feasible\":{", maxStates);
    bool first = true;
    for (int t = 0; t < FR; t++) if (tot >> t & 1) { printf("%s\"%d\":1", first ? "" : ",", t - FOFF); first = false; }
    printf("}}\n");
    return 0;
}
