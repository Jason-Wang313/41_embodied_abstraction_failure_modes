# Novelty Decision

Chosen thesis: embodied abstraction failure is a boundary problem, not merely a representation-quality problem.

Decision: kill/archive after v2 hardening

Reasoning:
- The literature strongly supports abstractions, latent states, hierarchical policies, and world models.
- The weak point is not the existence of abstractions but whether they preserve physically necessary variables.
- The strongest feasible paper would be an audit-and-demonstration paper about variable deletion at abstraction boundaries.
- However, the generated toy evidence does not survive a tuned abstract baseline.
- A tuned constant abstract controller reaches 0.987 held-out success, exceeding the full-state controller's 0.962.
- The current draft should not be submitted because its central empirical support collapses.

Rejected weaker directions:
- bigger model
- better data
- new benchmark only
- add uncertainty
- add active learning
- add verifier
- combine two existing modules
- use an LLM as planner
- use reinforcement learning
