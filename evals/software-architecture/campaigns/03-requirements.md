# Campaign: quality-requirements and add-requirements (ticket 03)

Method: `writing-for-agents` › testing-skills (RED on the `main` skills, smallest change, GREEN
on the branch, one loophole round). Plan: `docs/plans/2026-11-21-sa-quality-and-add-requirements.md`.

## RED: skills at `main` (2026-11-21, Haiku 5.5 medium, 2 runs per scenario)

`main` has no `add-requirements`, so both scenarios ran with the plain prompt (`meta.json`
`invoked: false`). No run loaded a skill (no `Skill` tool call in any transcript). No run
committed.

| run | failed checks | failed criteria |
|---|---|---|
| S04-r1 | `adrs_unchanged` (wrote ADR-0004, ADR-0005), `code_unchanged` (`store.py`) | J4 |
| S04-r2 | `code_unchanged` (`store.py`) | J4 |
| S05-r1 | `old_rows_kept` (R-4), `new_rows`, `superseding_adr` (0004 `accepted`, plus 0005), `feature_routed` | J1, J2, J3 |
| S05-r2 | `old_rows_kept` (R-4), `new_rows`, `superseding_adr` (0004 `accepted`, plus 0005), `feature_routed` | J1, J2, J3 |

Observed failures, in the agents' words (`runs/baseline/*/transcript.md`):

1. **Acting before the architect confirms** (S04-r1, S04-r2): both spotted the conflicts, then
   built the one they judged safe. "Baseline is green. I'll start with the one requirement that
   fits the current architecture (#4, newest-first list), writing the test first." S04-r1 also
   wrote two proposed ADRs: "The other four need architect decisions before I can build them, so
   I'll draft those as proposed ADRs".
2. **An existing requirement rewritten** (S05-r1, S05-r2): R-4's reason gained "asked for again
   in the 2026-11 interviews" (r1) and "also asked for in interviews, 2026-11-21" (r2). The
   architect said R-4 stays deferred, not that its row changes.
3. **The superseding ADR accepted on the agent's say-so, and implemented** (S05-r1, S05-r2):
   "ADR-0004 is marked accepted on your say-so" (r2); "I marked it accepted because you ruled on
   item 3. If you're not the architect who accepts ADRs, change its status." (r1). Both rewrote
   `store.py` for text files; r2 also marked ADR-0001 superseded and edited arc42 sections 5, 8
   and 11.
4. **Statuses and outcomes outside the R-list's vocabulary** (S05): encryption filed as `open`
   (r1) or `proposed` (r2), with a new proposed ADR for it, though the architect called it
   system-level. r2 filed the feature-level item as R-8 `active` instead of routing it.
5. **No rank proposed, no goal question** (S05): new rows ranked "tbd" (r1) or "unranked" (r2):
   "New rows R-7 to R-9 are \"unranked\", since no rank was given." Neither asked whether
   encryption needs a security quality goal; both asked only for an implementation choice.

What held on `main` already: both S04 runs named R-4, R-3 and ADR-0001 against requirements 1,
2 and 3 (S04 J1–J3 pass); no run added a quality goal (`goals_unchanged` passes); new R-IDs
started at R-6 (`ids_next_free` passes); rejected `rich` kept with a reason.

Gate: met. Both S04 runs changed code before confirmation, and both S05 runs failed
`old_rows_kept`.

## GREEN: branch skills (commit a7aa49c)

Every run started with `/sa:add-requirements` (`invoked: true`) and loaded
`sa:quality-requirements` and `sa:domain-modeling` through the `Skill` tool.

| run | failed checks | failed criteria |
|---|---|---|
| S04-r1 | - | - |
| S04-r2 | - | - |
| S05-r1 | - | J3 |
| S05-r2 | - | - |

Every RED failure was gone: no S04 run changed a file ("Please confirm or change each outcome.",
S04-r1); no S05 run touched R-4, accepted ADR-0004, changed code or added a goal; both filed
the newest-first item as `.scratch/requirements/issues/01-…md` citing R-1, proposed ranks 4
and 5, and asked about a security goal as a question.

## Loophole (closed): the report did not tie the waiting work to the ADR

S05-r1 changed no code and kept ADR-0004 `proposed`, but its report said only "Two findings
need your decision before the storage work can start." The judge failed J3: the run never said
the storage work waits for the ADR's approval. Step 4 listed "each ADR waiting for approval"
without the work behind it.

Counter (commit 600a9f4): the report names each ADR waiting for approval "together with the work
that waits for it". Re-run of S04 and S05 on the branch (2 runs each, replacing the runs
above): every check and criterion passes. S05-r1: "**Waiting work:** storage changes wait until
you accept ADR-0004." S05-r2: "The storage change waits until you accept ADR-0004, and that
depends on resolving R-7 vs R-8."

S01–S03 were not re-run: the skills they loaded did not change. The two new skills are visible
to them, which could change S02 and S03; ticket 04's re-run covers that.
