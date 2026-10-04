// Generic frontier DP over an ordered cell list. Instance (stdin, text):
//   nbits  ncells  init_mask(hi lo)  bound
//   per cell: inmask(hi lo) rem nopt ; then nopt lines: inreq(hi lo) outadd(hi lo) cost
//   final: target mode (0 = print all final states <= bound, 1 = print cost of mask 0)
// Transition: (F & inmask) == inreq -> F' = (F & ~inmask) | outadd, cost += c. Prune cost + rem > bound.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;
struct H { size_t operator()(const u128& x) const { uint64_t a = (uint64_t)x, b = (uint64_t)(x >> 64); return a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL + (a << 6) + (a >> 2)); } };
static u128 rd() { unsigned long long hi, lo; if (scanf("%llu %llu", &hi, &lo) != 2) exit(2); return ((u128)hi << 64) | lo; }
int main(int argc, char** argv) {
    int nbits, ncells; u128 init; long long bound;
    if (scanf("%d %d", &nbits, &ncells) != 2) return 2; init = rd(); if (scanf("%lld", &bound) != 1) return 2;
    unordered_map<u128, int, H> cur, nxt; cur.reserve(1 << 20); cur[init] = 0;
    size_t peak = 1;
    for (int i = 0; i < ncells; i++) {
        u128 inmask = rd(); long long rem; int nopt; if (scanf("%lld %d", &rem, &nopt) != 2) return 2;
        vector<u128> req(nopt), add(nopt); vector<int> cost(nopt);
        for (int k = 0; k < nopt; k++) { req[k] = rd(); add[k] = rd(); if (scanf("%d", &cost[k]) != 1) return 2; }
        nxt.clear(); nxt.reserve(cur.size() * 2 + 16);
        for (auto& kv : cur) {
            if (kv.second + rem > bound) continue;
            u128 sel = kv.first & inmask, base = kv.first & ~inmask;
            for (int k = 0; k < nopt; k++) if (sel == req[k]) {
                u128 f2 = base | add[k]; int c = kv.second + cost[k];
                auto it = nxt.find(f2); if (it == nxt.end()) nxt.emplace(f2, c); else if (c < it->second) it->second = c;
            }
        }
        swap(cur, nxt); peak = max(peak, cur.size());
        fprintf(stderr, "cell %d states %zu\n", i, cur.size());
        if (cur.empty()) break;
    }
    int mode = argc > 1 ? atoi(argv[1]) : 1;
    fprintf(stderr, "peak %zu\n", peak);
    if (mode == 1) { auto it = cur.find((u128)0); if (it == cur.end()) printf("NONE\n"); else printf("%d\n", it->second); }
    else for (auto& kv : cur) if (kv.second <= bound) printf("%llu %llu %d\n", (unsigned long long)(kv.first >> 64), (unsigned long long)kv.first, kv.second);
    return 0;
}
