// corner_charge.cpp - independent check of the corner endpoint charge lemma
// (w-turnstheory/FINDINGS.md section 7.3), KT Edge Searcher, 2026-10-02. Own code, no solver.
//
// Statement checked: bottom-left corner, integer R. Q_R = directed dual path
//   (3/2,R+1/2) -> (1/2,R+1/2) -> (1/2,1/2) -> (R+1/2,1/2) -> (R+1/2,3/2), in unit steps.
// omega(s) = phi(s) - chi(b(s)), phi(s) = sum over tour edges properly crossing s of chi(end on the
// LEFT of s), b(s) = cell on the RIGHT of s next to its midpoint, chi = +1 iff x+y even.
// Hypothesis: every cell has degree 2; left strip cells (0,y),(1,y), R-1<=y<=R+2, have exactly the
// pattern edges of P (s=+1) or P' (s=-1): (0,y)~(2,y+s),(1,y+2s); (1,y)~(3,y+s),(0,y-2s);
// bottom strip cells (x,0),(x,1), R-1<=x<=R+2, the transposed pattern with its own sign.
// Claim: sum over s in Q_R of omega(s) = 1 (mod 3), for every corner completion.
//
// Method: sum omega is linear in the edge set. Every edge with a non-zero coefficient is classified:
//  (i)  incident to a "middle" boundary cell (0,y) or (y,0), 4<=y<=R-2: the program verifies that
//       EVERY knight edge at such a cell has coefficient -chi(cell); with degree 2 the cell gives
//       exactly -2 chi(cell), whatever its edges are;
//  (ii) incident to a pattern cell: fixed by the hypothesis;
//  (iii) incident to one of the 7 corner cells K = (0,0..3),(1..3,0): all choices of two on-board
//       neighbours per K cell with every K cell of degree exactly 2 are enumerated.
// The program aborts if an edge with a non-zero coefficient fits none of (i)-(iii), or fits (i) and
// another class.
#include <bits/stdc++.h>
using namespace std;
typedef array<int, 2> P2;
static int chi(P2 c) { return ((c[0] + c[1]) % 2 == 0) ? 1 : -1; }
static long long orient(long long ax, long long ay, long long bx, long long by, long long cx, long long cy) { long long v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax); return (v > 0) - (v < 0); }
const int MV[8][2] = {{1, 2}, {2, 1}, {2, -1}, {1, -2}, {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}};

