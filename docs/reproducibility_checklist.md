# Reproducibility Checklist

## Commands

Run the full-scale suite:

```powershell
python tools/run_full_scale_abstraction_boundary_suite.py
```

Build the canonical PDF:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

## Expected Outputs

- `results/full_scale/condition_metrics.csv`
- `results/full_scale/controller_summary.csv`
- `results/full_scale/mask_summary.csv`
- `results/full_scale/task_summary.csv`
- `results/full_scale/hidden_variable_summary.csv`
- `results/full_scale/stress_summary.csv`
- `results/full_scale/regime_summary.csv`
- `results/full_scale/negative_control_summary.csv`
- `results/full_scale/experiment_validation.json`
- `figures/full_scale/*.pdf`
- `C:/Users/wangz/Downloads/41.pdf`

## Validation

- Expected condition rows: 235,872.
- Actual condition rows: 235,872.
- Represented trial evaluations: 34,871,316,480.
- Final PDF pages: 26.
- Final PDF SHA256: `9334E545BBDB8218703B8E53A8E15C410DE2BF0D4C9968A6CE77E1C4A0C39DEE`.
- Link-box QA: affected pages 6, 7, 10, 12, 13, 16, and 17 rendered at 160 dpi after rebuild; green citation boxes and red internal-reference boxes match the VLA-style boxed annotation target.
