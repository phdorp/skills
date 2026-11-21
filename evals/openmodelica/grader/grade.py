#!/usr/bin/env python3
"""Deterministic grader for the OpenModelica benchmark (see ../TASKS.md).

Usage:  python3 -I grade.py TASK RUN_DIR      (TASK in T1..T8)

Copies RUN_DIR into a fresh temp dir (RUN_DIR is never written), drives omc through generated
.mos scripts (getErrorString() after every call, simulate(..., outputFormat="csv") with the
model's own experiment annotation), and prints one JSON object with per-check results.

Standard library only (no numpy/pandas needed).

omc 1.27 quirks this relies on:
- `r := simulate(...)` does not bind a usable record (`r.resultFile` is "not found"), so every
  call's result is echoed with echo(true) between markers and parsed from stdout.
- extendsFrom(A, B) returns false even when A extends B, so inheritance is checked with a
  transitive walk over getInheritedClasses().
- simulate() applies the model's __OpenModelica_simulationFlags annotation only when the call has
  no simflags argument: any simflags (even "-alarm=120") replaces the annotation's flags, and the
  echoed simulationOptions then report "method = 'dassl'" whatever runs. T6 therefore simulates
  without simflags, reads the applied flags from the echoed "simflags = '...'", and re-runs with
  those flags plus -lv=LOG_SOLVER, whose log names the solver ("recognized solver: gbode") and
  the gbode method ("Chosen gbode method: radauIIA3"). An unknown solver (-s=radau5) logs
  "unrecognized option -s radau5" as runtime warnings and the simulation fails.
- gbode with omc's default numeric Jacobian logs the runtime warning "Numerical Jacobians without
  coloring are currently not supported by GBODE"; __OpenModelica_commandLineOptions =
  "--generateDynamicJacobian=symbolic" removes it. no_warnings counts it like any other warning.
"""
import bisect
import csv
import json
import math
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

OMC = os.environ.get("OMC", "omc")
OMC_TIMEOUT_S = 900          # whole omc invocation
SIM_ALARM_S = 120            # simulation executable aborts itself after this (-alarm)
MSL_VERSION = "4.1.0"
TASKS = tuple(f"T{i}" for i in range(1, 9))
IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")

# ---------------------------------------------------------------------------------------------
# Expected values, derived from the task statements in TASKS.md.
# ---------------------------------------------------------------------------------------------

# T1: Torricelli, A dh/dt = -a sqrt(2 g h)  =>  sqrt(h) falls linearly; empty at
#     t = (A/a) * sqrt(2 h0 / g)  (= 180.609 s).
T1_A, T1_a, T1_h0, T1_g, T1_STOP = 2.0, 0.01, 4.0, 9.81, 300.0
T1_T_EMPTY = (T1_A / T1_a) * math.sqrt(2 * T1_h0 / T1_g)

# T2: ball from h0, restitution e; impacts at t1 = sqrt(2 h0/g), t_{k+1} = t_k + 2 e v_k / g.
T2_h0, T2_g, T2_e, T2_STOP = 10.0, 9.81, 0.8, 5.0


def _t2_impacts(stop):
    t = math.sqrt(2 * T2_h0 / T2_g)
    v = T2_g * t
    impacts = []
    while t <= stop:
        impacts.append(t)
        v *= T2_e
        t += 2 * v / T2_g
    return impacts


T2_IMPACTS = _t2_impacts(T2_STOP)            # [1.4278, 3.7124]; the next one is at 5.540 s
T2_N = len(T2_IMPACTS)                        # 2
T2_T_FIRST = T2_IMPACTS[0]                    # 1.42784

# T3: m x'' + d x' + c x = 0, x(0) = x0, x'(0) = 0  (underdamped).
T3_m, T3_c, T3_d, T3_x0, T3_STOP = 1.0, 100.0, 2.0, 0.1, 3.0


def t3_x(t):
    wn = math.sqrt(T3_c / T3_m)
    zeta = T3_d / (2 * math.sqrt(T3_c * T3_m))
    wd = wn * math.sqrt(1 - zeta ** 2)
    return T3_x0 * math.exp(-zeta * wn * t) * (math.cos(wd * t) + zeta * wn / wd * math.sin(wd * t))


T3_POINTS = [(0.0, 1e-6), (0.5, 1e-4), (1.0, 1e-4)]   # (time, abs tolerance)

