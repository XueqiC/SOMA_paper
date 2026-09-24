# Revision notes — ICLR 2027 submission (from the NeurIPS 2026 reviews)

All *added or rewritten* text is wrapped in `\rev{...}` and renders in **red**.
Set `\newcommand{\rev}[1]{#1}` in `main.tex` before submission to remove the color.
Deletions cannot be shown in red; they are listed below.

Layout as of this revision: main text is exactly 9 pages (ends at the bottom of page 9,
zero slack); Section 5 (experiments) begins on page 7 (no forced page break; the user later
asked not to force it). Any further edit needs a recompile and a page check.

## Round 2 — restructuring (2026-09-23, evening)

- **Limitations** moved back to the appendix (Appendix I); the conclusion ends with a
  one-line pointer.
- **Theory (Section 4) compressed.** The main text keeps only the acceptance bound
  (Theorem 4.1), the net-gain equation (Eq. 5), and a short paragraph on the candidate
  count. Full statements now live in Appendix E as proper environments: Lemma E.1
  (warm-start generalization), Corollary E.2 (switching rule), Theorem E.3 (coverage),
  Lemma E.4 (directional suboptimality), Corollary E.5 (candidate budget). The
  displayed cost decomposition `C_SOMA` was folded into the net-gain equation.
- **Experiments enriched from the appendix.** Now in the main text: Table 2 (Qwen
  response similarity), Figure 2 (throughput, both families), Figure 3 (LLaMA ablation,
  Qwen ablation, MT-Bench-101 ability profile), Figure 4 (warm-start switching
  behavior). The old token-usage panel moved to Appendix F.1 next to the per-dataset
  token costs; the variance-concentration figure stays in the appendix.
- **Preliminaries rewritten** (Section 2) and **method prose polished** (Section 3):
  complete subject–verb sentences, shorter lead sentences, longer explanatory ones;
  all equations, the problem statement, Definition 3.1 and Theorem 3.2 are unchanged.
  These rewrites are *not* marked red (the user asked for red only on review-driven
  content changes); diff against commit `a86db29` to see them.
- **Space recovered**: three intro paragraphs condensed (long-tail motivation, "big head",
  SOMA pipeline description, contribution bullet 1); wrapfigure re-anchored at the
  "Figure 1 shows…" paragraph with 13 reserved lines and a shorter caption; Tables 1–2
  placed at page bottoms (`[!b]`), all other §5 floats `[!t]`; figure widths trimmed.
- Paragraph-final "dangling" lines: none shorter than 1/3 of the text width on pages 1–9
  (checked with a `pdftotext -bbox-layout` script).
- Follow-up (user feedback): all §5 floats are `[!t]` (tables/figures at page tops; Table 1
  therefore sits above the Section 5 heading on page 7), and the gap below §4.3 left by the
  page break was filled by restoring Theorem 4.2 (coverage) and one sentence in §4.1; the
  forced `\newpage` before Section 5 was then removed at the user's request.

## Round 11 — one colour and one marker per method and per dataset, in every figure (2026-09-24)

Scheme in `figure/src/paper_style.py`:
- Methods: Original navy ■, Surrogate ochre ▲, History-Prefix light gray ▼, History-FT dark gray ◆, LLMLingua-2 lavender, RouteLLM sand,
  SOMA teal ● (bars: teal + hatch). SOMA ablation variants are teal tints. Degraded conditions (no history, no rollback) are red ▼.
- Datasets: ShareGPT violet ●, ReMeDi green ■, Craigslist berry ▲, Multi-Char azure ◆, MATH mustard ▼, MT-Bench sienna ✚
  (palette checked with the dataviz validator; it avoids the method hues).
Changed figures (plotted values verified identical against the previous PDFs): Fig. 1, Fig. 3 (a–c), Fig. 4, Fig. 5 (a–c; caption key now uses
the marker glyphs), Fig. 6 (a, b), App. token-cost figure, App. variance figure. Figures 6 and the variance plot were re-rendered from the
notebook cells with fixed seeds (`notes/fig_cell5{0,1,4}_regen.py`); only colours and markers changed.

## Round 10 — references end on page 13 (2026-09-24)

- Dropped the GPT-2 citation (radford2019language) from the "GPT series" group in the introduction; GPT-3 and GPT-4 remain. The last
  reference no longer spills onto its own page, and the PDF is 24 pages. Main text unchanged (still exactly 9 pages).

## Round 9 — table captions state their takeaway (2026-09-24)

- Tables 1–3 captions each end with one red sentence stating what the table shows (SOMA best on all six datasets, 75.1→93.1 and +0.9 over RouteLLM on LLaMA;
  +27.1 over the surrogate on Qwen; 77–78% of the surrogate-to-original EM gap recovered on MATH). Notation tables left as is.
