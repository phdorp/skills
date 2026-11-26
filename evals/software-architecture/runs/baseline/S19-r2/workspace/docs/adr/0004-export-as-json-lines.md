# 4. Export notes as JSON lines

## Status

accepted 2026-11-20

## Context

People want to take their notes to other tools. Several export formats were possible: CSV,
one JSON document, or one JSON object per line.

## Decision

`notes export` prints every note as one JSON object per line, with the fields `id`, `text`
and `created`, oldest first.

## Consequences

Other tools can read the export line by line. A note containing a newline stays on one line,
because JSON escapes it.
