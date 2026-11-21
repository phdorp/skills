within Fleet.Examples;
model CarCoast "Car coasting from 25 m/s"
  extends Modelica.Icons.Example;
  Fleet.Coast coast(redeclare Fleet.Car p);
  annotation(experiment(StopTime = 300));
end CarCoast;
