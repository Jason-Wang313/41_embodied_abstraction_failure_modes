# Reviewer Attacks

1. This is just partial observability.
   Response: the paper narrows the question to whether a specific interface deletes variables that change feasible safe actions.

2. Tuned abstract policies may solve the task.
   Response: correct in tunable regimes; tuned constant, linear, and quadratic baselines are included and reported.

3. The suite is synthetic.
   Response: true; the manuscript presents it as a controlled boundary audit and states that real robot validation is future work.

4. Abstention lowers completion.
   Response: abstention is reported separately. Boundary-certified control trades completion for a 0.006 unsafe rate.

5. The certificate may overcall risk.
   Response: negative controls are included and have 0.807 safe completion with 0.039 irreducible score.

6. The result may be a simulator artifact.
   Response: the suite includes benign, tunable, ambiguous, and irreducible regimes under one deterministic code path, with all metrics and tables committed.

7. The old toy was falsified.
   Response: accepted. The final paper keeps the old result as a historical tunable-regime example and does not use it as positive proof.
