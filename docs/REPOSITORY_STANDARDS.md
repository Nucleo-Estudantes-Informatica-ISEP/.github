# NEI-ISEP repository standards

This repository is the source of truth for organization-wide contribution defaults and shared CI building blocks.

## GitHub Free constraints

The organization currently uses GitHub Free.

- Organization-level rulesets that target multiple repositories require GitHub Team or Enterprise, so they are not used.
- Repository-level rulesets are available on GitHub Free for **public** repositories.
- Private repositories on GitHub Free cannot use repository rulesets. Keep existing protections in place until the repository is public.
- Shared actions in this public `.github` repository can be consumed by the organization's repositories, subject to each repository's GitHub Actions policy.

## Default community files

The root `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md` are organization defaults. GitHub uses them for repositories that do not define a repository-specific version.

Repository-specific files take precedence and should only exist when the project genuinely needs different policy.

## CODEOWNERS

GitHub does **not** inherit CODEOWNERS from the organization's special `.github` repository. Every maintained project therefore keeps a local `.github/CODEOWNERS` file with the default owners:

```text
* @hugo2006alm @dinisjcorreia @david-fs-valente
```

Projects can append more specific path rules below that line. A more specific rule overrides the matching ownership for that path, so include every intended owner on the specific rule.

## Release policy

Repositories using semantic releases keep a small local `.github/workflows/release.yml`, while the implementation lives in the central composite actions:

- `.github/actions/release-policy`
- `.github/actions/release-publish`

For pull requests into `main`:

- runtime changes require exactly one `release:patch`, `release:minor` or `release:major` label;
- Dependabot PRs are release-exempt;
- changes exclusively under `.github/`, `docs/`, Markdown/community files, `.gitignore`, `.editorconfig` or `.vscode/` are release-exempt;
- eligible merged PRs publish a GitHub Release and SemVer tag automatically.

One-time `release-bootstrap.yml` workflows must be deleted after a repository has its SemVer baseline.

## Secret scanning

The central `.github/actions/secret-scan` action pins and verifies Gitleaks. Keep a local job named `secret-scan`/`Secret scan` when existing rules depend on that status-check name; only the implementation step should be replaced.

Normal CI scans the PR commit range or latest pushed commit. Use `full-history: "true"` explicitly for a publication/security audit.

A revoked historical credential is not, by itself, a reason to rewrite Git history. Rewrite history only if a still-sensitive value must be removed and coordinate it carefully because rewriting changes commit SHAs and can invalidate branches, tags and open pull requests.

## Public repository checklist

Before changing a private project to public:

1. Confirm production credentials historically committed to Git have been rotated/revoked.
2. Confirm the current tree and pending release branch contain no secrets or private data.
3. Review `.env` examples, seed data, fixtures, screenshots and documentation for personal or partner information.
4. Keep an existing license unchanged. If the project has no license and the goal is maximum restriction, leave it without a `LICENSE`; GitHub's default copyright rules then apply.
5. Add the local CODEOWNERS file.
6. After publication, apply the repository-level baseline ruleset with `scripts/apply-public-ruleset.sh` and keep repository-specific required status checks in their existing rules/protection configuration.
7. Enable GitHub secret scanning and push protection for the public repository.

## CI boundaries

Centralize policy and repeated infrastructure, not application knowledge.

Keep these repository-specific:

- package-manager install commands;
- lint/typecheck/test/build commands;
- databases and service containers;
- Prisma/Lucid migrations and schema audits;
- OpenAPI drift checks;
- Dockerfiles and deployment-specific tests;
- environment variables required by the application.

This keeps a framework or package-manager migration in one project from breaking every other project.
