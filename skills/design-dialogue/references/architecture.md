# Design dialogue in a set-up project

Part of [design-dialogue](../SKILL.md). A set-up project has `docs/architecture/arc42.md`: its
requirements, quality goals and decisions are the architect's, and the design works inside them.

## 1. Read

Read arc42 sections 1 (the R-list and the quality goals), 5, 8 and 10, then every ADR in the
ADR directory that section 9 links, noting each one's status.

Done when you can name the requirement (`R-n`) the change serves, every quality goal (`QG-n`)
it touches, and every ADR in its area with its status.

## 2. Quality goals

Before you lay out approaches, name the quality goals the change touches by ID, including any
goal it would hurt, and ask the architect to confirm the list. Cite only IDs arc42 defines.

Done when your message names each touched `QG-n` with one line on how the change bears on it.

## 3. Structural choices

When an approach turns on a paradigm, an architectural or design pattern, or a decision on the
"Record architecture decisions" list, lay out the options in that form:

- 2–3 options, each with the `QG-n` it serves and the `QG-n` it hurts;
- one recommended, with the goal that decides it.

An option you cannot tie to a quality goal is not an option here: drop it. Once the architect
picks one, record the choice as a proposed ADR through
[domain-modeling](../../domain-modeling/SKILL.md).

## 4. New requirements

A need the R-list does not cover, at system level (it constrains the whole system, like
encryption at rest or a new platform), is a new requirement. Name it as one and suggest that
the architect run `/add-requirements` with it. The R-list changes only through that skill, and
the architect starts it.

## 5. Proposed ADRs

A `proposed` ADR is an open decision. Name it as open wherever the design touches it, and build
the approaches so each one still stands if the architect rejects it.
