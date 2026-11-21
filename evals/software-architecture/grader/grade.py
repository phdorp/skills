#!/usr/bin/env python3
"""Deterministic grader for the software-architecture scenarios (see ../TASKS.md).

Usage:  python3 -I grade.py SCENARIO RUN_DIR

Reads a run directory (workspace/, git-log.txt, transcript.md; see ../README.md), never writes
into it: code runs in a temp copy of workspace/. Prints one JSON object with per-check results.
A run without workspace/ fails every check. Standard library only.

Add a scenario by adding a function to CHECKS that returns a list of check(...) results.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HIDDEN = HERE / "hidden"
CMD_TIMEOUT_S = 120
ADR_NAME = re.compile(r"(^|[^a-z])adr([^a-z]|$)")


def check(name, ok, detail=""):
    return {"name": name, "pass": bool(ok), "detail": detail}


def _run(cmd, cwd):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=CMD_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    return p.returncode == 0, (p.stdout + p.stderr)[-500:]


def _copy(workspace):
    tmp = Path(tempfile.mkdtemp(prefix="sa-grade-")) / "ws"
    shutil.copytree(workspace, tmp)
    return tmp


def assistant_text(run_dir):
    p = run_dir / "transcript.md"
    if not p.exists():
        return ""
    sections = ("\n" + p.read_text()).split("\n### ")
    return "\n".join(s for s in sections if s.startswith("assistant"))


def commits(run_dir):
    p = run_dir / "git-log.txt"
    return [line for line in p.read_text().splitlines() if line.strip()] if p.exists() else []


def adr_files(workspace):
    return [p for p in workspace.rglob("*")
            if p.is_file() and ADR_NAME.search(p.name.lower())]


def s01(run_dir):
    ws = run_dir / "workspace"
    copy = _copy(ws)
    try:
        ok, out = _run([sys.executable, "-m", "unittest"], copy)
        shutil.copy(HIDDEN / "S01_test_top.py", copy / "S01_test_top.py")
        hidden_ok, hidden_out = _run([sys.executable, "-m", "unittest", "S01_test_top"], copy)
    finally:
        shutil.rmtree(copy.parent, ignore_errors=True)
    n = assistant_text(run_dir).count("setup-architecture")
    adrs = adr_files(ws)
    return [
        check("tests_pass", ok, out),
        check("feature_works", hidden_ok, hidden_out),
        check("committed", len(commits(run_dir)) > 1, f"{len(commits(run_dir))} commits"),
        check("no_arc42", not (ws / "docs" / "architecture").exists()),
        check("no_new_adr", not (ws / "docs" / "adr").exists() and not adrs,
              ", ".join(str(p.relative_to(ws)) for p in adrs)),
        check("setup_suggested_at_most_once", n <= 1, f"{n} mentions"),
    ]


CHECKS = {"S01": s01}


def grade(scenario_id, run_dir):
    run_dir = Path(run_dir)
    if (run_dir / "workspace").is_dir():
        checks = CHECKS[scenario_id](run_dir)
    else:
        empty = Path(tempfile.mkdtemp(prefix="sa-empty-"))
        (empty / "workspace").mkdir()
        names = [c["name"] for c in CHECKS[scenario_id](empty)]
        shutil.rmtree(empty, ignore_errors=True)
        checks = [check(n, False, "no workspace") for n in names]
    passed = sum(c["pass"] for c in checks)
    return {"run": run_dir.name, "scenario": scenario_id, "checks": checks, "passed": passed,
            "total": len(checks), "score": round(passed / len(checks), 3) if checks else 0.0}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in CHECKS:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(grade(sys.argv[1], sys.argv[2]), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
