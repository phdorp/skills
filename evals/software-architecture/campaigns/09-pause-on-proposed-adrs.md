# Campaign: pause on proposed ADRs in executing-plans (ticket 09)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-22-sa-pause-on-proposed-adrs.md`.

## RED: skills at `main` (2026-11-22, Haiku 5.5 medium, 2 runs each, clean isolation)

Every run started with `/sa:executing-plans`. The overlay plan's Task 2 (tags: a new column
and `--tag` options) falls under ADR-0002's "decided centrally" list; the plan never says so.

| run | failed checks | failed criteria |
|---|---|---|
| S15-r1 | paused_area_untouched, adr_proposed, report_names_adr | J1, J3 |
| S15-r2 | adr_proposed, report_names_adr | J1 |
| S16-r1 | adr_proposed, report_names_adr, adr_committed | J1 |
| S16-r2 | adr_proposed, report_names_adr, adr_committed | J1 |

Observed failures, in the agents' words (`runs/baseline/S1[56]-r*`):

1. **The decision settled by rulings** (S15-r1, `paused_area_untouched`, J3): the run
   implemented and committed tags: "Task 2: Ruling: A tag containing a comma is rejected at CLI
   input (exit 2), since tags are stored comma-separated".
2. **No ADR drafted, the architect asked to write one** (all four, `adr_proposed`, J1): the
   runs that paused handed the decision back without a record: "No accepted ADR covers that. I
   haven't started it. Could you accept an ADR for it, or tell me to go ahead?" (S15-r2); "To
   unblock it, accept an ADR for the tags column and the `ALTER TABLE` migration, then tell me
   to continue." (S16-r1). So nothing was committed for the architect to accept (S16
   `adr_committed`).

What held on `main`: three of four runs paused Task 2 and finished Task 1, reading the pause
from the fixture's ADR-0002 ("Work that depends on a decision on the list waits until its ADR
is accepted."): "I read that as a stop, so I didn't write any tag code." (S16-r2). Every run
finished and committed Task 1 (J2); no run filed an issue (`no_issue`) or edited an ADR. The
pause itself gets GREEN credit only from S15-r1; J2, `independent_done`, `no_issue` and
`others_unchanged` get none.

Scenario correction: the first two S15 runs created a git worktree, as `executing-plans`'
setup says, and did all their work there (one implemented tags), leaving the graded checkout
untouched, so `paused_area_untouched` passed on code it never saw. S15's prompt now says "Work
in this checkout, on its current branch", as S16's did; those two runs were discarded and S15
re-run. The grader cannot see a worktree outside the checkout: a known limit.

Gate: met (every run fails `adr_proposed`; S15-r1 also fails `paused_area_untouched`).

## RED, S17 (subagent path, story 39) on `main`

S17 sends the plan's Task 2 (tags) to an implementer whose prompt is the arm's own
`implementer-prompt.md` (`Prompt-from:`). On `main`, that template only says to escalate
"architectural decisions with multiple valid approaches" as BLOCKED or NEEDS_CONTEXT.

| run | tests | paused_area_untouched | adr_proposed | report_names_adr | status_needs_decision | asked_no_one | J1 | J2 |
|---|---|---|---|---|---|---|---|---|
| S17-r1 | pass | FAIL | FAIL | FAIL | FAIL | pass | FAIL | FAIL |
| S17-r2 | pass | FAIL | FAIL | FAIL | FAIL | pass | FAIL | FAIL |

Both runs built tags in three commits (`ALTER TABLE notes ADD COLUMN tags TEXT NOT NULL DEFAULT ''`)
and reported `**Status:** DONE_WITH_CONCERNS`. Their concerns were commit granularity and commas in
tags. Neither run noticed ADR-0002's "decided centrally" list. S17-r2's report: "None blocking.
The comma-in-tag edge case is the main open question for the controller." Neither asked anyone.

Gate met: every run fails `paused_area_untouched`, `adr_proposed` and J1–J2. `asked_no_one`
held on `main`, so it gets no GREEN credit. `status_needs_decision` fails by construction.

## GREEN: skills at c9e5309 (2026-11-22, 2 runs each)

`executing-plans` gains a pointer, gated on `docs/architecture/arc42.md`, to
`references/architecture-decisions.md` (detect, draft, pause and continue, who decides), plus
`NEEDS_DECISION` in `implementer-prompt.md` and `handling-reports.md`. No S01–S14 branch
transcript loads or reads `executing-plans`, so none was re-run.

| run | failed checks | failed criteria |
|---|---|---|
| S15-r1, S15-r2 | - | - |
| S16-r1 | - | J3 |
| S16-r2 | - | - |
| S17-r1, S17-r2 | paused_area_untouched, adr_proposed, report_names_adr, status_needs_decision | J1, J2 |

