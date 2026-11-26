# Software Architecture Scenario Suite Skeleton Implementation Plan

**Goal:** A maintainer can run one scenario on a copy of a fixture with either arm's skills,
grade the result, have an Opus 5.5 judge score it with quoted evidence, and record the results;
the first scenario (S01) proves a project without setup gets no new steps (story 47).

**Architecture:** `evals/software-architecture/` mirrors `evals/openmodelica/`. `run.py` exports
an arm's skills from a git ref, copies a fixture into a temp workspace outside the repo, runs
`claude -p` on Haiku 5.5 with only that arm's skills, proves isolation from the stream-json
`init` event, and saves the workspace and transcript under `runs/`. `grade.py` checks file and
transcript outcomes per scenario; `judge.py` runs the Opus 5.5 judge against `RUBRIC.md` and
rejects any verdict whose quote is not found verbatim in the run.

**Tech Stack:** Python 3.13 standard library (`unittest`, `subprocess`, `json`), `claude` CLI
2.1.326, git.

**Spec:** `docs/specs/2026-11-21-software-architecture-skill-set-spec.md` (Testing Decisions);
ticket `.scratch/software-architecture-skill-set/issues/01-eval-suite-skeleton.md`.

## Global Constraints

- Suite lives in `evals/software-architecture/`, laid out like `evals/openmodelica/`: `README.md`, `TASKS.md`, `fixtures/`, `grader/`, `runs/`, `results/`.
- Grader: Python standard library only; run scripts with `python3 -I`.
- Arms: `baseline` = skills at `main`; `branch` = skills at the branch HEAD. Each arm's skills come from `git archive <ref>`, never from the working tree.
- Scenario runs: `claude-haiku-5-5`, `--effort medium`. Judge: `claude-opus-5-5`.
- 2 runs per scenario and arm.
- Every judge verdict carries a quoted passage from the run.
- `python3 scripts/validate-skills.py` passes.
- Commits: Conventional Commits, ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Probe findings (2026-11-21, already verified)

- `--setting-sources project` keeps `~/.claude/skills/*` (the other clone) out.
- `--plugin-dir <dir>` loads `<dir>/skills/*` as `<basename(dir)>:<skill>`. Both arms therefore
  export into a directory named `sa`, so skill names are `sa:<skill>` on either arm.
- The stream-json `system/init` event lists `plugins` (name, path) and `skills`, so isolation is
  checked deterministically, without asking the model.
- The CLI ships a built-in `code-review` skill; it appears unprefixed beside `sa:code-review`.
  Known gap for ticket 10.
- The child needs a clean environment: `env -i HOME PATH LANG IS_SANDBOX=1`. Inheriting this
  session's `CLAUDECODE`/`CLAUDE_CODE_*` variables would make it a child session.
- `--bare` is unusable: it requires `ANTHROPIC_API_KEY`, and this host uses OAuth.

## Review Focus

1. A workspace inside the repo would let the run discover this repo's `AGENTS.md` and git root; the workspace must live under the system temp dir.
2. A run whose `init` event shows a non-builtin plugin other than the arm, or a user-only skill unprefixed, must be marked invalid and excluded from results, not graded.
3. A judge quote that is paraphrased, empty, or cites a file absent from the run must invalidate that verdict and flag the run for review.
4. A run that ends early (agent asks a question in `-p` mode, timeout, CLI error) must still produce a run directory the grader can score (all checks fail rather than crash).
5. Two runs of the same scenario and arm must not share a workspace or overwrite each other's run directory.

## File Structure

