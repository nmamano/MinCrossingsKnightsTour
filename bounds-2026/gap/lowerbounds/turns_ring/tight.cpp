// Tight side paths: from each source state s, walk the arcs of the free strip graph with reduced cost
// S*c + h(u) - h(v) == 0 (h linear, WFILE as in stripz), layer by layer up to length LMAX.
// Stops when a layer (set of states at exact length L) repeats: then lengths are periodic from "pre" with period "per"
// (pre = per = -1: the walk set died out or LMAX was reached). Prints, for each source, the target states (from the targets file) reached and at which lengths.
// usage: WFILE=w.txt tight W pairs.txt LMAX      (pairs.txt lines: s t sigma_t, hex; sources = col 1, targets = col 3)
#include <bits/stdc++.h>
using namespace std;
#include "stripz_expand.inc"
int main(int argc, char** argv) {
    W = atoi(argv[1]); int LMAX = atoi(argv[3]); init_slots();
    FILE* f = fopen(getenv("WFILE"), "r"); long long SC, d; vector<long long> w; fscanf(f, "%lld", &SC); while (fscanf(f, "%lld", &d) == 1) w.push_back(d); fclose(f);
    auto h = [&](uint64_t s) { long long t = 0; for (size_t k = 0; k < slots.size(); k++) if (s >> k & 1) t += w[k]; return t; };
    ifstream in(argv[2]); string a, b, c; set<uint64_t> src; set<uint64_t> tgt;
    while (in >> a >> b >> c) { src.insert(stoull(a, 0, 16)); tgt.insert(stoull(c, 0, 16)); }
    unordered_map<uint64_t,int> best; long long hits = 0;
    for (uint64_t s : src) {
        unordered_set<uint64_t> cur{s}; map<uint64_t, vector<int>> hit; size_t maxlayer = 1;
        map<vector<uint64_t>, int> seenLayer; int pre = -1, per = -1;
        for (int L = 0; L <= LMAX && !cur.empty(); L++) {
            vector<uint64_t> key(cur.begin(), cur.end()); sort(key.begin(), key.end());
            auto it = seenLayer.find(key); if (it != seenLayer.end()) { pre = it->second; per = L - it->second; break; }
            seenLayer[key] = L;
            for (uint64_t u : cur) if (tgt.count(u)) hit[u].push_back(L);
            if (L == LMAX) break;
            unordered_set<uint64_t> nxt;
            for (uint64_t u : cur) { expand(u, best); long long hu = h(u);
                for (auto& kv : best) if (SC * kv.second + hu - h(kv.first) == 0) nxt.insert(kv.first); }
            cur.swap(nxt); maxlayer = max(maxlayer, cur.size());
            if (cur.size() > 3000000) { printf("source %llx: layer too big at L=%d\n", (unsigned long long)s, L); break; }
        }
        printf("source %llx maxlayer %zu pre %d per %d targets hit %zu", (unsigned long long)s, maxlayer, pre, per, hit.size());
        for (auto& kv : hit) { printf(" | %llx:", (unsigned long long)kv.first); for (int L : kv.second) printf(" %d", L); hits++; }
        printf("\n"); fflush(stdout);
    }
    printf("total source-target hits %lld\n", hits);
}
