# Final Review and Finish

Part of [executing-plans](../SKILL.md). Every task is complete. This is the whole-branch review for subagent-driven mode and the closing review for task-graph mode; inline mode's variant is in [inline.md](inline.md).

Give the review a package: `bash scripts/review-package PLAN_FILE MERGE_BASE HEAD` (MERGE_BASE = the commit the branch started from, e.g. `git merge-base main HEAD`). Include the printed path in the dispatch so the reviewer reads one file instead of re-deriving the branch diff with git commands.

Dispatch on the most capable available model, using the `code-review` skill's review method: standards plus spec compliance. Give it the package path, the plan and spec paths, the plan's Review Focus section verbatim if it has one, and the ledger's deferred-minor, parked, and `Ruling:` lines so it can triage what must be fixed before merge.

## One Fix Wave

If the review returns findings, dispatch ONE fix subagent with the complete findings list — not one fixer per finding. Per-finding fixers each rebuild context and re-run suites; a real session's final fix wave cost more than all its tasks combined. Each fix is verified by TDD: the failing test first, then the fix, then the suite.

Then run exactly one scoped re-review of the fix wave: `bash scripts/review-package PLAN_FILE FIX_BASE HEAD` over the fix range, with [../re-review-prompt.md](../re-review-prompt.md).

Adjudicate any residual finding as the fix loop's breaker does ([fix-loop.md](fix-loop.md)): park it with a ruling, or rule on the load-bearing ones and ledger what you decided. Only the four stops at the top of SKILL.md stop you here. There is no second fix wave — residual load-bearing findings surface to your human partner when `finishing-a-development-branch` presents the options.

## Finish

Before you delete anything, collect every ledger line containing `Ruling:` — preflight rulings, parked findings, breaker adjudications, all of them — into your final message under "Rulings I made", in the order you made them, each with what it costs if wrong. Collect every `minor (deferred)` line under "Deferred minors". Both lists are exhaustive: if the ledger holds a ruling, the list holds it. That list is the only place the decisions you took on your human partner's behalf reach them — they read it and rework whatever you got wrong. A ruling that dies with the workspace was a decision made in secret.

When the final review is clean and its fixes are merged, delete this plan's workspace (`rm -rf <workspace>`) — the git history is the record now. Sibling directories belong to other plans; leave them alone.

Use `finishing-a-development-branch`.
