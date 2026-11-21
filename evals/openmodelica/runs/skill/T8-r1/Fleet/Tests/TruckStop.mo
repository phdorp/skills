within Fleet.Tests;
model TruckStop "Truck from 25 m/s: a = 3e-4, b = 0.06867; tStop = 226.1768 s, x = 2194.215 m"
  Fleet.Coast coast(redeclare parameter Fleet.Truck p);
equation
  assert(coast.v >= -1e-6, "the truck rolls backwards: v = " + String(coast.v, significantDigits = 15));
  when terminal() then
    assert(abs(coast.tStop - 226.1768) < 0.01, "stop time wrong: " + String(coast.tStop, significantDigits = 15));
    assert(abs(coast.x - 2194.215) < 0.1, "stopping distance wrong: " + String(coast.x, significantDigits = 15));
    assert(coast.stopped and abs(coast.v) < 1e-12, "the truck should be at rest: v = " + String(coast.v, significantDigits = 15));
    assert(abs(coast.p.m - 12000) < 1e-9, "truck record not used: m = " + String(coast.p.m));
  end when;
  annotation(experiment(StopTime = 300, Tolerance = 1e-8));
end TruckStop;
