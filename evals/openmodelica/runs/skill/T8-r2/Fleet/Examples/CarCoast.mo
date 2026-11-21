within Fleet.Examples;
model CarCoast "Car coasting from 25 m/s to rest"
  Fleet.Coast coast(redeclare parameter Fleet.Car p);
  annotation(experiment(StopTime = 300));
end CarCoast;
