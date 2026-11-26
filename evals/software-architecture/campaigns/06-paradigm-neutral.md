# Campaign: architecture scan of a dataflow project (ticket 06)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-21-sa-paradigm-neutral-vocabulary.md`.

## RED: skills at `main` (2026-11-21, Haiku 5.5 medium, 2 runs, clean isolation)

Both runs started with `/sa:improve-codebase-architecture` and kept one session over both
turns. r1 loaded `codebase-design`; r2 loaded no further skill. Neither loaded `domain-modeling`.

| run | failed checks | failed criteria |
|---|---|---|
| S08-r1 | `goals_cited`, `code_unchanged`, `adr_proposed` | J2, J4 |
| S08-r2 | `goals_cited`, `code_unchanged`, `adr_proposed` | J1, J2, J4 |

Observed failures, in the agents' words (`runs/baseline/S08-r*/transcript.md`):

1. **Accepting a candidate meant implementing it** (both): "Candidate A is implemented in the
   working tree." (r1); "I implemented candidate 1 (option A) in the working tree." (r2). Both
   edited `Room.mo`, `System.mo`, `Thermostat.mo`, `package.mo` and `package.order`.
2. **No ADR for a change to the parameter flow between blocks** (both): r2 reasoned it away:
   "Option A over option B, so no constant goes into `Interfaces` and no new ADR is needed."
3. **Candidates tied to design terms, not quality goals** (both fail `goals_cited`): neither
   report names a `QG-n`; the judge quotes "locality: plant values live with the room that owns
   them" (r1).
4. **Object-oriented framing of a Modelica fix** (r2, J1): "a variant is a new class that
   extends the base; `System` does not change."

What held on `main`: both found the intended friction (the thermostat reads the room's heat
capacity through a package constant), wrote the report to `/tmp`, left turn 1's workspace
unchanged, ended turn 1 with "Which of these would you like to explore?" (J3), read ADR-0001,
and kept it unchanged. These rules (`report_outside_repo`, `t1_unchanged`, `adr0001_unchanged`,
J3) get no GREEN credit.

Judge note: Modelica's own `extends` and `replaceable` are idiomatic, so J1 can only fail
framing that borrows the object-oriented reading (classes with methods, subclass variants).

Gate: met.

## GREEN, first attempt: skills at `deec33d` (2026-11-21, 2 runs)

Both runs loaded `codebase-design` and `domain-modeling`; both pass every check.

| run | failed checks | failed criteria |
|---|---|---|
| S08-r1 | - | - |
| S08-r2 | - | J1 |

r2 proposed the right Modelica seam in object-oriented words: "Add partial base classes with the
port contract, and declare the two components `replaceable` in `System`." Baseline r2 slipped
the same way ("a new class that extends the base").

Gate: not met (J1, r2).

## Loophole round

`codebase-design` names the dataflow seam in Modelica's terms (a `replaceable` block constrained
by a partial model that holds the port contract) and asks for each construct in the language's
own words. J1 stays as written. Both branch runs were replaced.

## GREEN: skills at `86ca20a` (2026-11-21, 2 runs, clean isolation)

Both runs loaded `codebase-design` and `domain-modeling`.

| run | failed checks | failed criteria |
|---|---|---|
| S08-r1 | - | - |
| S08-r2 | - | - |

Each report gives every candidate a quality-goal line citing existing IDs (QG-2, QG-3). After
the reply, both wrote `docs/adr/0002-*.md` as `proposed` with a `QG-n` in its Context and left
the `.mo` files unchanged: "Candidate 1 is now a proposed ADR, and the code is unchanged." (r1);
"the shared-value code stays as it is until the architect approves the ADR." (r2). Both describe
the coupling as "a package constant. Two blocks read it directly instead of receiving it through
a port or parameter" (r2).

Credit: `goals_cited`, `code_unchanged`, `adr_proposed`, J1, J2, J4 went RED → GREEN.
`report_outside_repo`, `t1_unchanged`, `adr0001_unchanged` and J3 held on `main` and get no
GREEN credit. With 2 runs per arm, a J1 slip back to object-oriented wording is not ruled out.

Gate: met.

## Final review fix pass: skills at `af42af5` (2026-11-21, 2 runs)

The final review found that GREEN r2 also rewrote `tests/check.mos` after acceptance ("I also
implemented the test-script change, which needed no decision"), unseen because
`code_unchanged` compared only `.mo` files. `code_unchanged` now covers every file except ADRs,
`GLOSSARY.md` and the report; `improve-codebase-architecture` ends the run with the ADR "including
parts the 'made centrally' list leaves to the blocks". The GREEN runs above were replaced.

| run | failed checks | failed criteria |
|---|---|---|
| S08-r1 | `code_unchanged` (`tests/SteadyStateTest.mo`, `tests/check.mos`) | J3 |
| S08-r2 | - | - |

r1 held the model change ("Held until you accept ADR-0002 … The model files are unchanged") but
built the test that guarded it: "The test and check script are finished, but the
`Thermostat`/`System` change is held." Its turn 1 ended on notes, not on the question (J3).

**Open loophole:** a safety-net test for the accepted change is written before the ADR is
accepted. One fix pass is spent; this stays open.

**Isolation gap:** r2 loaded `codebase-design` and `domain-modeling` without the `sa:` prefix,
from the machine's `~/.claude/skills/`, whose copies differ from the branch. The run shares
`HOME` with the machine (known gap); its pass rests partly on the installed skills.

Gate: not met (r1); reported as an open loophole.
