# Notes

## Requirements
| Requirement | Check | Status |
|---|---|---|
| LinearDrag F = k*v | Tests.CoastAnalytic: F = 10 v at all times | PASS |
| QuadraticDrag F = 0.5 rho cd A v^2 | Tests.CoastAnalytic: F = 0.36 v^2 at all times, 324 N at t = 0 | PASS |
| Car coasts from 30 m/s, linear drag: v(100) = 11.0364 | Tests.CoastAnalytic (whole trajectory and at t = 100) | PASS |
| Car coasts, quadratic drag: v(100) = 14.4231 | Tests.CoastAnalytic (whole trajectory and at t = 100) | PASS |
| Examples simulate | run_tests.py on Examples | PASS |
