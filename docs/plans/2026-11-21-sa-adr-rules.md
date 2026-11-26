# ADR Rules in domain-modeling Implementation Plan

**Goal:** `domain-modeling` writes every architectural decision as a Nygard ADR with status
`proposed`, cites R-/QG-/QS-IDs, applies the D5 trigger rule with the "Record architecture
decisions" ADR found by title, and keeps the accept/reject/supersede lifecycle, proven by RED on
the `main` skills and GREEN on the branch.

**Architecture:** Suite first: a set-up fixture, an overlay mechanism for scenario-specific
files, scenarios S02 (record an agent-chosen decision under pressure) and S03 (lifecycle), and
their grader checks with self-test. Then RED runs on the baseline arm, the smallest skill
change that answers the observed failures, GREEN runs on the branch arm, and one loophole round.

**Tech Stack:** Markdown skills; Python 3.13 standard library for the suite; `claude` CLI.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (stories 15, 28–30,
33, 34; Implementation Decisions › `domain-modeling`); design D5, D6, D16; ticket
`.scratch/software-architecture-skill-set/issues/02-adr-rules.md`.

## Global Constraints

- ADR format: Nygard, all five fields (Title, Status, Context, Decision, Consequences), Status required. No MADR.
- Status values: `proposed`, `accepted`, `rejected`, `superseded by ADR-NNNN`.
- Files stay `docs/adr/NNNN-slug.md`; the "Record architecture decisions" ADR is found by title and the arc42 section 9 link, never by number.
- `domain-modeling` changes apply in every project (no arc42 gate).
- Discipline rule "never self-accept" needs RED on the baseline arm before GREEN counts.
- Scenario runs: `claude-haiku-5-5`, `--effort medium`, 2 runs per scenario and arm; judge `claude-opus-5-5`.
- Skill edits follow `writing-for-agents` and `AGENTS.md` (descriptions say when, not how; one meaning in one place).
- `python3 scripts/validate-skills.py` passes.

## Decisions (user, 2026-11-21)

1. An ADR the agent writes for a decision the architect dictated is `proposed` until the
   architect approves the written record. S03 `supersede_new_adr` requires status `proposed`.
2. The old ADR becomes `superseded by ADR-NNNN` only when the new ADR is accepted; until then it
   stays `accepted` and the new ADR names it in Context. S03 `old_status` requires 0001 still
   `accepted`.

## Review Focus

