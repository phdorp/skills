model MSD "Mass-spring-damper: fixed point, spring and damper in parallel, 1 kg mass"
  import Modelica.Units.SI;
  Modelica.Mechanics.Translational.Components.Fixed fixed(s0 = 0) "Fixed point at s = 0";
  Modelica.Mechanics.Translational.Components.Spring spring(c = 100, s_rel0 = 0) "Spring, rest length 0";
  Modelica.Mechanics.Translational.Components.Damper damper(d = 2) "Damper parallel to the spring";
  Modelica.Mechanics.Translational.Components.Mass mass(
    m = 1,
    L = 0,
    s(start = 0.1, fixed = true),
    v(start = 0, fixed = true)) "Mass, starts at rest displaced 0.1 m";
  SI.Position x "Displacement of the mass from the spring's rest position";
equation
  connect(fixed.flange, spring.flange_a);
  connect(fixed.flange, damper.flange_a);
  connect(spring.flange_b, mass.flange_a);
  connect(damper.flange_b, mass.flange_a);
  x = mass.s;
  annotation(experiment(StopTime = 3));
end MSD;
