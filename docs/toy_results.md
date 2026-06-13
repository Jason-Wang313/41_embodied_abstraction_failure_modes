# Toy Results

- Full-state success: 0.963
- Abstract-state success: 0.197
- Success gap: 0.765
- Nominal squeeze error vs failure correlation: -0.231

Original interpretation: the abstract controller can be close in action-space to the full controller while still failing more often because the deleted variables control the feasible physical regime.

## V2 tuned-abstraction stress

- Original abstract controller: 0.187 held-out success
- Full-state controller: 0.962 held-out success
- Tuned constant abstraction: 0.987 held-out success
- Tuned visible-goal abstraction: 0.987 held-out success

V2 interpretation: the original toy interpretation is invalid. The environment can be solved by a tuned abstract constant action, so the old success gap reflects a weak abstract policy rather than a necessary failure of abstraction.