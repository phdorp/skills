within Fleet.Examples;
model TruckCoast "Truck coasting from 25 m/s to rest"
  Fleet.Coast coast(redeclare parameter Fleet.Truck p);
  annotation(experiment(StopTime = 300));
end TruckCoast;
