# Cloud Deployment

## Railway service

The FastAPI service is deployed from the GitHub repository through the Railway
GitHub integration. Its public endpoint is:

`https://k4-l3a-day12-thaihuutuan-l3a202602543-cloudservi-production.up.railway.app`

The generated Railway domain retains an older service name after the GitHub
repository was renamed. The domain name does not need to match the current
student ID as long as the Railway service source points to the correct repo.

The service uses Railway-provided `PORT`, a secret `AGENT_API_KEY`, and a
`REDIS_URL` reference to a Redis service in the same Railway project. Rate,
budget, and log-level settings are also stored as service variables.

## Verified behavior

Verification on 2026-09-28 produced these results:

- `/health` returned HTTP 200 with service status `ok`.
- `/ready` returned HTTP 200 with `redis: true`.
- `/ask` without an API key returned HTTP 401.
- `/ask` with the configured API key returned HTTP 200 and the expected fields.
- Repeated requests for one user reached the limit and returned HTTP 429.

An initial Railway deployment returned HTTP 502 because the service had not
been fully configured and redeployed with the current container setup. Check
the deployment log, service variables, Redis reference, and runtime port when
the Railway edge reports `Application failed to respond`.
