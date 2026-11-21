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
| S06-r1 | all 7 | J1, J3, J4 |
| S06-r2 | all 7 | J1, J3, J4 |

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
