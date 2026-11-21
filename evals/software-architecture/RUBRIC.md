# Rubric

Judged criteria per scenario. The judge (`grader/judge.py`, Claude Opus 5.5) gives each
criterion a pass or fail and quotes the passage of the run that shows it. Deterministic checks
live in `grader/grade.py`, not here.

## S01

- **J1**: The agent neither asked for quality goals or quality requirements nor invented any (no quality goals, quality scenarios or ISO 25010 characteristics appear in its messages or files).
- **J2**: The agent created no architecture decision record (ADR) and did not propose writing one.
- **J3**: The agent's steps are those of an ordinary feature change (read code, test, implement, verify, commit); it ran no architecture setup, recovery or documentation step. One suggestion to run `setup-architecture` is allowed.
