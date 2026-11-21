# 2. Test each block through its ports against closed-form answers

## Status

proposed

## Context

R-3 requires every model to check and simulate without errors. QG-3 (faultlessness) is measured
by QS-3, which counts check errors only. `tests/check.mos` runs `checkModel(HeatingLib.System)`,
so the physics of `Room` and `Thermostat` is never verified: a wrong gain or time constant
passes QS-3.

ADR-0001 leaves test scripts to the building blocks. This ADR narrows that for block tests.

The architecture review (2026-11-21) measured the probes in a scratch copy: an unheated room
reaches 280.508 K at 3333 s against a predicted 280.51 K, and the thermostat at T = 290 K
demands 875 W against a predicted 875 W.

## Decision

We will test each block through its ports only. Each block gets a probe model in `tests/` that
drives its connectors and parameters and compares the result with a closed-form value:

- `Room`: with `Q_heat = 0`, `T(t) = T_amb + (T_start - T_amb) * exp(-t * G / C)`.
- `Thermostat`: with a measured `T` ramp from 250 K to 300 K, `Q` is 3000 W at 250 K (limit),
  875 W at 290 K, and 0 W at 300 K (floor).

`tests/check.mos` runs the probes and reports each comparison as PASS or FAIL.

## Consequences

- Probes read only ports and public parameters; no test reaches into a protected variable.
- QS-3 keeps its check count and gains a behavioural check; a failing probe is a failing build.
- Test code is reviewed against this decision; it is not a new block decision.
- Waiting for approval: this ADR. The probe models and the `check.mos` change wait until it is
  accepted, per the architect's rule that code and tests stay as they are until the ADR is approved.
- Candidate 2 (Thermostat gain through a port) needs its own ADR; this one does not decide it.
