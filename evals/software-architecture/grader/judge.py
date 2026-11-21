#!/usr/bin/env python3
"""Score one run against ../RUBRIC.md with a judge agent (Claude Opus 5.5).

Usage:  python3 -I judge.py RUN_DIR [--scenario SNN]

The scenario defaults to the run directory's name prefix (S01-r2 -> S01). The judge gets the
task, the criteria, transcript.md and the workspace's text files in one prompt, with no tools,
in an empty temp directory with the same isolated settings as the runs. Every verdict must quote
its evidence; verify_quotes() checks each quote occurs (whitespace-normalised) in its source.
Writes RUN_DIR/judge.json: {"verdicts", "quote_errors", "needs_review", "cost_usd"}.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import run  # noqa: E402

JUDGE_MODEL = "claude-opus-5-5"
JUDGE_TIMEOUT_S = 900
FILE_MAX = 100_000
SECTION = re.compile(r"^## (S\d+)\s*$", re.M)
CRITERION = re.compile(r"^- \*\*(J\d+)\*\*:\s*(.+)$", re.M)
JSON_BLOCK = re.compile(r"```json\s*\n(.*?)```", re.S)


@dataclass
class Criterion:
    id: str
    text: str


def load_rubric(rubric_md):
    text = Path(rubric_md).read_text()
    heads = list(SECTION.finditer(text))
    rubric = {}
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        rubric[m.group(1)] = [Criterion(c, t.strip()) for c, t in CRITERION.findall(body)]
    return rubric


def _workspace_files(run_dir):
    ws = Path(run_dir) / "workspace"
    if not ws.is_dir():
        return []
    files = []
    for p in sorted(ws.rglob("*")):
        if not p.is_file() or p.stat().st_size > FILE_MAX:
            continue
        try:
            files.append((p.relative_to(run_dir).as_posix(), p.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            continue
    return files


def build_prompt(scenario, criteria, run_dir):
    run_dir = Path(run_dir)
    transcript = run_dir / "transcript.md"
    files = "\n".join(f"=== {name} ===\n{text}" for name, text in _workspace_files(run_dir))
    return ((HERE / "judge-prompt.md").read_text()
            .replace("{{TASK}}", scenario.prompt.rstrip())
            .replace("{{CRITERIA}}", "\n".join(f"- {c.id}: {c.text}" for c in criteria))
            .replace("{{TRANSCRIPT}}", transcript.read_text() if transcript.exists() else "(none)")
            .replace("{{FILES}}", files or "(no workspace files)"))


def parse_verdicts(text):
    blocks = JSON_BLOCK.findall(text)
    if not blocks:
        raise ValueError("no ```json block in judge output")
    verdicts = json.loads(blocks[-1])
    if not isinstance(verdicts, list):
        raise ValueError("judge output is not a list of verdicts")
    return verdicts


def _norm(s):
    return " ".join(s.split())


def verify_quotes(verdicts, run_dir):
    run_dir = Path(run_dir).resolve()
    errors = []
    for v in verdicts:
        cid, quote, source = v.get("criterion"), _norm(v.get("quote") or ""), v.get("source") or ""
        path = (run_dir / source).resolve()
        if not quote:
            errors.append(f"{cid}: empty quote")
        elif not path.is_relative_to(run_dir) or not path.is_file():
            errors.append(f"{cid}: source not in run: {source}")
        elif quote not in _norm(path.read_text(encoding="utf-8", errors="replace")):
            errors.append(f"{cid}: quote not found in {source}")
    return errors


def assess(verdicts, criterion_ids, run_dir):
    errors = verify_quotes(verdicts, run_dir)
    given = [v.get("criterion") for v in verdicts]
    errors += [f"{c}: no verdict" for c in criterion_ids if c not in given]
    errors += [f"{c}: more than one verdict" for c in set(given) if given.count(c) > 1]
    return {"verdicts": verdicts, "quote_errors": errors, "needs_review": bool(errors)}


def _judge(prompt):
    cmd = ["claude", "-p", "--model", JUDGE_MODEL, "--setting-sources", "project",
           "--tools", "", "--output-format", "json"]
    with tempfile.TemporaryDirectory(prefix="sa-judge-") as cwd:
        p = subprocess.run(cmd, input=prompt, cwd=cwd, env=run._child_env(), capture_output=True,
                           text=True, timeout=JUDGE_TIMEOUT_S)
    out = json.loads(p.stdout)
    return out.get("result", ""), out.get("total_cost_usd")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--scenario")
    a = ap.parse_args()
    run_dir = Path(a.run_dir)
    sid = a.scenario or run_dir.name.split("-")[0]
    scenario = run.load_scenarios(run.SUITE / "TASKS.md")[sid]
    criteria = load_rubric(run.SUITE / "RUBRIC.md")[sid]
    text, cost = _judge(build_prompt(scenario, criteria, run_dir))
    try:
        result = assess(parse_verdicts(text), [c.id for c in criteria], run_dir)
    except (ValueError, json.JSONDecodeError) as e:
        result = {"verdicts": [], "quote_errors": [f"unparseable judge output: {e}"],
                  "needs_review": True, "raw": text}
    result["cost_usd"] = cost
    (run_dir / "judge.json").write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
    passed = sum(bool(v.get("pass")) for v in result["verdicts"])
    print(f"{run_dir}: {passed}/{len(criteria)} criteria pass, "
          f"needs_review {result['needs_review']}, ${cost}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
