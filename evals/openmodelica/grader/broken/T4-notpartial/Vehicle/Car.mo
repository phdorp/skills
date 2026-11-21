within Vehicle;
model Car "Coasting car"
  parameter Real m(unit = "kg") = 1000;
  parameter Real v0(unit = "m/s") = 30;
  Real v(unit = "m/s", start = v0, fixed = true);
  replaceable LinearDrag drag constrainedby Drag;
equation
  drag.v = v;
  m*der(v) = -drag.F;
end Car;
