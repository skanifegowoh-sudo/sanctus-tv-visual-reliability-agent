# Judge Video — maximum 5 minutes

## 0:00–0:30 — The real problem
Show Sanctus TV briefly. Explain: a stream may connect successfully while the actual picture is frozen or black. Sanctus needed visual health, not only URL health.

## 0:30–1:15 — Architecture
Show the architecture:
Live stream -> OpenCV 5 -> temporal evidence -> state machine -> bounded action -> OpenCV verification -> AWS audit -> operator dashboard.

State clearly that OpenCV evidence changes what the system does next.

## 1:15–2:25 — Controlled failure and recovery
Run/show the freeze scenario.
Point to frame change, freeze duration and CONFIRMED_FAILURE.
Show SAFE_RETEST.
Then show fresh frame activity and RECOVERED.
Show the trace in AWS/dashboard.

## 2:25–3:15 — Failure handling
Show stall_never_recovers.
Explain that the agent does not fabricate recovery: it ends in HUMAN_REVIEW.
Show Confirm/Override/Reject and explain that human decisions are separately audited.

## 3:15–4:05 — Real Sanctus broadcasts
Show the Real broadcast observations table.
Explain that these are genuine passive samples from multiple programming types.
Point out Healthy sample versus Inconclusive.
Mention the Georgia low-motion edge case and temporal-confirmation improvement.

## 4:05–4:35 — AWS and reproducibility
Show AWS architecture/deployment evidence, event history and repository structure.
Mention OpenCV 5.0.0, pinned dependencies, synthetic reproducible fixtures and infrastructure-as-code.

## 4:35–5:00 — Why it matters
Close on the operational goal: as Sanctus grows toward a large live-TV catalogue, one operator cannot manually watch every channel. The agent provides visual evidence, bounded recovery and human control without pretending uncertainty is certainty.

Do not claim continuous monitoring accuracy from bounded samples. Do not claim every channel can be automatically repaired.
