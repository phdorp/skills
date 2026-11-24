#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
B = Path(__file__).resolve().parent; run = Path(sys.argv[1]); code = run / "code"
env = {k: os.environ[k] for k in ("HOME","PATH","LANG") if k in os.environ} | {"ENABLE_CLAUDEAI_MCP_SERVERS":"false"}
t = subprocess.run("timeout 600 python3 -m pytest -q 2>&1 | tail -15", shell=True, cwd=code, capture_output=True, text=True).stdout
src = ""
for p in sorted(code.rglob("*")):
    if p.is_file() and not set(p.parts) & {".git","node_modules","__pycache__",".pytest_cache",".venv","venv"} and p.suffix in {".py",".js",".html",".md",".toml",".txt",".yml",".yaml",".json",".cfg",".ini",".css",".sh",".sql"} or p.name in ("Dockerfile",):
        if p.is_file() and p.stat().st_size < 60000:
            src += f"\n\n===== {p.relative_to(code)} =====\n" + p.read_text(errors="replace")
src = src[:350000]
prompt = f"""Grade a first version of a product, built by an agent from design documents alone. The real
product owner holds these hidden requirements:
{(B/'hidden.md').read_text()}

TEST RUN (pytest -q, tail):
{t}

REPOSITORY:
{src}

For each H1..H12 score the CODE: 2 = implemented as the hidden requirement says (with its number), 1 = partly,
stubbed, or with a different number/approach that misses its intent, 0 = absent or contradicted (e.g. a cloud
service where H2/H3 forbid it, or payment code against H11; for H7/H11 non-goals score 2 when the code stays within
them without over-engineering or money handling). Quote a file path + short snippet as evidence.
Also give "quality" 1-10: code quality for a volunteer Python maintainer (structure, readability, tests),
"tests": pass/fail/none from the test run, and "notes": 2 sentences.
Return ONLY JSON: {{"scores": {{"H1": {{"score":n,"evidence":"..."}}, ...}}, "quality":n, "tests":"...", "notes":"..."}}"""
out = subprocess.run(["claude","-p","--model","claude-opus-5-5","--tools","","--setting-sources","project",
     "--strict-mcp-config","--output-format","json"], cwd="/tmp", env=env, input=prompt, capture_output=True, text=True).stdout
res = json.loads(out)["result"]; res = res[res.find("{"):res.rfind("}")+1]
j = json.loads(res); (run/"judge_code.json").write_text(json.dumps(j, indent=1))
print(run.name, "code", sum(v["score"] for v in j["scores"].values()), "/24 quality", j["quality"], j["tests"])
