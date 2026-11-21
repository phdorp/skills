within Vehicle.Examples;
model CoastQuadratic
  Car car(redeclare QuadraticDrag drag);
  annotation(experiment(StopTime = 100));
end CoastQuadratic;
