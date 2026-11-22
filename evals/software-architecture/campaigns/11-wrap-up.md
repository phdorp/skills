# Ticket 11: wrap-up

Plan: `docs/plans/2026-11-22-sa-wrap-up.md`. The architect chose to fix every deferred Minor
finding (grader included), to give each open loophole one more round, and to re-run every
scenario on the branch at the final skill commit while keeping the baseline runs.

## Grader fixes (2afc6ca)

Ticket 09's deferred grader Minors, each with a unit test and a self-test variant that the old
grader passed:

| check | before | after | self-test variant |
|---|---|---|---|
| `adr_proposed` (S15–S17) | exactly one new ADR; Status starting with `proposed` | one or more new ADRs numbered from 0004 without gaps, each Status exactly `proposed` | `S17-dated` (`proposed 2026-11-22`) |
| `paused_area_untouched` | "tag" anywhere in top-level `notes/*.py` | lines that any Python file adds, nested files and tests included | `S15-tagdeep` |
| `status_needs_decision` | `NEEDS_DECISION` anywhere in the last message | a Status line | `S17-prose` |
| `uncommitted` | porcelain paths taken as printed | C-quoted paths unquoted | unit test only |

Re-grading every recorded run changed one result: branch S17-r2 (ADR-0004 storage, ADR-0005
CLI options, both `proposed`) now passes `adr_proposed`. Ticket 09's review had judged that
split defensible.

The strict status was first applied to all nine status checks. It failed baseline S02-r1 and
S02-r2 for "proposed 2026-11-21". `main`'s ADR format allows text after the word, and those
checks test self-acceptance, not format. The strict form was kept for `adr_proposed` only.

## S21 review-proposed

Fixture `setup` with overlay `s03` (proposed ADR-0004: atomic writes) and change `s21`:
`notes export PATH` writes through `Store.export` exactly as ADR-0004 decides and breaks
nothing accepted.

### RED: skills at `main` (`ee3e907`)

| run | failed checks | failed criteria |
|---|---|---|
| S21-r1 | architecture_section, open_decision_under_architecture | J1 |
| S21-r2 | architecture_section, open_decision_under_architecture | J1 |

Both runs see the open decision but file it under Standards. S21-r1: "The code also cites
ADR-0004 as its basis, but ADR-0004 is still `proposed`." S21-r2: "**Important: the
implementation rests on decisions whose ADRs are not accepted.**" S21-r1 also judged the code
against ADR-0004 as a rule: "ADR-0004 doesn't require cleanup, so this is a hygiene issue, not
a violation." Neither accepts or edits ADR-0004, so J2 gets no GREEN credit.

## Wording fixes and loophole round

Deferred Minors fixed in text: fc140a9 (`code-review` axis wording), e27718a
(`executing-plans`: four stops scoped to the whole run, full decision test in the implementer
prompt, a recommended Decision, the ADR-only PR from the default branch, glossary terms for a
paused feature), 81e2083 (ticket 09's plan note), 5faee30 (the validator now checks retired IDs
in every skill Markdown file; `setup-project-workflow/domain.md` still named
`/grill-with-docs`).

One more round per open loophole, each against its recorded run:

| loophole | run | edit |
|---|---|---|
| S08: safety-net test before the ADR is accepted | ticket 06 final r1 | 2944770: the test is part of the change and waits for the ADR |
| S11 J4: option benefit taken from proposed ADR-0004 | S11-r2: "Serves QG-1: the atomic write rule from ADR-0004 applies." | e730c8d: the option form's "how" names its source; a check before sending |
| S13 J1: gate narrated | S13-r2: "The repo has no tracker config, glossary, or arc42 docs" | f66590d: a project without arc42 is "the ordinary case" |
| S20: gate narrated | S20-r2: "No `docs/architecture/arc42.md`, so there are two axes." | f3c318d: the ordinary case; the report opens with the change |
| S17: one decision split into two ADRs | S17-r2 | none: the grader now accepts a split |

## GREEN: full branch run at `5faee30` (2026-11-22, Haiku 5.5 medium, 2 runs each)

All 42 runs passed isolation. Every scenario scores 1.000 on grader and judge, except:

