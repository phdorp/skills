model MSD "Mass-spring-damper from Modelica.Mechanics.Translational"
  import Modelica.Mechanics.Translational.Components;
  parameter Real s0(unit = "m") = 0.5 "Spring rest length";
  Components.Fixed fixed(s0 = 0);
  Components.Spring spring(c = 100, s_rel0 = s0);
  Components.Damper damper(d = 2);
  Components.Mass mass(m = 1, L = 0, s(start = s0 + 0.1, fixed = true), v(start = 0, fixed = true));
  Real x(unit = "m") = mass.s - fixed.s0 - s0 "Displacement from spring rest position";
equation
  connect(fixed.flange, spring.flange_a);
  connect(fixed.flange, damper.flange_a);
  connect(spring.flange_b, mass.flange_a);
  connect(damper.flange_b, mass.flange_a);
  annotation(experiment(StopTime = 3, Interval = 0.001));
end MSD;
