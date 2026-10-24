# Task-Graph Execution

Mode 3. The work is published as a spec plus tickets, and the tickets are a graph with blocking edges — not a list of steps. There is always a **frontier** of tickets that are ready to be grabbed.

**Goal:** the whole spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

**Communication is sparse.** Talk to subagents through **context pointers**: the spec, the ticket, research notes, previous commits. Never duplicate what a pointer already reaches.

**Concurrency:** run implementer subagents in the background where the platform supports it. Independent tickets in independent worktrees do not conflict; two agents in one worktree always do.

## Setup

1. Read the spec and the tickets. Build the graph: each ticket's blocking edges, and therefore the starting frontier.
2. Create the integration branch from the repository's main line, and an isolated worktree for it with `using-git-worktrees`. Record it in the ledger (`Progress: plan — <spec>`, `Branch: integration`, `Frontier: <ticket ids>`) so a resumed session rebuilds the frontier instead of the graph.
3. Optionally dispatch an **exploration subagent** for the codebase or external reading the tickets demand. It must be able to write files, and it saves Markdown notes outside the repository, at a path every later subagent can read. Implementers then spend their turns implementing, not searching.
4. If the tracker closes work through pull requests, or the human asks for one, open a draft PR after the first merge lands — a branch with no commits ahead of main cannot open one. Mark it as closing the spec and its tickets.

## The Frontier Loop

Repeat until no tickets remain:

1. **Take the frontier.** Every ticket whose blockers are all merged is ready. Dispatch one implementer subagent per ready ticket, in parallel, each on its own branch in its own worktree cut from the integration branch.
2. **Let each implementer finish its ticket.** Its brief is the ticket plus the spec pointer, the interfaces already merged that it consumes, and the rulings in the ledger that touch it. It implements under `test-driven-development`, commits on its branch, and reports status, commits, and concerns — the full detail goes in its report file.
3. **Merge with a merger subagent.** When an implementer reports DONE, dispatch a merger — not the human, and not yourself — to merge that branch into the integration branch. The merger:
   - confirms the ticket's worktree is based on the current integration tip, merging the tip in if it has moved;
   - merges the branch, resolves conflicts in favour of the spec, and records every conflict resolution as a ruling;
   - runs the ticket's tests and the repository's full suite on the integration branch;
   - commits the merge and reports the resulting tip, the suite result, and anything it had to decide.
   A merger that finds a ticket's tests failing on the integration branch sends the ticket back to its implementer with the failure output; it does not patch around it.
4. **Recompute the frontier.** A merge unblocks tickets. Dispatch them immediately — do not wait for the rest of the frontier to drain. Record the new frontier in the ledger in the same message as the merge confirmation.
5. **Close the ticket** the way the tracker closes work — a closing commit message, a state change, or the PR's closing reference. A merged ticket that is still open is work nobody can account for.

A ticket that blocks on a decision rather than a merge gets a ruling, not a stall: decide, ledger `Ruling: <decision> — <why> — <cost if wrong>`, and unblock it. The four stops in SKILL.md are the only reasons to interrupt the human.

## Review and Finish

1. When every ticket is merged, run the whole-branch review over the integration branch against the spec: dispatch it with the `code-review` skill on the most capable available model, pointed at a review package (`bash scripts/review-package SPEC_OR_PLAN_FILE MERGE_BASE HEAD`) and the spec.
2. Fix every Critical and Important finding in a single implementer subagent — not one fixer per finding. Per-finding fixers each rebuild context and re-run suites; a real session's final fix wave cost more than all its tasks combined.
3. Re-grade the residual findings by effect, exactly as in [final-review.md](final-review.md). One fix pass, then rulings for what stands. There is no second wave.
4. If a draft PR exists, mark it ready for review. Otherwise resolve each ticket the way the tracker closes work and report the integration branch.
5. Remove every implementer worktree (`git worktree remove`, `git worktree prune`), delete this run's workspace directory, and hand off to `finishing-a-development-branch` for the merge into the main line.
6. Your final message carries every ruling and every deferred minor, as in SKILL.md's Completion section.

## Failure Modes to Watch

| Symptom | Cause | Fix |
|---------|-------|-----|
| Implementer's branch lacks recent integration commits | Worktree cut from a stale tip | Merger merges the tip in before merging out; if the test suite then fails, send it back to the implementer |
| Two implementers editing the same file | Frontier dispatched a ticket whose blockers were not actually merged | Merge through the merger before dispatching dependents; never "just this once" |
| Conflict resolution changes behaviour silently | Merger resolved by picking a side | Every resolution is a ruling in the ledger with its cost if wrong |
| Integration suite green, ticket tests never ran | Merger trusted the implementer's report | Merger runs the ticket's tests itself on the integration branch |
| Frontier empties with tickets open | The graph has a cycle, or a blocker is waiting on a decision | Rule on the cycle or the decision, ledger it, and unblock |
