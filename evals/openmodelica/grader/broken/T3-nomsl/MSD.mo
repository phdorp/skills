model MSD "Hand-written equations instead of library components"
  parameter Real m = 1, c = 100, d = 2;
  Real x(start = 0.1, fixed = true);
  Real v(start = 0, fixed = true);
equation
  der(x) = v;
  m*der(v) = -c*x - d*v;
  annotation(experiment(StopTime = 3, Interval = 0.001));
end MSD;
