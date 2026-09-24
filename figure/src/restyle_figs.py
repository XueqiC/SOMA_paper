#!/usr/bin/env python3
"""Re-render figures whose plotted values are written directly in ~/Dropbox/intern/test.ipynb,
in the shared paper style. Values are copied verbatim from the cited notebook cells; only
styling (fonts, colours, sizes, labels) changes.

  figure/long_tail.pdf          Fig. 1   (cells 13, 17)
  figure/llama_through.pdf      Fig. 3a  (cell 47)
  figure/qwen_through.pdf       Fig. 3b  (cell 47)
  figure/overall_avg_token.pdf  appendix (cell 53)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator, LogLocator, NullFormatter
import paper_style as ps

ps.apply()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")
def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"))
    fig.savefig(os.path.join(HERE, name + ".png"), dpi=300)
    plt.close(fig)

# ---------------- Fig. 1: long-tail token pattern (cell 13 values, cell 17 layout) ----------------
final_results = {
    "ShareGPT": dict(zip([1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37],
                         [102.1174, 20.8, 10.10, 5.87, 4.92, 3.9375, 2.99, 2.5, 2.0, 1.71, 1.40, 1.43, 1.40])),
    "ReMeDi": dict(zip([1, 4, 7, 10, 13, 16, 19, 22, 25, 28],
                       [99.67, 11.31, 5.22, 3.11, 1.98, 1.51, 1.48, 1.54, 1.51, 1.54])),
    "Craigslist": dict(zip([1, 4, 7, 10, 13, 16, 19, 22], [6.72, 19.61, 19.61, 6.9, 3.86, 2.46, 2, 2])),
    "Multi-character": dict(zip([1, 4, 7, 10, 13, 16, 19], [7.3, 19.96, 19.076, 7.16, 4.71, 4, 3])),
}
colors = {"ShareGPT": ps.NAVY, "ReMeDi": ps.RED, "Craigslist": ps.TEAL, "Multi-character": ps.OCHRE}
group_turns = list(range(1, 41, 3))
bar_w = 0.6
fig, ax = plt.subplots(figsize=(2.32, 1.6))
for i, name in enumerate(final_results):
    series = final_results[name]
    y = [series.get(t, np.nan) for t in group_turns]
    xo = np.array(group_turns) + (i - 1.5) * bar_w
    ax.bar(xo, y, width=bar_w, color=colors[name], alpha=0.45, lw=0, zorder=2)
    ax.plot(xo, y, color=colors[name], lw=1.1, marker="o", ms=2.2, zorder=3,
            ls="-" if name in ("ShareGPT", "ReMeDi") else (0, (3, 1.5)), label=name)
ax.set_yscale("log")
ax.set_xlim(-1, 37)
ax.xaxis.set_major_locator(FixedLocator([1, 7, 13, 19, 25, 31, 37]))
ax.set_xlabel("Turn number", labelpad=1.5)
ax.set_ylabel("Rel. avg. tokens (×turn 1)", labelpad=1.5)
ax.yaxis.set_minor_formatter(NullFormatter())
ax.legend(loc="upper right", handlelength=1.8, handletextpad=0.4, borderaxespad=0.1, labelspacing=0.25)
fig.tight_layout(pad=0.2)
save(fig, "long_tail")

# ---------------- Fig. 3: throughput per dialogue, tokens/s (cell 47) ----------------
methods = ["Original", "Surrogate", "History-Prefix", "History-FT", "SOMA"]   # M0..M3, Ours
datasets = ["ShareGPT", "ReMeDi", "Craigslist", "Multi-Char", "MATH", "MT-Bench"]
llama = np.array([  # rows = datasets, cols = methods
    [18.910526, 74.345804, 66.911224, 72.858888, 70.628514],
    [19.844837, 82.188585, 73.969727, 80.544813, 78.079155],
    [19.904177, 71.564385, 64.407947, 70.133097, 67.986166],
    [19.943957, 71.385788, 64.247209, 69.958072, 67.816499],
    [19.956733, 82.620348, 74.358313, 80.967941, 78.489331],
    [19.976748, 71.549102, 64.394192, 70.118120, 67.971647]])
qwen = np.array([
    [73.382851, 251.779826, 226.601843, 246.244229, 239.190835],
    [82.038648, 267.890163, 241.101147, 262.532360, 254.495655],
    [69.957222, 260.127796, 234.115016, 254.925240, 247.121406],
    [69.835743, 260.350324, 234.315292, 255.143318, 247.332808],
    [80.622339, 265.328229, 238.795406, 259.021664, 252.061818],
    [69.564893, 258.066661, 232.259995, 252.905328, 245.163328]])
for name, data, ylim in (("llama_through", llama, (10, 400)), ("qwen_through", qwen, (40, 1500))):
    fig, ax = plt.subplots(figsize=(2.45, 1.6))
    x = np.arange(len(datasets)); w = 0.16
    for j, m in enumerate(methods):
        ax.bar(x + (j - 2) * w, data[:, j], width=w, color=ps.METHOD_COLOR[m], edgecolor="#1A1A1A", lw=0.35,
               hatch="////" if m == "SOMA" else None, label=m, zorder=2)
    ax.set_yscale("log"); ax.set_ylim(*ylim)
    ax.set_xticks(x); ax.set_xticklabels(datasets, rotation=30, ha="right", rotation_mode="anchor", fontsize=6.8)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Throughput (tokens/s)", labelpad=1.5)
    ax.yaxis.set_minor_formatter(NullFormatter())
    ps.ygrid(ax)
    ax.legend(loc="upper left", ncol=3, fontsize=6.3, handlelength=1.1, handletextpad=0.3, columnspacing=0.6,
              borderaxespad=0.05, labelspacing=0.2)
    fig.tight_layout(pad=0.2)
    save(fig, name)

# ---------------- appendix: average tokens per dialogue (cell 53) ----------------
tm = ["RouteLLM", "Original", "Surrogate", "History-Prefix", "History-FT", "LLMLingua-2", "SOMA"]
llama_means = np.array([1.55, 1.45, 1.10, 1.21, 1.08, 0.97, 0.90]) * 1e4
qwen_means = np.array([1.83, 1.72, 1.57, 1.46, 1.41, 1.33, 1.23]) * 1e4
fig, ax = plt.subplots(figsize=(3.3, 1.9))
x = np.arange(len(tm)); w = 0.34
ax.bar(x - w / 2, llama_means, width=w, color=ps.SLATE_D, label="LLaMA", zorder=2)
ax.bar(x + w / 2, qwen_means, width=w, color=ps.SLATE_L, label="Qwen", zorder=2)
ax.set_yscale("log"); ax.set_ylim(8.5e3, 2.1e4)
ax.yaxis.set_major_locator(FixedLocator([1e4, 1.5e4, 2e4]))
ax.set_yticklabels(["1.0", "1.5", "2.0"]); ax.yaxis.set_minor_locator(NullLocator())
ax.set_ylabel("Avg. tokens per dialogue (×$10^4$)", labelpad=1.5)
ax.set_xticks(x); ax.set_xticklabels(tm, rotation=22, ha="right", rotation_mode="anchor", fontsize=7.2)
ax.tick_params(axis="x", length=0)
ps.ygrid(ax)
ax.legend(loc="upper right", handlelength=1.2)
fig.tight_layout(pad=0.2)
save(fig, "overall_avg_token")
print("wrote long_tail, llama_through, qwen_through, overall_avg_token")