# T4: m v' = -F(v), v(0) = v0, simulated to T.
T4_m, T4_v0, T4_STOP = 1000.0, 30.0, 100.0
T4_k = 10.0
T4_rho, T4_cd, T4_Area = 1.2, 0.3, 2.0
T4_b = 0.5 * T4_rho * T4_cd * T4_Area
T4_V_LIN = T4_v0 * math.exp(-T4_k * T4_STOP / T4_m)             # 30 e^-1 = 11.0364
T4_V_QUAD = T4_v0 / (1 + T4_b * T4_v0 * T4_STOP / T4_m)          # 14.4231
T4_REL_TOL = 0.005

# T5: pendulum released at rest from theta0 = pi/2. Exact period T = 4 sqrt(L/g) K(sin(theta0/2)),
#     K the complete elliptic integral of the first kind, K(k) = pi / (2 AGM(1, sqrt(1 - k^2))).
#     phi first reaches 0 at T/4.
T5_L, T5_g, T5_THETA0, T5_STOP = 1.0, 9.81, math.pi / 2, 3.0
T5_g_MSL = 9.80665                    # Modelica.Mechanics.MultiBody.World default


def _agm(a, b):
    while abs(a - b) > 1e-15 * a:
        a, b = (a + b) / 2, math.sqrt(a * b)
    return a


def t5_quarter_period(g):
    k = math.sin(T5_THETA0 / 2)
    return math.sqrt(T5_L / g) * math.pi / (2 * _agm(1.0, math.sqrt(1 - k * k)))


T5_T_QUARTER = t5_quarter_period(T5_g)                  # 0.591960 s
T5_T_QUARTER_MSL_G = t5_quarter_period(T5_g_MSL)        # 0.592062 s, 1.01e-4 s later
# The tolerance must separate g = 9.81 from the MSL default g = 9.80665: put it at half the gap,
# so the wrong-g value misses by the same 5.1e-5 s margin the right one is allowed. The reference
# solution's crossing (cubic interpolation of the default 500-interval output) is 2.2e-6 s off.
T5_T_QUARTER_TOL = abs(T5_T_QUARTER_MSL_G - T5_T_QUARTER) / 2
T5_PHI_TOL = 1e-3

# T6: Robertson at t = 40, reference values from Hairer & Wanner, Solving ODEs II (1996), sec. IV.10.
#     Confirmed by a gbode/radauIIA3 run at Tolerance = 1e-10 in omc 1.27.2:
#     y1 = 0.7158270687263, y2 = 9.185534768e-6, y3 = 0.2841637457389 (relative deviation < 1e-9).
T6_STOP = 40.0
T6_REF = {"y1": 0.7158270687, "y2": 9.185534764e-6, "y3": 0.2841637457}
T6_REL_TOL = 1e-4
T6_SUM_TOL = 1e-6
T6_SOLVER, T6_GBM = "gbode", "radauIIA3"     # Radau IIA, 3 stages = order 5

# T7: C T' = P*on - G (T - Tamb). With the heater on, T relaxes to Tamb + P/G = 30 degC; with it
#     off, to Tamb = 0 degC; time constant tau = C/G. Times between thresholds follow from
#     T(t) - T_inf = (T(0) - T_inf) exp(-t/tau).
T7_C, T7_G, T7_P, T7_TAMB_C, T7_STOP = 2e5, 100.0, 3000.0, 0.0, 86400.0
T7_T0_C, T7_ON_C, T7_OFF_C = 15.0, 19.0, 21.0
T7_K = 273.15
T7_TAU = T7_C / T7_G                                                       # 2000 s


def _t7_relax(t_from, t_to, t_inf):
    return T7_TAU * math.log((t_from - t_inf) / (t_to - t_inf))


T7_HOT_C = T7_TAMB_C + T7_P / T7_G                                         # 30 degC
T7_T_OFF1 = _t7_relax(T7_T0_C, T7_OFF_C, T7_HOT_C)                         # 1021.65 s
T7_COOL = _t7_relax(T7_OFF_C, T7_ON_C, T7_TAMB_C)                          # tau ln(21/19)
T7_HEAT = _t7_relax(T7_ON_C, T7_OFF_C, T7_HOT_C)                           # tau ln(11/9)
T7_CYCLE = T7_COOL + T7_HEAT                                               # 601.51 s
T7_N_ON = math.floor((T7_STOP - T7_T_OFF1 - T7_COOL) / T7_CYCLE) + 1       # 142 (last at 86034 s)
T7_REL_TOL = 0.005
T7_BAND_TOL = 0.05

# T8: m v' = -(rho cdA v^2 / 2 + cr m g)  =>  v' = -(a v^2 + b), a = rho cdA / (2 m), b = cr g,
#     v reaches 0 at t = atan(v0 sqrt(a/b)) / sqrt(a b).
T8_rho, T8_g, T8_v0, T8_STOP = 1.2, 9.81, 25.0, 300.0
T8_VEHICLES = {"Car": (1200.0, 0.6, 0.01), "Truck": (12000.0, 6.0, 0.007)}  # m, cdA, cr


