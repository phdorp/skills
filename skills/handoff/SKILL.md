---
name: handoff
description: Compact a session into a handoff document, or seed a fresh background agent with it.
metadata:
  opencode/autoinvoke: false
---

# Handoff

Two modes, same content:

1. **Handoff document** — a file another agent or person picks up later.
2. **Fresh background agent** — write that file, then start an agent with it as its prompt.

The next agent starts with none of this conversation. Everything it needs must be in the handoff or reachable from it.

## What to carry over

- **Goal and current state.** What the work is meant to achieve, what is done, what is verified, what is known broken. Evidence, not optimism.
- **Next action.** The first concrete step, with the command or file path. Not "continue the refactor".
- **Decisions and why.** Choices already made, and the alternatives rejected. This is what stops the next agent relitigating them.
- **Open questions.** Anything waiting on a person, with who and what.
- **Artifacts, by reference.** Spec, plan, ADR, issue URL, branch name, commit SHAs, worktree path, failing test command, logs, screenshots. Give absolute paths or URLs.
- **Environment facts.** How to run tests, build, and lint; ports; env var names (never values); services that must be running.
- **Suggested skills.** Name the skills the next agent should load and when: [systematic-debugging](../systematic-debugging/SKILL.md) for the failing parser test, [test-driven-development](../test-driven-development/SKILL.md) before the next fix, [code-review](../code-review/SKILL.md) before merge.

## What to omit

- The narrative of the conversation: what you tried, in what order, how you felt about it.
- Dead ends, except as a one-line conclusion ("tried X; rejected because Y") so they are not retried.
- Content already in an artifact. Reference the spec, plan, ADR, issue, commit range, or diff instead of pasting it.
- Large file contents, full diffs, and logs. Point at them; paste only the excerpt that proves the state.
- Secrets: API keys, tokens, passwords, personal data, private URLs. Redact them. In mode 2 the document becomes another agent's prompt, so treat it as public.

## Mode 1: Handoff document

Write to the OS temp directory, not the workspace: `$TMPDIR` if set, else `/tmp` (`%TEMP%` on Windows).

```bash
dir="${TMPDIR:-/tmp}"
file="$dir/handoff-<topic>-<date>.md"
```

Tailor the document to the arguments the user passed: they describe what the next session will focus on. A handoff for "finish the migration" leads with migration state; a handoff for "review this branch" leads with the range and the spec.

Structure it in whatever order serves the next reader, but do not drop the suggested-skills section or the artifact pointers.

When done, report the absolute path, a one-line summary, and the first command the next agent should run. Do not paste the document into the chat.

## Mode 2: Fresh background agent

Write the summary to the temp directory first, then seed an agent with it. For a Claude Code CLI background agent:

```bash
claude --bg --name "<descriptive name>" -- "$(cat <summary file>)"
```

- `--` before the prompt stops the CLI parsing the summary as flags.
- `"$(cat <file>)"` passes the file as one argument, so the shell does not execute backticks or expand `$` inside the summary.
- Always pass `-n`/`--name` with a descriptive name; it sets the display name in the job list, session picker, and terminal title.
- It starts in the current working directory and returns immediately. The user manages it with `claude agents`.

Other harnesses have their own background or new-session entry point. Seed it with the same file, in the same working directory, and keep the same content rules.

**Point at the transcript.** If the harness keeps a session transcript or log, give its path or URL and say what to look for in it. Do not hand over the raw transcript as the prompt: it carries your dead ends and burns the new agent's context. Artifacts the new agent can read are better than a retelling.

**Verify it started**, then report:

- the job appears in the harness's job list with the name you gave it;
- its first output or log references the right branch, worktree, or task — proof it read the summary rather than starting cold;
- it did not exit immediately on a shell, permission, or path error.

If it started with the wrong context, fix the document and start again rather than coaching the running agent through the gap. If it failed to start, report the error and leave the document in place — the user can continue in Mode 1.

## Before you hand off

- Re-read the document as someone with no context: is the first step unambiguous?
- Check every path and URL resolves now, from the working directory you name.
- Confirm nothing sensitive survived the redaction pass.
- Run [verification-before-completion](../verification-before-completion/SKILL.md) on any claim in the document that work is done or tests pass.
