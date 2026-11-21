# Software architecture scenarios

Each scenario gives a fresh agent one task on a copy of one fixture (`fixtures/<name>/`, a git
repository with one `fixture` commit). The prompt in the `text` block is passed verbatim with
`claude -p`; anything the architect would answer is written into the prompt, because nobody
answers questions during a run. The grader's checks and the judge's rubric (`RUBRIC.md`) are
never shown to the agent.

## S01 no-setup: ordinary change in a project without architecture setup

Fixture: plain

Proves story 47: a project that has not run `setup-architecture` gets no new steps, apart from
at most one suggestion to run it.

```text
Add a `--top N` option to the tally CLI that prints only the N most frequent words
(all words when the option is absent). Work the way you normally would on a change like this,
add tests, make sure all tests pass, and commit your work. I'm not available for questions.
```
