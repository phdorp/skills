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

## S04 add-requirements-propose: new requirements are checked and proposed, nothing changes

Fixture: setup
Invoke: add-requirements

Tests D18 (stories 17–21, 25): each new requirement is checked against every R-list row
(deferred and rejected included), the active requirements, the constraints and the accepted
ADRs, and gets a proposed outcome. No file changes before the architect confirms. On an arm
that has `add-requirements`, the prompt starts with `/sa:add-requirements`.

```text
New requirements from this week's user interviews:
1. Notes sync between my laptop and my desktop.
2. Install with `pip install notes-cli`, using the `rich` library for coloured output.
3. Notes can be read and edited with any text editor.
4. `notes list` shows the newest notes first.
5. Notes are encrypted at rest, so a stolen laptop exposes nothing.
Please integrate them into the project.
```

## S05 add-requirements-confirmed: the architect's triage is applied, goals stay as they are

Fixture: setup
Invoke: add-requirements

Tests D18 and D4 (stories 22–25, 4–6): confirmed outcomes change the R-list (next free IDs,
old rows untouched, rejected kept with its reason), a conflict with an accepted ADR becomes a
`proposed` superseding ADR, a feature-level item goes to the tracker, and the quality goals
change only after the architect confirms.

```text
New requirements from this week's user interviews:
1. Notes sync between my laptop and my desktop.
2. Install with `pip install notes-cli`, using the `rich` library for coloured output.
3. Notes can be read and edited with any text editor.
4. `notes list` shows the newest notes first.
5. Notes are encrypted at rest, so a stolen laptop exposes nothing.
Please integrate them into the project.

My triage, already decided: 1 is a duplicate of R-4, which stays deferred. 2 is rejected: it
breaks R-3. 3 is system-level and replaces the SQLite decision. 4 is feature-level.
5 is system-level. Apply this. I'm not available for questions today.
```

## S06 setup-fresh: set up the architecture of a new project over two turns

Fixture: fresh
Invoke: setup-architecture

Tests D1 (fresh), D3, D4, D5, D10 (stories 1–10): turn 1 writes only the arc42 skeleton and
proposes triage, ranking, quality goals with scenarios, gap questions and the "made centrally"
list; the architect's scripted reply (the `reply` block, sent with `--resume`) confirms the
proposals; then the agent writes the R-list, 3–5 measured goals and ADR-0001 "Record
architecture decisions" as `proposed`. `workspace-t1/` is the workspace after turn 1.

```text
Set up the architecture for birdlog, a command-line tool for logging bird sightings.
My requirements:
1. Birders log a sighting (species, place, time, count) from the command line.
2. No sighting is ever lost, even if the laptop dies mid-write.
3. Runs offline on Linux, macOS and Windows with nothing but Python installed.
4. Sightings export to the eBird CSV format.
5. It must be fast.
6. `birdlog list` shows the latest sighting first.
```

```reply
Your triage and your ranking are confirmed as proposed. The quality goals you proposed are
confirmed in your order, except any you could not give a measure: keep those as open
questions. To your "did you leave out" questions: no, nothing is missing. Write everything
down now. I'm offline after this, so finish without asking me again.
```

## S07 setup-documented: map existing documentation, upgrade legacy ADRs

Fixture: documented
Invoke: setup-architecture

Tests D1 (documented), D5, D16 (stories 11, 12, 15): the project already describes its
architecture in its README and keeps status-less ADRs in `docs/decisions/`. Turn 1 writes only
an arc42 file that links to those documents and proposes the setup plus a one-batch upgrade of
the legacy ADRs; after the architect's reply the legacy ADRs become `accepted (legacy)` with
their decisions unchanged, and "Record architecture decisions" is `docs/decisions/0003-…`,
`proposed`. Nothing is moved, deleted or copied.

```text
Bring this project's architecture documentation into shape. My requirements:
1. Readers add, list and find books by title or ISBN from the command line.
2. The catalog survives a crash mid-write.
3. Runs with only the Python standard library.
4. An ISBN is checked before a book is stored.
5. Adding a command touches only cli.py and one new module.
```

```reply
Confirmed as proposed: your triage, your ranking, the quality goals (except any without a
measure: keep those open), where each existing document maps, and the upgrade of the existing
ADRs. To your "did you leave out" questions: no, nothing is missing. Write everything down now.
I'm offline after this, so finish without asking me again.
```
