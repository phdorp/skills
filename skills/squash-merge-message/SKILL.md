---
name: squash-merge-message
description: Use when squash-merging a pull request, or writing the commit message a squash merge lands on the default branch. Triggers include "merge the PR", "squash and merge", "close the PR", and "write the merge commit message".
---

# Squash-Merge Message

A squash merge turns a whole pull request into one commit on the default branch. That commit is what release tooling such as release-please reads, so its message serves two readers:

| Reader | Reads | Wants |
|---|---|---|
| **User** of the released software | The changelog and release notes | What changed for them, and what they must do about it |
| **Developer** of the codebase | `git log` and `git blame` | Why the change was made, how it works, and what to watch for |

Release tooling publishes only the **changelog parts** of the message: each conventional-commit header's description, and each `BREAKING CHANGE:` footer. The body never reaches the changelog. So every user-relevant fact goes in a changelog part, and the body is for developers.

Format rules (types, the 50-character header, 72-column body, `Closes:`/`Refs:` footers) come from [conventional-commits](../conventional-commits/SKILL.md). This skill decides what goes where.

## 1. Inventory the user-visible changes

Read the pull request's net diff against its base (`gh pr diff <n>`), not the list of branch commits. Branch commits record how the work happened (`test:`, `refactor:`, fix-ups) and are not changes a user can see.

List every change a user of the released software would notice: new or removed features, changed defaults, changed output, logging, or error messages, fixed bugs, raised version floors, and anything that requires them to change their code or configuration. List internal changes (tests, refactors, docs for maintainers, CI) separately.

Done when every changed public behaviour, default, and message in the diff is in one of the two lists.

## 2. Write one changelog entry per user-visible change

Each entry is a conventional-commit header: type, optional scope, and a description written for the user.

- Describe the outcome the user sees, in the vocabulary of the user-facing docs: `fix: abort chattering simulations instead of hanging`, not `fix: pass -abortSlowSimulation in _build_flags`.
- Pick the type from the user's point of view: `feat` for a capability they gain, `fix` for a defect they no longer hit (including information that was wrongly hidden), `perf` for speed they notice. Internal changes get no entry of their own; they go in the body.
- Keep every entry within 50 characters. The header's limit excludes the ` (#<n>)` suffix GitHub appends.
- The most important change becomes the **header** of the message.
- Every other entry becomes an **additional entry** at the bottom of the message (step 4). Release-please turns each one into its own changelog line.

## 3. Write the body for developers

The body explains the change to someone reading history later: the problem, the approach and why it was chosen, trade-offs, and limits. Mention the internal changes from step 1 here. Leave out the branch's commit list.

## 4. Assemble the footers and additional entries

Order the message as follows:

```
<header>

<body>

BREAKING CHANGE: <what breaks and what the user must do>
Closes: #<issue>

<type>[(<scope>)]: <additional entry>

<type>[(<scope>)]: <additional entry>
  BREAKING CHANGE: <a break that belongs to this entry>
```

- **Breaking change**: a change that forces users to edit their code, configuration, or workflow to keep working. Mark it with `!` on its header and a `BREAKING CHANGE:` footer under that header. Write the footer as a migration note for the user: what stopped working and what to do instead. Give each break its own footer. When the pull request marks itself breaking, write a footer for every break it names; when you and the pull request disagree, ask.
- `Closes:` and `Refs:` follow [conventional-commits](../conventional-commits/SKILL.md). Close an issue the pull request resolves. The pull request number is already in the header suffix.
- Additional entries come last, one blank line apart. A footer that belongs to an additional entry is indented by two spaces under it.
- Keep the trailers the session or user requires (for example `Co-Authored-By:`) on the last lines, after the additional entries.

Done when every item in the user-visible list from step 1 appears in exactly one changelog part, and every internal item appears in the body.

## 5. Merge with the message

Pass the header and the rest separately so GitHub keeps the message instead of building its default from the branch commits:

```bash
gh pr merge <n> --squash --subject "<header> (#<n>)" --body-file - <<'EOF'
<body, footers, additional entries, trailers>
EOF
```

To correct a message after the merge, edit the pull request description and add the corrected message between `BEGIN_COMMIT_OVERRIDE` and `END_COMMIT_OVERRIDE` lines; release-please uses it on its next run.

## Example

A pull request adds a dry-run mode to a sync tool, shows progress, fixes a config lookup, and starts rejecting unsafe targets:

```
feat: add a dry-run mode to sync (#57)

Users could not preview what sync would delete. The planner already
built the full action list before executing it, so --dry-run prints
that list and stops; no second code path exists to drift. The config
loader now resolves paths through one helper, which the new fallback
and the target check both use.

feat: show progress while syncing

fix(config): fall back to ~/.syncrc

fix!: reject sync targets outside the workspace
  BREAKING CHANGE: sync now refuses targets outside the workspace
  root. Move the target inside the workspace, or pass
  --allow-outside to keep the old behaviour.
```

## Check before merging

- [ ] Every user-visible change has its own header or additional entry; none lives only in the body.
- [ ] Every description reads as a changelog line for a user, in the user-facing vocabulary.
- [ ] Every breaking change has `!` on its entry and a `BREAKING CHANGE:` footer that tells the user what to do.
- [ ] The body explains why and how for developers and carries the internal changes.
- [ ] The header fits within 50 characters before ` (#<n>)`.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "The body mentions it" | The changelog never shows the body. A user-visible change that lives only there is missing from the release notes. |
| "One header is enough for one PR" | One PR often ships several user-visible changes. Each needs its own entry. |
| "The PR title is the header" | A PR title is written for the reviewer. Rewrite it for the user, and cut it to 50 characters. |
| "GitHub's default body lists the commits" | Branch commits record how the work happened. Replace them with the body from step 3. |
| "Internal refactors deserve a changelog line" | Users cannot see them. They go in the body. |
