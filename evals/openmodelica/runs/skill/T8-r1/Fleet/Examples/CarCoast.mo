within Fleet.Examples;
model CarCoast "A car coasting from 25 m/s"
  Fleet.Coast coast(redeclare parameter Fleet.Car p);
  annotation(experiment(StopTime = 300));
end CarCoast;
