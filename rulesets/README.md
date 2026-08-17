# Repository ruleset presets

GitHub Free for organizations supports repository-level rulesets for **public** repositories. The active NEI platforms are public, so the presets in this directory can be enforced without GitHub Team.

## Automated application

The preferred path is `scripts/apply-repository-governance.sh`, exposed through the **Apply repository governance** workflow in the organization `.github` repository.

The script is idempotent and applies the baseline to Antirecurso, Antirecurso API, Orbit, Unclassed and Fallstack:

1. enable dependency/vulnerability alerts;
2. enable Dependabot security updates;
3. enable secret scanning and repository push protection;
4. configure CodeQL Default Setup;
5. create missing repository rulesets or update existing rulesets with the JSON presets below.

For the workflow, create a repository Actions secret named `NEI_GOVERNANCE_TOKEN` in the `.github` repository. Use a fine-grained PAT owned by an organization owner with access limited to the five target repositories and **Repository permissions → Administration: Read and write**. Do not commit or paste the token into workflow YAML, issues, PRs, or chat.

Run the workflow once with `dry_run=true`, inspect the plan, then run it with `dry_run=false`. Re-running it later updates the existing rulesets rather than creating duplicates.

The same script can also be run locally:

```bash
GH_TOKEN='<fine-grained PAT>' DRY_RUN=true bash scripts/apply-repository-governance.sh
GH_TOKEN='<fine-grained PAT>' DRY_RUN=false bash scripts/apply-repository-governance.sh
```

## What the presets require

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

Antirecurso already has an active repository ruleset named `main`. The automation updates that ruleset in place so its required checks match `antirecurso-main.json`; it does not create a duplicate.

### Unclassed

The `main` preset assumes the CI currently accumulated on `dev` is part of the `dev → main` release promotion. If the application check names change when that work is promoted, update `unclassed-main.json` before re-running the governance workflow.

### Fallstack

`fallstack-main.json` matches the CI currently on `main`. The stabilization work on `dev` has stronger/differently named checks. When that CI is promoted to `main`, update the main preset to use the same application check names as `fallstack-dev.json` plus `validate-release-label`, then re-run the governance workflow.

## Integration IDs

The JSON files pin GitHub Actions checks to integration ID `15368` and GitHub CodeQL's `CodeQL` check to integration ID `57789`, matching the checks currently produced by GitHub.com. If GitHub changes these integrations or a repository intentionally switches scanning provider, export/update the ruleset instead of weakening required checks.
