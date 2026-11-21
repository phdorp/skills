within Fleet.Tests;
model CarStopTime "Car stops at the analytic time and stays at rest"
  extends CoastStopTime(redeclare Fleet.Coast coast(redeclare Fleet.Car p));
  annotation(experiment(StopTime = 300));
end CarStopTime;
