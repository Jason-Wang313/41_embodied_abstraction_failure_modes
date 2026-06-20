# Paper 41 Full-Scale Execution Plan

Paper: `41_embodied_abstraction_failure_modes`

Working title: `Embodied Abstraction Failure Modes: Boundary Certificates for State Compression in Contact-Rich Control`

Date: 2026-06-15

## Starting State

The starting repository contained a four-page v2 negative-result note. The prior toy claim was insufficient because a tuned constant abstract controller beat the full-state controller on the held-out split. The starting document therefore could not be used as the final batch paper, and there was no canonical `C:/Users/wangz/Downloads/41.pdf` artifact in place.

The core salvageable idea is not "abstractions fail" and not "full state always wins." The defensible paper is sharper: an abstraction boundary becomes unsafe when it deletes a variable whose value changes the feasible action set, the safe action ordering, or the observability needed to choose between incompatible contacts. A serious paper must include tuned abstract baselines from the start and must show both benign cases where abstraction works and certified boundary-failure cases where no tuned policy using the compressed interface can recover the deleted information.

## Current Claim

Full-scale claim to test:

1. Embodied abstraction failure is a boundary property, not a representation-size property.
2. A compressed state can be predictive on logged or benign data while still being insufficient for safe contact-rich control when the deleted variable changes feasibility.
3. A boundary certificate can separate three regimes: benign compression, tunable compression, and irreducible compression failure.
4. The old tuned-constant counterexample is expected and should be reported as a benign/tunable regime, not hidden.

## Gaps To Close

- The current evidence is a single toy that was falsified by a tuned abstract baseline.
- There is no large seed sweep, no task family diversity, no OOD stress, no boundary-mask ablation, and no safety/regret decomposition.
- There are no tuned abstract policies beyond the old counterexample.
- There is no certificate-style analysis proving when the hidden variable matters.
- The manuscript is only four pages and does not contain a final full-scale experiment.
- Existing docs/status files must be updated only after the new results are verified.

## Target Experiment

Build a RAM-light deterministic suite with synthetic but contact-grounded families. Each trial samples visible task variables, hidden physical variables, and a true safe action interval. A controller succeeds when its action lies inside the interval and satisfies task reward, slip, damage, and energy constraints.

Factor grid:

- 18 task families: lift, slide, insert, pull, twist, pour, wipe, handoff, cable-route, peg-seat, press-fit, peel, scoop, latch, drape, push-turn, stack, and tool-use.
- 14 hidden physical variables: friction, payload, compliance, contact mode, local geometry, fluid fill, cable tension, adhesion, tactile latency, surface anisotropy, backlash, occlusion depth, grasp affordance, and support stiffness.
- 8 abstraction masks: full state, visible only, task only, object only, no hidden physical variables, no contact variables, overcompressed latent, and random feature hash.
- 13 controllers: oracle full-state, tuned constant, tuned visible linear, tuned visible quadratic, abstract nearest-regime, abstract history summary, uncertainty abstention, conservative safe action, optimistic reward action, logged-risk minimizer, mask-aware diagnostic policy, boundary-certified policy, and no-audit latent policy.
- 9 OOD/noise settings: in-distribution, friction shift, payload shift, geometry shift, sensor noise, delayed tactile cue, combined shift, rare-regime upweight, and adversarial boundary swap.
- 7 train/test splits.
- 11 seeds.
- 5 safety margins.
- 6 task-cost weights.

Represented trial evaluations: at least 2 billion controller-mask-family-stress-margin-weight checks. Actual data written should be compact aggregate CSVs plus streamed representative traces, not a giant in-memory table.

## Baselines

Baselines must include the old failure attack:

- Tuned constant abstract policy selected on training performance.
- Tuned visible-only linear and quadratic policies.
- Full-state oracle with access to hidden physical variables.
- Conservative safe policy that chooses the action with minimum expected damage.
- Optimistic reward policy that ignores safety.
- History-summary abstract policy that gets a short interaction prefix.
- No-audit latent policy that optimizes mean prediction.
- Boundary-certified policy that abstains or escalates when the abstraction cannot identify the safe interval.

## Ablations

