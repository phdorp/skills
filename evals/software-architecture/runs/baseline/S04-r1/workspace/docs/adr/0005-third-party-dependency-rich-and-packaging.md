# 5. Third-party dependency `rich` and pip packaging

## Status

proposed 2026-11-21 — needs the architect's acceptance before any implementation

## Context

Requirement from this week's interviews: install with `pip install notes-cli`, and use the
`rich` library for coloured output.

- R-3 and the constraints in arc42 section 2: "Python 3.11 or later, standard library only."
- ADR-0002 lists "third-party dependencies" among the decisions made centrally.
- The repository has no packaging metadata (`pyproject.toml`); `pip install notes-cli` needs it.

## Options

A. **Accept `rich` as the first third-party dependency.** Requires changing R-3 and the
   constraint in arc42 section 2, and adds packaging (`pyproject.toml`, the `notes-cli`
   distribution name, and a `notes` console entry point).

B. **Package without `rich`.** `pip install notes-cli` works with the standard library only.
   Coloured output uses ANSI escape codes, switched off when stdout is not a terminal or when
   `NO_COLOR` is set. R-3 holds.

## Recommendation

Option B, unless the architect accepts that R-3 is no longer a requirement. The coloured-output
need is met without a dependency. Packaging (the `pip install` requirement) is needed under either
option and does not conflict with R-3.

## Decision

Pending: architect to choose A or B.

## Consequences

If A is accepted: R-3 and arc42 section 2 are rewritten, and the dependency list is pinned in
`pyproject.toml`. If B is accepted: `pyproject.toml` is added without dependencies, and a
small `notes/color.py` helper (kept out of `store.py`) handles ANSI output.
