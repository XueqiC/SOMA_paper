# Revision notes — ICLR 2027 submission (from the NeurIPS 2026 reviews)

All *added or rewritten* text is wrapped in `\rev{...}` and renders in **red**.
Set `\newcommand{\rev}[1]{#1}` in `main.tex` before submission to remove the color.
Deletions cannot be shown in red; they are listed below.

Main text is exactly 9 pages (ends at the bottom of page 9). Any further edit to the
main text needs a recompile and a page check.

## What changed (main text)

| Where | Change | Addresses |
|---|---|---|
| Abstract | "Extensive experiments show the effectiveness" → six benchmarks, preserves responses, reduces cost *for medium-to-long, locally coherent sessions* | rf31 W6 (narrow claims) |
| Intro §1 | grammar fix "openings that set the issues and anchors of a conversation" | S22Q minor L45 |
| Method §3.1 | targets $a_t^F$ generated once in the warm-start window and kept fixed; $F$ never re-queried during optimization (→ App. Design Rationale) | CFB7 W4/Q2 |
| Method §3.3 | Random-FT no longer presented as a baseline; sentence now says SOMA trains on the least-aligned turns instead of all/random turns | CFB7 W3/Q1 |
| Method §3.3 | drift statistic is continuous → gradual drift lowers it monotonically and triggers rollback once the margin is exhausted | iJGX Q2 |
| Theory §4 opening | "effective *because* later turns remain tied … not because they are intrinsically *easier than early ones*"; theory characterizes operating conditions, does not claim advantage over other mining strategies | S22Q L222, CFB7 W5, rf31 W5 |
| Theory §4.2 end | "very short / medium-to-long" → 1–4 turns vs ≥5 turns, pointing to Table 3 | S22Q L259 |
| Exp §5 Datasets/Models/Implementation | pointers to App. C.1 (filtering), C.3 (baselines), C.2 (hyperparameter ranges); Random-FT sentence removed | S22Q, CFB7 |
| Exp §5 Metrics | latency = end-to-end wall-clock incl. mining + LoRA + gating; **all models served with vLLM 0.10.2 with automatic prefix caching enabled** | AC①, AC③, S22Q Q1, rf31 Q3, CFB7 Q9 |
| Exp RQ3 | "very short / medium / long" → numeric buckets from Table 3 | S22Q L259 |
| Exp RQ5 | "most of the loss is recovered / false rollback low" → within 2.1–2.6 pts of clean, 88.9–90.8% detection, 3.8–4.3% false rollback | S22Q L343 |
| Conclusion | claim narrowed; **Limitations paragraph added to the main text** | rf31 W6, S22Q |

## What changed (appendix; no page limit)

- **Related Work**: CachedAttention named explicitly (was cited as gao2024cost only); added LoopServe, FlowKV, Router-R1, Temp-LoRA, StreamAdapter, S-LoRA; new paragraph on why prefix/KV caching is orthogonal to SOMA and on test-time adaptation vs. cross-model distillation (iJGX W2/Q3, rf31 W4/Q3, CFB7 strengths).
- **Related Work — Local Manifold Approximation**: the survey of classical manifold methods is replaced by a scoped statement of what "local manifold" means here and what it does not (no intrinsic dimension, tangent spaces, geodesics) (CFB7 W6). Dropped citations: coifman2006diffusion, sun2020zernet, xiong2020loco, zeng2021contrastive, fang2025non, van2008visualizing, mcinnes2018umap, ngo2023enhancing.
- **Implementation of LLM Judge**: prompt attribution corrected — adapted from MT-Bench / MT-Bench-101 single-answer grading; the reference-based framing and the 0–1 scale are ours; three judges averaged (S22Q).
- **New section "Design Rationale and Serving Considerations"**: why soft prompts / why adversarial (CFB7 Q4, Q5); relation to divergence-weighted History-FT and Random-FT (CFB7 W1–W3, AC②); sensitivity vs. divergence and the perturbation space, stated as assumptions (CFB7 Q6, Q7); number of $F$ calls and target consistency (CFB7 Q2); drift detection and what Cor. 4.3 does and does not guarantee (CFB7 Q8, iJGX Q2); adapter size and multi-adapter serving (rf31 Q1).
- **Limitations**: gradual drift only indirectly tested; no head-to-head against divergence-weighted History-FT / Random-FT.
- The old appendix section "LLM Usage" was removed earlier (superseded by the ICLR AI-use statement).

## Deletions (to fit 9 pages; not visible in red)

1. Intro §1: "Existing research reveals that multi-turn interactions are widespread, underscoring the need for serving systems capable of handling extended conversations in a context-aware manner~\citep{chen2024sharegpt4v, gao2024cost}."
2. Intro §1: "…compounding the difficulty of maintaining coherence *in multi-turn settings*" → trailing phrase dropped.
3. Intro §3: "Extensive experiments show the effectiveness of our proposed method." and "Together, these components allow the small model to effectively approximate the larger model's reasoning process within the context of a given session, enabling both cost-effective and context-aware multi-turn serving."
4. Prelim §2.3: "It adapts $G$ to match the local behavior of $F$ around the current dialogue prefix."
5. Theory §4.1: the displayed Gap equation is now inline; the "intended operating regime" paragraph condensed to one sentence.
6. Exp RQ1: "SOMA is designed as a drop-in replacement for large-model serving." and "The gap over History-Prefix shows that simply giving the small model more history is insufficient."
7. Exp RQ2: last sentence condensed ("Thus SOMA's gains are not only surface-level matching: …").
8. Exp RQ4: "In other words, SOMA works not only because it adapts the surrogate locally, but also because it mines more informative weak-alignment directions before adaptation."; anti-degeneration sentence condensed.
9. Exp RQ5: first sentence condensed to "We next test when SOMA's locality assumption holds and how rollback helps when it fails."
10. Figure 2 / Table 4 captions shortened; Figure 2 subfigures 0.42/0.54 → 0.37/0.48 width; Table 1 0.96\textwidth; Table 2 0.72\textwidth; Table 4 subtables 0.41/0.52; Figure 1 wrapfigure 14 lines / 0.42\textwidth and anchored one paragraph later.

## Open items that need an author's confirmation

- **Table 3**: which model pair (LLaMA?) — the caption still does not say.
- **Prefix caching**: the statement "all models are served with vLLM 0.10.2 with automatic prefix caching enabled" is based on the vLLM runs found on LONI (`/work/xueqic/LLM`, `enable_prefix_caching=True`, vLLM 0.10.2). Confirm this holds for every reported efficiency number, including the SOMA runs.
- **$F$ targets fixed during mining**: based on the released reference implementation (`soma/pipeline.py`, `prompt_mining.py`). Confirm the experiments did the same; §3.1 still formulates $a_t^F = F(V(\mathbf P)\oplus\cdots)$.
- **Hardware inconsistency** (pre-existing): App. C.2 says "one node with 4×80G A100 GPUs", App. C.6 says "a server equipped with Nvidia A6000 GPUs".
- **LoRA targets inconsistency** (pre-existing): §3.3 says "attention and MLP projections"; App. C.2 says "LoRA on attention projections".
- Random-FT / divergence-weighted History-FT / prompt-length ablation / judge agreement / per-dataset break-even: **not added** (no logs found that align with the paper's numbers; new runs would involve Qwen/DeepSeek).
