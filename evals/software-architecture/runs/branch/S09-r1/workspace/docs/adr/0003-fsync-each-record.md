# 0003. Fsync each record before a command reports success

## Status

proposed

## Context

Found in `store._append`: each record is flushed and passed to `os.fsync` before the function
returns. Serves R-2 and QG-1.

## Decision

We will fsync each appended record before the command reports success (exit 0).

## Consequences

Each command waits for the disk. An item whose `add` returned success is written to disk, as far
as the file's data goes. The directory entry is not fsynced when the file is first created
(section 11), so this decision does not yet cover that case; closing it is a separate decision.
