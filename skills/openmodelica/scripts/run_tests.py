"""Simulate every test model of a Modelica file or library with omc and report PASS/FAIL.

Usage: python3 run_tests.py FILE.mo [FILE.mo ...] [NAME-PART ...] [--timeout SECONDS]

Each FILE.mo is a single file (a model, or a package of them) or any file of a library folder
(the top-level package.mo is found by walking up); all of them are loaded together, so a test
file can use a model from another file. Test models are the non-partial models inside a package named Tests,
TestCases or Examples; NAME-PART arguments keep only the models whose name contains one of them.
Each model runs with its own experiment annotation in its own omc process.

A model fails on any omc error or warning, a violated assert, a failed simulation, or no result
within the timeout. Exit code 0 means every selected model passed; 1 means a failure or no test
models; 2 means bad usage.
"""

import concurrent.futures
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

TEST_PACKAGES = {"Tests", "TestCases", "Examples"}
# Runtime warnings that change nothing about the result.
HARMLESS = ("Numerical Jacobians without coloring are currently not supported by GBODE",)


def omc(script, workdir, timeout):
    """Run a .mos script in workdir; return its stdout, or None after the timeout."""
    path = os.path.join(workdir, "run.mos")
    with open(path, "w") as f:
        f.write(script)
    proc = subprocess.Popen(["omc", path], cwd=workdir, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        return proc.communicate(timeout=timeout)[0]
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)  # also the simulation process omc started
        proc.communicate()
        return None


def section(out, name):
    """Text between '@@NAME' and the next '@@' marker."""
    m = re.search(r"^@@" + name + r"\n(.*?)(?=^@@)", out, re.S | re.M)
    return m.group(1).strip() if m else ""


def top_file(path):
    path = os.path.abspath(path)
    folder = os.path.dirname(path)
    if not os.path.exists(os.path.join(folder, "package.mo")):
        return path
    while os.path.exists(os.path.join(os.path.dirname(folder), "package.mo")):
        folder = os.path.dirname(folder)
    return os.path.join(folder, "package.mo")


def load(paths):
    # omc collects messages until getErrorString() returns them; the calls echo only true/false
    return ('loadModel(Modelica);\n'
            + "".join(f'loadFile("{p}");\n' for p in paths)
            + 'print("@@LOAD\\n" + getErrorString() + "\\n@@END\\n");\n')


def list_models(paths, workdir, timeout):
    script = load(paths) + "".join(
        f'for top in parseFile("{p}") loop\n'
        '  for cl in getClassNames(top, recursive = true, qualified = true) loop\n'
        '    if isModel(cl) and not isPartial(cl) then\n'
        '      print("@@MODEL " + typeNameString(cl) + "\\n");\n'
        '    end if;\n'
        '  end for;\n'
        'end for;\n' for p in paths)
    out = omc(script, workdir, timeout)
    if out is None:
        return None, []
    models = re.findall(r"^@@MODEL (\S+)$", out, re.M)
    return section(out, "LOAD"), models


def problems(errors, messages):
    """The lines that make a run fail, each message once."""
    # an omc message starts with [file:line], Error or Warning and may continue on more lines
    blocks = re.split(r"(?m)^(?=\[|Error|Warning|Notification)", errors)
    found = [l for b in dict.fromkeys(b.strip() for b in blocks)
             if re.search(r"\b(Error|Warning)\b", b) for l in b.splitlines()]
    keep = False
    for line in messages.splitlines():
        if line.startswith("|"):  # continuation of the runtime message above (an assert's text)
            if keep:
                found.append(line)
            continue
        keep = (("LOG_ASSERT" in line or "| error" in line or "| warning" in line
                 or "failed" in line) and not any(h in line for h in HARMLESS))
        if keep:
            found.append(line)
    if len(found) > 30:  # a solver retrying repeats a message with other numbers
        first = {}
        for line in found:
            first.setdefault(re.sub(r"\d[\d.e+-]*", "N", line), line)
        found = list(first.values())[:30] + [f"... ({len(found)} lines in all)"]
    return found


def run_model(paths, model, workdir, timeout):
    script = load(paths) + (
        f'checkModel({model});\n'  # simulate() alone skips the unit check
        'checkErrors := getErrorString();\n'
        f'r := simulate({model});\n'
        'simErrors := getErrorString();\n'
        # a record field works in an assignment, not inside another call's arguments
        'file := r.resultFile; options := r.simulationOptions; messages := r.messages;\n'
        'print("@@RESULT\\n" + file + "\\n@@OPTIONS\\n" + options + "\\n@@MESSAGES\\n" + messages'
        ' + "\\n@@ERRORS\\n" + checkErrors + simErrors + "\\n@@END\\n");\n')
    out = omc(script, workdir, timeout)
    if out is None:
        return False, "?", [f"no result after {timeout} s: chattering, very many events, or a stiff "
                           "model with an explicit solver (see SKILL.md, Messages)"]
    if "@@RESULT" not in out:
        return False, "?", out.strip().splitlines()[-20:]
    stop = re.search(r"stopTime = ([^,]+)", section(out, "OPTIONS"))
    errors = (section(out, "LOAD") + "\n" + section(out, "ERRORS")).strip()
    found = problems(errors, section(out, "MESSAGES"))
    if not section(out, "RESULT") and not found:
        found = section(out, "MESSAGES").splitlines() or ["simulation failed without a message"]
    return not found, stop.group(1) if stop else "?", found


def main(argv):
    timeout = 120
    if "--timeout" in argv:
        i = argv.index("--timeout")
        timeout = float(argv[i + 1])
        del argv[i:i + 2]
    files = [a for a in argv if a.endswith(".mo")]
    parts = [a for a in argv if not a.endswith(".mo")]
    if not files or any(p.startswith("-") for p in parts) or not all(map(os.path.exists, files)):
        print(__doc__.strip())
        return 2
    if not shutil.which("omc"):
        print("omc not found on PATH")
        return 1
    paths = list(dict.fromkeys(top_file(f) for f in files))
    path = " ".join(paths)
    build = tempfile.mkdtemp(prefix="run_tests_")
    try:
        load_errors, models = list_models(paths, build, timeout)
        if load_errors is None:
            print(f"listing the models of {path} took over {timeout} s: give a larger --timeout")
            return 1
        if re.search(r"\b(Error|Warning)\b", load_errors):
            print(f"FAIL loading {path}\n  " + load_errors.replace("\n", "\n  "))
            return 1
        tests = [m for m in models if TEST_PACKAGES & set(m.split(".")[:-1])
                 and (not parts or any(p in m for p in parts))]
        if not tests:
            print(f"no test models found in {path} (non-partial models in a package named "
                  + ", ".join(sorted(TEST_PACKAGES)) + ")")
            return 1
        print(f"{path}: {len(tests)} test models")
        dirs = {m: os.path.join(build, m) for m in tests}
        for d in dirs.values():
            os.makedirs(d)
        with concurrent.futures.ThreadPoolExecutor(os.cpu_count() or 2) as pool:
            runs = {m: pool.submit(run_model, paths, m, dirs[m], timeout) for m in tests}
            failed = 0
            for m in tests:
                ok, stop, found = runs[m].result()
                failed += not ok
                print(f"{'PASS' if ok else 'FAIL'} {m} (until t={stop})")
                for line in found:
                    print("    " + line)
        print(f"{len(tests) - failed} passed, {failed} failed")
        return 1 if failed else 0
    finally:
        shutil.rmtree(build, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
