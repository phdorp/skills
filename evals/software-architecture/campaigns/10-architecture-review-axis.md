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