- `evals/software-architecture/README.md` - purpose, layout, run procedure (both arms, models), results table, known gaps.
- `evals/software-architecture/TASKS.md` - scenarios; each `## S<NN> <slug>` has a `Fixture:` line and the prompt in one fenced `text` block.
- `evals/software-architecture/RUBRIC.md` - per scenario `## S<NN>`, judged criteria `J1…` with pass conditions.
- `evals/software-architecture/.gitignore` - `grader/selftest/`, `runs/*/*/transcript.jsonl`, `__pycache__/`.
- `evals/software-architecture/fixtures/plain/` - small Python CLI `tally` (word frequencies) with unittest tests; no architecture docs.
- `evals/software-architecture/grader/run.py` - arm export, workspace prep, `claude` invocation, isolation check, transcript rendering, run directory layout.
- `evals/software-architecture/grader/grade.py` - per-scenario deterministic checks; prints one JSON object.
- `evals/software-architecture/grader/summarize.py` - grades every `runs/<arm>/<S>-r<k>`, merges `judge.json`, writes `results/<arm>.json`, prints a Markdown table and the disagreement list.
- `evals/software-architecture/grader/selftest.py` - grader self-test over `reference/` and `broken/`.
- `evals/software-architecture/grader/judge.py` - judge prompt building, judge invocation, quote verification, writes `<run>/judge.json`.
- `evals/software-architecture/grader/judge-prompt.md` - judge instructions template.
- `evals/software-architecture/grader/reference/S01/`, `grader/broken/S01-*/` - hand-made run directories.
- `evals/software-architecture/grader/tests/test_run.py`, `tests/test_judge.py` - unit tests of the pure functions.
- `evals/software-architecture/runs/<arm>/S01-r<k>/` - `workspace/` (no `.git`), `git-log.txt`, `transcript.md`, `meta.json`, `judge.json`.
- `evals/software-architecture/results/<arm>.json` - summarised grades and judge verdicts.

A run directory is the contract between all scripts:

```
<run>/workspace/        files the agent left, .git removed
<run>/git-log.txt       `git log --format='%H %s'` of the workspace
<run>/transcript.jsonl  raw stream-json (gitignored)
<run>/transcript.md     rendered transcript: user prompt, assistant text, tool calls and results
<run>/meta.json         {"scenario","arm","ref","sha","model","effort","cost_usd","duration_s","exit_code","isolation_ok","isolation_errors"}
```

## Tasks

### Task 1: Runner with isolation check

**Files:**
- Create: `evals/software-architecture/grader/run.py`
- Create: `evals/software-architecture/.gitignore`
- Test: `evals/software-architecture/grader/tests/test_run.py`, fixtures `grader/tests/data/init-ok.json`, `init-leak.json`, `stream-sample.jsonl` (trimmed from real probe output)

**Interfaces:**
- Produces:
  - `@dataclass Scenario(id: str, fixture: str, prompt: str)`
  - `load_scenarios(tasks_md: Path) -> dict[str, Scenario]` - raises `ValueError` on a section without `Fixture:` or without exactly one `text` block.
  - `export_arm(ref: str, dest: Path) -> Path` - `git archive <ref>` into `dest/sa`, returns that path.
  - `prepare_workspace(fixture_dir: Path) -> Path` - copies into a new `tempfile.mkdtemp(prefix="sa-eval-")`, `git init`, commits all as `fixture`.
  - `check_isolation(init: dict, plugin_dir: Path, user_skill_names: set[str]) -> list[str]` - errors: a non-builtin plugin other than `plugin_dir`; prefixed skills (`sa:*`) ≠ subdirs of `plugin_dir/skills`; any of `user_skill_names - {"code-review"}` present unprefixed.
  - `render_transcript(jsonl: Path) -> str` - Markdown with `### user`, `### assistant`, `### tool_use <name>` (input JSON), `### tool_result` (text, truncated to 4000 chars).
  - `run_scenario(scenario: Scenario, arm: str, ref: str, k: int, suite: Path) -> Path` - creates `suite/runs/<arm>/<id>-r<k>/` (refuses if it exists), writes the run directory contract.
  - CLI: `python3 -I run.py probe --ref REF` (prompt `Reply OK.`, prints isolation errors, exit 0 only when none) and `python3 -I run.py run S01 --arm baseline --ref main -k 1`.
  - Constants: `MODEL = "claude-haiku-5-5"`, `EFFORT = "medium"`, `TIMEOUT_S = 1800`, `CHILD_ENV_KEYS = ("HOME", "PATH", "LANG")` plus `IS_SANDBOX=1`.

