# Submission Readiness Decision

Decision: kill/archive.

Reason: the v2 tuned-abstraction stress invalidates the core evidence. A tuned constant abstract controller reaches 0.987 held-out success, which exceeds the full-state controller's 0.962. The paper therefore does not establish that high-level state compression deleted variables needed for physical success.

Next useful research move: redesign the toy or real-robot evaluation so that tuned abstract baselines are included from the start, and only revive the submission if abstraction still fails because a physically necessary variable is unavailable.
