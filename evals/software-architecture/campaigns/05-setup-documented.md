# Campaign: setup-architecture on a documented project (ticket 05)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-21-sa-setup-documented.md`.

## Isolation fix found on the way

The first two baseline S07 runs saw the account's claude.ai "Claude Docs" connector, and r2
followed its instructions ("I did not create a Claude Docs document, since you asked for the
repo's documentation"). The init events showed the connector in 20 of the suite's 26 runs: every
branch run and baseline S02, S03 and S07. Runs now set `ENABLE_CLAUDEAI_MCP_SERVERS=false` and
`--strict-mcp-config`, and any MCP server fails isolation. The contaminated baseline runs of
S02, S03 and S07 were re-run; every branch run is re-run in this ticket's GREEN step. The S02
re-run changed ticket 02's RED record: see the addendum in
[02-adr-rules.md](02-adr-rules.md).

## RED: skills at `main` (2026-11-21, Haiku 5.5 medium, 2 runs, clean isolation)

`main` has no `setup-architecture`, so the plain prompt ran. Both runs kept one session over
both turns, with no MCP server and no skill loaded.

| run | failed checks | failed criteria |
|---|---|---|
| S07-r1 | `t1_only_arc42`, `arc42_links_existing`, `no_copy`, `legacy_upgraded`, `made_centrally_next`, `goals_measured` | J1–J4 |
| S07-r2 | all 7 | J1–J4 |

Observed failures, in the agents' words (`runs/baseline/S07-r*/transcript.md`):

1. **Turn 1 rewrote the documentation instead of proposing** (both): r1 wrote
   `docs/architecture.md` and changed the README; r2 "rewrote the architecture documentation
   against your five requirements", replacing the README's "How it works" text and writing
   three new ADRs (0003–0005) in turn 1, numbered into the slot the "made centrally" ADR needs.
2. **The README's architecture copied into a second document** (both fail `no_copy`): the
   modules and the "`cli` calls `catalog`" rule now live in two places.
3. **Legacy ADRs marked plainly `Accepted`, or left without a Status** (both fail
   `legacy_upgraded`): r1 "upgraded the ADRs" to `Accepted`; r2 left them untouched.
4. **No arc42 structure, no "made centrally" ADR, no measured goals** (both).
5. **Turn 2 found nothing to confirm**: "I can't find the plan you're confirming. I never
   proposed a triage, a ranking, quality goals, a document-to-section mapping, or an ADR
   upgrade." (r2)

What held on `main`: r1 kept every README line (it only added a link), and neither changed code.

Gate: met.

## GREEN: branch skills (commit 7ad6170, then c6c2ac2)

Every branch run was re-run with clean isolation (S01–S07, 2 each); S01–S05 stay at
1.000 / 1.000. Three first-attempt runs (S06-r2, S07-r1, S07-r2) lost turn 2 to the account's
5-hour usage limit ("You've hit your 5-hour limit"); the per-turn exit check failed them
("turn 2 exited 1") and they were re-run after the reset.

First S06/S07 round (commit 7ad6170): S07 passed every check in both runs, but neither said the
mapped documents stay where they are (J1). S06-r1 ranked R-2…R-5 without reasons (J1) and
filed a goal from the feature-level item ("R-6 (issue under R-1)"); S06-r2 filed two measured
goals and left the rest open, which the reply asked for, so `goals_measured` now accepts
1–5 goals (self-test `S06-twogoals`). That run was replaced by the re-run below before it was
committed; the self-test case is the only kept evidence.

Loophole round (commit c6c2ac2): the proposal now asks for a reason per rank, derives goals from
system-level requirements only, and says each mapped document "stays where and as it is".
Re-run of S06 and S07 (2 each):

| run | failed checks | failed criteria |
|---|---|---|
| S06-r1 | - | - |
| S06-r2 | - | J1 (R-4 ranked without a reason) |
| S07-r1 | `goals_measured` (QS-4 "the diff touches only cli.py and one new module") | J1 (section 9 and "stays" missing) |
| S07-r2 | `goals_measured` (QS-1 "each passes its acceptance test") | - |

What now holds in every S07 run: turn 1 wrote only arc42; the README stayed byte for byte;
both legacy ADRs became `accepted (legacy)` with "Decision text is unchanged" (r1); the
"made centrally" ADR is `docs/decisions/0003-record-architecture-decisions.md`,
`proposed`: "**Central-decision ADR (0003) awaits your approval.**" (r2). The mapping line
landed where the agent followed it: "README \"How it works\" → linked from arc42 sections 3
and 5. The README stays as it is." (r2).

## Open loopholes (one round spent)

1. **Unmeasured goals filed despite the confirmation reply** (S07 r1, r2): a pass/fail
   condition or "passes its acceptance test" is written as the measure. The scenario
   reference says a measure is a count, time, share or limit; the agent does not apply it to
   its own candidates. Next counter: the proposal lists each candidate's measure, and one that
   is not a number goes to the open questions.
2. **Proposal parts dropped under load** (S06-r2 one rank reason, S07-r1 the section 9 mapping
   and the "stays" line): the instructions are present and followed in the other runs; Haiku
   skips single items in a long proposal. A structural slot (a fixed proposal template with one
   row per item) is the matching form if it recurs.
