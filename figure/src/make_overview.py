#!/usr/bin/env python3
"""Generate the SOMA method-overview figure (SVG -> figure/overview.pdf + preview PNG).

One left-to-right storyline, mirrored by a session timeline underneath:
  (1) Warm-start          F answers turns 1..W                      -> context-reply pairs
  (2) Soft-prompt mining  prompt P on frozen G, three-term objective -> anchoring score of each turn
  (3) Localized LoRA      frozen weights + low-rank update, anchoring-weighted -> adapted G
  (4) Gated serving       fidelity + locality gate, compressed context, drift monitor
  bottom: turns 1-3 by F | one-time adaptation | turns 4-7 by G | drift at turn 8 -> back to (1)

Palette (checked with the dataviz validator, all pairs, light mode): navy F, ochre G,
teal = trained parameters, muted red = drift; everything else is grayscale.
viewBox 800 wide, printed at \\textwidth, so 12px ~ 6pt.
"""
import math, os
import cairosvg

NAVY, NAVY_T = "#3A62A0", "#E3EAF4"     # original model F
OCHRE, OCHRE_T = "#D08A45", "#F8ECDF"   # surrogate G
TEAL, TEAL_T = "#2A9D8F", "#DDF0ED"     # trained parameters (soft prompt, LoRA)
RED, RED_T = "#B5454A", "#F5E1E2"       # drift / rollback
INK, INK2, MUTED = "#111111", "#2F2F2F", "#6F6F6F"
RULE, SOFT, FROZEN = "#A9A9A9", "#F2F2F2", "#E6E6E6"
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"

out = []
def add(s): out.append(s)

def text(x, y, s, size=12.5, weight="normal", fill=INK, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}">{s}</text>')

