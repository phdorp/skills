# Bouncing ball

## Requirements (expected values computed with python3)
- h(0) = 10 m, free fall with g = 9.81 m/s^2.
- First impact tFirst = sqrt(2*10/9.81) = 1.42784 s, impact speed 14.0071 m/s.
- Restitution 0.8: apex after the first bounce 6.4 m; second impact at 3.71239 s.
- n(5 s) = 2, h(5) = 3.41068 m, v(5) = -3.66686 m/s.
- h never noticeably below 0 (check: min h > -1e-6, plus an assert in the model).
- Zeno point at 12.85 s: the ball must come to rest there, not sink (check: run to 20 s).

## Plan
1. Model Ball: der(h) = v, der(v) = -g while flying; when h <= 0 reinit v = -e*pre(v), count n,
   record tFirst.
2. Resting mode: when the rebound speed falls below vMin the ball stays at h = 0.
3. sim.mos: checkModel + simulate (csv), check numbers above with python3.

## Status (sim.mos, sim20.mos, check.py on the current Ball.mo)
- checkModel: 5 equations, 5 variables; simulate: no warnings.  PASS
- tFirst = 1.427843 (expected 1.427843).  PASS
- apex 6.39999993 (expected 6.4); impacts at 1.42784, 3.71239.  PASS
- n(5) = 2, h(5) = 3.410685, v(5) = -3.666863 (expected 3.41068, -3.66686).  PASS
- min h = -1.0e-10 (5 s and 20 s runs); assert h > -1e-4 never violated.  PASS
- 20 s run: ball at rest at 12.85 s (Zeno 12.8506), h = 0, v = 0, n = 43.  PASS
