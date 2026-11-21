within Fleet.Examples;
model TruckCoast "Truck coasting from 25 m/s"
  Fleet.Coast coast(redeclare Fleet.Truck p);
  annotation(experiment(StopTime = 300));
end TruckCoast;
