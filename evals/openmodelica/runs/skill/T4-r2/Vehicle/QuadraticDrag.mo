within Vehicle;
model QuadraticDrag "Aerodynamic drag: F = 0.5*rho*cd*A*v^2"
  extends Drag;
  import Modelica.Units.SI;
  parameter SI.Density rho = 1.2 "Air density";
  parameter Real cd = 0.3 "Drag coefficient";
  parameter SI.Area A = 2 "Frontal area";
equation
  F = 0.5*rho*cd*A*v*abs(v) "v*abs(v) = v^2 for v >= 0 and keeps opposing motion for v < 0";
end QuadraticDrag;
