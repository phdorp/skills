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


def _code_changes(ws, base):
    """Changed, added or deleted `notes/*.py` files."""
    code = [p.name for p in _changed_py(ws, base, "notes")]
    return code + [p.name for p in sorted((base / "notes").glob("*.py"))
                   if not (ws / "notes" / p.name).exists()]


def s04(run_dir):
    ws, base = run_dir / "workspace", base_workspace("S04")
    try:
        arc_same = _read(ws / ARC42) == _read(base / ARC42) and (ws / ARC42).is_file()
        adrs = [p.name for p in adr.new_adrs(ws, base) + adr.changed_adrs(ws, base)]
        code = _code_changes(ws, base)
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
    """New issue or spec files: under .scratch/**/issues/, or docs/ outside adr/ and architecture/."""
    out = []
    for p in ws.rglob("*"):
        rel = p.relative_to(ws).parts
        if not p.is_file() or (base / p.relative_to(ws)).exists():
            continue
        if (rel[0] == "docs" and rel[1:2] not in (("adr",), ("architecture",))) \
                or (rel[0] == ".scratch" and "issues" in rel):
            out.append(p)
    return out


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
        code = _code_changes(ws, base)
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
    bare = [r["id"] for r in added if re.fullmatch(r"\d+", r.get("rank", "").strip("*_` "))]
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
        check("ranks_marked_proposed", bool(added) and not bare, ", ".join(bare)),
        check("code_unchanged", not code, ", ".join(code)),
    ]


SECTION_HEAD = re.compile(r"^## (\d{1,2})\.?\s+\S", re.M)
# A measure states a number: digits, "zero", or a quantifier over a count ("all three OSes").
NUMBER_WORD = r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
MEASURE = re.compile(r"\d|\bzero\b|\b(?:all|each|every|both)\s+(?:one\s+of\s+)?(?:the\s+)?"
                     + NUMBER_WORD + r"\b", re.I)


def has_measure(text):
    return bool(MEASURE.search(text))
QG_ID = re.compile(r"\bQG-\d+\b")
QS_ID = re.compile(r"\bQS-\d+\b")
R_ANY = re.compile(r"\bR-\d+\b")
BLOCK_TABLE = re.compile(r"^\|\s*block\s*\|", re.M | re.I)


def _rows(text, column):
    return [r for r in arc42.table(text, "ID", column=column) if r.get("id", "").strip()]


def _section(text, n):
    heads = list(SECTION_HEAD.finditer(text))
    for i, m in enumerate(heads):
        if int(m.group(1)) == n:
            return text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
    return ""


def _files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file()} if root.is_dir() else {}


def goals_measured(text):
    """1-5 goals, each citing existing R-IDs and a scenario whose measure states a number.

    The spec's "top 3-5" is what the architect confirms; S06 and S07 tell the agent to leave
    unmeasured goals open, so fewer than three measured goals can be right.
    """
    rids = {r["id"] for r in _rows(text, "requirement")}
    goals, scen = _rows(text, "from"), {r["id"]: r for r in _rows(text, "stimulus")}

    def measured(g):
        cited = set(R_ANY.findall(g.get("from", "")))
        qs = QS_ID.findall(g.get("scenario", ""))
        return (bool(cited) and cited <= rids and bool(qs)
                and all(q in scen and has_measure(scen[q].get("measure", "")) for q in qs))

    ok = 1 <= len(goals) <= 5 and all(measured(g) for g in goals)
    return ok, ", ".join(f"{g['id']}{'' if measured(g) else ' (unmeasured or uncited)'}" for g in goals)


