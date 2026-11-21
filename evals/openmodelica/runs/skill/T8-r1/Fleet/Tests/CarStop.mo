within Fleet.Tests;
model CarStop "Car from 25 m/s: a = 3e-4, b = 0.0981; tStop = atan(v0 sqrt(a/b))/sqrt(a b) = 174.1192 s, x = ln(1 + a v0^2/b)/(2 a) = 1781.008 m"
  Fleet.Coast coast(redeclare parameter Fleet.Car p);
equation
  assert(coast.v >= -1e-6, "the car rolls backwards: v = " + String(coast.v, significantDigits = 15));
  when time >= 100 then
    assert(abs(coast.tStop) < 1e-12 and not coast.stopped, "tStop should be 0 while moving, got " + String(coast.tStop, significantDigits = 15));
  end when;
  when terminal() then
    assert(abs(coast.tStop - 174.1192) < 0.01, "stop time wrong: " + String(coast.tStop, significantDigits = 15));
    assert(abs(coast.x - 1781.008) < 0.1, "stopping distance wrong: " + String(coast.x, significantDigits = 15));
    assert(coast.stopped and abs(coast.v) < 1e-12, "the car should be at rest: v = " + String(coast.v, significantDigits = 15));
  end when;
  annotation(experiment(StopTime = 300, Tolerance = 1e-8));
end CarStop;
