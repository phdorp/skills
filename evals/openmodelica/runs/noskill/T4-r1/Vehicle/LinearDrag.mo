within Vehicle;
model LinearDrag "Linear (viscous) drag F = k*v"
  extends Vehicle.Drag;
  parameter Modelica.Units.SI.TranslationalDampingConstant k = 10 "Damping coefficient";
equation
  F = k*v;
end LinearDrag;
