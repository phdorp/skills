within Vehicle;
model Car "Car coasting without drive force, with exchangeable drag"
  parameter Modelica.Units.SI.Mass m = 1000 "Vehicle mass";
  parameter Modelica.Units.SI.Velocity v0 = 30 "Initial velocity";
  Modelica.Units.SI.Velocity v(start = v0, fixed = true) "Vehicle velocity";
  replaceable Vehicle.LinearDrag drag constrainedby Vehicle.Drag "Drag model";
equation
  drag.v = v;
  m*der(v) = -drag.F;
end Car;
