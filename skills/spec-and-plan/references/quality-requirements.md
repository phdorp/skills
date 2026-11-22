# Quality Requirements in a set-up project

Part of [spec-and-plan](../SKILL.md). A set-up project has `docs/architecture/arc42.md`; the
spec says which of its requirements, quality scenarios and decisions the work rests on.

## Read

The R-list and quality goals in arc42 section 1, the quality scenarios (`QS-n`) in section 10,
and every ADR with its status.

## Write the section

Add this section to the spec after Testing Decisions. Cite by ID; arc42 and the ADRs hold the
text, so a scenario's measure stays there.

```markdown
### Quality Requirements

- **Serves:** <R-n, the parent requirements>
- **Keeps:** <QS-n, the quality scenarios the work must still meet>
- **Builds on:** <ADR-nnnn, the accepted ADRs it relies on>
- **Blocked by:** <ADR-nnnn, each proposed ADR that settles a decision the work needs>
```

A proposed ADR is an open decision: list it under **Blocked by**, mark the spec's status as
blocked on it, and say so in your final message. The spec builds on it once the architect
accepts it.

## Red flags

| Thought | Reality |
|---|---|
| "The design says ADR-0004, so the spec follows it" | A proposed ADR is open. List it under Blocked by until the architect accepts it. |
