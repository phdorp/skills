### user

Review the last commit.

### assistant

I'll read the diff.

### assistant

# Review of HEAD~1..HEAD

## Standards

- No findings.

## Spec

- No findings: `notes export PATH` writes one JSON line per note, atomically.

## Architecture

- Compliant with proposed ADR-0004: `Store.export` writes atomically.
- No findings against ADR-0001, ADR-0003 or arc42 §8.

Worst per axis: Standards none; Spec none; Architecture none.

### result (success)
