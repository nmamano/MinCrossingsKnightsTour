def chart(title, rows, vmin, vmax, ticks, x0=318, x1=640, fmt=lambda v: f"{v:g}n"):
    W, rh, top = 720, 26, 40
    H = top + rh * len(rows) + 34
    X = lambda v: x0 + (v - vmin) * (x1 - x0) / (vmax - vmin)
    o = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12">']
    o.append(f'<text x="10" y="16" fill="#8a97a1" font-size="12">{title}</text>')
    o.append(f'<circle cx="{x0+6}" cy="28" r="4" fill="#c0392b"/><text x="{x0+14}" y="32" fill="#8a97a1" font-size="11">lower bound</text>')
    o.append(f'<circle cx="{x0+96}" cy="28" r="4" fill="#0b7a75"/><text x="{x0+104}" y="32" fill="#8a97a1" font-size="11">upper bound</text>')
    yb = top + rh * len(rows)
    for t in ticks:
        o.append(f'<line x1="{X(t):.1f}" y1="{top}" x2="{X(t):.1f}" y2="{yb}" stroke="#8a97a1" stroke-opacity="0.25" stroke-width="1"/>')
        o.append(f'<text x="{X(t):.1f}" y="{yb+16}" text-anchor="middle" fill="#8a97a1" font-size="11">{fmt(t)}</text>')
    for i, (who, when, lo, hi, lol, hil, ours) in enumerate(rows):
        y = top + rh * i + rh / 2
        col = "#0b7a75" if ours else "#9aa7b0"
        o.append(f'<text x="268" y="{y+4:.1f}" text-anchor="end" fill="currentColor">{who} <tspan fill="#8a97a1" font-size="11">· {when}</tspan></text>')
        o.append(f'<rect x="{X(lo):.1f}" y="{y-5:.1f}" width="{max(X(hi)-X(lo),0.5):.1f}" height="10" rx="3" fill="{col}" fill-opacity="0.35"/>')
        o.append(f'<circle cx="{X(lo):.1f}" cy="{y:.1f}" r="4" fill="#c0392b"/>')
        o.append(f'<circle cx="{X(hi):.1f}" cy="{y:.1f}" r="4" fill="#0b7a75"/>')
        o.append(f'<text x="{X(lo)-7:.1f}" y="{y+4:.1f}" text-anchor="end" fill="#c0392b" font-size="11" font-weight="bold">{lol}</text>')
        o.append(f'<text x="{X(hi)+7:.1f}" y="{y+4:.1f}" fill="currentColor" font-size="11" font-weight="bold">{hil}</text>')
    o.append('</svg>')
    return "\n".join(o)

BJMO, AT = "Besa, Johnson, Mamano, Osegueda", "Agent Team"
X_rows = [
    (BJMO, "Apr 2019", 4, 13, "4n", "13n", False),
    ("Parker Williams", "Jan 2022", 4, 12, "4n", "12n", False),
    ("Shisheng Li", "May 2026", 4, 11.5, "4n", "11.5n", False),
    (AT, "Oct 1, 4:59 pm", 4, 9, "4n", "9n", True),
    (AT, "Oct 1, 6:55 pm", 4, 7.15, "4n", "7.15n", True),
    (AT, "Oct 1, 8:31 pm", 4, 19/3, "4n", "6.33n", True),
    (AT, "Oct 1, 9:26 pm", 4.0001, 19/3, "4.0001n", "6.33n", True),
    (AT, "Oct 1, 9:59 pm", 4 + 1/17, 19/3, "4.06n", "6.33n", True),
    (AT, "Oct 1, 10:30 pm", 4.125, 19/3, "4.13n", "6.33n", True),
    (AT, "Oct 1, 10:42 pm", 4 + 4/23, 19/3, "4.17n", "6.33n", True),
    (AT, "Oct 1, 10:56 pm", 4 + 4/15, 19/3, "4.27n", "6.33n", True),
    (AT, "Oct 1, 11:14 pm", 4 + 4/11, 19/3, "4.36n", "6.33n", True),
    (AT, "Oct 1, 11:51 pm", 4.5, 19/3, "4.5n", "6.33n", True),
    (AT, "Oct 2, 12:21 am", 14/3, 19/3, "4.67n", "6.33n", True),
]
T_rows = [
    (BJMO, "Apr 2019", 6, 9.5, "6n", "9.5n", False),
    ("Parker Williams", "Jan 2022", 6, 9.25, "6n", "9.25n", False),
    (AT, "Oct 1, 5:26 pm", 8, 9.25, "8n", "9.25n", True),
    (AT, "Oct 1, 5:42 pm", 8, 8.5, "8n", "8.5n", True),
    (AT, "Oct 1, 6:23 pm", 8, 8, "8n", "8n: closed", True),
]
open("/tmp/charts/crossings.svg", "w").write(chart("Crossings: best known lower and upper bound after each step (times in PT)", X_rows, 3.5, 13.5, range(4, 14)))
open("/tmp/charts/turns.svg", "w").write(chart("Turns: best known lower and upper bound after each step (times in PT)", T_rows, 5.5, 10, [6, 7, 8, 9, 10]))