- Remove each hidden variable family from the full-state interface.
- Collapse contact-mode variables while retaining object/task labels.
- Remove the certificate and keep only prediction loss.
- Vary safety margin from loose to strict.
- Vary training coverage from balanced to rare-regime sparse.
- Compare action regret, unsafe-force rate, slip rate, damage rate, abstention rate, and certificate recall.
- Separate cases where tuned abstraction works from cases where it fails irreducibly.

## Stress Tests

- Distribution shifts on friction, payload, compliance, and geometry.
- Rare physical regimes that are nearly absent in training.
- Sensor-noise and delayed-observability settings.
- Adversarial boundary swaps where the same visible task maps to opposite safe actions depending on the hidden variable.
- Safety-threshold tightening to test whether abstractions fail first in conservative settings.
- Negative controls where the hidden variable is irrelevant, proving the method does not call all abstractions unsafe.

## Figures And Tables

Required figures:

1. Regime map showing benign, tunable, and irreducible boundary-failure zones.
2. Controller success/regret/unsafe heatmap across task families and masks.
3. OOD stress plot for full-state, tuned abstract, and boundary-certified policies.
4. Abstention versus unsafe-rate tradeoff.
5. Representative traces showing the same visible state needing different actions because of a hidden variable.
6. Variable-deletion ablation bars.

Required tables:

1. Scale table with factor counts and represented checks.
2. Main performance table across controllers.
3. Mask ablation table.
4. Task-family summary table.
5. OOD robustness table.
6. Certificate precision/recall table.
7. Negative-control table showing abstraction succeeds when hidden variables are irrelevant.
8. Final falsification table explaining how the old tuned-constant result fits the new taxonomy.

## Writing Expansion

The manuscript should become a full final paper of at least 25 pages. Expansion should come from:

- A precise problem statement and definitions of abstraction boundary failure.
- A theorem/proposition-style information-boundary argument.
- Full experimental protocol.
- Full baseline descriptions.
- Results separated by benign/tunable/irreducible regimes.
- Stress tests and ablations.
- Reconciliation with the old v2 falsification.
- Limitations, reproducibility, and reviewer-attack response.
- Human-readable references and related work discussion.

No padding: every page should carry methods, results, analysis, figures, tables, limitations, or reproducibility material.

## RAM-Light Execution Strategy

- Use one deterministic Python runner with standard library plus numpy/matplotlib.
- Stream seed-level rows to CSV instead of holding all trial results.
- Keep only compact controller aggregates in memory.
- Generate figures from aggregate CSVs and bounded representative traces.
- Use fixed seeds and deterministic grids.
- Avoid huge raw trial dumps; store aggregate metrics, validation JSON, snippets, and representative traces.
- Run sequentially if needed; do not lower experiment quality because of RAM constraints.

## Final Acceptance Checklist

Do not move to Paper42 until all items pass:

- `docs/full_scale_execution_plan.md` exists before code/manuscript edits.
- Full-scale runner completes and writes validation with expected row counts.
- New results include tuned abstract baselines and negative controls.
- Manuscript presents the previous v2 result only as historical context, not as the current decision.
- Final compiled paper is at least 25 pages.
- `C:/Users/wangz/Downloads/41.pdf` exists only after final build.
- The local `main.pdf` is removed after canonical export.
- Final PDF text contains the full-scale markers and does not contain stale submission-failure language as the current decision.
- Final PDF is rendered to PNG pages under `tmp/pdfs/` and visually inspected.
- LaTeX logs have no unresolved references/citations and no overfull boxes that damage layout.
- Docs/status files are updated to final v3/full-scale status.
- Git diff checks pass.
- Changes are committed and pushed before starting Paper42.

## Execution Outcome

Completed on 2026-06-15.

- Full-scale runner completed.
- Expected condition rows: 235,872.
- Actual condition rows: 235,872.
- Represented trial evaluations: 34,871,316,480.
- Final manuscript pages: 26.
- Canonical PDF: `C:/Users/wangz/Downloads/41.pdf`.
- Canonical PDF SHA256: `9334E545BBDB8218703B8E53A8E15C410DE2BF0D4C9968A6CE77E1C4A0C39DEE`.
- Local `main.pdf` after canonical build: absent.
- Visual render check from Downloads PDF: passed.
- VLA-style visible link-box QA completed on pages 6, 7, 10, 12, 13, 16, and 17, with 22 green citation boxes, 13 red internal-reference boxes, and 35 visible borders.
- Log and text-marker scans: passed.
