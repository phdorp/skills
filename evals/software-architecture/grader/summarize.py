#!/usr/bin/env python3
"""Grade every RUNS/<arm>/<scenario>-r<k> and summarise.

Usage:  python3 -I summarize.py RUNS [--results DIR]

Writes <results>/<arm>.json (default results dir: RUNS/../results) and prints a Markdown summary.
Each run carries its grade, its judge.json (or null) and `valid` (meta.json isolation_ok).
Invalid runs are graded but left out of the scores and listed. A run needs review when its
judge flagged it, or when grader and judge disagree: every check passed but a criterion
failed, or a check failed but every criterion passed.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

RUN_NAME = re.compile(r"^(S\d+)-r(\d+)$")


def _load_grade():
    path = Path(__file__).resolve().parent / "grade.py"
    spec = importlib.util.spec_from_file_location("sa_grade", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


grade_mod = _load_grade()


def _json(path):
    return json.loads(path.read_text()) if path.exists() else None


def judge_rate(judge):
    if not judge or not judge.get("verdicts"):
        return None
    v = judge["verdicts"]
    return round(sum(bool(x.get("pass")) for x in v) / len(v), 3)


def needs_review(result):
    judge, rate = result["judge"], judge_rate(result["judge"])
    if judge is None or not result["valid"]:
        return False
    if judge.get("needs_review"):
        return True
    return (result["score"] == 1.0 and rate < 1.0) or (result["score"] < 1.0 and rate == 1.0)


def summarize_arm(arm_dir):
    runs = []
    for run in sorted(p for p in arm_dir.iterdir() if p.is_dir()):
        m = RUN_NAME.match(run.name)
        if not m or m.group(1) not in grade_mod.CHECKS:
            print(f"skipping {run}", file=sys.stderr)
            continue
        print(f"grading {run}", file=sys.stderr)
        r = grade_mod.grade(m.group(1), run)
        meta = _json(run / "meta.json") or {}
        r.update(valid=bool(meta.get("isolation_ok")), judge=_json(run / "judge.json"),
                 cost_usd=meta.get("cost_usd"))
        r["needs_review"] = needs_review(r)
        runs.append(r)
    scenarios = {}
    for r in runs:
        if r["valid"]:
            scenarios.setdefault(r["scenario"], []).append(r)
    summary = {}
    for sc, rs in sorted(scenarios.items()):
        rates = [judge_rate(r["judge"]) for r in rs if judge_rate(r["judge"]) is not None]
        summary[sc] = {"runs": len(rs),
                       "score": round(sum(r["score"] for r in rs) / len(rs), 3),
                       "judge": round(sum(rates) / len(rates), 3) if rates else None,
                       "cost_usd": round(sum(r["cost_usd"] or 0 for r in rs), 3)}
    return {"arm": arm_dir.name, "summary": summary, "runs": runs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs")
    ap.add_argument("--results")
    a = ap.parse_args()
    runs_root = Path(a.runs).resolve()
    out_dir = Path(a.results) if a.results else runs_root.parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = ["| arm | scenario | valid runs | grader | judge | cost $ |", "|---|---|---:|---:|---:|---:|"]
    flagged = []
    for arm_dir in sorted(p for p in runs_root.iterdir() if p.is_dir()):
        res = summarize_arm(arm_dir)
        (out_dir / f"{res['arm']}.json").write_text(json.dumps(res, indent=1) + "\n")
        for sc, s in res["summary"].items():
            judge = "-" if s["judge"] is None else f"{s['judge']:.3f}"
            lines.append(f"| {res['arm']} | {sc} | {s['runs']} | {s['score']:.3f} | {judge} | "
                         f"{s['cost_usd']:.2f} |")
        flagged += [f"- {res['arm']}/{r['run']}: invalid (isolation)" for r in res["runs"]
                    if not r["valid"]]
        flagged += [f"- {res['arm']}/{r['run']}: needs review" for r in res["runs"]
                    if r["needs_review"]]
    print("\n".join(lines))
    if flagged:
        print("\nFlagged runs:\n" + "\n".join(flagged))
    return 0


if __name__ == "__main__":
    sys.exit(main())
