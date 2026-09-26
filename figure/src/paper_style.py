"""Shared matplotlib style for the SOMA paper's data figures.

High-contrast house style in the spirit of figures4papers (top/right spines off, frameless
legends, explicit limits, consistent weights), set in the paper's serif face so figure text
matches the body: Times New Roman, bold, black text. Palette = the colour-blind-checked set
used in Figures 2 and 5 (navy = original model F, ochre = surrogate G, teal = SOMA/trained,
muted red = contrast), plus neutral grays for other baselines.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 2026-09-26: one muted, low-saturation palette for every figure in the paper (author request)
# 2026-09-26 (2nd pass): palette taken from the author's overview figure (teacher tan, student teal, trainable violet, rollback brick, slate neutrals)
NAVY, OCHRE, TEAL, RED = "#B89A6C", "#B7C7C3", "#4E9588", "#B25E59"   # NAVY = Original/teacher colour, OCHRE = Surrogate
GRAY_L, GRAY_M, GRAY_D = "#CFCFCF", "#9A9A9A", "#5E5E5E"
SLATE_D, SLATE_L = "#46586B", "#A9B6C4"
INK, GRID = "#1E2A2F", "#E4E8E7"

# ---- one colour and one marker per method, shared by every figure in the paper ----
# The two history baselines use grays that also read as lines and as caption text.
METHOD_COLOR = {
    "Original": NAVY, "Surrogate": OCHRE, "History-Prefix": "#8A9D99", "History-FT": "#4F5F63",
    "LLMLingua-2": "#C9C0DC", "RouteLLM": "#E3D6BF", "SOMA": TEAL,
}
METHOD_MARKER = {
    "Original": "s", "Surrogate": "^", "History-Prefix": "v", "History-FT": "D",
    "LLMLingua-2": "P", "RouteLLM": "X", "SOMA": "o",
}
SOMA_HATCH = "////"                        # SOMA bars are teal and hatched everywhere
TEAL_D = "#2F6A60"                         # dark teal for SOMA text labels
SOMA_VARIANT = {"SOMA": TEAL, "SOMA w/o ADL": "#84B4A7", "SOMA w/o ExpW+ADL": "#C6DDD5"}  # ablations: teal tints
DEGRADED = RED                             # conditions that remove context or rollback (no history, no rollback)
DEGRADED_MARKER = "v"

# ---- one colour and one marker per dataset (palette checked with the dataviz validator:
#      chroma, lightness and adjacent CVD separation pass; mustard needs markers/legend relief) ----
DATASET_COLOR = {
    "ShareGPT": "#8474B3", "ReMeDi": "#4E9588", "Craigslist": "#B89A6C",
    "Multi-Char": "#86AECB", "MATH": "#B25E59", "MT-Bench": "#3F5560",
}
DATASET_COLOR["Multi-Character"] = DATASET_COLOR["Multi-Char"]
DATASET_MARKER = {
    "ShareGPT": "o", "ReMeDi": "s", "Craigslist": "^", "Multi-Char": "D", "MATH": "v", "MT-Bench": "P",
}
DATASET_MARKER["Multi-Character"] = DATASET_MARKER["Multi-Char"]

def apply():
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix", "mathtext.default": "bf",
        "font.size": 8, "font.weight": "bold", "axes.labelsize": 8.5, "axes.labelweight": "bold",
        "axes.labelcolor": INK, "text.color": INK, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "xtick.color": INK, "ytick.color": INK, "legend.fontsize": 7, "legend.frameon": False,
        "axes.edgecolor": "#1A1A1A", "axes.linewidth": 0.8, "xtick.major.width": 0.8,
        "ytick.major.width": 0.8, "xtick.minor.width": 0.5, "ytick.minor.width": 0.5,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300,
    })

def ygrid(ax):
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)
