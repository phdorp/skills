# Requirements

| Requirement | Check | Status |
|---|---|---|
| Car stops at 174.119 s (analytic) | Tests.CarStop: abs(tStop - 174.1192) < 0.01 | pass (174.1194) |
| Car coasting distance 1781.0 m | Tests.CarStop: abs(x - 1781.008) < 0.1 | pass |
| Truck stops at 226.177 s, 2194.2 m | Tests.TruckStop | pass (226.1771, 2194.217) |
| Truck record really used (m = 12000) | Tests.TruckStop | pass |
| tStop = 0 before stop | Tests.CarStop: assert at t = 100 | pass |
| No backward roll, v = 0 after stop | Tests.*: v >= -1e-6 throughout, v = 0 at t = 300 | pass |
| Examples simulate, StopTime 300 | run_tests.py: Examples.CarCoast, Examples.TruckCoast | pass |

Run: python3 SKILL_DIR/scripts/run_tests.py Fleet/package.mo
