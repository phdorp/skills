# Tank plan

## Requirements (checks)
- R1 simulates 300 s without errors/warnings: run_tests.py / sim.mos.
- R2 tEmpty = 2*sqrt(h0)*A/(a*sqrt(2g)) = 180.609 s (python3); assert in Tests.TankEmpties, tol 0.5 s.
- R3 h(t) = (sqrt(h0) - k*t/2)^2, k = a/A*sqrt(2g): h(50) = 2.0918, h(100) = 0.7968; assert.
- R4 tEmpty = 0 before empty; h stays >= 0 and = 0 after tEmpty; assert.

## Structure
- Tank.mo: model Tank. TankTests.mo: package Tests with TankEmpties (extends Tank, asserts).

## Steps
1. Tank with der(h) = -q/A, q = a*sqrt(2*g*max(h,0)); simulate.
2. Event when h <= 0: empty = true, tEmpty = time, reinit(h, 0); outflow off when empty.
3. Test model with asserts; run_tests.py.

## Notes
- Guard sqrt with max(h, 0) (solver trial steps past 0).
