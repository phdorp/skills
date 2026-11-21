within Fleet.Tests;
partial model CoastStopTime "Compare the simulated stop time with the analytic solution"
  extends Modelica.Icons.Example;
  replaceable Fleet.Coast coast;
  parameter Modelica.Units.SI.Time tol = 0.1 "Allowed stop-time error";
  // m*dv/dt = -(a + b*v^2)*m  =>  t_stop = atan(v0*sqrt(b/a))/sqrt(a*b)
  final parameter Real a = coast.p.cr*coast.g;
  final parameter Real b = 0.5*coast.rho*coast.p.cdA/coast.p.m;
  final parameter Modelica.Units.SI.Time tExpected = atan(coast.v0*sqrt(b/a))/sqrt(a*b) "Analytic stop time";
equation
  assert(coast.v >= -1e-6, "Vehicle rolls backwards: v = " + String(coast.v));
  assert(time < tExpected + 1 or coast.stopped, "Vehicle has not stopped by t = " + String(time));
  assert(not coast.stopped or abs(coast.tStop - tExpected) < tol,
    "tStop = " + String(coast.tStop) + " differs from analytic " + String(tExpected));
  assert(not coast.stopped or abs(coast.v) < 1e-6, "Vehicle moves after stopping: v = " + String(coast.v));
  annotation(experiment(StopTime = 300));
end CoastStopTime;