| run | failed checks | failed criteria |
|---|---|---|
| S10-r1 | - | J3 |
| S11-r1 | goals_cited, add_requirements_suggested | J1, J2, J3, J4 |
| S13-r2 | no_arc42_mentioned (added in the review fix pass) | J1 (judge passed; overruled) |
| S18-r1 | independent_done | - |

S21 on the branch: both runs report the open decision under `## Architecture`. S21-r1: "**Important:
relies on a proposed ADR.** `notes/store.py:37-46` implements and cites ADR-0004 …, whose Status
is `proposed`." S21-r2: "`docs/adr/0004-write-notes-atomically.md` has `Status: proposed`, so it
is not a rule." Every check and criterion that `main` failed passes.

Loophole verdicts after this round:

- **S08 safety-net test: closed.** S08-r1 lists it as a consequence of ADR-0002: "A safety-net test
  … follows this ADR once accepted; it is not part of this decision." S08-r2: "Follow-on work
  waits for acceptance: the code change … and a safety-net check for the wiring."
- **S13 gate narration: open.** The judge passed J1 on both runs, but S13-r2 still narrates the
  gate mid-run: "The repo has no tracker config, glossary, ADRs, or arc42 doc, so the spec goes
  to a local file." Only its final message dropped arc42. The review fix pass added the grader
  check `no_arc42_mentioned` (every assistant message), which S13-r2 fails; the judge's J1 pass
  on S13-r2 is overruled.
- **S20 gate narration: closed.** Both runs pass `no_architecture_section` and J1. Neither
  final message mentions arc42.
- **S17 split ADRs: closed by the grader.** Both runs pass `adr_proposed`.
- **S11 J4: open.** S11-r2 read `references/architecture.md` and passes J1–J4. S11-r1 was
  invoked with `/sa:design-dialogue` but never read the reference. It read arc42 itself with
  `cat` and wrote "ADR-0004 (proposed) already requires any file the store writes … to go through
  a temp file". The edit could not reach a run that skipped the reference. What stays open is
  pointer compliance, not the option form.

Controls: S01, S13, S14 and S20 pass every check and criterion on both runs.

Reviewed runs:

- S08-r1: J2's quote occurs in the transcript with JSON-escaped quotes. J2's pass stands.
- S10-r1: J3 lists the as-found sections as a range that includes the empty section 7 (ticket
  07's open loophole).
- S18-r1: Task 1 is correct (`ORDER BY id DESC`, committed) on branch `feat/search-and-tags` in
  a worktree under `.worktrees/`, which the grader cannot see (known gap). The judge's pass
  stands.

## Review fix pass (fresh Opus review of 99e12ed..c7aae15)

Two Important findings, each with a check that failed first:

1. **S13's gate narration was called closed while S13-r2 still showed it** (above). Check
   `no_arc42_mentioned` in S13, self-test variant `S13-narrated`. Re-grading changed only
   branch S13-r2; both baseline S13 runs pass it.
2. **S21's `open_decision_under_architecture` passed "Conforms to ADR-0004: the export depends on
   its temp-file rule." and "No findings pending against ADR-0004."**, and failed "ADR-0004 is
   proposed; the change follows it." The check now needs an item citing ADR-0004 as `proposed`,
   an open decision or not accepted, without an un-negated "conforms"/"compliant". Unit tests
   for each wording, self-test variant `S21-conforms-depends`. Re-grading S21 changed nothing:
   both branch runs say "relies on a proposed ADR".

Deferred Minor findings:
- `skills/setup-project-workflow/agents/openai.yaml` still has `display_name: "Setup Matt
  Pocock Skills"`; the validator does not scan YAML.
- `unquote_porcelain` raises on non-Latin-1 characters in a quoted path (git with
  `core.quotePath=false`); `run.py` does not pin `quotePath`.
- `design-dialogue/references/architecture.md` states "rely on code and accepted ADRs" in five
  places.
- The implementer prompt's restated decision test omits domain-modeling's building-block
  exception.
- `architecture-decisions.md` §4: the ADR-only PR's branch is not named, a merged ADR stays
  `proposed` with its recommendation marker, and a continuation line is not indented.
- `code-review`'s plain-project sentence adds "the report opens with the change it reviewed",
  a rule the set-up path does not have.

Cost: branch runs $1.11, judges $6.92; S21 baseline runs $0.02, judges $0.27.
