within Fleet.Tests;
model CarStopTime "Compare the Car stop time with the analytical solution and check it never rolls back"
  extends Fleet.Examples.CarCoast;
  final parameter Real a = 0.5*coast.rho*coast.p.cdA/coast.p.m "Drag term per unit v^2";
  final parameter Real b = coast.p.cr*coast.g "Rolling deceleration";
  final parameter Modelica.Units.SI.Time tExact =
    atan(coast.v0*sqrt(a/b))/sqrt(a*b) "Analytical stop time";
equation
  assert(coast.v >= -1e-6, "Vehicle rolls backwards");
  when terminal() then
    assert(coast.stopped, "Vehicle did not stop before the end of the run");
    assert(abs(coast.tStop - tExact) < 0.01,
      "Stop time " + String(coast.tStop) + " differs from analytical " + String(tExact));
    assert(abs(coast.v) < 1e-9, "Vehicle not at rest at the end");
  end when;
  annotation(experiment(StopTime = 300));
end CarStopTime;
