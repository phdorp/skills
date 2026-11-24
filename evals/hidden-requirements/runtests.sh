#!/bin/bash
D=$(cd "$(dirname "$0")" && pwd); r=$1; code=$D/runs/$r/code; v=$D/venvs/$r
python3 -m venv $v >/dev/null && cd $code
for f in requirements.txt requirements-dev.txt; do [ -f $f ] && $v/bin/pip install -q -r $f >/dev/null 2>&1; done
[ -f pyproject.toml ] && $v/bin/pip install -q -e ".[dev]" >/dev/null 2>&1 || [ -f pyproject.toml ] && $v/bin/pip install -q -e . >/dev/null 2>&1
$v/bin/pip install -q pytest >/dev/null 2>&1
echo "$r: $(timeout 900 $v/bin/python -m pytest -q -p no:cacheprovider 2>&1 | tail -1)"
