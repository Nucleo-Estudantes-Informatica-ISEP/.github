# Contributing to NEI-ISEP projects

Thank you for contributing to software maintained by the Núcleo de Estudantes de Informática do ISEP.

This is the default contribution guide for repositories that do not provide a more specific one. Repository-specific instructions, `AGENTS.md` files and README documentation take precedence when present.

## Before you start

- Read the repository README and open issues.
- Follow the organization [Code of Conduct](./CODE_OF_CONDUCT.md).
- Never commit credentials, tokens, passwords, private student data or production secrets.
- For security-sensitive reports, use the [Security Policy](./SECURITY.md) instead of a public issue.

## Workflow

1. Create or choose an issue when the work needs discussion or tracking.
2. Branch from the repository's documented development branch. If none is documented, branch from the default branch.
3. Prefer branch names such as `feat/short-description`, `fix/short-description`, `docs/short-description`, `test/short-description`, `build/short-description` or `chore/short-description`.
4. Keep commits logically scoped and use clear commit messages. Conventional Commits are preferred where the repository already uses them.
5. Add or update tests for behavior changes whenever practical.
6. Run the repository's documented lint, typecheck, test and build commands before requesting review.
7. Open a pull request with a clear description, validation notes, rollout/migration impact and links to resolved issues.
8. Address review comments and keep the branch up to date with its target branch.

## Pull requests to `main`

For repositories using the NEI semantic-release workflow:

- runtime-changing PRs to `main` require exactly one of `release:patch`, `release:minor` or `release:major`;
- Dependabot PRs do not require a release label;
- PRs that only change documentation, GitHub Actions or repository metadata do not require a release label;
- merging an eligible PR to `main` publishes the corresponding GitHub Release automatically.

Use `release:patch` for backwards-compatible fixes, `release:minor` for backwards-compatible functionality and `release:major` only for intentional breaking changes to the application/platform contract.

## Reviews and ownership

The default code owners for actively maintained Informatics Department repositories are:

- `@hugo2006alm`
- `@dinisjcorreia`
- `@david-fs-valente`

Repositories may append more specific CODEOWNERS rules for individual paths or subsystems.
