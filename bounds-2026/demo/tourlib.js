// Tour decoding and independent checks, shared by the page (window.KT) and check.js (node).
(function (root) {
  'use strict';
  const ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
  const MI = [-2, -1, 1, 2, 2, 1, -1, -2], MJ = [1, 2, 2, 1, -1, -2, -2, -1];
  const DIRV = [[2, 1], [1, 2], [2, -1], [1, -2]];   // same order as DIRS in app.js
  // ---------- data ----------
  function decode(rec) {
    const n = rec.n, N = n * n, A = new Int8Array(N), B = new Int8Array(N);
    for (let c = 0; c < N; c++) { const v = ALPHA.indexOf(rec.cells[c]); A[c] = v >> 3; B[c] = v & 7; }
    return { n, A, B, rec };
  }

  // independent check in the browser: two reciprocal knight moves per square, one closed cycle
  function analyse(t) {
    const { n, A, B } = t, N = n * n;
    const nb = (c, k) => { const i = (c / n) | 0, j = c % n, a = i + MI[k], b = j + MJ[k];
      return (a < 0 || b < 0 || a >= n || b >= n) ? -1 : a * n + b; };
    let ok = true;
    const nbr = new Int32Array(2 * N);
    for (let c = 0; c < N && ok; c++) {
      if (A[c] === B[c]) ok = false;
      for (const [s, k] of [[0, A[c]], [1, B[c]]]) {
        const d = nb(c, k);
        if (d < 0 || (nb(d, A[d]) !== c && nb(d, B[d]) !== c)) ok = false;
        nbr[2 * c + s] = d;
      }
    }
    if (ok) {   // walk the cycle
      let prev = -1, cur = 0, steps = 0;
      do { const nx = nbr[2 * cur] !== prev ? nbr[2 * cur] : nbr[2 * cur + 1]; prev = cur; cur = nx; steps++; }
      while (cur !== 0 && steps <= N);
      ok = steps === N;
    }
    // edges (each once), in (x, y-down) = (column, row) board units, cell centre at +0.5
    const E = [];   // [x1, y1, x2, y2, dir]
    for (let c = 0; c < N; c++) for (const d of [nbr[2 * c], nbr[2 * c + 1]]) if (d > c) {
      const x1 = c % n, y1 = (c / n) | 0, x2 = d % n, y2 = (d / n) | 0;
      let dx = x2 - x1, dy = y1 - y2; if (dx < 0) { dx = -dx; dy = -dy; }
      E.push([x1, y1, x2, y2, DIRV.findIndex((q) => q[0] === dx && q[1] === dy)]);
    }
    // crossings: proper intersection of open segments, among edges whose first ends are near
    const bucket = new Map();
    E.forEach((e, id) => { const k = e[1] * n + e[0]; if (!bucket.has(k)) bucket.set(k, []); bucket.get(k).push(id); });
    const orient = (ax, ay, bx, by, cx, cy) => Math.sign((bx - ax) * (cy - ay) - (by - ay) * (cx - ax));
    const X = [];
    E.forEach((e, id) => {
      const [x1, y1, x2, y2] = e;
      for (let dy = -3; dy <= 3; dy++) for (let dx = -3; dx <= 3; dx++) {
        const L = bucket.get((y1 + dy) * n + (x1 + dx)); if (!L || x1 + dx < 0 || x1 + dx >= n) continue;
        for (const fid of L) {
          if (fid <= id) continue;
          const [u1, v1, u2, v2] = E[fid];
          const o1 = orient(x1, y1, x2, y2, u1, v1), o2 = orient(x1, y1, x2, y2, u2, v2);
          const o3 = orient(u1, v1, u2, v2, x1, y1), o4 = orient(u1, v1, u2, v2, x2, y2);
          if (o1 * o2 < 0 && o3 * o4 < 0) {
            const rx = x2 - x1, ry = y2 - y1, sx = u2 - u1, sy = v2 - v1;
            const tt = ((u1 - x1) * sy - (v1 - y1) * sx) / (rx * sy - ry * sx);
            X.push([x1 + tt * rx, y1 + tt * ry]);
          }
        }
      }
    });
    const T = [];
    for (let c = 0; c < N; c++) if (Math.abs(A[c] - B[c]) !== 4) T.push(c);
    return { ok, E, X, T };
  }

  const KT = { decode, analyse };
  if (typeof module !== 'undefined') module.exports = KT; else root.KT = KT;
})(this);
