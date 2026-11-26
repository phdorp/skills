# Handling a Report That Isn't DONE

Part of [executing-plans](../SKILL.md). Applies to subagent-driven mode, and to any subagent mode 3 dispatches.

**DONE_WITH_CONCERNS:** The implementer completed the work but flagged doubts. Read the concerns before proceeding. If they are about correctness or scope, address them before review. If they are observations ("this file is getting large"), note them and proceed to review.

**NEEDS_CONTEXT:** The implementer needs information that was not provided. Provide the missing context and dispatch again.

**NEEDS_DECISION:** The implementer met an architectural decision and wrote it as a proposed ADR. Apply [architecture-decisions.md](architecture-decisions.md) as the parent: pause the tasks behind it and take it to the architect, or commit and report it.

**BLOCKED:** The implementer cannot complete the task. Assess the blocker:

1. If it is a context problem, provide more context and dispatch again with the same model.
2. If it needs more reasoning, dispatch again with a more capable model.
3. If the task is too large, break it into smaller pieces.
4. If the plan itself is wrong, rule on the correction, ledger it, and dispatch again with the ruling carried in the dispatch.

Never ignore an escalation or force the same model to retry unchanged. If the implementer said it is stuck, something must change.
