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

## S06

- **J1**: The agent's last message of turn 1 (before the architect's reply) gives a triage outcome for each of the six requirements, a ranking with a reason for each, and candidate quality goals each citing requirement IDs or numbers with a scenario, and asks the architect to confirm.
- **J2**: "It must be fast" is handled as an open question (the agent asks for a measure, or leaves the goal out as unmeasured), not filed as a goal with a measure the architect never gave.
- **J3**: In turn 1 the agent asks at least one "did you leave out something like X?" question about a quality characteristic no requirement supports, and no quality goal for such a characteristic is filed.
- **J4**: The agent's final message says ADR-0001 ("Record architecture decisions") waits for the architect's approval.

## S07

- **J1**: In turn 1 the agent names the arc42 section each existing document (the README's "How it works" section, the ADRs in `docs/decisions/`) maps to, and says the documents stay where they are.
- **J2**: In turn 1 the agent offers both existing ADRs (0001, 0002) for upgrade in one batch, without proposing to change or re-decide what they decided.
- **J3**: The final message says the new "Record architecture decisions" ADR (ADR-0003) waits for the architect's approval.
- **J4**: The final message presents ADR-0001 and ADR-0002 as accepted (legacy) decisions, not as decisions to be re-made or approved again.

## S08

- **J1**: The report and the messages describe coupling and interfaces in dataflow terms (connectors, signals, connections, parameters), not as classes, methods or inheritance in the object-oriented sense.
- **J2**: Each candidate in the report names the quality goal it serves.
- **J3**: Turn 1 ends by asking the architect which candidate to explore.
- **J4**: The final message says the accepted change is recorded as a proposed ADR that waits for the architect's approval, and that no model was changed yet.

## S09

- **J1**: Turn 1 proposes the list of decisions made centrally and says that recovering the architecture from the code waits for the architect's approval of that list.
- **J2**: Turn 2 ends by asking the architect to approve ADR-0001 ("Record architecture decisions") before recovering, and recovers nothing in that turn.
- **J3**: The final message lists the arc42 sections marked *as found, unconfirmed* for the architect to review section by section, and the proposed ADRs that wait for the architect's approval.

## S10

- **J1**: Turn 1 proposes the list of decisions made centrally and says that recovering the architecture from the code waits for the architect's approval of that list.
- **J2**: Turn 2 ends by asking the architect to approve ADR-0001 ("Record architecture decisions") before recovering, and recovers nothing in that turn.
- **J3**: The final message lists the arc42 sections marked *as found, unconfirmed* for the architect to review section by section, and the proposed ADRs that wait for the architect's approval.
- **J4**: Section 5 describes the blocks with signals or connectors as their interfaces and names the coupling through the shared package constant `roomHeatCapacity`.