- To keep the main text at exactly 9 pages: shorter §4 opening, last clause of §4.2 dropped (RQ3 covers it), Proposition 4.1 ends at the certificate,
  §3.3 "compressed context" clause dropped (described in the next paragraph).

## Round 8 — theory corrected and narrative unified with the implementation (2026-09-24)

Details and verification: `../notes/theory_check_2026-09-24.md` (in the soma project repo).
- Removed Thm 3.2 (Directional Recovery); its proof was wrong (min vs. max, dimension mismatch, invalid linear-term cancellation).
- Problem 2.1 made computable (output-space gap over later states via a shared encoder) + the measurable prediction of the local view.
- §4.1: m-dependent effective sample size (Janson 2004); correct Hoeffding lemma; one acceptance proposition (absolute gap, held-out batch,
  locality premise) in both main text and App. E; main text states the reuse of warm-start turns and that γ_B (0.25) exceeds the thresholds.
- Coverage bound corrected (exact cap probability ½·I, valid lower bound, fixed budget proof); §4.3 moved to App. E, scoped to initial directions.
- r_t renamed and re-explained as an anchoring score (agreement surviving the adversarial probe) everywhere, including Figure 2 labels.
- §3.1: F never receives V(P); targets are the warm-start responses. Notation table updated.
- Main text still exactly 9 pages; floats unchanged (p7 Tables 1–3, p8 Figures 3–4, p9 Figures 5–6); no short last lines.

## Round 7 — author decisions on the consistency items (2026-09-24)

- **Figure 5(b)**: Qwen ReMeDi bars were 5 points too high (typo). Now SOMA 83.2 (= Table 2), w/o ADL 82.1,
  w/o ExpW+ADL 80.4; everything else in the panel is unchanged. Axis label "Precentage" → "Percentage" in
  both ablation panels.
- **App. F.1**: the average-tokens figure is removed; the paragraph cites only the per-dataset token figure
  (now Figure 9). "for both model families" and "unadapted surrogate" added to keep the last line long.
- **App. C.2**: hardware now "Nvidia A6000 GPUs" (red), consistent with C.6.
- **Figure 6(b)**: axis label "Precentage" → "Percentage" by editing only the label text in the PDF (plot not re-run; all drawing paths identical).
- Main text unchanged: still exactly 9 pages; no new short last lines.

## Round 6 — even float layout, main text fills 9 pages (2026-09-24)

- Experiment floats re-anchored so figure numbers follow the reading order and each results
  page carries a similar share of floats: page 7 Tables 1–3; page 8 Figure 3 (operating range
  and reliability) and Figure 4 (throughput); page 9 Figure 5 (ablation) and Figure 6 (warm-start).
- Section 2: the long-tail paragraph now notes that ShareGPT and ReMeDi peak at the opening turn
  while Craigslist and Multi-Character peak shortly after it (read off Figure 1); §2.3 states that
  the goal is a local rather than global match. A redundant clause was removed.
- Conclusion: two sentences added (red) on applicability to API-served F given access to G's
  embedding layer, and on when SOMA is most useful. The main text now ends at the bottom of page 9.

## Round 5 — figure styling pass (2026-09-24)

- Shared style module `figure/src/paper_style.py` (Times New Roman bold, black text, palette of
  Figures 2 and 5, figures4papers-style spines/legends). `figure/src/restyle_figs.py` re-renders
  Figure 1 (long tail), Figure 3 (throughput) and the appendix average-token figure with the
  values copied verbatim from `~/Dropbox/intern/test.ipynb` cells 13, 47, 53. Figure 3's y-axis
  now reads "Throughput (tokens/s)" (the old PDF said "Similarity Precentage"), and the Qwen panel's
  y-range no longer clips bars above 150.
- Figures 4 and 6 and the appendix variance figure are unchanged, per the author's request, until
  the measured arrays for the values the notebook computes at plot time are available
  (see `notes/figure_provenance.md`).
- Figure 2: darker text and borders, 12.5px labels; caption cut to about three lines.
- Appendix: every short paragraph ending fixed; question-style headings replaced by declarative
  phrases (Sections 4.1–4.3, RQ4/RQ5, appendix design-rationale heading).

## Round 4 — tables to figures (2026-09-23, night)

- Table 3 (MATH exact match) now spans the full text width.
- Former Table 4 (ShareGPT break-even) and Table 5 (reliability: MATH context dependency and
  topic-shift stress test) are replaced by one three-panel figure, Figure 5
  (`figure/operating.pdf`, generated by `figure/src/make_result_figs.py`): (a) saving vs.
  session length (latency and tokens), (b) MATH EM with vs. without history per turn bucket
  with the drop annotated, (c) a dot plot of similarity under a topic shift (no rollback,
  SOMA, no shift, with ± std) plus SOMA's detection / false-rollback rates. Every number is
  copied verbatim from the former tables; nothing was re-measured. All references now point
  to Figure 5(a)/(b)/(c) (theory §4.2, RQ3, RQ5, conclusion, appendix G and I).
