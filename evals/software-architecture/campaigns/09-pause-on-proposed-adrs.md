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
