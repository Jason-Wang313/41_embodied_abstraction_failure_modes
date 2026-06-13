# Final Audit

Paper: 41_embodied_abstraction_failure_modes

Decision: kill/archive

Submission-hardening version: v2

## Original positive evidence

- Original full-state controller success: 0.963.
- Original abstract controller success: 0.197.
- Original success gap: 0.766.
- Original interpretation: deleting hidden friction/load variables caused physical failure.

## V2 falsification

- Tuned constant abstract controller: 0.988 train success, 0.987 held-out success.
- Tuned visible-goal abstract controller: 0.988 train success, 0.987 held-out success.
- Full-state controller: 0.959 train success, 0.962 held-out success.
- The tuned constant abstraction beats the full-state controller on held-out trials.

## Audit judgment

The central toy evidence is invalid as support for the paper's thesis. The generated draft mostly demonstrated that one fixed abstract policy was poorly tuned, not that the abstraction deleted a necessary physical variable. The broader boundary-audit idea may still be useful, but this repository no longer contains a defensible submission claim.

## Artifacts

- Paper source: `main.tex`
- Original experiment: `tools/run_toy_experiment.py`
- V2 stress results: `docs/tuned_abstraction_stress.csv`
- V2 stress table: `docs/tuned_abstraction_stress_table.tex`
- Original figure: `outputs/toy_abstraction_failure.png`
- Original stats: `outputs/toy_experiment_stats.json`
- Build wrapper: `scripts/build_pdf.ps1`

## PDF and repository

- Canonical PDF: `C:/Users/wangz/Downloads/41.pdf`
- Local tracked/generated PDF: removed after build
- Desktop copy: absent
- GitHub URL: `https://github.com/Jason-Wang313/41_embodied_abstraction_failure_modes`
