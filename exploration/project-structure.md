# Project Structure

## Runtime topology

The FastAPI service in `app/` exposes `/health`, `/ready`, and `/ask`. It is
built from the root `Dockerfile` and runs as the non-root `appuser`. The
container reads `PORT` at runtime and defaults to port 8000.

Docker Compose runs two services:

- `agent` publishes host port 8000 and connects to Redis at
  `redis://redis:6379/0` over the private Compose network.
- `redis` persists data in the `redis-data` volume. Redis is not published to
  the host because only the agent needs to reach it.

Conversation history, rate-limit entries, and monthly cost totals live in
Redis so multiple agent instances can share state.

## Deployment and automation

`railway.toml` and `render.yaml` contain platform-specific deployment settings.
The GitHub Actions workflow at `.github/workflows/ci.yml` runs local checkpoint
tests, builds the Docker image, and gates the deploy job on both jobs passing.
Deployment uses the `DEPLOY_HOOK_URL` GitHub secret; the optional smoke test
uses the public `PUBLIC_URL` repository variable.
