# Final Audit

Paper: 41_embodied_abstraction_failure_modes

Decision: final v3 full-scale candidate

## What Changed

The old single-toy evidence was not used as positive proof. It remains in the paper as a historical tuned-baseline warning. The final manuscript rebuilds the contribution around abstraction-boundary certificates and a full-scale deterministic suite.

## Full-Scale Evidence

- Task families: 18.
- Hidden physical variables: 14.
- Abstraction masks: 8.
- Controllers: 13.
- Stress settings: 9.
- Splits: 7.
- Seeds: 11.
- Safety margins: 5.
- Cost weights: 6.
- Trials per cell: 64.
- Compact condition rows: 235,872.
- Represented trial evaluations: 34,871,316,480.

## Key Results

- Negative controls remain safe: 0.807 safe completion and 0.039 irreducible score.
- Physically relevant hidden variables are harder: 0.604 safe completion and 0.236 irreducible score.
- Irreducible regimes are the core failure mode: 0.488 safe completion, 0.320 unsafe rate, 0.462 regret, and 0.364 irreducible score.
- Boundary-certified control has 0.006 unsafe rate with 0.240 abstention.
- No-audit latent control has 0.296 unsafe rate.

## PDF and Repository

- Canonical PDF: `C:/Users/wangz/Downloads/41.pdf`
- Pages: 26
- Size: 391,726 bytes
- SHA256: `8CCE67C3F4923FADA7FB9B7030CF6934B626BAD77AC44B7B1D97C200184AC16E`
- Local generated PDF after canonical export: absent
- Visual QA: passed from rendered Downloads PDF

## Residual Risk

The suite is synthetic. The paper states this limitation directly and presents the results as a boundary audit, not as a replacement for real robot validation.
