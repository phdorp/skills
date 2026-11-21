within Vehicle.Tests;
model LinearAnalytic "Linear drag: v(t) = v0*exp(-k/m*t)"
  extends Vehicle.Examples.CoastLinear;
  Real vExact = car.v0*exp(-car.drag.k/car.m*time) "Analytic solution";
equation
  assert(abs(car.v - vExact) < 1e-3, "Linear drag velocity deviates from analytic solution");
  when terminal() then
    assert(abs(car.v - 30*exp(-1)) < 1e-3, "Final velocity is not 30*exp(-1) m/s");
  end when;
  annotation(experiment(StopTime = 100));
end LinearAnalytic;
