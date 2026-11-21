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
