#!/usr/bin/env python3
"""Generate the SOMA method-overview figure (SVG -> figure/overview.pdf + preview PNG).

Layout (viewBox 800x372, printed at \\textwidth, so 12px ~ 6pt):
  top row : an example session as a timeline (block width = length of the user turn),
            coloured by who serves it: F (blue), G (orange), drift (red)
  panel 2 : soft-prompt mining on the frozen surrogate, drawn as mechanisms
  panel 3 : localized LoRA on frozen base weights, weighted by hardness
  panel 4 : acceptance gate (agreement + locality), compact serving, drift monitor
"""
import math, os
import cairosvg

# ---- palette: dataviz reference palette slots 1-3, status critical, neutrals ----
BLUE, BLUE_T = "#2a78d6", "#cde2fb"      # original model F
ORANGE, ORANGE_T = "#eb6834", "#fde3d7"  # surrogate G
AQUA, AQUA_T = "#1baf7a", "#d3f3e6"      # soft prompt, weak spots, adapter
RED, RED_T = "#d03b3b", "#f8dede"        # drift / rollback / rejected
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8985"
GRAY, GRAY_S = "#f0efec", "#c3c2b7"
FONT = "Helvetica, Arial, 'Liberation Sans', sans-serif"

out = []
def add(s): out.append(s)

def text(x, y, s, size=12, weight="normal", fill=INK, anchor="start", italic=False):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    st = ' font-style="italic"' if italic else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{st}>{s}</text>')

