within Vehicle;
model LinearDrag "F = k*v"
  extends Drag;
  parameter Real k(unit = "N.s/m") = 10;
equation
  F = k*v;
end LinearDrag;
