# Design dialogue in a set-up project

Part of [design-dialogue](../SKILL.md). A set-up project has `docs/architecture/arc42.md`: its
requirements, quality goals and decisions are the architect's, and the design works inside them.

## 1. Read

Read arc42 sections 1 (the R-list and the quality goals table), 5, 8 and 10, then every ADR in
the ADR directory that section 9 links, noting each one's status.

Done when you can name the requirement (`R-n`) the change serves, every quality goal (`QG-n`)
it touches, and every ADR in its area with its status.

## 2. Quality goals

The quality goals are the `QG-n` rows in arc42 section 1. A requirement (`R-n`) or a quality
scenario (`QS-n`) is not a goal: cite it beside the goal it belongs to, never in its place.

Before you lay out approaches, put this line in your message, with every goal the change
helps or hurts, and ask the architect to confirm it:

```markdown
**Quality goals this touches:** QG-1 <name> (<how the change bears on it>), QG-2 <name> (...)
```

Cite only IDs arc42 defines.

## 3. Structural choices

When an approach turns on a paradigm, an architectural or design pattern, or a decision on the
"Record architecture decisions" list, lay out 2–3 options, each in this form:

```markdown
**Option N: <name>.** <what it is>. Serves QG-x (<how>). Hurts QG-y (<how>).
```

Every option names at least one `QG-n` it serves or hurts. An option you cannot tie to a goal
is dropped before you write the message; if it matters to the architect, mention it after the
options as set aside, with the reason. Recommend one option and name the goal that decides it.
Once the architect picks one, record the choice as a proposed ADR through
[domain-modeling](../../domain-modeling/SKILL.md).

## 4. New requirements

A need the R-list does not cover, at system level (it constrains the whole system, like
encryption at rest or a new platform), is a new requirement. Name it as one and suggest that
the architect run `/add-requirements` with it. The R-list changes only through that skill, and
the architect starts it.

## 5. Proposed ADRs

A `proposed` ADR is an open decision. Name it as open wherever the design touches it, and build
the approaches so each one still stands if the architect rejects it.

## Red flags

| Thought | Reality |
|---|---|
| "The requirements and scenarios I cited cover the goals" | Name the `QG-n` they belong to. Requirements and scenarios support goals; they are not goals. |
| "This option has no goal, but it is worth listing too" | Tie it to a goal or set it aside after the options. |
| "The change needs a new capability, I'll add it to the requirements" | Suggest `/add-requirements`. The R-list changes only through it. |
