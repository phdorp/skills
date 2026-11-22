# Resuming From an Existing Ledger

Part of [executing-plans](../SKILL.md). This plan's workspace already has a ledger at `<workspace>/progress.md`.

If the ledger's first line names your plan file, tasks with a `Task <N>: complete` line are DONE — do not redo or re-dispatch them; resume at the first task without one. A task with a `Paused:` line resumes only once its ADR's Status is `accepted`; while it is `proposed` the task stays paused, and a `rejected` ADR needs the architect's direction. A task whose last line is a fix round is mid-loop: resume the loop at the next round.

A ledger whose first line names a different plan file — or a stray ledger at an older flat path such as `.skills/sdd/progress.md` — is another plan's progress: leave it in place and start your own, fresh.

After compaction, trust the ledger and `git log` over your own recollection. The commits it names exist in git even when your context no longer remembers making them.
