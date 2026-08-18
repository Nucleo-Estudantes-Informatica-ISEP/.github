# NEI-ISEP repository standards

This repository is the source of truth for organization-wide contribution defaults, shared GitHub Actions policy and reusable CI/security building blocks.

## GitHub Free constraints

The organization currently uses GitHub Free.

- Organization-level rulesets that target multiple repositories require GitHub Team or Enterprise, so they are not used.
- Repository-level rulesets are available on GitHub Free for **public** repositories.
- Private repositories on GitHub Free cannot use repository rulesets. Keep existing protections in place until the repository is public.
- GitHub Code Quality is not available on GitHub Free; it requires GitHub Team or Enterprise Cloud. Do not enable or rely on it as an organization gate while the organization remains on Free.
- CodeQL code scanning is available for public repositories and is the organization-standard free static-security analysis.
- Dependency review is available for public repositories with the dependency graph enabled; public repositories have the dependency graph enabled by default.
- Shared actions/workflows in this public `.github` repository can be consumed by the organization's repositories, subject to each repository's GitHub Actions policy.

## Default community files

The root `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md` are organization defaults. GitHub uses them for repositories that do not define a repository-specific version.

Repository-specific files take precedence and should only exist when the project genuinely needs different policy.

## CODEOWNERS

GitHub does **not** inherit CODEOWNERS from the organization's special `.github` repository. Every maintained project therefore keeps a local `.github/CODEOWNERS` file with the default owners:

```text
* @hugo2006alm @dinisjcorreia @david-fs-valente
```

Projects can append more specific path rules below that line. A more specific rule overrides the matching ownership for that path, so include every intended owner on the specific rule.

## Workflow architecture

Centralize organization policy and repeated infrastructure here; keep application knowledge in each application repository.

### Central `.github` repository

The central repository owns:

- release-label validation and semantic release publishing;
- dependency review policy;
- the verified/pinned Gitleaks implementation;
- the reusable Security workflow that composes dependency review + secret scanning;
- the reusable Release workflow that composes validation + publishing;
- optional advanced CodeQL workflow support;
- workflow templates and repository/ruleset standards.

### Application repositories

Application repositories keep only:

- the event trigger/caller files required by GitHub Actions;
- package-manager install commands;
- lint/typecheck/test/build commands;
- application-specific CI environment variables;
- databases and service containers;
- Prisma/Lucid migrations and schema audits;
- OpenAPI drift checks;
- Docker build/runtime checks;
- deployment-specific validation.

Do **not** duplicate organization policy implementation locally. Local workflows should call the reusable workflows/actions in this repository.

## Canonical trigger policy

Avoid running the same expensive checks both for a pull request and again for the push produced by merging that pull request.

### Application CI

The default for maintained repositories with protected branches is:

```yaml
on:
  pull_request:
    branches: [dev, main]
  workflow_dispatch:
```

Full application CI should **not** also run on every `push` to `dev` or `main` by default. The pull request already validated the code before merge, and protected branches should prevent ordinary unreviewed direct pushes.

A repository may add a post-merge `push` workflow only for a genuinely different purpose such as deployment, smoke verification, artifact publication or another post-merge concern. Do not repeat the full PR quality suite merely because the branch advanced.

### Security

Security callers run on pull requests and may expose `workflow_dispatch` for manual audits. The implementation is centralized in `.github/workflows/security.yml`.

### Release

Release callers target pull requests into `main`. Release-policy validation reruns when release labels or the PR contents change because the release label is itself policy input. Publishing only happens when an eligible PR is closed as merged.

That small metadata-driven rerun is intentional; duplicating the entire application CI on both PR and branch push is not.

## Release policy

Repositories using semantic releases keep only a small local caller workflow. The implementation lives in the reusable `.github/workflows/release.yml`, which in turn uses:

- `.github/actions/release-policy`
- `.github/actions/release-publish`

Canonical caller:

```yaml
name: Release

on:
  pull_request:
    branches: [main]
    types: [opened, reopened, synchronize, labeled, unlabeled, closed]

jobs:
  release:
    name: Release
    permissions:
      contents: write
      pull-requests: read
    uses: Nucleo-Estudantes-Informatica-ISEP/.github/.github/workflows/release.yml@master
    with:
      product-name: ${{ github.event.repository.name }}
```

For pull requests into `main`:

- runtime changes require exactly one `release:patch`, `release:minor` or `release:major` label;
- Dependabot PRs are release-exempt;
- changes exclusively under `.github/`, `docs/`, Markdown/community files, `.gitignore`, `.editorconfig` or `.vscode/` are release-exempt;
- eligible merged PRs publish a GitHub Release and SemVer tag automatically.

One-time `release-bootstrap.yml` workflows must be deleted after a repository has its SemVer baseline.

## Security and secret scanning

The standard local `security.yml` should be a caller for `.github/workflows/security.yml` instead of reimplementing dependency review or keeping a second secret-scan job inside application CI.

Canonical caller:

```yaml
name: Security

on:
  pull_request:
    branches: [dev, main]
  workflow_dispatch:

jobs:
  security:
    name: Security
    permissions:
      contents: read
    uses: Nucleo-Estudantes-Informatica-ISEP/.github/.github/workflows/security.yml@master
```

The reusable workflow:

- runs dependency review on eligible public-repository pull requests;
- runs the verified organization-standard Gitleaks action;
- supports an explicit full-history Gitleaks audit when required.

A revoked historical credential is not, by itself, a reason to rewrite Git history. Rewrite history only if a still-sensitive value must be removed and coordinate it carefully because rewriting changes commit SHAs and can invalidate branches, tags and open pull requests.

When migrating an existing repository to the reusable Security/Release callers, verify the status-check contexts produced by the new caller and update that repository's ruleset/branch protection in the same repository migration. Never weaken required checks merely to make a renamed context pass.

## CodeQL

For public repositories, prefer **CodeQL Default Setup** in GitHub's repository security settings. Default Setup and an advanced CodeQL Actions configuration are mutually exclusive; enabling both causes the advanced analysis upload to fail.

The reusable `.github/workflows/codeql.yml` workflow is retained only for repositories that genuinely require an advanced CodeQL configuration. Before using it, disable Default Setup for that repository and document why advanced configuration is needed.

## Public repository checklist

Before changing a private project to public:

1. Confirm production credentials historically committed to Git have been rotated/revoked.
2. Confirm the current tree and pending release branch contain no secrets or private data.
3. Review `.env` examples, seed data, fixtures, screenshots and documentation for personal or partner information.
4. Keep an existing license unchanged. If the project has no license and the goal is maximum restriction, leave it without a `LICENSE`; GitHub's default copyright rules then apply.
5. Add the local CODEOWNERS file.
6. After publication, import/apply the relevant repository-level ruleset preset and keep its required status checks synchronized with the repository's actual workflow contexts.
7. Enable Dependabot alerts and security updates.
8. Enable GitHub secret scanning and push protection.
9. Enable CodeQL Default Setup.
10. Keep the local Security reusable-workflow caller enabled.

## Migration order for existing repositories

Normalize repositories one at a time:

1. keep the application-specific CI jobs but remove redundant `push` triggers for the full quality suite;
2. replace local Security implementation and CI secret-scan duplication with the central Security caller;
3. replace local Release implementation with the central Release caller;
4. run a PR and record the actual status-check contexts;
5. update the repository ruleset/branch protection to those contexts;
6. only then remove any obsolete workflow files/check requirements.

This order keeps protections active throughout the migration and prevents one repository's stack-specific changes from affecting another repository.
