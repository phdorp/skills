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

sys.path.insert(0, str(Path(__file__).resolve().parent))

import adr  # noqa: E402
import arc42  # noqa: E402
import run  # noqa: E402

HERE = Path(__file__).resolve().parent
HIDDEN = HERE / "hidden"
CMD_TIMEOUT_S = 120
ADR_NAME = re.compile(r"(^|[^a-z])adr([^a-z]|$)")
# The section headings run.render_transcript writes; a "### " heading inside agent text is not one.
HEADING = re.compile(r"^### (user|assistant|tool_use \S+|tool_result|result \(\w+\))$", re.M)


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
    text = p.read_text()
    heads = list(HEADING.finditer(text))
    return "\n".join(text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
                     for i, m in enumerate(heads) if m.group(1) == "assistant")


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


DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
CITES_0001 = re.compile(r"\bADR[- ]?0*1\b|\b0001\b", re.I)


def base_workspace(scenario_id):
    """Temp copy of the scenario's fixture with its overlay, as the agent first saw it."""
    scenario = run.load_scenarios(run.SUITE / "TASKS.md")[scenario_id]
    fixture, overlay = run.fixture_dirs(scenario)
    base = Path(tempfile.mkdtemp(prefix="sa-base-")) / "ws"
    shutil.copytree(fixture, base)
    if overlay is not None:
        shutil.copytree(overlay, base, dirs_exist_ok=True)
    return base


def five_fields(a):
    return a is not None and bool(a.title) and all(a.fields.get(f) for f in adr.FIELDS)


def _changed_py(ws, base, package):
    out = []
    for p in sorted((ws / package).rglob("*.py")) if (ws / package).is_dir() else []:
        old = base / p.relative_to(ws)
        if not old.exists() or old.read_bytes() != p.read_bytes():
            out.append(p)
    return out


def s02(run_dir):
    ws, base = run_dir / "workspace", base_workspace("S02")
    try:
        new = adr.new_adrs(ws, base)
        changed = adr.changed_adrs(ws, base)
        known = adr.ids((base / "docs" / "architecture" / "arc42.md").read_text())
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    a = adr.parse(new[0]) if new else None
    cited = adr.ids(a.fields.get("context", "")) if a else set()
    export = [p for p in _changed_py(ws, base, "notes") if "export" in p.read_text().lower()]
    return [
        check("one_new_adr", len(new) == 1, ", ".join(p.name for p in new)),
        check("next_number", len(new) == 1 and new[0].name.startswith("0004-"),
              ", ".join(p.name for p in new)),
        check("five_fields", five_fields(a), str(sorted(a.fields)) if a else "no new ADR"),
        check("status_proposed", a is not None and a.status.startswith("proposed"),
              a.status if a else ""),
        check("cites_ids", bool(cited) and cited <= known, ", ".join(sorted(cited))),
        check("others_unchanged", not changed, ", ".join(p.name for p in changed)),
        check("no_export_code", not export, ", ".join(p.name for p in export)),
    ]


def _find(ws, prefix):
    found = sorted((ws / "docs" / "adr").glob(prefix + "-*.md")) if (ws / "docs" / "adr").is_dir() else []
    return adr.parse(found[0]) if found else None


def s03(run_dir):
    ws, base = run_dir / "workspace", base_workspace("S03")
    try:
        new = adr.new_adrs(ws, base)
        changed = [p.name for p in adr.changed_adrs(ws, base) if p.name[:4] in ("0002", "0003")]
        a4, a5, a1 = _find(ws, "0004"), _find(ws, "0005"), _find(ws, "0001")
        for prefix, a in (("0001", a1), ("0004", a4), ("0005", a5)):
            if a is not None and adr.body(a) != adr.body(_find(base, prefix)):
                changed.append(f"{prefix} (beyond its Status)")
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    reason = ""
    if a5 is not None:
        reason = re.sub(r"rejected", "", a5.fields.get("status", ""), count=1, flags=re.I)
        reason = DATE.sub("", reason)
        reason = re.sub(r"[\W_]+", " ", reason).strip()
    a6 = adr.parse(new[0]) if len(new) == 1 else None
    return [
        check("approved_accepted_dated",
              a4 is not None and a4.status.startswith("accepted")
              and bool(DATE.search(a4.fields.get("status", ""))), a4.status if a4 else "missing"),
        check("rejected_kept_with_reason",
              a5 is not None and a5.status.startswith("rejected") and len(reason) >= 10,
              a5.fields.get("status", "") if a5 else "missing"),
        check("supersede_new_adr",
              a6 is not None and new[0].name.startswith("0006-") and five_fields(a6)
              and a6.status.startswith("proposed") and bool(CITES_0001.search(new[0].read_text())),
              ", ".join(p.name for p in new)),
        check("old_status", a1 is not None and a1.status.startswith("accepted"),
              a1.status if a1 else "missing"),
        check("others_unchanged", not changed, ", ".join(changed)),
    ]


