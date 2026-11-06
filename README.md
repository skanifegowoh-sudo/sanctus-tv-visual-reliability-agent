# Sanctus TV Visual Reliability Agent

OpenCV AI Competition 2026 — OpenCV 5 + AWS Agentic Vision

## The problem
A live-TV stream can return a successful network response while viewers still see a frozen or black picture. Sanctus TV existed before this competition and encountered this problem while operating a growing live-channel catalogue. URL checks alone cannot answer the important question: **is there actually a usable television picture?**

## What this competition project adds
The Visual Reliability Agent gives Sanctus visual perception. OpenCV 5 decodes and measures successive frames, temporal evidence distinguishes sustained failures from legitimate low-motion content, a bounded state machine chooses safe next steps, OpenCV verifies recovery visually, and AWS preserves the evidence and decisions.

**Core loop:** Live stream -> OpenCV perception -> evidence -> decision -> bounded action -> OpenCV verification -> AWS audit -> operator review.

OpenCV is not decorative analytics here: its visual evidence changes the next action.

## Live demo
Broadcast Health: https://sanctus-tv.pages.dev/competition/stream-health/

The dashboard contains two deliberately separate kinds of evidence:
- a controlled failure/recovery scenario demonstrating the complete agentic loop and human controls;
- real passive observations from genuine Sanctus TV broadcasts.

## Key results
- OpenCV runtime: 5.0.0.
- Controlled classification fixtures: healthy, sustained freeze, black/blank and legitimate low-motion all produced the expected final classification.
- Failed recovery escalates to HUMAN_REVIEW rather than falsely reporting success.
- Diverse real-stream campaign: 12 Sanctus channels across 10 programming groups, 5,314 decoded frames and 525 sampled OpenCV observations.
- Continuous-observer validation: two repeated 12-channel rounds; all 24 structured observation events were accepted by the live AWS API.
- Real-stream validation remains observation-only: zero destructive production actions.

These are bounded evaluation results, not claims of continuous 100% channel-health accuracy.

## Architecture
See docs/architecture.txt and docs/technical-report.md.

The system separates:
1. perception and evidence;
2. automated bounded decisions;
3. safe recovery/retest;
4. post-action visual verification;
5. human authority;
6. AWS audit history.

## Repository guide
- src/health_engine_v2.py — temporal OpenCV detector
- src/state_machine.py — bounded health states
- src/orchestrator.py — agent decision logic
- src/closed_loop_eval.py — recovery verification evaluation
- src/campaign_runner.py — bounded concurrent real-stream validator
- src/continuous_observer.py — repeated observation rounds + AWS event publication
- aws/template.yaml — AWS infrastructure
- aws/lambda/health_api.py — event/history API
- dashboard/ — Broadcast Health control surface
- tests/ — deterministic synthetic fixtures and evaluation scripts
- evidence/ — machine-readable evaluation/audit evidence
- docs/technical-report.md — technical report
- docs/reproduction.md — reproduction instructions
- docs/judge-video-script.md — <=5 minute demo plan

## Reproduce the controlled evaluation
Create a Python environment, install requirements.lock, then generate the deterministic fixtures:

    python tests/generate_cases.py
    python tests/build_recovery_cases.py

Run the controlled detector evaluation:

    PYTHONPATH=src python src/eval_v2.py

Run state/agent/API contract checks:

    python tests/test_state_machine.py
    python tests/test_agentic_trace.py
    python tests/aws/test_health_api.py

See docs/reproduction.md for the complete guide.

## Responsible operation
The system prefers uncertainty over false certainty. A stream that cannot provide sufficient visual evidence is INCONCLUSIVE, not automatically broken. Permanent deletion, automatic source replacement, DRM/authentication bypass and geographic-restriction bypass are outside the competition agent. Operator Confirm / Override / Reject decisions are separately auditable.

## What existed before the competition
Sanctus TV itself, its viewer/player, channel catalogue and existing network-level reliability work predate this competition.

## What was built for the competition
The OpenCV 5 visual-health engine, temporal evidence model, controlled failure lab, agentic state/recovery loop, post-recovery visual verification, AWS health-event backend, real-stream visual campaign, continuous observer, human audit controls and Broadcast Health competition dashboard were built as the competition subsystem.

## Limitations
Broadcast content is difficult: a priest at an altar may barely move, a film may intentionally fade to black, and CDN/codec/network behavior may prevent frame decoding. This is why the system uses temporal confirmation, repeated observations, explicit INCONCLUSIVE results and human review.

## Submission
See docs/submission-checklist.md for the final human submission steps.


## Maintainer and portfolio

Developed by **Paul Nativity** as part of **Sanctus Technology**.

The wider [Sanctus TV streaming platform](https://sanctus-tv.pages.dev/) existed before this visual-reliability project. This repository documents the OpenCV/AWS subsystem, including reproducible tests and bounded evaluation evidence.

- [Sanctus Technology website](https://sanctustechnology.com.ng)
- [Developer GitHub portfolio](https://github.com/skanifegowoh-sudo)
