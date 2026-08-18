# Repository ruleset presets

GitHub Free for organizations supports repository-level rulesets only for **public** repositories. These presets therefore become applicable after each project is made public.

## Order of operations

For a repository that is currently private:

1. Merge the central reusable-workflow policy in this `.github` repository.
2. Migrate that application repository to the canonical local callers/CI triggers.
3. Change repository visibility to Public when appropriate.
4. Enable Dependabot alerts and Dependabot security updates.
5. Enable Secret Protection / secret scanning and repository push protection.
6. Enable CodeQL **Default Setup**. Do not add the shared advanced CodeQL workflow unless Default Setup is intentionally disabled.
7. Confirm a pull request produces the expected application CI, reusable Security and reusable Release-policy checks.
8. Update/import the matching repository ruleset so its required status-check contexts exactly match those observed checks.

The presets require:

- no branch deletion;
- no force-push/non-fast-forward updates;
- branches must be up to date with the target before merge;
- one approving review;
- CODEOWNERS approval;
- approval of the most recent push by someone other than the pusher;
- all review threads resolved;
- application CI, Security checks, release-policy checks on `main`, and CodeQL where enabled.

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

## Workflow-centralization migration

The JSON files are repository-specific snapshots, not organization-wide live configuration. Reusable-workflow migration can change the exact status-check context exposed by GitHub (for example, a caller job may prefix a called-workflow job name).

Therefore, migrate **one repository at a time**:

1. update that repository's workflows;
2. let a real pull request run;
3. record the exact check contexts GitHub reports;
4. update that repository's ruleset/preset to those contexts;
5. only then remove obsolete required check names.

Do not pre-emptively weaken or delete required checks just because their workflows are being centralized.

Antirecurso already has an active repository ruleset named `main`; edit it rather than creating a duplicate. The same principle applies to any repository that already has an active ruleset.

## Integration IDs

The JSON files pin GitHub Actions checks to integration ID `15368` and GitHub CodeQL's `CodeQL` check to integration ID `57789`, matching the checks currently produced by GitHub.com. If GitHub changes these integrations or a repository intentionally switches scanning provider, export/update the ruleset instead of weakening required checks.
