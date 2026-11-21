# Quality scenario

A quality goal is testable only through a scenario (Bass, Clements and Kazman, *Software
Architecture in Practice*; arc42 section 10). Each part answers one question:

| part | answers | example (QG: Reliability: fault tolerance, from R-2) |
|---|---|---|
| source | who or what causes the stimulus (when it matters) | the operating system |
| stimulus | what happens | the process is killed with SIGKILL during `add` |
| artifact | which part is affected (when it matters) | the note store |
| environment | under which conditions | normal operation |
| response | what the system does | the note is either fully stored or absent; the store still opens |
| measure | the number that decides whether the goal is met | 0 unreadable stores in 100 trials |

The measure is a count, a time, a share or a limit someone can check. "Fast", "robust" or
"easy" is not a measure: ask the architect for the number, or for the observation that would
show the goal is met, and keep the goal open until they give one.

## arc42 section 10 row

```markdown
| ID | goal | stimulus | environment | response | measure |
|---|---|---|---|---|---|
| QS-1 | QG-1 | the process is killed with SIGKILL during `add` | normal operation | the note is either fully stored or absent; the store still opens | 0 unreadable stores in 100 trials |
```

Fold source and artifact into the stimulus when they need saying. Each `QS-n` names its
`QG-n`, and the goal's row in section 1 names its `QS-n` back.