- [ ] **Step 1: Write the failing tests**

```python
def test_load_scenarios_reads_fixture_and_prompt(self):  # tmp TASKS.md with one S99 section
    s = load_scenarios(path)["S99"]
    assert (s.fixture, s.prompt) == ("plain", "Do the thing.\n")
def test_load_scenarios_rejects_section_without_fixture(self): ...  # assertRaises(ValueError)
def test_isolation_ok(self):        # init-ok.json, plugin_dir named sa with 2 skills
    assert check_isolation(init_ok, plugin_dir, {"codebase-design", "code-review"}) == []
def test_isolation_flags_user_skill_leak(self):  # init-leak.json has unprefixed "codebase-design"
    assert any("codebase-design" in e for e in check_isolation(...))
def test_isolation_flags_foreign_plugin(self): ...  # extra plugin with a non-"builtin" path
def test_isolation_flags_missing_arm_skill(self): ...  # sa:<x> absent for an existing skills/<x>
def test_render_transcript_has_prompt_text_and_tool_calls(self):  # stream-sample.jsonl
    md = render_transcript(sample)
    assert "### user" in md and "### tool_use Bash" in md
def test_prepare_workspace_is_outside_repo_and_committed(self):
    ws = prepare_workspace(fixture)
    assert not ws.resolve().is_relative_to(REPO_ROOT)
    assert git_log(ws) == ["fixture"]
```

- [ ] **Step 2: Run, see fail.** `cd evals/software-architecture/grader && python3 -I -m unittest discover -s tests` → ImportError/failures.
- [ ] **Step 3: Implement `run.py`.** Command: `claude -p <prompt> --model MODEL --effort EFFORT --setting-sources project --plugin-dir <arm>/sa --output-format stream-json --verbose --dangerously-skip-permissions`, `cwd=workspace`, env built from `CHILD_ENV_KEYS`. `user_skill_names` = names in `~/.claude/skills`. On isolation failure the run directory is still written with `isolation_ok: false`. A timeout or non-zero exit still writes the run directory (Review Focus 4).
- [ ] **Step 4: Run, see pass.** Same command → `OK`.
- [ ] **Step 5: Live probe.** `python3 -I run.py probe --ref main` and `--ref design/software-architecture-skill-set` → both exit 0, print `isolation ok (30 sa: skills)` or the current count.
- [ ] **Step 6: Commit** `feat(evals): add software-architecture scenario runner`.

### Task 2: Plain fixture, scenario S01, grader and self-test

**Files:**
- Create: `fixtures/plain/` (`README.md`, `tally/__init__.py`, `tally/cli.py`, `tests/test_cli.py`)
- Create: `TASKS.md`, `grader/grade.py`, `grader/summarize.py`, `grader/selftest.py`, `grader/hidden/S01_test_top.py`
- Create: `grader/reference/S01/`, `grader/broken/S01-{arc42,adr,nofeature,failingtest,uncommitted,nagging}/`

**Interfaces:**
- Consumes: run directory contract; `load_scenarios` (Task 1).
- Produces:
  - `grade(scenario_id: str, run_dir: Path) -> dict` → `{"run", "scenario", "checks": [{"name", "pass", "detail"}], "passed", "total", "score"}`.
  - `CHECKS: dict[str, Callable[[Path], list[dict]]]` - one entry per scenario; later tickets add entries.
  - `summarize.py RUNS [--results DIR]` → `results/<arm>.json` `{"arm", "runs": [grade ∪ {"judge": judge.json or null, "valid": isolation_ok}]}`; skips runs with `isolation_ok: false` from scores and lists them.

Fixture `tally`: `python3 -m tally FILE` prints `word count` lines, most frequent first, ties alphabetical; `tests/test_cli.py` covers that. The fixture tests pass with `python3 -m unittest`.

S01 `no-setup`, Fixture `plain`, prompt:

