within Fleet.Examples;
model CarCoast "Car coasting from 25 m/s"
  Fleet.Coast coast(redeclare Fleet.Car p);
  annotation(experiment(StopTime = 300));
end CarCoast;
