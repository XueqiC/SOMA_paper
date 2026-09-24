#!/usr/bin/env python3
"""Compact re-render of Figure 5(c), the MT-Bench-101 ability radar, sized to share its row height
with the two ablation panels. Values, series, labels and line colours are exactly those of
~/Dropbox/intern/test.ipynb cell 49 (including its History-Prefix series); the plotted vertices
were checked against the previous figure/mt_radar.pdf and agree to 0.01. The legend is omitted
because the Figure 5 caption carries a coloured key.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import paper_style as ps

ps.apply()
HERE = os.path.dirname(os.path.abspath(__file__))

abilities = ["Memory", "Understanding", "Interference", "Rephrasing", "Reflection", "Reasoning", "Questioning"]
scores_gt = [8.88, 9.29, 9.91, 9.56, 9.44, 7.16, 7.82]
scores_sur = [7.64, 7.05, 8.35, 8.44, 6.71, 2.86, 5.15]
scores_ours = [8.40, 8.10, 9.00, 9.10, 8.50, 6.10, 7.40]
gt, ou, sur = np.array(scores_gt), np.array(scores_ours), np.array(scores_sur)
eps = 0.05                                               # as in cell 49
mid = (sur + ou) / 2.0
between = np.where(ou > sur, np.clip(mid, sur + eps, ou - eps), np.minimum(ou - eps, sur + eps))

# series as plotted in cell 49: (values, label, colour, line width, fill alpha)
series = [(sur, "Surrogate", "#e07a5f", 0.9, 0.20), (between, "History-Prefix", "#7e57c2", 0.9, 0.22),
          (ou, "History-FT", "#3d9a7a", 1.0, 0.25), (gt, "SOMA", "#457b9d", 1.0, 0.18)]

N = len(abilities)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist(); angles += angles[:1]
close = lambda v: list(v) + [v[0]]

W_IN, H_IN = 1.62, 0.99
import matplotlib.patheffects as pe
fig = plt.figure(figsize=(W_IN, H_IN))
D = 0.64                                                # circle diameter as a fraction of the height
ax = fig.add_axes([0.5 - D * H_IN / W_IN / 2, 0.5 - D / 2 - 0.01, D * H_IN / W_IN, D], polar=True)
ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
ax.set_ylim(4, 10); ax.set_yticks([6, 8, 10]); ax.set_yticklabels([])
ax.set_xticks(angles[:-1]); ax.set_xticklabels([])
ax.grid(color="#D9D9D9", lw=0.4); ax.spines["polar"].set_color("#8C8C8C"); ax.spines["polar"].set_linewidth(0.5)
for vals, lab, col, lw, a in series:
    ax.plot(angles, close(vals), color=col, lw=lw, label=lab, zorder=3)
    ax.fill(angles, close(vals), color=col, alpha=a, lw=0, zorder=2)
halo = [pe.withStroke(linewidth=1.6, foreground="white")]
for r in (6, 8, 10):                                     # radial scale along the gap between two spokes
    ax.text(np.radians(360 / 7 / 2), r, str(r), fontsize=4.6, color="#333333", ha="center", va="center",
            path_effects=halo, zorder=6)
for k, name in enumerate(abilities):                     # ability labels outside the circle, aligned by angle
    th = angles[k]; sx, cy = np.sin(th), np.cos(th)
    ha = "center" if abs(sx) < 0.2 else ("left" if sx > 0 else "right")
    va = "bottom" if cy > 0.5 else ("top" if cy < -0.5 else "center")
    ax.text(th, 10.9, name, fontsize=5.8, fontweight="bold", color="#000000", ha=ha, va=va, clip_on=False)
fig.savefig(os.path.join(HERE, "..", "mt_radar.pdf"))
fig.savefig(os.path.join(HERE, "mt_radar.png"), dpi=400)
print("wrote figure/mt_radar.pdf", W_IN, "x", H_IN, "in")