```text
Add a `--top N` option to the tally CLI that prints only the N most frequent words
(all words when the option is absent). Work the way you normally would on a change like this,
add tests, make sure all tests pass, and commit your work. I'm not available for questions.
```

S01 checks (deterministic):

| check | passes when |
|---|---|
| `tests_pass` | `python3 -m unittest` exits 0 in a temp copy of `workspace/` |
| `feature_works` | hidden test `S01_test_top.py` passes in that copy (`--top 2` on a known text prints exactly the 2 expected lines) |
| `committed` | `git-log.txt` has more than the `fixture` commit |
| `no_arc42` | `workspace/docs/architecture/` absent |
| `no_new_adr` | no `workspace/docs/adr/` and no file whose name matches `adr` (case-insensitive) |
| `setup_suggested_at_most_once` | `setup-architecture` occurs at most once in assistant text of `transcript.md` |

- [ ] **Step 1: Write the self-test** with `EXPECT` exactly:

```python
EXPECT = {
    "S01-arc42": {"no_arc42"},
    "S01-adr": {"no_new_adr"},
    "S01-nofeature": {"feature_works"},
    "S01-failingtest": {"tests_pass"},        # an agent test asserts wrongly; feature correct
    "S01-uncommitted": {"committed"},
    "S01-nagging": {"setup_suggested_at_most_once"},
}
```
plus: `reference/S01` fails nothing; an empty run dir fails every check and still yields a result.
- [ ] **Step 2: Run, see fail.** `python3 -I selftest.py` → `SELF-TEST FAILED` (no grader).
- [ ] **Step 3: Write fixture, `TASKS.md` (intro as in openmodelica, plus S01), `grade.py`, `summarize.py`.** Grader never writes into the run dir (copies `workspace/` to a temp dir).
- [ ] **Step 4: Run, see pass.** `python3 -I selftest.py` → table all PASS, `SELF-TEST PASSED`. Also `cd fixtures/plain && python3 -m unittest` → `OK`.
- [ ] **Step 5: Commit** `feat(evals): add plain fixture, no-setup scenario and grader`.

### Task 3: Judge with verified quotes

**Files:**
- Create: `RUBRIC.md`, `grader/judge.py`, `grader/judge-prompt.md`
- Test: `grader/tests/test_judge.py`

**Interfaces:**
- Consumes: run directory contract; `Scenario` (Task 1).
- Produces:
  - `load_rubric(rubric_md: Path) -> dict[str, list[Criterion]]`, `@dataclass Criterion(id: str, text: str)`.
  - `build_prompt(scenario: Scenario, criteria: list[Criterion], run_dir: Path) -> str` - fills `judge-prompt.md` with the task prompt, criteria, `transcript.md`, and every text file in `workspace/` (each under a `=== workspace/<path> ===` header).
  - `parse_verdicts(text: str) -> list[dict]` - extracts the last fenced `json` block: `[{"criterion","pass": bool,"quote","source"}]`.
  - `verify_quotes(verdicts: list[dict], run_dir: Path) -> list[str]` - error per verdict whose `quote` is empty or not found (whitespace-normalised) in `source` (`transcript.md` or `workspace/<path>`).
  - CLI `python3 -I judge.py RUN_DIR` → runs `claude -p --model claude-opus-5-5 --setting-sources project --tools ""` in an empty temp dir with the same clean env, writes `<run>/judge.json` `{"verdicts", "quote_errors", "needs_review": bool, "cost_usd"}`. `needs_review` is true when any quote error exists or a criterion has no verdict.

S01 rubric: `J1` the agent did not ask for or invent quality goals or quality requirements; `J2` the agent created no ADR or architecture decision record and did not propose one; `J3` the agent's working steps match an ordinary feature change (no architecture setup, recovery or documentation step).

`judge-prompt.md` requires: one verdict per criterion; `quote` copied character for character from the run; for a "did not do X" verdict, quote the passage that shows what was done instead (e.g. the final report); output only the JSON block at the end.

- [ ] **Step 1: Write failing tests**

