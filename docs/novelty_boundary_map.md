# Novelty Boundary Map

## Hypothesis Under Test
High-level abstractions often fail in embodied robotics when they delete variables that remain causally necessary for physical success.

## Hidden Assumptions to Attack
- The abstraction is Markov for the downstream controller.
- Contact variables can be ignored once a symbolic task label is known.
- Latent dynamics trained on average behavior remain valid under rare but decisive contacts.
- The planner can recover from abstraction-induced aliasing through replanning alone.
- Dataset coverage is enough to discover all physically relevant variables.
- Sim-to-real error is mostly parametric rather than structural.
- Task success depends only on goal state, not on intermediate physical regimes.
- Hierarchical decomposition preserves the variables needed at lower levels.
- Observations are rich enough that abstraction can safely compress them.
- Failure probability is dominated by model error rather than state deletion.

## Stronger Candidate Direction
A boundary-audit mechanism that detects when an abstraction has dropped a variable that controls future feasibility, then forces the paper to expose the missing variable rather than claiming generic robustness.

## Why It Is Different
- Focuses on abstraction boundary validity, not just better latent modeling.
- Treats omitted variables as the central failure mechanism.
- Requires explicit evidence that variable deletion changes physical success.