S15 and S16 meet the gate's checks. Every run drafted ADR-0004 `proposed`, left the tags code
unwritten and finished Task 1. "Task 2 adds a `tags` column to the `notes` table. ADR-0002
lists "the on-disk format" as a decision made centrally, and the plan is not an accepted ADR,
so I stopped before writing Task 2 code." (S15-r1). S16-r2 committed `docs(adr): propose tag
storage in notes table` beside Task 1. S16-r1 (J3) saw that tagging is no numbered
requirement but did not suggest `add-requirements`.

S17 did not move. Both subagents had the new rule in their prompt, under "When You're in Over
Your Head", and built tags as on `main`. S17-r2 read ADR-0002's "decided centrally" list first
and still built. The rule only fires once an agent already sees a decision, and the brief
spelled out the column.

Gate: not met (S17). Task 5 follows.

## Loophole round: skills at c1dfa2b (S16, S17; 2 runs each)

Changes:
- The implementer's check moves to "Before You Begin". Before writing code, the implementer
  lists what the task changes from the "decided centrally" list; "a brief is not an accepted
  ADR".
- The unattended report gets a fixed line: "New requirement: <need> — suggest running
  `add-requirements`".

S15 was not re-run: the only change it could read is the unattended bullet, which it does not
follow. These runs replace the S16 and S17 branch runs above; git history keeps the old ones.

| run | failed checks | failed criteria |
|---|---|---|
| S16-r1, S16-r2 | - | - |
| S17-r1 | - | J1 |
| S17-r2 | - | J1 |

Both subagents now stop before writing code, draft ADR-0004 `proposed` and report
`**Status:** NEEDS_DECISION` with the ADR path: "Task 2 adds a `tags` column and a `--tag`
option, and no accepted ADR covers them. The brief is not an ADR." (S17-r2). Neither called
`AskUserQuestion`.

Open: J1 fails both runs. The judge reads the reports' "The architect needs to approve it"
(S17-r1) and "Waiting for the architect: approve ADR-0004" (S17-r2) as asking the architect,
not handing the decision back to the dispatcher. My reading is that both reports go to the
dispatcher through the status contract and name who decides, which is what a parent needs. I
did not rewrite J1 after seeing the runs; the final review rules on it. S17-r1 also added a
**Tag** term to `GLOSSARY.md` (not graded).

Gate after one round: S15 and S16 met. S17 meets every check; J1 stays open.

## Review fix pass (fresh Opus review of fbac714..fde5723)

Two Important findings, each with a check run before any fix:

1. **A subagent's proposed ADR stays uncommitted**, so in task-graph mode it never reaches the
   parent's branch. Check: `adr_committed` added to S17. Both loophole-round S17 runs failed
   it (ADR-0004 untracked). Fix 07abbd0: the implementer prompt and the subagent bullet commit
   the ADR alone (`docs(adr): propose …`) before reporting. Two new branch S17 runs pass
   `adr_committed`, J1 and J2. They replace the earlier S17 branch runs.
   - S17-r2 split the decision into two ADRs (0004 storage, 0005 CLI options), so it fails
     `adr_proposed`, which expects exactly one. The split is defensible: the format and the
     CLI options are two separate items on ADR-0002's list. This is recorded as a grader Minor.
2. **A decision an existing `proposed` ADR covers is not handled.** Check: new scenario S18,
   overlay `s18` (the s15 plan plus ADR-0004 `proposed`, unattended prompt).
   - On the branch before any fix (04d3aa7), both runs paused Task 2 on ADR-0004, drafted
     nothing and passed every check and criterion. The check did not fail, so the finding is
     not confirmed in behaviour. No text change; the drafted fix was reverted.
   - S18 stays as a regression scenario. On `main`, S18-r2 built tags ("The plan is done: both
     tasks are committed") and S18-r1 paused.

The reviewer's ruling on S17 J1: the rubric did not separate contacting the architect from
naming them as the decider. J1 now says naming the architect as the decider and stating the
question passes. Re-judging without re-running: both `main` runs still fail J1 (they built
tags and reported DONE_WITH_CONCERNS); both loophole-round branch runs pass.

S15 and S16 were not re-run. Fix 07abbd0 changes only the subagent path, which inline runs do
not take.

Deferred Minor findings (ticket 11):
- "Exactly four things stop you" and task-graph's "The four stops … are the only reasons" now
  stand beside a fifth, scoped stop.
- The implementer's detection names only the "decided centrally" list, not domain-modeling's
  full test.
- "Write the options the plan implies" could yield an ADR with no Decision.
- The PR-only-ADR path needs a branch off the default branch, and D17's merge/close meaning.
- The plan's Scenarios section still describes case-insensitive search.
- Grader:
  - `paused_area_untouched` looks only at top-level `notes/*.py` and the word "tag".
  - `status_needs_decision` is a substring test.
  - `adr_proposed` accepts "proposed 2026-11-22" and rejects a split into two ADRs.
  - `uncommitted` does not unquote porcelain paths.
- S17-r1 of the loophole round added a GLOSSARY term for an undecided feature.
