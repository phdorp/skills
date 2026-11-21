within Vehicle;
model LinearDrag "Linear drag: F = k*v"
  extends Drag;
  parameter Real k(unit = "N.s/m") = 10 "Linear drag coefficient";
equation
  F = k*v;
end LinearDrag;
