within Vehicle.Examples;
model CoastLinear "Car coasting with linear drag"
  extends Modelica.Icons.Example;
  Vehicle.Car car(redeclare Vehicle.LinearDrag drag);
  annotation(experiment(StopTime = 100));
end CoastLinear;
