#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent; run = Path(sys.argv[1])
docs = ""
for p in sorted((run / "workspace").rglob("*")):
    if p.is_file() and ".git" not in p.parts and p.name != "README.md":
        docs += f"\n\n===== FILE {p.relative_to(run/'workspace')} =====\n" + p.read_text(errors="replace")
prompt = f"""You grade a design session. A designer agent interviewed a simulated architect who held hidden
requirements (listed below; the designer never saw them). Grade what the session produced.

HIDDEN REQUIREMENTS:
{(B/'hidden.md').read_text()}

TRANSCRIPT:
{(run/'transcript.md').read_text()}

FILES THE DESIGNER WROTE:
{docs or '(none)'}

For each H1..H12 give a score:
 2 = recorded in the written files, accurately (with its measure/number where the hidden requirement has one)
 1 = surfaced in the dialogue but missing, wrong or vague in the files (or no files written)
 0 = never surfaced
Quote the file or transcript text that justifies each score (short exact quote).
Also report:
 - "questions": total number of distinct questions the designer asked the architect
 - "rounds": number of designer messages that asked something
 - "unasked_decisions": decisions the designer recorded as settled that the architect never made or confirmed (list)
 - "contradictions": anything written that contradicts a hidden requirement (list)
 - "extras": useful things recorded that go beyond the hidden list (short list)
 - "artifact": one line on what was written (files, structure)
Return ONLY JSON: {{"scores": {{"H1": {{"score":n,"quote":"..."}}, ...}}, "questions":n, "rounds":n,
"unasked_decisions":[...], "contradictions":[...], "extras":[...], "artifact":"..."}}"""
env = {k: os.environ[k] for k in ("HOME","PATH","LANG") if k in os.environ} | {"ENABLE_CLAUDEAI_MCP_SERVERS":"false"}
out = subprocess.run(["claude","-p",prompt,"--model","claude-opus-5-5","--tools","","--setting-sources","project",
     "--strict-mcp-config","--output-format","json"], cwd="/tmp", env=env, capture_output=True, text=True).stdout
res = json.loads(out)["result"].strip()
res = res[res.find("{"):res.rfind("}")+1]
j = json.loads(res); (run/"judge.json").write_text(json.dumps(j, indent=1))
print(run.name, sum(v["score"] for v in j["scores"].values()), "/24")
