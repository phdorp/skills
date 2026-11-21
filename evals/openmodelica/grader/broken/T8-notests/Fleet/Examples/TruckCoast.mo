within Fleet.Examples;
model TruckCoast
  Coast coast(p = Truck());
  annotation(experiment(StopTime = 300));
end TruckCoast;
