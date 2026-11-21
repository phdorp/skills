within Vehicle.Tests;
model QuadraticAnalytic "Quadratic drag: 1/v(t) = 1/v0 + c/m*t, c = 0.5*rho*cd*A"
  extends Vehicle.Examples.CoastQuadratic;
  parameter Real c = 0.5*car.drag.rho*car.drag.cd*car.drag.A "Lumped drag constant";
  Real vExact = 1/(1/car.v0 + c/car.m*time) "Analytic solution";
equation
  assert(abs(car.v - vExact) < 1e-3, "Quadratic drag velocity deviates from analytic solution");
  when terminal() then
    assert(abs(car.v - 1/(1/30 + 0.036)) < 1e-3, "Final velocity is not 1/(1/30+0.036) m/s");
  end when;
  annotation(experiment(StopTime = 100));
end QuadraticAnalytic;
