within Vehicle.Tests;
model DragForces "Forces at v = 30 m/s: linear 10*30 = 300 N, quadratic 0.5*1.2*0.3*2*30^2 = 324 N"
  Vehicle.LinearDrag lin(v = 30);
  Vehicle.QuadraticDrag quad(v = 30);
  Vehicle.QuadraticDrag quadBack(v = -30) "negative velocity: force must also reverse";
equation
  assert(abs(lin.F - 300) < 1e-9, "LinearDrag F wrong: " + String(lin.F, significantDigits = 15));
  assert(abs(quad.F - 324) < 1e-9, "QuadraticDrag F wrong: " + String(quad.F, significantDigits = 15));
  assert(abs(quadBack.F + 324) < 1e-9, "QuadraticDrag should oppose motion: " + String(quadBack.F, significantDigits = 15));
  annotation(experiment(StopTime = 1));
end DragForces;
