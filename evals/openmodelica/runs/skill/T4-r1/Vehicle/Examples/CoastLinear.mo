within Vehicle.Examples;
model CoastLinear "Car coasting from 30 m/s with linear drag"
  Vehicle.Car car(redeclare Vehicle.LinearDrag drag);
  annotation(experiment(StopTime = 100));
end CoastLinear;
