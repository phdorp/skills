# MSD plan

Structure: one file `MSD.mo`, one model `MSD` from Modelica.Mechanics.Translational.Components:
Fixed (s0 = 0) -> Spring (c = 100, s_rel0 = 0) and Damper (d = 2) in parallel -> Mass (m = 1, L = 0).

Steps:
1. Look up Fixed, Spring, Damper, Mass in MSL 4.1.0 (done: Mass has L = 0 default, s is its centre).
2. Write MSD.mo with x = mass.s, initial s = 0.1 fixed, v = 0 fixed, experiment(StopTime = 3).
3. checkModel + simulate via sim.mos (no errors or warnings).
4. Compare x(t) with the analytic solution (verify.py).

## Notes
- Sign convention: x = mass.s, positive away from the fixed point; spring force on mass = -c*x.
- m x'' + d x' + c x = 0, wn = 10 rad/s, zeta = 0.1 (underdamped), sigma = d/(2m) = 1 1/s,
  wd = sqrt(wn^2 - sigma^2).
- x(t) = x0 e^(-sigma t) (cos(wd t) + sigma/wd sin(wd t)), x0 = 0.1 m.

## Requirements
- R1 x(0) = 0.1 m, v(0) = 0: check x[0], mass.v[0] in result.
- R2 dynamics match analytic: max |x - x_analytic| < 1e-4 m over 0..3 s.
- R3 decays: |x(3)| < 0.1*e^-3*1.01.
- R4 checkModel/simulate clean (no warnings).
