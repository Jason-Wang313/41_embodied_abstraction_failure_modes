# Embodied Abstraction Failure Modes

Recovered paper 41 in the robotics 60-paper batch.

## Contents

- `main.tex` and `main.pdf`: ICLR-style paper source and built PDF.
- `outputs/toy_abstraction_failure.png`: toy experiment figure used in the paper.
- `outputs/toy_experiment_stats.json`: measured toy results.
- `docs/`: literature matrix, novelty notes, reviewer attacks, and final audit.
- `tools/`: scripts used to gather literature and run the toy experiment.

## Build

Run:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The recovered build produced `main.pdf` with 4 pages.
