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
- Final PDF SHA256: `8CCE67C3F4923FADA7FB9B7030CF6934B626BAD77AC44B7B1D97C200184AC16E`.