```python
def test_load_rubric_reads_criteria(self): assert [c.id for c in load_rubric(p)["S01"]] == ["J1", "J2", "J3"]
def test_parse_verdicts_takes_last_json_block(self): ...
def test_verify_quotes_accepts_exact_quote_with_whitespace_differences(self): ...
def test_verify_quotes_rejects_paraphrase(self): ...
def test_verify_quotes_rejects_empty_quote(self): ...
def test_verify_quotes_rejects_missing_source_file(self): ...
def test_build_prompt_contains_transcript_and_workspace_files(self): ...  # uses grader/reference/S01
```
- [ ] **Step 2: Run, see fail.** `python3 -I -m unittest discover -s tests` → failures in `test_judge`.
- [ ] **Step 3: Implement `judge.py`, `judge-prompt.md`, `RUBRIC.md`.**
- [ ] **Step 4: Run, see pass.** All tests `OK`. Then `python3 -I judge.py reference/S01` (live, one Opus call) → `judge.json` with 3 verdicts, `quote_errors: []`.
- [ ] **Step 5: Commit** `feat(evals): add rubric judge with verified quotes`.

### Task 4: README and recorded runs on both arms

**Files:**
- Create: `evals/software-architecture/README.md`
- Create: `runs/baseline/S01-r{1,2}/`, `runs/branch/S01-r{1,2}/`, `results/baseline.json`, `results/branch.json`

**Interfaces:**
- Consumes: CLIs of Tasks 1–3.

README sections: what it measures; contents; run it (self-test, probe, `run.py run` per arm with refs `main` and the branch, `judge.py`, `summarize.py`); models (Haiku 5.5 medium runs, Opus 5.5 judge); review rule (the user reviews runs with `needs_review`, runs where grader and judge disagree, and a sample); results table (scenario × arm: grader score, judge pass rate, cost); known gaps: the unattended "PR containing only the ADR" path is not exercised (fixtures have no pull-request remote); the built-in `code-review` skill is visible beside `sa:code-review`; 2 runs per scenario cannot detect small effects; at this ticket both arms carry identical skills, so S01 is a baseline to re-run in ticket 11.

- [ ] **Step 1: Run** `run.py run S01 --arm baseline --ref main -k 1` and `-k 2`, then the same with `--arm branch --ref design/software-architecture-skill-set`. Expected: four run dirs, each `meta.json` `isolation_ok: true`.
- [ ] **Step 2: Judge** each run dir; `summarize.py ../runs`. Expected: `results/baseline.json`, `results/branch.json`; table printed.
- [ ] **Step 3: Write README** with the table from Step 2. Review any `needs_review` or disagreement run and record the outcome in the README.
- [ ] **Step 4: Verify.** `python3 -I grader/selftest.py` → `SELF-TEST PASSED`; unit tests `OK`; `python3 scripts/validate-skills.py` → passes.
- [ ] **Step 5: Commit** `test(evals): record no-setup scenario on both arms`.

## Self-review

- Spec coverage: layout (all tasks), fixtures (Task 2, plain only; other four in tickets 04–07), scenarios (S01; others in later tickets), grader + self-test (Task 2), judge with quotes (Task 3), arms and models (Task 1, README), user review of disagreements (Tasks 2, 4), known gap (Task 4), validator (Task 4). RED-before-GREEN for discipline rules belongs to tickets 02 and 09.
- Review Focus pins: 1 → `test_prepare_workspace_is_outside_repo_and_committed`; 2 → isolation tests + `summarize` skipping invalid runs; 3 → `verify_quotes` tests; 4 → empty-dir self-test case; 5 → `run_scenario` refuses an existing run dir.
- Names consistent across tasks: `Scenario`, `load_scenarios`, `grade`, `CHECKS`, `verify_quotes`, `judge.json`, `meta.json.isolation_ok`.

## Execution handoff

Recommended: execute in this session task by task (four tightly coupled tasks sharing one run
directory contract; a subagent per task would re-derive the contract). Live cost: about 6 Haiku
runs and 5 Opus judge calls.
