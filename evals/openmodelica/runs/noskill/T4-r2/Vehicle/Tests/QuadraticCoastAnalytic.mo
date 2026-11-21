within Vehicle.Tests;
model QuadraticCoastAnalytic "Check quadratic coast against v(t) = v0/(1 + c*v0*t/m)"
  extends Vehicle.Examples.CoastQuadratic;
  final parameter Real c = 0.5*car.drag.rho*car.drag.cd*car.drag.A "Lumped drag constant";
  Modelica.Units.SI.Velocity vExact = car.v0/(1 + c*car.v0*time/car.m) "Analytic velocity";
  parameter Real tol = 1e-3 "Relative tolerance";
equation
  assert(abs(car.v - vExact) <= tol*car.v0, "Quadratic coast deviates from analytic solution");
  when terminal() then
    assert(abs(car.v - 30/2.08) <= tol*car.v0, "v(100 s) should be 30/2.08 = 14.42 m/s");
  end when;
end QuadraticCoastAnalytic;
