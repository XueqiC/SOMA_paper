# SOMA: Efficient Multi-turn LLM Serving via Small Language Model

LaTeX source of the SOMA paper, formatted for **ICLR 2027** (double-blind submission).

## Build

```bash
latexmk -pdf main.tex
```

Requires `pdflatex` + `bibtex`. The ICLR 2027 style files
(`iclr2027_conference.sty/.bst`, `fancyhdr.sty`, `natbib.sty`) are included as
shipped by the conference; do not modify them.

## Layout

- `main.tex` — preamble, title, abstract, section includes
- `introduction.tex`, `prelim.tex`, `method_new.tex`, `theory_new.tex`,
  `experiment_new.tex`, `conclusion.tex` — main text (9-page limit)
- `statements.tex` — AI use statement, Ethics statement, Reproducibility
  statement (end of main text, before references; not counted toward the limit)
- `appendix.tex` — appendices
- `ref.bib`, `figure/` — bibliography and figures

## Camera-ready

Uncomment `\iclrfinalcopy` in `main.tex` and fill in the `\author{}` block.
The author block is intentionally absent from the submission source.
