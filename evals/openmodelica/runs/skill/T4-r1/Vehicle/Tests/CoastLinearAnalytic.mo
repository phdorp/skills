within Vehicle.Tests;
model CoastLinearAnalytic "Linear drag: v(t) = 30*exp(-k*t/m); v(100) = 30*exp(-1) = 11.0364 m/s"
  extends Vehicle.Examples.CoastLinear;
  Real vExact = car.v0*exp(-car.drag.k*time/car.m) "Analytic velocity";
equation
  assert(abs(car.v - vExact) < 1e-3, "v deviates from analytic solution: " + String(car.v, significantDigits = 15));
  when terminal() then
    assert(abs(car.v - 11.0364) < 1e-3, "v(100) wrong: " + String(car.v, significantDigits = 15));
  end when;
  annotation(experiment(StopTime = 100, Tolerance = 1e-8));
end CoastLinearAnalytic;
