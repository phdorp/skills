within Fleet.Tests;
model CarStop "Car coasting from 25 m/s: analytic tStop = 174.1191743 s, distance = 1781.008106 m, v(30 s) = 17.95484754 m/s"
  Fleet.Coast coast(redeclare parameter Fleet.Car p);
  parameter Real tStopExp = 174.1191743 "Analytic stop time, s";
  parameter Real sExp = 1781.008106 "Analytic stopping distance, m";
  parameter Real v30Exp = 17.95484754 "Analytic velocity at 30 s, m/s";
equation
  assert(coast.v > -1e-6, "the vehicle rolls backwards: v = " + String(coast.v, significantDigits = 15));
  assert(coast.stopped or abs(coast.tStop) < 1e-12, "tStop should be 0 before the stop: " + String(coast.tStop, significantDigits = 15));
  when time >= 30 then
    assert(abs(coast.v - v30Exp) < 1e-3, "v(30) wrong: " + String(coast.v, significantDigits = 15));
  end when;
  when terminal() then
    assert(coast.stopped, "the vehicle should have stopped");
    assert(abs(coast.tStop - tStopExp) < 1e-2, "tStop wrong: " + String(coast.tStop, significantDigits = 15));
    assert(abs(coast.s - sExp) < 1e-2, "stopping distance wrong: " + String(coast.s, significantDigits = 15));
    assert(abs(coast.v) < 1e-9, "the vehicle should be at rest: v = " + String(coast.v, significantDigits = 15));
  end when;
  annotation(experiment(StopTime = 300, Tolerance = 1e-8));
end CarStop;
