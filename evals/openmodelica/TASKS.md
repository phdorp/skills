# OpenModelica benchmark tasks

Each task is given verbatim to an agent working in an empty directory. Names in `code` are
fixed so the grader can find them. The grader never shows its expected values to the agents.

## T1 tank: draining tank

Write `Tank.mo` with a model `Tank` of a cylindrical water tank draining through a hole at the
bottom (Torricelli's law, outflow q = a*sqrt(2*g*h)). Tank cross-section A = 2 m^2, hole area
a = 0.01 m^2, initial level h = 4 m, g = 9.81 m/s^2. Name the level `h` (in metres). Record the
time the tank runs empty in a variable `tEmpty` (seconds; it stays 0 until the tank is empty).
Simulate for 300 s with `experiment(StopTime = 300)`. The model must simulate without errors.

## T2 ball: bouncing ball

Write `Ball.mo` with a model `Ball` of a ball dropped from height 10 m (g = 9.81 m/s^2) that
bounces on the floor at h = 0 with coefficient of restitution 0.8. Name the height `h`, count
the bounces in an Integer `n`, and record the time of the first impact in `tFirst`. Simulate for
5 s with `experiment(StopTime = 5)`. The ball must never go noticeably below the floor.

## T3 msd: mass-spring-damper from the Standard Library

Write `MSD.mo` with a model `MSD` built from Modelica Standard Library components
(Modelica.Mechanics.Translational): a fixed point, a spring (c = 100 N/m), a damper
(d = 2 N.s/m) in parallel between the fixed point and a 1 kg mass. The mass starts at rest,
displaced 0.1 m from the spring's rest position. Expose that displacement as a Real `x`
(metres, 0 at the spring's rest position). Simulate for 3 s with `experiment(StopTime = 3)`.

## T4 vehicle: library with exchangeable drag models

Write a Modelica library `Vehicle` as a folder (one file per class, `package.mo` files):
- a partial model `Vehicle.Drag` (the interface): input velocity `v`, output force `F`;
- `Vehicle.LinearDrag` (F = k*v, k = 10 N.s/m) and `Vehicle.QuadraticDrag`
  (F = 0.5*rho*cd*A*v^2 with rho = 1.2 kg/m^3, cd = 0.3, A = 2 m^2), both extending `Drag`;
- `Vehicle.Car`: a 1000 kg car coasting (no drive force) from v = 30 m/s, velocity `v`, with an
  exchangeable drag component `drag`;
- example models `Vehicle.Examples.CoastLinear` and `Vehicle.Examples.CoastQuadratic` that use
  `Car` with each drag model (the car instance is named `car`), each with
  `experiment(StopTime = 100)`;
- a package `Vehicle.Tests` with at least one test model that checks a result with `assert`.
All models must simulate without errors.

## T5 pendulum: MultiBody pendulum

Write `Pendulum.mo` with a model `Pendulum` built from Modelica.Mechanics.MultiBody: a 1 kg
point mass at the end of a massless rod of length 1 m, hinged at a fixed pivot so it swings in a
vertical plane, with gravity g = 9.81 m/s^2 pointing down. It starts at rest with the rod
horizontal. Expose the angle `phi` (rad) between the rod and the downward vertical (phi = 0 when
hanging straight down). Simulate for 3 s with `experiment(StopTime = 3)`. The model must
simulate without errors or warnings.

## T6 robertson: stiff chemical kinetics with a chosen solver

Write `Robertson.mo` with a model `Robertson` of Robertson's chemical reaction system:
dy1/dt = -0.04*y1 + 1e4*y2*y3, dy2/dt = 0.04*y1 - 1e4*y2*y3 - 3e7*y2^2, dy3/dt = 3e7*y2^2,
with y1(0) = 1, y2(0) = 0, y3(0) = 0. Name the states `y1`, `y2`, `y3`. Simulate for 40 s with
`experiment(StopTime = 40, Tolerance = 1e-8)`. Make the model choose its own solver: an
implicit Radau IIA method of order 5, set in the model's annotation so that every simulation of
the model uses it without extra arguments.

## T7 thermostat: room heating with hysteresis

Write `Thermostat.mo` with a model `Thermostat` of a room heated by an on/off heater:
C*dT/dt = P*(heater on) - G*(T - Tamb) with C = 2e5 J/K, G = 100 W/K, P = 3000 W, ambient
temperature 0 degC. The room starts at 15 degC with the heater on. The heater switches off when
the room reaches 21 degC and on again when it falls to 19 degC. Name the room temperature `T`
(in kelvin), the heater state Boolean `heaterOn`, count the off-to-on switches in an Integer
`nOn` (the initial on state does not count), and record the time of the first switch-off in
`tOff1`. Simulate one day with `experiment(StopTime = 86400)`.

## T8 fleet: parameter records and coast-down to a stop

Write a Modelica library `Fleet` as a folder (one file per class, `package.mo` files):
- a record `Fleet.Params` with the vehicle mass `m` (kg), the drag area `cdA` (m^2) and the
  rolling resistance coefficient `cr`;
- records `Fleet.Car` (m = 1200, cdA = 0.6, cr = 0.01) and `Fleet.Truck` (m = 12000, cdA = 6,
  cr = 0.007), both extending `Params`;
- a model `Fleet.Coast`: a vehicle on a flat road coasting from v = 25 m/s with
  m*dv/dt = -(0.5*rho*cdA*v^2 + cr*m*g) (rho = 1.2 kg/m^3, g = 9.81 m/s^2) until it stops; it
  then stays at rest (v = 0, it must not roll backwards). Its parameter set is exchangeable;
  name it `p`, the velocity `v`, and record the time it stops in `tStop` (0 until then);
- example models `Fleet.Examples.CarCoast` and `Fleet.Examples.TruckCoast` that use `Coast` with
  each record (the instance is named `coast`), each with `experiment(StopTime = 300)`;
- a package `Fleet.Tests` with at least one test model that checks a result with `assert`.
All models must simulate without errors.
