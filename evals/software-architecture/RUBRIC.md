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
