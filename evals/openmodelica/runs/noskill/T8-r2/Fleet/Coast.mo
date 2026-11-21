within Fleet;
model Coast "Vehicle coasting on a flat road until it stops"
  replaceable parameter Fleet.Car p constrainedby Fleet.Params
    "Vehicle parameter set";
  parameter Modelica.Units.SI.Velocity v0 = 25 "Initial velocity";
  parameter Modelica.Units.SI.Density rho = 1.2 "Air density";
  parameter Modelica.Units.SI.Acceleration g = 9.81 "Gravitational acceleration";
  Modelica.Units.SI.Velocity v(start = v0, fixed = true) "Vehicle velocity";
  Boolean stopped(start = false, fixed = true) "True once the vehicle has stopped";
  discrete Modelica.Units.SI.Time tStop(start = 0, fixed = true)
    "Time at which the vehicle stopped (0 until then)";
equation
  p.m*der(v) = if stopped then 0 else -(0.5*rho*p.cdA*v^2 + p.cr*p.m*g);
  when v <= 0 then
    stopped = true;
    tStop = time;
    reinit(v, 0);
  end when;
end Coast;
