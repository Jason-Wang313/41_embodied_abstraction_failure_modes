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
- SHA256: `9334E545BBDB8218703B8E53A8E15C410DE2BF0D4C9968A6CE77E1C4A0C39DEE`
- Local generated PDF after canonical export: absent
- Visual QA: passed from rendered Downloads PDF
- VLA-style link-box QA: affected pages 6, 7, 10, 12, 13, 16, and 17 rendered at 160 dpi; verified 22 green citation boxes, 13 red internal-reference boxes, and 35 visible `(0, 0, 1)` borders with no visual collisions.

## Residual Risk

The suite is synthetic. The paper states this limitation directly and presents the results as a boundary audit, not as a replacement for real robot validation.