def s06(run_dir):
    ws, t1, base = run_dir / "workspace", run_dir / "workspace-t1", base_workspace("S06")
    try:
        before, after_t1 = _files(base), _files(t1)
        new_t1 = sorted(k for k, v in after_t1.items() if before.get(k) != v)
        routed_files = _new_files(ws, base)
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    t1_text, text = _read(t1 / ARC42), _read(ws / ARC42)
    t1_rows = sum(len(_rows(t1_text, c)) for c in ("requirement", "from", "stimulus"))
    heads = [int(m.group(1)) for m in SECTION_HEAD.finditer(text)]
    rows = _rows(text, "requirement")
    rids = [r["id"] for r in rows]
    statuses = {_status(r) for r in rows}
    goals, scen = _rows(text, "from"), {r["id"]: r for r in _rows(text, "stimulus")}
    adrs = sorted((ws / "docs" / "adr").glob("*.md")) if (ws / "docs" / "adr").is_dir() else []
    a = adr.parse(adrs[0]) if len(adrs) == 1 else None
    known = set(rids) | {g["id"] for g in goals} | set(scen)
    cited = adr.ids(a.fields.get("context", "")) if a else set()
    routed = [p for p in routed_files
              if "latest" in _read(p).lower() and set(R_ANY.findall(_read(p))) & set(rids)]
    return [
        check("t1_only_skeleton", t1.is_dir() and new_t1 == [ARC42.as_posix()] and t1_rows == 0,
              f"new: {', '.join(new_t1)}; rows: {t1_rows}" if t1.is_dir() else "no workspace-t1"),
        check("headings", heads == list(range(1, 13)), str(heads)),
        check("rlist", len(rows) >= 4 and rids == [f"R-{i}" for i in range(1, len(rows) + 1)]
              and statuses <= {"active", "deferred", "rejected"}
              and not any("latest" in r.get("requirement", "").lower() for r in rows),
              ", ".join(f"{r['id']} {_status(r)}" for r in rows)),
        check("goals_measured", *goals_measured(text)),
        check("adr_0001", a is not None and adrs[0].name.startswith("0001-")
              and "record architecture decisions" in a.title.lower() and five_fields(a)
              and a.status.startswith("proposed") and bool(cited) and cited <= known,
              f"{', '.join(p.name for p in adrs)}; status {a.status if a else '-'}; cites {sorted(cited)}"),
        check("section5_started", bool(BLOCK_TABLE.search(_section(text, 5)))),
        check("section9_links_adr", "adr/" in _section(text, 9)),
        check("feature_routed", bool(routed), ", ".join(str(p.relative_to(ws)) for p in routed)),
    ]


DECISIONS = Path("docs") / "decisions"
LEGACY = {"0001": "one json file", "0002": "checked locally"}
README_SENTENCE = "`cli` calls `catalog`, never the file directly."


def _t1_untouched(t1, base):
    """(ok, detail): turn 1 added only arc42.md, changed nothing, and filled no table."""
    if not t1.is_dir():
        return False, "no workspace-t1"
    before, after = _files(base), _files(t1)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    rows = sum(len(_rows(_read(t1 / ARC42), c)) for c in ("requirement", "from", "stimulus"))
    return changed == [ARC42.as_posix()] and rows == 0, f"changed: {', '.join(changed)}; rows: {rows}"


def s07(run_dir):
    ws, t1, base = run_dir / "workspace", run_dir / "workspace-t1", base_workspace("S07")
    try:
        t1_ok, t1_detail = _t1_untouched(t1, base)
        before, after = _files(base), _files(ws)
        missing = sorted(set(before) - set(after))
        readme_lost = [line for line in before.get("README.md", b"").decode().splitlines()
                       if line.strip() and line not in after.get("README.md", b"").decode().splitlines()]
        code = [k for k in before if k.startswith("shelf/") and before[k] != after.get(k)]
        new_adrs = sorted(k for k in after if k not in before and k.endswith(".md")
                          and (k.startswith("docs/decisions/") or k.startswith("docs/adr/")))
    finally:
        shutil.rmtree(base.parent, ignore_errors=True)
    text = _read(ws / ARC42)
    heads = [int(m.group(1)) for m in SECTION_HEAD.finditer(text)]
    known = ({r["id"] for r in _rows(text, "requirement")} | {g["id"] for g in _rows(text, "from")}
             | {s["id"] for s in _rows(text, "stimulus")})
    legacy_bad = []
    for prefix, phrase in LEGACY.items():
        found = sorted((ws / DECISIONS).glob(prefix + "-*.md")) if (ws / DECISIONS).is_dir() else []
        a = adr.parse(found[0]) if found else None
        cited = adr.ids(a.fields.get("context", "")) if a else set()
        if not (a and five_fields(a) and a.status.startswith("accepted (legacy)")
                and cited and cited <= known and phrase in _norm(a.fields.get("decision", "")).lower()):
            legacy_bad.append(f"{prefix} ({a.status if a else 'missing'})")
    a3 = adr.parse(ws / new_adrs[0]) if len(new_adrs) == 1 else None
    return [
        check("t1_only_arc42", t1_ok, t1_detail),
        check("docs_kept", not missing and not readme_lost and not code,
              "; ".join(x for x in (", ".join(missing), " | ".join(readme_lost)[:200], ", ".join(code)) if x)),
        check("arc42_links_existing", heads == list(range(1, 13)) and "README.md" in text
              and "decisions/" in text, str(heads)),
        check("no_copy", bool(text) and _norm(README_SENTENCE) not in _norm(text)),
        check("legacy_upgraded", not legacy_bad, ", ".join(legacy_bad)),
        check("made_centrally_next", a3 is not None and new_adrs[0].startswith("docs/decisions/0003-")
              and "record architecture decisions" in a3.title.lower() and a3.status.startswith("proposed")
              and not (ws / "docs" / "adr").exists(), ", ".join(new_adrs)),
        check("goals_measured", *goals_measured(text)),
    ]


CHECKS = {"S01": s01, "S02": s02, "S03": s03, "S04": s04, "S05": s05, "S06": s06, "S07": s07}


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