def rrect(x, y, w, h, r=6, fill="none", stroke=INK2, sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

def line(x1, y1, x2, y2, stroke=INK2, sw=1.2, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linecap="round"{d}{m}/>')

def path(d, stroke=INK2, sw=1.4, fill="none", marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round" '
        f'stroke-linecap="round"{m}{dd}/>')

def circle(cx, cy, r, fill="none", stroke="none", sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

# ---------------- icons ----------------
def robot(cx, cy, size, color, tint):
    """Friendly robot head (size = head width) with a small body; returns the bottom y."""
    hw, hh = size, size * 0.78
    x, y = cx - hw / 2, cy - hh / 2
    line(cx, y - size * 0.2, cx, y, stroke=color, sw=1.5)
    circle(cx, y - size * 0.24, size * 0.07, fill=color)
    rrect(x, y, hw, hh, r=size * 0.18, fill=tint, stroke=color, sw=1.6)
    ex, ey, er = size * 0.22, cy - hh * 0.08, size * 0.075
    circle(cx - ex, ey, er, fill=color); circle(cx + ex, ey, er, fill=color)
    path(f'M{cx-ex*0.8},{cy+hh*0.2} Q{cx},{cy+hh*0.36} {cx+ex*0.8},{cy+hh*0.2}', stroke=color, sw=1.4)
    bw, bh = hw * 0.62, hh * 0.3
    rrect(cx - bw / 2, y + hh + 2, bw, bh, r=3, fill=tint, stroke=color, sw=1.4)
    return y + hh + 2 + bh

def snowflake(cx, cy, r=6, color=BLUE):
    for a in (0, 60, 120):
        t = math.radians(a)
        dx, dy = r * math.cos(t), r * math.sin(t)
        line(cx - dx, cy - dy, cx + dx, cy + dy, stroke=color, sw=1.4)
        for s in (1, -1):
            ex, ey = cx + s * dx * 0.68, cy + s * dy * 0.68
            base = t if s > 0 else t + math.pi
            for b in (140, -140):
                tb = base + math.radians(b)
                line(ex, ey, ex + r * 0.38 * math.cos(tb), ey + r * 0.38 * math.sin(tb), stroke=color, sw=1.1)

def flame(cx, cy, s=1.0):
    path(f'M{cx},{cy-9*s} C{cx+7*s},{cy-2*s} {cx+6*s},{cy+6*s} {cx},{cy+7*s} '
         f'C{cx-6*s},{cy+6*s} {cx-7*s},{cy-1*s} {cx-2*s},{cy-5*s} C{cx-2*s},{cy-1*s} {cx},{cy} {cx},{cy-9*s} z',
         stroke="#e0621f", sw=1, fill="#f79a3e")
    path(f'M{cx},{cy-1*s} C{cx+3*s},{cy+2*s} {cx+3*s},{cy+5*s} {cx},{cy+6*s} '
         f'C{cx-3*s},{cy+5*s} {cx-2*s},{cy+2*s} {cx},{cy-1*s} z', stroke="none", sw=0, fill="#fde3a0")

def star(cx, cy, r=8, fill=BLUE):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        a = math.radians(-90 + 36 * k)
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    add(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#ffffff" stroke-width="0.8"/>')

def diamond(cx, cy, r=5, fill=ORANGE):
    add(f'<polygon points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}" fill="{fill}" '
        'stroke="#ffffff" stroke-width="0.8"/>')

def check(x, y, color=AQUA, s=10, sw=2.4):
    path(f'M{x},{y} l{s*0.35},{s*0.35} l{s*0.7},-{s*0.8}', stroke=color, sw=sw)

def cross(cx, cy, r=5, color=RED, sw=2.2):
    line(cx - r, cy - r, cx + r, cy + r, stroke=color, sw=sw)
    line(cx - r, cy + r, cx + r, cy - r, stroke=color, sw=sw)

def trash(x, y, w=16, h=18, color=MUTED):
    rrect(x, y + 4, w, h, r=2, fill="#fff", stroke=color, sw=1.2)
    line(x - 2, y + 4, x + w + 2, y + 4, stroke=color, sw=1.4)
    rrect(x + w / 2 - 4, y, 8, 4, r=1, fill="#fff", stroke=color, sw=1.2)
    for dx in (4, 8, 12):
        line(x + dx, y + 8, x + dx, y + h, stroke=color, sw=1)

def prompt_row(x, y, n=4, s=12, gap=3, color=AQUA, tint=AQUA_T, sw=1.3):
    for i in range(n):
        rrect(x + i * (s + gap), y, s, s, r=2, fill=tint, stroke=color, sw=sw)
    return x + n * (s + gap) - gap

def doc_card(x, y, w, h, color=MUTED, fill="#fff", nlines=2):
    rrect(x, y, w, h, r=3, fill=fill, stroke=color, sw=1.2)
    for i in range(nlines):
        yy = y + (i + 1) * h / (nlines + 1)
        line(x + 5, yy, x + w - 5 - 6 * i, yy, stroke=GRAY_S, sw=1.6)

def badge(cx, cy, n, color, r=8.5):
    circle(cx, cy, r, fill=color)
    text(cx, cy + 4.2, str(n), size=12, weight="bold", fill="#fff", anchor="middle")

def panel(x, y, w, h, n, title, color):
    rrect(x, y, w, h, r=9, fill="#ffffff", stroke=GRAY_S, sw=1)
    add(f'<path d="M{x},{y+24} v-15 a9,9 0 0 1 9,-9 h{w-18} a9,9 0 0 1 9,9 v15 z" fill="{color}"/>')
    circle(x + 15, y + 12, 8.5, fill="#fff")
    text(x + 15, y + 16.2, str(n), size=12, weight="bold", fill=color, anchor="middle")
    text(x + 30, y + 17, title, size=14.5, weight="bold", fill="#fff")

# =====================================================================
W, H = 800, 372
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
    'aria-label="SOMA overview: F answers the early turns; a soft prompt on the frozen surrogate G finds the '
    'turns where G is easiest to push away from F; a low-rank adapter is fitted on those turns; a gate hands '
    'the session to G, which serves from a compact context until a drift monitor rolls back to F.">')
add('<defs>'
    + "".join(f'<marker id="{mid}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" '
              f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>'
              for mid, col in (("arr", INK2), ("arrA", AQUA), ("arrR", RED), ("arrO", ORANGE), ("arrB", BLUE)))
    + '</defs>')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')

# ---------------- top row: example session timeline ----------------
text(10, 17, "An example session", size=14, weight="bold")
text(146, 17, "(block width = length of the user turn)", size=12, fill=INK2)
TY, TH = 26, 28
turns = [  # (width, label, kind); None marks the switch point
    (180, "“5-day veggie Kyoto trip, $2k”", "F"), (108, "“lighter day 3”", "F"), (90, "“tofu place?”", "F"),
    None,
    (62, "t4", "G"), (56, "t5", "G"), (62, "t6", "G"), (56, "t7", "G"),
    (84, "“my taxes?”", "R")]
x = 8; spans = {}
for t in turns:
    if t is None:
        spans["switch"] = (x, x + 28); x += 28; continue
    w, lab, kind = t
    fill, stroke = {"F": (BLUE_T, BLUE), "G": (ORANGE_T, ORANGE), "R": (RED_T, RED)}[kind]
    rrect(x, TY, w - 4, TH, r=5, fill=fill, stroke=stroke, sw=1.3)
    col = INK2 if kind == "G" else INK
    text(x + (w - 4) / 2, TY + 18.5, lab, size=12, fill=col, anchor="middle")
    spans.setdefault(kind, [x, x + w - 4]); spans[kind][1] = x + w - 4
    x += w
s0, s1 = spans["switch"]; sc = (s0 + s1) / 2 - 2
line(sc, TY - 2, sc, TY + TH + 2, stroke=ORANGE, sw=1.4, dash="3 3")
circle(sc, TY + TH / 2, 8, fill="#fff", stroke=ORANGE, sw=1.4)
check(sc - 4.2, TY + TH / 2 + 0.5, color=ORANGE, s=8, sw=2)
text(sc, TY - 5, "gate", size=12, weight="bold", fill=ORANGE, anchor="middle")
def bracket(x0, x1, color, y=TY + TH + 5):
    path(f'M{x0},{y} v5 H{x1} v-5', stroke=color, sw=1.3)
fx0, fx1 = spans["F"]; gx0, gx1 = spans["G"]; rx0, rx1 = spans["R"]
bracket(fx0, fx1, BLUE); bracket(gx0, gx1, ORANGE); bracket(rx0, rx1, RED)
by = TY + TH + 25
badge(fx0 + 30, by - 4, 1, BLUE)
text(fx0 + 42, by, "warm-start: F answers, and its replies are kept as targets", size=12)
badge(gx0 + 12, by - 4, 4, ORANGE)
text(gx0 + 24, by, "G serves from a compact context", size=12)
text((rx0 + rx1) / 2, by, "drift: back to F", size=12, weight="bold", fill=RED, anchor="middle")

# ---------------- panels ----------------
PY, PH = 96, 270
P2x, P2w = 8, 312
P3x, P3w = 334, 190
P4x, P4w = 538, 254
panel(P2x, PY, P2w, PH, 2, "Mine weak spots with a soft prompt", AQUA)
panel(P3x, PY, P3w, PH, 3, "Patch G locally", AQUA)
panel(P4x, PY, P4w, PH, 4, "Gate, serve, roll back", ORANGE)
for xa, xb in ((P2x + P2w, P3x), (P3x + P3w, P4x)):
    line(xa + 1, PY + PH / 2, xb - 1, PY + PH / 2, stroke=INK2, sw=1.8, marker="arr")

# ===== panel 2: soft-prompt mining =====
x0 = P2x
cy = 156
text(x0 + 42, cy - 23, "soft prompt", size=12, fill=AQUA, anchor="middle")
px1 = prompt_row(x0 + 12, cy - 7, n=4, s=13, gap=3)
flame(px1 + 9, cy - 1, s=0.8)
text(px1 + 24, cy + 5, "+", size=15, weight="bold", fill=INK2, anchor="middle")
doc_card(px1 + 34, cy - 11, 44, 22, nlines=2)
text(px1 + 56, cy - 23, "turns 1–3", size=12, fill=INK2, anchor="middle")
line(px1 + 82, cy, px1 + 98, cy, stroke=INK2, sw=1.4, marker="arr")
gx = px1 + 116
robot(gx, cy - 2, 26, ORANGE, ORANGE_T)
snowflake(gx + 21, cy + 6, r=5.5, color=BLUE)
text(gx + 4, cy - 24, "G (frozen)", size=12, fill=ORANGE, anchor="middle")
line(gx + 28, cy, gx + 42, cy, stroke=INK2, sw=1.4, marker="arr")
hx = gx + 48
for i, h in enumerate((8, 22, 13, 6, 17, 4)):
    add(f'<rect x="{hx + i*8:.1f}" y="{cy + 10 - h:.1f}" width="6" height="{h}" rx="1.5" fill="{MUTED}"/>')
line(hx - 2, cy + 10, hx + 48, cy + 10, stroke=GRAY_S, sw=1)
text(hx + 23, cy - 23, "next word", size=12, fill=INK2, anchor="middle")
path(f'M{gx-10},{cy+19} C{gx-50},{cy+34} {x0+70},{cy+34} {x0+42},{cy+11}', stroke=AQUA, sw=1.4,
     dash="4 3", marker="arrA")
text((gx + x0 + 42) / 2 + 6, cy + 42, "gradients update P only", size=12, fill=AQUA, anchor="middle")

# (b) G's embedding space: push G's mass off F's word and its neighbours
ex0, ey0, ew, eh = x0 + 8, 206, 198, 94
rrect(ex0, ey0, ew, eh, r=6, fill="#f8f8f6", stroke=GRAY_S, sw=1)
text(ex0 + 7, ey0 + 15, "G's word-embedding space", size=12, fill=INK2)
sx, sy, R = ex0 + 44, ey0 + 56, 21
circle(sx, sy, R, fill="#eef6fd", stroke=BLUE, sw=1.1, dash="3 3")
for dx, dy in ((-12, -9), (11, 10), (12, -9)):
    circle(sx + dx, sy + dy, 3, fill=MUTED)
star(sx, sy, r=8)
diamond(sx + 6, sy + 5, r=4.2)
for ang in (35, 145, -145):
    t = math.radians(ang)
    line(sx + (R + 2) * math.cos(t), sy - (R + 2) * math.sin(t),
         sx + (R + 15) * math.cos(t), sy - (R + 15) * math.sin(t), stroke=AQUA, sw=1.8, marker="arrA")
lx, ly = ex0 + 86, ey0 + 31
star(lx, ly - 4, r=6); text(lx + 10, ly, "F's word “temple”", size=12, fill=BLUE, weight="bold")
circle(lx, ly + 11, 3, fill=MUTED); text(lx + 10, ly + 15, "its neighbours", size=12, fill=INK2)
diamond(lx, ly + 26, r=4.2); text(lx + 10, ly + 30, "G's mean guess", size=12, fill=ORANGE)
text(lx + 10, ly + 44, "(near: weigh more)", size=12, fill=INK2)
line(lx - 5, ly + 55, lx + 5, ly + 55, stroke=AQUA, sw=1.8, marker="arrA")
text(lx + 10, ly + 59, "push G away", size=12, weight="bold", fill=AQUA)

# (c) keep entropy
cx0 = ex0 + ew + 6; cw = P2x + P2w - cx0 - 8
rrect(cx0, ey0, cw, eh, r=6, fill="#f8f8f6", stroke=GRAY_S, sw=1)
text(cx0 + cw / 2, ey0 + 16, "keep entropy", size=12, weight="bold", fill=INK, anchor="middle")
base = ey0 + 60
for i, h in enumerate((3, 30, 3, 2)):
    add(f'<rect x="{cx0 + 8 + i*9:.1f}" y="{base - h:.1f}" width="6" height="{h}" rx="1.5" fill="{MUTED}"/>')
for i, h in enumerate((12, 16, 14, 10)):
    add(f'<rect x="{cx0 + cw - 42 + i*9:.1f}" y="{base - h:.1f}" width="6" height="{h}" rx="1.5" fill="{AQUA}"/>')
line(cx0 + 5, base, cx0 + cw - 5, base, stroke=GRAY_S, sw=1)
cross(cx0 + 22, base + 11, r=4)
check(cx0 + cw - 30, base + 11, s=9)
text(cx0 + 22, base + 28, "spike", size=12, fill=RED, anchor="middle")
text(cx0 + cw - 24, base + 28, "spread", size=12, fill=AQUA, anchor="middle")

# (d) best of M prompts -> hardness per warm-start turn
dy0 = 310
for k in range(3):
    prompt_row(x0 + 14, dy0 + k * 13, n=4, s=9, gap=2.5, sw=1.1,
               color=AQUA if k == 1 else MUTED, tint=AQUA_T if k == 1 else "#ffffff")
check(x0 + 62, dy0 + 18, s=9)
text(x0 + 34, dy0 + 52, "best of M", size=12, fill=INK2, anchor="middle")
line(x0 + 80, dy0 + 18, x0 + 98, dy0 + 18, stroke=INK2, sw=1.4, marker="arr")
bb = dy0 + 38
for i, (h, c) in enumerate(((30, AQUA), (8, GRAY_S), (25, AQUA))):
    add(f'<rect x="{x0 + 108 + i*24:.1f}" y="{bb - h:.1f}" width="15" height="{h}" rx="3" fill="{c}"/>')
    text(x0 + 115.5 + i * 24, bb + 14, f"t{i+1}", size=12, fill=INK2, anchor="middle")
line(x0 + 102, bb, x0 + 178, bb, stroke=GRAY_S, sw=1)
text(x0 + 190, dy0 + 10, "hardness per turn:", size=12, fill=INK2)
text(x0 + 190, dy0 + 26, "t1, t3 = weak spots", size=12, weight="bold", fill=AQUA)
text(x0 + 190, dy0 + 42, "(G easy to push)", size=12, fill=INK2)

# ===== panel 3: localized LoRA =====
x0 = P3x
wx, wy = x0 + 14, 134
rrect(wx, wy, 54, 54, r=3, fill="#eeeeec", stroke=MUTED, sw=1.2)
snowflake(wx + 27, wy + 27, r=11, color=BLUE)
text(wx + 27, wy + 70, "base weights", size=12, fill=INK2, anchor="middle")
text(wx + 70, wy + 33, "+", size=16, weight="bold", fill=INK2, anchor="middle")
rrect(wx + 84, wy, 13, 54, r=2, fill=AQUA_T, stroke=AQUA, sw=1.4)
rrect(wx + 102, wy, 54, 13, r=2, fill=AQUA_T, stroke=AQUA, sw=1.4)
flame(wx + 129, wy + 36, s=0.95)
text(wx + 121, wy + 70, "LoRA (low-rank)", size=12, fill=AQUA, anchor="middle")
text(x0 + P3w / 2, wy + 86, "on attention + MLP", size=12, fill=INK2, anchor="middle")
cy0 = 238
for i, wgt in enumerate((34, 9, 28)):
    yy = cy0 + i * 19
    hard = wgt > 20
    rrect(x0 + 12, yy, 30, 15, r=3, fill="#fff", stroke=AQUA if hard else MUTED, sw=1.2)
    text(x0 + 27, yy + 11.5, f"t{i+1}", size=12, fill=INK2, anchor="middle")
    add(f'<rect x="{x0 + 47:.1f}" y="{yy + 3:.1f}" width="{wgt}" height="9" rx="2" fill="{AQUA if hard else GRAY_S}"/>')
line(x0 + 88, cy0 + 26, x0 + 104, cy0 + 26, stroke=INK2, sw=1.4, marker="arr")
rrect(x0 + 108, cy0 + 11, 72, 30, r=7, fill=BLUE_T, stroke=BLUE, sw=1.2)
text(x0 + 144, cy0 + 30, "F's replies", size=12, fill=INK, anchor="middle")
text(x0 + 12, cy0 + 70, "weight = hardness", size=12, fill=INK2)
trash(x0 + 14, 326)
prompt_row(x0 + 12, 314, n=3, s=6, gap=2, sw=1)
text(x0 + 38, 336, "prompt", size=12, fill=MUTED)
text(x0 + 38, 350, "discarded", size=12, fill=MUTED)
flame(x0 + 124, 333, s=0.75)
text(x0 + 134, 337, "trained", size=12, fill=INK2)
snowflake(x0 + 124, 351, r=5, color=BLUE)
text(x0 + 134, 355, "frozen", size=12, fill=INK2)

# ===== panel 4: gate, serve, roll back =====
x0 = P4x
text(x0 + 10, 139, "gate: both checks must pass", size=12, weight="bold", fill=ORANGE)
ox, oy = x0 + 16, 198
for ang, col, mk in ((62, BLUE, "arrB"), (44, ORANGE, "arrO")):
    t = math.radians(ang)
    line(ox, oy, ox + 46 * math.cos(t), oy - 46 * math.sin(t), stroke=col, sw=2, marker=mk)
path(f'M{ox + 17*math.cos(math.radians(44)):.1f},{oy - 17*math.sin(math.radians(44)):.1f} '
     f'A17,17 0 0 0 {ox + 17*math.cos(math.radians(62)):.1f},{oy - 17*math.sin(math.radians(62)):.1f}',
     stroke=INK2, sw=1)
text(ox + 14, oy - 46, "F", size=12, weight="bold", fill=BLUE)
text(ox + 39, oy - 30, "G", size=12, weight="bold", fill=ORANGE)
text(ox + 56, oy - 16, "replies", size=12)
text(ox + 56, oy - 2, "agree", size=12)
check(ox + 90, oy - 50, s=10)
qx, qy = x0 + 150, 176
circle(qx, qy, 24, fill="#eef6fd", stroke=BLUE, sw=1.1, dash="3 3")
for dx, dy in ((-10, -9), (9, -12), (-13, 8), (5, 11)):
    circle(qx + dx, qy + dy, 3, fill=BLUE)
line(qx - 3, qy - 3, qx + 3, qy + 3, stroke=INK, sw=1.4); line(qx - 3, qy + 3, qx + 3, qy - 3, stroke=INK, sw=1.4)
circle(qx + 14, qy + 1, 4.2, fill=ORANGE, stroke="#fff", sw=1)
text(qx + 30, qy - 2, "query", size=12)
text(qx + 30, qy + 12, "on topic", size=12)
check(qx + 60, qy - 28, s=10)
sy0 = 226
robot(x0 + 22, sy0 + 20, 24, ORANGE, ORANGE_T)
line(x0 + 38, sy0 + 20, x0 + 52, sy0 + 20, stroke=INK2, sw=1.3, marker="arr")
doc_card(x0 + 54, sy0 + 6, 38, 28, color=ORANGE, nlines=3)
for i in range(3):
    rrect(x0 + 108 + i * 12, sy0 + 6, 9, 28, r=2, fill=GRAY, stroke=MUTED, sw=1)
text(x0 + 99, sy0 + 25, "+", size=13, weight="bold", fill=INK2, anchor="middle")
text(x0 + 98, sy0 + 48, "summary + last K turns", size=12, fill=INK2, anchor="middle")
rrect(x0 + 164, sy0 + 14, 80, 12, r=3, fill=GRAY, stroke=MUTED, sw=1)
line(x0 + 162, sy0 + 32, x0 + 246, sy0 + 8, stroke=RED, sw=1.8)
text(x0 + 204, sy0 + 48, "full history", size=12, fill=MUTED, anchor="middle")
text(x0 + 10, 296, "drift monitor", size=12, weight="bold")
ax0, ay0, ax1, ay1 = x0 + 16, 344, x0 + 146, 302
line(ax0, ay0, ax1, ay0, stroke=MUTED, sw=1)
line(ax0, ay0, ax0, ay1, stroke=MUTED, sw=1, marker="arr")
thr = 321
line(ax0, thr, ax1, thr, stroke=RED, sw=1.2, dash="4 3")
pts = [(ax0 + 16 + 24 * i, y) for i, y in enumerate((337, 333, 338, 315, 308))]
path("M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts), stroke=MUTED, sw=1.2)
for i, (px, py) in enumerate(pts):
    circle(px, py, 4, fill=RED if py < thr else ORANGE, stroke="#fff", sw=1)
    text(px, ay0 + 14, f"t{i+4}", size=12, fill=INK2, anchor="middle")
text(pts[3][0] + 12, 302, "2 in a row", size=12, fill=RED, anchor="middle")
line(ax1 + 6, 321, ax1 + 30, 321, stroke=RED, sw=1.6, marker="arrR")
robot(x0 + 212, 316, 26, BLUE, BLUE_T)
text(x0 + 212, 354, "back to F", size=12, weight="bold", fill=RED, anchor="middle")

add('</svg>')
svg = "\n".join(out)
here = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(here, "overview.svg")
open(svg_path, "w").write(svg)
cairosvg.svg2pdf(url=svg_path, write_to=os.path.join(here, "..", "overview.pdf"))
cairosvg.svg2png(url=svg_path, write_to=os.path.join(here, "overview.png"), output_width=2400)
print("wrote", svg_path, "and figure/overview.pdf")
