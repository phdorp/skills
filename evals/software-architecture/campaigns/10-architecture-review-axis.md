# Campaign: the Architecture axis in code-review (ticket 10)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-22-sa-architecture-review-axis.md`.

S19 reviews a change in the set-up project: `notes export` opens SQLite in `notes/cli.py`
(breaks ADR-0003, touches QS-3) and lets a failure end in a traceback (breaks arc42 §8), and
ADR-0004 is accepted with a Context that names no R-, QG- or QS-ID. S20 is the control: a
`--stopwords` change to `tally` with one long `main`, in a project without arc42. Every run
started with `/sa:code-review`.

## RED: skills at `main` (2026-11-22, Haiku 5.5 medium, 2 runs each, clean isolation)

| run | failed checks | failed criteria |
|---|---|---|
| S19-r1 | architecture_section, adr_under_architecture, section8_under_architecture, qs_under_architecture, trace_under_architecture | J1, J2, J4 |
| S19-r2 | architecture_section, adr_under_architecture, section8_under_architecture, qs_under_architecture, trace_under_architecture | J1, J2, J4 |
| S20-r1 | - | - |
| S20-r2 | - | - |

Observed failures, in the agents' words (`runs/baseline/S19-r*`):

1. **Architecture folded into Standards** (both, every `*_under_architecture` check, J1, J4):
   `main`'s standards discovery lists "ADRs, architecture notes", so both runs read arc42 and
   the ADRs as coding standards: "**Standards:** `docs/adr/0001`–`0004`,
   `docs/architecture/arc42.md` (§5, §8), `GLOSSARY.md`" (S19-r1), then "## Standards … 1.
   **Important: breaks ADR-0003 (the CLI must reach storage only through `Store`).**" The
   closing line has two axes: "Standards: 2 Important, 1 Minor (worst: the ADR-0003
   violation …). Spec: 0 findings." (S19-r2).
2. **No traceability check** (both, `trace_under_architecture`, J2): ADR-0004 was read as a
   rule the change obeys, not as a record to check: "Compliant: ADR-0004 is accepted and
   matches the output format." (S19-r1).

What held on `main`: both S19 runs found the ADR-0003 breach, the §8 error rule and QS-3 (J3:
"a contributor who swaps the storage engine (QS-3) must now also change `cli.py`", S19-r2), only
under the wrong heading. No run changed a file (`read_only`). Both S20 runs kept two axes,
raised no architecture setup (J1, `no_architecture_section`), and named the long `main` as a
judgement call: "**Minor: long `main()`.** It now reads files, parses stopwords, counts, ranks,
and prints." (S20-r1); "possible Divergent Change … extract `load_stopwords`" (S20-r2). So J3,
`read_only`, and every S20 check and criterion get no GREEN credit; S20 stays as the D15
regression control. No run dispatched a reviewer subagent; all reviewed both axes inline.

Prompt note: the prompt says "against main's state before it", but the workspace's branch is
`master`. Every run noticed `main` does not resolve and used `HEAD~1`, as the prompt's range
names. Kept as is for GREEN comparability.

Gate: met (every S19 run fails `architecture_section`).

## GREEN round 1: branch at `f383d3d` (superseded; runs in that commit's history)

| run | failed checks | failed criteria |
|---|---|---|
| S19-r1 | - | - |
| S19-r2 | - | - |
| S20-r1 | - | J2 |
| S20-r2 | no_architecture_section | J1 |

S19 passed every check and criterion in both runs, each with an `## Architecture` section:
"**Traceability, `docs/adr/0004-export-as-json-lines.md`:** the ADR is `accepted 2026-11-20`,
so it is not legacy, and its Context names no `R-n`, `QG-n` or `QS-n`." (S19-r1), and a closing
line per axis: "Standards 2 findings (worst: no test for the new command). Spec 1 finding (worst:
export crashes on a fresh DB). Architecture 4 findings (worst: ADR-0003 breach at
`notes/cli.py:3`)." The Standards section deferred ADRs to Architecture (S19-r2).

Two S20 regressions against `main`, which passed both:

1. **The gate reported as a section** (S20-r2, `no_architecture_section`, J1): "## Architecture
   / Skipped: `docs/architecture/arc42.md` does not exist." The run read the pointer and the
   aggregate step's "(and `## Architecture` when that axis ran)" and reported the skip.
2. **Long method not labelled a judgement call** (S20-r1, J2): "1. **Duplicated logic in
   `main` (Important).** … `main` is also a long method". The run took README as the only
   standard and graded smells without the judgement-call label; nothing in the change points
   at this, and `main`'s runs varied the same way in wording ("Minor: long `main()`").

No branch run dispatched a reviewer subagent.

## Loophole round (`18ca2f3`)

`SKILL.md`'s pointer now ends "Otherwise the review has these two axes, and its report has
exactly two sections, `## Standards` and `## Spec`.", and step 5 no longer names
`## Architecture` (the reference adds it). S20-r1's J2 failure has no cause in the change, so
the round leaves it to the re-run. All four branch runs are re-run, since every one loaded the
changed `SKILL.md`.

## GREEN: branch at `1087264` (after the loophole round)

| run | failed checks | failed criteria |
|---|---|---|
| S19-r1 | - | - |
| S19-r2 | - | - |
| S20-r1 | - | - |
| S20-r2 | no_architecture_section | - |

Every check and criterion `main` failed now passes in both S19 runs:

- `architecture_section`, `adr_under_architecture`, J1: "- **Important, breach of ADR-0003**
  (`notes/cli.py:3, 18`): the accepted Decision says "Only `notes/store.py` imports `sqlite3` or
  touches the database file."" (S19-r1, under `## Architecture`).
- `trace_under_architecture`, J2: "- **[Minor] Traceability.** ADR-0004 is `accepted`, not
  legacy, and its Context names no `R-n`, `QG-n` or `QS-n`." (S19-r2).
- J4: "- Architecture: 4 findings. Worst: ADR-0003 breach (Important). - Standards: 2 findings.
  … - Spec: 1 finding." (S19-r2).
- `section8_under_architecture` and `qs_under_architecture` pass in both.

S20: the "Skipped" section is gone, and r1 labels the long `main` a judgement call again (J2).
Neither run suggests setting up an architecture (J1 passes in both). S20-r2 still narrates the
gate in its preamble: "No `docs/architecture/arc42.md`, so there are two axes." That fails
`no_architecture_section` (it names arc42); the judge passes J1, since no section or setup
advice follows, so `summarize.py` marks the run "needs review". No branch run dispatched a
reviewer subagent.

Gate: met for S19 (every check and criterion `main` failed now passes). S20 has no GREEN credit
(it passed on `main`); it regressed in round 1 and, after the loophole round, keeps one open
loophole: the gate narrated in one sentence (1 of 2 runs). Stays open; the one loophole round
is spent.
