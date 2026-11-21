within Vehicle.Tests;
model LinearDecay "Compare with v = v0*exp(-k*t/m)"
  extends Examples.CoastLinear;
equation
  assert(abs(car.v - car.v0*exp(-2*car.drag.k*time/car.m)) < 1e-3, "linear coast deviates from analytic solution");
  annotation(experiment(StopTime = 100));
end LinearDecay;