def rect(x, y, w, h, r=3, fill="none", stroke=INK2, sw=1.1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

def line(x1, y1, x2, y2, stroke=INK2, sw=1.1, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linecap="round"{d}{m}/>')

def path(d, stroke=INK2, sw=1.2, fill="none", marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round" '
        f'stroke-linecap="round"{m}{dd}/>')

def circle(cx, cy, r, fill="none", stroke="none", sw=1.1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

# ---------------- glyphs ----------------
def lock(cx, cy, s=1.0, color=INK2):
    rect(cx - 4.5 * s, cy - 1 * s, 9 * s, 7 * s, r=1.2, fill=color, stroke=color, sw=0.8)
    path(f'M{cx-3*s},{cy-1*s} v{-2.5*s} a{3*s},{3*s} 0 0 1 {6*s},0 v{2.5*s}', stroke=color, sw=1.3)

def model(x, y, w, h, letter, color, tint, frozen=False, adapter=False, size=15):
    """A model drawn as a small stack of layers with its letter; lock = frozen, teal strip = LoRA."""
    for k in (2, 1):
        rect(x + 3 * k, y - 3 * k, w, h, r=3, fill="#ffffff", stroke=color, sw=0.9)
    rect(x, y, w, h, r=3, fill=tint, stroke=color, sw=1.3)
    text(x + w / 2 - (2 if adapter else 0), y + h / 2 + size * 0.36, letter, size=size, weight="bold",
         fill=color, anchor="middle")
    if adapter:
        rect(x + w - 6, y + 3, 4, h - 6, r=1, fill=TEAL, stroke=TEAL, sw=0.6)
    if frozen:
        lock(x + w + 10, y + h - 4, s=0.9)

def star(cx, cy, r=7, fill=NAVY):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        a = math.radians(-90 + 36 * k)
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    add(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#ffffff" stroke-width="0.7"/>')

def diamond(cx, cy, r=4.2, fill=OCHRE):
    add(f'<polygon points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}" fill="{fill}" '
        'stroke="#ffffff" stroke-width="0.7"/>')

def check(x, y, color=TEAL, s=9, sw=2.0):
    path(f'M{x},{y} l{s*0.35},{s*0.35} l{s*0.7},-{s*0.8}', stroke=color, sw=sw)

def bars(x, base, heights, color, w=5, gap=2):
    for i, h in enumerate(heights):
        add(f'<rect x="{x + i*(w+gap):.1f}" y="{base - h:.1f}" width="{w}" height="{h}" rx="1" fill="{color}"/>')

def doc(x, y, w, h, nlines=2, stroke=MUTED):
    rect(x, y, w, h, r=2, fill="#ffffff", stroke=stroke, sw=1)
    for i in range(nlines):
        yy = y + (i + 1) * h / (nlines + 1)
        line(x + 4, yy, x + w - 4 - 5 * i, yy, stroke=RULE, sw=1.4)

def panel(x, y, w, h, n, title, sub):
    rect(x, y, w, h, r=6, fill="#ffffff", stroke=RULE, sw=1.3)
    circle(x + 15, y + 16, 9, fill="#222222")
    text(x + 15, y + 20.2, str(n), size=12.5, weight="bold", fill="#ffffff", anchor="middle")
    text(x + 30, y + 21, title, size=14, weight="bold", fill=INK)
    text(x + 10, y + 39, sub, size=12.5, fill=INK2)

def chip(x, y, w, label, h=24):
    rect(x, y, w, h, r=4, fill=SOFT, stroke=RULE, sw=1.2)
    text(x + 8, y + 16, label, size=12.5, weight="bold", fill=INK)

# =====================================================================
W, H = 800, 330
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
    'aria-label="SOMA overview. Warm-start: F answers the first turns. An adversarial soft prompt on the frozen G scores '
    'how robustly G still reproduces F on each warm-start turn. Localized LoRA fits G to F, weighted by this score. Gated serving: G takes over '
    'after a fidelity and locality check and serves from a compressed context; a drift monitor rolls back to F.">')
add('<defs>' + "".join(
    f'<marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" '
    f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>'
    for mid, col in (("arr", INK2), ("arrT", TEAL), ("arrR", RED), ("arrN", NAVY), ("arrO", OCHRE))) + '</defs>')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')

PY_, PH = 6, 244
P = {1: (8, 168), 2: (190, 214), 3: (418, 168), 4: (600, 192)}
panel(P[1][0], PY_, P[1][1], PH, 1, "Warm-start", "F answers turns 1–W")
panel(P[2][0], PY_, P[2][1], PH, 2, "Soft-prompt mining", "probe frozen G on turns 1–W")
panel(P[3][0], PY_, P[3][1], PH, 3, "Localized LoRA", "fit G to F's replies")
panel(P[4][0], PY_, P[4][1], PH, 4, "Gated serving", "switch if both checks pass")
for a, b in ((1, 2), (2, 3), (3, 4)):
    xa = P[a][0] + P[a][1]; xb = P[b][0]
    line(xa + 1, PY_ + PH / 2, xb - 1, PY_ + PH / 2, stroke=INK, sw=2.2, marker="arr")
CHIP_Y = 216

# ===== (1) warm-start =====
x0 = P[1][0]
for i, w in enumerate((82, 58, 38)):           # user turns, long -> short
    rect(x0 + 12, 56 + i * 15, w, 11, r=2, fill=FROZEN, stroke=MUTED, sw=0.9)
text(x0 + 100, 76, "user turns", size=12.5, fill=INK2)
line(x0 + 40, 102, x0 + 40, 116, stroke=INK2, sw=1.3, marker="arr")
model(x0 + 22, 126, 38, 32, "F", NAVY, NAVY_T)
text(x0 + 100, 146, "large LLM", size=12.5, fill=INK2)
line(x0 + 40, 162, x0 + 40, 174, stroke=INK2, sw=1.3, marker="arr")
for i, w in enumerate((78, 60, 48)):           # F's replies
    rect(x0 + 12, 178 + i * 11, w, 8, r=2, fill=NAVY_T, stroke=NAVY, sw=0.9)
text(x0 + 100, 196, "replies", size=12.5, fill=INK2)
chip(x0 + 8, CHIP_Y, P[1][1] - 16, "context–reply pairs")

# ===== (2) soft-prompt mining =====
x0 = P[2][0]
cy = 74
for i in range(4):                             # trainable soft prompt
    rect(x0 + 10 + i * 13, cy - 6, 10, 12, r=2, fill=TEAL_T, stroke=TEAL, sw=1.1)
text(x0 + 66, cy + 5, "+", size=14, weight="bold", fill=INK2, anchor="middle")
doc(x0 + 74, cy - 10, 30, 20)
line(x0 + 108, cy, x0 + 122, cy, stroke=INK2, sw=1.3, marker="arr")
model(x0 + 126, cy - 12, 26, 26, "G", OCHRE, OCHRE_T, frozen=True, size=13)
line(x0 + 168, cy, x0 + 178, cy, stroke=INK2, sw=1.3, marker="arr")
bars(x0 + 180, cy + 10, (6, 18, 11, 4), MUTED)
text(x0 + 35, cy + 26, "prompt P", size=12.5, fill=INK2, anchor="middle")
text(x0 + 89, cy + 26, "context", size=12.5, fill=INK2, anchor="middle")
text(x0 + 184, cy + 26, "next token", size=12.5, fill=INK2, anchor="middle")
line(x0 + 10, 112, x0 + P[2][1] - 10, 112, stroke=RULE, sw=1)
ex, ey = x0 + 46, 152                          # objective in G's embedding space
circle(ex, ey, 22, fill=NAVY_T, stroke=NAVY, sw=1, dash="3 2.5")
for dx, dy in ((-12, -9), (11, 10), (12, -9)):
    circle(ex + dx, ey + dy, 2.8, fill=MUTED)
star(ex, ey)
diamond(ex + 7, ey + 6)
for ang in (40, 140, -140, -40):
    t = math.radians(ang)
    line(ex + 24 * math.cos(t), ey - 24 * math.sin(t), ex + 36 * math.cos(t), ey - 36 * math.sin(t),
         stroke=TEAL, sw=1.6, marker="arrT")
text(ex, ey + 46, "F's token and", size=12.5, fill=INK2, anchor="middle")
text(ex, ey + 59, "its neighbors", size=12.5, fill=INK2, anchor="middle")
lx = x0 + 106                                  # the three terms of the objective
line(lx, 127, lx + 12, 127, stroke=TEAL, sw=1.6, marker="arrT")
text(lx + 20, 131, "neighborhood", size=12)
text(lx + 20, 144, "unlikelihood", size=12)
diamond(lx + 6, 158)
text(lx + 20, 162, "expectation", size=12)
text(lx + 20, 175, "weighting", size=12)
bars(lx + 1, 193, (6, 8, 7), TEAL, w=3, gap=1.5)
text(lx + 20, 193, "entropy", size=12)
text(lx + 20, 206, "regularizer", size=12)
rect(x0 + 8, CHIP_Y, P[2][1] - 16, 24, r=4, fill=SOFT, stroke=RULE, sw=1)
text(x0 + 16, CHIP_Y + 16, "anchoring score per turn", size=12.5, weight="bold")
for i, h in enumerate((15, 5, 12)):
    add(f'<rect x="{x0 + 170 + i*10:.1f}" y="{CHIP_Y + 20 - h:.1f}" width="7" height="{h}" rx="1" fill="{TEAL}"/>')

# ===== (3) localized LoRA =====
x0 = P[3][0]
rect(x0 + 12, 56, 44, 44, r=2, fill=FROZEN, stroke=MUTED, sw=1.1)
lock(x0 + 34, 77, s=1.2)
text(x0 + 66, 83, "+", size=15, weight="bold", fill=INK2, anchor="middle")
rect(x0 + 78, 56, 10, 44, r=2, fill=TEAL_T, stroke=TEAL, sw=1.2)
rect(x0 + 92, 56, 44, 10, r=2, fill=TEAL_T, stroke=TEAL, sw=1.2)
text(x0 + 34, 116, "frozen", size=12.5, fill=INK2, anchor="middle")
text(x0 + 94, 86, "low-rank", size=12.5, fill=INK2)
text(x0 + 94, 99, "update", size=12.5, fill=INK2)
text(x0 + 10, 134, "on attention and MLP", size=12.5, fill=INK2)
for i, wgt in enumerate((30, 9, 25)):          # warm-start turns weighted by anchoring score
    yy = 148 + i * 17
    rect(x0 + 12, yy, 22, 12, r=2, fill="#ffffff", stroke=MUTED, sw=1)
    add(f'<rect x="{x0 + 38:.1f}" y="{yy + 2:.1f}" width="{wgt}" height="8" rx="1" fill="{TEAL}"/>')
line(x0 + 74, 171, x0 + 86, 171, stroke=INK2, sw=1.3, marker="arr")
rect(x0 + 90, 158, 68, 26, r=4, fill=NAVY_T, stroke=NAVY, sw=1)
text(x0 + 124, 175, "F's replies", size=12.5, anchor="middle")
text(x0 + 10, 206, "turns weighted by anchoring", size=12.5, fill=INK2)
chip(x0 + 8, CHIP_Y, P[3][1] - 16, "adapted G")
model(x0 + 110, CHIP_Y + 4, 22, 16, "G", OCHRE, OCHRE_T, adapter=True, size=11)

# ===== (4) gated serving =====
x0 = P[4][0]
ox, oy = x0 + 18, 100                          # fidelity: G's reply points where F's does
for ang, col, mk in ((64, NAVY, "arrN"), (46, OCHRE, "arrO")):
    t = math.radians(ang)
    line(ox, oy, ox + 42 * math.cos(t), oy - 42 * math.sin(t), stroke=col, sw=1.8, marker=mk)
path(f'M{ox + 15*math.cos(math.radians(46)):.1f},{oy - 15*math.sin(math.radians(46)):.1f} '
     f'A15,15 0 0 0 {ox + 15*math.cos(math.radians(64)):.1f},{oy - 15*math.sin(math.radians(64)):.1f}',
     stroke=INK2, sw=0.9)
text(ox + 12, oy - 42, "F", size=12.5, weight="bold", fill=NAVY)
text(ox + 36, oy - 26, "G", size=12.5, weight="bold", fill=OCHRE)
text(ox + 26, oy + 18, "fidelity", size=12.5, anchor="middle")
check(ox + 52, oy - 44)
qx, qy = x0 + 130, 78                          # locality: query near the warm-start centroid
circle(qx, qy, 20, fill=NAVY_T, stroke=NAVY, sw=1, dash="3 2.5")
for dx, dy in ((-9, -8), (8, -10), (-11, 7), (4, 9)):
    circle(qx + dx, qy + dy, 2.6, fill=NAVY)
line(qx - 3, qy - 3, qx + 3, qy + 3, stroke=INK, sw=1.3); line(qx - 3, qy + 3, qx + 3, qy - 3, stroke=INK, sw=1.3)
circle(qx + 12, qy + 1, 3.8, fill=OCHRE, stroke="#ffffff", sw=0.8)
text(qx, oy + 18, "locality", size=12.5, anchor="middle")
check(qx + 26, oy - 44)
line(x0 + 10, 128, x0 + P[4][1] - 10, 128, stroke=RULE, sw=1)
doc(x0 + 12, 138, 34, 26, nlines=3)            # compressed context -> adapted G
text(x0 + 53, 156, "+", size=12.5, weight="bold", fill=INK2, anchor="middle")
for i in range(3):
    rect(x0 + 60 + i * 10, 138, 7, 26, r=1.5, fill=FROZEN, stroke=MUTED, sw=0.9)
line(x0 + 94, 151, x0 + 112, 151, stroke=INK2, sw=1.3, marker="arr")
model(x0 + 118, 138, 28, 26, "G", OCHRE, OCHRE_T, adapter=True, size=13)
text(x0 + 10, 180, "summary + last K turns", size=12.5, fill=INK2)
bx0, by0 = x0 + 12, 238                        # drift monitor
line(bx0, by0, bx0 + 96, by0, stroke=MUTED, sw=0.9)
line(bx0, by0, bx0, 194, stroke=MUTED, sw=0.9)
thr = 212
line(bx0, thr, bx0 + 96, thr, stroke=RED, sw=1.1, dash="4 3")
pts = [(bx0 + 12 + 18 * i, y) for i, y in enumerate((232, 228, 233, 207, 201))]
path("M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts), stroke=MUTED, sw=1)
for px, py in pts:
    circle(px, py, 3.4, fill=RED if py < thr else OCHRE, stroke="#ffffff", sw=0.8)
text(bx0 + 108, 216, "drift", size=12)
text(bx0 + 108, 229, "monitor", size=12)

# ===== session timeline, aligned with the stages above =====
TY, TH = 258, 22
tx = P[1][0]
for i, w in enumerate((64, 48, 40)):
    rect(tx, TY, w, TH, r=3, fill=NAVY_T, stroke=NAVY, sw=1)
    text(tx + w / 2, TY + 15.5, f"t{i+1}", size=12.5, anchor="middle")
    tx += w + 4
line(tx, TY + TH / 2, P[2][0] - 2, TY + TH / 2, stroke=INK2, sw=1.2, marker="arr")
ax0, ax1 = P[2][0], P[3][0] + P[3][1]
rect(ax0, TY, ax1 - ax0, TH, r=3, fill=SOFT, stroke=MUTED, sw=1, dash="4 3")
text((ax0 + ax1) / 2, TY + 15.5, "one-time adaptation between turn 3 and turn 4 (steps 2–3)", size=12.5,
     fill=INK2, anchor="middle")
line(ax1 + 2, TY + TH / 2, P[4][0] - 2, TY + TH / 2, stroke=INK2, sw=1.2, marker="arr")
tx = P[4][0]
for i in range(4):
    rect(tx, TY, 34, TH, r=3, fill=OCHRE_T, stroke=OCHRE, sw=1)
    text(tx + 17, TY + 15.5, f"t{i+4}", size=12.5, anchor="middle")
    tx += 38
xe = P[4][0] + P[4][1]
rect(tx, TY, xe - tx, TH, r=3, fill=RED_T, stroke=RED, sw=1.2)
t8c = tx + (xe - tx) / 2
text(t8c, TY + 15.5, "t8", size=12.5, weight="bold", fill=RED, anchor="middle")
path(f'M{t8c:.1f},{TY + TH + 1} V{TY + TH + 16} H{P[1][0] + 32} V{TY + TH + 3}', stroke=RED, sw=1.5, marker="arrR")
add(f'<rect x="{400 - 200}" y="{TY + TH + 9}" width="400" height="15" fill="#ffffff"/>')
text(400, TY + TH + 21, "drift detected at turn 8: roll back to F and refresh the warm-start state",
     size=12.5, fill=RED, anchor="middle")
lgx, lgy = P[4][0] + 50, H - 4                  # legend
rect(lgx, lgy - 10, 12, 10, r=2, fill=TEAL_T, stroke=TEAL, sw=1)
text(lgx + 17, lgy, "trained", size=12.5, fill=INK2)
lock(lgx + 78, lgy - 5, s=1.0)
text(lgx + 88, lgy, "frozen", size=12.5, fill=INK2)

add('</svg>')
svg = "\n".join(out)
here = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(here, "overview.svg")
open(svg_path, "w").write(svg)
cairosvg.svg2pdf(url=svg_path, write_to=os.path.join(here, "..", "overview.pdf"))
cairosvg.svg2png(url=svg_path, write_to=os.path.join(here, "overview.png"), output_width=2400)
print("wrote", svg_path, "and figure/overview.pdf")
