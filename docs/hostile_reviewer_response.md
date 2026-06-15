# Hostile Reviewer Response

## Strongest Attack

The strongest attack on the old draft was correct: the original abstract controller was weak, and a tuned constant abstraction reached 0.987 held-out success.

## Final Response

The final v3 paper accepts that attack and uses it as a design constraint. Tuned constant, tuned visible linear, and tuned visible quadratic baselines are included from the start. The revised claim is only about regimes where the compressed interface aliases states with incompatible safe actions.

## Evidence That The Attack Is Addressed

- Tunable regimes are reported as positive abstraction cases, not failures.
- Negative controls are included.
- Irreducible regimes are separated from tunable regimes.
- The boundary-certified controller is evaluated against tuned abstract baselines and no-audit latent control.
- The old tuned-constant result appears in the manuscript as a reconciliation table.
