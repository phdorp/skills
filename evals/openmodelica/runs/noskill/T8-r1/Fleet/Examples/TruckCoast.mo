within Fleet.Examples;
model TruckCoast "Truck coasting from 25 m/s"
  extends Modelica.Icons.Example;
  Fleet.Coast coast(redeclare Fleet.Truck p);
  annotation(experiment(StopTime = 300));
end TruckCoast;
