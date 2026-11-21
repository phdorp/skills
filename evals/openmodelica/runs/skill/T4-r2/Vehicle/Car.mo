within Vehicle;
model Car "A car coasting (no drive force) against an exchangeable drag"
  import Modelica.Units.SI;
  parameter SI.Mass m = 1000 "Mass of the car";
  parameter SI.Velocity v0 = 30 "Initial velocity";
  SI.Velocity v(start = v0, fixed = true) "Velocity";
  replaceable LinearDrag drag constrainedby Drag "Drag law";
equation
  drag.v = v;
  m*der(v) = -drag.F;
  annotation(experiment(StopTime = 100));
end Car;
