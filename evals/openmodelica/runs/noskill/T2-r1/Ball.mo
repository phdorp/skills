model Ball "Ball dropped from 10 m, bouncing on the floor at h = 0"
  parameter Real h0(unit = "m") = 10 "Initial height";
  parameter Real g(unit = "m/s2") = 9.81 "Gravitational acceleration";
  parameter Real e = 0.8 "Coefficient of restitution";
  parameter Real vMin(unit = "m/s") = 1e-3
    "Rebound speed below which the ball is treated as resting (avoids Zeno chattering)";
  Real h(unit = "m", start = h0, fixed = true) "Height above the floor";
  Real v(unit = "m/s", start = 0, fixed = true) "Vertical velocity";
  Integer n(start = 0, fixed = true) "Number of bounces";
  discrete Real tFirst(unit = "s", start = -1, fixed = true)
    "Time of first impact (-1 until the first impact)";
  Boolean resting(start = false, fixed = true) "Ball has come to rest on the floor";
equation
  der(h) = if resting then 0 else v;
  der(v) = if resting then 0 else -g;
  when h <= 0 and v < 0 then
    n = pre(n) + 1;
    tFirst = if pre(n) == 0 then time else pre(tFirst);
    resting = e * abs(pre(v)) < vMin;
    reinit(h, 0);
    reinit(v, if e * abs(pre(v)) < vMin then 0 else -e * pre(v));
  end when;
  annotation(experiment(StartTime = 0, StopTime = 5, Tolerance = 1e-6, Interval = 0.001));
end Ball;
