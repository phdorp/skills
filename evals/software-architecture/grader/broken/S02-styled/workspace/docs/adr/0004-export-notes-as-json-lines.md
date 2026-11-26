# 4. Export notes as JSON Lines through a `notes export` command

**Status:** Proposed

**Context:** Users want to back up their notes and move them to other tools (R-1). The export must use only
the standard library (R-3, QG-2) and must not leave a partial file after a crash (R-2, QG-1).
Export formats and CLI command names are decided centrally (ADR-0002).

**Decision:** Add a `notes export FILE` command. It writes one JSON object per note per line (`id`, `text`,
`created`). `cli` calls a new `Store.export` method; only `store` reads the notes (ADR-0003).

**Consequences:** Any tool that reads JSON can import the notes. A new command name and exit codes follow
arc42 section 8.
