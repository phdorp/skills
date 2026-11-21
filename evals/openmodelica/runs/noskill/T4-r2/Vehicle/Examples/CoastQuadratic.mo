within Vehicle.Examples;
model CoastQuadratic "Car coasting with quadratic drag"
  extends Modelica.Icons.Example;
  Vehicle.Car car(redeclare Vehicle.QuadraticDrag drag);
  annotation(experiment(StopTime = 100));
end CoastQuadratic;
