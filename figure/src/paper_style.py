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

NAVY, OCHRE, TEAL, RED = "#3A62A0", "#D08A45", "#2A9D8F", "#B5454A"
GRAY_L, GRAY_M, GRAY_D = "#CFCFCF", "#9A9A9A", "#5E5E5E"
SLATE_D, SLATE_L = "#46586B", "#A9B6C4"
INK, GRID = "#000000", "#E3E3E3"

# ---- one colour and one marker per method, shared by every figure in the paper ----
# The two history baselines use grays that also read as lines and as caption text.
METHOD_COLOR = {
    "Original": NAVY, "Surrogate": OCHRE, "History-Prefix": "#A8A8A8", "History-FT": "#5E5E5E",
    "LLMLingua-2": "#B8AED6", "RouteLLM": "#E7CBA9", "SOMA": TEAL,
}
METHOD_MARKER = {
    "Original": "s", "Surrogate": "^", "History-Prefix": "v", "History-FT": "D",
    "LLMLingua-2": "P", "RouteLLM": "X", "SOMA": "o",
}
SOMA_HATCH = "////"                        # SOMA bars are teal and hatched everywhere
TEAL_D = "#1D6E64"                         # dark teal for SOMA text labels
SOMA_VARIANT = {"SOMA": TEAL, "SOMA w/o ADL": "#7FC4BA", "SOMA w/o ExpW+ADL": "#C4E5E0"}  # ablations: teal tints
DEGRADED = RED                             # conditions that remove context or rollback (no history, no rollback)
DEGRADED_MARKER = "v"

# ---- one colour and one marker per dataset (palette checked with the dataviz validator:
#      chroma, lightness and adjacent CVD separation pass; mustard needs markers/legend relief) ----
DATASET_COLOR = {
    "ShareGPT": "#6A4FB0", "ReMeDi": "#4E9A3A", "Craigslist": "#C44E8C",
    "Multi-Char": "#2C8FC9", "MATH": "#C99A1E", "MT-Bench": "#9A4F2A",
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
