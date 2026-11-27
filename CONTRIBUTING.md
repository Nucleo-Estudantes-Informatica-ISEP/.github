# Contributing

Default contribution guide for repositories that do not provide their own.
Repository-specific docs (`README`, `AGENTS.md`, `docs/`) take precedence.

- Follow the [Code of Conduct](./CODE_OF_CONDUCT.md).
- Report security issues through the [Security Policy](./SECURITY.md), never a public issue.
- Never commit credentials, tokens, private data or production secrets.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<optional scope>): <description>
```

- Write the header only. No body, no footer, no trailers. Put context, motivation
  and issue links in the PR.
- Make one logical change per commit. Split unrelated work.
- **Description:** required, imperative present tense, lowercase start, no trailing
  period, under 72 characters.
- **Scope:** optional, names the code area (`feat(auth): ...`). Never use an issue
  number as scope. Use only scopes the repository defines, if it defines any.
- **Breaking change:** add `!` before the colon (`feat(api)!: remove status endpoint`)
  and make the description state the break. Describe migration steps in the PR.
- **Revert and merge commits:** keep Git's default messages
  (`Revert "<subject>"`, `Merge branch '<name>'`).

| Type       | Use for                                                          |
| ---------- | ---------------------------------------------------------------- |
| `feat`     | Adding, changing or removing a feature in the API or UI          |
| `fix`      | Fixing a bug in the API or UI                                    |
| `refactor` | Restructuring code without changing behavior                     |
| `perf`     | Performance improvements                                         |
| `style`    | Formatting only (whitespace, semicolons)                         |
| `test`     | Adding or correcting tests                                       |
| `docs`     | Documentation only                                               |
| `build`    | Build tools, dependencies, project version                       |
| `ops`      | Infrastructure, deployment, CI/CD, backups, monitoring, recovery |
| `chore`    | Other maintenance (`.gitignore`, initial commit `chore: init`)   |

Types map to versions: breaking change → major, `feat` → minor, everything else → patch.

## Branches

- Use [Conventional Branch](https://conventionalbranch.org/): `<type>/<short-kebab-description>`.
- Types: `feat`, `fix`, `hotfix`, `release`, or any commit type above (`docs`, `test`,
  `build`, `ops`, `chore`, `refactor`, `perf`).
- Derive the description from the issue title, in 2-5 words
  (`feat/add-export-button`). The issue number is optional.

## Branch workflow

Use the model the repository documents in its own `AGENTS.md`, `CONTRIBUTING.md` or
`README`. If none is documented, use **main-only**.

- **main-only:** branch from `main`, open the PR into `main`.
- **dev/main:** branch from `dev`, open the PR into `dev`. A reviewed
  `dev` → `main` promotion PR ships a release.

Keep the branch up to date with its target before review. Do not push directly to
`main` or `dev`.

## Pull requests

**Description**

- Use the PR template if the repository has one.
- State what changed and why, and link the issue.
- State any migration, environment, storage or deployment configuration change.

**Metadata**

- Add labels, an assignee, and reviewers (see `CODEOWNERS`).
- Where the repository uses release labels, a runtime-changing PR to `main` needs
  exactly one of `release:major`, `release:minor` or `release:patch`.
  Documentation, CI, repository metadata and Dependabot PRs are exempt.
- Pick the label by impact: `patch` for backwards-compatible fixes, `minor` for
  backwards-compatible features, `major` only for intentional breaking changes.
- Where the repository uses semantic-release, merging to `main` publishes the
  release. Otherwise follow the repository's release docs.

**Target branch**

- Follow the branch workflow above.
- A `dev` → `main` promotion PR lists the changes it ships.

**Closing issues**

- `Closes #N` links the issue. GitHub closes it only when the change reaches the
  default branch. In dev/main repositories that happens at promotion.
- Use `Refs #N` when the PR only partly resolves the issue.

**Testing and verification**

- Every behavior change needs a test at the lowest useful level.
  For bug fixes and business rules, write the failing test first.
- Before review, run the repository's documented lint, typecheck, test and build commands.
- Exercise the change manually: run the app, open the changed page or route, and for
  APIs check the response body and status.
- Report what you ran and what you could not run. CI is authoritative.
  Do not weaken or skip checks to make them pass.

**Specific situations**

- **Migrations:** commit them with the schema change. Do not edit applied migrations.
- **Docs-only:** verify content, links, filenames and `git diff --check`, and run the
  formatter on changed files. Application checks are not needed locally.
- **Dependencies:** same gates as code. Major upgrades need a migration plan.
- **Design decisions:** add or update an ADR when the PR settles a meaningful decision.
- **Architecture changes:** update the architecture docs (for example the SAD).

## Issues

Use the templates in `.github/ISSUE_TEMPLATE` when available. Remove optional
sections that do not apply.

**Epic**

- A parent issue for a goal that spans several issues.
- Contains Goal, Outcome, and a checklist of child issues. No implementation details.

**Task / Feature**

- **Description**, optional **Why**, **Scope**, **Acceptance Criteria**,
  optional **Dependencies** (one checkbox per dependency).

**Bug**

- Steps to reproduce, expected behavior, actual behavior, environment, and logs or screenshots.
- Report only reproducible problems.

## Reviews

- Address review comments and push fixes to the same branch.
- Code owners are defined in `CODEOWNERS`.

---

## Agents

Rules for AI agents, in addition to everything above. When a rule here conflicts
with a general rule, this section wins.

**Scope**

- Do only what the issue or request asks. Record follow-up work as a new issue.
- Ask before destructive actions, major dependency upgrades, or changes to CI or
  deployment configuration.

**Commits**

- Commit and push only when asked.
- Write a one-line header. Omit the body, footer, AI co-author trailers and
  "generated by" lines.
- Never force-push or rewrite shared history. Never commit secrets or `.env` files.

**Branches**

- Never work directly on `main` or `dev`.
- Name the branch from the issue title, using the format above.

**Branch workflow**

- Read `AGENTS.md`, `CONTRIBUTING.md` and the `README` to find the model in use.
  If they are silent but a `dev` branch exists, ask.
- Fetch and update the base branch before branching.
- Never merge a PR or open a promotion PR unless asked.

**Pull requests**

- Fill every section of the PR template. Leave none empty.
- Apply the labels and assignee you can. Say which you could not.
- Do not claim a deployment happened unless you observed it.

**Verification**

- Never report a check as passing unless you ran it.
- Do not delete, skip or loosen tests, lint rules or CI to get a green result.
- Report pre-existing failures separately from failures you caused.

**Issues**

- Link the issue in the PR.
- If no issue exists for non-trivial work, propose one using the right template.
