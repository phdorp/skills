within Vehicle.Examples;
model CoastQuadratic "Car coasting from 30 m/s against quadratic (aerodynamic) drag"
  Vehicle.Car car(redeclare Vehicle.QuadraticDrag drag);
  annotation(experiment(StopTime = 100));
end CoastQuadratic;
