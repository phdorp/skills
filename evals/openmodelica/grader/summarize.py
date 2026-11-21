#!/usr/bin/env python3
"""Grade every RUNS/<arm>/<task>-r<k> and summarise.

Usage:  python3 -I summarize.py RUNS [-j JOBS] [--results DIR]

Writes <results>/<arm>.json (default results dir: RUNS/../results) and prints a Markdown
summary to stdout. Progress goes to stderr.
"""
import argparse
import importlib.util
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RUN_NAME = re.compile(r"^(T[1-8])-r(\d+)$")


def _load_grade():
    path = Path(__file__).resolve().parent / "grade.py"
    spec = importlib.util.spec_from_file_location("bench_grade", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


grade_mod = _load_grade()


def find_runs(runs_root):
    runs = []
    for arm in sorted(p for p in Path(runs_root).iterdir() if p.is_dir()):
        for run in sorted(p for p in arm.iterdir() if p.is_dir()):
            m = RUN_NAME.match(run.name)
            if m:
                runs.append((arm.name, m.group(1), int(m.group(2)), run))
            else:
                print(f"skipping {run} (not <task>-r<k>)", file=sys.stderr)
    return runs


def grade_all(runs, jobs):
    def one(item):
        arm, task, k, path = item
        res = grade_mod.grade(task, str(path))
        res.update(arm=arm, run=f"{task}-r{k}")
        failed = [c["name"] for c in res["checks"] if not c["pass"]]
        print(f"graded {arm}/{task}-r{k}: {res['passed']}/{res['total']}"
              + (f" failed={failed}" if failed else ""), file=sys.stderr)
        return res

    with ThreadPoolExecutor(max_workers=jobs) as ex:
        return list(ex.map(one, runs))


def markdown(results):
    out = ["## Per arm and task", "",
           "| arm | task | runs | mean score | fully passing | mean warnings |",
           "|---|---|---:|---:|---:|---:|"]
    groups = {}
    for r in results:
        groups.setdefault((r["arm"], r["task"]), []).append(r)
    for (arm, task), rs in sorted(groups.items()):
        n = len(rs)
        mean = sum(r["score"] for r in rs) / n
        full = sum(r["passed"] == r["total"] for r in rs)
        warn = sum(r["warnings"]["count"] for r in rs) / n
        out.append(f"| {arm} | {task} | {n} | {mean:.3f} | {full}/{n} | {warn:.1f} |")
    out += ["", "## Per run", "",
            "| arm | run | score | warnings | failed checks |", "|---|---|---:|---:|---|"]
    for r in sorted(results, key=lambda r: (r["arm"], r["run"])):
        failed = ", ".join(c["name"] for c in r["checks"] if not c["pass"]) or "-"
        out.append(f"| {r['arm']} | {r['run']} | {r['passed']}/{r['total']} "
                   f"| {r['warnings']['count']} | {failed} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs")
    ap.add_argument("-j", "--jobs", type=int, default=2)
    ap.add_argument("--results", help="results dir (default: RUNS/../results)")
    a = ap.parse_args()
    runs_root = Path(a.runs).resolve()
    results_dir = Path(a.results) if a.results else runs_root.parent / "results"
    results = grade_all(find_runs(runs_root), max(1, a.jobs))
    results_dir.mkdir(parents=True, exist_ok=True)
    for arm in sorted({r["arm"] for r in results}):
        rs = sorted((r for r in results if r["arm"] == arm), key=lambda r: r["run"])
        (results_dir / f"{arm}.json").write_text(json.dumps({"arm": arm, "runs": rs}, indent=2) + "\n")
    print(markdown(results))


if __name__ == "__main__":
    main()
