within Vehicle.Tests;
model CoastQuadraticAnalytic "Quadratic drag, c = 0.36: 1/v = 1/30 + c*t/m; v(100) = 14.4231 m/s, x(100) = 2034.355 m"
  extends Vehicle.Examples.CoastQuadratic;
  Real c = 0.5*car.drag.rho*car.drag.cd*car.drag.A;
  Real vExact = 1/(1/car.v0 + c*time/car.m) "Analytic velocity";
equation
  assert(abs(car.v - vExact) < 1e-3, "v deviates from analytic solution: " + String(car.v, significantDigits = 15));
  when terminal() then
    assert(abs(car.v - 14.4231) < 1e-3, "v(100) wrong: " + String(car.v, significantDigits = 15));
    assert(abs(car.x - 2034.355) < 0.01, "x(100) wrong: " + String(car.x, significantDigits = 15));
    assert(car.v > 0 and car.v < car.v0, "car should slow down but not reverse");
  end when;
  annotation(experiment(StopTime = 100, Tolerance = 1e-8));
end CoastQuadraticAnalytic;
