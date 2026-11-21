within Fleet;
model Coast "Vehicle coasting on a flat road until it stops; it then stays at rest"
  import Modelica.Units.SI;
  replaceable parameter Fleet.Car p constrainedby Fleet.Params "Vehicle parameter set";
  parameter SI.Density rho = 1.2 "Air density";
  parameter SI.Acceleration g = 9.81 "Gravitational acceleration";
  parameter SI.Velocity v0 = 25 "Initial velocity";
  SI.Velocity v(start = v0, fixed = true) "Velocity";
  SI.Length s(start = 0, fixed = true) "Distance travelled";
  Boolean stopped(start = false, fixed = true) "True once the vehicle has stopped";
  discrete SI.Time tStop(start = 0, fixed = true) "Time the vehicle stopped (0 until then)";
equation
  der(s) = v;
  p.m*der(v) = if stopped then 0 else -(0.5*rho*p.cdA*v^2 + p.cr*p.m*g);
  when v <= 0 then
    stopped = true;
    tStop = time;
    reinit(v, 0);
  end when;
  annotation(experiment(StopTime = 300));
end Coast;
