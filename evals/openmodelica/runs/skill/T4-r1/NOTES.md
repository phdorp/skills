# NOTES

## Requirements (expected values from python3)
| Requirement | Check | Status |
|---|---|---|
| LinearDrag: F = k v, k = 10 | Tests.DragForces: F(v=30) = 300 N | PASS |
| QuadraticDrag: F = 0.5 rho cd A v^2 | Tests.DragForces: F(v=30) = 324 N, F(v=-30) = -324 N | PASS |
| Car coasting, linear: v(100) = 30 e^-1 = 11.0364 m/s | Tests.CoastLinearAnalytic (whole trajectory + final value) | PASS |
| Car coasting, quadratic: v(100) = 1/(1/30 + 0.036) = 14.4231 m/s, x(100) = 2034.355 m | Tests.CoastQuadraticAnalytic | PASS |
| Examples simulate, StopTime 100 | run_tests.py (Examples.CoastLinear, Examples.CoastQuadratic) | PASS |
| Car simulates standalone (default LinearDrag) | sim.mos: v(100) = 11.03640, x(100) = 1896.36 m (analytic 11.03638, 1896.36) | PASS |

Run: python3 SKILL_DIR/scripts/run_tests.py Vehicle/package.mo --timeout 3000
