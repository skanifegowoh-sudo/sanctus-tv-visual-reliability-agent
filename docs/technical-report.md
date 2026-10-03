# Sanctus TV Visual Reliability Agent — Technical Report

## Problem
A live stream can return HTTP 200 and still show a frozen or black picture. Sanctus TV already operated as a multi-channel live-TV product before this competition and encountered this operational problem in practice. URL health alone is therefore insufficient.

## Solution
The competition subsystem adds visual health perception with OpenCV 5. Decoded frames are measured for luminance, dark-pixel ratio and temporal frame change. Sustained evidence is classified as healthy, black/blank, frozen, attention or inconclusive. Evidence enters a bounded state machine rather than directly triggering destructive action.

## Agentic loop
Live stream -> OpenCV perception -> temporal evidence -> decision -> bounded recovery/retest -> OpenCV verification -> recovered or human review -> AWS audit.

OpenCV is causal: a visual failure changes the next system action. A recovery is not accepted merely because networking succeeds; fresh visual evidence must verify picture activity.

## Human control and safety
Passive observation is the default for real-stream validation. Destructive actions, permanent deletion and automatic source replacement are disabled. Ambiguous/no-frame probes remain INCONCLUSIVE. Riskier intervention is separated from AI evidence and operator decisions are recorded independently.

## OpenCV 5
Runtime validation used OpenCV 5.0.0. The detector uses VideoCapture, grayscale conversion, absdiff, luminance statistics and temporal confirmation across successive samples.

## AWS
A deployed AWS HTTP API persists structured health events to DynamoDB and exposes channel history. Real OpenCV observations, controlled recovery traces and human decisions are retrievable through the production dashboard's same-origin proxy.

## Evaluation
Controlled fixtures cover healthy motion, sustained freeze, black/blank, legitimate low motion, recovery success and recovery failure. The controlled classifier produced the expected result on all four classification fixtures with no false positive on the healthy/low-motion fixtures. A failed recovery escalated to HUMAN_REVIEW rather than being falsely reported recovered.

Real-stream validation then sampled diverse Sanctus broadcasts. An early short Georgia Hollywood observation exposed a possible low-motion false alarm. Temporal confirmation was strengthened and controlled tests were rerun before real-stream retesting. A later 12-channel campaign covered 10 programming groups and processed 5,314 decoded frames / 525 sampled observations. Results were stored as bounded samples, never continuous-health guarantees.

The continuous-observer validation ran two repeated 12-channel rounds. Round 1 produced 7 healthy samples and 5 inconclusive probes; round 2 produced 10 healthy and 2 inconclusive. All 24 observation events were accepted by the live AWS API. No production intervention occurred.

## Limitations
Short sampling windows cannot prove continuous channel health. CDN, codec, geolocation and transient network behavior can prevent decoding. Low-motion television can resemble a freeze. Black frames can be editorially intentional. These are why temporal confirmation, INCONCLUSIVE state, repeated observation and human review are retained.

## Responsible operation
The system favors uncertainty over false certainty. It records evidence and provenance, bounds automated actions, separates AI recommendations from operator decisions and preserves audit history.

## Reproducibility
Pinned environment: requirements.lock. Synthetic fixtures are generated locally by tests/generate_cases.py and tests/build_recovery_cases.py. Core validation scripts are in src/. AWS infrastructure is declared in aws/template.yaml. The dashboard is in dashboard/.
