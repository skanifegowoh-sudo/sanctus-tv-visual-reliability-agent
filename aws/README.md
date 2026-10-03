# AWS component
Meaningful competition backend: API Gateway + Lambda + encrypted DynamoDB stores auditable visual-health/agent events and exposes per-channel history. DynamoDB uses on-demand billing. Lambda receives least-privilege table access via SAM policy. No AWS credentials belong in this repository.

Endpoints: GET /healthz; POST /health-events; GET /channels/{channel_id}/history.
