// jbase.cpp - state count of a generic strip transfer graph (KT Edge Searcher, 2026-10-03).
// Columns 0..NC-1, scan order (row, column). DEG string: per column 'E' (degree exactly 2) or 'L' (<= 2).
// PAIRS: list of allowed column pairs "ab" (a<=b), e.g. "01,02,12,13,23,34,35".
// No cycle. Only counts states/arcs (no weights). usage: jbase DEG PAIRS [cap]
#include <bits/stdc++.h>
using namespace std;
const int UPX[4] = {2, -2, 1, -1}, UPY[4] = {1, 1, 2, 2};
int NC; string DEG; bool AL[8][8]; bool SLAB = false;   // SLAB: path labels only on S edges (an end in col 0/1)
static bool isS(int a, int b) { return a < 2 || b < 2; }
struct PE { int lx, ly, ux, uy, comp; };
static bool operator<(const PE& a, const PE& b) { return tie(a.lx, a.ly, a.ux, a.uy) < tie(b.lx, b.ly, b.ux, b.uy); }
struct St { int x; vector<PE> e; };
static string enc(const St& s) { string k; k.push_back((char)s.x); for (auto& p : s.e) { k.push_back((char)(p.lx * 3 + p.ly + 2)); k.push_back((char)(p.ux * 3 + p.uy)); k.push_back((char)p.comp); } return k; }
static St dec(const string& k) { St s; s.x = k[0]; for (size_t i = 1; i < k.size(); i += 3) { int a = k[i], b = k[i + 1]; s.e.push_back({a / 3, a % 3 - 2, b / 3, b % 3, k[i + 2]}); } return s; }
int main(int argc, char** argv) {
    DEG = argv[1]; NC = DEG.size(); string pairs = argv[2]; long cap = argc > 3 ? atol(argv[3]) : 100000000; SLAB = argc > 4 && string(argv[4]) == "slab";
    for (size_t i = 0; i + 1 < pairs.size(); i += 3) { int a = pairs[i] - '0', b = pairs[i + 1] - '0'; AL[a][b] = AL[b][a] = true; }
    unordered_map<string, int> id; vector<string> keys; long arcs = 0; size_t maxpend = 0;
    auto get = [&](const St& s) { string k = enc(s); auto it = id.find(k); if (it != id.end()) return it->second; int n = keys.size(); id[k] = n; keys.push_back(k); return n; };
    St st0; st0.x = 0; get(st0);
    for (size_t q = 0; q < keys.size(); q++) {
        if ((long)keys.size() > cap) { printf("CAP reached at %zu states (processed %zu)\n", keys.size(), q); return 0; }
        St s = dec(keys[q]); int x = s.x; maxpend = max(maxpend, s.e.size());
        vector<PE> in, rest;
        for (auto& p : s.e) (p.ux == x && p.uy == 0 ? in : rest).push_back(p);
        vector<array<int, 4>> cand;
        for (int m = 0; m < 4; m++) { int tx = x + UPX[m]; if (tx >= 0 && tx < NC && AL[x][tx]) cand.push_back({x, 0, tx, UPY[m]}); }
        int din = in.size(); if (din > 2) continue;
        vector<PE> inS; for (auto& p : in) if (!SLAB || isS(p.lx, p.ux)) inS.push_back(p);
        if (inS.size() == 2 && inS[0].comp == inS[1].comp) continue;
        vector<int> need; if (DEG[x] == 'E') need = {2 - din}; else for (int r = 0; r <= 2 - din; r++) need.push_back(r);
        set<int> outs; int nc = cand.size();
        for (int r : need) for (int msk = 0; msk < (1 << nc); msk++) {
            if (__builtin_popcount(msk) != r) continue;
            vector<array<int, 4>> ch; for (int i = 0; i < nc; i++) if (msk >> i & 1) ch.push_back(cand[i]);
            map<pair<int, int>, int> td; bool ok = true;
            for (auto& p : rest) td[{p.ux, p.uy}]++;
            for (auto& f : ch) if (++td[{f[2], f[3]}] > 2) ok = false;
            if (!ok) continue;
            const int NEW = 100, NOL = 99; int label = inS.size() ? inS[0].comp : NEW, merge = inS.size() == 2 ? inS[1].comp : -1;
            vector<PE> ne;
            for (auto p : rest) { if (merge >= 0 && p.comp == merge) p.comp = label; ne.push_back(p); }
            for (auto& f : ch) ne.push_back({f[0], f[1], f[2], f[3], (!SLAB || isS(f[0], f[2])) ? label : NOL});
            int nx = x + 1, sh = 0; if (nx == NC) { nx = 0; sh = 1; }
            for (auto& p : ne) { p.ly -= sh; p.uy -= sh; }
            sort(ne.begin(), ne.end());
            map<int, int> rl; for (auto& p : ne) { if (p.comp == NOL) { p.comp = 63; continue; } if (!rl.count(p.comp)) { int v = rl.size(); rl[p.comp] = v; } p.comp = rl[p.comp]; }
            St t; t.x = nx; t.e = ne; outs.insert(get(t));
        }
        arcs += outs.size();
    }
    printf("DEG %s PAIRS %s: states %zu arcs %ld max pending %zu\n", DEG.c_str(), pairs.c_str(), keys.size(), arcs, maxpend);
}
