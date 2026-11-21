model Pendulum "Hand-written pendulum ODE, right answer but no MultiBody"
  parameter Real g(unit = "m/s2") = 9.81;
  parameter Real L(unit = "m") = 1;
  Real phi(unit = "rad", start = 3.141592653589793/2, fixed = true);
  Real w(unit = "rad/s", start = 0, fixed = true);
equation
  der(phi) = w;
  der(w) = -g/L*sin(phi);
  annotation(experiment(StopTime = 3));
end Pendulum;
