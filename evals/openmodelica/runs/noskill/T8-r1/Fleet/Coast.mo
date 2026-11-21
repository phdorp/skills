within Fleet;
model Coast "Vehicle coasting to rest on a flat road"
  import SI = Modelica.Units.SI;
  replaceable parameter Fleet.Car p constrainedby Fleet.Params "Vehicle parameter set";
  parameter SI.Velocity v0 = 25 "Initial velocity";
  parameter SI.Density rho = 1.2 "Air density";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";
  SI.Velocity v(start = v0, fixed = true) "Vehicle velocity";
  Boolean stopped(start = false, fixed = true) "True once the vehicle has come to rest";
  discrete SI.Time tStop(start = 0, fixed = true) "Time the vehicle stopped (0 until then)";
equation
  p.m*der(v) = if stopped then 0 else -(0.5*rho*p.cdA*v^2 + p.cr*p.m*g);
  when v <= 0 then
    stopped = true;
    tStop = time;
    reinit(v, 0);
  end when;
  annotation(Documentation(info = "<html><p>Coasting vehicle with aerodynamic drag and rolling resistance.
Once the velocity reaches zero the vehicle stays at rest; <code>tStop</code> records that time.</p></html>"));
end Coast;
