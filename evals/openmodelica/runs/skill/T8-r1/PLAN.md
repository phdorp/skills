# Plan: Fleet

Structure: Fleet/{Params, Car, Truck, Coast}, Fleet.Examples.{CarCoast, TruckCoast}, Fleet.Tests.
Exchangeable part: the parameter record `p` in Coast (`replaceable parameter Params p`),
swapped with `redeclare parameter Car p`.

Steps
1. package.mo files and records Params, Car, Truck.
2. Coast: der(v) with drag + rolling; when v <= 0: reinit(v, 0), stopped = true, tStop = time.
3. Examples CarCoast, TruckCoast (StopTime 300), run_tests.
4. Tests: stop time and distance vs analytic, v stays 0 after stop.

## Notes
- m dv/dt = -(k v^2 + c), k = 0.5 rho cdA, c = cr m g. With a = k/m, b = c/m:
  tStop = atan(v0 sqrt(a/b)) / sqrt(a b), xStop = ln(1 + a v0^2 / b) / (2 a).
- Car: a = 3e-4, b = 0.0981 -> tStop = 174.1192 s, xStop = 1781.008 m.
- Truck: a = 3e-4, b = 0.06867 -> tStop = 226.1768 s, xStop = 2194.215 m.
- At rest: stopped = true sets der(v) = 0, so v stays exactly 0 (no backwards roll).
