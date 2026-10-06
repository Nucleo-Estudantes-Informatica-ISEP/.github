# AGENTS.md

## Pull request metadata

- Whenever opening a pull request, add the applicable existing repository
  labels. Follow the repository's label conventions; do not leave the PR
  unlabeled.
- Assign every pull request to its creator (the GitHub PR author). Read the PR
  author from GitHub and use that account; use `--add-assignee @me` only when
  the authenticated account is the PR author.
- Link the issue the PR addresses through GitHub's **Development** relationship
  and verify that the link exists. A plain `Refs #N` mention is not sufficient.
  Use a closing keyword when the PR completes the issue, or explicitly link it
  through Development for partial work. For a non-default target branch,
  explicitly establish the Development link rather than relying on a closing
  keyword. Do not link a parent for closure unless its full scope is completed.
- Verify the labels, creator assignment and Development issue link before
  reporting the PR as opened.
