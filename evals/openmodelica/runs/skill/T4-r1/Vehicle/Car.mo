within Vehicle;
model Car "A car coasting without drive force, slowed by an exchangeable drag model"
  import Modelica.Units.SI;
  parameter SI.Mass m = 1000 "Car mass";
  parameter SI.Velocity v0 = 30 "Initial velocity";
  SI.Velocity v(start = v0, fixed = true) "Car velocity";
  SI.Position x(start = 0, fixed = true) "Distance travelled";
  replaceable LinearDrag drag constrainedby Drag "Drag model; swap with redeclare";
equation
  drag.v = v "in the equation section: a modifier on drag would be lost on redeclare";
  der(x) = v;
  m*der(v) = -drag.F;
  annotation(experiment(StopTime = 100));
end Car;
