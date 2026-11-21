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
