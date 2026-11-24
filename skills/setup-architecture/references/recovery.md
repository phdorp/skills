# Recovery: an undocumented project after the list is approved

Recovery turns code into a draft of its as-is architecture for the architect to review. It
starts in the turn in which the architect approves the "Record architecture decisions" ADR,
because that ADR's list decides which findings become ADRs. Everything you write is *found*,
not *decided*: the architect decides it by confirming it, section by section and ADR by ADR.

## 1. Accept the approved ADR

Mark the "Record architecture decisions" ADR `accepted YYYY-MM-DD` with today's date, as
`domain-modeling` describes. Its text stays exactly as the architect approved it; a decision you
would add to its list goes into your report as a proposal.

Done when its Status is the only line that changed.

## 2. Read the code

List what the code shows: its modules or blocks, what each one uses, its entry points, its
storage and data formats, its dependencies, its conventions (errors, units, naming). For
dataflow code (Modelica, Simulink, signal graphs) read it in its own terms with
`codebase-design` › Paradigms: blocks, signals and connectors as their interfaces, and coupling
through connections and shared parameters or constants.

Done when every source file belongs to a block you can name, with what it uses.

## 3. Fill arc42 with what you found

Fill sections 2–8 and 11 of `docs/architecture/arc42.md` with what the code shows. Section 5
gets one row per block in its table. For dataflow code, the table is
`| block | responsibility | in | out | may use |`: `in` and `out` name the block's input and
output connectors or signals, and a shared parameter or constant two blocks read is a row's
`may use` entry and a sentence under the table. Start each section you fill with the line:

```markdown
*As found, unconfirmed.*
```

In sections 2 and 3, the constraints and out-of-scope items the architect confirmed at setup
stay first, without the marker; what you found follows under it.

The marker stays until the architect confirms that section. A section the code says nothing
about stays empty. Sections 1, 9, 10 and 12 hold what the architect confirmed and carry no marker.

Done when every section you filled starts with the marker.

## 4. Propose ADRs for listed decisions

For each decision on the accepted list that the code has already made, write one ADR in the
project's ADR directory, next free number, status `proposed`. Its Context says the decision was
found in the code, names where, and cites the R- and QG-IDs it serves; its Decision states what
the code does. A decision off the list (an algorithm inside one block, a helper, a test layout,
the form of an equation) goes into arc42 only.

Done when each listed decision the code made has exactly one proposed ADR, and no ADR covers an
off-list decision.

## 5. Leave the code as it is

Recovery documents the code; it changes no file outside the documentation. What looks wrong (a
race, a hidden coupling, a missing check) goes into section 11 as a risk, for the architect to
decide on later.

Done when `git status` shows changes only under `docs/` (and `GLOSSARY.md`).

## 6. Report

End with these three lists, each under its own heading:

```markdown
**Sections to review, one at a time:**
1. Section 5, building blocks: <one line on what it claims>
2. ...

**Proposed ADRs to approve or reject:**
- ADR-0002 <title>: <the question it asks, e.g. "keep the append-only file?">

**Risks in section 11:**
- <risk>: <what it threatens>
```

List every section you marked *as found, unconfirmed*, in the order the architect should review
them.

Done when the architect can confirm or correct each section and approve or reject each ADR from
your message.
