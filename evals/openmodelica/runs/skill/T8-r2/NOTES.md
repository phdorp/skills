# Notes

## Requirements (expected values computed with python3)
| Requirement | Expected | Check | Status |
|---|---|---|---|
| Car stops at analytic time | tStop = 174.1192 s | Tests.CarStop | PASS |
| Car distance | 1781.008 m | Tests.CarStop | PASS |
| Car v(30 s) | 17.95485 m/s | Tests.CarStop | PASS |
| Truck stops at analytic time | tStop = 226.1768 s | Tests.TruckStop | PASS |
| Truck distance | 2194.215 m | Tests.TruckStop | PASS |
| Truck v(30 s) | 18.69460 m/s | Tests.TruckStop | PASS |
| No rolling back: v >= 0 always, v = 0 after stop | | Tests.CarStop, Tests.TruckStop | PASS |
| tStop = 0 before the stop | | Tests.CarStop, Tests.TruckStop | PASS |
| Examples simulate (StopTime 300) | | run_tests.py | PASS |
