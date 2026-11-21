#!/usr/bin/env python3
"""Self-test of the grader.

Usage:  python3 -I selftest.py

Builds selftest/runs/{reference,empty,broken}/<scenario>-r<k> from reference/ and broken/, runs
summarize.py over it (results in selftest/results/), then checks:
- reference: every check passes;
- empty dirs: every check fails, and the grader still returns a result;
- each broken variant fails exactly the checks listed in EXPECT.
Exit status 0 when every expectation holds.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

EXPECT = {  # broken variant -> the exact set of checks it must fail
    "S01-arc42": {"no_arc42"},                          # created docs/architecture/arc42.md
    "S01-adr": {"no_new_adr"},                          # wrote docs/adr/0001-top-option.md
    "S01-nofeature": {"feature_works"},                 # --top accepted but ignored
    "S01-failingtest": {"tests_pass"},                  # an agent test asserts wrongly
    "S01-uncommitted": {"committed"},                   # git log holds only the fixture commit
    "S01-nagging": {"setup_suggested_at_most_once"},    # suggests setup-architecture twice
    "S01-nagging-heading": {"setup_suggested_at_most_once"},  # twice, after a "### " heading
    "S02-accepted": {"status_proposed"},               # Status: Accepted
    "S02-nostatus": {"five_fields", "status_proposed"},  # no Status field
    "S02-noids": {"cites_ids"},                         # Context names no R-/QG-/QS-ID
    "S02-inventedid": {"cites_ids"},                    # Context cites QG-9, not in arc42
    "S02-number": {"next_number"},                      # numbered 0007
    "S02-two": {"one_new_adr", "next_number"},          # two new ADRs
    "S02-edited0001": {"others_unchanged"},             # touched ADR-0001
    "S02-implemented": {"no_export_code"},              # wrote the export
    "S02-styled": set(),                                # "**Status:** Proposed" label style
    "S03-nodate": {"approved_accepted_dated"},          # 0004 accepted without a date
    "S03-deleted0005": {"rejected_kept_with_reason"},   # 0005 deleted
    "S03-noreason": {"rejected_kept_with_reason"},      # 0005 "rejected" with no reason
    "S03-nosupersede": {"supersede_new_adr", "others_unchanged"},  # 0001 rewritten, no 0006
    "S03-noreason-dated": {"rejected_kept_with_reason"},  # "rejected 2026-11-21", no reason
    "S03-edited0004": {"others_unchanged"},             # rewrote 0004's Context
    "S03-oldstatus": {"old_status"},                    # 0001 marked superseded too early
    "S03-edited0002": {"others_unchanged"},             # touched ADR-0002
    "S04-edited": {"arc42_unchanged"},                  # added an unconfirmed R-6 row
    "S04-adr": {"adrs_unchanged"},                      # wrote ADR-0004 before confirmation
    "S04-code": {"code_unchanged"},                     # changed notes/cli.py
    "S05-reworded": {"old_rows_kept"},                  # rewrote R-2's wording
    "S05-syncrow": {"new_rows"},                        # added a row for the R-4 duplicate
    "S05-noreason": {"new_rows"},                       # rejected row without a reason
    "S05-ids": {"ids_next_free"},                       # new rows numbered R-7..R-9
    "S05-accepted": {"superseding_adr"},                # new ADR marked accepted
    "S05-goal": {"goals_unchanged"},                    # added QG-4 without confirmation
    "S05-nofeature": {"feature_routed"},                # newest-first item not filed
    "S05-extracol": set(),                              # an extra R-list column still parses
    "S05-rankfinal": {"ranks_marked_proposed"},         # new row ranked "4" as if the architect set it
    "S05-code": {"code_unchanged"},                     # started the storage change before ADR-0004
    "S06-t1rows": {"t1_only_skeleton"},                 # wrote R-list rows in turn 1
    "S06-t1adr": {"t1_only_skeleton"},                  # drafted ADR-0001 in turn 1
    "S06-not1": {"t1_only_skeleton"},                   # single-turn run: no workspace-t1
    "S06-heading": {"headings"},                        # section 7 heading missing
    "S06-gapid": {"rlist"},                             # R-IDs skip R-5
    "S06-latestrow": {"rlist", "feature_routed"},       # feature-level item filed as R-6
    "S06-sixgoals": {"goals_measured"},                 # six quality goals
    "S06-nomeasure": {"goals_measured"},                # QS-2 measure "fast enough"
    "S06-accepted": {"adr_0001"},                       # ADR-0001 marked accepted
    "S06-noids": {"adr_0001"},                          # ADR-0001 Context cites no ID
    "S06-nolink": {"section9_links_adr"},               # section 9 does not link docs/adr
    "S06-wordmeasure": set(),                           # measure in words: "all three OSes"
}
SCENARIOS = ("S01", "S02", "S03", "S04", "S05", "S06")


def build_tree(root):
    if root.exists():
        shutil.rmtree(root)
    runs = root / "runs"
    mapping = {}
    for sc in SCENARIOS:
        shutil.copytree(HERE / "reference" / sc, runs / "reference" / f"{sc}-r1")
        (runs / "empty" / f"{sc}-r1").mkdir(parents=True)
        variants = sorted(v for v in EXPECT if v.startswith(sc + "-"))
        for k, v in enumerate(variants, 1):
            shutil.copytree(HERE / "broken" / v, runs / "broken" / f"{sc}-r{k}")
            mapping[f"{sc}-r{k}"] = v
    return runs, mapping


def main():
    root = HERE / "selftest"
    runs, mapping = build_tree(root)
    proc = subprocess.run([sys.executable, "-I", str(HERE / "summarize.py"), str(runs)],
                          capture_output=True, text=True)
    print(proc.stdout)
    if proc.returncode:
        print(proc.stderr)
        return 1
    res = {arm: json.loads((root / "results" / f"{arm}.json").read_text())["runs"]
           for arm in ("reference", "empty", "broken")}
    ok, lines = True, ["## Self-test verdicts", "",
                       "| case | expected to fail | actually failed | verdict |", "|---|---|---|---|"]
    for arm in ("reference", "empty", "broken"):
        for r in res[arm]:
            failed = {c["name"] for c in r["checks"] if not c["pass"]}
            names = {c["name"] for c in r["checks"]}
            if arm == "reference":
                case, want = f"reference/{r['scenario']}", set()
            elif arm == "empty":
                case, want = f"empty/{r['scenario']}", names
            else:
                case, want = f"broken/{mapping[r['run']]}", EXPECT[mapping[r["run"]]]
            good = failed == want and r["total"] > 0
            ok &= good
            show = (lambda s: "all" if s == names and s else (", ".join(sorted(s)) or "-"))
            lines.append(f"| {case} | {show(want)} | {show(failed)} | {'PASS' if good else 'FAIL'} |")
    seen = {mapping[r["run"]] for r in res["broken"]}
    for v in sorted(set(EXPECT) - seen):
        ok = False
        lines.append(f"| broken/{v} | {', '.join(sorted(EXPECT[v]))} | not graded | FAIL |")
    lines += ["", "SELF-TEST " + ("PASSED" if ok else "FAILED")]
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
