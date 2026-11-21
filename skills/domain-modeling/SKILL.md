---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, making a decision that is expensive to change or crosses a module boundary, or recording, approving, rejecting, or superseding an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

## Architectural decisions

The architect decides the architecture; you draft the record. ADRs use the format in
[ADR-FORMAT.md](./ADR-FORMAT.md).

### When a decision needs an ADR

A decision is **architectural** when any of these holds:

- it is expensive to change later;
- it crosses a module boundary: interfaces, data formats, dependency rules, versioning, or
  crosscutting conventions such as naming, units, and error handling;
- it is on the project's list of decisions made centrally.

The list lives in the ADR titled "Record architecture decisions". Find it by that title in
`docs/adr/`, or through the link in arc42 section 9 (`docs/architecture/arc42.md`); its number
differs between projects. Read it before you decide anything it might cover.

A decision inside one building block is left to implementation and gets no ADR.

### Status belongs to the architect

Every ADR you write starts as `proposed`. That holds when the architect dictated the decision
(you still wrote its Context and Consequences and filled its gaps), when a team is waiting,
and when the architect is away. Their approval of the written record is what makes it
`accepted`.

| Event | What you write |
|---|---|
| The architect explicitly approves this ADR in the conversation | `accepted YYYY-MM-DD` |
| The architect rejects it | `rejected YYYY-MM-DD: <their reason in one line>`; the file stays |
| The architect changes a decision | a new `proposed` ADR whose Context names the ADR it replaces; the old ADR keeps `accepted` |
| The replacing ADR is accepted | the old ADR becomes `superseded by ADR-NNNN` |
| An existing ADR has no Status | treat it as accepted (legacy) |

Edit only the ADRs the architect's instruction names. When a decision affects another accepted
ADR, name it in the new ADR's Consequences and in your report. ADRs are never deleted.

Context cites the requirement and quality-goal IDs that already exist (`R-n`, `QG-n`, `QS-n`
in arc42 section 1 and 10). A requirement the architect has not confirmed is named in words and
listed in your report for them.

End your report with the ADRs that wait for the architect, each with its number, title, and
the question they answer by approving it.

| Thought | Reality |
|---|---|
| "The team needs it by morning, so I'll mark it accepted" | It stays `proposed`. The report tells the architect what to approve first. |
| "The architect stated the decision, so the ADR is accepted" | They decided the direction; the record holds your wording and your details. `proposed` until they approve it. |
| "I'll mark the old ADR superseded now" | The old ADR changes when the replacing ADR is accepted. |
| "I'll add the requirement to arc42 so I can cite it" | Requirements are the architect's. Cite existing IDs; name the new one in your report. |
| "This other ADR's wording is outdated, I'll fix it" | Name it in Consequences and the report; a changed decision is a new ADR. |
