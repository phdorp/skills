within Fleet.Tests;
model StopTimes "Compare both stop times with t = atan(v0*sqrt(a/b))/sqrt(a*b)"
  Examples.CarCoast car;
  Examples.TruckCoast truck;
  function stopTime
    input Params p;
    input Real rho;
    input Real g;
    input Real v0;
    output Real t;
  protected
    Real a = rho*p.cdA/(2*p.m);
    Real b = p.cr*g;
  algorithm
    t := atan(v0*sqrt(a/b))/sqrt(a*b);
  end stopTime;
equation
  when terminal() then
    assert(abs(car.coast.tStop - stopTime(car.coast.p, car.coast.rho, car.coast.g, car.coast.v0)) < 0.1, "car stop time deviates");
    assert(abs(truck.coast.tStop - stopTime(truck.coast.p, truck.coast.rho, truck.coast.g, truck.coast.v0)) < 0.1, "truck stop time deviates");
  end when;
  assert(car.coast.v >= -1e-6 and truck.coast.v >= -1e-6, "vehicle rolls backwards");
  annotation(experiment(StopTime = 300));
end StopTimes;
