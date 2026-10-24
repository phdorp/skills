# "Cannot Verify From Diff" Items

Part of [executing-plans](../SKILL.md).

The task reviewer may report "⚠️ Cannot verify from diff" items — requirements that live in unchanged code or span tasks. These do not block the rest of the review, but you must resolve each one yourself before marking the task complete: you hold the plan and the cross-task context the reviewer lacks.

Check the item against the plan, the spec, and the ledger's earlier rulings. If it holds, say so in the completion line's review. If you confirm it is a real gap, treat it as a failed spec review — it enters the fix loop with the other findings.
