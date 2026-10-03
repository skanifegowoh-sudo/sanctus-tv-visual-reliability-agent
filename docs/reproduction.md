# Judge Reproduction Guide

## Requirements
Python 3.12, FFmpeg-compatible OpenCV video I/O, and the pinned packages in requirements.lock.

## Local controlled evaluation
1. Create/activate a virtual environment.
2. Install requirements.lock.
3. Run: python tests/generate_cases.py
4. Run the detector against healthy, freeze, black and low_motion fixtures.
5. Run tests/test_state_machine.py and tests/test_agentic_trace.py.
6. Run src/closed_loop_eval.py against stall_then_recover.mp4 and stall_never_recovers.mp4.

Expected behavior:
- healthy and legitimate low motion remain healthy;
- sustained freeze and black/blank are detected;
- successful recovery requires fresh visual evidence;
- unrecovered failure ends in HUMAN_REVIEW.

## AWS
Infrastructure is declared in aws/template.yaml. aws/README.md documents deployment. The live competition deployment stores structured evidence and exposes health/history endpoints.

## Live UI
Production control surface:
https://sanctus-tv.pages.dev/competition/stream-health/

The dashboard separates the controlled recovery demonstration from real passive broadcast observations. "Healthy sample" is a bounded observation, while "Inconclusive" means insufficient decodable evidence.

## Safety
Do not point validation scripts at streams you are not authorized to access. The competition build does not bypass DRM, authentication or geographic restrictions and does not automatically delete or replace production sources.
