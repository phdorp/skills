model Ball "Bouncing ball"
  parameter Real g(unit = "m/s2") = 9.81;
  parameter Real e = 0.8 "Coefficient of restitution";
  parameter Real h0(unit = "m") = 10;
  Real h(unit = "m", start = h0, fixed = true);
  Real v(unit = "m/s", start = 0, fixed = true);
  Integer n(start = 0, fixed = true) "Number of bounces";
  discrete Real tFirst(unit = "s", start = 0, fixed = true) "Time of first impact";
equation
  der(h) = v;
  der(v) = -g;
  when h <= 0 then
    reinit(v, -e*pre(v));
    n = pre(n) + 1;
    tFirst = if pre(n) == 0 then time else pre(tFirst);
  end when;
  annotation(experiment(StopTime = 5));
end Ball;