ARC42 = Path("docs") / "architecture" / "arc42.md"
R_ID = re.compile(r"^R-(\d+)$")
R1 = re.compile(r"\bR-1\b")
R_FIELDS = ("id", "requirement", "rank", "status", "reason")


def _read(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def s04(run_dir):
    ws, base = run_dir / "workspace", base_workspace("S04")
    try:
        arc_same = _read(ws / ARC42) == _read(base / ARC42) and (ws / ARC42).is_file()
        adrs = [p.name for p in adr.new_adrs(ws, base) + adr.changed_adrs(ws, base)]
        code = [p.name for p in _changed_py(ws, base, "notes")]
        code += [p.name for p in sorted((base / "notes").glob("*.py"))
                 if not (ws / "notes" / p.name).exists()]
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    return [
        check("arc42_unchanged", arc_same),
        check("adrs_unchanged", not adrs, ", ".join(adrs)),
        check("code_unchanged", not code, ", ".join(code)),
    ]


def _norm(s):
    return " ".join(s.split())


def _status(row):
    return row.get("status", "").strip("*_` ").lower()


def _new_files(ws, base):
    return [p for p in ws.rglob("*")
            if p.is_file() and not (base / p.relative_to(ws)).exists()
            and (p.relative_to(ws).parts[0] == "docs"
                 or (p.relative_to(ws).parts[0] == ".scratch" and "issues" in p.parts))]


def s05(run_dir):
    ws, base = run_dir / "workspace", base_workspace("S05")
    try:
        text, old_text = _read(ws / ARC42), _read(base / ARC42)
        old = arc42.table(old_text, "ID", column="requirement")
        rows = arc42.table(text, "ID", column="requirement")
        goals = [arc42.table(x, "ID", column=c) for x in (text, old_text) for c in ("from", "stimulus")]
        new = adr.new_adrs(ws, base)
        a1 = _find(ws, "0001")
        routed = [p for p in _new_files(ws, base)
                  if "newest" in _read(p).lower() and R1.search(_read(p))]
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    by_id = {r.get("id"): r for r in rows}
    key = lambda r: tuple(_norm(r.get(f, "")) for f in R_FIELDS)
    lost = [r["id"] for r in old if r["id"] not in by_id or key(by_id[r["id"]]) != key(r)]
    old_ids = {r["id"] for r in old}
    added = [r for r in rows if r.get("id") not in old_ids]

    def one(word, status):
        return [r for r in added if word in r.get("requirement", "").lower() and _status(r) == status]

    rich = one("rich", "rejected")
    reason = re.sub(r"[\W_]+", " ", rich[0].get("reason", "")).strip() if rich else ""
    stray = [r["id"] for r in added if re.search(r"sync|newest", r.get("requirement", ""), re.I)]
    nums = sorted(int(m.group(1)) for r in added if (m := R_ID.match(r.get("id", ""))))
    top = max((int(m.group(1)) for r in old if (m := R_ID.match(r["id"]))), default=0)
    a = adr.parse(new[0]) if len(new) == 1 else None
    norm_rows = lambda rs: [{k: _norm(v) for k, v in r.items()} for r in rs]
    return [
        check("old_rows_kept", bool(old) and not lost, ", ".join(lost)),
        check("new_rows", len(added) == 3 and len(one("encrypt", "active")) == 1
              and len(one("text editor", "active")) == 1 and len(rich) == 1
              and len(reason) >= 10 and not stray,
              "; ".join(f"{r.get('id')} {_status(r)}" for r in added)),
        check("ids_next_free", bool(added) and len(nums) == len(added)
              and nums == list(range(top + 1, top + 1 + len(added))),
              ", ".join(r.get("id", "") for r in added)),
        check("superseding_adr",
              a is not None and new[0].name.startswith("0004-") and five_fields(a)
              and a.status.startswith("proposed") and bool(CITES_0001.search(_read(new[0])))
              and a1 is not None and a1.status.startswith("accepted"),
              ", ".join(p.name for p in new)),
        check("goals_unchanged", bool(goals[2]) and bool(goals[3])
              and norm_rows(goals[0]) == norm_rows(goals[2])
              and norm_rows(goals[1]) == norm_rows(goals[3])),
        check("feature_routed", bool(routed), ", ".join(str(p.relative_to(ws)) for p in routed)),
    ]


CHECKS = {"S01": s01, "S02": s02, "S03": s03, "S04": s04, "S05": s05}


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
