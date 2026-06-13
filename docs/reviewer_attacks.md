# Reviewer Attacks

1. This is just a restatement of partial observability.
2. The toy evidence may not generalize to real robots.
3. The paper claims novelty but only repackages existing abstraction and hierarchical RL ideas.
4. The boundary audit may be descriptive rather than prescriptive.
5. Physical variables are obvious in hindsight; the paper may not prove they were missing from prior abstractions.
6. The evidence may not establish a causal link between deleted variables and failure.
7. The abstract baseline may simply be badly tuned.

## V2 outcome

Attack 7 succeeds. A tuned constant abstraction selected on training trials reaches 0.987 held-out success, while the full-state controller reaches 0.962. The current toy therefore does not establish the paper's central causal mechanism.
