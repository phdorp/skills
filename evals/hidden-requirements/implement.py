#!/usr/bin/env python3
"""Code stage: a fresh agent (no skills) builds v1 from the docs a design run left behind."""
import json, os, shutil, subprocess, sys
from pathlib import Path
run = Path(sys.argv[1]); code = run / "code"
shutil.copytree(run / "workspace", code, ignore=shutil.ignore_patterns(".git"))
env = {k: os.environ[k] for k in ("HOME","PATH","LANG") if k in os.environ} | {"IS_SANDBOX":"1","ENABLE_CLAUDEAI_MCP_SERVERS":"false"}
subprocess.run("git init -q && git add -A && git -c user.name=e -c user.email=e@x commit -qm docs", shell=True, cwd=code)
prompt = ("Build the first version of this product as the documents in this repository describe it. "
          "Nobody is available to answer questions: make every decision the documents leave open yourself "
          "and note it in IMPLEMENTATION.md. Write automated tests and make sure they pass.")
out = subprocess.run(["claude","-p",prompt,"--model","claude-haiku-5-5","--effort","medium",
    "--setting-sources","project","--strict-mcp-config","--output-format","json",
    "--dangerously-skip-permissions"], cwd=code, env=env, capture_output=True, text=True, timeout=3600).stdout
j = json.loads(out); (run/"implement.json").write_text(json.dumps({"cost": j.get("total_cost_usd"), "result": j["result"]}, indent=1))
print(run.name, "implemented", j.get("total_cost_usd"))
