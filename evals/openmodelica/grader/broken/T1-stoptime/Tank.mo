model Tank "Cylindrical tank draining through a bottom hole (Torricelli's law)"
  parameter Real A(unit = "m2") = 2 "Tank cross-section";
  parameter Real a(unit = "m2") = 0.01 "Hole area";
  parameter Real g(unit = "m/s2") = 9.81 "Gravity";
  parameter Real h0(unit = "m") = 4 "Initial level";
  parameter Real hEps(unit = "m") = 1e-7 "Level treated as empty";
  Real h(unit = "m", start = h0, fixed = true) "Water level";
  Real q(unit = "m3/s") "Outflow";
  discrete Real tEmpty(unit = "s", start = 0, fixed = true) "Time the tank ran empty";
  Boolean empty(start = false, fixed = true);
equation
  q = if empty then 0 else a*sqrt(2*g*max(h, 0));
  A*der(h) = -q;
  when h <= hEps then
    empty = true;
    tEmpty = time;
    reinit(h, 0);
  end when;
  annotation(experiment(StopTime = 200));
end Tank;
