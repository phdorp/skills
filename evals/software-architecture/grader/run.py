#!/usr/bin/env python3
"""Run one software-architecture scenario on one arm (see ../README.md).

Usage:
  python3 -I run.py probe --ref REF
  python3 -I run.py run SCENARIO --arm ARM --ref REF -k K

An arm's skills come from `git archive REF` exported into a directory named `sa`, loaded with
--plugin-dir, so they appear as `sa:<skill>` on every arm. The scenario runs in a fresh temp
workspace outside this repository (so the repo's AGENTS.md and git root stay invisible), with
--setting-sources project (so ~/.claude/skills stays out) and a clean environment (so the child
is not treated as a child session of whoever starts it). The stream-json init event proves
isolation; a run that fails it is still saved, with isolation_ok false, and is not scored.

Writes runs/<arm>/<scenario>-r<k>/: workspace/ (without .git), git-log.txt, transcript.jsonl,
transcript.md, meta.json.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

MODEL = "claude-haiku-5-5"
EFFORT = "medium"
TIMEOUT_S = 1800
CHILD_ENV_KEYS = ("HOME", "PATH", "LANG")
PLUGIN_NAME = "sa"
BUILTIN_COLLISIONS = frozenset({"code-review"})  # CLI built-in skills that share a user skill name
TOOL_RESULT_MAX = 4000

SUITE = Path(__file__).resolve().parents[1]
REPO_ROOT = SUITE.parents[1]
USER_SKILLS = Path.home() / ".claude" / "skills"

SECTION = re.compile(r"^## (S\d+)\b.*$", re.M)
FIXTURE = re.compile(r"^Fixture:\s*(\S+)\s*$", re.M)
OVERLAY = re.compile(r"^Overlay:\s*(\S+)\s*$", re.M)
INVOKE = re.compile(r"^Invoke:\s*(\S+)\s*$", re.M)
PROMPT = re.compile(r"^```text\n(.*?)^```\s*$", re.M | re.S)
REPLY = re.compile(r"^```reply\n(.*?)^```\s*$", re.M | re.S)


@dataclass
class Scenario:
    id: str
    fixture: str
    prompt: str
    overlay: str | None = None
    invoke: str | None = None
    replies: list[str] = field(default_factory=list)


def load_scenarios(tasks_md):
    text = Path(tasks_md).read_text()
    heads = list(SECTION.finditer(text))
    scenarios = {}
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        fixture = FIXTURE.search(body)
        prompts = PROMPT.findall(body)
        if not fixture:
            raise ValueError(f"{m.group(1)}: no 'Fixture:' line")
        if len(prompts) != 1:
            raise ValueError(f"{m.group(1)}: expected one ```text block, found {len(prompts)}")
        overlay, invoke = OVERLAY.search(body), INVOKE.search(body)
        scenarios[m.group(1)] = Scenario(m.group(1), fixture.group(1), prompts[0],
                                         overlay.group(1) if overlay else None,
                                         invoke.group(1) if invoke else None,
                                         REPLY.findall(body))
    return scenarios


def build_prompt(scenario, plugin_dir):
    """The prompt, prefixed with `/sa:<invoke> ` when the arm has the user-invoked skill."""
    if scenario.invoke and (Path(plugin_dir) / "skills" / scenario.invoke / "SKILL.md").is_file():
        return f"/{PLUGIN_NAME}:{scenario.invoke} {scenario.prompt}"
    return scenario.prompt


def _git(*args, cwd=REPO_ROOT, **kw):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True,
                          **kw).stdout


def export_arm(ref, dest):
    out = Path(dest) / PLUGIN_NAME
    out.mkdir(parents=True)
    archive = subprocess.run(["git", "archive", ref], cwd=REPO_ROOT, check=True,
                             capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(out)], input=archive, check=True)
    return out


def prepare_workspace(fixture_dir, overlay_dir=None):
    ws = Path(tempfile.mkdtemp(prefix="sa-eval-")) / "project"
    if fixture_dir is None:
        ws.mkdir()
    else:
        shutil.copytree(fixture_dir, ws)
    if overlay_dir is not None:
        shutil.copytree(overlay_dir, ws, dirs_exist_ok=True)
    _git("init", "-q", cwd=ws)
    _git("add", "-A", cwd=ws)
    _git("-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "commit", "-q",
         "--allow-empty", "-m", "fixture", cwd=ws)
    return ws


def turn_errors(inits, plugin_dir, user_skill_names):
    """Isolation errors over every turn's init event; all turns must share turn 1's session."""
    errors = []
    for k, init in enumerate(inits, 1):
        if not init:
            errors.append(f"turn {k}: no init event")
            continue
        errors += [e if k == 1 else f"turn {k}: {e}"
                   for e in check_isolation(init, plugin_dir, user_skill_names)]
        if k > 1 and inits[0] and init.get("session_id") != inits[0].get("session_id"):
            errors.append(f"turn {k}: session {init.get('session_id')} is not turn 1's "
                          f"{inits[0].get('session_id')}")
    return errors


def check_isolation(init, plugin_dir, user_skill_names):
    plugin_dir = Path(plugin_dir).resolve()
    errors = []
    loaded = [p for p in init.get("plugins", []) if p.get("path") != "builtin"]
    for p in loaded:
        if Path(p["path"]).resolve() != plugin_dir:
            errors.append(f"foreign plugin loaded: {p.get('name')} at {p['path']}")
    if not any(Path(p["path"]).resolve() == plugin_dir for p in loaded):
        errors.append(f"arm plugin not loaded: {plugin_dir}")
    skills = set(init.get("skills", []))
    prefix = plugin_dir.name + ":"
    expected = {prefix + d.name for d in (plugin_dir / "skills").iterdir() if d.is_dir()}
    got = {s for s in skills if s.startswith(prefix)}
    errors += [f"arm skill missing: {s}" for s in sorted(expected - got)]
    errors += [f"unexpected arm skill: {s}" for s in sorted(got - expected)]
    errors += [f"MCP server loaded: {m.get('name')} ({m.get('source', '?')})"
               for m in init.get("mcp_servers", [])]
    errors += [f"user skill visible: {s}"
               for s in sorted((set(user_skill_names) - BUILTIN_COLLISIONS) & skills)]
    return errors


def _events(jsonl):
    for line in Path(jsonl).read_text().splitlines():
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _result_text(content):
    if isinstance(content, str):
        return content
    return "\n".join(c.get("text", "") for c in content or [] if isinstance(c, dict))


def render_transcript(jsonl, prompt):
    parts = [f"### user\n\n{prompt.rstrip()}"]
    for ev in _events(jsonl):
        kind = ev.get("type")
        content = (ev.get("message") or {}).get("content")
        if kind == "assistant":
            for c in content or []:
                if c.get("type") == "text" and c.get("text", "").strip():
                    parts.append(f"### assistant\n\n{c['text'].rstrip()}")
                elif c.get("type") == "tool_use":
                    body = json.dumps(c.get("input"), indent=1, ensure_ascii=False)
                    parts.append(f"### tool_use {c.get('name')}\n\n```json\n{body}\n```")
        elif kind == "user" and isinstance(content, list):
            for c in content:
                if c.get("type") == "tool_result":
                    text = _result_text(c.get("content"))
                    if len(text) > TOOL_RESULT_MAX:
                        text = text[:TOOL_RESULT_MAX] + f"\n[... {len(text) - TOOL_RESULT_MAX} chars cut]"
                    parts.append(f"### tool_result\n\n```\n{text}\n```")
        elif kind == "result":
            parts.append(f"### result ({ev.get('subtype')})")
    return "\n\n".join(parts) + "\n"


def render_turns(turns):
    """One transcript of every (jsonl, prompt) turn, in order."""
    return "\n".join(render_transcript(jsonl, prompt) for jsonl, prompt in turns)


def turn_summary(codes, costs, expected):
    """Exit code, cost and run errors over the turns that ran (expected: turns in the scenario).

    exit_code is the first non-zero code, else the last; cost is None when any turn reported
    none. In a multi-turn run a failed turn is an error, since later turns built on it.
    """
    failed = [c for c in codes if c != 0]
    errors = [f"turn {k} exited {c}" for k, c in enumerate(codes, 1) if c != 0 and expected > 1]
    if len(codes) < expected:
        errors.append(f"only {len(codes)} of {expected} turns ran")
    cost = None if not costs or any(c is None for c in costs) else round(sum(costs), 6)
    return {"exit_codes": list(codes), "exit_code": failed[0] if failed else (codes[-1] if codes else None),
            "cost_usd": cost, "errors": errors}


def fixture_dirs(scenario, suite=SUITE):
    """(fixture_dir, overlay_dir or None) of a scenario."""
    fixtures = Path(suite) / "fixtures"
    overlay = fixtures / "overlays" / scenario.overlay if scenario.overlay else None
    return fixtures / scenario.fixture, overlay


def new_run_dir(suite, arm, scenario_id, k):
    run_dir = Path(suite) / "runs" / arm / f"{scenario_id}-r{k}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def _child_env():
    env = {k: os.environ[k] for k in CHILD_ENV_KEYS if k in os.environ}
    env["IS_SANDBOX"] = "1"
    env["ENABLE_CLAUDEAI_MCP_SERVERS"] = "false"  # the account's claude.ai connectors stay out
    return env


def claude_cmd(prompt, plugin_dir, resume=None):
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--effort", EFFORT,
           "--setting-sources", "project", "--plugin-dir", str(plugin_dir), "--strict-mcp-config",
           "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions"]
    return cmd + ["--resume", resume] if resume else cmd


def _claude(prompt, cwd, plugin_dir, out_jsonl, resume=None):
    cmd = claude_cmd(prompt, plugin_dir, resume)
    start = time.time()
    with open(out_jsonl, "w") as out:
        try:
            code = subprocess.run(cmd, cwd=cwd, env=_child_env(), stdout=out,
                                  stderr=subprocess.DEVNULL, timeout=TIMEOUT_S).returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    return code, round(time.time() - start, 1)


def _init_and_cost(jsonl):
    init, cost = {}, None
    for ev in _events(jsonl):
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            init = ev
        elif ev.get("type") == "result":
            cost = ev.get("total_cost_usd")
    return init, cost


def _user_skill_names():
    return {p.name for p in USER_SKILLS.iterdir()} if USER_SKILLS.is_dir() else set()


def run_scenario(scenario, arm, ref, k, suite=SUITE):
    run_dir = new_run_dir(suite, arm, scenario.id, k)
    tmp = Path(tempfile.mkdtemp(prefix="sa-arm-"))
    try:
        plugin_dir = export_arm(ref, tmp)
        ws = prepare_workspace(*fixture_dirs(scenario, suite))
        prompt = build_prompt(scenario, plugin_dir)
        turns, inits, costs, codes, duration = [], [], [], [], 0.0
        for turn, text in enumerate([prompt] + scenario.replies, 1):
            if turn > 1:
                shutil.copytree(ws, run_dir / f"workspace-t{turn - 1}",
                                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            jsonl = run_dir / ("transcript.jsonl" if turn == 1 else f"transcript-t{turn}.jsonl")
            session = inits[0].get("session_id") if inits and inits[0] else None
            if turn > 1 and not session:
                break
            code, seconds = _claude(text, ws, plugin_dir, jsonl, resume=session)
            init, cost = _init_and_cost(jsonl)
            turns.append((jsonl, text))
            inits.append(init)
            costs.append(cost)
            codes.append(code)
            duration += seconds
        summary = turn_summary(codes, costs, 1 + len(scenario.replies))
        errors = turn_errors(inits, plugin_dir, _user_skill_names()) + summary["errors"]
        (run_dir / "transcript.md").write_text(render_turns(turns))
        (run_dir / "git-log.txt").write_text(_git("log", "--format=%H %s", cwd=ws))
        shutil.copytree(ws, run_dir / "workspace",
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        meta = {"scenario": scenario.id, "arm": arm, "ref": ref,
                "sha": _git("rev-parse", ref).strip(), "model": MODEL, "effort": EFFORT,
                "cost_usd": summary["cost_usd"], "duration_s": round(duration, 1),
                "exit_code": summary["exit_code"], "exit_codes": summary["exit_codes"],
                "turns": len(turns), "session_ids": [i.get("session_id") for i in inits],
                "invoked": prompt != scenario.prompt,
                "isolation_ok": not errors, "isolation_errors": errors}
        (run_dir / "meta.json").write_text(json.dumps(meta, indent=1) + "\n")
        shutil.rmtree(ws.parent, ignore_errors=True)
        return run_dir
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def probe(ref):
    tmp = Path(tempfile.mkdtemp(prefix="sa-probe-"))
    try:
        plugin_dir = export_arm(ref, tmp)
        ws = prepare_workspace(None)
        jsonl = tmp / "probe.jsonl"
        _claude("Reply OK.", ws, plugin_dir, jsonl)
        init, _ = _init_and_cost(jsonl)
        errors = check_isolation(init, plugin_dir, _user_skill_names()) if init else ["no init event"]
        shutil.rmtree(ws.parent, ignore_errors=True)
        if errors:
            print("\n".join(errors))
            return 1
        n = sum(1 for s in init["skills"] if s.startswith(PLUGIN_NAME + ":"))
        print(f"isolation ok ({n} {PLUGIN_NAME}: skills, ref {ref})")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("probe")
    p.add_argument("--ref", required=True)
    r = sub.add_parser("run")
    r.add_argument("scenario")
    r.add_argument("--arm", required=True)
    r.add_argument("--ref", required=True)
    r.add_argument("-k", type=int, required=True)
    a = ap.parse_args()
    if a.cmd == "probe":
        return probe(a.ref)
    scenario = load_scenarios(SUITE / "TASKS.md")[a.scenario]
    run_dir = run_scenario(scenario, a.arm, a.ref, a.k)
    meta = json.loads((run_dir / "meta.json").read_text())
    print(f"{run_dir}: exit {meta['exit_code']}, isolation_ok {meta['isolation_ok']}, "
          f"${meta['cost_usd']}")
    return 0 if meta["isolation_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
