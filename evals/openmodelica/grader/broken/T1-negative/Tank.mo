model Tank "Naive Torricelli: outflow ignores the empty tank, level goes negative"
  parameter Real A = 2, a = 0.01, g = 9.81;
  Real h(start = 4, fixed = true);
  discrete Real tEmpty(start = 0, fixed = true);
equation
  A*der(h) = -a*sqrt(2*g*abs(h));
  when h <= 0 then
    tEmpty = time;
  end when;
  annotation(experiment(StopTime = 300));
end Tank;
