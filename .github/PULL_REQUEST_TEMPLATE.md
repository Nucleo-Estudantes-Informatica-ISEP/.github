## Summary

Describe what changed and why.

## Validation

- [ ] Lint/typecheck checks pass where applicable
- [ ] Tests pass where applicable
- [ ] Production build passes where applicable
- [ ] Security/secret checks pass

## Release impact

For PRs targeting `main` in repositories using the NEI release workflow:

- [ ] `release:patch` — backwards-compatible fix
- [ ] `release:minor` — backwards-compatible functionality
- [ ] `release:major` — intentional breaking change
- [ ] Exempt — Dependabot or documentation/CI/metadata-only change

Select exactly one release label only when the PR changes runtime behavior.

## Deployment / migration notes

List database, environment variable, external service, authentication or rollout changes. Write `None` when there are none.

## Manual actions

List any action that maintainers must perform outside GitHub. Write `None` when there are none.

## Issues

Use `Closes #N` only for issues fully resolved by this PR.
