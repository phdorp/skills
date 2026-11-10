# Merger Subagent Prompt Template

Use this template in task-graph mode when an implementer reports DONE. One merger per merge, and only one merge into the integration branch at a time.

```
Subagent (general-purpose):
  description: "Merge ticket N into integration"
  model: [MODEL — REQUIRED: choose per SKILL.md Model Selection; a clean
         merge needs only a cheap model]
  prompt: |
    You are merging ticket N ([ticket title]) into the integration branch.

    - Ticket branch: [TICKET_BRANCH], worktree [TICKET_WORKTREE]
    - Integration branch: [INTEGRATION_BRANCH], worktree [INTEGRATION_WORKTREE]
    - Spec (binding authority for conflicts): [SPEC_FILE]
    - The ticket's tests: [TICKET_TESTS]
    - Full check commands: [CHECK_COMMANDS]

    ## Steps

    1. In the ticket worktree, confirm the branch contains the current
       integration tip. If the tip has moved, merge it in, then run the
       ticket's tests there. If they fail, stop: report SENT_BACK with the
       failing output, and leave the fix to the implementer.
    2. In the integration worktree, merge the ticket branch. Resolve each
       conflict in favour of the spec, and record each resolution as
       `Ruling: <what you chose> — <why> — <cost if wrong>`.
    3. Run the ticket's tests, then every full check command, on the
       integration branch. Run each command on its own and record its exit
       code. A check that prints nothing on success, such as isort, is
       proven by its exit code, not by its output.
    4. If everything passes, commit the merge. If the ticket's tests fail on
       the integration branch, undo the merge (`git merge --abort` or
       `git reset --hard ORIG_HEAD`) and report SENT_BACK with the output.

    **Long test runs:** run every test command in the foreground with the
    Bash `timeout` set to 600000 (its 10-minute maximum) and read its output
    when it returns. If the full suite can take longer than that, run it as
    one foreground call per test directory. Polling a background run with
    `sleep` is blocked here, and you have no tool to wait on one.

    **Scratch space:** put scratch files in your own `mktemp -d` directory.
    Other agents share `/tmp` and the git stash.

    ## Report

    Reply with ONLY (under 15 lines):
    - **Status:** MERGED | SENT_BACK | BLOCKED
    - Integration tip after the merge (short SHA), or "unchanged"
    - One line per check: `<command>: rc=<exit code>, <summary line>`
    - Each ruling you made, one per line
    - Concerns, if any
```

**Placeholders:**
- `[MODEL]` — REQUIRED: per SKILL.md Model Selection
- `[TICKET_TESTS]` — the test files or `-k` expression the ticket added or changed
- `[CHECK_COMMANDS]` — the repo's full check list (test suites, type checker, linters), each as its own command; take it from the repo's steering file or CI workflow
- Paths — absolute: the merger works across two worktrees
