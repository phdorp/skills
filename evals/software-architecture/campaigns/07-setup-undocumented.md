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
