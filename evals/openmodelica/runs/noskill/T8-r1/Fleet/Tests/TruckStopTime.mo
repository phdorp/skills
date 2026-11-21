within Fleet.Tests;
model TruckStopTime "Truck stops at the analytic time and stays at rest"
  extends CoastStopTime(redeclare Fleet.Coast coast(redeclare Fleet.Truck p));
  annotation(experiment(StopTime = 300));
end TruckStopTime;
