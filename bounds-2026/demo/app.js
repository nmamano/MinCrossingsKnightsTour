// Knight's tour constructions demo (KT Integrator, Research Lab, 2026-10-02). No build step.
(function () {
  'use strict';
  // 4 undirected directions in (x right, y up), dx > 0. Palette validated (CVD, all pairs).
  const DIRS = [
    { v: [2, 1], col: '#2a78d6', name: 'right 2, up 1' },
    { v: [1, 2], col: '#1baf7a', name: 'right 1, up 2' },
    { v: [2, -1], col: '#eda100', name: 'right 2, down 1' },
    { v: [1, -2], col: '#4a3aa7', name: 'right 1, down 2' },
  ];
  const PLAIN = '#7b8a97', RED = '#d03b3b', TURN = '#2b2b29', ACCENT = '#0b7a75';

  // Every step of the progression. period = step in n of the reuse argument (used for exact slopes).
  // band data drive the layout overlay of the lane designs.
  const LANE = { bandB: 4, bandL: 2 };
  const C = {
    orig: Object.assign({ name: 'Original formation heel', credit: 'Besa, Johnson, Mamano, Osegueda', date: '2019 (arXiv 1904.02824)',
      nmin: 48, period: 8, audit: 'Original formation construction from the paper. Claim 22 independently checks its strip counts and samples of this rebuild; the browser checks every displayed tour.',
      caption: {
        X: 'The first construction (Algorithm 1). Four knights move as a 2&times;2 formation along parallel diagonal lines and turn around at the top and bottom edges with an 8-column <b>heel</b>. ' +
          'Each heel has 32 crossings, and each 4-row side piece has 10: 2&middot;(32/8 + 10/4)&middot;n = <b>13n</b>.',
        T: 'The first construction (Algorithm 1). Every edge square must turn. The formation heel has 22 turns per 8 columns on the top and bottom edges, and the side pieces 2 per row: ' +
          '2&middot;(22/8 + 2)&middot;n = <b>9.5n</b>.' } }, LANE),
    paper: Object.assign({ name: 'Parker Williams heel (crossings)', credit: 'Parker Williams, in the paper', date: 'January 2022',
      nmin: 48, period: 8, audit: 'Paper Figure 11, right: 28 crossings and 22 turns per heel. Claims 21 and 22 check the counts; Claim 22 also matches the PDF move paths. Two small corner cases use the original heel.',
      caption: { X: 'Same layout, a better heel. Parker Williams\'s heel leaves the formation for a few moves and reaches the same exits with <b>28</b> crossings instead of 32: ' +
        '2&middot;(28/8 + 10/4)&middot;n = <b>12n</b>.' } }, LANE),
    heel21: Object.assign({ name: 'Parker Williams turn bound (reconstructed heel)', credit: 'Parker Williams, in the paper', date: 'January 2022',
      nmin: 48, period: 8, audit: 'Reconstruction by constrained search, reported OPTIMAL. Claim 22 independently confirms 21 turns, 31 crossings, and the paper\'s endpoint pairing. Its moves differ from Figure 11\'s centre panel. Two small corner cases use the original heel.',
      caption: { T: 'Same layout, a heel with <b>21</b> turns per 8 columns, one fewer than the formation heel, with the same exits: ' +
        '2&middot;(21/8 + 2)&middot;n = <b>9.25n</b>.' } }, LANE),
    P40: Object.assign({ name: 'Shisheng Li 4&times;40 block', credit: 'Shisheng Li', date: 'May 2026',
      nmin: 48, period: 40, audit: 'Shisheng Li\'s 4x40 block: Claim 22 independently checks 130 crossings and the pairing of five paper heels, plus full-tour samples. The demo uses the block on both horizontal bands where it fits.',
      caption: { X: 'Shisheng Li replaced five heels (40 columns) with one 4&times;40 block that keeps the same exits and path pairs. ' +
        'The block has <b>130</b> crossings, not 5&middot;28 = 140: 2&middot;(130/40 + 10/4)&middot;n = <b>11.5n</b>. A small board may have no room for a full block; at n=48 this step is the paper tour.' } }, LANE),
    H16a: Object.assign({ name: 'H16a heel', credit: 'Agent Team', date: 'October 1, 2026',
      nmin: 48, period: 24, audit: 'Audited: KT Verifier Claims 1, 4, 7 (all even n &ge; 48).',
      caption: { X: 'We use a heel whose strand order differs within each paired lane group, then join the paths with searched 6x6 corner pieces. ' +
        'The search then finds the heel <b>H16a</b> with 16 crossings per 8 columns: 2&middot;(16/8 + 10/4)&middot;n = <b>9n</b>.' } }, LANE),
    LF4: Object.assign({ name: 'Lane-free LF4', credit: 'Agent Team', date: 'October 1, 2026',
      nmin: 96, period: 48, audit: 'Audited: KT Verifier Claim 8 (all even n &ge; 96).',
      caption: { X: 'No formation lanes at all. Each edge gets its own periodic piece, found by search, and the corners join them into one tour. ' +
        'Crossings per unit of edge: 11/6 bottom, 37/16 top, 2 left, 1 right. Total <b>343n/48 &asymp; 7.15n</b>.' } }, LANE),
    FOLD: { name: 'Fold design', credit: 'Agent Team', date: 'October 1, 2026', nmin: 96, period: 24,
      audit: 'Audited: KT Verifier Claim 12 (all even n &ge; 96).',
      caption: { X: 'Two diagonal folds and two centre lines divide the unmodified field into eight triangles of parallel moves. ' +
        'Boundary U-turns and arch flips contribute 5n+O(1) crossings. Cheap endpoint patterns force a mod-three corner charge; diagonal corridors contribute 4n/3+O(1). ' +
        'The completed tours have at most 19n/3+142 crossings for every even n>=96.' } },
    T18: Object.assign({ name: 'T18 heel', credit: 'Agent Team', date: 'October 1, 2026',
      nmin: 48, period: 24, audit: 'Audited: KT Verifier Claims 3, 4 (lane rule, all even n &ge; 48).',
      caption: { T: 'We let the four knights come back in any order inside their lane pairs and fix the order in the corners. ' +
        'The search then finds the heel <b>T18</b> with 18 turns per 8 columns: 2&middot;(18/8 + 2)&middot;n = <b>8.5n</b>.' } }, LANE),
    TT16: Object.assign({ name: 'TT16', credit: 'Agent Team', date: 'October 1, 2026',
      nmin: 48, period: 8, audit: 'Audited: KT Verifier Claims 6, 7 (all even n &ge; 48).',
      caption: { T: 'New pieces on all four edges. <b>T16</b> makes 16 turns per 8 columns on the top and bottom, and new side pieces (2 turns per row) fit its line pairing: ' +
        '<b>8n &minus; 14</b>. Our lower bound is 8n &minus; 28, so the leading term 8n is exact.' } }, LANE),
  };
  const STEPS = { X: ['orig', 'paper', 'P40', 'H16a', 'LF4', 'FOLD'], T: ['orig', 'heel21', 'T18', 'TT16'] };
  const STEPNOTE = { X: '', T: 'Shisheng Li\'s block targets crossings only, so it is not a step here.' };
  const KNOWN = { X: { orig: [13, 1], paper: [12, 1], P40: [23, 2], H16a: [9, 1], LF4: [343, 48], FOLD: [19, 3] },
    T: { orig: [19, 2], heel21: [37, 4], T18: [17, 2], TT16: [8, 1] } };
  const LOWER = { X: [{ name: '4n: the paper\'s lower bound', f: (n) => 4 * n }, { name: '5n: new lower bound, Oct 3', f: (n) => 5 * n }],
    T: [{ name: '6n: the paper\'s lower bound on turns', f: (n) => 6 * n }, { name: '8n − 28: new lower bound', f: (n) => 8 * n - 28 }] };
  // Smallest n shown when a step is selected (P40: at n = 48 no 4x40 block fits, so 50), and the n rules per step.
  const NSTART = { P40: 50 };
  const ALG1 = 'For n ≡ 2 (mod 4) and n ≡ 6 (mod 8), one corner piece uses the original heel.';
  const NRULE = {
    orig: 'The demo builds it with Algorithm 1 of the paper at every even n shown.',
    paper: 'The demo builds it with Algorithm 1 at every even n shown. ' + ALG1,
    heel21: 'The demo builds it with Algorithm 1 at every even n shown. ' + ALG1,
    P40: 'The demo builds it with Algorithm 1 at every even n shown; 4×40 blocks are placed where they fit. At n = 48 no block fits, so the tour is the same as step 2 there. ' + ALG1,
    H16a: 'Proved for every even n ≥ 48 (one base board per residue of n mod 24, then insertion).',
    LF4: 'Proved for every even n ≥ 96 (one base board per residue of n mod 48, then insertion).',
    FOLD: 'Proved for every even n ≥ 96 (one base board per residue of n mod 24, then insertion).',
    T18: 'Proved for every even n ≥ 48 (one base board per residue of n mod 24, then insertion).',
    TT16: 'Proved for every even n ≥ 48 (base boards per residue of n mod 8, then insertion).',
  };
  const FIELD = { X: 'crossings', T: 'turns' };
  const NMAX = 200;

  const $ = (id) => document.getElementById(id);
  const canvas = $('board'), ctx = canvas.getContext('2d');
  const state = { metric: 'X', key: 'FOLD', n: 120, tour: null, view: null, summary: null };
  const cache = new Map();

  const { decode, analyse } = KT;

  async function getTour(key, n) {
    const id = key + n;
    if (!cache.has(id)) {
      cache.set(id, fetch(`data/${key}_n${n}.json`).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then((rec) => { const t = decode(rec); Object.assign(t, analyse(t)); t.solver = new Set(rec.solver); return t; }));
    }
    return cache.get(id);
  }

  // ---------- formulas ----------
  const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
  function slopeOf(key, m) {   // exact slope from n -> n + period over all n of the summary; null if not one value
    const rows = state.summary[key], P = C[key].period, seen = new Set(), f = FIELD[m];
    for (const s in rows) { const n = +s; if (rows[n + P]) seen.add(rows[n + P][f] - rows[n][f]); }
    if (seen.size !== 1) return null;
    const d = [...seen][0], g = gcd(d, P);
    return [d / g, P / g];
  }
  function fmtSlope([a, b]) { return b === 1 ? `${a}n` : (b === 2 || b === 4) ? `${a / b}n` : `${a}n/${b}`; }
  function fmtConst(v, b) {   // v = exact constant; b = its denominator. Prints a reduced fraction.
    const num = Math.round(v * b), sign = num < 0 ? '−' : '+';
    const q = Math.abs(num), g = gcd(q, b), a = q / g, d = b / g;
    return `${sign} ${d === 1 ? a : `${a}/${d}`}`;
  }

  // ---------- drawing ----------
  function resize() {
    const r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    draw();
  }
  function setView(name) {
    const n = state.n, W = canvas.width || 1, H = canvas.height || 1, m = Math.min(W, H);
    const [x0, y0, x1, y1, anchorBottom] = {
      fit: [-1, -1, n + 1, n + 1, false],
      edge: [-1, n - 14, 41, n + 1, true],       // a stretch of the bottom edge, from the left corner
      corner: [-1, n - 25, 24, n + 1, true],     // bottom-left corner
      centre: [n / 2 - 14, n / 2 - 14, n / 2 + 14, n / 2 + 14, false],
    }[name];
    const s = Math.max((x1 - x0) * m / W, (y1 - y0) * m / H), vw = s * W / m, vh = s * H / m;
    state.view = { x0: name === 'fit' || name === 'centre' ? (x0 + x1 - vw) / 2 : x0,
      y0: anchorBottom ? y1 - vh : (y0 + y1 - vh) / 2, s };
    draw();
  }
  const unit = () => Math.min(canvas.width, canvas.height) / state.view.s;   // device px per board unit
  function draw() {
    const t = state.tour; const W = canvas.width, H = canvas.height;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H);
    if (!t || !state.view) return;
    const n = t.n, v = state.view, k = unit();
    ctx.setTransform(k, 0, 0, k, -v.x0 * k, -v.y0 * k);   // now in board units
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, n, n);
    if ($('tChecker').checked && k / (window.devicePixelRatio || 1) >= 6) {   // faint checkerboard, a1 = bottom-left dark
      ctx.fillStyle = 'rgba(40,48,58,0.045)';
      for (let r = 0; r < n; r++) for (let x = (n - 1 - r) % 2; x < n; x += 2) ctx.fillRect(x, r, 1, 1);
    }
    if ($('tLayout').checked) drawLayout(n);
    if ($('tSolver').checked) {
      ctx.fillStyle = 'rgba(60,60,58,0.16)';
      for (const c of t.solver) ctx.fillRect(c % n, (c / n) | 0, 1, 1);
    }
    if (k > 9) {   // light grid when zoomed in
      ctx.strokeStyle = 'rgba(0,0,0,0.06)'; ctx.lineWidth = 1 / k; ctx.beginPath();
      for (let i = 0; i <= n; i++) { ctx.moveTo(0, i); ctx.lineTo(n, i); ctx.moveTo(i, 0); ctx.lineTo(i, n); }
      ctx.stroke();
    }
    ctx.strokeStyle = '#c9c8c2'; ctx.lineWidth = 1.5 / k; ctx.strokeRect(0, 0, n, n);
    // moves
    const colored = $('tColor').checked;
    const lw = Math.max(0.6, Math.min(2.2, k * 0.09)) / k;
    ctx.lineWidth = lw; ctx.lineCap = 'round';
    for (let d = 0; d < 4; d++) {
      ctx.strokeStyle = colored ? DIRS[d].col : PLAIN; ctx.globalAlpha = colored ? 0.9 : 0.75;
      ctx.beginPath();
      for (const e of t.E) if (e[4] === d) { ctx.moveTo(e[0] + .5, e[1] + .5); ctx.lineTo(e[2] + .5, e[3] + .5); }
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
    if ($('tTurns').checked) {
      const r = Math.max(1.2, Math.min(4, k * 0.14)) / k;
      ctx.fillStyle = TURN; ctx.beginPath();
      for (const c of t.T) { const x = c % n + .5, y = ((c / n) | 0) + .5; ctx.moveTo(x + r, y); ctx.arc(x, y, r, 0, 7); }
      ctx.fill();
    }
    if ($('tCross').checked) {
      const r = Math.max(1.6, Math.min(5, k * 0.16)) / k;
      ctx.beginPath();
      for (const [x, y] of t.X) { ctx.moveTo(x + .5 + r, y + .5); ctx.arc(x + .5, y + .5, r, 0, 7); }
      ctx.fillStyle = RED; ctx.fill();
      if (k > 6) { ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1 / k; ctx.stroke(); }
    }
  }
  function drawLayout(n) {
    const spec = C[state.key];
    if (state.key === 'FOLD') {
      // 8 triangles: tint each by the direction of its moves in the base tour (majority)
      const h = n / 2, tri = [
        [[0, 0], [h, h], [0, h]], [[0, 0], [h, h], [h, 0]], [[n, 0], [h, h], [h, 0]], [[n, 0], [h, h], [n, h]],
        [[n, n], [h, h], [n, h]], [[n, n], [h, h], [h, n]], [[0, n], [h, h], [h, n]], [[0, n], [h, h], [0, h]]];
      const dirOf = majorityDirs(n, tri);
      tri.forEach((p, i) => {
        ctx.fillStyle = hexA(DIRS[dirOf[i]].col, 0.08);
        ctx.beginPath(); ctx.moveTo(...p[0]); ctx.lineTo(...p[1]); ctx.lineTo(...p[2]); ctx.closePath(); ctx.fill();
      });
      ctx.strokeStyle = 'rgba(40,40,40,0.35)'; const u = 1 / unit(); ctx.lineWidth = 1.2 * u; ctx.setLineDash([4 * u, 3 * u]);
      ctx.beginPath(); ctx.moveTo(h, 0); ctx.lineTo(h, n); ctx.moveTo(0, h); ctx.lineTo(n, h); ctx.stroke();
      ctx.setLineDash([]);
      // diagonal corridors (3 squares wide), corner -> centre: frame cells 0 <= x < n/2, x <= y <= x + 2,
      // rotated to the 4 quadrants by (x, y) -> (n - 1 - y, x); y up, so canvas row = n - 1 - y
      ctx.fillStyle = 'rgba(11,122,117,0.18)';
      for (let r = 0; r < 4; r++) for (let x = 0; x < h; x++) for (let y = x; y <= x + 2; y++) {
        let p = [x, y];
        for (let q = 0; q < r; q++) p = [n - 1 - p[1], p[0]];
        ctx.fillRect(p[0], n - 1 - p[1], 1, 1);
      }
      return;
    }
    const b = spec.bandB, l = spec.bandL;
    ctx.fillStyle = 'rgba(11,122,117,0.10)';
    ctx.fillRect(0, n - b, n, b); ctx.fillRect(0, 0, n, b);          // bottom, top heel bands
    ctx.fillStyle = 'rgba(213,140,0,0.10)';
    ctx.fillRect(0, b, l, n - 2 * b); ctx.fillRect(n - l, b, l, n - 2 * b);   // left, right side bands
  }
  const triDirCache = new Map();
  function majorityDirs(n, tri) {
    const t = state.tour, id = state.key + n;
    if (triDirCache.has(id)) return triDirCache.get(id);
    const inside = (p, [a, b2, c]) => { const s = (u, v, w) => (v[0] - u[0]) * (w[1] - u[1]) - (v[1] - u[1]) * (w[0] - u[0]);
      const d1 = s(a, b2, p), d2 = s(b2, c, p), d3 = s(c, a, p); return !((d1 < 0 || d2 < 0 || d3 < 0) && (d1 > 0 || d2 > 0 || d3 > 0)); };
    const cnt = tri.map(() => [0, 0, 0, 0]);
    for (const e of t.E) { const p = [(e[0] + e[2]) / 2 + .5, (e[1] + e[3]) / 2 + .5];
      const i = tri.findIndex((q) => inside(p, q)); if (i >= 0) cnt[i][e[4]]++; }
    const out = cnt.map((c) => c.indexOf(Math.max(...c)));
    triDirCache.set(id, out); return out;
  }
  const hexA = (h, a) => `rgba(${parseInt(h.slice(1, 3), 16)},${parseInt(h.slice(3, 5), 16)},${parseInt(h.slice(5, 7), 16)},${a})`;

  // ---------- pan / zoom ----------
  let drag = null;
  canvas.addEventListener('wheel', (ev) => {
    ev.preventDefault(); const v = state.view; if (!v) return;
    const r = canvas.getBoundingClientRect(), m = Math.min(r.width, r.height);
    const px = ev.clientX - r.left, py = ev.clientY - r.top, bx = v.x0 + px / m * v.s, by = v.y0 + py / m * v.s;
    const s2 = Math.min(Math.max(v.s * Math.exp(ev.deltaY * 0.0015), 6), state.n * 1.6);
    v.s = s2; v.x0 = bx - px / m * s2; v.y0 = by - py / m * s2; draw();
  }, { passive: false });
  canvas.addEventListener('pointerdown', (ev) => { drag = { x: ev.clientX, y: ev.clientY }; canvas.setPointerCapture(ev.pointerId); canvas.classList.add('drag'); });
  canvas.addEventListener('pointermove', (ev) => {
    if (!drag) return; const r = canvas.getBoundingClientRect(), v = state.view, m = Math.min(r.width, r.height);
    v.x0 -= (ev.clientX - drag.x) / m * v.s; v.y0 -= (ev.clientY - drag.y) / m * v.s;
    drag = { x: ev.clientX, y: ev.clientY }; draw();
  });
  const endDrag = () => { drag = null; canvas.classList.remove('drag'); };
  canvas.addEventListener('pointerup', endDrag); canvas.addEventListener('pointercancel', endDrag);
  document.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => setView(b.dataset.view)));

  // ---------- panel ----------
  const stepsOf = () => STEPS[state.metric];
  function slopeFor(k, m) { return KNOWN[m][k] || slopeOf(k, m); }
  function renderSteps() {
    const m = state.metric, ks = stepsOf(), i = ks.indexOf(state.key);
    document.querySelectorAll('[data-metric]').forEach((b) => b.classList.toggle('on', b.dataset.metric === m));
    $('steps').innerHTML = ks.map((k, j) => `<button class="choice${k === state.key ? ' on' : ''}" data-k="${k}">` +
      `<div class="ct"><b><em>${j + 1}</em> ${C[k].name}</b><span class="f">${fmtSlope(KNOWN[m][k])}${k === 'TT16' ? ' − 14' : ''}</span></div>` +
      `<span>${C[k].credit} &middot; ${C[k].date}</span></button>`).join('') +
      (STEPNOTE[m] ? `<div class="note">${STEPNOTE[m]}</div>` : '') +
      '<div class="note">Step labels show leading terms; exact counts include size-dependent constants. TT16\'s turn count is exactly 8n-14. ' +
      'The demo\'s board-size range is narrower than some constructions\' full range.</div>';
    $('steps').querySelectorAll('.choice').forEach((b) => b.addEventListener('click', () => selectKey(b.dataset.k)));
    const r = $('steprange'); r.min = 1; r.max = ks.length; r.value = i + 1;
    $('stepnum').textContent = `step ${i + 1} of ${ks.length}`;
  }
  function selectKey(k) { state.key = k; state.n = NSTART[k] || C[k].nmin; load(true); }
  function setStep(j) {
    const ks = stepsOf(); j = Math.max(0, Math.min(ks.length - 1, j));
    if (ks[j] !== state.key) selectKey(ks[j]);
  }
  $('steprange').addEventListener('input', (e) => setStep(+e.target.value - 1));
  $('stepprev').addEventListener('click', () => setStep(stepsOf().indexOf(state.key) - 1));
  $('stepnext').addEventListener('click', () => setStep(stepsOf().indexOf(state.key) + 1));
  document.querySelectorAll('[data-metric]').forEach((b) => b.addEventListener('click', () => {
    if (b.dataset.metric === state.metric) return;
    state.metric = b.dataset.metric;
    $('tCross').checked = state.metric === 'X'; $('tTurns').checked = state.metric === 'T';
    if (!stepsOf().includes(state.key)) selectKey(stepsOf()[stepsOf().length - 1]); else load(true);
  }));
  function renderCounts() {
    const t = state.tour, k = state.key, n = t.n;
    const row = (m, label, val) => {
      const sl = slopeFor(k, m);
      const c = sl ? val - sl[0] * n / sl[1] : null;
      return `<div class="row${state.metric === m ? ' head' : ''}"><span class="lab">${label}</span><span class="val">${val}</span></div>` +
        `<div class="sl">${sl ? `${m} = ${val} = ${fmtSlope(sl)} ${fmtConst(c, sl[1])}` : ''}</div>`;
    };
    $('counts').innerHTML = state.metric === 'X' ? row('X', 'Crossings', t.X.length) + row('T', 'Turns', t.T.length)
      : row('T', 'Turns', t.T.length) + row('X', 'Crossings', t.X.length);
    const py = t.rec, okCounts = py.crossings === t.X.length && py.turns === t.T.length;
    const el = $('check');
    if (t.ok && py.valid && okCounts) {
      el.className = 'check ok';
      el.textContent = `One closed tour through all ${n * n} squares. Counts match the Python check` +
        (py.brute_crossings != null ? ' and a brute-force count.' : '.');
    } else {
      el.className = 'check bad';
      el.textContent = `Check failed: tour ok=${t.ok}, Python valid=${py.valid}, X ${t.X.length} vs ${py.crossings}, T ${t.T.length} vs ${py.turns}`;
    }
  }
  function renderLegend() {
    $('dirLegend').innerHTML = DIRS.map((d) => `<span><i style="background:${d.col}"></i>${d.name}</span>`).join('');
    $('dirLegend').style.display = $('tColor').checked ? '' : 'none';
  }
  function setRange() {
    const spec = C[state.key];
    state.n = Math.min(NMAX, Math.max(spec.nmin, state.n - (state.n % 2)));
    for (const el of [$('nrange'), $('nnum')]) { el.min = spec.nmin; el.max = NMAX; el.value = state.n; }
    $('nnote').innerHTML = `<b>n: even, ${spec.nmin} to ${NMAX} here.</b> Odd n has no closed tour (an odd number of squares). ${NRULE[state.key]}` +
      (state.key === 'P40' && state.n === 48 ? ' <b>At this n the count equals step 2.</b>' : '');
  }

  let loadSeq = 0;
  async function load(changedKey) {
    if (changedKey) renderSteps();
    setRange();
    const spec = C[state.key];
    $('caption').innerHTML = `<div class="ctitle"><strong>${spec.name}</strong><span>${spec.credit} &middot; ${spec.date}</span></div>` +
      `<div>${spec.caption[state.metric]}</div><div class="audit">${spec.audit}</div>`;
    const seq = ++loadSeq, key = state.key, n = state.n;
    $('loading').style.display = 'block';
    let t;
    try { t = await getTour(key, n); } catch (e) { $('loading').textContent = 'could not load data'; return; }
    if (seq !== loadSeq) return;
    $('loading').style.display = 'none';
    const keepView = state.tour && state.tour.n === n && state.view;
    state.tour = t;
    if (!keepView) setView('fit'); else draw();
    renderCounts(); renderCharts(); writeHash();
    for (const m of [n - 2, n + 2]) if (m >= C[key].nmin && m <= NMAX) getTour(key, m).catch(() => {});
  }
  let debounce = null;
  function setN(v) {
    state.n = Math.round(+v / 2) * 2; setRange();
    clearTimeout(debounce); debounce = setTimeout(() => load(false), 60);
  }
  $('nrange').addEventListener('input', (e) => setN(e.target.value));
  $('nnum').addEventListener('change', (e) => setN(e.target.value));
  $('nminus').addEventListener('click', () => setN(state.n - 2));
  $('nplus').addEventListener('click', () => setN(state.n + 2));
  for (const id of ['tCross', 'tTurns', 'tLayout', 'tSolver', 'tChecker']) $(id).addEventListener('change', () => { draw(); writeHash(); });
  $('tColor').addEventListener('change', () => { renderLegend(); draw(); writeHash(); });
  window.addEventListener('resize', resize);

  // ---------- chart: the selected measure for every step, with the lower bounds ----------
  function renderCharts() {
    const m = state.metric;
    $('charttitle').textContent = (m === 'X' ? 'Crossings' : 'Turns') + ' as n grows: tour counts and lower-bound reference lines';
    $('chartnote').textContent = m === 'X'
      ? 'Dashed lines: lower bounds on crossings, drawn by their leading terms. 4n is the paper\'s lower bound; 5n is the new one (Oct 3). Exact statements: X ≥ 4n − 2 and X ≥ 5n − 612 (audited, Claim 42).'
      : 'Dashed lines: lower bounds on turns. 6n is the leading term of the paper\'s lower bound, (6 − ε)n. 8n − 28 is the new exact lower bound.';
    chart($('chart'), FIELD[m]);
  }
  function chart(svg, f) {
    const m = state.metric, W = svg.clientWidth || 600, H = 260, pad = { l: 46, r: 270, t: 10, b: 26 };
    const S = state.summary, xs = [48, NMAX], ks = stepsOf();
    let ymax = 0;
    for (const k of ks) for (const s in S[k]) ymax = Math.max(ymax, S[k][s][f]);
    const step = [250, 500, 1000, 2000].find((v) => ymax / v <= 5) || 5000;
    ymax = Math.ceil(ymax / step) * step;
    const X = (n) => pad.l + (n - xs[0]) / (xs[1] - xs[0]) * (W - pad.l - pad.r);
    const Y = (v) => H - pad.b - v / ymax * (H - pad.t - pad.b);
    let g = '';
    for (let v = 0; v <= ymax; v += step) g += `<line x1="${pad.l}" x2="${W - pad.r}" y1="${Y(v)}" y2="${Y(v)}" stroke="#ecebe7"/>` +
      `<text x="${pad.l - 6}" y="${Y(v) + 4}" text-anchor="end" font-size="11" fill="#8a8983">${v}</text>`;
    for (let n = 50; n <= NMAX; n += 50) g += `<text x="${X(n)}" y="${H - 8}" text-anchor="middle" font-size="11" fill="#8a8983">n = ${n}</text>`;
    const labs = [];
    for (const lb of LOWER[m]) {
      g += `<line x1="${X(xs[0])}" y1="${Y(lb.f(xs[0]))}" x2="${X(xs[1])}" y2="${Y(lb.f(xs[1]))}" stroke="#8a8983" stroke-width="1.5" stroke-dasharray="5 4"/>`;
      labs.push({ y: Y(lb.f(NMAX)) + 4, text: lb.name, on: false, dim: true });
    }
    for (const k of ks.filter((k) => k !== state.key).concat([state.key])) {
      const pts = Object.keys(S[k]).map(Number).sort((a, b) => a - b), on = k === state.key;
      g += `<polyline fill="none" stroke="${on ? ACCENT : '#b9b8b2'}" stroke-width="2" stroke-linejoin="round" points="${pts.map((n) => `${X(n)},${Y(S[k][n][f])}`).join(' ')}"/>`;
    }
    ks.forEach((k, j) => labs.push({ y: Y(S[k][NMAX][f]) + 4, text: `${j + 1}. ${C[k].name.replace('&times;', '×').replace(/ \(.*\)$/, '')}`, on: k === state.key }));
    labs.sort((a, b) => a.y - b.y);
    for (let i = 1; i < labs.length; i++) labs[i].y = Math.max(labs[i].y, labs[i - 1].y + 13);
    for (const l of labs) g += `<text x="${X(NMAX) + 6}" y="${l.y}" font-size="11.5" fill="${l.on ? '#1d1d1b' : '#8a8983'}" font-weight="${l.on ? 600 : 400}"${l.dim ? ' font-style="italic"' : ''}>${l.text}</text>`;
    const cur = S[state.key][state.n];
    if (cur) g += `<circle cx="${X(state.n)}" cy="${Y(cur[f])}" r="5" fill="${ACCENT}" stroke="#fff" stroke-width="2"/>`;
    g += `<line class="xh" x1="0" x2="0" y1="${pad.t}" y2="${H - pad.b}" stroke="#52514e" stroke-dasharray="3 3" visibility="hidden"/>`;
    g += `<rect x="${pad.l}" y="${pad.t}" width="${W - pad.l - pad.r}" height="${H - pad.t - pad.b}" fill="transparent" class="hit"/>`;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.innerHTML = g;
    const hit = svg.querySelector('.hit'), xh = svg.querySelector('.xh'), tip = $('tip');
    const nAt = (ev) => { const r = svg.getBoundingClientRect(); const px = (ev.clientX - r.left) * W / r.width;
      return Math.max(xs[0], Math.min(xs[1], Math.round((xs[0] + (px - pad.l) / (W - pad.l - pad.r) * (xs[1] - xs[0])) / 2) * 2)); };
    hit.addEventListener('mousemove', (ev) => {
      const n = nAt(ev); xh.setAttribute('x1', X(n)); xh.setAttribute('x2', X(n)); xh.setAttribute('visibility', 'visible');
      tip.innerHTML = `<b>n = ${n}</b> (${f})<br>` + ks.map((k, j) => `${j + 1}. ${C[k].name}: ${S[k][n] ? S[k][n][f] : '&ndash;'}`).join('<br>') +
        '<br>' + LOWER[m].map((lb) => `<i>${lb.name}: ${Math.round(lb.f(n) * 10) / 10}</i>`).join('<br>') + '<br><span style="color:#8a8983">click to show this n</span>';
      tip.style.display = 'block'; tip.style.left = ev.clientX + 14 + 'px'; tip.style.top = ev.clientY + 10 + 'px';
    });
    hit.addEventListener('mouseleave', () => { xh.setAttribute('visibility', 'hidden'); tip.style.display = 'none'; });
    hit.addEventListener('click', (ev) => setN(nAt(ev)));
  }

  // ---------- start; the URL hash keeps the state shareable ----------
  // #m=X&k=H16a&n=96&view=edge&show=cross,turns,color,layout,solver
  const SHOW = [['tCross', 'cross'], ['tTurns', 'turns'], ['tColor', 'color'], ['tLayout', 'layout'], ['tSolver', 'solver'], ['tChecker', 'checker']];
  const hp = new URLSearchParams(location.hash.slice(1));
  if (hp.get('m') === 'T') state.metric = 'T';
  state.key = STEPS[state.metric].includes(hp.get('k')) ? hp.get('k') : STEPS[state.metric][STEPS[state.metric].length - 1];
  state.n = +hp.get('n') || NSTART[state.key] || C[state.key].nmin;
  $('tTurns').checked = state.metric === 'T'; $('tCross').checked = state.metric === 'X';
  if (hp.get('show') !== null) { const on = hp.get('show').split(','); for (const [id, nm] of SHOW) $(id).checked = on.includes(nm); }
  let firstView = hp.get('view');
  function writeHash() {
    const show = SHOW.filter(([id]) => $(id).checked).map(([, nm]) => nm);
    history.replaceState(null, '', `#m=${state.metric}&k=${state.key}&n=${state.n}&show=${show.join(',')}`);
  }
  fetch('data/summary.json').then((r) => r.json()).then((s) => {
    state.summary = s; renderLegend(); resize();
    load(true).then(() => { if (firstView) setView(firstView); firstView = null; });
  });
})();
