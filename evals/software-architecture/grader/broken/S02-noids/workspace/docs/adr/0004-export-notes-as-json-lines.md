# 4. Export notes as JSON Lines through a `notes export` command

## Status

proposed

## Context

Users want to back up their notes and move them to other tools.

## Decision

Add a `notes export FILE` command. It writes one JSON object per note per line (`id`, `text`,
`created`). `cli` calls a new `Store.export` method; only `store` reads the notes (ADR-0003).

## Consequences

Any tool that reads JSON can import the notes. A new command name and exit codes follow
arc42 section 8.
