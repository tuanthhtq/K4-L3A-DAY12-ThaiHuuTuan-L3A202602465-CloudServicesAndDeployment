# Project Rules

## Configuration and secrets

- Keep secrets in `.env`, the cloud platform secret store, or GitHub Actions
  secrets. Never commit `.env` or a real API/deploy key.
- `AGENT_API_KEY` is mandatory. Other runtime settings use the defaults in
  `app/config.py` unless environment variables override them.
- The container command must use the platform-provided `PORT` value.

## Containers and health checks

- Keep dependency installation before source copies so application changes do
  not invalidate the dependency layer.
- Run the production image as a non-root user.
- `/health` reports process liveness without calling Redis. `/ready` checks
  Redis and controls whether the instance should receive traffic.
- Redis stays on the private Compose network; do not expose port 6379 unless a
  local debugging task explicitly requires host access.

## CI/CD

- Pull requests and pushes to `main` run tests and build the Docker image.
- CI excludes CP5 because it calls a live deployment, and excludes the bonus
  test because its badge check depends on the workflow already being pushed.
- Configure `DEPLOY_HOOK_URL` before expecting the deploy step to trigger a
  platform. Configure `PUBLIC_URL` to enable the post-deploy health smoke test.
- Run `pytest tests/ -v`, `python grade.py`, and `docker compose config` before
  submission. A skipped environment-dependent test is not proof of success.
