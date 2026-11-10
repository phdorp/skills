---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Where a claim can be checked by running something (a small model, a script, a downloaded test file), run it and report the result next to the claim. Keep scratch files and downloads in its own `mktemp -d` directory, outside the repo.
3. Write the findings to a single Markdown file, citing each claim's source and marking every claim it could not check.
4. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
5. Commit the note alone on a `research/<topic>` branch in its own worktree (`using-git-worktrees`), with a `docs:` message. Don't push and don't open a PR unless the user asks. The note then reaches every later worktree through its branch, not as an untracked file in one checkout.

Its final report names the branch, the commit, and the note's path.
