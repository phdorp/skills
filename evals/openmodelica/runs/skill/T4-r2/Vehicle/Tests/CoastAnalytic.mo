within Vehicle.Tests;
model CoastAnalytic "Both example cars against the analytic solutions and the drag laws"
  // Linear:    m dv/dt = -k v    -> v(t) = v0 exp(-k t/m);      v(100) = 30/e = 11.0364 m/s
  // Quadratic: m dv/dt = -c v^2  -> v(t) = v0/(1 + c v0 t/m), c = 0.5*1.2*0.3*2 = 0.36 kg/m; v(100) = 14.4231 m/s
  Vehicle.Examples.CoastLinear lin;
  Vehicle.Examples.CoastQuadratic quad;
  Real vLinExact = 30*exp(-10*time/1000) "Analytic velocity, linear drag";
  Real vQuadExact = 30/(1 + 0.36*30*time/1000) "Analytic velocity, quadratic drag";
equation
  assert(abs(lin.car.drag.F - 10*lin.car.v) < 1e-9, "LinearDrag: F /= k*v");
  assert(abs(quad.car.drag.F - 0.36*quad.car.v^2) < 1e-9, "QuadraticDrag: F /= 0.5*rho*cd*A*v^2");
  assert(abs(lin.car.v - vLinExact) < 1e-3, "linear coast off the analytic solution: v = " + String(lin.car.v, significantDigits = 15));
  assert(abs(quad.car.v - vQuadExact) < 1e-3, "quadratic coast off the analytic solution: v = " + String(quad.car.v, significantDigits = 15));
  when initial() then
    assert(abs(quad.car.drag.F - 324) < 1e-6, "quadratic drag at 30 m/s should be 324 N: " + String(quad.car.drag.F, significantDigits = 15));
  end when;
  when terminal() then
    assert(abs(lin.car.v - 11.0363832351433) < 1e-3, "linear v(100) wrong: " + String(lin.car.v, significantDigits = 15));
    assert(abs(quad.car.v - 14.4230769230769) < 1e-3, "quadratic v(100) wrong: " + String(quad.car.v, significantDigits = 15));
    assert(quad.car.v > lin.car.v, "at 100 s the quadratic-drag car should be faster (its drag falls off faster)");
  end when;
  annotation(experiment(StopTime = 100));
end CoastAnalytic;
