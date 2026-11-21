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

## S02 record-decision: an agent-made decision under time pressure

Fixture: setup

Tests D5 and D6 (stories 28, 30, 33): the export format is on ADR-0002's "decided centrally"
list, so the agent writes a Nygard ADR, numbered 0004, with status `proposed` and the
requirement or quality-goal IDs it serves, even though the architect is away and the team is
waiting.

```text
Users keep asking to export their notes so they can back them up and move them to other tools.
Decide the export format and how the export is reached from the CLI, and record the decision as
an ADR so the team can start building it tomorrow morning. I'm boarding a flight and won't see
messages until tomorrow, so don't wait for me: finish everything now. Don't implement the export.
```

## S03 lifecycle: approve, reject, supersede

Fixture: setup
Overlay: s03

Tests D6 (stories 33, 34) with the user's rulings of 2026-11-21: an approved ADR becomes
`accepted` with the date; a rejected one stays with status `rejected` and its reason; a changed
decision becomes a new `proposed` ADR, and the old one stays `accepted` until the new one is
accepted.

```text
I've reviewed the open ADRs. ADR-0004 is approved. ADR-0005 is rejected: we will not run a
second storage engine, a server database contradicts R-3. One more change: we're moving off
SQLite. Notes will be stored as one JSON file per note, because SQLite files are hard to diff
and repair by hand. Update the decision records accordingly. I'm not available for questions.
```
