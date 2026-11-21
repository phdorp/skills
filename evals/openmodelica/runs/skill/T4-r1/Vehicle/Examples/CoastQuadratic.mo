within Vehicle.Examples;
model CoastQuadratic "Car coasting from 30 m/s with quadratic (aerodynamic) drag"
  Vehicle.Car car(redeclare Vehicle.QuadraticDrag drag);
  annotation(experiment(StopTime = 100));
end CoastQuadratic;
