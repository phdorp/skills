#!/usr/bin/env python3
"""Usage: drive.py <arm> <k>. Arm plugin: arms/<arm>/sa (see README.md).
Drive one arm: designer (claude -p, arm plugin) <-> simulated architect (no tools)."""
import json, os, shutil, subprocess, sys, time
from pathlib import Path
B = Path(__file__).resolve().parent
arm, k = sys.argv[1], sys.argv[2]
MAX = 10
SETUP = "/sa:setup-architecture Set up the architecture for this project. The idea is in README.md."
GRILL = "/sa:grill-me Grill me on the design of this project. The idea is in README.md."
PROMPTS = {"grill": GRILL}  # every other arm is a setup-architecture arm
run = B / "runs" / f"{arm}-r{k}"; ws = run / "workspace"
shutil.copytree(B / "project", ws)
env = {k_: os.environ[k_] for k_ in ("HOME", "PATH", "LANG") if k_ in os.environ}
env |= {"IS_SANDBOX": "1", "ENABLE_CLAUDEAI_MCP_SERVERS": "false"}
subprocess.run("git init -q && git add -A && git -c user.name=e -c user.email=e@x commit -qm init", shell=True, cwd=ws)
plugin = B / "arms" / arm / "sa"
system = (B / "architect-system.md").read_text()

def designer(prompt, session):
    cmd = ["claude", "-p", prompt, "--model", "claude-haiku-5-5", "--effort", "medium",
           "--setting-sources", "project", "--plugin-dir", str(plugin), "--strict-mcp-config",
           "--output-format", "json", "--dangerously-skip-permissions"]
    if session: cmd += ["--resume", session]
    out = subprocess.run(cmd, cwd=ws, env=env, capture_output=True, text=True, timeout=1800).stdout
    j = json.loads(out); return j["result"], j["session_id"], j.get("total_cost_usd", 0)

def architect(transcript):
    conv = "\n\n".join(f"### {who}\n{text}" for who, text in transcript)
    prompt = f"Conversation so far:\n\n{conv}\n\nWrite your reply to the designer's last message."
    cmd = ["claude", "-p", prompt, "--model", "claude-sonnet-5-5", "--tools", "", "--system-prompt", system,
           "--setting-sources", "project", "--strict-mcp-config", "--output-format", "json"]
    out = subprocess.run(cmd, cwd="/tmp", env=env, capture_output=True, text=True, timeout=600).stdout
    return json.loads(out)["result"]

transcript, session, cost = [("ARCHITECT (opening prompt)", PROMPTS.get(arm, SETUP))], None, 0
msg = PROMPTS.get(arm, SETUP)
for turn in range(MAX + 1):
    text, session, c = designer(msg, session); cost += c
    transcript.append(("DESIGNER", text))
    if turn == MAX: break
    reply = architect(transcript)
    ended = "[[END]]" in reply
    reply = reply.replace("[[END]]", "").strip()
    transcript.append(("ARCHITECT", reply))
    if ended: break
    msg = reply
(run / "transcript.md").write_text("\n\n".join(f"## {w}\n\n{t}" for w, t in transcript))
(run / "meta.json").write_text(json.dumps({"arm": arm, "designer_turns": sum(w=="DESIGNER" for w,_ in transcript),
    "designer_cost_usd": cost, "ended": transcript[-1][0] == "ARCHITECT"}, indent=1))
print(run, "done", cost)