- To stay at 9 pages: the §2.3 closing paragraph (superseded by the §3 four-step opening) was
  removed; the Figure 2 caption, the §4 opening, the §4.1/§4.2 openings, the switching-rule and
  candidate-count paragraphs, and two §3 implementation sentences were condensed. The
  warm-start switching figure panels are 0.40\textwidth instead of 0.42. Section 5 now starts
  at the bottom of page 6; no short paragraph endings on pages 1–9.

## Round 3 — method overview figure (2026-09-23, night; redrawn after user feedback)

- Figure 2 (`figure/overview.pdf`) at the start of Section 3, generated by
  `figure/src/make_overview.py` (SVG → PDF via cairosvg; `overview.png` is a preview).
- Second version (the first was judged too childish and without a clear storyline): one
  left-to-right pipeline of four numbered stages with the same terms as Section 3 —
  (1) Warm-start → context–reply pairs; (2) Soft-prompt mining on frozen G, with the three
  objective terms (neighborhood unlikelihood, expectation weighting, entropy regularizer)
  → hardness of each turn; (3) Localized LoRA (frozen weights + low-rank update on
  attention/MLP, hardness-weighted fit to F's replies) → adapted G; (4) Gated serving
  (fidelity + locality checks, summary + last K turns, drift monitor). A session timeline
  underneath is aligned with the stages and ends in a rollback loop back to step 1.
  Muted academic palette (navy F, ochre G, teal = trained, muted red = drift, grays),
  checked for colour-blind separation with the dataviz validator; models drawn as
  layered blocks with a lock for frozen parameters; figure text ≥ 12px (≈ 6pt printed).
- Caption rewritten step by step; the Section 3 opening now lists the same four steps and
  points to the subsections that implement them.
- To make room (main text still exactly 9 pages): Theorem 4.2 (coverage) statement moved
  back to Appendix E (main text keeps a one-paragraph summary with the budget); the §5
  Implementation paragraph is condensed; the §4.1 "short but context-dependent turns"
  sentence was dropped again. Figure 1 (long tail) is re-anchored at the start of §2.2 with
  14 reserved lines so it no longer spills onto page 3.
- All paragraph endings re-checked: none shorter than 1/3 of the line on pages 1–9.

## Round 1 — review-driven wording (main text)

| Where | Change | Addresses |
|---|---|---|
| Abstract | "Extensive experiments show the effectiveness" → six benchmarks, preserves responses, reduces cost *for medium-to-long, locally coherent sessions* | rf31 W6 (narrow claims) |
| Intro §1 | grammar fix "openings that set the issues and anchors of a conversation" | S22Q minor L45 |
| Method §3.1 | targets $a_t^F$ generated once in the warm-start window and kept fixed; $F$ never re-queried during optimization (→ App. G) | CFB7 W4/Q2 |
| Method §3.3 | Random-FT no longer presented as a baseline; sentence now says SOMA trains on the least-aligned turns instead of all/random turns | CFB7 W3/Q1 |
| Method §3.3 | drift statistic is continuous → gradual drift lowers it monotonically and triggers rollback once the margin is exhausted | iJGX Q2 |
| Theory §4 opening | "effective *because* later turns remain tied … not because they are intrinsically *easier than early ones*"; theory characterizes operating conditions, does not claim advantage over other mining strategies | S22Q L222, CFB7 W5, rf31 W5 |
| Theory §4.2 end | "very short / medium-to-long" → 1–4 turns vs ≥5 turns, pointing to Table 4 | S22Q L259 |
| Exp §5 Datasets/Models/Implementation | pointers to App. C.1 (filtering), C.3 (baselines), C.2 (hyperparameter ranges); Random-FT sentence removed | S22Q, CFB7 |
| Exp §5 Metrics | latency = end-to-end wall-clock incl. mining + LoRA + gating; **all models served with vLLM 0.10.2 with automatic prefix caching enabled** | AC①, AC③, S22Q Q1, rf31 Q3, CFB7 Q9 |
| Exp RQ3 | "very short / medium / long" → numeric buckets from Table 4 | S22Q L259 |
| Exp RQ5 | "most of the loss is recovered / false rollback low" → within 2.1–2.6 pts of clean, 88.9–90.8% detection, 3.8–4.3% false rollback | S22Q L343 |
| Conclusion | claim narrowed | rf31 W6 |

## Round 1 — appendix (no page limit)

- **Related Work**: CachedAttention named explicitly (was cited as gao2024cost only); added LoopServe, FlowKV, Router-R1, Temp-LoRA, StreamAdapter, S-LoRA; new paragraph on why prefix/KV caching is orthogonal to SOMA and on test-time adaptation vs. cross-model distillation (iJGX W2/Q3, rf31 W4/Q3, CFB7 strengths).
- **Related Work — Local Manifold Approximation**: the survey of classical manifold methods is replaced by a scoped statement of what "local manifold" means here and what it does not (CFB7 W6). Dropped citations: coifman2006diffusion, sun2020zernet, xiong2020loco, zeng2021contrastive, fang2025non, van2008visualizing, mcinnes2018umap, ngo2023enhancing.
- **Implementation of LLM Judge**: prompt attribution corrected — adapted from MT-Bench / MT-Bench-101 single-answer grading; the reference-based framing and the 0–1 scale are ours; three judges averaged (S22Q).
- **New section "Design Rationale and Serving Considerations"** (Appendix G): why soft prompts / why adversarial (CFB7 Q4, Q5); relation to divergence-weighted History-FT and Random-FT (CFB7 W1–W3, AC②); sensitivity vs. divergence and the perturbation space, stated as assumptions (CFB7 Q6, Q7); number of $F$ calls and target consistency (CFB7 Q2); drift detection and what the switching corollary does and does not guarantee (CFB7 Q8, iJGX Q2); adapter size and multi-adapter serving (rf31 Q1).
- **Limitations** (Appendix I): gradual drift only indirectly tested; no head-to-head against divergence-weighted History-FT / Random-FT.
- The old appendix section "LLM Usage" was removed earlier (superseded by the ICLR AI-use statement).

## Deletions (to fit 9 pages; not visible in red)

1. Intro §1: "Existing research reveals that multi-turn interactions are widespread, underscoring the need for serving systems capable of handling extended conversations in a context-aware manner~\citep{chen2024sharegpt4v, gao2024cost}."
2. Intro §1: "…compounding the difficulty of maintaining coherence *in multi-turn settings*" → trailing phrase dropped; "…as it better reflects real-world usage scenarios" dropped.
3. Intro §3: "Extensive experiments show the effectiveness of our proposed method." and "Together, these components allow the small model to effectively approximate the larger model's reasoning process within the context of a given session, enabling both cost-effective and context-aware multi-turn serving."; the "big head" paragraph and the pipeline paragraph condensed (see Round 2).
4. Prelim §2.3: "It adapts $G$ to match the local behavior of $F$ around the current dialogue prefix."; §2.2 opening sentence "The cost of multi-turn serving depends on how the dialogue state evolves." dropped.
5. Theory §4: Lemma (warm-start), Corollary (switching rule), Lemma (suboptimality), Corollary (candidate budget) and Theorem (coverage) statements moved to Appendix E; the displayed Gap equation inlined; the "intended operating regime" paragraph condensed to one sentence.
6. Exp RQ1: "SOMA is designed as a drop-in replacement for large-model serving." and "The gap over History-Prefix shows that simply giving the small model more history is insufficient."
7. Exp RQ2: last sentence condensed ("Thus SOMA's gains are not only surface-level matching: …").
8. Exp RQ4: "In other words, SOMA works not only because it adapts the surrogate locally, but also because it mines more informative weak-alignment directions before adaptation."; anti-degeneration sentence condensed.
9. Exp RQ5: first sentence condensed; "This is exactly the setting SOMA is designed for." dropped.
10. Conclusion: method-summary sentence shortened ("It mines soft-prompt directions, distills them with LoRA, and switches only when alignment is sufficient.").
11. Captions of Figures 2–4 and Table 5 shortened; figure widths reduced.

## Open items that need an author's confirmation

- **Table 4 (break-even)**: which model pair (LLaMA?) — the caption still does not say.
- **Prefix caching**: the statement "all models are served with vLLM 0.10.2 with automatic prefix caching enabled" is based on the vLLM runs found on LONI (`/work/xueqic/LLM`, `enable_prefix_caching=True`, vLLM 0.10.2). Confirm this holds for every reported efficiency number, including the SOMA runs.
- **$F$ targets fixed during mining**: based on the released reference implementation (`soma/pipeline.py`, `prompt_mining.py`). Confirm the experiments did the same; §3.1 still formulates $a_t^F = F(V(\mathbf P)\oplus\cdots)$.
- ~~Hardware inconsistency~~: resolved in Round 7 (A6000 everywhere, per the author).
- ~~LoRA targets inconsistency~~: resolved in the consistency pass (C.2 now "attention and MLP"); the History-FT baseline's placement (C.3) stays as written, per the author.
- Random-FT / divergence-weighted History-FT / prompt-length ablation / judge agreement / per-dataset break-even: **not added** (no logs found that align with the paper's numbers; new runs would involve Qwen/DeepSeek).
