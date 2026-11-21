#!/usr/bin/env python3
"""Self-test of the grader.

Usage:  python3 -I selftest.py [-j JOBS]

Builds selftest/runs/{reference,empty,broken}/<task>-r<k> from reference/ and broken/, runs
summarize.py over it (results in selftest/results/), then checks:
- reference: every check passes;
- empty dirs: every check fails, and the grader still returns a result;
- each broken variant fails exactly the checks listed in EXPECT.
Exit status 0 when every expectation holds.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

EXPECT = {  # broken variant -> the exact set of checks it must fail
    "T1-negative": {"h_nonnegative", "h_final_zero"},     # level goes below 0 and stays there
    "T1-nonascii": {"ascii"},                              # "m²" in a comment
    "T1-stoptime": {"stop_time"},                          # StopTime = 200
    "T2-restitution": {"n_bounces"},                       # e = 0.6 -> 4 bounces by 5 s
    "T2-nofloor": {"n_bounces", "t_first", "h_above_floor"},  # no impact handling
    "T2-warning": {"no_warnings"},                         # v(start) not fixed -> init warning
    "T3-nomsl": {"uses_msl"},                              # hand-written ODE, right answer
    "T3-damping": {"x_at_0_5", "x_at_1"},                  # d = 20 instead of 2
    "T4-notests": {"tests_have_assert", "tests_pass"},     # no Vehicle.Tests
    "T4-notpartial": {"drag_partial"},                     # Drag not partial
    "T4-noextends": {"drag_subclasses"},                   # QuadraticDrag plug-compatible only
    "T4-failingtest": {"simulates", "tests_pass"},         # a test assert fires
    "T5-mslgravity": {"t_quarter"},                        # World default g = 9.80665: T/4 +1.0e-4 s
    "T5-norcm": {"no_warnings"},                           # Body without r_CM: "has no value" warning
    "T5-nomsl": {"uses_msl"},                              # hand-written ODE, right answer
    "T6-gbodedefault": {"solver"},                         # s="gbode" only: esdirk4 runs
    "T6-noannotation": {"solver"},                         # no simulation flags: dassl runs
    "T6-radau5": {"simulates", "y1_at_40", "y2_at_40", "y3_at_40", "mass_conserved", "solver",
                  "no_warnings"},                          # old solver name: unrecognized, sim fails
    "T6-numjac": {"no_warnings"},                          # right solver, GBODE numeric-Jacobian warning
    "T7-nohysteresis": {"simulates", "heater_on", "t_off1", "n_on", "t_band",
                        "no_warnings"},                    # one 20 degC threshold: chatters, -alarm kills it
    "T7-countinitial": {"n_on"},                           # counts the initial on state: 143
    "T8-rollback": {"v_stopped", "no_rollback"},           # no stop logic, v goes negative
    "T8-notests": {"tests_have_assert", "tests_pass"},     # no Fleet.Tests
    "T8-noextends": {"records_extend"},                    # Truck repeats the fields of Params
}
TASKS = tuple(f"T{i}" for i in range(1, 9))


def build_tree(root):
    if root.exists():
        shutil.rmtree(root)
    runs = root / "runs"
    mapping = {}
    for task in TASKS:
        shutil.copytree(HERE / "reference" / task, runs / "reference" / f"{task}-r1")
        (runs / "empty" / f"{task}-r1").mkdir(parents=True)
        variants = sorted(v for v in EXPECT if v.startswith(task + "-"))
        for k, v in enumerate(variants, 1):
            shutil.copytree(HERE / "broken" / v, runs / "broken" / f"{task}-r{k}")
            mapping[f"{task}-r{k}"] = v
    return runs, mapping


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--jobs", type=int, default=2)
    a = ap.parse_args()
    root = HERE / "selftest"
    runs, mapping = build_tree(root)
    proc = subprocess.run([sys.executable, "-I", str(HERE / "summarize.py"), str(runs),
                           "-j", str(a.jobs)], capture_output=True, text=True)
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
                case, want = f"reference/{r['task']}", set()
            elif arm == "empty":
                case, want = f"empty/{r['task']}", names
            else:
                case, want = f"broken/{mapping[r['run']]}", EXPECT[mapping[r["run"]]]
            good = failed == want and r["total"] > 0
            ok &= good
            show = (lambda s: "all" if s == names and s else (", ".join(sorted(s)) or "-"))
            lines.append(f"| {case} | {show(want)} | {show(failed)} | {'PASS' if good else 'FAIL'} |")
    lines += ["", "SELF-TEST " + ("PASSED" if ok else "FAILED")]
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
