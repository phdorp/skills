within Vehicle.Examples;
model CoastLinear
  Car car(redeclare LinearDrag drag);
  annotation(experiment(StopTime = 100));
end CoastLinear;
