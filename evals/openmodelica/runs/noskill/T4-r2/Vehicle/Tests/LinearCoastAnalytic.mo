within Vehicle.Tests;
model LinearCoastAnalytic "Check linear coast against v(t) = v0*exp(-k*t/m)"
  extends Vehicle.Examples.CoastLinear;
  Modelica.Units.SI.Velocity vExact = car.v0*exp(-car.drag.k*time/car.m) "Analytic velocity";
  parameter Real tol = 1e-3 "Relative tolerance";
equation
  assert(abs(car.v - vExact) <= tol*car.v0, "Linear coast deviates from analytic solution");
  when terminal() then
    assert(abs(car.v - car.v0*exp(-1)) <= tol*car.v0, "v(100 s) should be 30*exp(-1) = 11.04 m/s");
  end when;
end LinearCoastAnalytic;
