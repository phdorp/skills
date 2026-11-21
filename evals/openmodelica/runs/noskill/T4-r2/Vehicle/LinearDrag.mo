within Vehicle;
model LinearDrag "Viscous drag F = k*v"
  extends Vehicle.Drag;
  parameter Modelica.Units.SI.TranslationalDampingConstant k = 10 "Drag coefficient";
equation
  F = k*v;
end LinearDrag;
