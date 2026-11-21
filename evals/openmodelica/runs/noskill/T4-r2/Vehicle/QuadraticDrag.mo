within Vehicle;
model QuadraticDrag "Aerodynamic drag F = 0.5*rho*cd*A*v^2"
  extends Vehicle.Drag;
  parameter Modelica.Units.SI.Density rho = 1.2 "Air density";
  parameter Real cd = 0.3 "Drag coefficient";
  parameter Modelica.Units.SI.Area A = 2 "Frontal area";
equation
  F = 0.5*rho*cd*A*v^2;
end QuadraticDrag;
