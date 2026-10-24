# Ticket Template

A ticket is a **tracer bullet**: a narrow but complete vertical slice through every layer, demoable or verifiable on its own, sized to one fresh context window.

One ticket per file, or one ticket per issue. Never combine several tickets in one artifact.

## Local file form

Path: `.scratch/<feature>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first).

```markdown
# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective. Not a layer-by-layer implementation list.

**Blocked by:** <numbers/titles of the tickets that gate this one, or "None (can start immediately)">

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

## Tracker issue form

- **Title**: `<Ticket title>`
- **Labels**: `ready-for-agent` unless instructed otherwise.
- **Parent**: the source spec or parent issue, when there is one.
- **Blocking**: the platform's native blocking relationship where it has one; otherwise write the blockers in the body and omit the section when native edges carry them.

```markdown
## Parent

<reference to the parent issue, if the source was an existing issue; omit otherwise>

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective. Not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- <reference to each blocking ticket, or "None (can start immediately)">
```

## Writing rules

- A completed ticket is demoable or verifiable by someone who did not build it.
- Each ticket cuts through schema, API, UI, and tests as needed. Avoid horizontal slices of one layer.
- Any prefactoring ticket comes first.
- Blockers are genuine gates, not merely related work.
- Prefer domain vocabulary from the project's glossary, and respect ADRs in the area.
- No specific file paths or code snippets; they go stale fast. Exception: a prototype-derived snippet that encodes a decision (state machine, reducer, schema, type shape), trimmed to the decision-rich parts and noted as coming from a prototype.

## Wide refactor form

A wide refactor (one mechanical change whose blast radius spans the codebase) does not fit a vertical slice. Sequence it as:

1. **Expand** ticket: add the new form beside the old. Nothing breaks.
2. **Migrate** tickets: one per batch sized by blast radius (package, directory). Each is blocked by the expand and keeps CI green.
3. **Contract** ticket: delete the old form once no caller remains. Blocked by every migrate ticket.

When batches cannot stay green alone, share an integration branch and add a final integrate-and-verify ticket that all batches block.
