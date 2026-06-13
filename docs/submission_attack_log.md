# Submission Attack Log

## Attack: under-tuned abstract controller

Question: Does the toy still show abstraction failure if the abstract controller is tuned on training trials?

Result: no. A tuned constant squeeze reaches 0.987 held-out success, higher than the full-state controller's 0.962.

Decision impact: fatal. The generated paper should be archived.

## Attack: causal variable deletion

Question: Does failure require deleted hidden friction/load variables?

Result: not in the current toy. A controller with no hidden-variable access can solve the held-out task.

Decision impact: fatal for the current empirical claim.

## Attack: submission readiness

Question: Can the paper be sent as a workshop claim with an honest limitation?

Result: no. The primary evidence contradicts the draft's central claim after hardening.

Decision impact: kill/archive.
