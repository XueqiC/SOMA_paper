#!/usr/bin/env python3
"""Figure that replaces the former Tables 4 and 5 (one row, three panels). Every number is copied verbatim from the
tables they replace (see the git history of experiment_new.tex); nothing is re-measured.

  figure/break_even.pdf   end-to-end savings vs. session length on ShareGPT (was: break-even table)
  figure/reliability.pdf  (a) MATH context dependency, (b) topic-shift stress test (was: reliability table)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")

import paper_style as ps   # shared method colours/markers: Original navy square, SOMA teal circle, degraded red down-triangle
NAVY, OCHRE, RED, GRAY = ps.METHOD_COLOR["Original"], ps.METHOD_COLOR["Surrogate"], ps.DEGRADED, "#8C8C8C"
TEAL, TEAL_D = ps.METHOD_COLOR["SOMA"], ps.TEAL_D
MK_ORIG, MK_SOMA, MK_DEG = ps.METHOD_MARKER["Original"], ps.METHOD_MARKER["SOMA"], ps.DEGRADED_MARKER
INK, INK2, GRID = "#1E2A2F", "#2E3B40", "#E4E8E7"
NAVY_D, OCHRE_D, RED_D = "#2B4C80", "#9C5A22", "#96303A"   # darker shades for text labels
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix", "mathtext.default": "bf", "font.size": 8, "font.weight": "bold",
    "axes.labelsize": 8.5, "axes.labelweight": "bold", "axes.labelcolor": INK, "text.color": INK,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5, "axes.edgecolor": INK2,
    "axes.linewidth": 0.8, "xtick.color": INK, "ytick.color": INK, "xtick.labelcolor": INK,
    "ytick.labelcolor": INK, "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})

# ---------------- one row: (a) break-even, (b) context dependency, (c) topic shift ----------------
fig, (e, a, b) = plt.subplots(1, 3, figsize=(5.5, 1.62), gridspec_kw={"width_ratios": [1.0, 0.95, 1.45]})
halo = dict(facecolor="white", edgecolor="none", pad=0.3)
def fmt(v): return f"{v:+.1f}".replace("-", "−")

# (a) end-to-end saving vs. session length (former Table 4)
buckets = ["1–4", "5–8", "9–12", "13+"]
latency = [-4.1, 4.7, 16.3, 29.1]
tokens = [-1.2, 8.5, 23.8, 37.2]
x = list(range(len(buckets)))
e.axhline(0, color=INK2, lw=0.7, ls=(0, (3, 2)), zorder=1)
e.text(3.3, 0.9, "break-even", fontsize=6.8, color=INK, ha="right", va="bottom")
e.plot(x, tokens, color=TEAL, marker=MK_SOMA, ms=3.4, lw=1.3, ls=(0, (3.2, 1.6)), mfc="white", mew=1.1, label="Tokens", zorder=3)
e.plot(x, latency, color=TEAL, marker=MK_SOMA, ms=3.4, lw=1.3, label="Latency", zorder=3)
for xi, t, l in zip(x, tokens, latency):
    e.text(xi, t + 2.3, fmt(t), ha="center", va="bottom", fontsize=6.8, color=TEAL_D, fontweight="bold", bbox=halo, zorder=5)
    e.text(xi, l - 2.5, fmt(l), ha="center", va="top", fontsize=6.8, color=TEAL_D, fontweight="bold", bbox=halo, zorder=5)
e.set_xticks(x); e.set_xticklabels(buckets); e.set_xlim(-0.4, 3.4)
e.set_xlabel("Session length (turns)", labelpad=1.5); e.set_ylabel("Saving vs. Original (%)", labelpad=1.5)
e.set_ylim(-14, 48); e.yaxis.set_major_locator(MultipleLocator(10))
e.grid(axis="y", color=GRID, lw=0.5, zorder=0)
e.legend(loc="upper left", frameon=False, handlelength=1.3, handletextpad=0.4, borderaxespad=0.1, fontsize=7.4)
e.text(-0.02, 1.06, "(a) Overhead is amortized", transform=e.transAxes, fontsize=8.5, fontweight="bold", va="bottom")

# (b) MATH context dependency (former Table 5a)
tb = ["1–3", "4–6", "7+"]
full, full_sd = [46.92, 47.18, 46.75], [0.58, 0.51, 0.49]
none, none_sd = [43.78, 34.92, 24.88], [0.66, 0.76, 0.86]
xs = [0, 1, 2]
a.fill_between(xs, none, full, color=RED, alpha=0.08, lw=0)
a.errorbar(xs, full, yerr=full_sd, color=NAVY, marker=MK_ORIG, ms=3.2, lw=1.3, capsize=2, label="Full history")
a.errorbar(xs, none, yerr=none_sd, color=RED, marker=MK_DEG, ms=3.6, lw=1.3, capsize=2, label="No history")
for xi, f, n in zip(xs, full, none):
    a.annotate("", xy=(xi, n + 1.1), xytext=(xi, f - 1.1),
               arrowprops=dict(arrowstyle="->", color=INK, lw=0.8, shrinkA=0, shrinkB=0))
    a.text(xi + 0.08, (f + n) / 2, "−" + f"{f - n:.1f}", fontsize=6.8, color=INK, va="center")
a.set_xticks(xs); a.set_xticklabels(tb); a.set_xlim(-0.3, 2.7)
a.set_ylim(20, 52); a.yaxis.set_major_locator(MultipleLocator(10))
a.set_xlabel("Turn index (bucket)", labelpad=1.5); a.set_ylabel("MATH EM (%)", labelpad=1.5)
a.grid(axis="y", color=GRID, lw=0.5, zorder=0)
a.legend(loc="lower left", frameon=False, handlelength=1.1, handletextpad=0.4, borderaxespad=0.1, fontsize=7.2)
a.text(-0.02, 1.06, "(b) Later turns need context", transform=a.transAxes, fontsize=8.5, fontweight="bold", va="bottom")

# (c) topic-shift stress test (former Table 5b), as a dot plot: similarity need not start at zero
data = [  # name, clean, clean_sd, no_rb, no_rb_sd, soma, soma_sd, detect, false_rb
    ("ShareGPT", 96.4, 1.91, 88.5, 2.03, 94.1, 1.47, 90.8, 4.3),
    ("ReMeDi", 93.2, 0.98, 85.7, 1.92, 91.1, 1.34, 89.6, 3.9),
    ("Craigslist", 91.9, 2.49, 83.1, 2.11, 89.3, 1.68, 88.9, 3.8)]
for r, (name, c, csd, n, nsd, s_, ssd, det, frb) in enumerate(data):
    y = 2 - r
    b.plot([n, c], [y, y], color=GRID, lw=2.2, zorder=1, solid_capstyle="round")
    b.annotate("", xy=(s_ - 0.35, y), xytext=(n + 0.35, y),
               arrowprops=dict(arrowstyle="->", color=INK, lw=0.8, shrinkA=0, shrinkB=0), zorder=2)
    b.errorbar(n, y, xerr=nsd, fmt=MK_DEG, color=RED, ms=3.8, capsize=1.6, lw=0.8, zorder=3,
               label="No rollback" if r == 0 else None)
    b.errorbar(s_, y, xerr=ssd, fmt=MK_SOMA, color=TEAL, ms=3.9, capsize=1.6, lw=0.8, zorder=4,
               label="SOMA" if r == 0 else None)
    b.errorbar(c, y, xerr=csd, fmt=MK_SOMA, mfc="white", mec=TEAL, mew=1.1, color=TEAL, ms=3.7, capsize=1.6, lw=0.8,
               zorder=3, label="No shift" if r == 0 else None)
    b.text(104.2, y, f"{det:.1f} / {frb:.1f}", fontsize=6.9, color=INK, va="center", ha="center")
    b.text(79.4, y + 0.3, name, fontsize=7.4, color=INK, va="bottom", ha="left")
b.text(104.2, 2.62, "detect /\nfalse RB", fontsize=6.6, color=INK, va="center", ha="center", linespacing=0.95)
b.axvline(100.9, color=GRID, lw=0.6)
b.set_yticks([])
b.set_xlim(79, 107.5); b.set_ylim(-1.25, 2.95)
b.set_xticks([80, 85, 90, 95, 100])
b.set_xlabel("Similarity under a topic shift", labelpad=1.5)
b.grid(axis="x", color=GRID, lw=0.5, zorder=0)
b.tick_params(axis="y", length=0)
b.legend(loc="lower left", ncol=3, frameon=False, handletextpad=0.2, columnspacing=0.7, handlelength=1.2,
         borderaxespad=0.1, fontsize=6.9)
b.text(-0.02, 1.06, "(c) Rollback recovers the drop", transform=b.transAxes, fontsize=8.5, fontweight="bold", va="bottom")

fig.tight_layout(pad=0.2, w_pad=0.9)
fig.subplots_adjust(top=0.86)
fig.savefig(os.path.join(OUT, "operating.pdf"))
fig.savefig(os.path.join(HERE, "operating.png"), dpi=300)
plt.close(fig)
print("wrote figure/operating.pdf")
