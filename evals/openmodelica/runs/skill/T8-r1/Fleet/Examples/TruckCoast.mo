within Fleet.Examples;
model TruckCoast "A truck coasting from 25 m/s"
  Fleet.Coast coast(redeclare parameter Fleet.Truck p);
  annotation(experiment(StopTime = 300));
end TruckCoast;
