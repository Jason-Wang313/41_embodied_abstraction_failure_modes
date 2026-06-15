# Full-Scale Abstraction Boundary Suite

Status: complete.

This directory contains the Paper 41 full-scale v3 experiment outputs. The suite evaluates 18 task families, 14 hidden physical variables, 8 abstraction masks, 13 controllers, and 9 stress settings. The compact condition table has 235,872 rows and represents 34,871,316,480 trial evaluations after splits, seeds, safety margins, cost weights, and repeated trials.

The suite keeps the old tuned-constant falsification as a negative result. It now distinguishes benign/tunable abstraction from irreducible boundary failure.

Key files:

- `condition_metrics.csv`: compact condition-level metrics.
- `controller_summary.csv`: controller aggregates.
- `mask_summary.csv`: abstraction-mask ablations.
- `task_summary.csv`: task-family aggregates.
- `hidden_variable_summary.csv`: hidden-variable aggregates.
- `stress_summary.csv`: OOD/stress aggregates.
- `regime_summary.csv`: benign, tunable, ambiguous, and irreducible regimes.
- `negative_control_summary.csv`: physically irrelevant hidden-variable controls.
- `table_*.tex`: LaTeX tables included in the manuscript.
