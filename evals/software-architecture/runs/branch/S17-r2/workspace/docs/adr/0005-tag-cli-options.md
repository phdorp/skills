# 5. Tag the CLI with `--tag` on add and list

## Status

proposed

## Context

Users need to tag a note when they add it and to list only the notes with a given tag (R-1).
CLI command names and exit codes are decided centrally (ADR-0002); this adds options to two
existing commands. Contributors must be able to change the CLI without learning the whole
program (QG-3, QS-3), and the CLI reaches storage only through `Store` (ADR-0003). The storage
format of tags is decided in ADR-0004.

## Decision

We will add a repeatable `--tag` option to `notes add`, which stores each given tag on the new
note. We will add a `--tag` option to `notes list`, which shows only notes carrying that tag.
Command names, the output format, and exit codes stay as they are.

## Consequences

- Existing invocations of `add`, `list` and `search` work unchanged.
- `list --tag` with a repeated value (for example `--tag work --tag home`) needs a rule: this
  ADR proposes that it match notes carrying any of the given tags. The architect must confirm it.
- `search` does not gain a tag filter here; a later ADR is needed if it does.
- The tag-storage rules in ADR-0004 (no commas in a tag) bind this option.
