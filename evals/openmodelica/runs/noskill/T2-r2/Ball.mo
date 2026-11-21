model Ball "Ball dropped from 10 m bouncing on a floor at h = 0"
  parameter Real h0(unit = "m") = 10 "Initial height";
  parameter Real g(unit = "m/s2") = 9.81 "Gravitational acceleration";
  parameter Real e = 0.8 "Coefficient of restitution";
  parameter Real vMin(unit = "m/s") = 1e-3
    "Rebound speed below which the ball is considered at rest on the floor";
  Real h(unit = "m", start = h0, fixed = true) "Height above the floor";
  Real v(unit = "m/s", start = 0, fixed = true) "Vertical velocity";
  Integer n(start = 0, fixed = true) "Number of bounces";
  discrete Real tFirst(unit = "s", start = -1, fixed = true)
    "Time of the first impact (-1 until it happens)";
  Boolean flying(start = true, fixed = true) "False once the ball rests on the floor";
equation
  der(h) = v;
  der(v) = if flying then -g else 0;
  when h <= 0 and v <= 0 then
    n = pre(n) + 1;
    tFirst = if pre(n) == 0 then time else pre(tFirst);
    flying = e*abs(pre(v)) > vMin;
    reinit(v, if flying then -e*pre(v) else 0);
    reinit(h, 0);
  end when;
  annotation(experiment(StartTime = 0, StopTime = 5, Tolerance = 1e-6, Interval = 0.001));
end Ball;
