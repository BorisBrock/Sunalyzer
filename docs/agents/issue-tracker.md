# Issue tracker: GitHub

Issues and PRDs for this repository live in GitHub Issues at `hothman7/Sunalyzer`. Use the `gh` CLI and pass `--repo hothman7/Sunalyzer` when the repository cannot be inferred from the working directory.

## Conventions

- Create: `gh issue create --repo hothman7/Sunalyzer --title "..." --body "..."`
- Read: `gh issue view <number> --repo hothman7/Sunalyzer --comments`
- List: `gh issue list --repo hothman7/Sunalyzer --state open --json number,title,body,labels,comments`
- Comment: `gh issue comment <number> --repo hothman7/Sunalyzer --body "..."`
- Label: `gh issue edit <number> --repo hothman7/Sunalyzer --add-label "..."`
- Remove a label: `gh issue edit <number> --repo hothman7/Sunalyzer --remove-label "..."`
- Close: `gh issue close <number> --repo hothman7/Sunalyzer --comment "..."`

Use a heredoc or body file for substantial multi-line issue bodies.

## Pull requests as a triage surface

**PRs as a request surface: no.**

GitHub shares one number space across issues and pull requests. If a reference is ambiguous, try `gh pr view <number>` and then `gh issue view <number>`.

## Skill operations

- When a skill says “publish to the issue tracker,” create a GitHub issue.
- When a skill says “fetch the relevant ticket,” read the GitHub issue with its comments and labels.
- Do not create or mutate issues unless the active task authorizes it.

## Wayfinding operations

A wayfinding map is an issue labelled `wayfinder:map`; its child tickets are GitHub sub-issues where supported.

- Child types use `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.
- Prefer GitHub’s native sub-issue and dependency features.
- If unavailable, link children through a task list and `Part of #<map>` text.
- Represent fallback blockers with `Blocked by: #<number>`.
- Claim work with `gh issue edit <number> --add-assignee @me`.
- A frontier ticket must be open, unassigned, and have no open blockers.
