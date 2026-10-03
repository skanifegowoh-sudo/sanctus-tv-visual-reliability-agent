# Submission Copy

## Project title
Sanctus TV Visual Reliability Agent

## One-line description
An OpenCV 5 agent that watches the actual picture of live-TV streams, distinguishes visual failure from network availability, performs bounded recovery, verifies the picture returned, and records the evidence in AWS with human oversight.

## Short description
Sanctus TV is an existing live-TV platform with a practical reliability problem: a stream may connect successfully while viewers still see a frozen or black picture. The Visual Reliability Agent adds OpenCV 5 perception to the operations layer. It analyses decoded frames over time, gathers evidence for freeze and black/blank conditions, chooses bounded next actions, and requires fresh visual evidence before declaring recovery. AWS stores the perception, decision, action and outcome trail. Ambiguous probes remain Inconclusive, and operators can confirm, override or reject decisions.

## Problem and impact
Traditional uptime checks can prove that an endpoint answered; they cannot prove that viewers are receiving a useful moving picture. This becomes increasingly difficult to manage manually as a live-TV catalogue grows across different content types. Sanctus turns the video itself into operational evidence while retaining conservative automation and human authority.

## Innovation
The project closes the loop between computer vision and operations. OpenCV does not merely produce a dashboard metric: visual evidence changes the state machine and subsequent action, and OpenCV is used again after intervention to verify that the broadcast picture actually recovered. Real broadcast edge cases are represented explicitly through Attention and Inconclusive states rather than forced binary labels.

## OpenCV use
OpenCV 5.0.0 handles video decoding and frame-level visual measurements including grayscale luminance, dark-pixel ratio, frame difference and temporal confirmation. Sustained evidence is required before freeze/black conditions become confirmed failures.

## AWS use
A deployed AWS HTTP API stores structured health events in DynamoDB and exposes channel history. Controlled agent traces, real passive broadcast observations and human decisions are persisted and retrieved by the Broadcast Health dashboard.

## Evaluation summary
Controlled fixtures cover healthy motion, freeze, black/blank, legitimate low motion, successful recovery and failed recovery. A diverse real-broadcast campaign sampled 12 Sanctus channels across 10 programming groups, processing 5,314 decoded frames and 525 sampled OpenCV observations. A repeated observer then ran two further 12-channel rounds and successfully stored all 24 structured observation events in AWS. Real-stream evaluation was passive: zero destructive production actions.

## Responsible operation
The agent prefers uncertainty to false certainty. Insufficient evidence becomes Inconclusive. Real-stream validation is observation-only. Destructive deletion, permanent source replacement and access-control bypass are not agent actions. Higher-risk ambiguity can end in Human Review, and operator decisions are separately audited.

## Live demo
https://sanctus-tv.pages.dev/competition/stream-health/
