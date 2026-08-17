# Repository ruleset presets

GitHub Free for organizations supports repository-level rulesets only for **public** repositories. These presets therefore become applicable after each project is made public.

## Order of operations

For a repository that is currently private:

1. Merge the repository's governance/security CI PRs.
2. Change repository visibility to Public.
3. Enable Dependabot alerts and Dependabot security updates.
4. Enable Secret Protection / secret scanning and repository push protection.
5. Enable CodeQL **Default Setup**. Do not add the shared advanced CodeQL workflow unless Default Setup is intentionally disabled.
6. Confirm a pull request produces the expected checks.
7. Import the matching JSON preset from **Settings → Rules → Rulesets → New ruleset → Import a ruleset**.

The presets require:

- no branch deletion;
- no force-push/non-fast-forward updates;
- branches must be up to date with the target before merge;
- one approving review;
- CODEOWNERS approval;
- approval of the most recent push by someone other than the pusher;
- all review threads resolved;
- application CI, secret scanning, release-policy checks (on `main`), dependency review and CodeQL.

## Presets

| Repository / branch | Preset |
| --- | --- |
| Antirecurso `main` | `antirecurso-main.json` |
| Antirecurso API `main` | `antirecurso-api-adonis-main.json` |
| Orbit `main` | `orbit-main.json` |
| Unclassed `main` | `unclassed-main.json` |
| Unclassed `dev` | `unclassed-dev.json` |
| Fallstack `main` | `fallstack-main.json` |
| Fallstack `dev` | `fallstack-dev.json` |

### Antirecurso

Antirecurso already has an active repository ruleset named `main`. Do **not** create a duplicate. Edit the existing ruleset so its required checks match `antirecurso-main.json`; in particular add `validate-release-label`, `dependency-review / Dependency review`, and `CodeQL` after the centralization PR is merged.

### Unclassed

The `main` preset assumes the CI currently accumulated on `dev` is part of the `dev → main` release promotion. If `main` is protected before that CI exists for main-targeting pull requests, verify those checks appear on the release PR before activating the ruleset.

### Fallstack

`fallstack-main.json` matches the CI currently on `main` (`Test, Typecheck & Lint` and the migrator-stage Docker check). The stabilization work on `dev` has stronger/differently named checks. When that CI is promoted to `main`, update the main ruleset to use the same application check names as `fallstack-dev.json` plus `validate-release-label`.

## Integration IDs

The JSON files pin GitHub Actions checks to integration ID `15368` and GitHub CodeQL's `CodeQL` check to integration ID `57789`, matching the checks currently produced by GitHub.com. If GitHub changes these integrations or a repository intentionally switches scanning provider, export/update the ruleset instead of weakening required checks.
