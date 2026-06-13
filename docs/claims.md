# Claims

1. Abstract robot representations can be physically incomplete even when they are predictive on logged data.
2. The missing variables are often contact, friction, load, and observability terms that matter only at execution time.
3. A policy or planner can look strong in abstraction-space metrics while failing in the physical regime because the abstraction deleted a causal variable.
4. The paper should therefore center on an abstraction-boundary audit rather than on a new latent model.

## V2 hardening result

The generated paper does not currently support these claims. A tuned constant abstract controller reaches 0.987 held-out success, beating the full-state controller's 0.962. The toy failure is therefore explained by an under-tuned abstract policy, not by a demonstrated structural need for hidden friction/load variables.
