# setup-architecture (documented project) Implementation Plan

**Goal:** The architect runs `setup-architecture` on a project that already has architecture
documentation in its own form (a README section, status-less ADRs in `docs/decisions/`). In the
first turn the agent writes only an arc42 file that links to where each existing document
lives, and proposes triage, ranking, goals, gap questions, the "made centrally" list and a
one-batch upgrade of the legacy ADRs. After the architect confirms, it writes the R-list and
goals, upgrades the legacy ADRs to `accepted (legacy)` without changing their decisions, and
drafts "Record architecture decisions" as the next free number in the existing ADR directory.
RED on `main` first, then GREEN on the branch.

**Architecture:** `setup-architecture` gains the documented branch: a mapping step (each arc42
section either links to where its content already lives or stays empty; nothing is moved or
copied) and the legacy batch. `domain-modeling` owns the legacy rule and gains the upgrade row
and "the project's ADR directory" (where existing ADRs live). The suite gains fixture
`documented` and two-turn scenario S07, reusing ticket 04's multi-turn runner and S06 helpers.

**Tech Stack:** Markdown skills; Python 3.13 standard library for the suite; `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 11, 12, 15;
1–9 reused); design D1 (documented), D5, D10, D16; ticket
`.scratch/software-architecture-skill-set/issues/05-setup-documented.md`.

## Global Constraints

- Map, never migrate: existing documents stay where they are, byte for byte apart from added lines; arc42 sections link to them instead of repeating them (D1, story 11).
- Status-less ADRs count as accepted (legacy) and are not reopened. Setup offers them for upgrade in one batch; on the architect's confirmation each gets the missing Nygard fields, Context citing R-/QG-IDs, and Status `accepted (legacy)`; its Decision text is unchanged (D16; user, 2026-11-21).
- The "made centrally" ADR takes the next free number in the directory where the project's ADRs already live, is `proposed`, and is found by its title and the arc42 section 9 link (D5, story 15).
- Turn 1 writes only `docs/architecture/arc42.md`, as in ticket 04 (user, 2026-11-21).
- ADR rules live in `domain-modeling`; `setup-architecture` points to them.
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per scenario and arm; judge `claude-opus-5-5`. Discipline rules need RED on `main` before GREEN.
- A branch run is replaced when a skill it loaded changes: S02–S06 load `domain-modeling`, so they are re-run.
- `python3 scripts/validate-skills.py` passes.

## Review Focus

1. The agent copies the README's architecture text into arc42 sections ("completing" the document), so the same facts live in two places. `no_copy` must fail it.
2. The agent "tidies" a legacy ADR's Decision while upgrading it, changing a decision nobody re-decided.
3. A legacy ADR becomes `proposed` or `accepted 2026-11-21`, reopening it or misdating it.
4. The "made centrally" ADR goes to a new `docs/adr/0001-…`, colliding in number with the existing `docs/decisions/0001-…`.
5. The agent edits the README to point at arc42 and deletes its architecture section in the same edit.

## File Structure

- `skills/setup-architecture/SKILL.md` - documented branch: mapping step, legacy batch in the proposal, writes after confirmation.
- `skills/setup-architecture/references/arc42-skeleton.md` - the mapping rule: a section whose content lives elsewhere links there.
- `skills/domain-modeling/SKILL.md` - "the project's ADR directory"; legacy upgrade row in the status table.
- `evals/software-architecture/fixtures/documented/` - `README.md` with a "How it works" section, `docs/decisions/0001-store-books-in-one-json-file.md` (one paragraph, no fields), `docs/decisions/0002-validate-isbn-locally.md` (Context/Decision/Consequences, no Status), `shelf/{__init__,__main__,cli,catalog,isbn}.py`, `tests/test_shelf.py`.
- `evals/software-architecture/grader/grade.py` - `s07`; `grader/{reference,broken}/S07*`; `TASKS.md`, `RUBRIC.md`, `README.md`, `campaigns/05-setup-documented.md`.

## Scenario S07 setup-documented (fixture `documented`, `Invoke: setup-architecture`)

Turn 1:

```text
Bring this project's architecture documentation into shape. My requirements:
1. Readers add, list and find books by title or ISBN from the command line.
2. The catalog survives a crash mid-write.
3. Runs with only the Python standard library.
4. An ISBN is checked before a book is stored.
5. Adding a command touches only cli.py and one new module.
```

Reply:

```text
Confirmed as proposed: your triage, your ranking, the quality goals (except any without a
measure: keep those open), where each existing document maps, and the upgrade of the existing
ADRs. To your "did you leave out" questions: no, nothing is missing. Write everything down now.
I'm offline after this, so finish without asking me again.
```

Checks:

| check | passes when |
|---|---|
| `t1_only_arc42` | `workspace-t1` adds only `docs/architecture/arc42.md` and changes no fixture file; its R-list, QG and QS tables have no rows |
| `docs_kept` | every fixture file exists; every non-blank line of the fixture README is still in it; `shelf/*.py` unchanged |
| `arc42_links_existing` | final arc42 has the 12 headings, links `README.md` and the `decisions/` directory |
| `no_copy` | the README sentence "`cli` calls `catalog`, never the file directly" does not appear in arc42 (whitespace-normalised) |
| `legacy_upgraded` | 0001 and 0002 each have five fields, status starting `accepted (legacy)`, Context citing an R- or QG-ID from arc42, and their original decision sentence ("one JSON file", "checked locally") |
| `made_centrally_next` | exactly one new ADR, `docs/decisions/0003-*.md`, title contains "record architecture decisions", status `proposed`; no `docs/adr/` |
| `goals_measured` | as S06 |

Rubric: J1 turn 1 names the arc42 section each existing document maps to and says nothing is
moved; J2 turn 1 offers both legacy ADRs for upgrade in one batch without reopening their
decisions; J3 the final message says ADR-0003 waits for the architect's approval; J4 the final
message presents ADR-0001 and ADR-0002 as accepted (legacy), not as decisions to re-make.

Self-test `EXPECT`:

```python
"S07-t1upgrade": {"t1_only_arc42"}, "S07-moved": {"docs_kept"}, "S07-copied": {"no_copy"},
"S07-nolink": {"arc42_links_existing"}, "S07-legacydated": {"legacy_upgraded"},
"S07-rewritten": {"legacy_upgraded"}, "S07-adrdir": {"made_centrally_next"},
"S07-code": {"docs_kept"}, "S07-readmelink": set(),   # a README line added, nothing removed
```

## Tasks

### Task 1: Fixture `documented`, S07 and its checks

**Files:** Modify `grader/grade.py`, `grader/selftest.py`, `TASKS.md`, `RUBRIC.md`; create the fixture, reference and broken runs.

**Interfaces:**
- Consumes: `run.Scenario.replies`, `workspace-t1` (ticket 04); `grade._rows`, `_section`, `_files`, `has_measure`, `s06`'s `measured` logic.
- Produces: `grade.goals_measured(text) -> tuple[bool, str]` factored out of `s06` (S06 self-test stays green); `grade.CHECKS["S07"]`.
- [ ] **Step 1:** Write the fixture (tests pass: `python3 -m unittest` in it), the self-test entries, reference and broken runs. Run the self-test. Expected: S07 rows `not graded`, S06 still passing.
- [ ] **Step 2:** Factor `goals_measured`, implement `s07`.
- [ ] **Step 3:** Run unit tests and self-test. Expected: `OK`, `SELF-TEST PASSED`.
- [ ] **Step 4: Commit** `feat(evals): add documented fixture and setup scenario S07`.

### Task 2: RED on the baseline arm

- [ ] **Step 1:** Run S07 on `--arm baseline --ref main` (k 1–2), judge, summarise.
- [ ] **Step 2:** Write `campaigns/05-setup-documented.md` (failures per run, wording verbatim, skills loaded, rules that held on `main`).
- [ ] **Step 3: Gate.** Expected: at least one run fails `t1_only_arc42`, `no_copy`, `legacy_upgraded` or `made_centrally_next`. Rules no run fails get no GREEN credit; say so.
- [ ] **Step 4: Commit** `test(evals): record documented setup on main skills (RED)`.

### Task 3: Documented branch (GREEN)

**Files:** Modify `skills/setup-architecture/SKILL.md`, `references/arc42-skeleton.md`, `skills/domain-modeling/SKILL.md`.

- `setup-architecture` › situation: documented → step 2 with a mapping part: for each existing document, the arc42 section it belongs to; that section gets one line linking it ("See [README › How it works](../../README.md#how-it-works).") and nothing of its content. The proposal adds "Where your documents map" and "Legacy ADRs to upgrade in one batch" (each listed with the IDs its Context would cite). After confirmation: upgrade per `domain-modeling`, then the "made centrally" ADR as the next free number in the existing ADR directory. Remove "this version handles fresh projects" for documented; keep it for undocumented (ticket 07).
- `arc42-skeleton.md`: the mapping rule in one paragraph.
- `domain-modeling`: "Find it by that title in the project's ADR directory (`docs/adr/`, or where its ADRs already live)"; status table row "The architect confirms the legacy upgrade batch | the missing fields and IDs added, Status `accepted (legacy)`, Decision text unchanged".
- [ ] **Step 1:** Edit; validator → `OK`. **Commit** `feat(setup-architecture): map existing documentation and upgrade legacy ADRs in one batch`.
- [ ] **Step 2:** Run S07 on the branch (k 1–2); re-run S02–S06 on the branch (they load `domain-modeling`); judge, summarise.
- [ ] **Step 3: Gate.** Expected: every branch S07 run passes every check and criterion; S01–S06 stay at 1.000/1.000. Otherwise Task 4.
- [ ] **Step 4:** Append GREEN to the campaign. **Commit** `test(evals): record documented setup on branch skills (GREEN)`.

### Task 4: Close loopholes (only if Task 3's gate failed)

One round, as before: quote the failure, add the specific counter, re-run the failing scenarios,
record the result; a failure that remains is reported as an open loophole.

### Task 5: README results

- [ ] Add the S07 row; refresh S02–S06 branch rows; verify unit tests, self-test, validator. **Commit** `docs(evals): record documented setup results`.

## Self-review

- Ticket checklist: fixture with README architecture section and status-less ADRs (T1), checks for nothing moved or deleted (`docs_kept`), arc42 links (`arc42_links_existing`), legacy untouched until confirmation (`t1_only_arc42`), RED/GREEN (T2, T3), validator (T5).
- Spec stories: 11 (`docs_kept`, `no_copy`, J1), 12 (`legacy_upgraded`, J2, J4), 15 (`made_centrally_next`); 16 (multi-context repo) is not exercised: no fixture has `GLOSSARY-MAP.md` (known gap, recorded in the README).
- Review Focus pins: 1 → `no_copy`; 2 → `legacy_upgraded` (original sentence); 3 → `legacy_upgraded` (status); 4 → `made_centrally_next`; 5 → `docs_kept` (README lines) with `S07-readmelink` proving an added line is allowed.
- Type consistency: `goals_measured` is named the same in Task 1 Interfaces and Step 2.

## Execution handoff

Recommended: inline, as tickets 02–04. Live cost: S07 4 two-turn runs plus S02–S06 10 re-runs,
with judges ≈ $3.
