# Embodied Abstraction Failure Modes

Paper 41 in the robotics 60-paper batch.

## V2 hardening decision

Decision: kill/archive.

The original toy result supported the draft only when the abstract controller was fixed badly. A v2 tuned-abstraction stress selects an abstract constant squeeze on training trials and reaches 0.987 held-out success, exceeding the full-state controller's 0.962. The generated paper is therefore archived as a failed submission candidate, not treated as a workshop-ready claim.

Canonical PDF: `C:/Users/wangz/Downloads/41.pdf`

## Contents

- `main.tex`: ICLR-style paper source with the v2 archive notice.
- `outputs/toy_abstraction_failure.png`: original toy experiment figure.
- `outputs/toy_experiment_stats.json`: original toy results.
- `docs/tuned_abstraction_stress.csv`: v2 stress-test results.
- `docs/`: literature matrix, novelty notes, reviewer attacks, and final audit.
- `tools/`: scripts used to gather literature and run the toy and stress experiments.

## Reproduce

Run the original toy experiment:

```powershell
python tools/run_toy_experiment.py
```

Run the v2 tuned-abstraction stress:

```powershell
python tools/run_toy_experiment.py --stress-only
```

Build the canonical PDF:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```
