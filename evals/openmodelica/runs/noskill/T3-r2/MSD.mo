model MSD "Mass-spring-damper: spring and damper in parallel between a fixed point and a 1 kg mass"
  import Modelica.Units.SI;
  parameter SI.TranslationalSpringConstant c = 100 "Spring constant";
  parameter SI.TranslationalDampingConstant d = 2 "Damping constant";
  parameter SI.Mass m = 1 "Mass";
  parameter SI.Position x0 = 0.1 "Initial displacement from the spring's rest position";

  Modelica.Mechanics.Translational.Components.Fixed fixed(s0 = 0)
    annotation(Placement(transformation(extent = {{-90, -10}, {-70, 10}})));
  Modelica.Mechanics.Translational.Components.Spring spring(c = c, s_rel0 = 0)
    annotation(Placement(transformation(extent = {{-40, 10}, {-20, 30}})));
  Modelica.Mechanics.Translational.Components.Damper damper(d = d)
    annotation(Placement(transformation(extent = {{-40, -30}, {-20, -10}})));
  Modelica.Mechanics.Translational.Components.Mass mass(
    m = m, L = 0,
    s(start = fixed.s0 + spring.s_rel0 + x0, fixed = true),
    v(start = 0, fixed = true))
    annotation(Placement(transformation(extent = {{20, -10}, {40, 10}})));

  SI.Position x "Displacement of the mass from the spring's rest position";
equation
  x = mass.s - fixed.s0 - spring.s_rel0;
  connect(fixed.flange, spring.flange_a);
  connect(fixed.flange, damper.flange_a);
  connect(spring.flange_b, mass.flange_a);
  connect(damper.flange_b, mass.flange_a);
  annotation(experiment(StartTime = 0, StopTime = 3, Interval = 0.001, Tolerance = 1e-8));
end MSD;
