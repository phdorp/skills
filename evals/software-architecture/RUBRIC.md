# Rubric

Judged criteria per scenario. The judge (`grader/judge.py`, Claude Opus 5.5) gives each
criterion a pass or fail and quotes the passage of the run that shows it. Deterministic checks
live in `grader/grade.py`, not here.

## S01

- **J1**: The agent neither asked for quality goals or quality requirements nor invented any (no quality goals, quality scenarios or ISO 25010 characteristics appear in its messages or files).
- **J2**: The agent created no architecture decision record (ADR) and did not propose writing one.
- **J3**: The agent's steps are those of an ordinary feature change (read code, test, implement, verify, commit); it ran no architecture setup, recovery or documentation step. One suggestion to run `setup-architecture` is allowed.

## S02

- **J1**: The agent's final message presents the new ADR as proposed and waiting for the architect's approval, not as final or accepted.
- **J2**: Before deciding, the agent read the "Record architecture decisions" ADR (ADR-0002) or the arc42 document that links it.
- **J3**: The ADR's Context names the requirement or quality goal the decision serves, by its ID (R-n, QG-n or QS-n).

## S03

- **J1**: The agent carried out each of the architect's three instructions (approve ADR-0004, reject ADR-0005 with the given reason, record the move off SQLite as a new ADR) and changed no other decision.
- **J2**: The agent did not mark the new ADR about leaving SQLite as accepted, and did not mark ADR-0001 as superseded yet; its final message says the new ADR waits for the architect's approval.

## S04

- **J1**: The agent identifies the sync requirement (1) as a duplicate of the deferred R-4.
- **J2**: The agent names R-3 or the standard-library-only constraint as conflicting with the `rich`/pip requirement (2).
- **J3**: The agent names ADR-0001 (SQLite storage) as conflicting with the text-editor requirement (3).
- **J4**: The agent proposes one outcome (system-level, feature-level, deferred or rejected) for each of the five requirements and asks the architect to confirm before changing anything.

## S05

- **J1**: The final message asks the architect whether encryption needs a security quality goal (with a proposed scenario and measure, or an open question for the measure) instead of adding one.
- **J2**: The agent proposes a rank for the new active requirements and asks the architect to set the order.
- **J3**: The agent says that work depending on the storage change waits for the new ADR's approval.
