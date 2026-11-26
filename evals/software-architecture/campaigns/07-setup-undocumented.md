# Campaign: recovering an undocumented project (ticket 07)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-21-sa-setup-undocumented.md`.

## RED: skills at `main` (2026-11-21, Haiku 5.5 medium, 2 runs each, clean isolation)

`main` has no `setup-architecture`, so the plain prompt ran (as S06 and S07 did). All four runs
kept one session over three turns and loaded no skill.

| run | failed checks | failed criteria |
|---|---|---|
| S09-r1 | all 7 | J1, J2, J3 |
| S09-r2 | all 7 | J1, J2, J3 |
| S10-r1 | all 7 | J1, J2, J3, J4 |
| S10-r2 | all 7 | J1, J2, J3, J4 |

Observed failures, in the agents' words (`runs/baseline/S09-r*`, `S10-r*`, `transcript.md`):

1. **Recovery in turn 1, before any list was proposed** (all four, J1, `t1_only_arc42`): each run
   wrote a whole architecture document in turn 1 (`ARCHITECTURE.md`, `docs/architecture.md` or
   `docs/ARCHITECTURE.md`) and linked it from the README: "I'll write the architecture doc to
   describe this as it is, and link it from the README." (S10-r1).
2. **No "made centrally" list, no ADR-0001 to approve** (all four, J2, `t2_waits`): turn 2 asked
   for a proposal that never existed: "I don't have a proposal to confirm." (S10-r1); "Could you
   paste the triage, the ranking and the quality goals, or point me to where they live?" (S10-r2).
3. **Recovered content reads as decided** (all four, `recovered_marked`, J3): no arc42 file, no
   *as found, unconfirmed* marker; "**Rest of the architecture:** I had already recovered it from
   the code." (S09-r1).
4. **No ADR for any found decision** (all four, `recovery_adrs`): the S09 runs wrote only a
   generic ADR-0001, left `proposed` because "The approval text was not found in the repository
   or the conversation" (S09-r2); S10-r1: "I didn't create an ADR, because there isn't one to
   approve."
5. **No R-list, no measured goals** (all four, `goals_measured`).
6. **Documents outside `docs/`** (all four, `code_unchanged`): the README was edited in every run,
   and two runs wrote `ARCHITECTURE.md` at the root. No run changed a source file.

What held on `main`: no run changed source code, although both S09 runs found a real defect in
`store.py` (a torn last line swallows the next appended item) and said so: "I'll document the
architecture and record that as a known gap, without changing the code, since you asked for
documentation." (S09-r1). So `code_unchanged`'s RED rests on documentation written outside
`docs/` (the README and a root `ARCHITECTURE.md`), not on code. The "change no code" rule itself
gets no GREEN credit.

Fixture note: the torn-line defect was not planned. It stays as a realistic temptation to "fix
what you find" (Review Focus 3).

Gate: met (every run fails `t2_waits`, `recovered_marked` and `recovery_adrs`).

## GREEN, first attempt: skills at `1868390` (2026-11-21, 2 runs each, clean isolation)

All runs started with `/sa:setup-architecture`, kept one session over every turn and loaded
`sa:domain-modeling` and `sa:quality-requirements`, except S06-r2 and S10-r2, which loaded no
skill through the Skill tool (S10-r2 read `references/recovery.md` with `cat`). S06 and S07
were re-run because their skill changed.

| run | failed checks | failed criteria |
|---|---|---|
| S06-r1 | - | - |
| S06-r2 | - | J1 |
| S07-r1 | - | - |
| S07-r2 | - | - |
| S09-r1 | - | - |
| S09-r2 | - | - |
| S10-r1 | - | - |
| S10-r2 | - | J4 |

S10-r2 kept the skeleton's `| block | responsibility | may use |` table and named no block's
signals: "`Room` | lumped room air: stores heat, loses it through the walls | `Interfaces`; the
package constant `roomHeatCapacity`". S10-r1 named them in the responsibility column ("outputs
its temperature `T`, takes heating power `Q_heat`").

S06-r2 ranked R-3 to R-5 without a reason ("3. R-3 log from CLI: `3 (proposed)`."), against
`quality-requirements` › Rank, which this ticket does not change.

Gate: not met (S10-r2 J4; S06-r2 J1).

## Loophole round

`references/recovery.md` step 3 gives dataflow code a structural slot: section 5's table is
`| block | responsibility | in | out | may use |`, and a shared constant is a `may use` entry
plus a sentence under the table. S06-r2's slip is outside this ticket's change and is recorded
as an open loophole, not fixed here. The S09 and S10 branch runs were replaced.

## GREEN: skills at `39cb1f4` (2026-11-21, 2 runs each, clean isolation)

All four runs started with `/sa:setup-architecture`, kept one session over three turns and
loaded `sa:domain-modeling` and `sa:quality-requirements` (r1 of each also `sa:add-requirements`).
S06 and S07 keep their runs at `1868390`: the fix touches only `references/recovery.md`, which
the fresh and documented situations do not reach.

| run | failed checks | failed criteria |
|---|---|---|
| S09-r1 | - | - |
| S09-r2 | `goals_measured` | - |
| S10-r1 | - | J3 |
| S10-r2 | - | - |

Every run wrote only the skeleton in turn 1, wrote ADR-0001 `proposed` in turn 2 and stopped:
"Recovery from the code waits for that approval, and sections 2–8 and 11 stay empty until
then." (S10-r1). In turn 3 each accepted ADR-0001 with only its Status changed, marked every
filled section *As found, unconfirmed.*, wrote `proposed` ADRs only for listed decisions
(S09-r1 6, S09-r2 8, S10-r1 3, S10-r2 4) and left the code alone; S10-r1 noted the room settling 7 K below its set point as a risk, not a fix.
Both S10 runs fill the `in`/`out` columns (J4).

Open loopholes:

1. S09-r2 filed QG-4 with a measure that states no number ("every item expiring within N days
   is listed, none later, sorted by expiry"): ticket 05's "unmeasured goal filed" loophole,
   recurring under `quality-requirements`.
2. S10-r1's final message lists the proposed ADRs for approval but names the as-found sections
   only in a summary ("sections 2–8 and 11 are filled from the code, each starting with *As
   found, unconfirmed.*"), not as a review list (J3; `recovery.md` step 6).
3. S06-r2 (first attempt) ranked requirements without reasons (J1).

Credit: `t1_only_arc42`, `t2_waits`, `list_accepted`, `recovered_marked`, `recovery_adrs`,
`goals_measured` and J1–J4 went RED → GREEN. `code_unchanged` went RED → GREEN only through
documentation written outside `docs/`; no baseline run changed code, so "change no code" gets
no GREEN credit. With 2 runs per arm, J3's per-section review list is not reliable.

Limit of the scenario (final review): `recovery_adrs` bounds the recovered ADRs by the length
of the agent's own list, which the scripted reply confirms unread. Both S09 runs turned every
list item into an ADR (6 of 6, 8 of 8), and S09-r2 put relative-date input on the list as CLI
syntax, so the planned off-list temptation (`dates.py`) was out of play there. "Off-list
decisions get no ADR" is tested only by S09-r1 (which left "parsing internals in `dates.py`" to
the block) and the S10 runs, and a long confirmed list still yields a long review set (story
13's "manageable set" is not measured).

Gate: not met in full (open loopholes 1–3); one loophole round spent.
