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

A proposed ADR is an open decision: list it under **Blocked by**, and say so in your final
message. While **Blocked by** lists an ADR, the spec's status line reads
`Status: blocked (ADR-nnnn)`, and a tracker issue gets the blocked marking instead of
`ready-for-agent`. The spec builds on the decision once the architect accepts the ADR.

## Red flags

| Thought | Reality |
|---|---|
| "The design relies on a proposed ADR, so the spec follows it" | A proposed ADR is open. List it under Blocked by until the architect accepts it. |
| "Blocked is in the notes, so the status can say ready-for-agent" | The status line is what an agent reads first. It says blocked until **Blocked by** is empty. |
