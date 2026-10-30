---
name: finishing-a-development-branch
description: Use when implementation is complete, the suite passes, and the work needs integrating - verify tests, choose merge/PR/keep, execute it, clean up owned worktrees, and write the PR body.
---

# Finishing a Development Branch

**Core principle:** verify tests → detect the environment → confirm the base → present the menu → execute the choice → clean up.

Integration is your human partner's decision. Your job is to make the options concrete and the execution safe.

## Step 1: Verify the Tests

Run the project's full suite (`npm test`, `cargo test`, `pytest`, `go test ./...`, or whatever the repo documents). Run it on the tree you are about to integrate, not a result remembered from earlier in the session.

If tests fail, report and stop. The menu comes after a green suite:

```
Tests failing (<N> failures). Must fix before completing:

[show the failures]
```

Use [verification-before-completion](../verification-before-completion/SKILL.md): a green run only proves the tree it ran on.

## Step 2: Detect the Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Capture now, while still inside the workspace: Step 5 changes directory
# before cleanup, which needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

| State | Menu | Cleanup |
|---|---|---|
| `GIT_DIR == GIT_COMMON` (normal repo) | 3 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | 3 options | Provenance-based, Step 6 |
| `GIT_DIR != GIT_COMMON`, detached HEAD | 2 options (no local merge) | Externally managed — leave in place |

Inside a submodule the same comparison holds but the workspace is not a worktree. [using-git-worktrees](../using-git-worktrees/SKILL.md) carries the guard: if `git rev-parse --show-superproject-working-tree` prints a path, treat it as a normal repo.

## Step 3: Confirm the Base Branch

The base is whatever this work forked from — usually named in the plan, the conversation, or the branch's upstream. If it is not already known, ask: "This branch split from `<best guess>` — is that correct?" Confirm before merging or opening a PR. Merging into the wrong base is expensive to undo.

## Step 4: Present the Menu

**Normal repo and named-branch worktree — exactly these 3 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

**Detached HEAD — exactly these 2 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

Present the menu as written and wait. Every option comes from the list above; discarding is not on it.

## Step 5: Execute the Choice

### Option 1: Merge locally

```bash
# Work from the main repo root, not the worktree
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify the merged result, not just the branch
<test command>
```

If the merged result fails, stop. Leave the worktree and branch in place and investigate. Nothing has been pushed, so the merge is local and recoverable.

Once the merged result is green: clean up the worktree (Step 6), then delete the branch:

```bash
git branch -d <feature-branch>
```

### Option 2: Push and create a PR

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

Create the pull/merge request against `<base-branch>` with the forge's tooling — its CLI if available, otherwise the creation URL it prints on push. Follow the repo's PR template and conventions. Report the URL.

**Keep the worktree.** PR feedback gets fixed there; it stays until the work lands. A rejected push means the remote moved — investigate. Force-push only on an explicit request.

### Option 3: Keep as-is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

### If your human partner asks to discard the work

This path exists only in response to an explicit request to throw the work away. Confirm with the exact list of what dies:

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>, including uncommitted files

Type 'discard' to confirm.
```

Wait for that exact word. "Yeah, get rid of it" is not confirmation. When `discard` arrives, change to the main repo root, clean up the worktree (Step 6), and force-delete the branch:

```bash
git branch -D <feature-branch>
```

## Step 6: Clean Up the Workspace

Runs for Option 1 and for confirmed discards. Options 2 and 3 always preserve the worktree. Both callers have already changed to the main repo root — removal must run from outside the worktree — and use the `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` values captured in Step 2.

**`GIT_DIR == GIT_COMMON`:** normal repo, nothing to clean up. Done.

**`WORKTREE_PATH` under `.worktrees/` or `worktrees/`:** this collection created the worktree, so we own cleanup:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # clears stale registrations
```

**Removal refused** (`contains modified or untracked files`): the worktree holds files that exist nowhere else — uncommitted plans, notes, scratch work. Never `--force` on your own initiative. Show what is at stake:

```bash
git -C "$WORKTREE_PATH" status --porcelain -uall
```

```
Worktree removal refused — these files were never committed:

<file list>

1. Commit them to <branch> before cleanup
2. Move them into <main repo root>
3. Delete them (unrecoverable)

Which?
```

Carry out the choice, then remove the worktree.

**Anything else:** the host environment owns the workspace. Leave it in place. If your platform provides a workspace-exit tool, use it.

Never clean up worktrees you did not create. Other entries under `.worktrees/` may belong to another session.

## Writing the PR body

Use [references/pr-body.md](references/pr-body.md). Three sections: **Summary** as the smallest visual that makes the point (pseudocode, call tree, component tree, file tree, Mermaid, or a diff), **Evidence** as a before/after (screenshot, output, failing-then-passing test), and **Merge Danger** as door type and blast radius. Skip preambles, and use the project's own vocabulary.

## Quick Reference

| Option | Merge | Push | Keep worktree | Delete branch |
|---|---|---|---|---|
| 1. Merge locally | yes | — | no | yes (after merge verifies) |
| 2. Create PR | — | yes | yes | — |
| 3. Keep as-is | — | — | yes | — |
| Discard (typed request only) | — | — | no | yes (force) |

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Tests passed earlier this session" | Run the suite on the tree you are about to integrate. |
| "They obviously want it merged" | Integration is their decision. Present the menu and wait. |
| "They seem done — I'll offer to discard" | The menu is complete as written. Discard only on explicit request. |
| "'Yeah, get rid of it' counts as confirmation" | Only the typed word `discard` authorizes deletion. |
| "The PR is up, so the worktree is clutter" | PR feedback gets fixed in that worktree. It stays. |
| "This other worktree looks stale — I'll clean it too" | Clean only worktrees under `.worktrees/` or `worktrees/` that this work created. |
| "Removal refused, so `--force` finishes the cleanup" | The refusal means files exist only there. `--force` destroys them permanently. Ask. |
| "The merged-result failure is probably flaky" | A failing merged result stops everything. Investigate first. |
| "The push was rejected — force-push will fix it" | The remote moved. Investigate; force only on explicit request. |
