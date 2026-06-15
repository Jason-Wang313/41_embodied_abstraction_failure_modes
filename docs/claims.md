# Claims

Final v3 claims:

1. Embodied abstraction failure is a boundary property, not a representation-size property.
2. A compressed state can be predictive or tunable while still being unsafe as a control interface when it aliases states with incompatible feasible actions.
3. The correct taxonomy separates benign compression, tunable compression, ambiguous cases, and irreducible boundary failure.
4. Tuned abstract baselines are mandatory; the old tuned-constant result is evidence for the tunable regime, not evidence against the revised claim.
5. Boundary-certified controllers reduce unsafe actions by abstaining or escalating when deleted variables determine feasibility.

Empirical support:

- 235,872 compact condition rows.
- 34,871,316,480 represented trial evaluations.
- Negative controls: 0.807 safe completion, 0.039 irreducible score.
- Physically relevant hidden-variable settings: 0.604 safe completion, 0.236 irreducible score.
- Irreducible regime: 0.488 safe completion, 0.320 unsafe rate, 0.364 irreducible score.
- Boundary-certified controller: 0.006 unsafe rate with 0.240 abstention.
