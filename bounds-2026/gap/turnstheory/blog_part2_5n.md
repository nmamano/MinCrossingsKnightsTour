## Part 2: why every tour needs about 5n crossings

The proof has five steps:

1. Each knight move owns a small tile. Their total area gives the tile bound `4n - 2`.
2. Colour the board like a chess board. The colours define a charge that only a badly tiled spot can change.
3. At each corner, a nested path is charged when its end rows pass a local test. There are about `2n` candidate paths across the four corners.
4. A charged path needs two bad quarters. If they are in its middle, they pay for half an extra crossing. Different paths use different quarters.
5. The side strips pay for paths that lose their charge, and for charged paths whose bad quarters stay near an end. Together, the paths add about `n` crossings to the tile bound.

### Step 1: knight tiles

Here, we put the cells at the integer points and look at the unit squares between them.

Each knight move is the long diagonal of a small parallelogram. Its short diagonal is the unit edge with the same midpoint. This parallelogram is the move's _tile_. It has area exactly 1.

Cutting each unit square along both diagonals gives four _quarter triangles_. Every tile is made of exactly four of them:

<BlogImage
  src="/blog/knights-tour-crossings/lb_tile.png"
  alt="A knight move, its tile, and the tile as four quarter triangles"
  width="80%"
/>

Two tiles overlap exactly when their moves cross. They share one or two quarters, never more:

<BlogImage
  src="/blog/knights-tour-crossings/lb_overlap.png"
  alt="Two pairs of crossing moves, overlapping in one and in two quarters"
  caption="Two crossing pairs. The shared quarters are red."
  width="80%"
/>

A tour has `n^2` moves, so its tiles have total area `n^2`. The unit squares between the cells only have area `(n - 1)^2`. The extra area has to go into overlaps. Each crossing creates at most `1/2` of overlap, which gives at least `4n - 2` crossings.

This tile bound is also checked in Lean, a proof assistant. The stronger `5n - 612` bound below uses a Python certificate.

### Step 2: gaps cost too

A quarter is _bad_ if it is not covered exactly once.

<BlogImage
  src="/blog/knights-tour-crossings/lb_tiled.png"
  alt="Tile multiplicities near the corner of a tour"
  caption="Near a corner of a 48 x 48 tour. Blue: quarters covered once. Red: covered at least twice. White: not covered. The long straight lines inside tile the board perfectly. All the trouble is at the sides."
  width="90%"
/>

The area count is exact. Every uncovered quarter must be paid for by extra overlap somewhere. Crossings whose tiles share only one quarter, and quarters covered three or more times, also add to the count beyond `4n - 2`.

To force bad quarters, we use a charge. Orient tour moves and unit grid edges from black to white. Along a path through square centres, add their signed crossings modulo 3. Around a closed loop the sum is zero. Where the tiles fit perfectly, the charge doesn't change.

So a path whose ends have different charges must pass next to a bad quarter. We call it _charged_.

### Step 3: paths around the corners

Take a path up the right side of a corner box and then left along its top:

<BlogImage
  src="/blog/knights-tour-crossings/lb_corner_box.png"
  alt="A corner box, the path along its right and top sides, and its two end rows"
  caption="The path around a corner box. Its two ends sit next to the sides of the board."
  width="50%"
/>

The full boundary has charge zero. No tour move crosses the part outside the board. If the two end rows pass the local endpoint test, the outside part has charge `1 (mod 3)`. The inside path must carry the rest, so it is charged.

Use every radius from 12 to `n/2 - 4`, at all four corners:

<BlogImage
  src="/blog/knights-tour-crossings/lb_nested.png"
  alt="Four families of nested corner paths"
  caption="The four families of corner paths (here n = 48). A failed end test can remove a path."
  width="60%"
/>

The paths don't touch. There are `2n - 60` candidates. We keep those whose charge and endpoint conditions let us use the count below. Each discarded path has a failed test at an end.

### Step 4: half a crossing per path

A unit square never has just one bad quarter. Each tile covers two adjacent quarters, so the four counts satisfy `m0 - m1 + m2 - m3 = 0`:

<BlogImage
  src="/blog/knights-tour-crossings/lb_square.png"
  alt="The alternating sum of a unit square, and a square with two bad quarters"
  width="60%"
/>

A charged path therefore has two bad quarters in one of its squares. The exact area identity lets us pay `1/4` for each of them, using gaps and overlap counts. A crossing can pay for at most two quarters. Different paths use different quarters, so these payments don't exceed the available count.

There is one exception: two quarters covered by the same crossing pair in a side strip. That pair belongs to the side count instead. Away from the sides, this exception can't occur. A bad square in a path's middle therefore pays the full half crossing.

### Step 5: the side strips pay the rest

The remaining paths either lost their charge or have too few quarters paid by Step 4. In the second case, a bad quarter must come from the side-strip exception, near one of the path's ends.

A finite check scans the four columns next to each side. It counts both kinds of end row: a failed endpoint test, or a visible two-quarter overlap. The side has at least one crossing per row, plus one extra for each counted row, up to a fixed allowance for the ends of the scan.

Each remaining path can choose a different counted row. The exact area identity combines the quarter payments with half of this extra side count. Thus every candidate path pays half a crossing, either through its quarters or through a side row.

The `2n - 60` paths add `n - O(1)` to the tile bound. Keeping the constants gives `X >= 5n - 612`.

