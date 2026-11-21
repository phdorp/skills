# Plan: Vehicle library

## Structure
- Vehicle/Drag.mo: partial model, input v (SI.Velocity), output F (SI.Force). The interface.
- Vehicle/LinearDrag.mo, QuadraticDrag.mo: extend Drag.
- Vehicle/Car.mo: m = 1000 kg, v(start = 30, fixed = true), m*der(v) = -drag.F,
  `replaceable LinearDrag drag constrainedby Drag`, drag.v = v.
- Vehicle/Examples: CoastLinear, CoastQuadratic (car with redeclare), StopTime = 100.
- Vehicle/Tests: asserts against analytic solutions.

## Steps
1. package.mo files + Drag + LinearDrag + Car; simulate Car.
2. QuadraticDrag.
3. Examples.
4. Tests with asserts; run_tests.py.

## Notes
- Sign: F is the drag force magnitude opposing motion (v > 0), so m*der(v) = -F.
- Linear: v(t) = 30*exp(-k t/m); v(100) = 30/e = 11.0364 m/s.
- Quadratic: c = 0.5*rho*cd*A = 0.36 kg/m; v(t) = v0/(1 + c v0 t/m); v(100) = 14.4231 m/s.
  (checked by Euler integration in python3: 11.0363, 14.4230)
- QuadraticDrag uses v*abs(v) so the force keeps opposing motion for v < 0 (equals v^2 for v >= 0).
