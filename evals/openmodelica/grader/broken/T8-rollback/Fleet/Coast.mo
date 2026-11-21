within Fleet;
model Coast "Vehicle coasting on a flat road until it stops"
  parameter Params p "Vehicle parameter set";
  parameter Real rho(unit = "kg/m3") = 1.2 "Air density";
  parameter Real g(unit = "m/s2") = 9.81;
  parameter Real v0(unit = "m/s") = 25 "Initial velocity";
  Real v(unit = "m/s", start = v0, fixed = true) "Velocity";
  discrete Real tStop(unit = "s", start = 0, fixed = true) "Time the vehicle stops";
equation
  p.m*der(v) = -(0.5*rho*p.cdA*v^2 + p.cr*p.m*g);
  when v <= 0 then
    tStop = time;
  end when;
end Coast;
