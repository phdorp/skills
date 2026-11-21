within Vehicle;
model QuadraticDrag "Plug-compatible with Drag, but does not extend it"
  input Real v(unit = "m/s");
  output Real F(unit = "N");
  parameter Real rho(unit = "kg/m3") = 1.2;
  parameter Real cd = 0.3;
  parameter Real A(unit = "m2") = 2;
equation
  F = 0.5*rho*cd*A*v*abs(v);
end QuadraticDrag;
