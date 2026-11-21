# Pendulum plan

Structure: one model `Pendulum` in Pendulum.mo, MultiBody parts:
world (fixed pivot = world.frame_b) -> Revolute rev (axis z) -> FixedTranslation rod
(r = {0,-1,0}, massless) -> PointMass mass (m = 1).

Steps
1. Write Pendulum.mo with the chain above, experiment(StopTime = 3).
2. checkModel + simulate via sim.mos, zero errors/warnings.
3. Check results against the requirements below with python (csv).

## Requirements / checks
- R1 simulates for 3 s without errors or warnings: omc output of sim.mos.
- R2 starts at rest, rod horizontal: phi(0) = pi/2, w(0) = 0.
- R3 phi = 0 when hanging down, angle from downward vertical: phi stays in [-pi/2, pi/2],
  reaches about -pi/2 at T/2.
- R4 physics: period T = 4*sqrt(L/g)*K(sin(pi/4)) = 2.36784 s (python, AGM); phi crosses 0
  first at T/4 = 0.59196 s; max |w| = sqrt(2 g / L) = 4.42945 rad/s;
  energy 0.5*m*L^2*w^2 - m*g*L*cos(phi) stays 0.

## Notes
- World: g along n = {0,-1,0} (minus y is down); set g = 9.81 explicitly (default is g_n).
- Revolute n = {0,0,1}: motion in the x-y plane. rod r = {0,-1,0} means rev.phi = 0 is
  hanging down; rev.phi = +pi/2 rotates the rod to +x (horizontal). So phi = rev.phi.
- Revolute phi/w have start 0 and StateSelect.prefer; set start + fixed = true.

## Results (current files, sim.mos run from build/)
- R1 PASS: checkModel 951 eq / 951 var, simulate "finished successfully", no warnings.
- R2 PASS: phi(0) = 1.5707963, w(0) = 0; mass starts at x = 1, y = 0.
- R3 PASS: phi in [-1.5707753, 1.5707963]; mass reaches y = -0.99999987 at the bottom.
- R4 PASS: first phi = 0 at 0.591963 s (expected 0.591960); period from zero crossings
  2.367840 s (expected 2.367842); max |w| 4.429445 (expected 4.429447);
  energy drift within [-6.6e-5, 2.3e-5] J.
