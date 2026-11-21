within Vehicle.Tests;
model QuadraticDecay "Compare with v = v0/(1 + b*v0*t/m)"
  extends Examples.CoastQuadratic;
  final parameter Real b = 0.5*car.drag.rho*car.drag.cd*car.drag.A;
equation
  assert(abs(car.v - car.v0/(1 + b*car.v0*time/car.m)) < 1e-3, "quadratic coast deviates from analytic solution");
  annotation(experiment(StopTime = 100));
end QuadraticDecay;
