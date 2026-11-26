# Campaign: setup-architecture on a fresh project (ticket 04)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-21-sa-setup-fresh.md`.

S06 is the suite's first two-turn scenario: turn 2 is the architect's scripted reply, sent with
`claude -p --resume`. `workspace-t1/` is the workspace after turn 1.

## RED: skills at `main` (2026-11-21, Haiku 5.5 medium, 2 runs)

`main` has no `setup-architecture`, so the plain prompt ran (`invoked: false`). Both runs kept
one session over both turns (`meta.json` `session_ids`). No run loaded a skill.

| run | failed checks | failed criteria |
|---|---|---|
| S06-r1 | all 8 | J1, J3, J4 |
| S06-r2 | all 8 | J1, J3, J4 |

Observed failures, in the agents' words (`runs/baseline/S06-r*/transcript.md`):

1. **"Set up the architecture" read as "build it"** (both): turn 1 wrote a working package with
   tests and a single `ARCHITECTURE.md`, deciding storage on its own: "SQLite with one explicit
   transaction per write and `synchronous=FULL` … I chose this over an append-only text log"
   (r1). No arc42 document, no R-IDs, no ADR.
2. **Nothing proposed for the architect to confirm** (both): turn 1 ended with a finished
   design, not a triage, ranking or goal proposal. Asked in turn 2 to confirm "your triage and
   your ranking", both agents said there was none: "I did not propose a triage, a ranking, or a
   \"did you leave anything out\" list in this conversation, so I could not record those as
   confirmed." (r1)
3. **Goals filed from the raw list, not confirmed** (both): "I recorded the quality goals from
   those, in your original order, and treated them as the ones you confirmed." (r2)
4. **No decision record, no approval question** (both): J4 fails; neither final message names
   an ADR.

What held on `main` already: both runs left "It must be fast" without an invented target
(J2): "No latency target has been set. Needs a number" (r1). That rule earns no GREEN credit.

Gate: met (both runs fail `t1_only_skeleton`, `goals_measured` and `adr_0001`).

## GREEN: branch skills (commit 3ec497d)

Both runs started with `/sa:setup-architecture` and loaded `sa:quality-requirements` and
`sa:domain-modeling`; r1 also loaded `sa:add-requirements` for the triage checks. Each kept one
session over both turns.

| run | failed checks | failed criteria |
|---|---|---|
| S06-r1 | - (after the grader fix below) | - |
| S06-r2 | - | - |

Turn 1 wrote only `docs/architecture/arc42.md` in both runs and ended with the proposal: "Confirm
or change the triage outcomes and the wording of R-1 to R-5." (r1). "Fast" stayed open: "Open
question (no measure yet, so no goal row): Performance efficiency: time behaviour, from R-5."
(r2). Gap questions were asked, not filed: "Security (confidentiality): should sighting locations
be protected from other users on the same machine?" (r1). After the reply both wrote R-1…R-5,
four measured goals, the latest-first issue citing the logging requirement (R-2 in r1, R-1 in
r2), and ADR-0001 `proposed`: "ADR-0001 is
`proposed` and waits for your approval of its text." (r1)

Grader fix (no skill change): r1's QS-4 measure "the suite passes on all three OSes in CI" is
checkable but has no digit, so `goals_measured` failed it. `goals_measured` now also accepts
number words; self-test case `S06-wordmeasure`. The final review narrowed this (below).

Re-run of S01–S05 on the same commit, now that three new skills are visible to them: every
check and criterion passes. S02 loaded `sa:domain-modeling` in 2 of 2 runs, S03 2 of 2, S04 and
S05 loaded all three requirement skills, S01 loaded none.

## Final review fixes

The whole-branch review found three Important issues; each fix started with a failing test.

1. **Section 5 not started.** Spec story 1 and the ticket start sections 1, 5, 9 and 10 at
   setup; the skeleton left 5 empty. New check `section5_started` (self-test `S06-nosection5`)
   failed both GREEN runs. Counter (commit d983dc7): the skeleton writes section 5's empty
   `| block | responsibility | may use |` table in the first turn.
2. **Vague measures passed.** Number words such as `every` let "every command feels fast"
   through `goals_measured`. `grade.has_measure` now accepts digits, `zero`, or a quantifier
   over a counted number ("all three OSes"); unit tests list the vague phrasings it rejects.
3. **A failed turn left no trace.** `meta.json` kept only the last turn's exit code and counted
   a missing cost as 0. `run.turn_summary` now records `exit_codes`, keeps a missing cost as
   `null`, and a failed turn in a multi-turn run fails the run.

Re-run of S06 on the branch (2 runs, replacing the runs above): both pass every check and
criterion, with section 5 started in turn 1. One grader correction on the way: r2's ADR-0001
Context cited QS-1 and QS-2, which exist, and `adr_0001` counted only R- and QG-IDs as known;
it now counts existing QS-IDs too (self-test `S06-citesqs`).