int main() {
    bool allOK = true;
    for (int R : {12, 13, 14, 15}) for (int sA : {1, -1}) for (int sB : {1, -1}) {
        // dual path in doubled coordinates (dual points are odd)
        vector<P2> pts = {{3, 2 * R + 1}, {1, 2 * R + 1}};
        for (int y = 2 * R - 1; y >= 1; y -= 2) pts.push_back({1, y});
        for (int x = 3; x <= 2 * R + 1; x += 2) pts.push_back({x, 1});
        pts.push_back({2 * R + 1, 3});
        auto coeff = [&](P2 a, P2 b) {   // a,b cells
            long long ax = 2 * a[0], ay = 2 * a[1], bx = 2 * b[0], by = 2 * b[1]; int c = 0;
            for (size_t i = 0; i + 1 < pts.size(); i++) {
                auto p = pts[i], q = pts[i + 1];
                int o1 = orient(p[0], p[1], q[0], q[1], ax, ay), o2 = orient(p[0], p[1], q[0], q[1], bx, by);
                int o3 = orient(ax, ay, bx, by, p[0], p[1]), o4 = orient(ax, ay, bx, by, q[0], q[1]);
                if (o1 * o2 < 0 && o3 * o4 < 0) c += chi(o1 > 0 ? a : b);   // o1>0: a is on the left of p->q
            }
            return c;
        };
        int rightSum = 0;
        for (size_t i = 0; i + 1 < pts.size(); i++) {
            auto p = pts[i], q = pts[i + 1]; int dx = (q[0] - p[0]) / 2, dy = (q[1] - p[1]) / 2;
            // midpoint (doubled) + right normal (dy,-dx) -> cell centre (doubled), then halve
            int mx = (p[0] + q[0]) / 2 + dy, my = (p[1] + q[1]) / 2 - dx;
            rightSum += chi({mx / 2, my / 2});
        }
        auto onb = [&](P2 c) { return c[0] >= 0 && c[1] >= 0; };
        auto isMid = [&](P2 c) { return (c[0] == 0 && c[1] >= 4 && c[1] <= R - 2) || (c[1] == 0 && c[0] >= 4 && c[0] <= R - 2); };
        auto isPat = [&](P2 c) { return (c[0] <= 1 && c[1] >= R - 1 && c[1] <= R + 2) || (c[1] <= 1 && c[0] >= R - 1 && c[0] <= R + 2); };
        set<P2> K = {{0, 0}, {0, 1}, {0, 2}, {0, 3}, {1, 0}, {2, 0}, {3, 0}};
        // pattern neighbour lists
        map<P2, set<P2>> pat;
        for (int y = R - 1; y <= R + 2; y++) {
            pat[{0, y}] = {{2, y + sA}, {1, y + 2 * sA}}; pat[{1, y}] = {{3, y + sA}, {0, y - 2 * sA}};
            pat[{y, 0}] = {{y + sB, 2}, {y + 2 * sB, 1}}; pat[{y, 1}] = {{y + sB, 3}, {y - 2 * sB, 0}};
        }
        bool ok = true;
        // pattern consistency between two pattern cells
        for (auto& kv : pat) for (auto& v : kv.second) if (pat.count(v) && !pat[v].count(kv.first)) { ok = false; printf("pattern inconsistent at (%d,%d)-(%d,%d)\n", kv.first[0], kv.first[1], v[0], v[1]); }
        int midSum = 0, patSum = 0;
        int B = R + 8;
        set<pair<P2, P2>> patEdges;
        for (auto& kv : pat) for (auto& v : kv.second) { P2 a = kv.first, b = v; if (b < a) swap(a, b); patEdges.insert({a, b}); }
        // classify every on-board knight edge with a non-zero coefficient
        for (int x = 0; x <= B; x++) for (int y = 0; y <= B; y++) for (auto& m : MV) {
            P2 a = {x, y}, b = {x + m[0], y + m[1]};
            if (!onb(b) || b < a) continue;
            int c = coeff(a, b);
            bool mid = isMid(a) || isMid(b), pt = isPat(a) || isPat(b), kk = K.count(a) || K.count(b);
            if (mid) {
                P2 mc = isMid(a) ? a : b;
                if (c != -chi(mc) || kk) { ok = false; printf("middle edge (%d,%d)-(%d,%d) coeff %d pat %d K %d\n", a[0], a[1], b[0], b[1], c, pt, kk); }
                continue;
            }
            if (c == 0) continue;
            if (pt && kk) { ok = false; printf("edge in two classes\n"); }
            if (pt) { if (patEdges.count({a, b})) patSum += c; }
            else if (!kk) { ok = false; printf("unclassified edge (%d,%d)-(%d,%d) coeff %d\n", a[0], a[1], b[0], b[1], c); }
        }
        for (int y = 4; y <= R - 2; y++) midSum += -2 * chi({0, y}) - 2 * chi({y, 0});
        // pattern edges must be on board and must not touch K cells
        for (auto& e : patEdges) if (!onb(e.first) || K.count(e.first) || K.count(e.second)) ok = false;
        // enumerate K choices
        vector<P2> Kv(K.begin(), K.end());
        vector<vector<pair<P2, P2>>> opts(Kv.size());
        vector<vector<array<pair<P2, P2>, 2>>> pairsOf(Kv.size());
        for (size_t i = 0; i < Kv.size(); i++) {
            vector<P2> nb; for (auto& m : MV) { P2 b = {Kv[i][0] + m[0], Kv[i][1] + m[1]}; if (onb(b)) nb.push_back(b); }
            for (size_t p = 0; p < nb.size(); p++) for (size_t q = p + 1; q < nb.size(); q++) {
                auto e1 = make_pair(min(Kv[i], nb[p]), max(Kv[i], nb[p])), e2 = make_pair(min(Kv[i], nb[q]), max(Kv[i], nb[q]));
                pairsOf[i].push_back({e1, e2});
            }
        }
        long nOpt = 0; map<int, long> resid;
        vector<int> pick(Kv.size(), 0);
        function<void(size_t)> rec = [&](size_t i) {
            if (i == Kv.size()) {
                set<pair<P2, P2>> E; for (size_t j = 0; j < Kv.size(); j++) { E.insert(pairsOf[j][pick[j]][0]); E.insert(pairsOf[j][pick[j]][1]); }
                for (auto& k : Kv) { int d = 0; for (auto& e : E) d += (e.first == k) + (e.second == k); if (d != 2) return; }
                nOpt++;
                int kSum = 0;
                for (auto& e : E) { if (isMid(e.first) || isMid(e.second) || isPat(e.first) || isPat(e.second)) { ok = false; } kSum += coeff(e.first, e.second); }
                int Q = midSum + patSum + kSum - rightSum;
                resid[((Q % 3) + 3) % 3]++;
                return;
            }
            for (size_t p = 0; p < pairsOf[i].size(); p++) { pick[i] = p; rec(i + 1); }
        };
        rec(0);
        printf("R=%d left=%s bottom=%s: K options %ld, residues of sum omega:", R, sA > 0 ? "P" : "P'", sB > 0 ? "P" : "P'", nOpt);
        for (auto& kv : resid) printf(" %d:%ld", kv.first, kv.second);
        printf("  classification %s\n", ok ? "OK" : "FAILED");
        if (!ok || resid.size() != 1 || !resid.count(1)) allOK = false;
    }
    printf("%s\n", allOK ? "ALL PASS: sum omega = 1 mod 3 in every case" : "SOME CHECK FAILED");
    return 0;
}
