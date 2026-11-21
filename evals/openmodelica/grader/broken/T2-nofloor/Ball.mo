model Ball "Bouncing ball"
  parameter Real g(unit = "m/s2") = 9.81;
  parameter Real e = 0.8 "Coefficient of restitution";
  parameter Real h0(unit = "m") = 10;
  Real h(unit = "m", start = h0, fixed = true);
  Real v(unit = "m/s", start = 0, fixed = true);
  Integer n = 0 "Number of bounces";
  Real tFirst = 0 "Time of first impact";
equation
  der(h) = v;
  der(v) = -g;
  annotation(experiment(StopTime = 5));
end Ball;
