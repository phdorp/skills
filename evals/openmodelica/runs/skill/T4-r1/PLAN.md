# PLAN: Vehicle library

## Structure
- Vehicle/package.mo, package.order
- Drag (partial, interface): input SI.Velocity v, output SI.Force F
- LinearDrag, QuadraticDrag: extend Drag
- Car: m = 1000 kg, v(start = 30, fixed = true), replaceable LinearDrag drag constrainedby Drag
- Examples: CoastLinear, CoastQuadratic (extend Car with redeclare), StopTime = 100
- Tests: asserts against the analytic solutions

## Steps
1. Package skeleton + Drag + LinearDrag + Car, checkModel/simulate Car.
2. QuadraticDrag.
3. Examples package with two coast models.
4. Tests package with analytic-solution asserts; run run_tests.py.

## Notes
- Sign convention: v > 0 forward; drag force F > 0 opposes motion: m*der(v) = -drag.F.
- Car sets drag.v = v in its equation section: a modifier drag(v = v) on the replaceable declaration is dropped by redeclare (seen: "Too few equations").
- Linear: v(t) = v0*exp(-k t/m); quadratic (c = 0.5 rho cd A = 0.36): 1/v = 1/v0 + c t/m.
- QuadraticDrag uses v*abs(v) so the force opposes motion for either sign (equals v^2 for v >= 0).
