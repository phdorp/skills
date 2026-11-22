# Architectural decisions during execution

Part of [executing-plans](../SKILL.md). A project with `docs/architecture/arc42.md` has an
architect, and the architecture is theirs to decide. A decision a task needs that no accepted
ADR settles is a fifth stop: it pauses only the tasks behind it.

## 1. Detect

Before each task, and whenever a step makes a choice its brief does not spell out, apply
[domain-modeling](../../domain-modeling/SKILL.md)'s "When a decision needs an ADR" test,
including the list in the ADR titled "Record architecture decisions". A choice inside one
building block is not architectural: rule on it as usual.

An architectural choice an `accepted` ADR settles → follow the ADR and proceed. Otherwise it is
an open decision. The plan and the ticket do not settle it: they are not accepted ADRs.

Done when every task you start has passed this test, or has its open decision.

## 2. Draft

Call the Skill tool with "domain-modeling" and write the decision as the next ADR in the ADR
directory, Status `proposed`, its Context citing the requirement and quality-goal IDs that
exist. Write the options the plan implies; leave the choice to the architect.

Done when the ADR file exists with five fields and Status `proposed`.

## 3. Pause and continue

Write one ledger line per task that depends on the decision:

```
Paused: Task N — waits for ADR-NNNN (<the question the architect answers>)
```

Leave its code unwritten. Then finish, test and commit every task that does not depend on it.

Done when every independent task has its completion line and every dependent task a `Paused:`
line.

## 4. Who decides

- **Architect in the conversation:** in the message that reports the ADR, ask them at once to
  accept or reject it, and say which tasks each answer unblocks. Then keep going on the
  independent tasks.
- **Nobody in the conversation** (an overnight or background run, a ticket, a handoff): commit
  the ADR alone on the working branch (`docs(adr): propose <title>`). When the remote takes pull
  requests, also open one with only the ADR. File no tracker issue: the ADR is the record. End
  with a final report that lists the ADR as proposed, the paused tasks, and what accepting it
  unblocks. When the change serves a need no `R-n` in arc42 section 1 names, add a line
  "New requirement: <need> — suggest running `add-requirements`".
- **You are a subagent:** the architect is not yours to contact. Commit the ADR alone
  (`docs(adr): propose <title>`) so it reaches your parent's branch, then report
  `NEEDS_DECISION` to the agent that dispatched you, with the ADR's path, the question, and the
  part of the task that waits.

When a subagent reports `NEEDS_DECISION`, apply sections 3 and 4 as the parent: ledger the
`Paused:` line and take it to the architect, or commit and report it.

## Red flags

| Thought | Reality |
|---|---|
| "The plan says add a column, so it's decided" | A plan is not an accepted ADR. Draft the ADR. |
| "I'll rule on it, rulings are how this skill works" | Rulings settle plan conflicts. An architectural decision waits for the architect. |
| "Nobody is here, so I'll decide and keep going" | Commit the proposed ADR, finish the independent tasks, report. |
| "The whole plan is blocked now" | Only the tasks behind the decision wait. Finish the rest. |
