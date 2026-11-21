# 3. Write the catalog atomically

## Context

A crash during a write must not leave the catalog truncated or half-written. Every add rewrites
the whole file, so a naive `open(..., "w")` would empty the file before the new content is in it.

## Decision

`catalog.save` writes the full list to a temporary file beside the catalog, then calls
`os.replace` to move it over the catalog. On POSIX this rename is atomic, so a reader or a
restarted process sees either the old catalog or the new one.

## Consequences

- A crash mid-write leaves the previous catalog intact. A stale `shelf.tmp` may remain and is
  overwritten by the next save.
- The write is not yet durable. The temp file and the directory are not fsynced, so a power loss
  just after the rename can lose the update. This is tracked in
  [ARCHITECTURE.md](../ARCHITECTURE.md#known-gaps).
- The temp file name is fixed, so concurrent writers are not supported.
