# Plan: Fleet library

Structure: Fleet/ folder library, one file per class.
- Fleet.Params (record, interface: m, cdA, cr), Fleet.Car, Fleet.Truck (extend Params with values).
- Fleet.Coast: `replaceable parameter Fleet.Car p constrainedby Fleet.Params` (exchangeable set).
- Fleet.Examples.CarCoast / TruckCoast: `Fleet.Coast coast(redeclare parameter Fleet.X p)`.
- Fleet.Tests: asserts against the analytic solution.

Steps
1. package.mo files + Params, Car, Truck.
2. Coast (minimal), simulate with the default Car.
3. Examples, simulate.
4. Tests with asserts; run_tests.py on everything.

## Notes
- Equation: m dv/dt = -(0.5 rho cdA v^2 + cr m g), v(0) = 25, rho = 1.2, g = 9.81.
- Stop: `when v <= 0`: stopped = true, tStop = time, reinit(v, 0); afterwards der(v) = 0
  (if-expression on the Boolean `stopped`), so v stays 0 and never goes negative.
- Analytic (k = 0.5 rho cdA / m, c = cr g): tStop = atan(v0 sqrt(k/c)) / sqrt(k c),
  distance = ln((k v0^2 + c)/c) / (2k), v(t) = sqrt(c/k) tan(atan(v0 sqrt(k/c)) - sqrt(k c) t).
