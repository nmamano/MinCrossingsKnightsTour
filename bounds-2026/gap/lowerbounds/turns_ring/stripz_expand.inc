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
void init_slots() {
    for (int y0 = -2; y0 <= -1; y0++) for (int x0 = 0; x0 < W; x0++) for (auto& m : MV) {
        int x1 = x0 + m[0], y1 = y0 + m[1];
        if (m[1] > 0 && x1 >= 0 && x1 < W && y1 >= 0) { slotid[{x0, y0, x1, y1}] = slots.size(); slots.push_back({x0, y0, x1, y1}); }
    }
}
