# "Record architecture decisions" ADR

The ADR that draws the line between decisions the architect makes centrally and decisions left
to whoever builds a block. It takes the next free number in the project's ADR directory (0001 in a
fresh project); skills find it by its title, never by its number. Format and status rules: `domain-modeling`.

```markdown
# <n>. Record architecture decisions

## Status

proposed

## Context

The architect decides the architecture; contributors and agents build it. <One sentence on
what this product needs from that line, citing the R- and QG-IDs it serves, e.g. "Sightings
must survive crashes (R-2, QG-1) and work everywhere with only Python (R-3, QG-2)".>

## Decision

We record architecture decisions as ADRs in `<the project's ADR directory>`, in Nygard form.

Decided centrally (needs an ADR the architect accepts):

- <items from the default list below, made concrete for this product>

Left to the building blocks (no ADR):

- <internal helpers, structure inside one block, test layout, …>

## Consequences

Work that depends on a decision on the list waits until its ADR is accepted.
```

## Default list

A decision is made centrally when it is expensive to change later or crosses a building-block
boundary. Start the list from these and keep the ones that apply:

- storage engine and on-disk or wire data formats;
- import and export formats;
- interfaces between building blocks, and the dependency rule between them;
- versioning of anything other systems or users depend on (APIs, file formats, CLI);
- crosscutting conventions: naming, units, error handling, logging;
- third-party dependencies.
