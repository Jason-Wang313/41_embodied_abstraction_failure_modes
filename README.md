# Embodied Abstraction Failure Modes

Paper 41 in the robotics 60-paper batch.

## V3 Full-Scale Status

Status: final v3 full-scale manuscript.

Canonical PDF: `C:/Users/wangz/Downloads/41.pdf`

- Pages: 26
- File size: 391,726 bytes
- SHA256: `9334E545BBDB8218703B8E53A8E15C410DE2BF0D4C9968A6CE77E1C4A0C39DEE`
- Local `main.pdf` after canonical build: absent
- Visual render check: passed
- VLA-style link-box check: passed on pages 6, 7, 10, 12, 13, 16, and 17

## Core Result

The old tuned-constant counterexample is retained as a historical negative result and reclassified as a tunable abstraction regime. The final v3 paper now tests the stronger claim: abstraction boundaries fail when a compressed state aliases physical states that require incompatible safe actions.

The full-scale suite evaluates 18 task families, 14 hidden physical variables, 8 abstraction masks, 13 controllers, and 9 stress settings. It writes 235,872 compact condition rows and represents 34,871,316,480 trial evaluations after splits, seeds, margins, cost weights, and repeated trials.

## Key Artifacts

- `main.tex`: final ICLR-style manuscript.
- `tools/run_full_scale_abstraction_boundary_suite.py`: deterministic full-scale runner.
- `results/full_scale/`: aggregate metrics, validation JSON, and LaTeX tables.
- `figures/full_scale/`: manuscript figures generated from aggregates.
- `docs/full_scale_execution_plan.md`: pre-edit plan and execution outcome.
- `docs/`: claims, audits, reviewer attacks, reproducibility notes, and readiness decision.

## Reproduce

Run the full-scale suite:

```powershell
python tools/run_full_scale_abstraction_boundary_suite.py
```

Build the canonical PDF:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```
