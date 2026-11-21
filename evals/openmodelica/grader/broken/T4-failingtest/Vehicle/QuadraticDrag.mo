within Vehicle;
model QuadraticDrag "F = 0.5*rho*cd*A*v^2"
  extends Drag;
  parameter Real rho(unit = "kg/m3") = 1.2;
  parameter Real cd = 0.3;
  parameter Real A(unit = "m2") = 2;
equation
  F = 0.5*rho*cd*A*v*abs(v);
end QuadraticDrag;
