model Robertson "Robertson's stiff chemical reaction system"
  Real y1(start = 1, fixed = true) "Concentration of species 1";
  Real y2(start = 0, fixed = true) "Concentration of species 2";
  Real y3(start = 0, fixed = true) "Concentration of species 3";
equation
  der(y1) = -0.04*y1 + 1e4*y2*y3;
  der(y2) = 0.04*y1 - 1e4*y2*y3 - 3e7*y2^2;
  der(y3) = 3e7*y2^2;
  // gbode method radauIIA3 = 3-stage Radau IIA, order 5 (OpenModelica numbers Radau methods by stages).
  annotation(
    experiment(StartTime = 0, StopTime = 40, Tolerance = 1e-8),
    __OpenModelica_simulationFlags(s = "gbode", gbm = "radauIIA3"));
end Robertson;