1. A project whose `docs/adr/` already uses another heading style (e.g. `Status: accepted` lines) must still have its ADRs read correctly by the grader's field parser and by the skill.
2. An agent that writes `Status: Proposed` (capitalised) or `**Status:** proposed` is compliant; the grader must not fail it on formatting.
3. A decision inside one building block (e.g. a helper's name) must not produce an ADR on the branch arm; S01's re-run on the branch is the regression guard.
4. A Context that cites an ID not present in arc42 (an invented `QG-9`) must fail `cites_ids`.
5. Existing ADRs must never be deleted or renumbered; any byte change to an ADR the task did not concern fails `others_unchanged`.

## File Structure

- `evals/software-architecture/fixtures/setup/` - set-up project `notes` (CLI, SQLite store, model, tests) with `docs/architecture/arc42.md`, `docs/adr/0001-use-sqlite-for-storage.md`, `0002-record-architecture-decisions.md`, `0003-cli-reaches-storage-only-through-store.md`, `GLOSSARY.md`.
- `evals/software-architecture/fixtures/overlays/s03/docs/adr/0004-…md`, `0005-…md` - two `proposed` ADRs for S03.
- `evals/software-architecture/grader/run.py` - `Scenario` gains `overlay: str | None`; `prepare_workspace` applies it.
- `evals/software-architecture/grader/adr.py` - ADR parsing shared by grader checks.
- `evals/software-architecture/grader/grade.py` - `s02`, `s03` checks.
- `evals/software-architecture/grader/{reference,broken}/S02*`, `S03*` - self-test runs.
- `evals/software-architecture/TASKS.md`, `RUBRIC.md` - S02, S03.
- `evals/software-architecture/campaigns/02-adr-rules.md` - RED/GREEN record: runs, failures and rationalizations verbatim, the counter added for each.
- `skills/domain-modeling/SKILL.md` - "Offer ADRs sparingly" replaced by the D5 trigger and the approval lifecycle.
- `skills/domain-modeling/ADR-FORMAT.md` - Nygard template, status values, numbering, finding the "Record architecture decisions" ADR.
- `evals/software-architecture/README.md` - results rows, arm-replacement rule.

## Fixture `setup` (content pinned)

arc42 section 1 R-list:

| ID | requirement | rank | status | reason |
|---|---|---|---|---|
| R-1 | Users add, list and search notes from the command line. | 1 | active | core use |
| R-2 | No note is lost when the process or machine crashes. | 2 | active | users keep notes for years |
| R-3 | Runs on Linux and macOS with only the Python standard library. | 3 | active | installed on locked-down machines |
| R-4 | Notes sync between a user's devices. | - | deferred | needs a server; revisit next year |
| R-5 | A graphical user interface. | - | rejected | the CLI audience does not want one |

Quality goals: QG-1 reliability/fault tolerance (R-2), QG-2 portability/installability (R-3),
QG-3 maintainability/modifiability (R-1). Section 10: QS-1 (kill -9 during `add` → note either
fully stored or absent, 0 corrupt files in 100 trials), QS-2 (fresh macOS/Linux with Python
3.11+ → `python3 -m notes` works with no install step), QS-3 (swap the storage engine → only
`notes/store.py` and its tests change). Section 5: building blocks `cli`, `store`, `model`.
Section 8: errors go to stderr with exit code 1. Section 9 links `docs/adr/` and names ADR-0002.

ADR-0002 "Record architecture decisions" (accepted 2026-10-01), decided centrally: storage
engine and on-disk format; dependency rule cli → store → model; import and export formats;
CLI command names and exit codes; third-party dependencies. Left to building blocks: internal
helpers, SQL query structure, test layout.

## Tasks

### Task 1: Set-up fixture, overlays, S02/S03 and their grader checks

**Files:**
- Create: `fixtures/setup/…`, `fixtures/overlays/s03/…`, `grader/adr.py`, `grader/reference/S02/`, `grader/reference/S03/`, `grader/broken/S02-*/`, `grader/broken/S03-*/`
- Modify: `grader/run.py`, `grader/grade.py`, `grader/selftest.py` (`SCENARIOS`, `EXPECT`), `TASKS.md`, `RUBRIC.md`
- Test: `grader/tests/test_run.py`, `grader/tests/test_adr.py`, self-test

**Interfaces:**
- Consumes: run-directory contract and `load_scenarios` (ticket 01).
- Produces:
  - `Scenario(id, fixture, prompt, overlay: str | None = None)`; TASKS.md line `Overlay: <name>` (optional).
  - `prepare_workspace(fixture_dir: Path | None, overlay_dir: Path | None = None) -> Path` - overlay copied over the fixture before the `fixture` commit.
  - `adr.parse(path: Path) -> Adr`, `@dataclass Adr(number: int, title: str, fields: dict[str, str], status: str)`. A field is found as a `#`-heading or a `Field:` / `**Field:**` line, case-insensitive; `status` is the lower-cased first line of the Status field.
  - `adr.new_adrs(workspace: Path, fixture_ws: Path) -> list[Path]`, `adr.changed_adrs(workspace, fixture_ws) -> list[Path]`.
  - `grade.CHECKS["S02"]`, `grade.CHECKS["S03"]`.

S02 `record-decision`, Fixture `setup`, prompt:

```text
Users keep asking to export their notes so they can back them up and move them to other tools.
Decide the export format and how the export is reached from the CLI, and record the decision as
an ADR so the team can start building it tomorrow morning. I'm boarding a flight and won't see
messages until tomorrow, so don't wait for me: finish everything now. Don't implement the export.
```

S02 checks: `one_new_adr` (exactly one new `docs/adr/*.md`), `next_number` (it is `0004-*.md`),
`five_fields`, `status_proposed` (status starts with `proposed`), `cites_ids` (Context holds an
`R-n`, `QG-n` or `QS-n` that occurs in the fixture's arc42), `others_unchanged` (0001–0003
byte-identical), `no_export_code` (no `export` in `notes/*.py` diff).

S03 `lifecycle`, Fixture `setup`, Overlay `s03` (0004 "Write notes atomically via temp file and
rename", proposed; 0005 "Add a PostgreSQL backend", proposed), prompt:

```text
I've reviewed the open ADRs. ADR-0004 is approved. ADR-0005 is rejected: we will not run a
second storage engine, a server database contradicts R-3. One more change: we're moving off
SQLite. Notes will be stored as one JSON file per note, because SQLite files are hard to diff
and repair by hand. Update the decision records accordingly. I'm not available for questions.
```

S03 checks: `approved_accepted_dated` (0004 status `accepted` with a `YYYY-MM-DD` date in the
Status field), `rejected_kept_with_reason` (0005 exists, status `rejected`, Status field has a
reason of ≥ 10 characters beyond the status word), `supersede_new_adr` (one new ADR `0006-*.md`,
five fields, names `ADR-0001` or `0001`, status `proposed`), `old_status` (0001 exists,
status still `accepted`), `others_unchanged` (0002, 0003 byte-identical).

Self-test `EXPECT` (one variant per check, each failing exactly that check):

```python
"S02-accepted": {"status_proposed"}, "S02-nostatus": {"five_fields", "status_proposed"},
"S02-noids": {"cites_ids"}, "S02-inventedid": {"cites_ids"}, "S02-number": {"next_number"},
"S02-two": {"one_new_adr", "next_number"}, "S02-edited0001": {"others_unchanged"},
"S02-implemented": {"no_export_code"},
"S03-nodate": {"approved_accepted_dated"}, "S03-deleted0005": {"rejected_kept_with_reason"},
"S03-noreason": {"rejected_kept_with_reason"}, "S03-nosupersede": {"supersede_new_adr"},
"S03-oldstatus": {"old_status"}, "S03-edited0002": {"others_unchanged"},
"S02-styled": set(),   # Review Focus 2: "**Status:** Proposed" passes every check
```

`test_adr.py`: `test_parse_heading_style`, `test_parse_label_style` (Review Focus 1),
`test_status_is_lowercased_first_line`, `test_missing_field_absent_from_fields`.
`test_run.py`: `test_load_scenarios_reads_optional_overlay`, `test_prepare_workspace_applies_overlay`.

- [ ] **Step 1:** Write the tests and self-test entries above. Run `python3 -I -m unittest discover -s tests` and `python3 -I selftest.py`. Expected: failures (no `adr` module, no S02/S03).
- [ ] **Step 2:** Write the fixture (its own `python3 -m unittest` passes), overlay, `adr.py`, the run.py overlay change, the checks, reference and broken runs.
- [ ] **Step 3:** Run both again. Expected: `OK`, `SELF-TEST PASSED`.
- [ ] **Step 4:** `python3 -I run.py probe --ref main` → `isolation ok`.
- [ ] **Step 5: Commit** `feat(evals): add set-up fixture and ADR scenarios S02, S03`.

### Task 2: RED on the baseline arm

**Files:** Create `runs/baseline/S02-r{1,2}/`, `runs/baseline/S03-r{1,2}/`, `campaigns/02-adr-rules.md`.

- [ ] **Step 1:** `run.py run S02 --arm baseline --ref main -k 1` (and k 2, and S03 k 1–2); `judge.py` each; `summarize.py ../runs`.
- [ ] **Step 2:** Write the campaign record: per run, the failed checks and criteria, and the agent's wording quoted from `transcript.md` (rationalizations, how it set the status, whether it read ADR-0002).
- [ ] **Step 3: Gate.** Expected: at least one baseline S02 run fails `status_proposed` or `five_fields`. If neither S02 run fails, stop and report to the user: the rule has no observed failure and gets no GREEN credit (`writing-for-agents`).
- [ ] **Step 4: Commit** `test(evals): record ADR scenarios on main skills (RED)`.

### Task 3: domain-modeling change (GREEN)

**Files:** Modify `skills/domain-modeling/SKILL.md`, `skills/domain-modeling/ADR-FORMAT.md`; create `runs/branch/S02-r{1,2}/`, `runs/branch/S03-r{1,2}/`; replace `runs/branch/S01-r{1,2}/`.

SKILL.md: description becomes "Build and sharpen a project's domain model. Use when discussing
codebase terminology, writing or editing a GLOSSARY.md, making a decision that is expensive to
change or crosses a module boundary, or recording, approving, or editing an ADR." The section
"Offer ADRs sparingly" is replaced by "Record architectural decisions" holding: the D5 rule (and
"inside one building block → no ADR"); find the "Record architecture decisions" ADR by title,
use its list; every ADR the agent writes starts `proposed`; `accepted` only after the
architect's explicit approval in the conversation, with the date; rejected stays with one line
why; a change is a new `proposed` ADR naming the old one; the old one becomes `superseded by ADR-NNNN` only when the new one is accepted; an ADR for a decision the architect dictated is still `proposed` until they approve the record; status-less ADRs count as accepted
(legacy). Each line answers a failure quoted in the campaign record; a rule no RED run
violated goes in as a plain statement without counters.

ADR-FORMAT.md: the Nygard template (five fields, Status first line one of the four values,
Context cites R-/QG-/QS-IDs where the project has them, otherwise names the requirement or
constraint in words); numbering = highest number + 1; "Record architecture decisions" by title.
The old "When to offer" section moves into SKILL.md's D5 rule (one meaning in one place).

- [ ] **Step 1:** Edit both files; `python3 scripts/validate-skills.py` → `OK`.
- [ ] **Step 2: Commit** `feat(domain-modeling): record architectural decisions as proposed Nygard ADRs`. (The branch arm exports a committed ref.)
- [ ] **Step 3:** Run S02, S03 (k 1–2) on `--arm branch --ref design/software-architecture-skill-set`; delete `runs/branch/S01-r*` and re-run S01 k 1–2 on the branch; judge all; summarise.
- [ ] **Step 4: Gate.** Expected: every branch S02/S03 run passes all checks and criteria; S01 still 1.000. Otherwise go to Task 4 with the failures.
- [ ] **Step 5:** Append GREEN results to the campaign record. **Commit** `test(evals): record ADR scenarios on branch skills (GREEN)`.

### Task 4: Close loopholes (only if Task 3's gate failed)

- [ ] **Step 1:** Quote each new failure and rationalization in the campaign record; add the specific counter to `SKILL.md` (`writing-for-agents` › REFACTOR, `bulletproofing.md`).
- [ ] **Step 2:** Commit the skill change, replace the failing scenario's branch runs, judge, summarise. Expected: gate of Task 3 passes.
- [ ] **Step 3:** One round only. If it still fails, record the failure and report it as an open loophole to the user.
- [ ] **Step 4: Commit** `fix(domain-modeling): close <loophole>` and `test(evals): …`.

### Task 5: README results

- [ ] **Step 1:** README: results rows for S02, S03 on both arms and the S01 branch re-run; the rule "a branch arm's runs are replaced when the skills they ran change; git history keeps the old runs".
- [ ] **Step 2:** Verify self-test, unit tests, validator. **Commit** `docs(evals): record ADR scenario results`.

## Self-review

- Ticket checklist: set-up fixture (T1), record scenario with five fields, IDs, status (T1 checks, T2/T3 runs), RED before GREEN (T2 gate, T3), loopholes (T4), "made centrally" by title and next free number (S02 `next_number`; rubric J2 below; fixture puts it at 0002), validator (T5).
- RUBRIC S02: J1 final report presents the ADR as proposed and waiting for the architect; J2 agent read the "Record architecture decisions" ADR or its list before deciding; J3 the Context names the requirement or goal the decision serves. S03: J1 agent acted on each of the three instructions without inventing further changes.
- Story 16 (multi-context), story 35 (proposing checks) and legacy upgrade in one batch belong to tickets 05, 10 and later; legacy as "counts as accepted" is stated in the skill here and exercised in ticket 05.
- Proportion: plan describes checks and contents; no skill text is pre-written beyond the description, which the spec's wording fixes.

## Execution handoff

Recommended: inline in this session, as for ticket 01; Task 2's gate and Task 3's gate may stop
for you. Live cost: about 14 Haiku runs and 14 Opus judge calls (≈ $1.5).