def t8_stop_time(m, cdA, cr):
    a, b = T8_rho * cdA / (2 * m), cr * T8_g
    return math.atan(T8_v0 * math.sqrt(a / b)) / math.sqrt(a * b)


T8_T_STOP = {k: t8_stop_time(*p) for k, p in T8_VEHICLES.items()}   # car 174.119 s, truck 226.177 s
T8_REL_TOL = 0.005
T8_V_TOL = 1e-3

# ---------------------------------------------------------------------------------------------
# omc driver
# ---------------------------------------------------------------------------------------------


def _mos_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _unescape(s):
    """omc echoes strings with only \\" and \\\\ escaped; newlines are literal."""
    return re.sub(r'\\(["\\])', r"\1", s)


def _parse_string_literal(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return _unescape(text[1:-1])
    return None


class Step:
    def __init__(self, label, expr, kind="query"):
        self.label, self.expr, self.kind = label, expr, kind
        self.value = None      # echoed result text (None: step never ran / omc died)
        self.errors = ""       # getErrorString() after the call


def run_omc(work, steps, log):
    """Run steps in one omc process inside `work`. Fills step.value / step.errors."""
    nonce = secrets.token_hex(4)
    lines = ["echo(false);"]
    for i, st in enumerate(steps):
        tag = f"@@{nonce}:{i}"
        lines += [f'print("{tag}:BEGIN\\n");', "echo(true);", st.expr + ";", "echo(false);",
                  f'print("\\n{tag}:ERRORS\\n");', "print(getErrorString());",
                  f'print("\\n{tag}:END\\n");']
    script = work.parent / f"grader_{nonce}.mos"
    script.write_text("\n".join(lines) + "\n")
    t0 = time.monotonic()
    proc = subprocess.Popen([OMC, str(script)], cwd=work, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, start_new_session=True)
    try:
        out, _ = proc.communicate(timeout=OMC_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        out, _ = proc.communicate()
        log["errors"].append(f"omc timed out after {OMC_TIMEOUT_S} s")
    log["omc_time_s"] += time.monotonic() - t0
    out = out.decode("utf-8", "replace")
    for i, st in enumerate(steps):
        tag = re.escape(f"@@{nonce}:{i}")
        m = re.search(tag + r":BEGIN\n(.*?)\n" + tag + r":ERRORS\n(.*?)\n" + tag + r":END\n",
                      out, re.S)
        if not m:
            st.errors = "step did not complete (omc aborted?)"
            continue
        val = m.group(1)
        val = val[len("true\n"):] if val.startswith("true\n") else ("" if val == "true" else val)
        st.value, st.errors = val.strip("\n"), m.group(2).strip("\n")
    if any(st.value is None for st in steps):
        tail = "\n".join(out.strip().splitlines()[-15:])
        log["errors"].append("omc did not finish the script; output tail:\n" + tail)
    return steps


# ---------------------------------------------------------------------------------------------
# result parsing
# ---------------------------------------------------------------------------------------------

WARN_LINE = re.compile(r"^(\[[^\]]*\]\s*)?Warning:")
ERR_LINE = re.compile(r"^(\[[^\]]*\]\s*)?Error:")
SIM_WARN = re.compile(r"^\S+\s*\|\s*warning\s*\|")
SIM_ERR = re.compile(r"^\S+\s*\|\s*error\s*\|")


def _messages(text, pattern):
    """Messages whose first line matches pattern, with continuation lines attached."""
    found, cur = [], None
    for line in text.splitlines():
        if pattern.match(line):
            cur = [line]
            found.append(cur)
        elif cur is not None and (line.startswith(" ") or line.startswith("|")):
            cur.append(line)
        else:
            cur = None
    return ["\n".join(m) for m in found]


def parse_bool(st):
    return st.value is not None and st.value.strip() == "true"


def parse_names(st):
    if st.value is None:
        return []
    v = st.value.strip()
    if not (v.startswith("{") and v.endswith("}")):
        return []
    return [n.strip() for n in v[1:-1].split(",") if n.strip()]


def parse_sim_options(st):
    """getSimulationOptions -> (startTime, stopTime, tolerance, numberOfIntervals, interval)."""
    if st.value is None:
        return None
    m = re.match(r"^\((.*)\)$", st.value.strip(), re.S)
    try:
        return tuple(float(x) for x in m.group(1).split(","))
    except (AttributeError, ValueError):
        return None


def read_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    header = [h.strip() for h in rows[0]]
    cols = {h: [] for h in header}
    for row in rows[1:]:
        if len(row) != len(header):
            continue
        for h, x in zip(header, row):
            try:
                cols[h].append(float(x))
            except ValueError:
                cols[h].append(float("nan"))
    return cols


class Sim:
    def __init__(self, model, st, work):
        self.model, self.ok, self.csv, self.messages, self.detail = model, False, None, "", ""
        v = st.value or ""
        rf = re.search(r'resultFile = "((?:[^"\\]|\\.)*)"', v)
        mm = re.search(r'messages = "((?:[^"\\]|\\.)*)"', v, re.S)
        self.result_file = _unescape(rf.group(1)) if rf else ""
        self.messages = _unescape(mm.group(1)) if mm else ""
        self.trans_errors = st.errors
        if not self.result_file:
            first = (self.messages.strip().splitlines() or [st.errors.strip() or "no result"])[0]
            self.detail = f"{model}: simulation failed ({first})"
            return
        try:
            self.csv = read_csv(self.result_file)
            assert self.csv.get("time"), "no time column"
            self.ok = True
            self.detail = f"{model}: ok, {len(self.csv['time'])} rows"
        except Exception as e:  # noqa: BLE001 - any unreadable CSV is a failed simulation
            self.detail = f"{model}: result file unreadable ({e})"

    def col(self, name):
        if not self.ok:
            return None
        return self.csv.get(name)

    def final(self, name):
        c = self.col(name)
        return c[-1] if c else None

    def at(self, name, t):
        """Linear interpolation; at duplicate (event) time stamps the last row wins."""
        c = self.col(name)
        if not c:
            return None
        ts = self.csv["time"]
        if t < ts[0] or t > ts[-1]:
            return None
        j = bisect.bisect_right(ts, t) - 1
        if ts[j] == t or j + 1 >= len(ts):
            return c[j]
        t0, t1 = ts[j], ts[j + 1]
        return c[j] + (c[j + 1] - c[j]) * (t - t0) / (t1 - t0)

    def first_zero_crossing(self, name):
        """Time where `name` first changes sign (or reaches 0), from a cubic through the four
        output points around the bracketing interval (linear when they are not distinct)."""
        c = self.col(name)
        if not c:
            return None
        ts = self.csv["time"]
        for k in range(1, len(c)):
            if c[k] == 0 or (c[k - 1] > 0) != (c[k] > 0) and c[k - 1] != 0:
                break
        else:
            return None
        if c[k] == 0:
            return ts[k]
        lo, hi = ts[k - 1], ts[k]
        nodes = list(range(max(0, k - 2), min(len(c), k + 2)))
        xs = [ts[i] for i in nodes]
        if len(set(xs)) == len(xs) == 4:
            def f(t):
                total = 0.0
                for i, xi in zip(nodes, xs):
                    w = 1.0
                    for xj in xs:
                        if xj != xi:
                            w *= (t - xj) / (xi - xj)
                    total += c[i] * w
                return total
        else:
            def f(t):
                return c[k - 1] + (c[k] - c[k - 1]) * (t - lo) / (hi - lo)
        flo = f(lo)
        for _ in range(100):
            mid = (lo + hi) / 2
            if (f(mid) > 0) == (flo > 0):
                lo, flo = mid, f(mid)
            else:
                hi = mid
        return (lo + hi) / 2

    def assertion_violated(self):
        return "assertion has been violated" in self.messages or any(
            "assert" in m.lower() for m in _messages(self.messages, SIM_ERR))


# ---------------------------------------------------------------------------------------------
# grading
# ---------------------------------------------------------------------------------------------


class Grade:
    def __init__(self, task, run_dir):
        self.task, self.run_dir = task, str(run_dir)
        self.checks, self.log = [], {"errors": [], "omc_time_s": 0.0}
        self.warnings = []
        self.work = None

    def check(self, name, ok, detail=""):
        self.checks.append({"name": name, "pass": bool(ok), "detail": detail})

    def clean(self, text):
        return text.replace(str(self.work) + "/", "").replace(str(self.work), ".")

    def collect(self, st, sim=None):
        """Record warnings/errors from a loadFile or simulate step."""
        for m in _messages(st.errors, WARN_LINE):
            self.warnings.append(self.clean(m))
        for m in _messages(st.errors, ERR_LINE):
            self.log["errors"].append(self.clean(m))
        if sim is not None:
            for m in _messages(sim.messages, SIM_WARN):
                self.warnings.append(f"{sim.model} (runtime): " + self.clean(m))
            if not sim.ok:
                self.log["errors"].append(self.clean(sim.detail))
                for m in _messages(sim.messages, SIM_ERR):
                    self.log["errors"].append(f"{sim.model} (runtime): " + self.clean(m))

    # -- common checks ---------------------------------------------------------------------

    def common_files(self, required):
        missing = [f for f in required if not (self.work / f).is_file()]
        self.check("files_exist", not missing,
                   "missing: " + ", ".join(missing) if missing else ", ".join(required))
        mos = sorted(self.work.rglob("*.mo"))
        bad = []
        for p in mos:
            data = p.read_bytes()
            for i, line in enumerate(data.split(b"\n"), 1):
                if any(b > 127 for b in line):
                    bad.append(f"{p.relative_to(self.work)}:{i}")
        self.check("ascii", mos and not bad,
                   "no .mo files" if not mos else
                   ("non-ASCII at " + ", ".join(bad[:10]) if bad else f"{len(mos)} .mo file(s)"))

    def preamble(self, load_file):
        return [Step("msl", f'loadModel(Modelica, {{"{MSL_VERSION}"}})'),
                Step("load", f"loadFile({_mos_str(load_file)})", "load")]

    def source(self, rel):
        p = self.work / rel
        return p.read_text("utf-8", "replace") if p.is_file() else ""

    def check_uses(self, rel, prefix):
        found = prefix in self.source(rel)
        self.check("uses_msl", found, f"{rel} mentions {prefix}" if found else f"no reference in {rel}")

    def library_facts(self, pkg, extra=()):
        """Load <pkg>/package.mo and return (names, facts) with per-class base classes, isModel,
        isPartial, `extra` predicates such as isRecord, and the source of <pkg>.Tests classes."""
        load_file = f"{pkg}/package.mo"
        p1 = self.preamble(load_file) + [Step("names", f"getClassNames({pkg}, recursive=true)")]
        run_omc(self.work, p1, self.log)
        self.check_load(p1)
        names = [n for n in parse_names(p1[2]) if IDENT.match(n)]
        preds = ("isModel", "isPartial") + tuple(extra)
        q = []
        for i, n in enumerate(names):
            q.append(Step(f"inh{i}", f"getInheritedClasses({n})"))
            q += [Step(f"{pr}{i}", f"{pr}({n})") for pr in preds]
            if n.startswith(f"{pkg}.Tests."):
                q.append(Step(f"list{i}", f"list({n})"))
        facts = {}
        if names:
            p2 = self.preamble(load_file) + q
            run_omc(self.work, p2, self.log)
            by = {st.label: st for st in p2}
            for i, n in enumerate(names):
                src = _parse_string_literal(by[f"list{i}"].value or "") if f"list{i}" in by else ""
                facts[n] = {"bases": parse_names(by[f"inh{i}"]), "src": src or ""}
                facts[n].update({pr: parse_bool(by[f"{pr}{i}"]) for pr in preds})
        return names, facts

    @staticmethod
    def extends(facts, c, base, seen=()):
        bases = facts.get(c, {}).get("bases", [])
        return base in bases or any(Grade.extends(facts, b, base, seen + (c,))
                                    for b in bases if b not in seen)

    def test_models(self, pkg, names, facts):
        tests = [n for n in names if n.startswith(f"{pkg}.Tests.")
                 and facts[n]["isModel"] and not facts[n]["isPartial"]]
        with_assert = [n for n in tests if re.search(r"\bassert\s*\(", facts[n]["src"])]
        self.check("tests_have_assert", bool(with_assert),
                   f"test models with assert: {with_assert}" if with_assert else
                   f"no non-partial model in {pkg}.Tests contains assert (models: {tests})")
        return tests

    def check_tests_pass(self, tests, sims):
        bad = [t for t in tests if not sims[t].ok or sims[t].assertion_violated()]
        self.check("tests_pass", bool(tests) and not bad,
                   "no test models" if not tests else
                   (f"failing: {bad}; " + "; ".join(self.clean(sims[t].detail) for t in bad)
                    if bad else f"{len(tests)} test model(s) pass"))

    def check_load(self, steps):
        msl, load = steps[0], steps[1]
        if not parse_bool(msl):
            self.log["errors"].append("grader: loadModel(Modelica 4.1.0) failed: " + msl.errors)
        errs = _messages(load.errors, ERR_LINE)
        ok = parse_bool(load) and not errs
        self.check("loads", ok, "ok" if ok else self.clean(
            "; ".join(errs) or load.errors or f"loadFile returned {load.value!r}"))
        self.collect(load)

    def sim_steps(self, models, simflags=f"-alarm={SIM_ALARM_S}"):
        """simflags=None simulates exactly as a plain simulate(): passing any simflags replaces
        the model's __OpenModelica_simulationFlags annotation instead of adding to it."""
        flags = "" if simflags is None else f", simflags={_mos_str(simflags)}"
        steps = []
        for i, m in enumerate(models):
            steps.append(Step(f"opts{i}", f"getSimulationOptions({m})"))
            steps.append(Step(f"sim{i}", f'simulate({m}, outputFormat="csv"{flags})', "simulate"))
        return steps

    def run_sims(self, models, steps, offset):
        sims = {}
        for i, m in enumerate(models):
            st = steps[offset + 2 * i + 1]
            sims[m] = Sim(m, st, self.work)
            self.collect(st, sims[m])
        return sims

    def check_sims(self, sims):
        ok = bool(sims) and all(s.ok for s in sims.values())
        self.check("simulates", ok, "; ".join(s.detail for s in sims.values()) or "nothing simulated")

    def check_stop(self, models, steps, offset, sims, stop):
        details, ok = [], True
        for i, m in enumerate(models):
            opts = parse_sim_options(steps[offset + 2 * i])
            ann = opts[1] if opts else None
            good = ann is not None and abs(ann - stop) <= 1e-9 * max(1.0, stop)
            sim = sims[m]
            if sim.ok:
                last = sim.csv["time"][-1]
                good = good and abs(last - stop) <= 1e-6 * max(1.0, stop)
                details.append(f"{m}: annotation StopTime={ann}, result ends at {last:g}")
            else:
                details.append(f"{m}: annotation StopTime={ann}")
            ok = ok and good
        self.check("stop_time", ok, f"expected {stop:g}; " + "; ".join(details))

    def value_check(self, name, value, lo, hi, what):
        if value is None or math.isnan(value):
            self.check(name, False, f"{what}: not available")
        else:
            self.check(name, lo <= value <= hi, f"{what} = {value:.6g}, expected [{lo:.6g}, {hi:.6g}]")

    # -- tasks -----------------------------------------------------------------------------

    def single_model_task(self, filename, model, stop):
        self.common_files([filename])
        steps = self.preamble(filename) + self.sim_steps([model])
        run_omc(self.work, steps, self.log)
        self.check_load(steps)
        sims = self.run_sims([model], steps, 2)
        self.check_sims(sims)
        self.check_stop([model], steps, 2, sims, stop)
        return sims[model]

    def t1(self):
        s = self.single_model_task("Tank.mo", "Tank", T1_STOP)
        self.value_check("h_final_zero", s.final("h"), -1e-3, 1e-3, "final h")
        h = s.col("h")
        self.value_check("h_nonnegative", min(h) if h else None, -1e-3, math.inf, "min h")
        tol = 0.01 * T1_T_EMPTY
        self.value_check("t_empty", s.final("tEmpty"), T1_T_EMPTY - tol, T1_T_EMPTY + tol,
                         "final tEmpty")

    def t2(self):
        s = self.single_model_task("Ball.mo", "Ball", T2_STOP)
        self.value_check("n_bounces", s.final("n"), T2_N, T2_N, "final n")
        self.value_check("t_first", s.final("tFirst"), T2_T_FIRST - 1e-3, T2_T_FIRST + 1e-3,
                         "final tFirst")
        h = s.col("h")
        self.value_check("h_above_floor", min(h) if h else None, -1e-3, math.inf, "min h")

    def t3(self):
        s = self.single_model_task("MSD.mo", "MSD", T3_STOP)
        self.check_uses("MSD.mo", "Modelica.Mechanics.Translational")
        for t, tol in T3_POINTS:
            ref = t3_x(t)
            self.value_check(f"x_at_{t:g}".replace(".", "_"), s.at("x", t), ref - tol, ref + tol,
                             f"x({t:g})")

    def t4(self):
        lin, quad = "Vehicle.Examples.CoastLinear", "Vehicle.Examples.CoastQuadratic"
        self.common_files(["Vehicle/package.mo"])
        names, facts = self.library_facts("Vehicle")
        drag = facts.get("Vehicle.Drag")
        self.check("drag_partial", bool(drag and drag["isPartial"]),
                   "Vehicle.Drag not found" if drag is None else f"isPartial = {drag['isPartial']}")
        sub = {c: self.extends(facts, c, "Vehicle.Drag")
               for c in ("Vehicle.LinearDrag", "Vehicle.QuadraticDrag")}
        self.check("drag_subclasses", all(sub.values()),
                   "; ".join(f"{c}: {'extends' if v else 'does not extend'} Vehicle.Drag"
                             + ("" if c in facts else " (class not found)") for c, v in sub.items()))
        tests = self.test_models("Vehicle", names, facts)
        models = [lin, quad] + tests
        p3 = self.preamble("Vehicle/package.mo") + self.sim_steps(models)
        run_omc(self.work, p3, self.log)
        sims = self.run_sims(models, p3, 2)
        self.check_sims(sims)
        self.check_stop([lin, quad], p3, 2, sims, T4_STOP)
        for name, model, ref in (("coast_linear", lin, T4_V_LIN), ("coast_quadratic", quad, T4_V_QUAD)):
            tol = T4_REL_TOL * ref
            self.value_check(name, sims[model].final("car.v"), ref - tol, ref + tol,
                             f"{model} final car.v")
        self.check_tests_pass(tests, sims)

    def t5(self):
        s = self.single_model_task("Pendulum.mo", "Pendulum", T5_STOP)
        self.check_uses("Pendulum.mo", "Modelica.Mechanics.MultiBody")
        phi = s.col("phi")
        self.value_check("phi_initial", abs(phi[0]) if phi else None,
                         T5_THETA0 - T5_PHI_TOL, T5_THETA0 + T5_PHI_TOL, "|phi(0)|")
        tq = T5_T_QUARTER
        self.value_check("t_quarter", s.first_zero_crossing("phi"),
                         tq - T5_T_QUARTER_TOL, tq + T5_T_QUARTER_TOL,
                         f"first phi = 0 (g = {T5_g}; g = {T5_g_MSL} gives {T5_T_QUARTER_MSL_G:.6f})")
        self.value_check("phi_bounded", max(abs(x) for x in phi) if phi else None,
                         -math.inf, T5_THETA0 + T5_PHI_TOL, "max |phi|")

    def t6(self):
        model = "Robertson"
        self.common_files(["Robertson.mo"])
        # phase 1: a plain simulate(), so the model's own __OpenModelica_simulationFlags apply.
        # No -alarm here (it would replace those flags); OMC_TIMEOUT_S still bounds the run.
        p1 = self.preamble("Robertson.mo") + self.sim_steps([model], simflags=None)
        run_omc(self.work, p1, self.log)
        self.check_load(p1)
        sims = self.run_sims([model], p1, 2)
        s = sims[model]
        self.check_sims(sims)
        self.check_stop([model], p1, 2, sims, T6_STOP)
        for y, ref in T6_REF.items():
            tol = T6_REL_TOL * ref
            self.value_check(f"{y}_at_40", s.at(y, T6_STOP), ref - tol, ref + tol, f"{y}(40)")
        ys = [s.final(y) for y in T6_REF]
        total = None if None in ys else sum(ys)
        self.value_check("mass_conserved", total, 1 - T6_SUM_TOL, 1 + T6_SUM_TOL, "final y1+y2+y3")
        # phase 2: the flags phase 1 applied, plus -lv=LOG_SOLVER, which names the solver that runs.
        # simflags is the last field of simulationOptions; omc echoes its quotes as \\'
        m = re.search(r"simflags = '(.*?)'\",?\s*$", p1[3].value or "", re.M)
        applied = re.sub(r"\\+'", "'", m.group(1)) if m else None
        solver = method = None
        if applied is not None:
            p2 = self.preamble("Robertson.mo") + self.sim_steps(
                [model], simflags=f"{applied} -lv=LOG_SOLVER -alarm={SIM_ALARM_S}".strip())
            run_omc(self.work, p2, self.log)
            log = Sim(model, p2[3], self.work).messages
            sm = re.search(r"recognized solver: (\S+)", log)
            gm = re.search(r"Chosen gbode method: (\S+)", log)
            solver, method = sm and sm.group(1), gm and gm.group(1)
        ran = f"{solver}" + (f"/{method}" if method else "") if solver else "no solver recognized"
        self.check("solver", (solver, method) == (T6_SOLVER, T6_GBM),
                   f"plain simulate applied simflags {applied!r}; ran {ran}; "
                   f"expected {T6_SOLVER}/{T6_GBM}")

    def t7(self):
        s = self.single_model_task("Thermostat.mo", "Thermostat", T7_STOP)
        self.check("heater_on", s.col("heaterOn") is not None,
                   "heaterOn in result" if s.col("heaterOn") is not None else
                   ("no heaterOn column" if s.ok else "no result"))
        tol = T7_REL_TOL * T7_T_OFF1
        self.value_check("t_off1", s.final("tOff1"), T7_T_OFF1 - tol, T7_T_OFF1 + tol, "final tOff1")
        self.value_check("n_on", s.final("nOn"), T7_N_ON, T7_N_ON, "final nOn")
        T, band = s.col("T"), None
        if T:
            after = [x for t, x in zip(s.csv["time"], T) if t >= T7_T_OFF1]
            band = (min(after), max(after)) if after else None
        lo, hi = T7_K + T7_ON_C - T7_BAND_TOL, T7_K + T7_OFF_C + T7_BAND_TOL
        self.check("t_band", band is not None and lo <= band[0] and band[1] <= hi,
                   f"T after {T7_T_OFF1:.6g} s in [{band[0]:.6g}, {band[1]:.6g}] K, expected "
                   f"[{lo:.6g}, {hi:.6g}]" if band else "T: not available")

    def t8(self):
        examples = {k: f"Fleet.Examples.{k}Coast" for k in T8_VEHICLES}
        self.common_files(["Fleet/package.mo"])
        names, facts = self.library_facts("Fleet", extra=("isRecord",))
        params = facts.get("Fleet.Params")
        self.check("params_record", bool(params and params["isRecord"]),
                   "Fleet.Params not found" if params is None else f"isRecord = {params['isRecord']}")
        sub = {f"Fleet.{k}": self.extends(facts, f"Fleet.{k}", "Fleet.Params") for k in T8_VEHICLES}
        self.check("records_extend", all(sub.values()),
                   "; ".join(f"{c}: {'extends' if v else 'does not extend'} Fleet.Params"
                             + ("" if c in facts else " (class not found)") for c, v in sub.items()))
        tests = self.test_models("Fleet", names, facts)
        models = list(examples.values()) + tests
        p3 = self.preamble("Fleet/package.mo") + self.sim_steps(models)
        run_omc(self.work, p3, self.log)
        sims = self.run_sims(models, p3, 2)
        self.check_sims(sims)
        self.check_stop(list(examples.values()), p3, 2, sims, T8_STOP)
        for k, model in examples.items():
            ref = T8_T_STOP[k]
            tol = T8_REL_TOL * ref
            self.value_check(f"t_stop_{k.lower()}", sims[model].final("coast.tStop"),
                             ref - tol, ref + tol, f"{model} final coast.tStop")
        finals = {m: sims[m].final("coast.v") for m in examples.values()}
        mins = {m: (min(sims[m].col("coast.v")) if sims[m].col("coast.v") else None)
                for m in examples.values()}
        for name, vals, what, ok in (
                ("v_stopped", finals, "final coast.v", lambda v: abs(v) <= T8_V_TOL),
                ("no_rollback", mins, "min coast.v", lambda v: v >= -T8_V_TOL)):
            good = all(v is not None and ok(v) for v in vals.values())
            self.check(name, good, "; ".join(
                f"{m} {what} = " + ("n/a" if v is None else f"{v:.6g}") for m, v in vals.items())
                + f"; tolerance {T8_V_TOL:g}")
        self.check_tests_pass(tests, sims)

    def run(self):
        t0 = time.monotonic()
        tmp = Path(tempfile.mkdtemp(prefix=f"grade-{self.task}-"))
        try:
            self.work = tmp / "work"
            src = Path(self.run_dir)
            if src.is_dir():
                shutil.copytree(src, self.work, symlinks=True)
            else:
                self.work.mkdir()
                self.log["errors"].append(f"run dir {src} does not exist")
            for stale in self.work.glob("*_res.*"):   # never read the agent's own results
                if stale.is_file():
                    stale.unlink()
            getattr(self, self.task.lower())()
        except Exception as e:  # noqa: BLE001 - a grader bug must still yield a result
            self.log["errors"].append(f"grader exception: {type(e).__name__}: {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        loaded = any(c["name"] == "loads" and c["pass"] for c in self.checks)
        self.check("no_warnings", loaded and not self.warnings,
                   f"{len(self.warnings)} warning(s)" if self.warnings else
                   ("none" if loaded else "not credited: the model did not load"))
        passed = sum(c["pass"] for c in self.checks)
        return {
            "task": self.task, "run_dir": self.run_dir, "checks": self.checks,
            "passed": passed, "total": len(self.checks),
            "score": round(passed / len(self.checks), 4) if self.checks else 0.0,
            "warnings": {"count": len(self.warnings), "text": self.warnings},
            "errors": self.log["errors"],
            "wall_time_s": round(time.monotonic() - t0, 2),
            "omc_time_s": round(self.log["omc_time_s"], 2),
        }


def grade(task, run_dir):
    if task not in TASKS:
        raise ValueError(f"unknown task {task!r}")
    return Grade(task, run_dir).run()


def main(argv):
    if len(argv) != 3 or argv[1] not in TASKS:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(grade(argv[1], argv[2]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
